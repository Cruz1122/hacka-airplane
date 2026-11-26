// The Pet in its circle on the sheet's edge: fully animated (breathing, tail, blinking, glancing
// around), thinking while an answer is worked out and talking while one arrives.
import { memo } from 'react';
import { StyleSheet, View } from 'react-native';

import { DEFAULT_PALETTE } from '@/onboarding/scene/preset';
import { Pet } from '@/ui/pet/Pet';
import { PET_PRESET, type PetEmotion, type VoiceState } from '@/ui/pet/petCore';
import { brand } from '@/ui/theme/tokens';

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

export const PetCircle = memo(function PetCircle({
  x,
  y,
  r,
  voice,
  ready,
  gaze,
}: {
  x: number;
  y: number;
  r: number;
  voice: VoiceState;
  ready: boolean;
  /** While the visitor types, the Pet looks at the last character. */
  gaze?: GazeChannel;
}) {
  const lookAt = useGaze(gaze);
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
        />
      </View>
      {ready && <View style={styles.online} />}
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
    width: 18,
    height: 18,
    borderRadius: 9,
    borderWidth: 3,
    borderColor: brand.card,
    backgroundColor: brand.online,
  },
});
