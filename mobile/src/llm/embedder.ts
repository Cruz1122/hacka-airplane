// e5-base query embedder: its own llama.rn context, never through ModelManager (which keeps one
// context and releases it before every load). Design: docs/history/phase3-architecture.md §2, fix 5.
import { Directory, File, Paths } from 'expo-file-system';
import { initLlama, type LlamaContext } from 'llama.rn';

// Must equal the manifest prefix: index vectors were built with it on every text.
export const E5_PREFIX = 'query: ';

const CONTEXT_PARAMS = {
  embedding: true,
  pooling_type: 'mean',
  n_ctx: 512,
  n_batch: 512,
  n_ubatch: 512, // non-causal BERT: the whole query must fit in one ubatch
  n_threads: 4, // measured on the Moto: 264 ms/query with 4 threads vs 499 ms with 2 (spike-e5)
  n_gpu_layers: 0,
} as const;

export interface Embedder {
  embed(text: string): Promise<Float32Array>;
  release(): Promise<void>;
}

function toNativePath(uri: string): string {
  return uri.replace(/^file:\/\//, '');
}

/** Side-loaded files live in the app files dir (scripts/push-knowledge.sh). */
export function findSideLoaded(name: string): File | null {
  const hit = new Directory(Paths.document).list().find((f) => !(f instanceof Directory) && f.name === name);
  return hit instanceof File ? hit : null;
}

export async function loadEmbedder(ggufName: string, expectedBytes: number): Promise<Embedder> {
  const file = findSideLoaded(ggufName);
  if (!file) throw new Error(`embedder ${ggufName} not found in app files; run scripts/push-knowledge.sh`);
  // Name + size check only: hashing ~300 MB in JS would take seconds (design §3.1).
  if (file.size !== expectedBytes) {
    throw new Error(`embedder ${ggufName}: ${file.size} bytes, manifest says ${expectedBytes}`);
  }
  const ctx: LlamaContext = await initLlama({ model: toNativePath(file.uri), ...CONTEXT_PARAMS });
  // Use the slot (parallel) path, not ctx.embedding(): in llama.rn 0.12.9 the direct path reuses the
  // previous prompt's common prefix, so every call after the first pools over a partial sequence
  // (cosine 0.94-0.99 vs the laptop GGUF on the Moto). The slot path matched 10/10 at 1.0000.
  await ctx.parallel.enable({ n_parallel: 1, n_batch: CONTEXT_PARAMS.n_batch });
  return {
    async embed(text: string) {
      const { promise } = await ctx.parallel.embedding(E5_PREFIX + text, { embd_normalize: 2 });
      return Float32Array.from((await promise).embedding);
    },
    release: () => ctx.release(),
  };
}

/** Reads the side-loaded float32 index into memory once. */
export async function loadVectors(name: string, expectedBytes: number): Promise<Float32Array> {
  const file = findSideLoaded(name);
  if (!file) throw new Error(`index ${name} not found in app files; run scripts/push-knowledge.sh`);
  if (file.size !== expectedBytes) throw new Error(`index ${name}: ${file.size} bytes, manifest says ${expectedBytes}`);
  return new Float32Array(await file.arrayBuffer());
}
