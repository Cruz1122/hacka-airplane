// Workshop lab for the chat input bar: the real ChatComposer at the bottom of a chat sheet, with
// live typing and sending, content presets, both appearances and a replayable entrance.
import { useEffect, useRef, useState, type ComponentRef } from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';

import type { ChatRow } from '@/chat/ChatView';
import { fill, t } from '@/i18n';
import { ChatBubble } from '@/ui/chat/ChatBubble';
import { ChatComposer, type ComposerVariant } from '@/ui/chat/ChatComposer';
import { TypingBubble } from '@/ui/chat/TypingBubble';
import { PET_NAME } from '@/ui/pet/petCore';

import {
  ActionButton,
  Choices,
  Entrance,
  Field,
  PhoneFrame,
  Stage,
  Status,
  type LabProps,
} from './chrome';
import { COMPOSER_TEXT, DEMO_REPLY, DEMO_SEND_MS, TALK } from './fixtures';

const w = t.dev.workshop;

type Preset = 'empty' | 'typing' | 'long' | 'pending';

/** What the demo composer is doing. The draft itself lives in the composer, not here. */
type ComposerDemo =
  | { kind: 'idle' }
  | { kind: 'typing'; text: string }
  | { kind: 'sending'; text: string }
  | { kind: 'disabled'; text: string };

const PRESETS: Record<Preset, ComposerDemo> = {
  empty: { kind: 'idle' },
  typing: { kind: 'typing', text: COMPOSER_TEXT.typing },
  long: { kind: 'typing', text: COMPOSER_TEXT.long },
  pending: { kind: 'disabled', text: COMPOSER_TEXT.pending },
};

const STATE_LABEL: Record<ComposerDemo['kind'], string> = {
  idle: w.stateIdle,
  typing: w.stateTyping,
  sending: w.stateSending,
  disabled: w.stateDisabled,
};

const START: ChatRow[] = TALK.slice(0, 2);
/** Docked: the base strip stands in for a phone's bottom inset. */
const DEMO_FLOOR = 14;

export function ComposerLab({ wide, reducedMotion }: LabProps) {
  const [variant, setVariant] = useState<ComposerVariant>('docked');
  const [preset, setPreset] = useState<Preset>('empty');
  const [demo, setDemo] = useState<ComposerDemo>(PRESETS.empty);
  const [rows, setRows] = useState<ChatRow[]>(START);
  const [lastSent, setLastSent] = useState<string | null>(null);
  const [hasDraft, setHasDraft] = useState(false);
  // Bumped to remount the composer: applies a preset's text and replays the entrance.
  const [mount, setMount] = useState(0);
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const list = useRef<ComponentRef<typeof ScrollView>>(null);

  const stopTimer = () => {
    if (timer.current) clearTimeout(timer.current);
    timer.current = null;
  };
  useEffect(() => stopTimer, []);

  const applyPreset = (p: Preset) => {
    stopTimer();
    setPreset(p);
    setDemo(PRESETS[p]);
    setMount((m) => m + 1);
  };
  const reset = () => {
    stopTimer();
    setRows(START);
    setLastSent(null);
    applyPreset('empty');
  };
  const send = (text: string) => {
    setDemo({ kind: 'sending', text });
    setLastSent(text);
    setRows((r) => [...r, { id: `u${r.length}`, role: 'user', text }]);
    stopTimer();
    timer.current = setTimeout(() => {
      timer.current = null;
      setRows((r) => [...r, { id: `a${r.length}`, role: 'assistant', text: DEMO_REPLY }]);
      setDemo({ kind: 'idle' });
    }, DEMO_SEND_MS);
  };

  const composer = (
    <ChatComposer
      key={`${variant}:${mount}`}
      variant={variant}
      disabled={demo.kind === 'sending' || demo.kind === 'disabled'}
      initialText={demo.kind === 'typing' || demo.kind === 'disabled' ? demo.text : undefined}
      placeholder={t.inputPlaceholder}
      sendLabel={t.send}
      onSend={send}
      onHasTextChange={setHasDraft}
      floor={DEMO_FLOOR}
      reducedMotion={reducedMotion}
    />
  );

  const preview = (
    <PhoneFrame height={wide ? 620 : 540}>
      <ScrollView
        ref={list}
        style={styles.list}
        contentContainerStyle={styles.listContent}
        onContentSizeChange={() => list.current?.scrollToEnd({ animated: !reducedMotion })}
      >
        {rows.map((row) => (
          <ChatBubble key={row.id} role={row.role} text={row.text} />
        ))}
        {demo.kind === 'sending' && (
          <TypingBubble label={fill(t.chatScreen.typing, { pet: PET_NAME })} />
        )}
      </ScrollView>
      <Entrance key={`${variant}:${mount}`} reducedMotion={reducedMotion} lift={16}>
        {variant === 'docked' ? composer : <View style={styles.floatingGap}>{composer}</View>}
      </Entrance>
    </PhoneFrame>
  );

  const controls = (
    <>
      <Field label={w.appearance}>
        <Choices
          value={variant}
          onChange={setVariant}
          options={[
            { value: 'docked', label: w.docked },
            { value: 'floating', label: w.floating },
          ]}
        />
      </Field>
      <Field label={w.sample}>
        <Choices
          value={preset}
          onChange={applyPreset}
          options={[
            { value: 'empty', label: w.presetEmpty },
            { value: 'typing', label: w.presetTyping },
            { value: 'long', label: w.presetLong },
            { value: 'pending', label: w.presetPending },
          ]}
        />
      </Field>
      <Field label={w.state}>
        <Status>
          {
            STATE_LABEL[
              demo.kind === 'idle' || demo.kind === 'typing'
                ? hasDraft
                  ? 'typing'
                  : 'idle'
                : demo.kind
            ]
          }
        </Status>
        <Status>{lastSent ? fill(w.lastSent, { text: lastSent }) : w.nothingSent}</Status>
      </Field>
      <View style={styles.actions}>
        <ActionButton icon="play" label={w.replay} onPress={() => setMount((m) => m + 1)} />
        <ActionButton icon="rotateCcw" label={w.reset} onPress={reset} />
      </View>
    </>
  );

  return <Stage wide={wide} preview={preview} controls={controls} />;
}

const styles = StyleSheet.create({
  list: { flex: 1 },
  listContent: { paddingTop: 16, paddingBottom: 8 },
  // The chat pads the floating pill off the bottom edge the same way.
  floatingGap: { paddingTop: 4, paddingBottom: 12 },
  actions: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
});
