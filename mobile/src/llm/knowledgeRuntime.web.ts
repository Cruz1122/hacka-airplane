// Browser build of the knowledge runtime: the same e5 GGUF on wllama (llama.cpp in WebAssembly)
// and the index vectors, both fetched from the dev server (metro.config.js serves models/knowledge
// at /knowledge-files/). No ONNX scorer: the engine's JS dot-product loop runs, fast under V8's JIT.
// Laya stays off, as on the phone.
import { Wllama } from '@wllama/wllama';

import { KnowledgeEngine } from '@/core/knowledge';

import { knowledgeAssets, type KnowledgeRuntime } from './knowledgeAssets';

export { degradedKnowledgeEngine, knowledgeAssets, type KnowledgeRuntime } from './knowledgeAssets';

// Must equal the manifest prefix: index vectors were built with it on every text.
const E5_PREFIX = 'query: ';
const FILES = '/knowledge-files/';

async function fetchChecked(name: string, expectedBytes: number): Promise<ArrayBuffer> {
  const res = await fetch(FILES + name);
  if (!res.ok) {
    throw new Error(
      `${name}: HTTP ${res.status}; put the model files in models/knowledge (README)`,
    );
  }
  const buf = await res.arrayBuffer();
  if (buf.byteLength !== expectedBytes) {
    throw new Error(`${name}: ${buf.byteLength} bytes, manifest says ${expectedBytes}`);
  }
  return buf;
}

export async function loadKnowledgeRuntime(): Promise<KnowledgeRuntime> {
  const t0 = performance.now();
  const m = knowledgeAssets.manifest;
  const emb = m.embedder as { file: string; bytes: number };
  const wllama = new Wllama({ default: `${FILES}wllama.wasm` }, { suppressNativeLog: true });
  const [gguf, vectors] = await Promise.all([
    fetchChecked(emb.file, emb.bytes),
    fetchChecked(m.vectors.file, m.vectors.bytes),
  ]);
  // Same context as the phone (src/llm/embedder.ts): non-causal BERT, one ubatch per query.
  await wllama.loadModel([new Blob([gguf])], {
    embeddings: true,
    pooling_type: 'mean',
    n_ctx: 512,
    n_batch: 512,
    n_ubatch: 512,
  });
  const embed = async (text: string) => {
    const out = await wllama.createEmbedding({ input: E5_PREFIX + text, embd_normalize: 2 });
    const v = out.data[0]?.embedding;
    if (!Array.isArray(v)) throw new Error('wllama returned no float embedding');
    return Float32Array.from(v);
  };
  const engine = new KnowledgeEngine(knowledgeAssets, new Float32Array(vectors), embed);
  return { engine, loadMs: performance.now() - t0, release: () => wllama.exit() };
}
