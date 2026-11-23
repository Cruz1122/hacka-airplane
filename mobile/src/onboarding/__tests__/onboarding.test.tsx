import { act } from 'react';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot } from 'test-renderer';

import OnboardingScreen from '../../../app/onboarding';
import { defaultScene } from '../scene/preset';

// Each test counts the overlay's button renders (the overlay's onDone/onGo reach it) and drives the
// screen with its handlers, so the scene's SVG and the chat route are stubbed out.
const mockButton: { renders: number; press: () => void } = { renders: 0, press: () => {} };
const mockReplace = jest.fn();
let mockReduced = false;

jest.mock('expo-router', () => ({ router: { replace: (to: unknown) => mockReplace(to) } }));
jest.mock(
  'react-native-safe-area-context',
  () => jest.requireActual('react-native-safe-area-context/jest/mock').default,
);
jest.mock('@/onboarding/SceneCanvas', () => ({ SceneCanvas: () => null }));
jest.mock('@/chat/PetCircle', () => ({ PetCircle: () => null }));
jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => mockReduced }));
jest.mock('@/ui/PrimaryButton', () => ({
  PrimaryButton: ({ onPress }: { onPress: () => void }) => {
    mockButton.renders++;
    mockButton.press = onPress;
    return null;
  },
}));

const FRAME_MS = 16;
const TRANSITION_MS = defaultScene().timeline.transitionMs;
const realRaf = { request: global.requestAnimationFrame, cancel: global.cancelAnimationFrame };

/** A 60 Hz display on the fake clock, so frames are deterministic. */
function fakeFrames() {
  global.requestAnimationFrame = (cb) =>
    setTimeout(() => cb(Date.now()), FRAME_MS) as unknown as number;
  global.cancelAnimationFrame = (id) => clearTimeout(id);
}

function mount() {
  const root = createRoot();
  act(() => root.render(<OnboardingScreen />));
  return {
    // One act per frame: act batches every update inside it into a single render.
    frames: (n: number) => {
      for (let i = 0; i < n; i++) act(() => jest.advanceTimersByTime(FRAME_MS));
    },
    press: () => act(() => mockButton.press()),
    unmount: () => act(() => root.unmount()),
  };
}

describe('OnboardingScreen playback', () => {
  beforeEach(() => {
    jest.useFakeTimers();
    fakeFrames();
    mockButton.renders = 0;
    mockReplace.mockReset();
    mockReduced = false;
  });
  afterEach(() => {
    jest.useRealTimers();
    global.requestAnimationFrame = realRaf.request;
    global.cancelAnimationFrame = realRaf.cancel;
  });

  it('does not re-render the overlay on idle-motion frames', () => {
    const s = mount();
    s.frames(5);
    const settled = mockButton.renders;
    s.frames(60); // ~1 s of idle motion, ~30 idle clock ticks
    expect(mockButton.renders - settled).toBe(0);
    s.unmount();
  });

  it('re-renders the overlay while a transition moves the copy, then stops', () => {
    const s = mount();
    s.frames(5);
    const before = mockButton.renders;
    s.press(); // "next"
    s.frames(Math.ceil(TRANSITION_MS / FRAME_MS) + 2);
    const after = mockButton.renders;
    expect(after - before).toBeGreaterThan(5);
    s.frames(60);
    expect(mockButton.renders).toBe(after);
    s.unmount();
  });

  it('hands the idle-motion pose on screen to the chat when leaving', () => {
    const s = mount();
    s.frames(20);
    for (let i = 0; i < 2; i++) {
      s.press(); // "next"
      s.frames(Math.ceil(TRANSITION_MS / FRAME_MS) + 2);
    }
    s.frames(10);
    s.press(); // "start" on the last screen
    s.frames(120); // the handoff motion, then the route change
    expect(mockReplace).toHaveBeenCalledTimes(1);
    const to = mockReplace.mock.calls[0][0] as { pathname: string; params: { sceneTime: string } };
    expect(to.pathname).toBe('/');
    expect(Number(to.params.sceneTime)).toBeGreaterThan(0);
    s.unmount();
  });

  it('opens the chat without a handoff or idle-motion time under reduced motion', () => {
    mockReduced = true;
    const s = mount();
    s.press();
    s.press();
    s.press(); // "start" on the last screen
    expect(mockReplace).toHaveBeenCalledWith('/');
    s.unmount();
  });
});
