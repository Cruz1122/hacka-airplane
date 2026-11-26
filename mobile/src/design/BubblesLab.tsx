// Workshop lab for messages: the real ChatBubble/TypingBubble on the chat sheet, with a
// replayable last reply (entrance and word-by-word reveal, keywords in bold) and the sources
// sheet, and the whole chat screen in each of its fixture states.
import { useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { ChatView, type ChatRow } from '@/chat/ChatView';
import { fill, t } from '@/i18n';
import { ChatBubble } from '@/ui/chat/ChatBubble';
import type { ChatSource } from '@/ui/chat/citations';
import { keywordsFor } from '@/ui/chat/keywords';
import { revealRows } from '@/ui/chat/MediaGallery';
import { replyReveal } from '@/ui/chat/reveal';
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
import { CHAT_STATES, PHOTO_THREADS, READY, SOURCED, TALK, URGENT } from './fixtures';

const w = t.dev.workshop;
const seconds = (ms?: number) =>
  ms != null ? fill(t.chatScreen.seconds, { s: (ms / 1000).toFixed(1) }) : undefined;
const noop = () => {};
const THREADS = { talk: TALK, sources: SOURCED, urgent: URGENT, photos: PHOTO_THREADS.single };
const NOTHING_SEEN = new Set<string>();

export function BubblesLab({ wide, reducedMotion }: LabProps) {
  const [view, setView] = useState<'bubbles' | 'screen'>('bubbles');
  const [thread, setThread] = useState<keyof typeof THREADS>('talk');
  // The photos thread shows one gallery layout at a time, so its turn fits the frame and replays.
  const [gallery, setGallery] = useState<keyof typeof PHOTO_THREADS>('single');
  const [sheet, setSheet] = useState<ChatSource[] | null>(null);
  const [thinking, setThinking] = useState(false);
  // 0 shows the thread as read; each replay types its last turn out again under fresh row ids.
  const [replay, setReplay] = useState(0);
  const [screen, setScreen] = useState(CHAT_STATES[0].label);
  const state = CHAT_STATES.find((s) => s.label === screen) ?? CHAT_STATES[0];

  const messages = thread === 'photos' ? PHOTO_THREADS[gallery] : THREADS[thread];
  // The last turn: the assistant rows after the last question (a banner and its reply).
  const turn = messages.findLastIndex((m) => m.role === 'user') + 1;
  const replayId = (m: ChatRow, n: number) => `lab/${thread}/${m.id}/${n}`;
  const replayTurn = () => {
    const n = replay + 1;
    const rows = messages.slice(turn).map((m) => ({ ...m, id: replayId(m, n) }));
    replyReveal.schedule(revealRows(rows), NOTHING_SEEN, performance.now());
    setReplay(n);
  };
  const pickThread = (next: keyof typeof THREADS) => {
    setThread(next);
    setReplay(0);
  };
  const pickGallery = (next: keyof typeof PHOTO_THREADS) => {
    setGallery(next);
    setReplay(0);
  };
  const bubble = (m: ChatRow, revealId?: string) => (
    <ChatBubble
      key={m.id}
      role={m.role}
      text={m.text}
      meta={seconds(m.latencyMs)}
      sources={m.sources}
      onOpenSources={setSheet}
      keywords={keywordsFor(m.entryId)}
      revealId={revealId}
      media={m.media}
    />
  );
  const preview =
    view === 'bubbles' ? (
      <PhoneFrame height={wide ? 620 : 540}>
        <View style={styles.thread}>
          {messages.slice(0, turn).map((m) => bubble(m))}
          <Entrance key={`${thread}-${gallery}-${replay}`} reducedMotion={reducedMotion}>
            {messages
              .slice(turn)
              .map((m) => bubble(m, replay > 0 ? replayId(m, replay) : undefined))}
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
          // A fresh mount per state: its rows count as read, so switching never replays them.
          key={screen}
          messages={state.messages}
          busy={!!state.busy}
          model={state.model ?? READY}
          sceneTime={null}
          onSend={noop}
          onReset={noop}
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
              onChange={pickThread}
              options={[
                { value: 'talk', label: w.threadTalk },
                { value: 'sources', label: w.threadSources },
                { value: 'urgent', label: w.threadUrgent },
                { value: 'photos', label: w.threadPhotos },
              ]}
            />
          </Field>
          {thread === 'photos' && (
            <Field label={w.gallery}>
              <Choices
                value={gallery}
                onChange={pickGallery}
                options={[
                  { value: 'single', label: w.gallerySingle },
                  { value: 'rows', label: w.galleryRows },
                  { value: 'columns', label: w.galleryColumns },
                ]}
              />
            </Field>
          )}
          <Toggle label={w.thinking} value={thinking} onChange={setThinking} />
          <ActionButton icon="play" label={w.replayReply} onPress={replayTurn} />
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
