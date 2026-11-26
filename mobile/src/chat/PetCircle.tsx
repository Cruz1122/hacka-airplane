// The Pet in its circle on the sheet's edge: fully animated (breathing, tail, blinking, glancing
// around), thinking while an answer is worked out and talking while one arrives. It holds still
// while another screen covers the chat (the stack keeps this one mounted underneath). Its corner
// badge is the model's state: a spinning arrow while it loads, a green dot once it is ready.
import { useIsFocused } from 'expo-router';
import { memo, useEffect, useState } from 'react';
import { Animated, Easing, Platform, StyleSheet, View } from 'react-native';

import { t } from '@/i18n';
import { DEFAULT_PALETTE } from '@/onboarding/scene/preset';
import { Icon } from '@/ui/icons/Icon';
import { Pet } from '@/ui/pet/Pet';
import { PET_PRESET, type PetEmotion, type VoiceState } from '@/ui/pet/petCore';
import { brand } from '@/ui/theme/tokens';
import { useReducedMotion } from '@/ui/useReducedMotion';

import { type GazeChannel, useGaze } from './gaze';

const RING = 4;
/**
 * The face for each chat moment. Emotion changes are what the Pet component morphs (fleibo-face's
 * own transition); the voice alone would only switch the mouth.
 */
const EMOTION: Record<VoiceState, PetEmotion> = {
  idle: 'happy',
  listening: 'listening',
  thinking: 'thinking',
  speaking: 'speaking',
};
// Square window on the Pet with teal room around it, as in the chat mock; the circle cuts the
// tail below its first curl.
const b = PET_PRESET.body;
const HALF = Math.max(b.width, b.height) * 0.78;
const CROP = { x: b.x - HALF, y: b.y + 4 - HALF, width: HALF * 2, height: HALF * 2 };
const DOT = 18;
const SPINNER = 22;
/** One turn of the loading arrow. */
const TURN_MS = 1100;

/** The loading badge: turns on the native driver; still under reduced motion or out of focus. */
function LoadingBadge({ spinning }: { spinning: boolean }) {
  const [turn] = useState(() => new Animated.Value(0));
  useEffect(() => {
    if (!spinning) return;
    const loop = Animated.loop(
      Animated.timing(turn, {
        toValue: 1,
        duration: TURN_MS,
        easing: Easing.linear,
        useNativeDriver: Platform.OS !== 'web',
      }),
    );
    loop.start();
    return () => loop.stop();
  }, [spinning, turn]);
  const [rotate] = useState(() =>
    turn.interpolate({ inputRange: [0, 1], outputRange: ['0deg', '360deg'] }),
  );
  return (
    <View
      style={styles.loading}
      accessible
      accessibilityRole="progressbar"
      accessibilityLabel={t.modelLoading}
    >
      <Animated.View style={{ transform: [{ rotate }] }}>
        <Icon name="refreshCw" size={14} color={brand.primary} strokeWidth={2.5} />
      </Animated.View>
    </View>
  );
}

export const PetCircle = memo(function PetCircle({
  x,
  y,
  r,
  voice,
  ready,
  loading = false,
  gaze,
}: {
  x: number;
  y: number;
  r: number;
  voice: VoiceState;
  /** The green dot. */
  ready: boolean;
  /** The spinning arrow while the model loads; the dot wins if both are set. */
  loading?: boolean;
  /** While the visitor types, the Pet looks at the last character. */
  gaze?: GazeChannel;
}) {
  const lookAt = useGaze(gaze);
  const focused = useIsFocused();
  const reduced = useReducedMotion();
  return (
    <View
      style={[styles.root, { left: x - r, top: y - r, width: r * 2, height: r * 2 }]}
      pointerEvents="none"
    >
      <View style={[styles.clip, { borderRadius: r }]}>
        <Pet
          size={r * 2 - RING * 2}
          crop={CROP}
          // The scene's mist colors: the same vapor Pet that rose out of the crater.
          fill={DEFAULT_PALETTE.mist}
          shade={DEFAULT_PALETTE.cloudShade}
          emotion={EMOTION[voice]}
          voice={voice}
          audioLevel={voice === 'speaking' ? 0.7 : 0}
          lookAt={lookAt}
          paused={!focused}
          lookAround={focused}
        />
      </View>
      {ready && <View style={styles.online} />}
      {loading && !ready && <LoadingBadge spinning={focused && !reduced} />}
    </View>
  );
});

const styles = StyleSheet.create({
  root: { position: 'absolute' },
  clip: {
    flex: 1,
    overflow: 'hidden',
    borderWidth: RING,
    borderColor: brand.card,
    backgroundColor: brand.primary,
  },
  online: {
    position: 'absolute',
    right: 4,
    bottom: 4,
    width: DOT,
    height: DOT,
    borderRadius: DOT / 2,
    borderWidth: 3,
    borderColor: brand.card,
    backgroundColor: brand.online,
  },
  // Centred where the dot sits, a little larger so the arrow reads.
  loading: {
    position: 'absolute',
    right: 4 - (SPINNER - DOT) / 2,
    bottom: 4 - (SPINNER - DOT) / 2,
    width: SPINNER,
    height: SPINNER,
    borderRadius: SPINNER / 2,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: brand.card,
  },
});
