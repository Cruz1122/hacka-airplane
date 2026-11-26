import { memo } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { useColors } from './theme';
import { fontSize, radius, spacing } from './theme/tokens';

interface Props {
  role: 'user' | 'assistant';
  text: string;
  latencyMs?: number;
}

// Memoized on primitives so typing in the input never re-renders existing rows.
export const MessageRow = memo(function MessageRow({ role, text, latencyMs }: Props) {
  const c = useColors();
  const mine = role === 'user';
  return (
    <View style={[styles.row, mine ? styles.right : styles.left]}>
      <View style={[styles.bubble, { backgroundColor: mine ? c.primary : c.surface }]}>
        <Text style={{ color: mine ? c.onPrimary : c.text, fontSize: fontSize.md }}>{text}</Text>
      </View>
      {latencyMs != null && (
        <Text style={[styles.meta, { color: c.textMuted }]}>
          {(latencyMs / 1000).toFixed(1)} s
        </Text>
      )}
    </View>
  );
});

const styles = StyleSheet.create({
  row: { paddingHorizontal: spacing.lg, paddingVertical: spacing.xs },
  left: { alignItems: 'flex-start' },
  right: { alignItems: 'flex-end' },
  bubble: { maxWidth: '85%', borderRadius: radius.md, padding: spacing.md },
  meta: { fontSize: fontSize.sm, marginTop: 2 },
});
