// Per-frame cost of the real onboarding screen (native renderer: SceneCanvas.native + Skia on
// CanvasKit wasm), for transitions, finger drags and idle motions. Skipped unless BENCH=1:
//   BENCH=1 npx jest src/onboarding/__tests__/frameCost.bench.test.tsx
// Counts (renders, recordings, Pet frames per display frame) are the result; the milliseconds are
// desktop JIT, dev-build React and wasm, useful only to compare runs on one machine.
/* eslint-disable @typescript-eslint/no-require-imports -- CanvasKit has to load before Skia's
   mock and the modules that import it, so they are required after it. */
import { act } from 'react';
import { PanResponder, type PanResponderCallbacks } from 'react-native';
import { createRoot } from 'test-renderer';

jest.mock('@shopify/react-native-skia', () =>
  require('@shopify/react-native-skia/lib/commonjs/mock').Mock(
    (global as unknown as { CanvasKit: unknown }).CanvasKit,
  ),
);
jest.mock('expo-router', () => ({ router: { replace: () => {} } }));
jest.mock(
  'react-native-safe-area-context',
  () => jest.requireActual('react-native-safe-area-context/jest/mock').default,
);
jest.mock('@/chat/PetCircle', () => ({ PetCircle: () => null }));
jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => false }));

const mockCounts: Record<string, number> = {};
const mockBump = (k: string) => (mockCounts[k] = (mockCounts[k] ?? 0) + 1);
const mockPress = { next: () => {} };
jest.mock('@/ui/PageDots', () => {
  const real = jest.requireActual('@/ui/PageDots');
  return { ...real, PageDots: (p: object) => (mockBump('PageDots'), real.PageDots(p)) };
});
jest.mock('@/ui/PrimaryButton', () => {
  const real = jest.requireActual('@/ui/PrimaryButton');
  return {
    ...real,
    PrimaryButton: (p: { onPress: () => void }) => {
      mockBump('PrimaryButton');
      mockPress.next = p.onPress;
      return real.PrimaryButton(p);
    },
  };
});
jest.mock('@/onboarding/SceneCanvas', () => {
  const real = jest.requireActual('@/onboarding/SceneCanvas');
  return { SceneCanvas: (p: object) => (mockBump('SceneCanvas'), real.SceneCanvas(p)) };
});
jest.mock('@/onboarding/layout', () => {
  const real = jest.requireActual('@/onboarding/layout');
  return {
    ...real,
    onboardingLayout: (...a: unknown[]) => (mockBump('OnboardingScreen'), real.onboardingLayout(...a)),
  };
});
jest.mock('@/ui/pet/petCore', () => {
  const real = jest.requireActual('@/ui/pet/petCore');
  return { ...real, petFrame: (...a: unknown[]) => (mockBump('petFrame'), real.petFrame(...a)) };
});

const FRAME_MS = 11; // the reference phone's 90 Hz
const bench = process.env.BENCH ? it : it.skip;

bench('onboarding frame cost', async () => {
  const g = global as unknown as { CanvasKit: unknown };
  g.CanvasKit = await require('canvaskit-wasm/bin/full/canvaskit')({});
  const { Skia } = require('@shopify/react-native-skia');
  // CanvasKit lacks MakeMatrixTransform: the half-resolution blur becomes a plain blur here.
  Skia.ImageFilter.MakeMatrixTransform = (_m: unknown, _f: unknown, _mm: unknown, input: unknown) =>
    input ?? Skia.ImageFilter.MakeOffset(0, 0, null);
  const recorder = Skia.PictureRecorder.bind(Skia);
  Skia.PictureRecorder = () => (mockBump('pictures recorded'), recorder());
  let pan: PanResponderCallbacks = {};
  const create = PanResponder.create.bind(PanResponder);
  jest.spyOn(PanResponder, 'create').mockImplementation((config) => ((pan = config), create(config)));

  // performance stays fake so the Pet's face morph (performance.now) runs on display frames too.
  jest.useFakeTimers({ doNotFake: ['hrtime'] });
  global.requestAnimationFrame = (cb) =>
    setTimeout(() => cb(Date.now()), FRAME_MS) as unknown as number;
  global.cancelAnimationFrame = (id) => clearTimeout(id);
  const OnboardingScreen = require('../../../app/onboarding').default;
  const root = createRoot();
  act(() => root.render(<OnboardingScreen />));

  const rows: string[] = [];
  const measure = (label: string, frames: number, perFrame: (f: number) => void = () => {}) => {
    for (const k of Object.keys(mockCounts)) mockCounts[k] = 0;
    const t0 = process.hrtime.bigint();
    for (let f = 0; f < frames; f++)
      act(() => {
        perFrame(f);
        jest.advanceTimersByTime(FRAME_MS);
      });
    const ms = Number(process.hrtime.bigint() - t0) / 1e6 / frames;
    const counts = Object.entries(mockCounts)
      .filter(([, v]) => v > 0)
      .map(([k, v]) => `${k} ${(v / frames).toFixed(2)}`)
      .join(', ');
    rows.push(`${label.padEnd(26)} ${ms.toFixed(2)} ms/frame | per frame: ${counts}`);
  };
  measure('warm-up (idle)', 90);
  measure('idle', 270);
  for (let s = 0; s < 2; s++) {
    act(() => mockPress.next());
    measure(`transition ${s + 1}->${s + 2} (480 ms)`, 44);
    measure('face morph tail + idle', 30);
  }
  // A finger drag back toward screen 1: two touch moves per display frame (180 Hz touch sampling).
  act(() => pan.onPanResponderGrant?.({} as never, {} as never));
  measure('drag (2 moves/frame)', 60, (f) => {
    for (const k of [0, 0.5])
      pan.onPanResponderMove?.({} as never, { dx: (f + k) * 4 } as never);
  });
  act(() => pan.onPanResponderRelease?.({} as never, { vx: 0 } as never));
  measure('settle after drag', 50);
  act(() => root.unmount());
  console.log(rows.join('\n'));
});
