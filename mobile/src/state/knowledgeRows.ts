// Knowledge chat rows -> the main chat's ChatRow (src/chat/ChatView.tsx). Pure, so the mapping is
// tested without React. A banner becomes its own assistant bubble above the reply.
import type { ChatRow } from '@/chat/ChatView';
import type { KnowledgeReply } from '@/core/knowledge/types';

import type { KnowledgeRow } from './knowledgeChat';

/** Placeholder attribution attached to smalltalk/editorial catalog entries; not a real source. */
const EDITORIAL_SOURCE = /^\s*texto editorial del asistente\b/i;

// Only the reply itself: the curated title stays out of the bubble (it read as a pasted heading),
// and the natural reply already carries the steps that matter.
function replyText(r: KnowledgeReply): string {
  return r.text;
}

/** `errorText` is the i18n copy for a failed question (the raw error stays out of the bubble). */
export function toChatRows(rows: readonly KnowledgeRow[], errorText: string): ChatRow[] {
  return rows.flatMap((row): ChatRow[] => {
    if (row.role === 'user') return [{
      id: row.id, role: 'user', text: row.text, ...(row.photoUri ? { photoUri: row.photoUri } : {}),
    }];
    if ('error' in row) return [{ id: row.id, role: 'assistant', text: errorText }];
    const { reply } = row;
    // An urgent banner is the emergency entry's `short`, under its one source id; a policy
    // banner has none.
    const bannerEntry = reply.banner?.sourceIds[0];
    const banner: ChatRow[] = reply.banner
      ? [
          {
            id: `${row.id}:banner`,
            role: 'assistant',
            text: reply.banner.text,
            ...(bannerEntry ? { entryId: bannerEntry } : {}),
          },
        ]
      : [];
    const realSources =
      reply.type === 'answer'
        ? reply.sources
            .filter((s) => !EDITORIAL_SOURCE.test(s.title))
            .map((s, i) => ({
              id: `${reply.id}#${i}`,
              ...s,
              ...(reply.verified ? { verified: true } : {}),
            }))
        : [];
    const sources = realSources.length ? realSources : undefined;
    return [
      ...banner,
      {
        id: row.id,
        role: 'assistant',
        text: replyText(reply),
        ...(row.keywords ? { keywords: row.keywords } : {}),
        ...(reply.type === 'answer' ? { entryId: reply.id } : {}),
        ...(row.timing ? { latencyMs: Math.max(1, Math.round(row.timing.totalMs)) } : {}),
        ...(sources ? { sources } : {}),
        ...(row.media ? { media: row.media } : {}),
      },
    ];
  });
}
