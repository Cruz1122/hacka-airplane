// Port of experiments/laya/export_knowledge.py Index.retrieve (unmasked), the dataset contract the
// pools were trained and fitted on. Spec: __fixtures__/retrieval.json.
//
// Python runs in float32 (numpy 2: float32 - python float stays float32), so every score is rounded
// with a Float32Array store or Math.fround before it is compared.

import type { LoadedIndex } from './assets';

export interface RetrievalResult {
  pool: string[]; // entry ids, best first
  cos: number[]; // entry score (top-k mean cosine, fused with the context when given), same order
  gates: string[]; // gated section ids, best first
  scores: Float32Array; // final score of every entry, catalog order (-1 for an entry without rows)
}

/** Previous-turn entry scores to blend in: s' = (s + w * c) / (1 + w). */
export interface RetrievalContext {
  scores: Float32Array;
  w: number;
}

export class RetrievalInputError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'RetrievalInputError';
  }
}

// Python orders strings by code point; ids are ASCII, where `<` agrees. localeCompare would not.
const cmpStr = (a: string, b: string) => (a < b ? -1 : a > b ? 1 : 0);
const desc = (a: number, b: number) => b - a;

/**
 * `queryVec` must be the L2-normalised e5 embedding of "query: " + text.
 * `sims`, when given, holds the dot products of every index row (text rows, then section
 * description rows) with `queryVec`, computed natively (onnxruntime scorer); the JS loop is skipped.
 * `context`, when given, fuses every entry score with the previous turn's before gating.
 */
