// Shapes of the GENERATED knowledge assets (experiments/nlu/export_nlu.py) and their
// load-time validation. The vectors are side-loaded, so they arrive as a Float32Array argument.

import type { EntryKind } from './types';

export interface CatalogSource {
  label: string;
  url?: string;
  retrieved_at?: string;
}

export interface CatalogEntry {
  id: string;
  section: string;
  kind: EntryKind;
  label: string;
  menu_label: string;
  short: string;
  // The exporter emits each step as a list of paragraphs; plain strings are tolerated.
  steps: (string | string[])[];
  sources: CatalogSource[];
  last_verified: string | null;
}

export interface SectionInfo {
  id: string;
  order: number;
  title: string;
  top_k: number;
  featured: string[];
}

export interface KnowledgePolicy {
  version: string;
  T: number;
  k: number;
  min_pool: number;
  max_sections: number;
  delta: number;
  /** Entry score = mean of its best `score_topk` row cosines. Absent in older exports: 1 (max). */
  score_topk?: number;
  /**
   * Follow-up fusion: a short or low-confidence turn blends in the previous turn's entry scores
   * with weight `w`. Absent in older exports: null (off).
   */
  followup?: KnowledgeFollowup | null;
  /** Strip chat fillers (clean.ts) before embedding; the index texts were stripped the same way. */
  strip_fillers?: boolean;
  /** "Sigue" runtime (R4). Absent or null: the engine behaves as before. */
  continuation?: KnowledgeContinuation | null;
  emergency_direct: string[];
  emergency_line_id: string;
  texts: {
    abstain: string;
    offline_status: string;
  };
  laya: {
    enabled: boolean;
    model: string;
    catalog_sha256: string | null;
    mode: string;
  };
}

export interface KnowledgeFollowup {
  /**
   * What a follow-up turn is blended with: 'scores' = the previous turn's final entry scores;
   * 'concat' = the scores of "<previous user text> <this text>" embedded together (the e5
   * fine-tune trained on such joined 2-turn conversations). Absent: 'scores'.
   */
  mode?: 'scores' | 'concat';
  w: number; // weight of the context scores
  max_words: number; // a turn with at most this many words is a follow-up
  below: number; // ... and so is one whose own top cosine is below this
  /**
   * Optional connective pattern (case-insensitive, unicode), e.g. turns opening with "y", "con",
   * "eso". When set, a turn is a follow-up if it matches, or if it is short (<= max_words) AND
   * weakly matched on its own (< below): a short but self-sufficient question ("hay señal de
   * celular") is no longer blended with the previous topic.
   */
  cue?: string | null;
}

export interface KnowledgeContinuation {
  /** Whole-message pattern over accent-folded text (foldText), e.g. "sigue", "mas", "que mas". */
  cue: string;
  max_words: number; // the whole message has at most this many words
  /** Whole-message pattern for a bare "por que". */
  why_cue: string;
  /** Fact-free clauses that open a related-topic reply. */
  bridges: string[];
  texts: {
    no_state: string;
    exhausted: string;
    /** "{topics}" is replaced by two related labels. Absent: the exhausted text stands alone. */
    related?: string;
  };
}

/** A whole pre-approved text and the complement fact ids it states (key facts are implied). */
export interface DepthText {
  text: string;
  atoms: string[];
}

export interface DepthLayer {
  kind: string; // why | how | specifics
  texts: DepthText[]; // paraphrases of one layer
}

export interface DepthEntry {
  /** L0 paraphrases the rotation serves (R6.5); the canonical text only when not R7.6-eligible. */
  l0: DepthText[];
  layers: DepthLayer[];
  walk: string[]; // related entry ids, best first
  /** Every complement fact id of the entry (R7.1); empty: no inventory, layers go in order. */
  complements: string[];
  /** Emergency entries only: indexes into `l0` approved twice (R6.6); fewer than 3 keeps the canonical text. */
  rotation?: number[];
}

export interface KnowledgeDepth {
  entries: Record<string, DepthEntry>;
}

export interface IndexManifest {
  embedder: Record<string, unknown>;
  prefix: string;
  dims: number;
  rows: number;
  text_rows: number;
  row_entry: number[]; // text row -> catalog index
  section_rows: string[]; // section ids, in the order of the description rows
  entry_section: number[]; // catalog index -> position in section_rows
  vectors: { file: string; bytes: number; sha256: string; dtype: string };
  /** ONNX MatMul over the same vectors (export_knowledge.write_scorer); the phone scores with it. */
  scorer?: { file: string; bytes: number; input: string; output: string };
  corpus_sha256: string;
}

