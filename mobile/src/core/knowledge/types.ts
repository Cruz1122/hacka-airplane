// Contract between the knowledge engine and the chat UI. Pure types; no React/RN imports.
// Design: docs/history/phase3-architecture.md §2. The engine never states a fact that is not a curated answer.

export type EntryKind = 'faq' | 'action' | 'emergency';

export interface Source {
  title: string;
  url?: string;
  date?: string;
}

/** Fixed notice shown ABOVE the reply (urgent safety or "offline, can't confirm today's status"). */
export interface Banner {
  kind: 'urgent_safety' | 'offline_current_status';
  text: string;
  sourceIds: string[];
}

/**
 * Top-1 policy (user decision 2026-11-22): one curated answer or an abstain text, never a menu.
 * Every text is a curated catalog field or a policy text, verbatim.
 */
export type KnowledgeReply =
  | {
      type: 'abstain';
      banner?: Banner;
      text: string; // ask to rephrase
    }
  | {
      type: 'answer';
      banner?: Banner;
      id: string;
      title: string;
      text: string; // curated answer.short, verbatim
      steps?: string[];
      sources: Source[];
      reviewed?: string; // last_verified date
      /** The entry comes from the official UTON guion (catalog verified_by_uton): the chat shows a seal. */
      verified: boolean;
    };

export interface KnowledgeTiming {
  rulesMs: number;
  embedMs: number;
  retrieveMs: number;
  rerankMs: number;
  totalMs: number;
}
