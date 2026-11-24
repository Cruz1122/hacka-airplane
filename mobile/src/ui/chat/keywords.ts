// Per-answer keywords set in bold (assets/data/knowledge-keywords.json, keyed by catalog id). Each
// is a verbatim, whole-word phrase of the entry's `short`; a test checks the file against the
// catalog, and one that stopped matching just shows plain.
import data from '@/../assets/data/knowledge-keywords.json';

const entries: Readonly<Record<string, readonly string[]>> = data.entries;
const NONE: readonly string[] = [];

/** The same array on every call (none: one shared empty one), so memoized bubbles stay put. */
export function keywordsFor(entryId: string | undefined): readonly string[] {
  return entryId !== undefined && Object.hasOwn(entries, entryId) ? entries[entryId] : NONE;
}
