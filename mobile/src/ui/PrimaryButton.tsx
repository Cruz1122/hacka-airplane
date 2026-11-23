// Primary action: a defined ink surface, inset edge and a separate directional affordance.
import { useState } from 'react';
import { Animated, Pressable, StyleSheet, Text, View } from 'react-native';

import { Icon } from './icons/Icon';
import { brand, type } from './theme/tokens';
import { useReducedMotion } from './useReducedMotion';

export const PRIMARY_BUTTON_HEIGHT = 54;

export interface PrimaryButtonProps {
  label: string;
  onPress: () => void;
  chevron?: boolean;
}

export function PrimaryButton({ label, onPress, chevron = true }: PrimaryButtonProps) {
  const reduced = useReducedMotion();
  const [scale] = useState(() => new Animated.Value(1));
  const [focused, setFocused] = useState(false);
  const move = (toValue: number) => {
    scale.stopAnimation();
    if (reduced) scale.setValue(1);
    else Animated.timing(scale, { toValue, duration: 130, useNativeDriver: true }).start();
  };
  return (
    <Animated.View style={{ transform: [{ scale }] }}>
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={label}
        onPress={onPress}
        onPressIn={() => move(0.985)}
        onPressOut={() => move(1)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        style={({ pressed }) => [styles.root, focused && styles.focused, pressed && styles.pressed]}
      >
        <Text style={styles.label}>{label}</Text>
        {chevron && (
          <View style={styles.direction} pointerEvents="none">
            <Icon name="chevronRight" size={20} color={brand.onPrimary} />
          </View>
        )}
      </Pressable>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  root: {
    height: PRIMARY_BUTTON_HEIGHT,
    borderRadius: 17,
    borderWidth: 1,
    borderColor: brand.primary,
    backgroundColor: brand.ink,
    paddingLeft: 20,
    paddingRight: 8,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 14,
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 3,
  },
  focused: { outlineWidth: 2 },
  pressed: { backgroundColor: brand.primary },
  label: { ...type.label, color: brand.onPrimary, flexShrink: 1 },
  direction: {
    width: 36,
    height: 36,
    borderRadius: 11,
    borderWidth: 1,
    borderColor: brand.primary,
    alignItems: 'center',
    justifyContent: 'center',
  },
});
