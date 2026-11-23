import { Redirect, router, useLocalSearchParams } from 'expo-router';
import { useCallback, useMemo } from 'react';

import { ChatView, type ChatModel } from '@/chat/ChatView';
import { t } from '@/i18n';
import { onboardingDone } from '@/onboarding/launch';
import { toChatRows } from '@/state/knowledgeRows';
import { useKnowledge } from '@/state/useKnowledge';

// The knowledge engine has no routing steps or live draft; ChatView's debug props stay empty.
const NO_STEPS: never[] = [];

export default function ChatRoute() {
  // Each launch starts on the onboarding, which replaces itself with this route when it ends.
  if (!onboardingDone()) return <Redirect href="/onboarding" />;
  return <ChatScreen />;
}

function ChatScreen() {
  const { rows, ask, reset, busy, status } = useKnowledge();
  // Set by the onboarding so the header continues its last frame exactly.
  const { sceneTime } = useLocalSearchParams<{ sceneTime?: string }>();
  const onSend = useCallback((text: string) => void ask(text), [ask]);
  const messages = useMemo(() => toChatRows(rows, t.knowledge.error), [rows]);
  // Degraded still answers urgent questions (safety rules need no model), so sending stays on.
  const model: ChatModel = { id: 'e5-base', status: status === 'loading' ? 'loading' : 'ready' };
  return (
    <ChatView
      messages={messages}
      busy={busy}
      draft=""
      model={model}
      steps={NO_STEPS}
      state=""
      sceneTime={sceneTime ? Number(sceneTime) : null}
      fadeIn={sceneTime !== undefined}
      onSend={onSend}
      onReset={reset}
      onSettings={() => router.push('/settings')}
      onHistory={() => router.push('/history')}
    />
  );
}