export function retrieve(
  queryVec: Float32Array,
  idx: LoadedIndex,
  sims?: Float32Array,
  context?: RetrievalContext,
): RetrievalResult {
  const { dims, textRows, vectors, rowSection, entryRows, ids, sectionIds, scoreTopK } = idx;
  if (queryVec.length !== dims) {
    throw new RetrievalInputError(`query vector has ${queryVec.length} dims, index has ${dims}`);
  }
  for (let j = 0; j < dims; j++) {
    // A NaN would compare false everywhere and silently scramble every sort below.
    if (!Number.isFinite(queryVec[j]))
      throw new RetrievalInputError(`query vector[${j}] is ${queryVec[j]}`);
  }

  const nSec = sectionIds.length;
  const nEntries = ids.length;
  const nRows = textRows + nSec;
  if (sims && sims.length !== nRows) {
    throw new RetrievalInputError(`sims has ${sims.length} rows, index has ${nRows}`);
  }
  if (context && context.scores.length !== nEntries) {
    throw new RetrievalInputError(
      `context has ${context.scores.length} scores, index has ${nEntries} entries`,
    );
  }

  // Float32Array stores round to float32, like the numpy scores. The native path is float32 already.
  let rowSim = sims;
  if (!rowSim) {
    rowSim = new Float32Array(nRows);
    // Unrolled by 8 with a running pointer: under V8 --jitless (an interpreter proxy for Hermes) this
    // was ~1.7x faster than a plain loop; it is still ~0.47 s/query there, far above the 60 ms target.
    const tail = dims - (dims % 8);
    let p = 0;
    for (let r = 0; r < nRows; r++) {
      let acc = 0;
      let j = 0;
      for (; j < tail; j += 8, p += 8) {
        acc +=
          vectors[p] * queryVec[j] +
          vectors[p + 1] * queryVec[j + 1] +
          vectors[p + 2] * queryVec[j + 2] +
          vectors[p + 3] * queryVec[j + 3] +
          vectors[p + 4] * queryVec[j + 4] +
          vectors[p + 5] * queryVec[j + 5] +
          vectors[p + 6] * queryVec[j + 6] +
          vectors[p + 7] * queryVec[j + 7];
      }
      for (; j < dims; j++, p++) acc += vectors[p] * queryVec[j];
      rowSim[r] = acc;
    }
  }

  if (idx.overlay?.sections.length) {
    const { vectors: extra, sections } = idx.overlay;
    const combined = new Float32Array(nRows + sections.length);
    combined.set(rowSim);
    for (let r = 0; r < sections.length; r++) {
      let dot = 0;
      for (let j = 0; j < dims; j++) dot += extra[r * dims + j] * queryVec[j];
      combined[nRows + r] = dot;
    }
    rowSim = combined;
  }

  // Section score: max over its description row and every visible text row of its entries.
  const sec = new Float32Array(nSec).fill(-Infinity);
  for (let r = 0; r < textRows; r++) {
    const s = rowSection[r];
    if (s >= 0 && rowSim[r] > sec[s]) sec[s] = rowSim[r];
  }
  for (let s = 0; s < nSec; s++) {
    if (rowSim[textRows + s] > sec[s]) sec[s] = rowSim[textRows + s];
  }

  idx.overlay?.sections.forEach((s, i) => {
    if (rowSim[nRows + i] > sec[s]) sec[s] = rowSim[nRows + i];
  });

  // Entry score: mean of its best `scoreTopK` row cosines in float32, summed best-first one fround
  // at a time (numpy's float32 mean over <= 8 values is that sequential sum). k = 1 is the max.
  const scores = new Float32Array(nEntries).fill(-1);
  const buf: number[] = [];
  for (let n = 0; n < nEntries; n++) {
    const rows = entryRows[n];
    if (rows.length === 0) continue;
    if (scoreTopK === 1) {
      let best = -Infinity;
      for (let i = 0; i < rows.length; i++) if (rowSim[rows[i]] > best) best = rowSim[rows[i]];
      scores[n] = best;
      continue;
    }
    buf.length = 0;
    for (let i = 0; i < rows.length; i++) buf.push(rowSim[rows[i]]);
    buf.sort(desc);
    const m = Math.min(scoreTopK, buf.length);
    let sum = buf[0];
    for (let i = 1; i < m; i++) sum = Math.fround(sum + buf[i]);
    scores[n] = Math.fround(sum / m);
  }

  if (context) {
    // numpy float32 op python float: the scalar is cast to float32, every op rounds to float32.
    const w = Math.fround(context.w);
    const div = Math.fround(1 + context.w);
    for (let n = 0; n < nEntries; n++) {
      if (entryRows[n].length === 0) continue; // keep -1: never pooled
      const wc = Math.fround(w * context.scores[n]);
      scores[n] = Math.fround(Math.fround(scores[n] + wc) / div);
    }
  }

  const order = Array.from({ length: nSec }, (_, s) => s).sort(
    (a, b) => sec[b] - sec[a] || cmpStr(sectionIds[a], sectionIds[b]),
  );
  const floor = Math.fround(sec[order[0]] - Math.fround(idx.delta));
  const gates = order.filter((s) => sec[s] >= floor).slice(0, idx.maxSections);

  const byScore = (a: number, b: number) => scores[b] - scores[a] || cmpStr(ids[a], ids[b]);
  let pool: number[] = [];
  for (const s of gates) {
    const members = Array.from(idx.sectionMembers[s]).filter((n) => scores[n] > -1);
    pool.push(...members.sort(byScore).slice(0, idx.sectionTopK[s]));
  }
  pool = pool.sort(byScore).slice(0, idx.k);

  if (pool.length < idx.minPool) {
    // np.argsort(-scores, kind="stable"): descending score, ties by entry index.
    const seen = new Set(pool);
    const flat = Array.from({ length: nEntries }, (_, n) => n).sort(
      (a, b) => scores[b] - scores[a] || a - b,
    );
    for (const n of flat) {
      if (pool.length >= idx.minPool) break;
      if (!seen.has(n) && scores[n] > -1) {
        pool.push(n);
        seen.add(n);
      }
    }
    pool.sort(byScore);
  }

  return {
    pool: pool.map((n) => ids[n]),
    cos: pool.map((n) => scores[n]),
    gates: gates.map((s) => sectionIds[s]),
    scores,
  };
}

/**
 * The best `k` of `entries` (catalog indexes, each with index rows) by final score, ties by id,
 * as `retrieve` orders its pool. No gating: every listed entry competes.
 */
export function rankEntries(
  scores: Float32Array,
  ids: readonly string[],
  entries: readonly number[],
  k: number,
): Pick<RetrievalResult, 'pool' | 'cos'> {
  const top = [...entries]
    .sort((a, b) => scores[b] - scores[a] || cmpStr(ids[a], ids[b]))
    .slice(0, k);
  return { pool: top.map((n) => ids[n]), cos: top.map((n) => scores[n]) };
}
