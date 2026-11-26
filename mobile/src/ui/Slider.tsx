// A horizontal slider on brand tokens. The 8 pt track reads as three segments: from the start to
// `split` of the value in `primary`, from there to the thumb in `primarySoft`, past the thumb in
// `wineSoft` (with `split`; plain `cardShade` without). The 28 pt card knob has an ink edge and a
// glow, inside a 44 pt touch target. The knob follows the finger and settles on the nearest step
// when it lifts; `onChange` fires once per step crossed. Screen readers get an adjustable control
// with increment/decrement actions. No haptics.
import { useEffect, useRef, useState } from 'react';
import { StyleSheet, View, type AccessibilityActionEvent } from 'react-native';
import {
  GestureDetector,
  GestureHandlerRootView,
  usePanGesture,
} from 'react-native-gesture-handler';
import Animated, { useAnimatedStyle, useSharedValue, withTiming } from 'react-native-reanimated';

import { brand } from './theme/tokens';

/** Touch target and thumb box; the visible knob is smaller. */
export const SLIDER_THUMB = 44;
const KNOB = 28;
const TRACK = 8;
const SETTLE_MS = 120;

export interface SliderRange {
  min: number;
  max: number;
  step: number;
}

const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));

/** The stepped value under `x` (points from the slider's left edge) on a slider `width` wide. */
export function sliderValueAt(x: number, width: number, r: SliderRange): number {
  const span = Math.max(1, width - SLIDER_THUMB);
  const f = clamp((x - SLIDER_THUMB / 2) / span, 0, 1);
  return clamp(r.min + Math.round((f * (r.max - r.min)) / r.step) * r.step, r.min, r.max);
}

/** Centre of the thumb for `value`, in points from the slider's left edge. */
export function sliderX(value: number, width: number, r: SliderRange): number {
  const span = Math.max(0, width - SLIDER_THUMB);
  return SLIDER_THUMB / 2 + ((clamp(value, r.min, r.max) - r.min) / (r.max - r.min)) * span;
}

export interface SliderProps extends SliderRange {
  value: number;
  onChange: (value: number) => void;
  /** What the slider sets, for screen readers. */
  label: string;
  /** The value as read aloud, e.g. "30 m". */
  valueText: string;
  /** What changing it does, for screen readers. */
  hint?: string;
  /** 0..1: where along the value (from 0, not from `min`) the fill changes tone. */
  split?: number;
}

export function Slider({
  value,
  min,
  max,
  step,
  onChange,
  label,
  valueText,
  hint,
  split,
}: SliderProps) {
  const range = { min, max, step };
  const [width, setWidth] = useState(0);
  const x = useSharedValue(0);
  const dragging = useRef(false);
  const last = useRef(value);

  const placed = useRef(false);

  // Off the finger, the thumb rests on the value it was given: placed at once on the first
  // layout (no slide in from the left edge on mount), gliding on later changes.
  useEffect(() => {
    if (dragging.current || width === 0) return;
    last.current = value;
    const to = sliderX(value, width, { min, max, step });
    x.set(placed.current ? withTiming(to, { duration: SETTLE_MS }) : to);
    placed.current = true;
  }, [value, width, min, max, step, x]);

  const follow = (px: number) => {
    x.set(clamp(px, SLIDER_THUMB / 2, Math.max(SLIDER_THUMB / 2, width - SLIDER_THUMB / 2)));
    const next = sliderValueAt(px, width, range);
    if (next !== last.current) {
      last.current = next;
      onChange(next);
    }
  };

  const pan = usePanGesture({
    // Plain JS callbacks: the work per move is one comparison and, per step, one state update.
    runOnJS: true,
    // A horizontal drag moves it; a vertical one is left to the screen's scroll.
    activeOffsetX: [-4, 4],
    failOffsetY: [-12, 12],
    onActivate: (e) => {
      dragging.current = true;
      follow(e.x);
    },
    onUpdate: (e) => follow(e.x),
    onFinalize: () => {
      dragging.current = false;
      if (width > 0)
        x.set(withTiming(sliderX(last.current, width, range), { duration: SETTLE_MS }));
    },
  });

  // From the thumb's continuous position, so the split moves with the finger, not per step.
  const span = Math.max(1, width - SLIDER_THUMB);
  const thumbStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: x.value - SLIDER_THUMB / 2 }],
  }));
  const fillStyle = useAnimatedStyle(() => ({ width: x.value }));
  const nearStyle = useAnimatedStyle(() => {
    if (split === undefined) return { width: 0 };
    const v = min + ((x.value - SLIDER_THUMB / 2) / span) * (max - min);
    const at = Math.min(max, Math.max(min, split * v));
    return { width: SLIDER_THUMB / 2 + ((at - min) / (max - min)) * span };
  });

  const onAction = (e: AccessibilityActionEvent) => {
    const delta = e.nativeEvent.actionName === 'increment' ? step : -step;
    const next = clamp(value + delta, min, max);
    if (next !== value) onChange(next);
  };

  return (
    <GestureHandlerRootView style={styles.root}>
      <GestureDetector gesture={pan} touchAction="pan-y">
        <View
          style={styles.hit}
          onLayout={(e) => setWidth(e.nativeEvent.layout.width)}
          accessible
          accessibilityRole="adjustable"
          accessibilityLabel={label}
          accessibilityHint={hint}
          aria-valuemin={min}
          aria-valuemax={max}
          aria-valuenow={value}
          aria-valuetext={valueText}
          accessibilityActions={[{ name: 'increment' }, { name: 'decrement' }]}
          onAccessibilityAction={onAction}
        >
          <View style={[styles.track, split !== undefined && styles.trackBeyond]}>
            <Animated.View style={[styles.fill, styles.fillMid, fillStyle]} />
            {split !== undefined && <Animated.View style={[styles.fill, nearStyle]} />}
          </View>
          <Animated.View style={[styles.thumb, thumbStyle]} pointerEvents="none">
            <View style={styles.knob} />
          </Animated.View>
        </View>
      </GestureDetector>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  root: { alignSelf: 'stretch' },
  hit: { height: SLIDER_THUMB, justifyContent: 'center' },
  track: {
    marginHorizontal: SLIDER_THUMB / 2,
    height: TRACK,
    borderRadius: TRACK / 2,
    backgroundColor: brand.cardShade,
    overflow: 'hidden',
  },
  trackBeyond: { backgroundColor: brand.wineSoft },
  // Measured from the hit box's left edge, so a fill runs under the track's left margin too.
  fill: {
    position: 'absolute',
    left: -SLIDER_THUMB / 2,
    top: 0,
    bottom: 0,
    backgroundColor: brand.primary,
  },
  fillMid: { backgroundColor: brand.primarySoft },
  thumb: {
    position: 'absolute',
    left: 0,
    top: 0,
    width: SLIDER_THUMB,
    height: SLIDER_THUMB,
    alignItems: 'center',
    justifyContent: 'center',
  },
  knob: {
    width: KNOB,
    height: KNOB,
    borderRadius: KNOB / 2,
    backgroundColor: brand.card,
    borderWidth: 3,
    borderColor: brand.ink,
    boxShadow: `0 2px 8px ${brand.glow}`,
  },
});
