// Replies type themselves out word by word. Progress lives here, keyed by row id, not in the
// bubble: FlashList hands one cell to many rows, and a reply already read must stay whole when the
// chat mounts again. One frame loop serves every stream and keeps running with no bubble mounted,
// so a stream left mid-way ends on time.
import { useSyncExternalStore } from 'react';

import { replyDoc } from './markdown';

/** About as fast as a fast model streams tokens, counting a word and its whitespace as one. */
export const WORDS_PER_SECOND = 40;
const MS_PER_WORD = 1000 / WORDS_PER_SECOND;
/**
 * The frame loop moves the streams at most this often (~15 Hz), so a reply arrives in chunks of
 * two or three words, as a model's tokens do. Each move re-renders and re-lays out the bubble;
 * one per word (40 Hz) tripled the chat's long tasks on a throttled web run.
 */
const CHUNK_MS = 66;
const NO_KEYWORDS: readonly string[] = [];

interface Stream {
  start: number;
  words: number;
  /** Words on screen; `Infinity` once the whole reply is out. */
  shown: number;
}

const WHOLE: Stream = { start: -Infinity, words: 0, shown: Infinity };

export interface RevealRow {
  id: string;
  role: 'user' | 'assistant';
  text: string;
}

type Frame = (step: () => void) => void;

export class RevealStore {
  private readonly streams = new Map<string, Stream>();
  private readonly running = new Set<string>();
  private readonly listeners = new Set<() => void>();
  /** When the last scheduled stream ends; the next one waits for it. */
  private queueEnd = -Infinity;
  private ticking = false;
  private steppedAt = -Infinity;

  constructor(private readonly frame: Frame = (step) => requestAnimationFrame(step)) {}

  /**
   * Schedules each assistant row the store has not seen, in data order, so a banner types out
   * before its reply whatever order their cells mount in. Rows in `seen` (on screen when the chat
   * mounted: read before, or arrived while it was away) show whole.
   */
  schedule(rows: readonly RevealRow[], seen: ReadonlySet<string>, now: number): void {
    // Rows that left the chat (a new chat cleared it) stop holding the queue or memory.
    const ids = new Set(rows.map((r) => r.id));
    let added = false;
    for (const id of this.streams.keys()) {
      if (ids.has(id)) continue;
      this.streams.delete(id);
      this.running.delete(id);
      added = true;
    }
    this.queueEnd = -Infinity;
    for (const id of this.running) {
      const s = this.streams.get(id)!;
      this.queueEnd = Math.max(this.queueEnd, s.start + s.words * MS_PER_WORD);
    }
    for (const row of rows) {
      if (row.role !== 'assistant' || this.streams.has(row.id)) continue;
      added = true;
      if (seen.has(row.id)) {
        this.streams.set(row.id, WHOLE);
        continue;
      }
      const words = replyDoc(row.text, NO_KEYWORDS).stops.length;
      const start = Math.max(now, this.queueEnd);
      this.queueEnd = start + words * MS_PER_WORD;
      this.streams.set(row.id, { start, words, shown: 0 });
      this.running.add(row.id);
    }
    if (!added) return;
    this.advance(now);
    this.emit();
  }

  /** Moves every running stream to `now`. The frame loop calls it; tests call it directly. */
  step(now: number): void {
    this.steppedAt = now;
    if (this.advance(now)) this.emit();
  }

  private advance(now: number): boolean {
    let changed = false;
    for (const id of this.running) {
      const s = this.streams.get(id)!;
      const out = now < s.start ? 0 : 1 + Math.floor((now - s.start) / MS_PER_WORD);
      const shown = out >= s.words ? Infinity : out;
      if (shown === s.shown) continue;
      this.streams.set(id, { ...s, shown });
      if (shown === Infinity) this.running.delete(id);
      changed = true;
    }
    if (this.running.size > 0 && !this.ticking) this.tick();
    return changed;
  }

  private tick(): void {
    this.ticking = true;
    this.frame(() => {
      this.ticking = false;
      const now = performance.now();
      if (now - this.steppedAt >= CHUNK_MS) this.step(now);
      else if (this.running.size > 0) this.tick();
    });
  }

  private emit(): void {
    this.listeners.forEach((l) => l());
  }

  /** Words of row `id` on screen: 0 before its turn (or before it is scheduled). */
  shown = (id: string): number => this.streams.get(id)?.shown ?? 0;

  /** Whether row `id` is still typing out; `undefined` when it was never scheduled. */
  revealing = (id: string): boolean | undefined => {
    const s = this.streams.get(id);
    return s && s.shown !== Infinity;
  };

  /** Some reply is typing out or waiting for its turn. */
  busy = (): boolean => this.running.size > 0;

  subscribe = (listener: () => void) => {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  };
}

/** The app's one store: it outlives the chat screen like the knowledge chat itself does. */
export const replyReveal = new RevealStore();

/** Words of row `id` to show, or `Infinity` (all) without an id. */
export function useRevealedWords(id: string | undefined, store: RevealStore = replyReveal): number {
  const read = () => (id === undefined ? Infinity : store.shown(id));
  return useSyncExternalStore(store.subscribe, read, read);
}
