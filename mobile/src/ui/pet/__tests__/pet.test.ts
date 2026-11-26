import {
  blinkAt,
  interpolateFaceState,
  PET_ACCESSORIES,
  PET_ACCESSORY_VIEWBOX,
  PET_EMOTIONS,
  PET_PRESET,
  petFrame,
  petVaporPuffs,
  transitionFace,
  VOICE_STATES,
  type PetAccessory,
} from '../petCore';
import { parseTransform } from '@/ui/skia/svgTransform';

const finite = (value: unknown) => !/NaN|Infinity/.test(JSON.stringify(value));

describe('pet', () => {
  it('turns to look left in place: the body center does not move sideways', () => {
    const face = PET_PRESET.poses.idle;
    const at = (mirror: number) => {
      const f = petFrame(PET_PRESET, { time: 0, face, blink: 1, gaze: { x: 0, y: 0 }, mirror });
      const rim = f.vapor.slice(0, 14); // the head's rim puffs, centred on the body
      return rim.reduce((sum, p) => sum + p.x, 0) / rim.length + f.shiftX;
    };
    // Only the head's asymmetry flips side; the old turn slid the whole Pet 2 * |body.x| = 64.
    const asym = Math.abs(PET_PRESET.body.asymmetry) * 0.07 * 2;
    expect(Math.abs(at(1) - at(0))).toBeLessThanOrEqual(asym + 0.5);
    expect(Math.abs(at(0.5) - at(0))).toBeLessThanOrEqual(asym + 0.5);
  });

  it('the head shading turns with the head (no mask left on the face)', () => {
    const face = PET_PRESET.poses.idle;
    const at = (mirror: number) =>
      petFrame(PET_PRESET, { time: 0, face, blink: 1, gaze: { x: 0, y: 0 }, mirror });
    const before = at(0);
    const after = at(1);
    expect(before.headX).toBe(PET_PRESET.body.x);
    // On screen (after shiftX) the head center stays put while the shading follows it.
    expect(after.headX + after.shiftX).toBeCloseTo(before.headX + before.shiftX, 5);
  });

  it('draws every emotion and voice with finite geometry over time', () => {
    for (const emotion of PET_EMOTIONS) {
      for (const voice of VOICE_STATES) {
        const cfg = { ...PET_PRESET, emotion, voice, audio: 0.6 };
        for (const time of [0, 0.4, 3.3, 61.7]) {
          const frame = petFrame(cfg, {
            time,
            face: cfg.poses[emotion],
            blink: blinkAt(time, 4),
            gaze: { x: -0.7, y: 0.3 },
            mirror: 0.5,
          });
          expect({ emotion, voice, time, finite: finite(frame) }).toEqual({
            emotion,
            voice,
            time,
            finite: true,
          });
        }
      }
    }
  });

  it('starts at rest', () => {
    expect([PET_PRESET.emotion, PET_PRESET.voice, PET_PRESET.audio]).toEqual(['idle', 'idle', 0]);
  });

  it('blinks briefly once per interval and keeps its eyes open otherwise', () => {
    const samples = Array.from({ length: 4000 }, (_, i) => blinkAt(i / 100, 4));
    const closed = samples.filter((v) => v < 0.5).length / samples.length;
    expect(Math.min(...samples)).toBeGreaterThanOrEqual(0.045);
    expect(Math.max(...samples)).toBe(1);
    expect(closed).toBeGreaterThan(0);
    expect(closed).toBeLessThan(0.05);
  });

  it('keeps the vapor continuous when the tail flow loops', () => {
    // The tail flow wraps every 1 / 0.22 s; just before and after, every visible puff must have a
    // near-identical twin, or the tail would visibly jump.
    const wrap = 3 / 0.22;
    const before = petVaporPuffs(PET_PRESET, wrap - 1e-4);
    const after = petVaporPuffs(PET_PRESET, wrap + 1e-4);
    const close = (a: (typeof before)[number], b: (typeof before)[number]) =>
      Math.abs(a.x - b.x) < 0.5 &&
      Math.abs(a.y - b.y) < 0.5 &&
      Math.abs(a.r - b.r) < 0.5 &&
      Math.abs(a.opacity - b.opacity) < 0.02;
    for (const p of after.filter((q) => q.opacity > 0.02)) {
      expect(before.some((q) => close(p, q))).toBe(true);
    }
  });

  it('holds still under reduced motion', () => {
    const cfg = { ...PET_PRESET, voice: 'speaking' as const, audio: 0.8 };
    const at = (time: number) =>
      petFrame(cfg, { time, face: cfg.poses.idle, blink: 0.1, reduced: true });
    expect(at(1.3)).toEqual(at(7.9));
    expect(at(1.3).leftEye.d).toBe(
      petFrame(cfg, { time: 0, face: cfg.poses.idle, blink: 1, reduced: true }).leftEye.d,
    );
  });

  it('eases from one emotion pose to the next and lands exactly on it', () => {
    const cfg = { ...PET_PRESET, emotion: 'happy' as const };
    const from = cfg.poses.sad;
    expect(transitionFace(cfg, from, 0)).toEqual(interpolateFaceState(from, cfg.poses.happy, 0));
    expect(transitionFace(cfg, from, cfg.motion.transition)).toBe(cfg.poses.happy);
  });
});

describe('pet accessory', () => {
  const face = PET_PRESET.poses.idle;
  const at = (accessory: PetAccessory | undefined, mirror: number) =>
    petFrame({ ...PET_PRESET, accessory }, { time: 0, face, blink: 1, mirror });

  it('adds nothing to a Pet that wears none', () => {
    expect('accessory' in at(undefined, 0)).toBe(false);
  });

  it('sits on the head and turns with it', () => {
    for (const kind of PET_ACCESSORIES) {
      const ahead = parseTransform(at(kind, 0).accessory!.transform);
      const turned = parseTransform(at(kind, 1).accessory!.transform);
      // Facing right, then mirrored to face left: the x axis flips, the y axis does not.
      expect(Math.sign(ahead[0])).toBe(1);
      expect(Math.sign(turned[0])).toBe(-1);
      // Its origin is on the head's top, inside the accessory viewBox.
      expect(ahead[5]).toBeGreaterThan(PET_ACCESSORY_VIEWBOX.y);
      expect(ahead[5]).toBeLessThan(PET_PRESET.body.y);
    }
  });
});
