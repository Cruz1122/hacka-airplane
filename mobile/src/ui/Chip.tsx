import { memo } from 'react';
import { Pressable, StyleSheet, Text } from 'react-native';

import { brand, spacing, type } from './theme/tokens';

export const Chip = memo(function Chip(p: {
  label: string;
  selected: boolean;
  onPress: () => void;
  hint?: string;
}) {
  return (
    <Pressable
      onPress={p.onPress}
      accessibilityRole="button"
      accessibilityState={{ selected: p.selected }}
      style={({ pressed }) => [
        styles.chip,
        p.selected && styles.selected,
        pressed && styles.pressed,
      ]}
    >
      <Text style={[styles.label, p.selected && styles.selectedText]}>{p.label}</Text>
      {p.hint ? (
        <Text style={[styles.hint, p.selected && styles.selectedText]}>{p.hint}</Text>
      ) : null}
    </Pressable>
  );
});

const styles = StyleSheet.create({
  chip: {
    minHeight: 44,
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: brand.cardShade,
    backgroundColor: brand.card,
    borderRadius: 12,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.sm,
    outlineColor: brand.primary,
  },
  selected: { backgroundColor: brand.ink, borderColor: brand.ink },
  pressed: { opacity: 0.8 },
  label: { ...type.caption, color: brand.ink },
  hint: { ...type.caption, color: brand.inkMuted },
  selectedText: { color: brand.onPrimary },
});
