// E2E for the continuation runtime (A5, A11, A13) on the REAL engine, catalog and index vectors.
// Scorer and embedder are stubs that make the target entry the only match, so retrieval always
// lands on it and only the depth / rotation logic is under test.
//
// Run it with: cd mobile && npx jest e2e_sigue --silent=false   (see tools/e2e_sigue.ts there).
// Test-only: never import from app code.

import { KnowledgeEngine, type DepthEntry, type DepthText, type KnowledgeAssets } from '..';

export interface E2eInput {
  assets: KnowledgeAssets; // policy.continuation and depth must be set
  vectors: Float32Array;
  seeds?: number[];
}

interface Failure {
  id: string;
  seed: number;
  why: string;
}

export interface E2eReport {
  entries: number;
  seeds: number[];
  retrievalMisses: Failure[];
  a5: { repeats: Failure[]; shortOfThree: Failure[]; exhausted: number; headroomEntries: number };
  a11: { fails: Failure[]; checked: number };
  a13: { fails: Failure[]; checked: number };
}

const SIGUE_TURNS = 4;
const REPEAT_TURNS = 8;

export async function runE2e({
  assets,
  vectors,
  seeds = [11, 12, 13],
}: E2eInput): Promise<E2eReport> {
  const depth = assets.depth?.entries;
  const cont = assets.policy.continuation;
  if (!depth || !cont) throw new Error('assets need depth and policy.continuation');
  const dims = assets.manifest.dims;
  const known = new Set(assets.catalog.map((e) => e.id));
  const emergency = new Set(assets.policy.emergency_direct);
  // No follow-up fusion and no abstain floor: every turn is the target entry, nothing else.
  const policy = { ...assets.policy, followup: null, T: -1 };
  const bridges = cont.bridges;

  const atomsOf = (id: string, text: string): string[] | undefined => {
    const d = depth[id];
    const bare = bridges.reduce(
      (t, b) => (t.startsWith(`${b} `) ? t.slice(b.length + 1) : t),
      text,
    );
    return [...(d?.l0 ?? []), ...(d?.layers.flatMap((l) => l.texts) ?? [])].find(
      (t: DepthText) => t.text === bare,
    )?.atoms;
  };

  const report: E2eReport = {
    entries: Object.keys(depth).length,
    seeds,
    retrievalMisses: [],
    a5: { repeats: [], shortOfThree: [], exhausted: 0, headroomEntries: 0 },
    a11: { fails: [], checked: 0 },
    a13: { fails: [], checked: 0 },
  };

  const nRows = assets.manifest.rows;
  const ownRows = new Map<string, number[]>();
  assets.manifest.row_entry.forEach((n, r) => {
    const id = assets.catalog[n].id;
    ownRows.set(id, [...(ownRows.get(id) ?? []), r]);
  });
  for (const seed of seeds) {
    let target = '';
    // Scorer stub: the target entry's rows match perfectly, nothing else does (no 0.5 s JS dot-product
    // loop per turn, and retrieval cannot land elsewhere).
    const score = async () => {
      const sims = new Float32Array(nRows);
      for (const r of ownRows.get(target) ?? []) sims[r] = 1;
      return sims;
    };
    const embed = async () => new Float32Array(dims);
    // A fresh session per scenario: a x8 that straddles a rotation cycle may legitimately repeat.
    const session = () =>
      new KnowledgeEngine({ ...assets, policy }, vectors, embed, undefined, score, { seed });
    let engine = session();

    for (const [id, d] of Object.entries(depth) as [string, DepthEntry][]) {
      if (!known.has(id)) continue;
      target = id;
      engine = session();

      // ---- A5: ask -> sigue x4 --------------------------------------------------------------
      const first = await engine.ask('pregunta');
      if (first.reply.type !== 'answer' || first.reply.id !== id) {
        report.retrievalMisses.push({
          id,
          seed,
          why: `retrieved ${first.reply.type === 'answer' ? first.reply.id : 'abstain'}`,
        });
        continue;
      }
      const seq = [first.reply.text];
      const turns: string[] = [];
      const revealed: string[][] = []; // complement facts of the anchor each sigue showed
      const served = new Set(atomsOf(id, first.reply.text) ?? []);
      let exhausted = 0;
      let newFactEveryTurn = true;
      for (let i = 0; i < SIGUE_TURNS; i++) {
        const r = (await engine.ask('sigue')).reply;
        if (r.type === 'abstain') exhausted++;
        else {
          turns.push(r.text);
          if (r.id === id) {
            const atoms = atomsOf(id, r.text) ?? [];
            const fresh = atoms.filter((a) => !served.has(a));
            fresh.forEach((a) => served.add(a));
            revealed.push(fresh);
            if (d.complements.length >= 2 && fresh.length === 0) newFactEveryTurn = false;
          }
        }
        seq.push(r.text);
      }
      const shown = seq.filter(
        (t, i) => !(i > 0 && t === seq[i - 1] && t.startsWith(cont.texts.exhausted)),
      );
      if (new Set(shown).size !== shown.length)
        report.a5.repeats.push({ id, seed, why: 'a reply repeated' });
      report.a5.exhausted += exhausted > 0 ? 1 : 0;
      const headroom = d.layers.length + d.walk.length >= 3;
      if (headroom) {
        report.a5.headroomEntries++;
        if (new Set(turns).size < 3) {
          report.a5.shortOfThree.push({ id, seed, why: `${new Set(turns).size} distinct turns` });
        }
      }

      // ---- A11: same question x8 ------------------------------------------------------------
      engine = session();
      const again: string[] = [];
      const subsets = new Set<string>();
      let firstAtoms: string[] = [];
      for (let i = 0; i < REPEAT_TURNS; i++) {
        const r = (await engine.ask('pregunta')).reply;
        again.push(r.text);
        const atoms = atomsOf(id, r.text) ?? [];
        if (i === 0) firstAtoms = atoms;
        subsets.add([...atoms].sort().join(','));
      }
      const distinct = new Set(again).size;
      report.a11.checked++;
      const canonicalOnly = emergency.has(id) && (d.rotation?.length ?? 0) < 3;
      const need = emergency.has(id) ? (canonicalOnly ? 1 : 3) : REPEAT_TURNS;
      if (distinct < need)
        report.a11.fails.push({
          id,
          seed,
          why: `${distinct} distinct of ${REPEAT_TURNS}, need ${need}`,
        });

      // ---- A13: partial disclosure ----------------------------------------------------------
      if (d.complements.length >= 2) {
        report.a13.checked++;
        const why: string[] = [];
        if (firstAtoms.length >= d.complements.length)
          why.push('first reply carries every complement');
        if (subsets.size < 2) why.push('one complement subset across x8');
        if (!newFactEveryTurn) why.push('a sigue revealed no new fact');
        if (why.length) report.a13.fails.push({ id, seed, why: why.join('; ') });
      }
    }
  }
  return report;
}

