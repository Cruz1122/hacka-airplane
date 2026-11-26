import { act } from 'react';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot } from 'test-renderer';

import {
  usePlayback,
  usePlaybackClock,
  usePlaybackFrame,
  type Playback,
  type PlaybackClock,
  type PlaybackFrame,
  type PlaybackOptions,
} from '../usePlayback';

const FRAME_MS = 16;
const MS = 400;
const realRaf = { request: global.requestAnimationFrame, cancel: global.cancelAnimationFrame };

function mount(options: Partial<PlaybackOptions> = {}) {
  const seen: Playback[] = [];
  function Probe() {
    seen.push(
      usePlayback({
        transitionMs: MS,
        easing: 'easeOut',
        ambient: true,
        reduced: false,
        ...options,
      }),
    );
    return null;
  }
  const root = createRoot();
  act(() => root.render(<Probe />));
  const now = () => seen.at(-1)!;
  return {
    now,
    // One act per frame: act batches every update inside it into a single render.
    frames: (n: number) => {
      for (let i = 0; i < n; i++) act(() => jest.advanceTimersByTime(FRAME_MS));
    },
    run: (f: (p: Playback) => void) => act(() => f(now())),
    unmount: () => act(() => root.unmount()),
  };
}

describe('usePlayback', () => {
  beforeEach(() => {
    jest.useFakeTimers();
    // A 60 Hz display on the fake clock.
    global.requestAnimationFrame = (cb) =>
      setTimeout(() => cb(Date.now()), FRAME_MS) as unknown as number;
    global.cancelAnimationFrame = (id) => clearTimeout(id);
  });
  afterEach(() => {
    jest.useRealTimers();
    global.requestAnimationFrame = realRaf.request;
    global.cancelAnimationFrame = realRaf.cancel;
  });

  it('animates goTo to the target within the transition time', () => {
    const p = mount();
    p.run((x) => x.goTo(1));
    p.frames(3);
    expect(p.now().progress).toBeGreaterThan(0);
    expect(p.now().progress).toBeLessThan(1);
    expect(p.now().moving).toBe(true);
    p.frames(Math.ceil(MS / FRAME_MS) + 2);
    expect(p.now().progress).toBe(1);
    expect(p.now().animating).toBe(false);
    p.unmount();
  });

  it('jumps instead of animating under reduced motion, with idle motions off', () => {
    const p = mount({ reduced: true });
    p.run((x) => x.goTo(2));
    expect(p.now().progress).toBe(2);
    expect(p.now().animating).toBe(false);
    expect(p.now().time).toBeNull();
    expect(p.now().timeNow()).toBeNull();
    p.unmount();
  });

  it('starts an interrupting goTo from the progress on screen, not from the old target', () => {
    const p = mount();
    p.run((x) => x.goTo(2));
    p.frames(4);
    const mid = p.now().progressNow();
    expect(mid).toBeGreaterThan(0);
    expect(mid).toBeLessThan(2);
    p.run((x) => x.goTo(0));
    p.frames(1);
    // Heading back: never past where the first transition had got to.
    expect(p.now().progress).toBeLessThanOrEqual(mid);
    p.frames(Math.ceil((MS * 1.6) / FRAME_MS) + 2);
    expect(p.now().progress).toBe(0);
    p.unmount();
  });

  it('cancels a transition when scrubbed (swipe, Lab scrubber)', () => {
    const p = mount();
    p.run((x) => x.goTo(2));
    p.frames(3);
    p.run((x) => x.scrub(0.5));
    p.frames(10);
    expect(p.now().progress).toBe(0.5);
    expect(p.now().animating).toBe(false);
    p.unmount();
  });

  it('holds idle motions during a transition and resumes them without a jump', () => {
    const p = mount();
    p.frames(30);
    const before = p.now().time!;
    expect(before).toBeGreaterThan(0);
    p.run((x) => x.goTo(1));
    p.frames(Math.floor(MS / FRAME_MS) - 2);
    // Frozen at its last drawn value while the camera moves.
    expect(p.now().animating).toBe(true);
    expect(p.now().time).toBe(before);
    expect(p.now().timeNow()).toBe(before);
    p.frames(10);
    expect(p.now().animating).toBe(false);
    const after = p.now().time!;
    expect(after).toBeGreaterThan(before);
    // Resumes from the held pose: only the frames since the transition ended, not the paused span.
    expect(after - before).toBeLessThan((10 * FRAME_MS) / 1000);
    p.unmount();
  });

  it('takes over a running transition when a drag starts', () => {
    const p = mount();
    p.run((x) => x.goTo(2));
    p.frames(4);
    p.run((x) => x.beginDrag());
    const mid = p.now().progressNow();
    p.run((x) => x.dragBy(0.1));
    p.frames(10);
    expect(p.now().progress).toBeCloseTo(mid + 0.1, 10);
    expect(p.now().animating).toBe(false);
    expect(p.now().moving).toBe(true);
    p.run((x) => x.goTo(Math.round(p.now().progressNow())));
    p.frames(Math.ceil((MS * 1.6) / FRAME_MS) + 2);
    expect(Number.isInteger(p.now().progress)).toBe(true);
    expect(p.now().moving).toBe(false);
    p.unmount();
  });

  it('keeps idle motions running while the user drags', () => {
    const p = mount();
    p.frames(10);
    p.run((x) => x.beginDrag());
    const before = p.now().time!;
    p.run((x) => x.dragBy(0.3));
    p.frames(10);
    expect(p.now().moving).toBe(true);
    expect(p.now().time!).toBeGreaterThan(before);
    p.unmount();
  });

  describe('clock outside React', () => {
    const screenOf = (f: PlaybackFrame) => Math.round(f.progress);
    function mountClock() {
      const seen = { renders: 0, screen: -1, clock: null as PlaybackClock | null };
      function Probe() {
        const clock = usePlaybackClock({
          transitionMs: MS,
          easing: 'easeOut',
          ambient: true,
          reduced: false,
        });
        seen.clock = clock;
        seen.screen = usePlaybackFrame(clock, screenOf);
        seen.renders++;
        return null;
      }
      const root = createRoot();
      act(() => root.render(<Probe />));
      return {
        seen,
        clock: () => seen.clock!,
        frames: (n: number) => {
          for (let i = 0; i < n; i++) act(() => jest.advanceTimersByTime(FRAME_MS));
        },
        unmount: () => act(() => root.unmount()),
      };
    }
    const valueOf = (c: PlaybackClock) =>
      (c.progressValue as unknown as { __getValue: () => number }).__getValue();

    it('renders a page subscriber only when the rounded page changes', () => {
      const p = mountClock();
      p.frames(30); // idle frames: the page does not change
      const idle = p.seen.renders;
      expect(idle).toBe(1);
      act(() => p.clock().goTo(2));
      p.frames(Math.ceil((MS * 1.6) / FRAME_MS) + 2);
      expect(p.seen.screen).toBe(2);
      // 0 -> 1 -> 2: one render per page crossed.
      expect(p.seen.renders - idle).toBe(2);
      expect(valueOf(p.clock())).toBe(2);
      p.unmount();
    });

    it('draws finger moves once per frame, with the latest one', () => {
      const p = mountClock();
      const clock = p.clock();
      let published = 0;
      const unsubscribe = clock.subscribe(() => published++);
      act(() => clock.beginDrag());
      published = 0;
      act(() => {
        clock.dragBy(0.1);
        clock.dragBy(0.2);
        clock.dragBy(0.3);
      });
      // Not drawn yet: the moves wait for the display frame.
      expect(clock.frame().progress).toBe(0);
      expect(clock.progressNow()).toBeCloseTo(0.3, 10);
      p.frames(1);
      expect(published).toBe(1);
      expect(clock.frame().progress).toBeCloseTo(0.3, 10);
      expect(valueOf(clock)).toBeCloseTo(0.3, 10);
      unsubscribe();
      p.unmount();
    });

    it('stops a running transition where it is when a drag starts', () => {
      const p = mountClock();
      const clock = p.clock();
      act(() => clock.goTo(2));
      p.frames(4);
      act(() => clock.beginDrag());
      const held = clock.progressNow();
      p.frames(5);
      expect(clock.frame().progress).toBe(held);
      expect(clock.frame().animating).toBe(false);
      expect(clock.frame().moving).toBe(true);
      p.unmount();
    });
  });
});