export interface KnowledgeAssets {
  catalog: CatalogEntry[];
  sections: SectionInfo[];
  policy: KnowledgePolicy;
  manifest: IndexManifest;
  /** depth.json (export_nlu.py); only read when policy.continuation is set. */
  depth?: KnowledgeDepth | null;
}

/** Retrieval view of the assets, with every lookup precomputed once at load. */
export interface LoadedIndex {
  dims: number;
  textRows: number;
  vectors: Float32Array; // (textRows + sectionIds.length) x dims, row-major
  rowEntry: Int32Array; // text row -> entry
  rowSection: Int32Array; // text row -> section
  entryRows: Int32Array[]; // entry -> its text rows
  ids: string[]; // entry -> id
  sectionIds: string[];
  sectionMembers: Int32Array[]; // section -> entries, catalog order
  sectionTopK: Int32Array;
  k: number;
  minPool: number;
  maxSections: number;
  delta: number;
  scoreTopK: number;
}

export class KnowledgeAssetError extends Error {
  constructor(readonly problems: string[]) {
    super(`Invalid knowledge assets: ${problems.join('; ')}`);
    this.name = 'KnowledgeAssetError';
  }
}

const isInt = (n: unknown): n is number => typeof n === 'number' && Number.isInteger(n);

/** Checks the assets against each other and the vectors, then builds the retrieval view. Throws KnowledgeAssetError. */
export function validateAssets(assets: KnowledgeAssets, vectors: Float32Array): LoadedIndex {
  const { catalog, sections, policy, manifest: m } = assets;
  const problems: string[] = [];
  const fail = (p: string) => problems.push(p);

  if (!isInt(m.dims) || m.dims <= 0) fail(`dims ${m.dims}`);
  if (!isInt(m.text_rows) || m.text_rows < 0) fail(`text_rows ${m.text_rows}`);
  if (m.rows !== m.text_rows + m.section_rows.length) {
    fail(`rows ${m.rows} != text_rows ${m.text_rows} + ${m.section_rows.length} section rows`);
  }
  if (vectors.length !== m.rows * m.dims) {
    fail(`vectors hold ${vectors.length} floats, manifest says ${m.rows} x ${m.dims}`);
  }
  if (m.row_entry.length !== m.text_rows) fail(`row_entry has ${m.row_entry.length} rows`);
  if (m.entry_section.length !== catalog.length) {
    fail(`entry_section has ${m.entry_section.length} entries, catalog ${catalog.length}`);
  }

  const ids = catalog.map((e) => e.id);
  const idSet = new Set(ids);
  if (idSet.size !== ids.length) fail('duplicate catalog ids');

  const topKById = new Map(sections.map((s) => [s.id, s.top_k]));
  const sectionTopK = new Int32Array(m.section_rows.length);
  m.section_rows.forEach((s, i) => {
    const k = topKById.get(s);
    if (!isInt(k) || k < 1) fail(`section ${s} has no valid top_k`);
    else sectionTopK[i] = k;
  });

  const entrySection = new Int32Array(catalog.length);
  m.entry_section.forEach((s, n) => {
    if (!isInt(s) || s < 0 || s >= m.section_rows.length) return fail(`entry ${n} section ${s}`);
    entrySection[n] = s;
    if (catalog[n] && catalog[n].section !== m.section_rows[s]) {
      fail(
        `entry ${catalog[n].id} is in ${catalog[n].section}, manifest says ${m.section_rows[s]}`,
      );
    }
  });

  const rowEntry = new Int32Array(m.row_entry.length);
  const rowSection = new Int32Array(m.row_entry.length);
  m.row_entry.forEach((n, r) => {
    if (!isInt(n) || n < 0 || n >= catalog.length) return fail(`row ${r} entry ${n}`);
    rowEntry[r] = n;
    rowSection[r] = entrySection[n];
  });

  for (const id of [...policy.emergency_direct, policy.emergency_line_id]) {
    if (!idSet.has(id)) fail(`policy id ${id} not in catalog`);
  }
  for (const key of ['T', 'delta'] as const) {
    if (!Number.isFinite(policy[key])) fail(`policy.${key} ${policy[key]}`);
  }
  for (const key of ['k', 'min_pool', 'max_sections'] as const) {
    if (!isInt(policy[key]) || policy[key] < 1) fail(`policy.${key} ${policy[key]}`);
  }

  const scoreTopK = policy.score_topk ?? 1;
  if (!isInt(scoreTopK) || scoreTopK < 1) fail(`policy.score_topk ${policy.score_topk}`);
  const f = policy.followup;
  if (f && f.mode !== undefined && f.mode !== 'scores' && f.mode !== 'concat') {
    fail(`policy.followup.mode ${String(f.mode)}`);
  }
  if (f != null) {
    if (!Number.isFinite(f.w) || f.w <= 0) fail(`policy.followup.w ${f.w}`);
    if (!isInt(f.max_words) || f.max_words < 0) fail(`policy.followup.max_words ${f.max_words}`);
    if (!Number.isFinite(f.below)) fail(`policy.followup.below ${f.below}`);
    if (f.cue != null) {
      try {
        new RegExp(f.cue, 'iu');
      } catch {
        fail(`policy.followup.cue ${f.cue}`);
      }
    }
  }

  validateContinuation(assets, idSet, fail);

  if (problems.length) throw new KnowledgeAssetError(problems);

  const buckets: number[][] = m.section_rows.map(() => []);
  entrySection.forEach((s, n) => buckets[s].push(n));
  const rowsOf: number[][] = catalog.map(() => []);
  rowEntry.forEach((n, r) => rowsOf[n].push(r));

  return {
    dims: m.dims,
    textRows: m.text_rows,
    vectors,
    rowEntry,
    rowSection,
    entryRows: rowsOf.map((r) => Int32Array.from(r)),
    ids,
    sectionIds: m.section_rows,
    sectionMembers: buckets.map((b) => Int32Array.from(b)),
    sectionTopK,
    k: policy.k,
    minPool: policy.min_pool,
    maxSections: policy.max_sections,
    delta: policy.delta,
    scoreTopK,
  };
}

