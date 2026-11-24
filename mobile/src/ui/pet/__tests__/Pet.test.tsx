import { act, type ComponentProps } from 'react';
import { createRoot } from 'test-renderer';

import type { FrameStore } from '../frameLoop';
import { Pet } from '../Pet';
import { copyConfig, PET_PRESET, petFrame, type PetEmotion, type PetFrame } from '../petCore';

// The canvas is the only subscriber to the Pet's frames: record what it would paint.
const mockPainted: PetFrame[] = [];
jest.mock('../PetVaporCanvas', () => ({
  PetVaporCanvas: function Probe({ frames }: { frames: FrameStore }) {
    mockPainted.push(jest.requireActual('../frameLoop').useFrame(frames));
    return null;
  },
}));
let mockPetRenders = 0;
jest.mock('@/ui/useReducedMotion', () => ({
  useReducedMotion: () => {
    mockPetRenders++;
    return false;
  },
}));

const HZ = 90;

/** A manual display clock: rAF callbacks run only when step() advances one vsync. */
function displayClock() {
  let now = 0;
  let id = 0;
  let queue = new Map<number, FrameRequestCallback>();
  jest.spyOn(globalThis, 'requestAnimationFrame').mockImplementation((cb) => {
    queue.set(++id, cb);
    return id;
  });
  jest
    .spyOn(globalThis, 'cancelAnimationFrame')
    .mockImplementation((h) => void queue.delete(Number(h)));
  jest.spyOn(performance, 'now').mockImplementation(() => now);
  return {
    run(seconds: number) {
      for (let i = 0; i < seconds * HZ; i++) {
        now += 1000 / HZ;
        const due = queue;
        queue = new Map();
        act(() => due.forEach((cb) => cb(now)));
      }
    },
    pending: () => queue.size,
  };
}

function mount(props: Partial<ComponentProps<typeof Pet>>) {
  const root = createRoot();
  const render = (next: Partial<ComponentProps<typeof Pet>>) =>
    act(() => root.render(<Pet emotion="happy" {...props} {...next} />));
  render({});
  return { render, unmount: () => act(() => root.unmount()) };
}

/** The still frame of `emotion` that a reduced-motion Pet shows. */
function stillFrame(emotion: PetEmotion) {
  const cfg = copyConfig(PET_PRESET);
  cfg.emotion = emotion;
  cfg.motion.reducedEffects = true;
  const face = cfg.poses[emotion];
  return petFrame(cfg, { time: 0, face, blink: 1, gaze: { x: 0, y: 0 }, mirror: 0, reduced: true });
}

describe('Pet loop', () => {
  beforeEach(() => {
    mockPainted.length = 0;
    mockPetRenders = 0;
  });
  afterEach(() => jest.restoreAllMocks());

  it('paints frames without re-rendering the Pet, at a slow rate when idle', () => {
    const clock = displayClock();
    const pet = mount({});
    clock.run(1); // the first second also eases into the initial glance
    mockPetRenders = 0;
    const before = mockPainted.length;
    clock.run(4);
    const perSecond = (mockPainted.length - before) / 4;
    expect(mockPetRenders).toBe(0);
    // Ambient 30 Hz plus the frames of a blink or a glance, far under the 90 Hz display.
    expect(perSecond).toBeGreaterThanOrEqual(30);
    expect(perSecond).toBeLessThan(50);
    pet.unmount();
  });

  it('sleeps once paused and settled, and wakes to morph to a new emotion', () => {
    const clock = displayClock();
    const pet = mount({ paused: true, lookAround: false });
    clock.run(1);
    expect(clock.pending()).toBe(0);
    const asleep = mockPainted.length;
    pet.render({ emotion: 'surprised' });
    clock.run(PET_PRESET.motion.transition / 1000 / 2);
    expect(mockPainted.length).toBeGreaterThan(asleep);
    expect(clock.pending()).toBe(1); // still morphing
    clock.run(1);
    expect(clock.pending()).toBe(0);
    pet.unmount();
  });

  it('shows the new pose at once under reduced motion, with no loop', () => {
    const clock = displayClock();
    const pet = mount({ reducedMotion: true });
    expect(clock.pending()).toBe(0);
    pet.render({ reducedMotion: true, emotion: 'surprised' });
    const shown = mockPainted.at(-1)!;
    const expected = stillFrame('surprised');
    expect(shown.mouth).toEqual(expected.mouth);
    expect(shown.leftEye).toEqual(expected.leftEye);
    expect(clock.pending()).toBe(0);
    pet.unmount();
  });

  it('paints the same frame as the preset, minus the smoke no drawer paints', () => {
    displayClock();
    const pet = mount({ reducedMotion: true, emotion: 'curious' });
    const shown = mockPainted.at(-1)!;
    expect(shown.smoke).toEqual([]);
    expect({ ...shown, smoke: [] }).toEqual({ ...stillFrame('curious'), smoke: [] });
    pet.unmount();
  });
});
