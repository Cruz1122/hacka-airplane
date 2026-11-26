// React binding of KnowledgeChat. One store per app process, so the e5 context survives screen
// focus changes. The root layout starts it at launch (preloadKnowledge) so the models load while
// the onboarding plays; the chat reads the same store.
import { useSyncExternalStore } from 'react';

import { MEDIA } from '@/core/media/bundled';
import { degradedKnowledgeEngine, loadKnowledgeRuntime } from '@/llm/knowledgeRuntime';

import { KnowledgeChat, type KnowledgeChatState } from './knowledgeChat';

let store: KnowledgeChat | null = null;

function getStore(): KnowledgeChat {
  store ??= new KnowledgeChat(
    () =>
      loadKnowledgeRuntime().then(
        (rt) => ({ engine: rt.engine }),
        (cause: unknown) => {
          console.warn('Knowledge runtime failed to load; only the safety rules answer.', cause);
          return {
            engine: degradedKnowledgeEngine(cause),
            degraded: cause instanceof Error ? cause.message : String(cause),
          };
        },
      ),
    { media: MEDIA },
  );
  return store;
}

/** Starts loading the knowledge runtime; later calls (and the chat) share that one load. */
export function preloadKnowledge(): void {
  getStore();
}

export function useKnowledge(): KnowledgeChatState & {
  ask: (text: string) => Promise<void>;
  reset: () => void;
} {
  const s = getStore();
  const state = useSyncExternalStore(s.subscribe, s.snapshot);
  return {
    ...state,
    ask: (t) => s.ask(t),
    reset: () => s.reset(),
  };
}
