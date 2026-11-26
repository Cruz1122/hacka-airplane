import { Redirect, router, useLocalSearchParams } from 'expo-router';
import { useCallback, useMemo } from 'react';

import { ChatView, type ChatModel } from '@/chat/ChatView';
import { t } from '@/i18n';
import { onboardingDone } from '@/onboarding/launch';
import { toChatRows } from '@/state/knowledgeRows';
import { useKnowledge } from '@/state/useKnowledge';

const NO_STEPS: never[] = [];

export default function ChatRoute() {
  if (!onboardingDone()) return <Redirect href="/onboarding" />;
  return <ChatScreen />;
}

function ChatScreen() {
  const { rows, ask, reset, busy, status } = useKnowledge();
  const { sceneTime } = useLocalSearchParams<{ sceneTime?: string }>();
  const onSend = useCallback((text: string) => void ask(text), [ask]);
  const messages = useMemo(() => toChatRows(rows, t.knowledge.error), [rows]);
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
      aboveTabBar
      onSend={onSend}
      onReset={reset}
      onSettings={() => router.push('/settings')}
      onHistory={() => router.push('/history')}
    />
  );
}