const head = (f: Failure[], n = 8): string =>
  f.length
    ? '\n' +
      f
        .slice(0, n)
        .map((x) => `    ${x.id} (seed ${x.seed}): ${x.why}`)
        .join('\n') +
      (f.length > n ? `\n    ... +${f.length - n} more` : '')
    : '';

export function formatReport(r: E2eReport): string {
  const runs = r.entries * r.seeds.length;
  const line = (name: string, bad: number, of: number, extra = '') =>
    `${name.padEnd(34)} ${String(bad).padStart(5)} / ${String(of).padEnd(6)} ${bad === 0 ? 'PASS' : 'FAIL'} ${extra}`;
  return [
    `e2e_sigue: ${r.entries} entries with depth data x seeds ${r.seeds.join(',')} (${runs} runs)`,
    line('retrieval stub misses', r.retrievalMisses.length, runs) + head(r.retrievalMisses),
    line('A5 repeated replies', r.a5.repeats.length, runs) + head(r.a5.repeats),
    line(
      'A5 <3 distinct turns (headroom)',
      r.a5.shortOfThree.length,
      r.a5.headroomEntries,
      '(headroom: layers + walk >= 3)',
    ) + head(r.a5.shortOfThree),
    `${'A5 runs that reached "exhausted"'.padEnd(34)} ${String(r.a5.exhausted).padStart(5)} / ${runs}`,
    line('A11 x8 distinct (emergency: >=3)', r.a11.fails.length, r.a11.checked) + head(r.a11.fails),
    line('A13 partial disclosure', r.a13.fails.length, r.a13.checked) + head(r.a13.fails),
  ].join('\n');
}

export const e2ePasses = (r: E2eReport): boolean =>
  !r.retrievalMisses.length &&
  !r.a5.repeats.length &&
  !r.a5.shortOfThree.length &&
  !r.a11.fails.length &&
  !r.a13.fails.length;
