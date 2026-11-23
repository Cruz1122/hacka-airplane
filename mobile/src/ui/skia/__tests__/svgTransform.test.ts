import { applyTransform, transformMatrix } from '@/onboarding/scene/geometry';
import { applyMat, IDENTITY, multiply, parseTransform } from '../svgTransform';

const close = (a: { x: number; y: number }, b: { x: number; y: number }) => {
  expect(a.x).toBeCloseTo(b.x, 2);
  expect(a.y).toBeCloseTo(b.y, 2);
};

it('matches the scene transform it was written from', () => {
  const t = {
    x: 40,
    y: -12,
    scaleX: 1.4,
    scaleY: 0.7,
    rotation: 25,
    anchorX: 10,
    anchorY: 30,
    opacity: 1,
  };
  const m = parseTransform(transformMatrix(t));
  for (const p of [
    { x: 0, y: 0 },
    { x: 10, y: 30 },
    { x: -50, y: 80 },
  ]) {
    close(applyMat(m, p.x, p.y), applyTransform(t, p));
  }
});

it('applies a list left to right like SVG', () => {
  const m = parseTransform('translate(10 0) scale(2) rotate(90 1 0)');
  // rotate(90 about (1,0)) maps (2,0) to (1,1); scale 2 -> (2,2); translate -> (12,2).
  close(applyMat(m, 2, 0), { x: 12, y: 2 });
  close(applyMat(multiply(IDENTITY, m), 2, 0), { x: 12, y: 2 });
});

it('treats an empty transform as identity and rejects unknown kinds', () => {
  expect(parseTransform('')).toEqual(IDENTITY);
  expect(parseTransform(null)).toEqual(IDENTITY);
  expect(() => parseTransform('skewX(10)')).toThrow(/unsupported/);
  expect(() => parseTransform('garbage')).toThrow(/bad transform/);
});
