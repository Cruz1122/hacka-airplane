// The guide's screen before anyone joins: the guide's own Pet (as dressed) in its teal circle,
// soft teal rings expanding out of the circle (the phone calling the group in), what to do next
// and, with `onCancel`, a way back to the role chooser. Visitors join by bringing their phone to
// the guide's, so the copy says exactly that. Under reduced motion the rings stand still.
import { useEffect, useState } from 'react';
import { Animated, Easing, Platform, StyleSheet, Text, View } from 'react-native';

import { t } from '@/i18n';

import { PET_FACE_VIEWBOX, type PetAccessory, type PetTint } from '../pet/petCore';
import { Pet } from '../pet/Pet';
import { SecondaryButton } from '../SecondaryButton';
import { brand, spacing, type } from '../theme/tokens';
import { useReducedMotion } from '../useReducedMotion';

const CIRCLE = 128;
/** Room around the circle for the rings to grow into. */
const ART = CIRCLE * 1.9;
const RINGS = 3;
const RING_MS = 2400;
/** Where each ring stands under reduced motion: two quiet halos. */
const STILL = [0.35, 0.7];

export interface EmptyLaneProps {
  /** What the guide's Pet wears. */
  wears: { accessory?: PetAccessory; tint?: PetTint };
  /** Ends the guide session; no button without it. */
  onCancel?: () => void;
}

const GROWN = ART / CIRCLE;

/** One ring at `phase`: 0 hugging the circle, 1 at the edge of the art, faded out. */
function Ring({ phase }: { phase: Animated.AnimatedInterpolation<number> }) {
  return (
    <Animated.View
      pointerEvents="none"
      style={[
        styles.ring,
        {
          opacity: phase.interpolate({ inputRange: [0, 1], outputRange: [0.55, 0] }),
          transform: [
            { scale: phase.interpolate({ inputRange: [0, 1], outputRange: [1, GROWN] }) },
          ],
        },
      ]}
    />
  );
}

function Pulse() {
  const reduced = useReducedMotion();
  const [clock] = useState(() => new Animated.Value(0));
  useEffect(() => {
    if (reduced) return clock.setValue(0);
    const loop = Animated.loop(
      Animated.timing(clock, {
        toValue: 1,
        duration: RING_MS,
        easing: Easing.linear,
        useNativeDriver: Platform.OS !== 'web',
      }),
    );
    loop.start();
    return () => loop.stop();
  }, [reduced, clock]);
  if (reduced) {
    return STILL.map((p) => (
      <View
        key={p}
        pointerEvents="none"
        style={[
          styles.ring,
          { opacity: 0.55 * (1 - p), transform: [{ scale: 1 + p * (GROWN - 1) }] },
        ]}
      />
    ));
  }
  // One clock; ring i runs i/RINGS of a period behind, eased out, and wraps from 1 back to 0.
  return Array.from({ length: RINGS }, (_, i) => {
    const offset = i / RINGS;
    // An input range must not step back, so ring 0 (no wrap) gets the plain one.
    const phase = clock.interpolate(
      i === 0
        ? { inputRange: [0, 1], outputRange: [0, 1] }
        : {
            inputRange: [0, 1 - offset, 1 - offset + 0.0001, 1],
            outputRange: [offset, 1, 0, offset],
          },
    );
    return (
      <Ring
        key={i}
        phase={phase.interpolate({
          inputRange: [0, 1],
          outputRange: [0, 1],
          easing: Easing.out(Easing.quad),
        })}
      />
    );
  });
}

export function EmptyLane({ wears, onCancel }: EmptyLaneProps) {
  return (
    <View style={styles.root} accessibilityLiveRegion="polite">
      <View
        style={styles.art}
        aria-hidden
        accessibilityElementsHidden
        importantForAccessibility="no-hide-descendants"
      >
        <Pulse />
        <View style={styles.circle}>
          <Pet
            size={CIRCLE * 0.9}
            emotion="curious"
            accessory={wears.accessory}
            tint={wears.tint}
            crop={PET_FACE_VIEWBOX}
            lookAround
          />
        </View>
      </View>
      <View style={styles.copy}>
        <Text style={styles.title} accessibilityRole="header">
          {t.group.emptyTitle}
        </Text>
        <Text style={styles.body}>{t.group.emptyBody}</Text>
      </View>
      {onCancel && (
        <SecondaryButton
          label={t.group.cancelGuide}
          hint={t.group.cancelGuideHint}
          onPress={onCancel}
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    alignItems: 'center',
    justifyContent: 'center',
    gap: spacing.lg,
    paddingHorizontal: spacing.xl,
  },
  art: { width: ART, height: ART, alignItems: 'center', justifyContent: 'center' },
  ring: {
    position: 'absolute',
    width: CIRCLE,
    height: CIRCLE,
    borderRadius: CIRCLE / 2,
    borderWidth: 3,
    borderColor: brand.primary,
    backgroundColor: brand.cardShade,
  },
  // The Pet is drawn in card colors, so it sits in a teal circle as on the chat sheet.
  circle: {
    width: CIRCLE,
    height: CIRCLE,
    borderRadius: CIRCLE / 2,
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    backgroundColor: brand.primary,
    borderWidth: 4,
    borderColor: brand.primarySoft,
  },
  copy: { gap: spacing.sm, maxWidth: 300 },
  title: { ...type.title, color: brand.ink, textAlign: 'center' },
  body: { ...type.body, color: brand.inkMuted, textAlign: 'center' },
});
