// Port of nevados_bench.guards: deterministic checks on model output before a visitor
// sees it. Guards only remove answers or arguments; they never add a value.
import type { ToolCall } from './types';
import {
  ABSTAIN_ES,
  containsNamedValue,
  evidenceValues,
  extractCitations,
  extractValues,
  isAbstention,
  normalizeText,
} from './values';
import type { GazetteerEntry, Passage, World } from './world';
import { loadWorld, regex } from './world';

const G = loadWorld().json.guards;

export const SAFETY_REFERRAL_ES: string = G.safety_referral_es;
const FUZZY_RATIO: number = G.fuzzy_ratio;
const FUZZY_MIN_CHARS: number = G.fuzzy_min_chars;
const GENERIC_WORDS = new Set<string>(G.generic_words);
const SHORT_NAME_PREFIXES: string[] = G.short_name_prefixes;
const NEGATION_TOKENS = new Set<string>(G.negation_tokens);
const NEGATION_EXCEPTION: string = G.negation_exception;
const NEGATION_WINDOW: number = G.negation_window;
const MONTH_WORDS: string[] = G.month_words;
const DATE_RE = regex(G.date_re);
const VISITOR_RE = regex(G.visitor_re);
const COUNT_RE = regex(G.count_re);

// Only these arguments are checked: their values cannot be inferred from the question topic.
export const CHECKED_ARGS: readonly string[] = G.checked_args;

export interface GuardResult {
  text: string;
  passed: boolean;
  reasons: string[];
}

// --------------------------------------------------------------------------- difflib

/** difflib.SequenceMatcher(None, a, b).ratio(). No junk; autojunk only matters for
 * len(b) >= 200, which guard phrases never reach (asserted). Hot path of the guards:
 * plain loops, no destructuring (Babel helpers dominated the profile). */
export function sequenceRatio(a: string, b: string): number {
  // Code points like Python; plain indexing is identical for BMP-only text.
  const astral = /[\uD800-\uDFFF]/;
  const A: ArrayLike<string> = astral.test(a) ? Array.from(a) : a;
  const B: ArrayLike<string> = astral.test(b) ? Array.from(b) : b;
  if (B.length >= 200) throw new Error('sequenceRatio: autojunk not ported (len(b) >= 200)');
  // Python's j2len dicts as two dense rows: identical k values and tie order (ascending j).
  let prev = new Int32Array(B.length + 1);
  let cur = new Int32Array(B.length + 1);
  let matches = 0;
  const queue: number[] = [0, A.length, 0, B.length]; // flat (alo, ahi, blo, bhi) quads
  while (queue.length > 0) {
    const bhi = queue.pop()!;
    const blo = queue.pop()!;
    const ahi = queue.pop()!;
    const alo = queue.pop()!;
    // find_longest_match
    let besti = alo;
    let bestj = blo;
    let bestsize = 0;
    prev.fill(0);
    for (let i = alo; i < ahi; i++) {
      cur.fill(0);
      const ai = A[i];
      for (let j = blo; j < bhi; j++) {
        if (B[j] !== ai) continue;
        const k = (j > blo ? prev[j - 1] : 0) + 1;
        cur[j] = k;
        if (k > bestsize) {
          besti = i - k + 1;
          bestj = j - k + 1;
          bestsize = k;
        }
      }
      const swap = prev;
      prev = cur;
      cur = swap;
    }
    while (besti > alo && bestj > blo && A[besti - 1] === B[bestj - 1]) {
      besti--;
      bestj--;
      bestsize++;
    }
    while (
      besti + bestsize < ahi &&
      bestj + bestsize < bhi &&
      A[besti + bestsize] === B[bestj + bestsize]
    )
      bestsize++;
    if (bestsize === 0) continue;
    matches += bestsize;
    if (alo < besti && blo < bestj) queue.push(alo, besti, blo, bestj);
    if (besti + bestsize < ahi && bestj + bestsize < bhi)
      queue.push(besti + bestsize, ahi, bestj + bestsize, bhi);
  }
  const total = A.length + B.length;
  return total ? (2 * matches) / total : 1;
}

// --------------------------------------------------------------------------- fuzzy names

function tokens(norm: string): string[] {
  return norm.match(/[a-z0-9]+/g) ?? [];
}

function similar(a: string, b: string): boolean {
  if (a === b) return true;
  if (b.length < FUZZY_MIN_CHARS) return false;
  // Exact pre-filter: ratio <= 2*min(len)/(len a + len b) (difflib real_quick_ratio).
  if ((2 * Math.min(a.length, b.length)) / (a.length + b.length) < FUZZY_RATIO) return false;
  return sequenceRatio(a, b) >= FUZZY_RATIO;
}

/** Start index of the last window of len(phrase words) tokens similar to `phrase`. */
export function fuzzyLastIndex(toks: string[], phrase: string): number | null {
  const n = phrase.split(/\s+/).filter(Boolean).length;
  let hit: number | null = null;
  for (let i = 0; i < toks.length - n + 1; i++) {
    if (similar(toks.slice(i, i + n).join(' '), phrase)) hit = i;
  }
  return hit;
}

