// Workshop lab for messages: the real ChatBubble/TypingBubble on the chat sheet, with a
// replayable new-message entrance and the sources sheet, and the whole chat screen in each of its
// fixture states.
import { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { ChatView } from '@/chat/ChatView';
import { fill, t } from '@/i18n';
import { ChatBubble } from '@/ui/chat/ChatBubble';
import type { ChatSource } from '@/ui/chat/citations';
import { SourcesSheet } from '@/ui/chat/SourcesSheet';
import { TypingBubble } from '@/ui/chat/TypingBubble';
import { PET_NAME } from '@/ui/pet/petCore';

import {
  ActionButton,
  Choices,
  Entrance,
  Field,
  PhoneFrame,
  Stage,
  Toggle,
  type LabProps,
} from './chrome';
import { CHAT_STATES, READY, ROUTER_DRAFT, SOURCED, TALK } from './fixtures';

const w = t.dev.workshop;
const seconds = (ms?: number) =>
  ms != null ? fill(t.chatScreen.seconds, { s: (ms / 1000).toFixed(1) }) : undefined;
const noop = () => {};

export function BubblesLab({ wide, reducedMotion }: LabProps) {
  const [view, setView] = useState<'bubbles' | 'screen'>('bubbles');
  const [thread, setThread] = useState<'talk' | 'sources'>('talk');
  const [sheet, setSheet] = useState<ChatSource[] | null>(null);
  const [thinking, setThinking] = useState(false);
  const [replay, setReplay] = useState(0);
  const [screen, setScreen] = useState(CHAT_STATES[0].label);
  const state = CHAT_STATES.find((s) => s.label === screen) ?? CHAT_STATES[0];

  const messages = thread === 'talk' ? TALK : SOURCED;
  const last = messages.at(-1)!;
  const bubble = (m: (typeof messages)[number]) => (
    <ChatBubble
      key={m.id}
      role={m.role}
      text={m.text}
      meta={seconds(m.latencyMs)}
      sources={m.sources}
      onOpenSources={setSheet}
    />
  );
  const preview =
    view === 'bubbles' ? (
      <PhoneFrame height={wide ? 620 : 540}>
        <View style={styles.thread}>
          {messages.slice(0, -1).map(bubble)}
          <Entrance key={`${thread}-${replay}`} reducedMotion={reducedMotion}>
            {bubble(last)}
          </Entrance>
          {thinking && <TypingBubble label={fill(t.chatScreen.typing, { pet: PET_NAME })} />}
        </View>
        <SourcesSheet
          sources={sheet}
          onClose={() => setSheet(null)}
          reducedMotion={reducedMotion}
        />
      </PhoneFrame>
    ) : (
      <PhoneFrame height={780}>
        <ChatView
          messages={state.messages}
          busy={!!state.busy}
          draft={ROUTER_DRAFT}
          model={state.model ?? READY}
          steps={[]}
          state="ROUTER"
          sceneTime={null}
          onSend={noop}
          onReset={noop}
          onSettings={noop}
          onHistory={noop}
        />
      </PhoneFrame>
    );

  const controls = (
    <>
      <Field label={w.view}>
        <Choices
          value={view}
          onChange={setView}
          options={[
            { value: 'bubbles', label: w.bubbleView },
            { value: 'screen', label: w.screenView },
          ]}
        />
      </Field>
      {view === 'bubbles' ? (
        <>
          <Field label={w.thread}>
            <Choices
              value={thread}
              onChange={setThread}
              options={[
                { value: 'talk', label: w.threadTalk },
                { value: 'sources', label: w.threadSources },
              ]}
            />
          </Field>
          <Toggle label={w.thinking} value={thinking} onChange={setThinking} />
          <ActionButton icon="play" label={w.replay} onPress={() => setReplay((r) => r + 1)} />
        </>
      ) : (
        <Field label={w.screenState}>
          <Choices
            value={screen}
            onChange={setScreen}
            options={CHAT_STATES.map((s) => ({ value: s.label, label: s.label }))}
          />
        </Field>
      )}
    </>
  );

  return <Stage wide={wide} preview={preview} controls={controls} />;
}

const styles = StyleSheet.create({
  thread: { flex: 1, justifyContent: 'flex-end', paddingBottom: 16 },
});
