// Drives the onboarding: the progress value between screens (transitions, swipe scrubbing) and the
// idle-motion clock (seconds since mount, held during transitions). One requestAnimationFrame
// loop, running only while needed.
//
// Per-frame values live outside React state. A screen subscribes only the component that draws
// them (usePlaybackFrame), so a frame re-renders the scene canvas and nothing else, and
// `progressValue` carries progress to native-driven styles (card copy, page dots) with no render.
import { useEffect, useLayoutEffect, useMemo, useState } from 'react';
import { Animated, PanResponder, Platform } from 'react-native';

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

/** What one drawn frame shows. A new object only when one of its values changed. */
export interface PlaybackFrame {
  progress: number;
  /**
   * Seconds for idle motions, or null when they are off. The clock holds still during a
   * transition and resumes from the same pose afterwards.
   */
  time: number | null;
  animating: boolean;
  /** A transition or a drag is moving the camera; the scene draws cheap view transforms. */
  moving: boolean;
}

export interface PlaybackControls {
  /** `time` as last drawn, for event handlers that must not re-render on every idle frame. */
  timeNow: () => number | null;
  goTo: (target: number) => void;
  /** Jump to a progress value, cancelling any transition (Lab scrubber, reduced motion). */
  scrub: (p: number) => void;
  /** Progress right now, for event handlers that run between renders. */
  progressNow: () => number;
  /** Start a drag at the progress on screen, stopping a running transition there. */
  beginDrag: () => void;
  /** Drag relative to the start; finger moves are drawn once per display frame. */
  dragBy: (delta: number) => void;
}

export interface PlaybackClock extends PlaybackControls {
  /** Progress for native-driven styles. Set on every frame that moves it; never re-renders. */
  progressValue: Animated.Value;
  subscribe: (listener: () => void) => () => void;
  frame: () => PlaybackFrame;
  setOptions: (options: PlaybackOptions) => void;
  /** Starts the frame loop if anything needs it; stop() cancels it (unmount). */
  start: () => void;
  stop: () => void;
}

export type Playback = PlaybackFrame & PlaybackControls;

// react-native-web has no native animated module; its JS driver updates the DOM style directly.
const NATIVE_DRIVER = Platform.OS !== 'web';

