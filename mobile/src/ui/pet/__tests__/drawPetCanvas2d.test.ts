import { PET_PRESET, petFrame } from '../petCore';
import { pathBox } from '../drawPetCanvas2d';

describe('pathBox', () => {
  it('measures a cubic by its curve, not its control points (SVG objectBoundingBox)', () => {
    // Control points reach y = -10; the curve itself peaks at y = -7.5.
    expect(pathBox('M 0 0 C 0 -10 10 -10 10 0 Z')).toEqual({ x: 0, y: -7.5, width: 10, height: 7.5 });
  });

  it('covers straight segments and every point of the body petFrame draws', () => {
    expect(pathBox('M 1 2 L 5 -3 L 4 8 Z')).toEqual({ x: 1, y: -3, width: 4, height: 11 });
    const f = petFrame(PET_PRESET, {
      time: 1.3,
      face: PET_PRESET.poses.speaking,
      blink: 1,
      gaze: { x: 0.2, y: 0 },
      mirror: 0,
      reduced: false,
    });
    for (const d of [f.body, f.volume]) {
      const box = pathBox(d);
      const ends = [...d.matchAll(/(-?\d*\.?\d+) (-?\d*\.?\d+)(?= [A-Z]|$| Z)/g)].map((m) => [
        Number(m[1]),
        Number(m[2]),
      ]);
      for (const [x, y] of ends) {
        expect(x).toBeGreaterThanOrEqual(box.x - 1e-9);
        expect(y).toBeGreaterThanOrEqual(box.y - 1e-9);
        expect(x).toBeLessThanOrEqual(box.x + box.width + 1e-9);
        expect(y).toBeLessThanOrEqual(box.y + box.height + 1e-9);
      }
    }
  });

  it('rejects commands it does not measure instead of returning a wrong box', () => {
    expect(() => pathBox('M 0 0 A 5 5 0 0 1 10 0')).toThrow(/unsupported command A/);
  });
});
