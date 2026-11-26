import { useLocalSearchParams } from 'expo-router';
import { useCallback, useMemo } from 'react';

import { ChatView, type ChatModel } from '@/chat/ChatView';
import { t } from '@/i18n';
import { toChatRows } from '@/state/knowledgeRows';
import { useKnowledge } from '@/state/useKnowledge';
import { AppNavBar } from '@/ui/AppNavBar';

// The onboarding gate lives in the tabs layout (app/(tabs)/_layout.tsx).
export default function ChatScreen() {
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
      model={model}
      sceneTime={sceneTime ? Number(sceneTime) : null}
      fadeIn={sceneTime !== undefined}
      onSend={onSend}
      onReset={reset}
      nav={<AppNavBar active="chat" />}
    />
  );
}
