// Test-only loaders (node:fs). Never import this from app code.
import { createHash } from 'node:crypto';
import { existsSync, readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';

import type { KnowledgeAssets } from '../assets';

const MOBILE = resolve(__dirname, '..', '..', '..', '..');
const REPO = resolve(MOBILE, '..');
const EXPORTER =
  'cd experiments/laya && uv run python ../nlu/export_nlu.py --gguf ../../models/knowledge/e5-nlu-ft4-f16.gguf --T 0.5 --w 5.0 --max-words 5 --below 0.7 --cue';

// Read with fs, not import: tsc would otherwise infer types for MBs of JSON.
export const readJson = <T>(path: string): T => JSON.parse(readFileSync(path, 'utf8')) as T;
export const fixture = <T>(name: string): T => readJson<T>(join(__dirname, name));

export function loadAssets(): KnowledgeAssets {
  const dir = join(MOBILE, 'assets', 'data', 'knowledge');
  return {
    catalog: readJson(join(dir, 'catalog.json')),
    sections: readJson(join(dir, 'sections.json')),
    policy: readJson(join(dir, 'policy.json')),
    manifest: readJson(join(dir, 'index.json')),
  };
}

export const VECTORS_PATH =
  process.env.KNOWLEDGE_VECTORS ?? join(REPO, 'models', 'knowledge', 'index.f32.bin');

/** The side-loaded index vectors; throws with the regenerate command when missing or stale. */
export function loadVectors(expectedSha256: string): Float32Array {
  if (!existsSync(VECTORS_PATH)) {
    throw new Error(`Missing ${VECTORS_PATH}. Regenerate it from the repo root: ${EXPORTER}`);
  }
  const buf = readFileSync(VECTORS_PATH);
  const sha = createHash('sha256').update(buf).digest('hex');
  if (sha !== expectedSha256) {
    throw new Error(
      `${VECTORS_PATH} sha256 ${sha} does not match the fixture (${expectedSha256}). Regenerate both: ${EXPORTER}`,
    );
  }
  // Copy into an aligned buffer: Buffer slices of the fs pool need not be 4-byte aligned.
  const bytes = new Uint8Array(buf.length);
  bytes.set(buf);
  return new Float32Array(bytes.buffer);
}
