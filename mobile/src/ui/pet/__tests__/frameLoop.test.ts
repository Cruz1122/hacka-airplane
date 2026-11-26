import { AMBIENT_HZ, GAZE_STEP, shouldDraw, type FrameInputs } from '../frameLoop';
import { DEFAULT_TRACKING, PET_PRESET } from '../petCore';

const still: FrameInputs = {
  time: 0,
  face: PET_PRESET.poses.idle,
  blink: 1,
  gazeX: 0,
  gazeY: 0,
  mirror: 0,
};

/** Draws in one second on a `hz` display, with `step` changing the inputs every vsync. */
function drawsPerSecond(hz: number, step: (i: number, prev: FrameInputs) => FrameInputs) {
  let drawn: FrameInputs | null = still;
  let drawnAt = 0;
  let inputs = still;
  let draws = 0;
  for (let i = 1; i <= hz; i++) {
    const now = (i * 1000) / hz;
    inputs = step(i, inputs);
    if (shouldDraw(drawn, inputs, now - drawnAt)) {
      draws++;
      drawn = inputs;
      drawnAt = now;
    }
  }
  return draws;
}

const breathing = (hz: number) => (i: number, prev: FrameInputs) => ({ ...prev, time: i / hz });

describe('shouldDraw', () => {
  it('draws the first frame', () => {
    expect(shouldDraw(null, still, 0)).toBe(true);
  });

  it.each([60, 90, 120])('draws slow motion at the ambient rate on a %i Hz display', (hz) => {
    expect(drawsPerSecond(hz, breathing(hz))).toBe(AMBIENT_HZ);
  });

  it('draws a blink, a face morph and the turn on every display frame', () => {
    const hz = 90;
    const blink = (i: number, p: FrameInputs) => ({ ...p, time: i / hz, blink: 1 - i / 200 });
    const morph = (i: number, p: FrameInputs) => ({ ...p, time: i / hz, face: { ...p.face } });
    const turn = (i: number, p: FrameInputs) => ({ ...p, time: i / hz, mirror: i / hz });
    expect(drawsPerSecond(hz, blink)).toBe(hz);
    expect(drawsPerSecond(hz, morph)).toBe(hz);
    expect(drawsPerSecond(hz, turn)).toBe(hz);
  });

  it('draws nothing while nothing moves', () => {
    expect(drawsPerSecond(90, (_, p) => p)).toBe(0);
    expect(shouldDraw(still, { ...still }, 60_000)).toBe(false);
  });

  it('keeps a slow gaze (typing) at the ambient rate but draws a fast glance at once', () => {
    const hz = 90;
    // Eye travel well under GAZE_STEP per frame: a gaze easing toward a typed character.
    const slow = GAZE_STEP / DEFAULT_TRACKING.maxMoveX / 20;
    expect(drawsPerSecond(hz, (_, p) => ({ ...p, gazeX: p.gazeX + slow }))).toBe(AMBIENT_HZ);
    const glance = { ...still, gazeX: (GAZE_STEP / DEFAULT_TRACKING.maxMoveX) * 1.01 };
    expect(shouldDraw(still, glance, 1)).toBe(true);
  });
});
