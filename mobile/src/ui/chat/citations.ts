// Citation markers in the assistant's text. The driver quotes passages as `... [fuente: EST-A-01]`
// and asks the model for the same syntax (src/core/driver.ts); the bubble shows the prose without
// them and lists the sources behind a button. Only that syntax is a marker: any other bracket, like
// the driver's `[trámite: admite datos parciales]`, is prose and stays.
import type { Source } from '@/core/knowledge/types';

/** One reference behind an assistant message, already resolved from canonical data. */
export interface ChatSource extends Source {
  /** Passage or catalog id; unique within a message. */
  id: string;
  /** The passage the answer rests on, verbatim, when the source has no link to open. */
  excerpt?: string;
}

const ID = /^[A-Z]{2,5}(?:-[A-Z0-9]{1,4})+$/;
const SEPARATOR = /\s*(?:[,;]|\by\b)\s*/;
const MARKER = /[ \t]*\[\s*fuentes?\s*:\s*([^[\]]*?)\s*\]/giu;
/** An unclosed marker at the end of streamed text: `[`, `[fue`, `[fuente: EST-A`. */
const PARTIAL = /[ \t]*\[\s*(?:f(?:u(?:e(?:n(?:t(?:e(?:s?\s*(?::[^[\]]*)?)?)?)?)?)?)?)?$/iu;

function markerIds(list: string): string[] | null {
  const ids = list.split(SEPARATOR).filter(Boolean);
  return ids.length > 0 && ids.every((id) => ID.test(id)) ? ids : null;
}

/**
 * The text to show, without citation markers or a trailing half-written one, and the ids those
 * markers cite, first mention first and each once.
 */
export function parseCitations(text: string): { prose: string; ids: string[] } {
  const ids = new Set<string>();
  const prose = text
    .replace(MARKER, (marker, list: string) => {
      const cited = markerIds(list);
      if (!cited) return marker;
      cited.forEach((id) => ids.add(id));
      return '';
    })
    .replace(PARTIAL, '')
    // A marker on a line of its own would leave a blank line under the answer.
    .trim();
  return { prose, ids: [...ids] };
}
