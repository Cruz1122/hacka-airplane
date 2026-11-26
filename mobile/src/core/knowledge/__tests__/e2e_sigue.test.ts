// Runs __fixtures__/e2e_sigue.ts (documented in research_notes/depth_v1/tools/e2e_sigue.ts) on the real assets. Skips (and says so) while
// depth.json does not exist; report-only unless E2E_SIGUE_STRICT=1.
import { existsSync } from 'node:fs';
import { join } from 'node:path';

import { e2ePasses, formatReport, runE2e } from '../__fixtures__/e2e_sigue';
import type { DepthEntry, DepthText, KnowledgeContinuation, KnowledgeDepth } from '../assets';
import { fixture, loadAssets, loadVectors, readJson } from '../__fixtures__/load';

const depthPath = join(
  __dirname,
  '..',
  '..',
  '..',
  '..',
  'assets',
  'data',
  'knowledge',
  'depth.json',
);
const assets = loadAssets();
const ready = existsSync(depthPath) && assets.policy.continuation != null;

(ready ? test : test.skip)(
  'e2e sigue x4, same question x8, partial disclosure (real engine, real depth.json)',
  async () => {
    const vectors = loadVectors(
      fixture<{ vectors_sha256: string }>('retrieval.json').vectors_sha256,
    );
    const depth = readJson<KnowledgeDepth>(depthPath);
    const report = await runE2e({ assets: { ...assets, depth }, vectors });
    console.log(formatReport(report));
    if (process.env.E2E_SIGUE_STRICT === '1') expect(e2ePasses(report)).toBe(true);
  },
  600_000,
);

if (!ready) {
  test('e2e sigue skipped: no depth.json / policy.continuation yet', () => {
    console.log(
      'e2e_sigue: SKIPPED. mobile/assets/data/knowledge/depth.json (and policy.continuation) do not exist; ' +
        'export_nlu.py emits them once data/knowledge/app/{depth_replies,reply_variants,fact_inventory}.json exist.',
    );
  });
}

// The harness itself, on generated depth data for 40 real entries (real catalog and vectors).
describe('e2e_sigue harness', () => {
  const T = (text: string, ...atoms: string[]): DepthText => ({ text, atoms });
  const subsets = [
    ['f1', 'f2'],
    ['f3', 'f4'],
    ['f1', 'f3'],
    ['f2', 'f4'],
    ['f1', 'f4'],
    ['f2', 'f3'],
    ['f1'],
    ['f4'],
  ];

  test('runs end to end and its checks hold on well-formed depth', async () => {
    const vectors = loadVectors(
      fixture<{ vectors_sha256: string }>('retrieval.json').vectors_sha256,
    );
    const ids = assets.catalog.map((e) => e.id);
    const emergency = new Set(assets.policy.emergency_direct);
    const entries: Record<string, DepthEntry> = {};
    ids.slice(0, 40).forEach((id, n) => {
      entries[id] = {
        l0: subsets.map((a, i) => T(`${id} L0 variante ${i}`, ...a)),
        layers: [
          {
            kind: 'why',
            texts: [1, 2, 3, 4].map((i) => T(`${id} L1 variante ${i}`, 'f1', 'f2', 'f3')),
          },
          {
            kind: 'specifics',
            texts: [1, 2, 3, 4].map((i) => T(`${id} L2 variante ${i}`, 'f3', 'f4')),
          },
        ],
        walk: [ids[(n + 1) % ids.length], ids[(n + 2) % ids.length], ids[(n + 3) % ids.length]],
        complements: ['f1', 'f2', 'f3', 'f4'],
        ...(emergency.has(id) ? { rotation: [0, 1, 2, 3] } : {}),
      };
    });
    const continuation = fixture<KnowledgeContinuation>('continuation.json');
    const report = await runE2e({
      assets: {
        ...assets,
        policy: { ...assets.policy, continuation },
        depth: { entries },
      },
      vectors,
      seeds: [1, 2],
    });
    console.log(formatReport(report));
    expect(report.entries).toBe(40);
    expect(report.a5.repeats).toEqual([]);
    expect(report.a11.fails).toEqual([]);
    expect(report.a13.fails).toEqual([]);
    expect(report.a13.checked).toBeGreaterThan(0);
  }, 120_000);
});
