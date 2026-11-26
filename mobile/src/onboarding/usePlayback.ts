// Drives the onboarding: the progress value between screens (transitions, swipe scrubbing) and the
// idle-motion clock (seconds since mount, held during transitions). One requestAnimationFrame
// loop, running only while needed.
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { PanResponder } from 'react-native';

import { EASINGS } from './scene/timeline';
import type { EasingName } from './scene/types';
import { ONBOARDING_SCREENS } from './scene/types';

const LAST = ONBOARDING_SCREENS - 1;
/** Idle motions are slow; 30 fps is enough and halves the render cost on mid-range phones. */
const IDLE_FRAME_MS = 33;

const clamp = (p: number) => Math.min(LAST, Math.max(0, p));

interface Transition {
  from: number;
  to: number;
  start: number | null;
  ms: number;
  easing: EasingName;
}

export interface PlaybackOptions {
  transitionMs: number;
  easing: EasingName;
  /** Run idle motions (steam, clouds, mist, leaves). */
  ambient: boolean;
  /** Reduced motion: no idle motions and screen changes jump instead of animating. */
  reduced: boolean;
}

export interface Playback {
  progress: number;
  /**
   * Seconds for idle motions, or null when they are off. The clock holds still during a
   * transition and resumes from the same pose afterwards.
   */
  time: number | null;
  /** `time` as last drawn, for event handlers that must not re-render on every idle frame. */
  timeNow: () => number | null;
  animating: boolean;
  /** A transition or a drag is moving the camera; the scene draws cheap view transforms. */
  moving: boolean;
  goTo: (target: number) => void;
  /** Jump to a progress value, cancelling any transition (swipe, Lab scrubber). */
  scrub: (p: number) => void;
  /** Progress right now, for event handlers that run between renders. */
  progressNow: () => number;
  /** Start a drag at the current progress; dragBy then scrubs relative to that start. */
  beginDrag: () => void;
  dragBy: (delta: number) => void;
}

export function usePlayback({ transitionMs, easing, ambient, reduced }: PlaybackOptions): Playback {
  const [progress, setProgress] = useState(0);
  const [time, setTime] = useState(0);
  const [animating, setAnimating] = useState(false);
  const [dragging, setDragging] = useState(false);
  const current = useRef(0);
  const transition = useRef<Transition | null>(null);
  // Idle-motion seconds: advances only outside transitions; `drawn` is the value last rendered.
  const clock = useRef(0);
  const drawn = useRef(0);
  const idle = ambient && !reduced;

  useEffect(() => {
    if (!idle && !animating) return;
    let raf = 0;
    let last: number | null = null;
    let lastIdle = -Infinity;
    const tick = (now: number) => {
      const dt = last === null ? 0 : now - last;
      last = now;
      const tr = transition.current;
      if (tr) {
        tr.start ??= now;
        const t = Math.min(1, (now - tr.start) / tr.ms);
        current.current = tr.from + (tr.to - tr.from) * EASINGS[tr.easing](t);
        setProgress(current.current);
        if (t >= 1) {
          transition.current = null;
          setAnimating(false);
        }
      } else if (idle) {
        // Idle motions hold during a transition: their redraws were most of each camera frame's
        // work (about 4 of 5 object re-renders on the default scene, __tests__/idleCost.test.ts),
        // and the camera move hides a short pause. The clock skips the paused span, so motions
        // resume without a jump.
        clock.current += dt / 1000;
        if (now - lastIdle >= IDLE_FRAME_MS) {
          lastIdle = now;
          drawn.current = clock.current;
          setTime(clock.current);
        }
      }
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [idle, animating]);

  const scrub = useCallback((p: number) => {
    transition.current = null;
    current.current = clamp(p);
    setProgress(current.current);
    setAnimating(false);
  }, []);

  const goTo = useCallback(
    (target: number) => {
      setDragging(false);
      const to = clamp(target);
      const from = current.current;
      if (reduced || Math.abs(to - from) < 1e-4) {
        scrub(to);
        return;
      }
      // Longer jumps (dot 1 -> dot 3) take longer, short settles after a swipe are quicker.
      const ms = transitionMs * Math.min(1.6, Math.max(0.4, Math.abs(to - from)));
      transition.current = { from, to, start: null, ms, easing };
      setAnimating(true);
    },
    [reduced, transitionMs, easing, scrub],
  );

  const progressNow = useCallback(() => current.current, []);
  const timeNow = useCallback(() => (idle ? drawn.current : null), [idle]);
  const dragStart = useRef(0);
  const beginDrag = useCallback(() => {
    dragStart.current = current.current;
    setDragging(true);
  }, []);
  const dragBy = useCallback((delta: number) => scrub(dragStart.current + delta), [scrub]);
  return {
    progress,
    time: idle ? time : null,
    timeNow,
    animating,
    moving: animating || dragging,
    goTo,
    scrub,
    progressNow,
    beginDrag,
    dragBy,
  };
}

/** Horizontal swipe: drags scrub the scene, release settles on a screen (flick = next/previous). */
export function useSwipe(
  play: Pick<Playback, 'goTo' | 'progressNow' | 'beginDrag' | 'dragBy'>,
  width: number,
) {
  const { goTo, progressNow, beginDrag, dragBy } = play;
  return useMemo(() => {
    const settle = (vx: number) => {
      const p = progressNow();
      if (vx < -0.3) goTo(Math.floor(p) + 1);
      else if (vx > 0.3) goTo(Math.ceil(p) - 1);
      else goTo(Math.round(p));
    };
    return PanResponder.create({
      onMoveShouldSetPanResponder: (_, g) =>
        Math.abs(g.dx) > 12 && Math.abs(g.dx) > Math.abs(g.dy) * 1.5,
      onPanResponderGrant: () => beginDrag(),
      onPanResponderMove: (_, g) => dragBy(-g.dx / Math.max(1, width)),
      onPanResponderRelease: (_, g) => settle(g.vx),
      onPanResponderTerminate: () => settle(0),
    });
  }, [goTo, progressNow, beginDrag, dragBy, width]);
}
