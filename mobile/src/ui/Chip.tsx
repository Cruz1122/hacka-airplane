import { memo } from 'react';
import { Pressable, StyleSheet, Text } from 'react-native';

import { useColors } from './theme';
import { fontSize, radius, spacing } from './theme/tokens';

export const Chip = memo(function Chip(p: { label: string; selected: boolean; onPress: () => void; hint?: string }) {
  const c = useColors();
  return (
    <Pressable
      onPress={p.onPress}
      accessibilityRole="button"
      accessibilityState={{ selected: p.selected }}
      style={[styles.chip, { borderColor: p.selected ? c.primary : c.border, backgroundColor: p.selected ? c.primary : c.surface }]}
    >
      <Text style={{ color: p.selected ? c.onPrimary : c.text, fontSize: fontSize.md }}>{p.label}</Text>
      {p.hint ? <Text style={{ color: p.selected ? c.onPrimary : c.textMuted, fontSize: fontSize.sm }}>{p.hint}</Text> : null}
    </Pressable>
  );
});

const styles = StyleSheet.create({
  chip: { borderWidth: 1, borderRadius: radius.md, paddingHorizontal: spacing.md, paddingVertical: spacing.sm },
});
