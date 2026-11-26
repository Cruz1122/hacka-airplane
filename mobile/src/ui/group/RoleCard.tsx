// One of the two big choices on the group screen, stacked one above the other. Each card takes its
// share of the screen's spare height (flex) and centres the role's own Pet (as the phone owner
// dressed it, sized from the card's measured height) above its label and a subtle teal chevron.
// A calm pulsing halo around the card edge signals it is pressable (still under reduced motion).
// The whole card is the button that picks the role; the pencil on the circle is a separate button
// that opens that Pet's options. The card's button is a layer under the content, so the pencil is
// its sibling, never nested.
import { useEffect, useState } from 'react';
import { Animated, Easing, Platform, Pressable, StyleSheet, Text, View } from 'react-native';

import { Icon } from '../icons/Icon';
import { PET_FACE_VIEWBOX, type PetAccessory, type PetTint } from '../pet/petCore';
import { Pet } from '../pet/Pet';
import { brand, spacing, type } from '../theme/tokens';
import { useAccessibilityTheme } from '../useAccessibilityTheme';
import { useReducedMotion } from '../useReducedMotion';

import { roleCircleSize } from './roleCardSize';

const PENCIL = 36;
const PULSE_MS = 2800;
/** The card's floor: keeps it usable when the customizer or the keyboard takes the room. */
export const ROLE_CARD_MIN = 168;

export interface RoleCardProps {
  label: string;
  /** What choosing this role does, for screen readers. */
  hint?: string;
  /** What this role's Pet wears; nothing when it is bare. */
  wears: { accessory?: PetAccessory; tint?: PetTint };
  onPress: () => void;
  width: number;
  /** Opens or closes this Pet's options; no pencil without it. */
  onEdit?: () => void;
  editLabel?: string;
  /** The options are open: the pencil turns into a check. */
  editing?: boolean;
  /** Just chosen: card pops with a brief spring while transitioning into the role. */
  selected?: boolean;
  /** The sibling role was chosen: softly recedes while transitioning. */
  dimmed?: boolean;
  /** Optional stagger (ms) so stacked cards pulse gently in turn instead of in lockstep. */
  pulseDelay?: number;
  disabled?: boolean;
}

