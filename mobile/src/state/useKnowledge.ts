// React binding of KnowledgeChat. One store per app process, so the e5 context survives screen
// focus changes; it loads on first use.
import { useSyncExternalStore } from 'react';

import { degradedKnowledgeEngine, loadKnowledgeRuntime } from '@/llm/knowledgeRuntime';

import { KnowledgeChat, type KnowledgeChatState } from './knowledgeChat';

let store: KnowledgeChat | null = null;

function getStore(): KnowledgeChat {
  store ??= new KnowledgeChat(() =>
    loadKnowledgeRuntime().then(
      (rt) => ({ engine: rt.engine }),
      (cause: unknown) => ({
        engine: degradedKnowledgeEngine(cause),
        degraded: cause instanceof Error ? cause.message : String(cause),
      }),
    ),
  );
  return store;
}

export function useKnowledge(): KnowledgeChatState & {
  ask: (text: string) => Promise<void>;
  askPhoto: KnowledgeChat['askPhoto'];
  reset: () => void;
} {
  const s = getStore();
  const state = useSyncExternalStore(s.subscribe, s.snapshot);
  return {
    ...state,
    ask: (t) => s.ask(t),
    askPhoto: (uri, caption, classify) => s.askPhoto(uri, caption, classify),
    reset: () => s.reset(),
  };
}
