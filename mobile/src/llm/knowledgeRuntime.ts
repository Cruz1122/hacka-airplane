// Builds the on-device KnowledgeEngine: bundled JSON assets + side-loaded e5 GGUF, index vectors and
// ONNX scorer (scripts/push-knowledge.sh), plus the Laya reorderer when policy.laya.enabled
// (docs/history/phase3-architecture.md §1.4). The browser build resolves knowledgeRuntime.web.ts.
import type { InferenceSession } from 'onnxruntime-react-native';

import { KnowledgeEngine } from '@/core/knowledge';

import { loadEmbedder, loadVectors } from './embedder';
import { knowledgeAssets, restoreKnowledgePatches, type KnowledgeRuntime } from './knowledgeAssets';
import { layaReranker, openLayaSession } from './laya';
import { loadScorer } from './scorer';

export { degradedKnowledgeEngine, knowledgeAssets, type KnowledgeRuntime } from './knowledgeAssets';

/** Laya is optional: a failed load leaves the engine on its retrieval order instead of degrading it. */
async function loadLaya(): Promise<InferenceSession | undefined> {
  const laya = knowledgeAssets.policy.laya;
  if (!laya.enabled) return undefined;
  try {
    return await openLayaSession(laya.model);
  } catch (cause) {
    console.warn('Laya reorderer failed to load; answering without it.', cause);
    return undefined;
  }
}

export async function loadKnowledgeRuntime(): Promise<KnowledgeRuntime> {
  const t0 = performance.now();
  const m = knowledgeAssets.manifest;
  const emb = m.embedder as { file: string; bytes: number };
  const [embedder, vectors, score, laya] = await Promise.all([
    loadEmbedder(emb.file, emb.bytes),
    loadVectors(m.vectors.file, m.vectors.bytes),
    // Without a scorer the engine falls back to the JS loop (~0.46 s per query in Hermes).
    m.scorer ? loadScorer(m.scorer.file, m.scorer.bytes, m.scorer) : Promise.resolve(undefined),
    loadLaya(),
  ]);
  const labels = new Map(knowledgeAssets.catalog.map((e) => [e.id, e.label]));
  const engine = new KnowledgeEngine(
    knowledgeAssets,
    vectors,
    (t) => embedder.embed(t),
    laya && layaReranker(laya, (id) => labels.get(id) ?? id),
    score,
  );
  await restoreKnowledgePatches(engine);
  return {
    engine,
    loadMs: performance.now() - t0,
    release: async () => {
      await Promise.all([embedder.release(), laya?.release()]);
    },
  };
}
