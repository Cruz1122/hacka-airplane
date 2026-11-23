// Builds the on-device KnowledgeEngine: bundled JSON assets + side-loaded e5 GGUF, index vectors and
// ONNX scorer (scripts/push-knowledge.sh). Laya stays off until policy.laya.enabled (docs/history/phase3-architecture.md §1.4).
import catalog from '@/../assets/data/knowledge/catalog.json';
import manifest from '@/../assets/data/knowledge/index.json';
import policy from '@/../assets/data/knowledge/policy.json';
import sections from '@/../assets/data/knowledge/sections.json';
import { KnowledgeEngine, type KnowledgeAssets } from '@/core/knowledge';

import { loadEmbedder, loadVectors } from './embedder';
import { loadScorer } from './scorer';

export const knowledgeAssets = { catalog, sections, policy, manifest } as unknown as KnowledgeAssets;

export interface KnowledgeRuntime {
  engine: KnowledgeEngine;
  loadMs: number;
  release(): Promise<void>;
}

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
  const engine = new KnowledgeEngine(knowledgeAssets, vectors, (t) => embedder.embed(t), undefined, score);
  return { engine, loadMs: performance.now() - t0, release: () => embedder.release() };
}

/**
 * Engine for when the side-loaded files are missing or fail to load: the safety rules still run
 * (urgent banner + curated emergency menu need no model); any other question raises
 * KnowledgeEngineError, which the chat shows as an error row.
 */
export function degradedKnowledgeEngine(cause: unknown): KnowledgeEngine {
  const m = knowledgeAssets.manifest;
  const zeros = new Float32Array(m.rows * m.dims);
  return new KnowledgeEngine(knowledgeAssets, zeros, () => Promise.reject(cause));
}
