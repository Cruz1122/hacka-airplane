import { act } from 'react';
import { createRoot } from 'test-renderer';

import { PetCircle } from '../PetCircle';

// The Pet's canvas is the only thing that repaints per frame: count what it receives.
let mockPaints = 0;
jest.mock('@/ui/pet/PetVaporCanvas', () => ({
  PetVaporCanvas: function Probe({ frames }: { frames: unknown }) {
    jest.requireActual('@/ui/pet/frameLoop').useFrame(frames);
    mockPaints++;
    return null;
  },
}));
// Like the real hook, focus changes re-render the (memoized) circle.
let mockFocused = true;
const mockListeners = new Set<() => void>();
jest.mock('expo-router', () => ({
  useIsFocused: () =>
    jest.requireActual('react').useSyncExternalStore(
      (listener: () => void) => {
        mockListeners.add(listener);
        return () => mockListeners.delete(listener);
      },
      () => mockFocused,
    ),
}));
const setFocused = (focused: boolean) =>
  act(() => {
    mockFocused = focused;
    mockListeners.forEach((l) => l());
  });

const HZ = 90;

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

describe('PetCircle', () => {
  afterEach(() => {
    mockFocused = true;
    jest.restoreAllMocks();
  });

  it('holds still while another screen covers the chat, and moves again on return', () => {
    const clock = displayClock();
    const root = createRoot();
    act(() => root.render(<PetCircle x={60} y={60} r={60} voice="idle" ready />));
    clock.run(1);
    setFocused(false);
    clock.run(2); // finish any glance in flight, then sleep
    expect(clock.pending()).toBe(0);
    const covered = mockPaints;
    clock.run(1);
    expect(mockPaints).toBe(covered);
    setFocused(true);
    clock.run(1);
    expect(mockPaints).toBeGreaterThanOrEqual(covered + 30);
    act(() => root.unmount());
  });
});