const isText = (t: unknown): t is DepthText =>
  typeof t === 'object' &&
  t !== null &&
  typeof (t as DepthText).text === 'string' &&
  (t as DepthText).text.trim() !== '' &&
  Array.isArray((t as DepthText).atoms) &&
  (t as DepthText).atoms.every((a) => typeof a === 'string');

function validateContinuation(
  assets: KnowledgeAssets,
  idSet: ReadonlySet<string>,
  fail: (p: string) => void,
): void {
  const c = assets.policy.continuation;
  // R4.8: with continuation off, depth is unused and must not reject assets the old engine accepted.
  if (c == null) return;
  for (const key of ['cue', 'why_cue'] as const) {
    try {
      new RegExp(c[key], 'u');
    } catch {
      fail(`policy.continuation.${key} ${String(c[key])}`);
    }
  }
  if (!isInt(c.max_words) || c.max_words < 1) fail(`policy.continuation.max_words ${c.max_words}`);
  if (!Array.isArray(c.bridges) || !c.bridges.length || c.bridges.some((b) => !b?.trim())) {
    fail('policy.continuation.bridges must be a non-empty list of texts');
  }
  for (const key of ['no_state', 'exhausted'] as const) {
    if (typeof c.texts?.[key] !== 'string' || !c.texts[key].trim()) {
      fail(`policy.continuation.texts.${key}`);
    }
  }
  if (c.texts?.related !== undefined && !c.texts.related.includes('{topics}')) {
    fail('policy.continuation.texts.related has no {topics}');
  }

  const depth = assets.depth;
  if (depth == null) return;
  for (const [id, d] of Object.entries(depth.entries)) {
    const at = `depth ${id}`;
    if (!idSet.has(id)) {
      fail(`${at} not in catalog`);
      continue;
    }
    if (!Array.isArray(d.l0) || !d.l0.every(isText)) fail(`${at}: bad l0`);
    if (
      !Array.isArray(d.layers) ||
      d.layers.some((l) => !Array.isArray(l.texts) || !l.texts.length || !l.texts.every(isText))
    ) {
      fail(`${at}: bad layers`);
    }
    if (!Array.isArray(d.complements)) fail(`${at}: bad complements`);
    const allowed = new Set(Array.isArray(d.complements) ? d.complements : []);
    const texts = [
      ...(Array.isArray(d.l0) ? d.l0 : []),
      ...(Array.isArray(d.layers) ? d.layers.flatMap((l) => l.texts ?? []) : []),
    ];
    for (const tx of texts) {
      for (const atom of tx.atoms ?? []) {
        if (!allowed.has(atom)) fail(`${at}: atom ${atom} not in complements`);
      }
    }
    for (const w of Array.isArray(d.walk) ? d.walk : [id]) {
      if (!idSet.has(w) || w === id) fail(`${at}: walk id ${w} not in catalog or self`);
    }
    if (d.rotation !== undefined) {
      const ok =
        Array.isArray(d.rotation) &&
        d.rotation.every((i) => isInt(i) && i >= 0 && i < (d.l0?.length ?? 0));
      if (!ok) fail(`${at}: rotation out of range`);
    }
  }
}
