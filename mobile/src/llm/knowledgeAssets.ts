// The bundled knowledge assets and the no-model fallback engine, shared by the native and the web
// runtime (knowledgeRuntime.ts, knowledgeRuntime.web.ts).
import catalog from '@/../assets/data/knowledge/catalog.json';
import manifest from '@/../assets/data/knowledge/index.json';
import policy from '@/../assets/data/knowledge/policy.json';
import sections from '@/../assets/data/knowledge/sections.json';
import { KnowledgeEngine, type KnowledgeAssets } from '@/core/knowledge';

export const knowledgeAssets = {
  catalog,
  sections,
  policy,
  manifest,
} as unknown as KnowledgeAssets;

export interface KnowledgeRuntime {
  engine: KnowledgeEngine;
  loadMs: number;
  release(): Promise<void>;
}

/**
 * Engine for when the model files are missing or fail to load: the safety rules still run
 * (urgent banner + curated emergency menu need no model); any other question raises
 * KnowledgeEngineError, which the chat shows as an error row.
 */
export function degradedKnowledgeEngine(cause: unknown): KnowledgeEngine {
  const m = knowledgeAssets.manifest;
  const zeros = new Float32Array(m.rows * m.dims);
  return new KnowledgeEngine(knowledgeAssets, zeros, () => Promise.reject(cause));
}
