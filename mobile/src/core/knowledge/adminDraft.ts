import type { CatalogEntry, DepthEntry } from './assets';
import type { QrEntry } from './qrPatch';
import { foldAccents } from './safety';

export type ListField = 'questions' | 'variants' | 'steps' | 'more' | 'why' | 'sources';
export type Draft = Pick<QrEntry, 'section' | 'title' | 'answer'> &
  Record<ListField, string> & { id: string; related: string[] };

const lines = (text: string) =>
  text
    .split(/\r?\n/)
    .map((item) => item.trim())
    .filter(Boolean);

export const emptyDraft = (section: string, id = ''): Draft => ({
  id,
  section,
  title: '',
  answer: '',
  questions: '',
  variants: '',
  steps: '',
  more: '',
  why: '',
  related: [],
  sources: '',
});

export function prepareDraft(draft: Draft): Draft {
  const title = draft.title.trim();
  if (!title) return draft;
  const slug = foldAccents(title)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '')
    .slice(0, 65);
  return {
    ...draft,
    id: draft.id.trim() || (slug ? draft.section + '.' + slug : ''),
    questions: draft.questions.trim() || title,
  };
}

export function draftFromEntry(id: string, entry: QrEntry): Draft {
  const { section, title, answer, questions, variants, steps, more, why, related, sources } = entry;
  return {
    id,
    section,
    title,
    answer,
    questions: questions.join('\n'),
    variants: variants.join('\n'),
    steps: steps.join('\n'),
    more: more.join('\n'),
    why: why.join('\n'),
    related: [...related],
    sources: sources.map(({ label, url }) => label + ' | ' + url).join('\n'),
  };
}

export function draftFromCatalog(entry: CatalogEntry, depth?: DepthEntry): Draft {
  return draftFromEntry(entry.id, {
    section: entry.section,
    title: entry.label,
    answer: entry.short,
    questions: [entry.label],
    variants: [
      ...new Set((depth?.l0 ?? []).map(({ text }) => text).filter((text) => text !== entry.short)),
    ],
    steps: entry.steps.map((step) => (Array.isArray(step) ? step.join(' ') : step)),
    more: (depth?.layers ?? [])
      .filter(({ kind }) => kind !== 'why')
      .flatMap(({ texts }) => texts.slice(0, 1).map(({ text }) => text))
      .slice(0, 5),
    why: (depth?.layers ?? [])
      .filter(({ kind }) => kind === 'why')
      .flatMap(({ texts }) => texts.slice(0, 1).map(({ text }) => text))
      .slice(0, 3),
    related: (depth?.walk ?? []).slice(0, 5),
    sources: entry.sources
      .flatMap(({ label, url }) => (url?.startsWith('https://') ? [{ label, url }] : []))
      .slice(0, 3),
  });
}

export function entryFromDraft(draft: Draft, sourceError: string): QrEntry {
  return {
    section: draft.section,
    title: draft.title.trim(),
    answer: draft.answer.trim(),
    questions: lines(draft.questions),
    variants: lines(draft.variants),
    steps: lines(draft.steps),
    more: lines(draft.more),
    why: lines(draft.why),
    related: draft.related.filter((id) => id !== draft.id),
    sources: lines(draft.sources).map((row) => {
      const split = row.indexOf('|');
      if (split === -1) throw new Error(sourceError);
      return { label: row.slice(0, split).trim(), url: row.slice(split + 1).trim() };
    }),
  };
}
