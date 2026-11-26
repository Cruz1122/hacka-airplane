// Tumak as a floating bubble: the same chat as the Chat tab, opened from a stage without leaving it.
import { useEffect, useMemo, useRef, useState, type ComponentRef } from 'react';
import { Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { fill, t } from '@/i18n';
import { es } from '@/i18n/es';
import { toChatRows } from '@/state/knowledgeRows';
import { useKnowledge } from '@/state/useKnowledge';
import { BottomSheet } from '@/ui/BottomSheet';
import { ChatBubble } from '@/ui/chat/ChatBubble';
import { ChatComposer } from '@/ui/chat/ChatComposer';
import { TypingBubble } from '@/ui/chat/TypingBubble';
import { Icon } from '@/ui/icons/Icon';
import { PET_FACE_VIEWBOX, PET_NAME } from '@/ui/pet/petCore';
import { PetStill } from '@/ui/pet/PetStill';
import { spacing, type } from '@/ui/theme/tokens';
import { useAccessibilityTheme } from '@/ui/useAccessibilityTheme';

import type { StationId } from './stations';

export const STAGE_FAB = 64;

export function StageTumak({ id, insetBottom }: { id: StationId; insetBottom: number }) {
  const [open, setOpen] = useState(false);
  const { palette, borderWidth } = useAccessibilityTheme();
  return (
    <>
      {open ? null : (
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={fill(t.trail.tumak.open, { pet: PET_NAME })}
          onPress={() => setOpen(true)}
          style={[
            styles.fab,
            {
              bottom: insetBottom,
              backgroundColor: palette.primary,
              borderColor: palette.card,
              borderWidth,
            },
          ]}
        >
          <PetStill size={46} emotion="curious" crop={PET_FACE_VIEWBOX} mirror={1} />
        </Pressable>
      )}
      <BottomSheet open={open} onClose={() => setOpen(false)} bottom={insetBottom}>
        {(close) => <StageChat id={id} onClose={close} />}
      </BottomSheet>
    </>
  );
}

function StageChat({ id, onClose }: { id: StationId; onClose: () => void }) {
  const { palette, scaled } = useAccessibilityTheme();
  const { rows, busy, status, ask } = useKnowledge();
  const messages = useMemo(() => toChatRows(rows, t.knowledge.error), [rows]);
  const scroll = useRef<ComponentRef<typeof ScrollView>>(null);
  useEffect(() => {
    scroll.current?.scrollToEnd({ animated: true });
  }, [messages.length, busy]);
  const greeting = fill(t.chatScreen.greeting, { pet: PET_NAME });
  const keywords = t.chatScreen.greetingKeywords.map((keyword) => fill(keyword, { pet: PET_NAME }));
  return (
    <View style={styles.chat}>
      <View style={styles.head}>
        <Text
          style={[styles.title, scaled.label, { color: palette.ink }]}
          accessibilityRole="header"
        >
          {fill(t.trail.tumak.title, { pet: PET_NAME })}
        </Text>
        <Pressable
          accessibilityRole="button"
          accessibilityLabel={fill(t.trail.tumak.close, { pet: PET_NAME })}
          onPress={onClose}
          hitSlop={8}
          style={styles.close}
        >
          <Icon name="x" size={20} color={palette.ink} />
        </Pressable>
      </View>
      <ScrollView
        ref={scroll}
        style={styles.transcript}
        contentContainerStyle={styles.transcriptContent}
      >
        <ChatBubble role="assistant" text={greeting} keywords={keywords} />
        {messages.map((item) => (
          <ChatBubble
            key={item.id}
            role={item.role}
            text={item.text}
            photoUri={item.photoUri}
            keywords={item.keywords}
            entryId={item.entryId}
            sources={item.sources}
            media={item.media}
          />
        ))}
        {busy ? <TypingBubble label={fill(t.chatScreen.typing, { pet: PET_NAME })} /> : null}
      </ScrollView>
      <ChatComposer
        disabled={busy || status === 'loading'}
        placeholder={t.inputPlaceholder}
        sendLabel={t.send}
        onSend={(text) =>
          void ask(text, fill(es.trail.tumak.context, { place: es.trail.stations[id].name }))
        }
      />
    </View>
  );
}

const styles = StyleSheet.create({
  fab: {
    position: 'absolute',
    right: spacing.lg,
    width: STAGE_FAB,
    height: STAGE_FAB,
    borderRadius: STAGE_FAB / 2,
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    zIndex: 5,
  },
  chat: { height: 420, paddingHorizontal: spacing.md },
  head: {
    minHeight: 44,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  title: { ...type.label, flex: 1 },
  close: {
    width: 44,
    height: 44,
    alignItems: 'center',
    justifyContent: 'center',
  },
  transcript: { flex: 1 },
  transcriptContent: { paddingBottom: spacing.md, gap: spacing.sm },
});
