/* eslint-disable @typescript-eslint/no-require-imports -- modules load after CanvasKit does */
// Per-frame JS cost of the animated Pet: petFrame, the Skia drawing path (real CanvasKit, the
// engine of Skia's web build) and the chat circle's loop at the A24's 90 Hz. Skipped by default;
// run with `PET_BENCH=1 npx jest src/ui/pet/__tests__/pet.bench`. Node on a desktop is several
// times faster than Hermes on the phone, and CanvasKit calls are not JSI calls: compare these
// numbers with each other, never with the phone's frame budget.
import { act, Profiler } from 'react';
import { createRoot } from 'test-renderer';

import { GazeChannel } from '@/chat/gaze';

const bench = process.env.PET_BENCH ? describe : describe.skip;

jest.mock('@shopify/react-native-skia', () =>
  require('@shopify/react-native-skia/lib/commonjs/mock').Mock(
    (globalThis as unknown as { CanvasKit: unknown }).CanvasKit,
  ),
);
jest.mock('expo-router', () => ({ useIsFocused: () => true }));
// One call per Pet render: counts the Pet's own renders, not its subtree's commits.
let mockPetRenders = 0;
jest.mock('@/ui/useReducedMotion', () => ({
  useReducedMotion: () => {
    mockPetRenders++;
    return false;
  },
}));

const HZ = 90;
const SECONDS = 10;
const ms = (start: bigint) => Number(process.hrtime.bigint() - start) / 1e6;

function timeIt(label: string, n: number, fn: (i: number) => void) {
  for (let i = 0; i < Math.min(200, n); i++) fn(i); // warm up the JIT
  const start = process.hrtime.bigint();
  for (let i = 0; i < n; i++) fn(i);
  console.log(`${label}: ${((ms(start) * 1000) / n).toFixed(1)} us/call`);
}

/** A manual display clock: rAF callbacks run only when step() advances one vsync. */
function displayClock(hz: number) {
  let now = 0;
  let id = 0;
  let queue = new Map<number, FrameRequestCallback>();
  const g = globalThis as unknown as {
    requestAnimationFrame: (cb: FrameRequestCallback) => number;
    cancelAnimationFrame: (h: number) => void;
  };
  g.requestAnimationFrame = (cb) => {
    queue.set(++id, cb);
    return id;
  };
  g.cancelAnimationFrame = (h) => void queue.delete(h);
  jest.spyOn(performance, 'now').mockImplementation(() => now);
  return {
    step() {
      now += 1000 / hz;
      const due = queue;
      queue = new Map();
      due.forEach((cb) => cb(now));
    },
  };
}

/** Deterministic glances: the loop's Math.random decides where and when the Pet looks. */
function seedRandom() {
  let s = 42;
  jest.spyOn(Math, 'random').mockImplementation(() => {
    s = (s * 1664525 + 1013904223) % 4294967296;
    return s / 4294967296;
  });
}

/** Counts Skia objects created through `fn` (each is a JSI host object on the phone). */
function countSkia(Skia: Record<string, Record<string, () => unknown>>, fn: () => void) {
  const spies = {
    Paint: jest.spyOn(Skia as unknown as Record<string, () => unknown>, 'Paint'),
    Point: jest.spyOn(Skia as unknown as Record<string, () => unknown>, 'Point'),
    Matrix: jest.spyOn(Skia as unknown as Record<string, () => unknown>, 'Matrix'),
    RadialGradient: jest.spyOn(Skia.Shader, 'MakeRadialGradient'),
    LinearGradient: jest.spyOn(Skia.Shader, 'MakeLinearGradient'),
    PathParse: jest.spyOn(Skia.Path, 'MakeFromSVGString'),
  };
  fn();
  return Object.fromEntries(
    Object.entries(spies).map(([k, spy]) => {
      const calls = spy.mock.calls.length;
      spy.mockRestore();
      return [k, calls];
    }),
  );
}

