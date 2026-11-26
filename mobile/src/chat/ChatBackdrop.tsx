// Chat header: the Nevado as the last onboarding screen leaves it, without its volcano, moved so
// the crater's spot sits over the Pet's circle, and the vapor sheet the onboarding card rises into.
// Static while reading (the model runs on this screen; only the Pet in its circle moves, see
// PetCircle); the sheet rises over the ranges while the keyboard is open.
import { memo, useMemo } from 'react';
import { Animated, StyleSheet, View } from 'react-native';

import { SceneCanvas } from '@/onboarding/SceneCanvas';
import { applyMotions } from '@/onboarding/scene/timeline';
import { CloudCard } from '@/ui/CloudCard';

import type { ChatLayout } from './chatLayout';
import { headerScene } from './headerScene';

export const ChatBackdrop = memo(function ChatBackdrop({
  width,
  height,
  layout,
  time,
  rise,
  extraLift = 0,
  hideScene = false,
}: {
  width: number;
  height: number;
  layout: ChatLayout;
  /** Vertical move of the vapor sheet (negative = up, at most max(keyboardLift, extraLift)). */
  rise?: Animated.WithAnimatedValue<number>;
  /** Extra lift height needed when the mist collapses to the top nav bar during a long chat. */
  extraLift?: number;
  /** Unmount the mountain illustration while the raised mist completely covers it. */
  hideScene?: boolean;
  /** Idle-motion time the clouds and mist stand still at (the onboarding's, after the handoff). */
  time: number | null;
}) {
  const doc = useMemo(
    () => (time === null ? headerScene : applyMotions(headerScene, time)),
    [time],
  );
  // Drawn at the zoomed size rather than scaled as a view, so Android never upscales a raster.
  const rect = layout.sceneRect;
  const maxLift = Math.max(layout.keyboardLift, extraLift);
  return (
    <View style={StyleSheet.absoluteFill} pointerEvents="none">
      {!hideScene && (
        <View style={{ position: 'absolute', left: rect.left, top: rect.top }}>
          <SceneCanvas doc={doc} width={rect.width} height={rect.height} />
        </View>
      )}
      {/* Rising with the keyboard or a long chat, the mist covers the ranges; taller by the max
          lift so no sky shows under it on the way up. */}
      <Animated.View
        style={[styles.sheet, { top: layout.sheetTop, transform: [{ translateY: rise ?? 0 }] }]}
      >
        <CloudCard width={width} height={height - layout.sheetTop + maxLift}>
          {null}
        </CloudCard>
      </Animated.View>
    </View>
  );
});

const styles = StyleSheet.create({
  sheet: { position: 'absolute', left: 0 },
});
