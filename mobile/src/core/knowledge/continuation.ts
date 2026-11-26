// "Sigue" runtime pieces (R4, R6.5, R7): cue detector, seeded rotation and the unserved-fact
// selection. Pure TS, no I/O; the engine owns the state and the replies.

import type { DepthEntry, DepthLayer, DepthText, KnowledgeContinuation } from './assets';
import { foldText } from './safety';

export type CueKind = 'more' | 'why';

export interface CueMatcher {
  match(text: string): CueKind | null;
}

/** Whole message, accent-folded, at most `max_words` words, must match the cue (R4.1 / R4.5). */
export function cueMatcher(c: KnowledgeContinuation): CueMatcher {
  const more = new RegExp(c.cue, 'u');
  const why = new RegExp(c.why_cue, 'u');
  return {
    match(text) {
      const q = foldText(text);
      if (!q || q.split(' ').length > c.max_words) return null;
      if (more.test(q)) return 'more';
      return why.test(q) ? 'why' : null;
    },
  };
}

/** mulberry32: tiny, seedable, good enough to shuffle a few paraphrases. */
export function seededRandom(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

interface Cycle {
  order: number[];
  pos: number;
  last: number;
}

/**
 * Per-text-key seeded shuffled cycles (R6.5). Each index comes up once per cycle; on wrap-around
 * the order is reshuffled so its head is never the text served last.
 */
export class Rotation {
  private readonly cycles = new Map<string, Cycle>();

  constructor(private readonly rng: () => number) {}

  random(): number {
    return this.rng();
  }

  private shuffle(n: number): number[] {
    const a = Array.from({ length: n }, (_, i) => i);
    for (let i = n - 1; i > 0; i--) {
      const j = Math.floor(this.rng() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  /**
   * Next index in 0..n-1 for `key`, restricted to `ok` when given. Never the index served last
   * for this key unless it is the only choice.
   */
  take(key: string, n: number, ok?: (i: number) => boolean): number {
    if (n <= 1) return 0;
    let c = this.cycles.get(key);
    if (!c || c.order.length !== n) {
      c = { order: this.shuffle(n), pos: 0, last: -1 };
      this.cycles.set(key, c);
    }
    for (let guard = 0; guard < 3 * n; guard++) {
      if (c.pos >= n) {
        c.order = this.shuffle(n);
        if (c.order[0] === c.last) {
          const j = 1 + Math.floor(this.rng() * (n - 1));
          [c.order[0], c.order[j]] = [c.order[j], c.order[0]];
        }
        c.pos = 0;
      }
      const i = c.order[c.pos++];
      if (i !== c.last && (!ok || ok(i))) {
        c.last = i;
        return i;
      }
    }
    // Only the last-served index is allowed (or the filter rejected everything): take any allowed one.
    const any = Array.from({ length: n }, (_, i) => i).find((i) => !ok || ok(i)) ?? 0;
    c.last = any;
    return any;
  }
}

/** What the engine remembers about the conversation on one entry. */
export interface ContinuationState {
  id: string; // anchor entry
  served: Set<string>; // "<entry id>\u0000<fid>" complement facts already shown
  layers: Set<number>; // layer indexes of the anchor already shown
  walked: Set<string>; // walk ids already shown
}

export const factKey = (id: string, fid: string): string => `${id}\u0000${fid}`;

export function newState(id: string): ContinuationState {
  return { id, served: new Set(), layers: new Set(), walked: new Set() };
}

export const unserved = (st: ContinuationState, id: string, atoms: readonly string[]): number =>
  atoms.reduce((n, f) => n + (st.served.has(factKey(id, f)) ? 0 : 1), 0);

/**
 * R7.4: among the unserved layers pick the one whose best text carries the most unserved
 * complement facts (ties: seeded RNG). It must reveal >= 1 new fact, except for an entry with no
 * complement inventory, where the layers just go in order. Returns the layer and the indexes of
 * its texts that carry that maximum.
 */
export function pickLayer(
  d: DepthEntry,
  st: ContinuationState,
  rng: () => number,
): { layer: number; texts: Set<number> } | undefined {
  const inOrder = d.complements.length === 0;
  const open = d.layers
    .map((l, layer) => ({ layer, g: bestGain(l, st) }))
    .filter((c) => !st.layers.has(c.layer));
  const cands = inOrder ? open.slice(0, 1) : open.filter((c) => c.g > 0);
  if (!cands.length) return undefined;
  const top = Math.max(...cands.map((c) => c.g));
  const tied = cands.filter((c) => c.g === top);
  const { layer } = tied[Math.floor(rng() * tied.length)];
  return { layer, texts: bestTexts(d.layers[layer], st) };
}

const gainOf = (st: ContinuationState, atoms: readonly string[]): number => unserved(st, st.id, atoms);

const disjoint = (st: ContinuationState, atoms: readonly string[]): boolean =>
  atoms.every((f) => !st.served.has(factKey(st.id, f)));

/**
 * Prefer texts that reveal only new complements. A text that also repeats one already shown
 * is eligible only when no fully new text in the layer reveals anything.
 */
const pool = (l: DepthLayer, st: ContinuationState): DepthText[] => {
  const positive = l.texts.filter((t) => gainOf(st, t.atoms) > 0);
  const fresh = positive.filter((t) => disjoint(st, t.atoms));
  return fresh.length ? fresh : positive;
};

const bestGain = (l: DepthLayer, st: ContinuationState): number =>
  Math.max(0, ...pool(l, st).map((t) => gainOf(st, t.atoms)));

/** Indexes of the layer's texts that carry the most unserved complement facts. */
export function bestTexts(l: DepthLayer, st: ContinuationState): Set<number> {
  const chosen = pool(l, st);
  // No complement left to reveal: keep every text so an in-order layer can still rotate.
  if (!chosen.length) return new Set(l.texts.map((_, i) => i));
  const g = Math.max(...chosen.map((t) => gainOf(st, t.atoms)));
  return new Set(
    l.texts.flatMap((t, i) => (chosen.includes(t) && gainOf(st, t.atoms) === g ? [i] : [])),
  );
}

export function joinTopics(labels: readonly string[]): string {
  if (labels.length < 2) return labels.join('');
  return `${labels.slice(0, -1).join(', ')} y ${labels[labels.length - 1]}`;
}
