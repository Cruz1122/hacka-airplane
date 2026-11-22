import { FlashList } from '@shopify/flash-list';
import { Link } from 'expo-router';
import { memo, useCallback, useRef, useState } from 'react';
import { ActivityIndicator, KeyboardAvoidingView, Platform, Pressable, StyleSheet, Text, TextInput, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { useAssistant } from '@/state/useAssistant';
import { DebugPanel } from '@/ui/DebugPanel';
import { MessageRow } from '@/ui/MessageRow';
import { es } from '@/ui/strings';
import { useColors } from '@/ui/theme';
import { fontSize, radius, spacing } from '@/ui/theme/tokens';

type Msg = ReturnType<typeof useAssistant>['messages'][number];

// Owns the draft text so keystrokes re-render only this component, not the list.
const Composer = memo(function Composer({ disabled, onSend }: { disabled: boolean; onSend: (t: string) => void }) {
  const c = useColors();
  const [text, setText] = useState('');
  const submit = () => {
    if (!text.trim() || disabled) return;
    onSend(text);
    setText('');
  };
  return (
    <View style={styles.composer}>
      <TextInput
        value={text}
        onChangeText={setText}
        placeholder={es.inputPlaceholder}
        placeholderTextColor={c.textMuted}
        onSubmitEditing={submit}
        style={[styles.input, { color: c.text, borderColor: c.border, backgroundColor: c.surface }]}
      />
      <Pressable
        onPress={submit}
        disabled={disabled}
        style={[styles.send, { backgroundColor: c.primary, opacity: disabled ? 0.5 : 1 }]}
      >
        <Text style={{ color: c.onPrimary, fontSize: fontSize.md }}>{es.send}</Text>
      </Pressable>
    </View>
  );
});

const renderItem = ({ item }: { item: Msg }) => (
  <MessageRow role={item.role} text={item.text} latencyMs={item.latencyMs} />
);
const keyExtractor = (m: Msg) => m.id;

export default function ChatScreen() {
  const c = useColors();
  const insets = useSafeAreaInsets();
  const { messages, send, reset, busy, draft, state, lastSteps, model } = useAssistant();
  const list = useRef<React.ComponentRef<typeof FlashList<Msg>>>(null);
  const onSend = useCallback((t: string) => void send(t), [send]);

  const banner =
    model.status === 'ready'
      ? null
      : model.status === 'loading'
        ? es.modelLoading
        : model.status === 'missing'
          ? `${es.modelMissing}: ${model.id}`
          : `${es.modelError}: ${model.error ?? ''}`;

  return (
    <KeyboardAvoidingView
      style={{ flex: 1, backgroundColor: c.background, paddingBottom: insets.bottom }}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <View style={[styles.bar, { borderColor: c.border }]}>
        <Link href="/settings" style={{ color: c.primary }}>{es.settings}</Link>
        <Link href="/history" style={{ color: c.primary }}>{es.history}</Link>
        <Pressable onPress={reset}><Text style={{ color: c.primary }}>{es.reset}</Text></Pressable>
      </View>
      {banner && <Text style={{ color: model.status === 'error' ? c.danger : c.textMuted, padding: spacing.md }}>{banner}</Text>}
      <FlashList
        ref={list}
        data={messages}
        renderItem={renderItem}
        keyExtractor={keyExtractor}
        onContentSizeChange={() => list.current?.scrollToEnd({ animated: true })}
        keyboardShouldPersistTaps="handled"
        style={{ flex: 1 }}
      />
      {busy && (
        <View style={styles.busy}>
          <ActivityIndicator color={c.primary} />
          {/* Live model output of the routing/extraction step (JSON), so generation is visible. */}
          <Text style={[styles.draft, { color: c.textMuted }]} numberOfLines={3}>
            {draft || es.thinking}
          </Text>
        </View>
      )}
      <DebugPanel steps={lastSteps} state={state} />
      <Composer disabled={busy || model.status !== 'ready'} onSend={onSend} />
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  bar: { flexDirection: 'row', justifyContent: 'space-between', padding: spacing.md, borderBottomWidth: StyleSheet.hairlineWidth },
  busy: { flexDirection: 'row', gap: spacing.sm, padding: spacing.md, alignItems: 'center' },
  draft: { flex: 1, fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace', fontSize: 12 },
  composer: { flexDirection: 'row', gap: spacing.sm, padding: spacing.md },
  input: { flex: 1, borderWidth: 1, borderRadius: radius.md, paddingHorizontal: spacing.md, fontSize: fontSize.md },
  send: { borderRadius: radius.md, paddingHorizontal: spacing.lg, justifyContent: 'center' },
});
