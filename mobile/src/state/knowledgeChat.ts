// Chat state for the knowledge engine (top-1 curated answers). Plain store so it is testable
// without React; useKnowledge.ts subscribes to it. Never touches modelManager: e5 has its own context.
import type { KnowledgeEngine } from '@/core/knowledge';
import type { KnowledgeReply, KnowledgeTiming } from '@/core/knowledge/types';
import { pickMedia, type MediaCatalog, type MediaPick } from '@/core/media/media';

export type KnowledgeRow =
  | { id: string; role: 'user'; text: string }
  | {
      id: string;
      role: 'assistant';
      reply: KnowledgeReply;
      timing?: KnowledgeTiming;
      /** Photos under the answer, decided once when the reply arrived. */
      media?: MediaPick;
    }
  | { id: string; role: 'assistant'; error: string };

export interface KnowledgeChatState {
  rows: KnowledgeRow[];
  busy: boolean;
  status: 'loading' | 'ready' | 'degraded';
  /** Why the runtime is degraded (missing side-loaded file, native load error). */
  error?: string;
}

type Engine = Pick<KnowledgeEngine, 'ask'> & Partial<Pick<KnowledgeEngine, 'resetContext'>>;
export interface LoadedEngine {
  engine: Engine;
  degraded?: string;
}

export interface KnowledgeChatOptions {
  /** Photos answers may show; without it no answer shows any. */
  media?: MediaCatalog;
  /** The dice for photos, in [0, 1). */
  rng?: () => number;
}

const message = (e: unknown) => (e instanceof Error ? e.message : String(e));

export class KnowledgeChat {
  private state: KnowledgeChatState = { rows: [], busy: false, status: 'loading' };
  private readonly listeners = new Set<() => void>();
  private readonly engine: Promise<Engine>;
  private readonly media: MediaCatalog | undefined;
  private readonly rng: () => number;
  private seq = 0;

  constructor(
    load: () => Promise<LoadedEngine>,
    { media, rng = Math.random }: KnowledgeChatOptions = {},
  ) {
    this.media = media;
    this.rng = rng;
    this.engine = load().then(({ engine, degraded }) => {
      this.set({ status: degraded ? 'degraded' : 'ready', ...(degraded ? { error: degraded } : {}) });
      return engine;
    });
  }

  snapshot = (): KnowledgeChatState => this.state;

  subscribe = (fn: () => void): (() => void) => {
    this.listeners.add(fn);
    return () => this.listeners.delete(fn);
  };

  async ask(text: string): Promise<void> {
    const q = text.trim();
    if (!q || this.state.busy) return;
    this.push({ id: this.id(), role: 'user', text: q }, true);
    try {
      const r = await (await this.engine).ask(q);
      const media = this.mediaFor(r.reply, q);
      this.push(
        {
          id: this.id(),
          role: 'assistant',
          reply: r.reply,
          timing: r.timing,
          ...(media ? { media } : {}),
        },
        false,
      );
    } catch (e) {
      this.push({ id: this.id(), role: 'assistant', error: message(e) }, false);
    }
  }

  /** Clears the chat and the engine's follow-up context, so the next question stands alone. */
  reset(): void {
    this.set({ rows: [], busy: false });
    // A load failure already surfaced through ask(); nothing to reset then.
    void this.engine.then(
      (e) => e.resetContext?.(),
      () => undefined,
    );
  }

  /**
   * Answers only. The banner row itself never shows photos (toChatRows); an urgent reply shows
   * none at all, while one under the offline-status notice still may.
   */
  private mediaFor(reply: KnowledgeReply, userText: string): MediaPick | null {
    if (!this.media || reply.type !== 'answer' || reply.banner?.kind === 'urgent_safety') {
      return null;
    }
    const previous = this.state.rows.findLast((r) => r.role === 'assistant');
    const afterMedia =
      previous !== undefined && 'reply' in previous && previous.media !== undefined;
    return pickMedia(this.media, { topicId: reply.id, userText, afterMedia }, this.rng);
  }

  private id(): string {
    return `k${++this.seq}`;
  }

  private push(row: KnowledgeRow, busy: boolean): void {
    this.set({ rows: [...this.state.rows, row], busy });
  }

  private set(patch: Partial<KnowledgeChatState>): void {
    this.state = { ...this.state, ...patch };
    this.listeners.forEach((fn) => fn());
  }
}