export function fuzzyContains(toks: string[], phrase: string): boolean {
  return fuzzyLastIndex(toks, phrase) !== null;
}

function shortName(name: string): string {
  let norm = normalizeText(name);
  for (const prefix of SHORT_NAME_PREFIXES) {
    if (norm.startsWith(prefix)) norm = norm.slice(prefix.length);
  }
  return norm;
}

function negated(toks: string[], index: number): boolean {
  const before = toks.slice(Math.max(0, index - NEGATION_WINDOW), index);
  return before.some((t) => NEGATION_TOKENS.has(t)) && !before.includes(NEGATION_EXCEPTION);
}

/** station id -> token index of its last (non-negated) mention; typo-tolerant. */
export function stationMentions(
  text: string,
  stationNames: Map<string, string>,
): Map<string, number> {
  const toks = tokens(normalizeText(text));
  const found = new Map<string, number>();
  for (const [stationId, name] of stationNames) {
    const short = shortName(name);
    const phrases = [short, ...short.split(/\s+/).filter((w) => w && !GENERIC_WORDS.has(w))];
    const hits = phrases
      .map((p) => fuzzyLastIndex(toks, p))
      .filter((i): i is number => i !== null && !negated(toks, i));
    if (hits.length > 0) found.set(stationId, Math.max(...hits));
  }
  return found;
}

/** The station `text` is about, or null. Several named: null unless `preferLast`. */
export function detectStation(
  text: string,
  stationNames: Map<string, string>,
  preferLast = false,
): string | null {
  const found = stationMentions(text, stationNames);
  if (found.size === 1) return found.keys().next().value!;
  if (found.size > 0 && preferLast) {
    let best: string | null = null;
    let bestIndex = -1;
    for (const [id, index] of found) {
      if (index > bestIndex) [best, bestIndex] = [id, index];
    }
    return best;
  }
  return null;
}

export function stationNames(world: World): Map<string, string> {
  return new Map([...world.stations].map(([id, s]) => [id, s.name]));
}

export function fallbackText(safety: boolean): string {
  return safety ? `${ABSTAIN_ES} ${SAFETY_REFERRAL_ES}` : ABSTAIN_ES;
}

// --------------------------------------------------------------------------- answers

/** Check a grounded answer against the passages that were shown. */
export function guardAnswer(
  text: string,
  opts: {
    userMessage: string;
    shown: Map<string, Passage>;
    targetStation: string | null;
    gazetteer?: Iterable<GazetteerEntry>;
    safety?: boolean;
  },
): GuardResult {
  if (isAbstention(text) || !text.trim()) return { text, passed: true, reasons: [] };
  const reasons: string[] = [];
  const shownUpper = new Map([...opts.shown].map(([pid, p]) => [pid.toUpperCase(), p]));
  const citedIds = extractCitations(text);
  const cited = citedIds.filter((c) => shownUpper.has(c)).map((c) => shownUpper.get(c)!);
  if (citedIds.some((c) => !shownUpper.has(c))) reasons.push('cited_not_shown');
  const target = opts.targetStation;
  if (target !== null && cited.some((p) => p.station !== null && p.station !== target))
    reasons.push('other_station_cited');

  const values = evidenceValues(text); // list numbering is not a stated value
  const supported = extractValues(opts.userMessage);
  for (const p of cited) {
    for (const v of extractValues(p.text)) supported.add(v);
    for (const v of p.values) supported.add(v);
  }
  if (values.size > 0 && citedIds.length === 0) reasons.push('uncited_values');
  else if ([...values].some((v) => !supported.has(v))) reasons.push('unsupported_values');

  if (target !== null) {
    const normText = normalizeText(text);
    const normUser = normalizeText(opts.userMessage);
    for (const entry of opts.gazetteer ?? []) {
      if (
        entry.station !== null &&
        entry.station !== target &&
        !/\d/.test(entry.value) &&
        containsNamedValue(normText, entry.value) &&
        !containsNamedValue(normUser, entry.value)
      ) {
        reasons.push('other_station_named_value');
        break;
      }
    }
  }

  if (reasons.length > 0)
    return { text: fallbackText(opts.safety ?? false), passed: false, reasons };
  return { text, passed: true, reasons: [] };
}

// --------------------------------------------------------------------------- tool calls

export interface RouteGuardResult {
  decision: string | null; // unchanged model decision, or 'clarify' when a slot is not grounded
  calls: ToolCall[];
  missing: string[]; // required args the user never stated: ask for these
  needsConfirmation: boolean; // a side-effect tool: execute only after an explicit "sí"
  // With `missing`: the calls minus the unstated arguments, so a flow can start with them.
  partialCalls: ToolCall[];
}

function statesDate(norm: string, toks: string[]): boolean {
  if (DATE_RE.test(norm)) return true;
  // "10 de dicembre", "December 3": a (possibly misspelt) month next to a day number.
  const hasMonth = toks.some((t) => MONTH_WORDS.some((m) => similar(t, m)));
  return hasMonth && toks.some((t) => /^\d{1,2}$/.test(t));
}

