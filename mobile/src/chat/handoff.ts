// The onboarding's exit into the chat: one clock t (0..1) drives everything with view transforms
// and opacity only, so the whole move runs on the native driver. At t = 1 the screen is exactly
// the chat's first frame (see ChatBackdrop and PetCircle), and the route switches without a cut.
import { Animated, Easing } from 'react-native';

import type { ChatLayout } from './chatLayout';

export const HANDOFF_MS = 550;

/** Card copy fades first, then the volcano and the scene's Pet; scene and sheet move together. */
const COPY_OUT = [0, 0.22];
const VOLCANO_OUT = [0.08, 0.5];
// One shared window for the scene and the sheet: both move linearly in t between two states that
// keep the scene behind the vapor edge, so no frame in between can open a gap.
const MOVE = [0.12, 0.88];
const CIRCLE_IN = [0.72, 0.86];

export function handoffTiming(t: Animated.Value): Animated.CompositeAnimation {
  return Animated.timing(t, {
    toValue: 1,
    duration: HANDOFF_MS,
    easing: Easing.inOut(Easing.cubic),
    useNativeDriver: true,
  });
}

const fade = (t: Animated.Value, range: number[], from: number, to: number) =>
  t.interpolate({ inputRange: range, outputRange: [from, to], extrapolate: 'clamp' });

/**
 * Styles for each moving part. `cardTop` is where the onboarding card's edge starts; the scene
 * box is width x layout.sceneHeight, transformed about its center like ChatLayout.scene says.
 */
export function handoffStyles(t: Animated.Value, layout: ChatLayout, cardTop: number) {
  const { scene } = layout;
  return {
    copy: { opacity: fade(t, COPY_OUT, 1, 0) },
    volcano: { opacity: fade(t, VOLCANO_OUT, 1, 0) },
    scene: {
      transform: [
        { translateX: fade(t, MOVE, 0, scene.x) },
        { translateY: fade(t, MOVE, 0, scene.y) },
        { scale: fade(t, MOVE, 1, scene.scale) },
      ],
    },
    sheet: { transform: [{ translateY: fade(t, MOVE, 0, layout.sheetTop - cardTop) }] },
    circle: {
      opacity: fade(t, CIRCLE_IN, 0, 1),
      transform: [
        {
          scale: t.interpolate({
            inputRange: [CIRCLE_IN[0], 0.9, 1],
            outputRange: [0.4, 1.08, 1],
            extrapolate: 'clamp',
          }),
        },
      ],
    },
  };
}
