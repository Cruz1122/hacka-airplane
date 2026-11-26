// React binding of KnowledgeChat. One store per app process, so the e5 context survives screen
// focus changes. The root layout starts it at launch (preloadKnowledge) so the models load while
// the onboarding plays; the chat reads the same store.
import { useSyncExternalStore } from 'react';

import type { KnowledgePatch } from '@/core/knowledge/qrPatch';
import { MEDIA } from '@/core/media/bundled';
import { degradedKnowledgeEngine, loadKnowledgeRuntime } from '@/llm/knowledgeRuntime';

import { KnowledgeChat, type KnowledgeChatState } from './knowledgeChat';
import { isKnowledgeOpenNow, loadParkAccess } from './parkAccess';
import { getVerifiedOnly, loadVerifiedOnly } from './verifiedOnly';

let store: KnowledgeChat | null = null;

function getStore(): KnowledgeChat {
  if (store) return store;
  // The saved switch loads with the models, so the first question already sees it.
  loadVerifiedOnly();
  loadParkAccess();
  store = new KnowledgeChat(
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
    { media: MEDIA, verifiedOnly: getVerifiedOnly, knowledgeOpen: isKnowledgeOpenNow },
  );
  return store;
}

/** Starts loading the knowledge runtime; later calls (and the chat) share that one load. */
export function preloadKnowledge(): void {
  getStore();
}

export function applyKnowledgePatch(patch: KnowledgePatch) {
  return getStore().applyPatches([patch], false);
}

export function applyKnowledgePatches(patches: readonly KnowledgePatch[]) {
  return getStore().applyPatches(patches);
}

export function useKnowledge(): KnowledgeChatState & {
  ask: (text: string, place?: string) => Promise<void>;
  askPhoto: KnowledgeChat['askPhoto'];
  reset: () => void;
} {
  const s = getStore();
  const state = useSyncExternalStore(s.subscribe, s.snapshot);
  return {
    ...state,
    ask: (t, place) => s.ask(t, place),
    askPhoto: (uri, caption, classify) => s.askPhoto(uri, caption, classify),
    reset: () => s.reset(),
  };
}