bench('pet bench', () => {
  beforeAll(async () => {
    const init = require('canvaskit-wasm/bin/full/canvaskit.js');
    (globalThis as unknown as { CanvasKit: unknown }).CanvasKit = await init();
    // The mocked View never measures; the Pet needs its box to aim at the typed character.
    require('@react-native/jest-preset/jest/MockNativeMethods').default.measureInWindow.mockImplementation(
      (cb: (x: number, y: number, w: number, h: number) => void) => cb(8, 8, 112, 112),
    );
  });

  it('per-frame cost of petFrame and drawPet', () => {
    const { PET_PRESET, petFrame, blinkAt, copyConfig } = require('../petCore');
    const { drawPet } = require('../drawPet');
    const { Skia } = require('@shopify/react-native-skia');
    const idle = copyConfig(PET_PRESET);
    idle.emotion = 'happy';
    const talk = copyConfig(PET_PRESET);
    talk.emotion = 'speaking';
    talk.voice = 'speaking';
    talk.audio = 0.7;
    const input = (cfg: typeof PET_PRESET, i: number) => {
      const time = i / HZ;
      return {
        time,
        face: cfg.poses[cfg.emotion],
        blink: blinkAt(time, cfg.motion.blinkInterval),
        gaze: { x: 0.2, y: -0.1 },
        mirror: 0,
      };
    };
    // What Pet.tsx passes: the vapor drawers paint no smoke, so the Pet zeroes its filaments.
    const pet = copyConfig(idle);
    pet.smoke.count = 0;
    const n = 3000;
    timeIt('petFrame idle', n, (i) => petFrame(idle, input(idle, i)));
    timeIt('petFrame idle, Pet config', n, (i) => petFrame(pet, input(pet, i)));
    timeIt('petFrame speaking', n, (i) => petFrame(talk, input(talk, i)));
    const frames = Array.from({ length: n }, (_, i) => petFrame(idle, input(idle, i)));
    const record = (i: number) => {
      const recorder = Skia.PictureRecorder();
      const canvas = recorder.beginRecording(Skia.XYWHRect(0, 0, 112, 112));
      canvas.scale(0.4, 0.4);
      drawPet(canvas, idle, frames[i], '#f4f1fb', '#b9b2d6');
      recorder.finishRecordingAsPicture().dispose();
    };
    timeIt('drawPet + record picture (CanvasKit)', n, record);
    record(0); // warm caches, then count one steady-state frame
    console.log('Skia objects per frame:', JSON.stringify(countSkia(Skia, () => record(1))));
  });

  const scenarios = [
    { name: 'chat idle', voice: 'idle' as const, typing: false },
    { name: 'chat speaking', voice: 'speaking' as const, typing: false },
    { name: 'chat typing', voice: 'idle' as const, typing: true },
  ];
  it.each(scenarios)('$name loop at 90 Hz', ({ name, voice, typing }) => {
    const clock = displayClock(HZ);
    seedRandom();
    const core = require('../petCore');
    const frameSpy = jest.spyOn(core, 'petFrame');
    const { PetCircle } = require('@/chat/PetCircle');
    const gaze = new GazeChannel();
    let commits = 0;
    const root = createRoot();
    act(() =>
      root.render(
        <Profiler id="pet" onRender={() => commits++}>
          <PetCircle x={60} y={60} r={60} voice={voice} ready gaze={gaze} />
        </Profiler>,
      ),
    );
    for (let i = 0; i < HZ; i++) act(() => clock.step()); // settle the first transition
    commits = 0;
    mockPetRenders = 0;
    frameSpy.mockClear();
    const start = process.hrtime.bigint();
    for (let i = 0; i < HZ * SECONDS; i++) {
      // About 6 characters a second along a line under the Pet, wrapping every 30.
      if (typing && i % 15 === 0) act(() => gaze.set({ x: 30 + ((i / 15) % 30) * 9, y: 420 }));
      act(() => clock.step());
    }
    const total = ms(start);
    const rate = (v: number) => (v / SECONDS).toFixed(1);
    console.log(
      `${name}: ${rate(mockPetRenders)} Pet renders/s, ${rate(commits)} commits/s, ` +
        `${rate(frameSpy.mock.calls.length)} petFrame/s, ${rate(total)} ms JS/s`,
    );
    act(() => root.unmount());
    jest.restoreAllMocks();
  });
});
