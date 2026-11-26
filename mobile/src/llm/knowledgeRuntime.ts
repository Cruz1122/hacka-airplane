// Builds the on-device KnowledgeEngine: bundled JSON assets + side-loaded e5 GGUF, index vectors and
// ONNX scorer (scripts/push-knowledge.sh). Laya stays off until policy.laya.enabled (docs/history/phase3-architecture.md §1.4).
// The browser build resolves knowledgeRuntime.web.ts instead.
import { KnowledgeEngine } from '@/core/knowledge';

import { loadEmbedder, loadVectors } from './embedder';
import { knowledgeAssets, type KnowledgeRuntime } from './knowledgeAssets';
import { loadScorer } from './scorer';

export { degradedKnowledgeEngine, knowledgeAssets, type KnowledgeRuntime } from './knowledgeAssets';

export async function loadKnowledgeRuntime(): Promise<KnowledgeRuntime> {
  const t0 = performance.now();
  const m = knowledgeAssets.manifest;
  const emb = m.embedder as { file: string; bytes: number };
  const [embedder, vectors, score] = await Promise.all([
    loadEmbedder(emb.file, emb.bytes),
    loadVectors(m.vectors.file, m.vectors.bytes),
    // Without a scorer the engine falls back to the JS loop (~0.46 s per query in Hermes).
    m.scorer ? loadScorer(m.scorer.file, m.scorer.bytes, m.scorer) : Promise.resolve(undefined),
  ]);
  const engine = new KnowledgeEngine(
    knowledgeAssets,
    vectors,
    (t) => embedder.embed(t),
    undefined,
    score,
  );
  return { engine, loadMs: performance.now() - t0, release: () => embedder.release() };
}
