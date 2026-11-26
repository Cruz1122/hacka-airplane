// One still frame of the Pet, for places that show many at once (the group lane's dots): no idle
// loop, no blinking, no gaze. An emotion change still morphs with the Pet's own transition
// (useFaceTransition), then nothing runs until the next change.
import { useEffect, useId, useMemo, useState } from 'react';
import { View } from 'react-native';

import { brand } from '../theme/tokens';
import { useReducedMotion } from '../useReducedMotion';

import { FrameStore } from './frameLoop';
import { PetVaporCanvas } from './PetVaporCanvas';
import {
  copyConfig,
  PET_ACCESSORY_VIEWBOX,
  PET_PRESET,
  PET_VIEWBOX,
  petFrame,
  type PetAccessory,
  type PetConfig,
  type PetEmotion,
  type PetTint,
} from './petCore';
import { useFaceTransition } from './useFaceTransition';

export interface PetStillProps {
  /** Width in points; height follows the crop. */
  size: number;
  emotion: PetEmotion;
  accessory?: PetAccessory;
  tint?: PetTint;
  /** Part of the Pet to show, in Pet units (see Pet's `crop`). */
  crop?: { x: number; y: number; width: number; height: number };
  fill?: string;
  shade?: string;
}

const frameOf = (cfg: PetConfig, face: PetConfig['poses'][PetEmotion]) =>
  petFrame(cfg, { time: 0, face, blink: 1, reduced: true });

export function PetStill({
  size,
  emotion,
  accessory,
  tint,
  crop,
  fill = brand.card,
  shade = brand.cardShade,
}: PetStillProps) {
  const prefix = `pets${useId().replace(/[^a-zA-Z0-9]/g, '')}`;
  const reduced = useReducedMotion();
  const cfg = useMemo(() => {
    const next = copyConfig(PET_PRESET);
    next.emotion = emotion;
    next.accessory = accessory;
    next.accessoryTint = tint;
    next.smoke.count = 0;
    return next;
  }, [emotion, accessory, tint]);
  const { transition, easing } = PET_PRESET.motion;
  const face = useFaceTransition(PET_PRESET.poses, emotion, reduced ? 0 : transition, easing);
  const [frames] = useState(() => new FrameStore(frameOf(cfg, face)));
  useEffect(() => frames.set(frameOf(cfg, face)), [cfg, face, frames]);
  const v = crop ?? (accessory ? PET_ACCESSORY_VIEWBOX : PET_VIEWBOX);
  return (
    <View
      style={{ width: size, aspectRatio: v.width / v.height }}
      pointerEvents="none"
      aria-hidden
      accessibilityElementsHidden
      importantForAccessibility="no-hide-descendants"
    >
      <PetVaporCanvas
        config={cfg}
        frames={frames}
        fill={fill}
        shade={shade}
        prefix={prefix}
        viewBox={v}
        width={size}
        height={(size * v.height) / v.width}
      />
    </View>
  );
}