// The driver re-grounds every earlier user message on each guarded call (O(turns^2)
// fuzzy matching); results are pure per (world, text), so memoize them, bounded.
const MEMO_MAX = 512;
const groundedMemo = new WeakMap<World, Map<string, Record<string, unknown>>>();

/** Arguments the user's own words support. Station/trail map to ids; others to true. */
export function groundedArgs(text: string, world: World): Record<string, unknown> {
  let memo = groundedMemo.get(world);
  if (!memo) groundedMemo.set(world, (memo = new Map()));
  let found = memo.get(text);
  if (!found) {
    if (memo.size >= MEMO_MAX) memo.clear();
    found = computeGroundedArgs(text, world);
    memo.set(text, found);
  }
  return { ...found };
}

function computeGroundedArgs(text: string, world: World): Record<string, unknown> {
  const norm = normalizeText(text);
  const toks = tokens(norm);
  const found: Record<string, unknown> = {};
  const trails = [...world.trails.values()].filter((t) => fuzzyContains(toks, shortName(t.name)));
  if (trails.length === 1) found.trail_id = trails[0].id;
  let station = detectStation(text, stationNames(world), true);
  if (station === null && trails.length === 1) station = trails[0].station;
  if (station !== null) found.station = station;
  if (statesDate(norm, toks)) found.date = true;
  if (VISITOR_RE.test(norm)) found.visitor_type = true;
  if (COUNT_RE.test(norm)) found.group_size = found.people_count = true;
  return found;
}

/** Validate the model's tool call against what the user actually said (see Python
 * guard_route). `contextTexts` (oldest first) only ground, never override. */
export function guardRoute(
  decision: string | null,
  callsIn: Iterable<ToolCall>,
  opts: {
    userText: string;
    world: World;
    contextTexts?: readonly string[];
    deviceStation?: string | null;
  },
): RouteGuardResult {
  const calls = [...callsIn];
  const { world } = opts;
  const deviceStation = opts.deviceStation ?? null;
  const pass = (d: string | null, c: ToolCall[]): RouteGuardResult => ({
    decision: d,
    calls: c,
    missing: [],
    needsConfirmation: false,
    partialCalls: [],
  });
  if (decision !== 'call' && !(decision === null && calls.length > 0)) return pass(decision, calls);
  const stated = groundedArgs(opts.userText, world); // current message: may override the model
  const fromContext: Record<string, unknown> = {};
  const names = stationNames(world);
  const mentioned = new Set(stationMentions(opts.userText, names).keys());
  for (const text of [...(opts.contextTexts ?? [])].reverse()) {
    for (const id of stationMentions(text, names).keys()) mentioned.add(id);
    for (const [name, value] of Object.entries(groundedArgs(text, world)))
      if (!(name in fromContext)) fromContext[name] = value;
  }
  const isPlace = (name: string) => name === 'station' || name === 'trail_id';
  const fixed: ToolCall[] = [];
  const missing: string[] = [];
  for (const call of calls) {
    const spec = world.tools.get(call.name);
    if (!spec) return pass('clarify', []); // hallucinated tool: never execute
    const args: Record<string, unknown> = { ...call.arguments };
    const unstated: string[] = [];
    const required: string[] = spec.parameters.required ?? [];
    for (const name of required) {
      if (!CHECKED_ARGS.includes(name)) continue;
      if (isPlace(name) && name in stated) args[name] = stated[name];
      else if (name === 'station' && mentioned.has(args[name] as string)) {
        // refers back to a station already in the conversation
      } else if (isPlace(name) && name in fromContext) args[name] = fromContext[name];
      else if (name === 'station' && deviceStation !== null) args[name] = deviceStation;
      else if (!(name in stated) && !(name in fromContext)) unstated.push(name);
    }
    for (const name of CHECKED_ARGS) {
      if (required.includes(name) || !(name in args)) continue;
      // Optional and unstated: drop it (nothing to ask), never execute it as said.
      if (isPlace(name) && name in stated) args[name] = stated[name];
      else if (isPlace(name) && name in fromContext) args[name] = fromContext[name];
      else if (!(name in stated) && !(name in fromContext)) delete args[name];
    }
    missing.push(...unstated);
    const kept = Object.fromEntries(Object.entries(args).filter(([k]) => !unstated.includes(k)));
    fixed.push({ ...call, arguments: kept });
  }
  if (missing.length > 0) {
    return {
      decision: 'clarify',
      calls: [],
      missing: [...new Set(missing)],
      needsConfirmation: false,
      partialCalls: fixed,
    };
  }
  const sideEffects = fixed.some((c) => world.tools.get(c.name)?.has_side_effects ?? false);
  return {
    decision: decision ?? 'call',
    calls: fixed,
    missing: [],
    needsConfirmation: sideEffects,
    partialCalls: [],
  };
}