function createClock(initial: PlaybackOptions): PlaybackClock {
  let options = initial;
  const idle = () => options.ambient && !options.reduced;
  let progress = 0;
  let transition: Transition | null = null;
  let dragging = false;
  let dragStart = 0;
  // A drag move waiting for the next frame: touch events can outnumber display frames.
  let pending = false;
  // Idle-motion seconds: advances only outside transitions; `drawn` is the value last published.
  let clock = 0;
  let drawn = 0;
  let raf = 0;
  let last: number | null = null;
  let lastIdle = -Infinity;
  let frame: PlaybackFrame = { progress, time: idle() ? 0 : null, animating: false, moving: false };
  const listeners = new Set<() => void>();
  const progressValue = new Animated.Value(0, { useNativeDriver: NATIVE_DRIVER });

  const publish = () => {
    const time = idle() ? drawn : null;
    const animating = transition !== null;
    const moving = animating || dragging;
    if (
      frame.progress === progress &&
      frame.time === time &&
      frame.animating === animating &&
      frame.moving === moving
    )
      return;
    if (frame.progress !== progress) progressValue.setValue(progress);
    frame = { progress, time, animating, moving };
    for (const listener of listeners) listener();
  };

  const tick = (now: number) => {
    raf = 0;
    const dt = last === null ? 0 : now - last;
    last = now;
    const tr = transition;
    if (tr) {
      tr.start ??= now;
      const t = Math.min(1, (now - tr.start) / tr.ms);
      progress = tr.from + (tr.to - tr.from) * EASINGS[tr.easing](t);
      if (t >= 1) transition = null;
    } else if (idle()) {
      // Idle motions hold during a transition: their redraws were most of each camera frame's
      // work (about 4 of 5 object re-renders on the default scene, __tests__/idleCost.test.ts),
      // and the camera move hides a short pause. The clock skips the paused span, so motions
      // resume without a jump.
      clock += dt / 1000;
      if (now - lastIdle >= IDLE_FRAME_MS) {
        lastIdle = now;
        drawn = clock;
      }
    }
    pending = false;
    publish();
    schedule();
  };

  function schedule() {
    if (raf) return;
    if (transition || pending || idle()) raf = requestAnimationFrame(tick);
    // A stopped loop restarts with dt = 0, so a pause never advances the idle clock.
    else last = null;
  }

  const stop = () => {
    cancelAnimationFrame(raf);
    raf = 0;
    last = null;
  };

  const scrub = (p: number) => {
    transition = null;
    pending = false;
    progress = clamp(p);
    publish();
  };

  return {
    progressValue,
    setOptions: (next) => {
      options = next;
    },
    subscribe: (listener) => {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    frame: () => frame,
    start: () => {
      // Options (ambient, reduced) may have changed since the last frame.
      publish();
      schedule();
    },
    stop,
    timeNow: () => (idle() ? drawn : null),
    progressNow: () => progress,
    scrub,
    goTo: (target) => {
      dragging = false;
      const to = clamp(target);
      const from = progress;
      if (options.reduced || Math.abs(to - from) < 1e-4) {
        scrub(to);
        return;
      }
      // Longer jumps (dot 1 -> dot 3) take longer, short settles after a swipe are quicker.
      const ms = options.transitionMs * Math.min(1.6, Math.max(0.4, Math.abs(to - from)));
      transition = { from, to, start: null, ms, easing: options.easing };
      publish();
      schedule();
    },
    beginDrag: () => {
      transition = null;
      dragStart = progress;
      dragging = true;
      publish();
    },
    dragBy: (delta) => {
      transition = null;
      progress = clamp(dragStart + delta);
      pending = true;
      schedule();
    },
  };
}

/** The playback clock, without re-rendering the caller on its frames. */
export function usePlaybackClock(options: PlaybackOptions): PlaybackClock {
  const [clock] = useState(() => createClock(options));
  const idle = options.ambient && !options.reduced;
  useLayoutEffect(() => clock.setOptions(options));
  // Turning idle motions on or off publishes the new `time` and starts or ends the loop.
  useLayoutEffect(() => {
    clock.start();
    return clock.stop;
  }, [clock, idle]);
  return clock;
}

/**
 * Re-renders the caller when `select(frame)` changes. `select` must be stable (module level).
 * State updates land in the same batch as other frame callbacks (the Pet's face morph), so a frame
 * that changes both still renders once.
 */
export function usePlaybackFrame<T>(clock: PlaybackClock, select: (frame: PlaybackFrame) => T): T {
  const [value, setValue] = useState(() => select(clock.frame()));
  useEffect(() => {
    // Compared here, not by React: a same-value setState with updates queued still renders once.
    let shown: T | undefined;
    const update = () => {
      const next = select(clock.frame());
      if (Object.is(next, shown)) return;
      shown = next;
      setValue(next);
    };
    update();
    return clock.subscribe(update);
  }, [clock, select]);
  return value;
}

const wholeFrame = (frame: PlaybackFrame) => frame;

/** Playback as React state: re-renders the caller on every frame (the Lab's editor needs it). */
export function usePlayback(options: PlaybackOptions): Playback {
  const clock = usePlaybackClock(options);
  const frame = usePlaybackFrame(clock, wholeFrame);
  const { timeNow, goTo, scrub, progressNow, beginDrag, dragBy } = clock;
  return { ...frame, timeNow, goTo, scrub, progressNow, beginDrag, dragBy };
}

/** Horizontal swipe: drags scrub the scene, release settles on a screen (flick = next/previous). */
export function useSwipe(
  play: Pick<PlaybackControls, 'goTo' | 'progressNow' | 'beginDrag' | 'dragBy'>,
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
