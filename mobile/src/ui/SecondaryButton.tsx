// Secondary action: a card surface with an ink edge and ink label, 44 pt tall. Sits beside or
// under the screen's main content without competing with `PrimaryButton`.
import { useState } from 'react';
import { Pressable, StyleSheet, Text } from 'react-native';

import { brand, spacing, type } from './theme/tokens';

export const SECONDARY_BUTTON_HEIGHT = 44;

export interface SecondaryButtonProps {
  label: string;
  onPress: () => void;
  /** What pressing it does, for screen readers. */
  hint?: string;
}

export function SecondaryButton({ label, onPress, hint }: SecondaryButtonProps) {
  const [focused, setFocused] = useState(false);
  return (
    <Pressable
      accessibilityRole="button"
      accessibilityLabel={label}
      accessibilityHint={hint}
      onPress={onPress}
      onFocus={() => setFocused(true)}
      onBlur={() => setFocused(false)}
      hitSlop={2}
      style={({ pressed }) => [styles.root, focused && styles.focused, pressed && styles.pressed]}
    >
      <Text style={styles.label}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  root: {
    minHeight: SECONDARY_BUTTON_HEIGHT,
    minWidth: 140,
    paddingHorizontal: spacing.xl,
    paddingVertical: spacing.sm,
    borderRadius: 17,
    borderWidth: 1.5,
    borderColor: brand.ink,
    backgroundColor: brand.card,
    alignItems: 'center',
    justifyContent: 'center',
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 3,
  },
  focused: { outlineWidth: 2 },
  pressed: { backgroundColor: brand.cardShade },
  label: { ...type.label, color: brand.ink, textAlign: 'center', flexShrink: 1 },
});
