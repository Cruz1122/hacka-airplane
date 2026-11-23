// Chat state for the knowledge engine (top-1 curated answers). Plain store so it is testable
// without React; useKnowledge.ts subscribes to it. Never touches modelManager: e5 has its own context.
import type { KnowledgeEngine } from '@/core/knowledge';
import type { KnowledgeReply, KnowledgeTiming } from '@/core/knowledge/types';

export type KnowledgeRow =
  | { id: string; role: 'user'; text: string }
  | { id: string; role: 'assistant'; reply: KnowledgeReply; timing?: KnowledgeTiming }
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

const message = (e: unknown) => (e instanceof Error ? e.message : String(e));

export class KnowledgeChat {
  private state: KnowledgeChatState = { rows: [], busy: false, status: 'loading' };
  private readonly listeners = new Set<() => void>();
  private readonly engine: Promise<Engine>;
  private seq = 0;

  constructor(load: () => Promise<LoadedEngine>) {
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
      this.push({ id: this.id(), role: 'assistant', reply: r.reply, timing: r.timing }, false);
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
