import { act } from 'react';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot } from 'test-renderer';

import { PET_PRESET, type FaceState, type PetEmotion } from '../petCore';
import { useFaceTransition } from '../useFaceTransition';

const { poses, motion } = PET_PRESET;
// A face key that differs between the poses used here, to tell where a morph is.
const KEY = (Object.keys(poses.happy) as (keyof FaceState)[]).find(
  (k) => poses.happy[k] !== poses.surprised[k] && typeof poses.happy[k] === 'number',
)!;

function track(initial: PetEmotion) {
  const seen: FaceState[] = [];
  function Probe({ emotion }: { emotion: PetEmotion }) {
    seen.push(useFaceTransition(poses, emotion, motion.transition, motion.easing));
    return null;
  }
  const root = createRoot();
  act(() => root.render(<Probe emotion={initial} />));
  return {
    seen,
    set: (emotion: PetEmotion) => act(() => root.render(<Probe emotion={emotion} />)),
    wait: (ms: number) => act(() => jest.advanceTimersByTime(ms)),
  };
}

describe('useFaceTransition', () => {
  beforeEach(() => jest.useFakeTimers());
  afterEach(() => jest.useRealTimers());

  it('morphs to the new pose over the Pet transition instead of snapping', () => {
    const p = track('happy');
    p.set('surprised');
    p.wait(motion.transition / 2);
    const mid = p.seen.at(-1)![KEY] as number;
    const [a, b] = [poses.happy[KEY] as number, poses.surprised[KEY] as number];
    expect(mid).toBeGreaterThan(Math.min(a, b));
    expect(mid).toBeLessThan(Math.max(a, b));
    p.wait(motion.transition);
    expect(p.seen.at(-1)).toBe(poses.surprised);
  });

  it('starts a new change from the face on screen, not from a pose', () => {
    const p = track('happy');
    p.set('surprised');
    p.wait(motion.transition / 2);
    const before = p.seen.at(-1)![KEY] as number;
    p.set('happy');
    p.wait(20);
    const after = p.seen.at(-1)![KEY] as number;
    const span = Math.abs((poses.happy[KEY] as number) - (poses.surprised[KEY] as number));
    expect(Math.abs(after - before)).toBeLessThan(span * 0.2);
    p.wait(motion.transition);
    expect(p.seen.at(-1)).toBe(poses.happy);
  });
});