export function RoleCard({
  label,
  hint,
  wears,
  onPress,
  width,
  onEdit,
  editLabel,
  editing = false,
  selected = false,
  dimmed = false,
  pulseDelay = 0,
  disabled = false,
}: RoleCardProps) {
  const reduced = useReducedMotion();
  const { palette, scaled, highContrast } = useAccessibilityTheme();
  const [height, setHeight] = useState(ROLE_CARD_MIN);
  const [cardFocused, setCardFocused] = useState(false);
  const [cardPressed, setCardPressed] = useState(false);
  const [pencilFocused, setPencilFocused] = useState(false);
  const [scale] = useState(() => new Animated.Value(1));
  const [lift] = useState(() => new Animated.Value(0));
  const [fade] = useState(() => new Animated.Value(1));
  const [pulse] = useState(() => new Animated.Value(0));
  const native = Platform.OS !== 'web';

  const shouldPulse = !reduced && !disabled && !editing && !selected && !dimmed && !cardPressed;
  useEffect(() => {
    if (!shouldPulse) {
      pulse.setValue(0);
      return;
    }
    let loop: Animated.CompositeAnimation | null = null;
    const startLoop = () => {
      pulse.setValue(0);
      loop = Animated.loop(
        Animated.timing(pulse, {
          toValue: 1,
          duration: PULSE_MS,
          easing: Easing.out(Easing.quad),
          useNativeDriver: native,
        }),
      );
      loop.start();
    };
    const timer = pulseDelay > 0 ? setTimeout(startLoop, pulseDelay) : null;
    if (!timer) startLoop();
    return () => {
      if (timer) clearTimeout(timer);
      loop?.stop();
    };
  }, [shouldPulse, pulseDelay, pulse, native]);

  useEffect(() => {
    if (reduced) {
      scale.setValue(1);
      lift.setValue(0);
      fade.setValue(dimmed ? 0.45 : 1);
      return;
    }
    if (selected) {
      Animated.parallel([
        Animated.spring(scale, {
          toValue: 1.025,
          tension: 260,
          friction: 14,
          useNativeDriver: native,
        }),
        Animated.timing(lift, { toValue: -2, duration: 130, useNativeDriver: native }),
        Animated.timing(fade, { toValue: 1, duration: 130, useNativeDriver: native }),
      ]).start();
      return;
    }
    if (dimmed) {
      Animated.parallel([
        Animated.timing(scale, { toValue: 0.96, duration: 160, useNativeDriver: native }),
        Animated.timing(lift, { toValue: 0, duration: 160, useNativeDriver: native }),
        Animated.timing(fade, { toValue: 0.42, duration: 160, useNativeDriver: native }),
      ]).start();
      return;
    }
    Animated.parallel([
      Animated.spring(scale, {
        toValue: 1,
        tension: 240,
        friction: 18,
        useNativeDriver: native,
      }),
      Animated.timing(lift, { toValue: 0, duration: 140, useNativeDriver: native }),
      Animated.timing(fade, { toValue: 1, duration: 140, useNativeDriver: native }),
    ]).start();
  }, [selected, dimmed, reduced, scale, lift, fade, native]);

  const onCardPressIn = () => {
    setCardPressed(true);
    if (reduced || selected) return;
    Animated.parallel([
      Animated.timing(scale, { toValue: 0.97, duration: 100, useNativeDriver: native }),
      Animated.timing(lift, { toValue: 2, duration: 100, useNativeDriver: native }),
    ]).start();
  };

  const onCardPressOut = () => {
    setCardPressed(false);
    if (reduced || selected || dimmed) return;
    Animated.parallel([
      Animated.spring(scale, {
        toValue: 1,
        tension: 260,
        friction: 16,
        useNativeDriver: native,
      }),
      Animated.timing(lift, { toValue: 0, duration: 120, useNativeDriver: native }),
    ]).start();
  };

  const active = cardPressed || selected;
  const labelRoom = scaled.title.lineHeight + spacing.md;
  const circle = roleCircleSize(height, width, 2 * spacing.lg + labelRoom);
  return (
    <Animated.View
      style={[
        styles.root,
        { width, opacity: disabled && !selected && !dimmed ? 0.5 : fade },
        { transform: [{ translateY: lift }, { scale }] },
      ]}
      onLayout={(e) => setHeight(e.nativeEvent.layout.height)}
    >
      {shouldPulse && (
        <Animated.View
          pointerEvents="none"
          aria-hidden
          accessibilityElementsHidden
          importantForAccessibility="no-hide-descendants"
          style={[
            StyleSheet.absoluteFill,
            styles.pulseHalo,
            { borderColor: palette.primary },
            {
              opacity: pulse.interpolate({
                inputRange: [0, 0.2, 0.75, 1],
                outputRange: [0, 0.42, 0, 0],
              }),
              transform: [
                {
                  scale: pulse.interpolate({
                    inputRange: [0, 0.75, 1],
                    outputRange: [1, 1.03, 1.03],
                  }),
                },
              ],
            },
          ]}
        />
      )}
      <Pressable
        onPress={onPress}
        onPressIn={onCardPressIn}
        onPressOut={onCardPressOut}
        onFocus={() => setCardFocused(true)}
        onBlur={() => setCardFocused(false)}
        disabled={disabled}
        accessibilityRole="button"
        accessibilityLabel={label}
        accessibilityHint={hint}
        accessibilityState={{ disabled, selected }}
        style={[
          StyleSheet.absoluteFill,
          styles.card,
          {
            backgroundColor: palette.card,
            borderColor: highContrast ? palette.ink : palette.primarySoft,
          },
          cardFocused && [styles.focused, { borderColor: palette.primary }],
          active && { backgroundColor: palette.cardShade, borderColor: palette.primary },
        ]}
      />
      <View style={styles.content} pointerEvents="box-none">
        <View style={{ width: circle, height: circle }} pointerEvents="box-none">
          <View
            pointerEvents="none"
            aria-hidden
            accessibilityElementsHidden
            importantForAccessibility="no-hide-descendants"
            style={[
              styles.circle,
              {
                backgroundColor: palette.primary,
                borderColor: active ? palette.primary : palette.primarySoft,
                width: circle,
                height: circle,
                borderRadius: circle / 2,
              },
            ]}
          >
            <Pet
              size={circle * 0.9}
              emotion="happy"
              accessory={wears.accessory}
              tint={wears.tint}
              crop={PET_FACE_VIEWBOX}
              lookAround
            />
          </View>
          {onEdit && (
            <Pressable
              onPress={onEdit}
              onFocus={() => setPencilFocused(true)}
              onBlur={() => setPencilFocused(false)}
              disabled={disabled}
              accessibilityRole="button"
              accessibilityLabel={editLabel}
              accessibilityState={{ expanded: editing, disabled }}
              hitSlop={6}
              // On the circle's lower right edge.
              style={({ pressed }) => [
                styles.pencil,
                {
                  borderColor: palette.card,
                  backgroundColor: palette.ink,
                  left: circle * 0.854 - PENCIL / 2,
                  top: circle * 0.854 - PENCIL / 2,
                },
                pencilFocused && styles.focused,
                pressed && styles.pencilPressed,
              ]}
            >
              <Icon name={editing ? 'check' : 'pencil'} size={16} color={palette.onPrimary} />
            </Pressable>
          )}
        </View>
        <View
          style={styles.labelRow}
          pointerEvents="none"
          aria-hidden
          accessibilityElementsHidden
          importantForAccessibility="no-hide-descendants"
        >
          <Text
            style={[
              styles.label,
              {
                fontSize: scaled.title.fontSize,
                lineHeight: scaled.title.lineHeight,
                color: palette.ink,
              },
            ]}
            numberOfLines={2}
          >
            {label}
          </Text>
          <Icon name="chevronRight" size={20} color={palette.primary} strokeWidth={2.4} />
        </View>
      </View>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, minHeight: ROLE_CARD_MIN },
  pulseHalo: {
    borderRadius: 28,
    borderWidth: 2,
    borderColor: brand.primary,
  },
  card: {
    borderRadius: 28,
    borderWidth: 2,
    borderColor: brand.primarySoft,
    backgroundColor: brand.card,
    boxShadow: `0 6px 18px ${brand.glow}`,
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 3,
  },
  cardPressed: {
    backgroundColor: brand.cardShade,
    borderColor: brand.primary,
  },
  focused: { outlineWidth: 2, borderColor: brand.primary },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.md,
    padding: spacing.lg,
  },
  // The Pet is drawn in card colors, so it sits in a teal circle as on the chat sheet.
  circle: {
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    backgroundColor: brand.primary,
    borderWidth: 4,
    borderColor: brand.primarySoft,
  },
  circleActive: { borderColor: brand.primary },
  labelRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.xs,
    maxWidth: '100%',
  },
  label: { ...type.title, color: brand.ink, textAlign: 'center', flexShrink: 1 },
  // 36 pt badge, 48 pt target with the hit slop.
  pencil: {
    position: 'absolute',
    width: PENCIL,
    height: PENCIL,
    borderRadius: PENCIL / 2,
    borderWidth: 3,
    borderColor: brand.card,
    backgroundColor: brand.ink,
    alignItems: 'center',
    justifyContent: 'center',
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 2,
  },
  pencilPressed: { opacity: 0.75 },
});
