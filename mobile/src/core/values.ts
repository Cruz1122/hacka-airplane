// Port of nevados_bench.values plus scoring.grounding.evidence_values (used by guards).
import { loadWorld, regex } from './world';

const W = loadWorld().json;

export const ABSTAIN_ES = W.values.abstain_es;
export const ABSTAIN_EN = W.values.abstain_en;
const ABSTAIN_PATTERNS = W.values.abstain_patterns;
const SMALL_NUMBER_LIMIT = W.grounding.small_number_limit;

// Global copies are rebuilt per call: a shared /g RegExp carries lastIndex state.
const timeRe = () => regex(W.values.time_re, 'g');
const numberRe = () => regex(W.values.number_re, 'g');
const citationRe = () => regex(W.values.citation_re, 'g');

// Combining marks of Latin text (what unicodedata.combining() drops after NFKD); explicit
// ranges because Unicode property escapes are not guaranteed on every Hermes build.
const COMBINING_RE = /[̀-ͯ᪰-᫿᷀-᷿⃐-⃿︠-︯]/g;

/** Lowercase, strip accents, collapse whitespace. */
export function normalizeText(text: string): string {
  const stripped = text.normalize('NFKD').replace(COMBINING_RE, '');
  return stripped.replace(/’/g, "'").replace(/\s+/g, ' ').trim().toLowerCase();
}

function canonicalTime(hour: string, minute: string, meridiem: string | undefined): string | null {
  let h = parseInt(hour, 10);
  const m = parseInt(minute, 10);
  if (meridiem) {
    const isPm = meridiem.toLowerCase().startsWith('p');
    if (h === 12) h = isPm ? 12 : 0;
    else if (isPm) h += 12;
  }
  if (h > 23 || m > 59) return null;
  return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
}

export function extractTimes(text: string): Set<string> {
  const found = new Set<string>();
  for (const match of text.matchAll(timeRe())) {
    const canonical = canonicalTime(match[1], match[2], match[3]);
    if (canonical) found.add(canonical);
  }
  return found;
}

/** Digit-only quantities, with time expressions and citation IDs removed first. */
export function extractNumbers(text: string): Set<string> {
  const cleaned = text.replace(citationRe(), ' ').replace(timeRe(), ' ');
  return new Set([...cleaned.matchAll(numberRe())].map((m) => m[0].replace(/[.,]/g, '')));
}

export function extractValues(text: string): Set<string> {
  return new Set([...extractTimes(text), ...extractNumbers(text)]);
}

export function escapeRegExp(text: string): string {
  return text.replace(/[.*+?^${}()|[\]\\/-]/g, '\\$&');
}

/** Whole-phrase match of a named (non-numeric) canonical value in free text. */
export function containsNamedValue(text: string, value: string): boolean {
  const pattern = new RegExp(`(?<!\\w)${escapeRegExp(normalizeText(value))}(?!\\w)`);
  return pattern.test(normalizeText(text));
}

export function extractCitations(text: string): string[] {
  return [...text.matchAll(citationRe())].map((m) => (m[1] || m[2] || '').toUpperCase());
}

export function isAbstention(text: string): boolean {
  const normalized = normalizeText(text);
  return ABSTAIN_PATTERNS.some((p) => normalized.includes(p));
}

export function stripEnumerations(text: string): string {
  return text
    .replace(regex(W.grounding.enum_line_re, 'g'), '$1')
    .replace(regex(W.grounding.enum_paren_re, 'g'), ' ');
}

/** Answer values that count as evidence (non-evidence rule applied). */
export function evidenceValues(text: string): Set<string> {
  const values = extractValues(stripEnumerations(text));
  return new Set(
    [...values].filter((v) => !(/^\d+$/.test(v) && parseInt(v, 10) < SMALL_NUMBER_LIMIT)),
  );
}
