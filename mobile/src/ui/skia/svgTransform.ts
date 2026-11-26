// SVG transform attributes as 2D affine matrices, so the Skia renderers can reuse the transform
// strings the scene geometry and the Pet already produce (transformMatrix, parallaxMatrix, petFrame).
// A matrix [a, b, c, d, e, f] maps (x, y) to (a x + c y + e, b x + d y + f), as in SVG.

export type Mat = readonly [number, number, number, number, number, number];

export const IDENTITY: Mat = [1, 0, 0, 1, 0, 0];

/** `m` applied after `n` (SVG order: parent first, then child). */
export function multiply(m: Mat, n: Mat): Mat {
  return [
    m[0] * n[0] + m[2] * n[1],
    m[1] * n[0] + m[3] * n[1],
    m[0] * n[2] + m[2] * n[3],
    m[1] * n[2] + m[3] * n[3],
    m[0] * n[4] + m[2] * n[5] + m[4],
    m[1] * n[4] + m[3] * n[5] + m[5],
  ];
}

const translate = (x: number, y: number): Mat => [1, 0, 0, 1, x, y];

function rotate(degrees: number, cx = 0, cy = 0): Mat {
  const r = (degrees * Math.PI) / 180;
  const c = Math.cos(r);
  const s = Math.sin(r);
  const m: Mat = [c, s, -s, c, 0, 0];
  return cx === 0 && cy === 0 ? m : multiply(multiply(translate(cx, cy), m), translate(-cx, -cy));
}

const cache = new Map<string, Mat>();
const CACHE_LIMIT = 512;

/**
 * Parses the subset of SVG transform syntax this app writes: matrix, translate, rotate, scale.
 * Throws on anything else so a new transform kind fails loudly instead of drawing in the wrong place.
 */
export function parseTransform(text: string | null | undefined): Mat {
  if (!text) return IDENTITY;
  const hit = cache.get(text);
  if (hit) return hit;
  let out: Mat = IDENTITY;
  const re = /(\w+)\s*\(([^)]*)\)/g;
  let match: RegExpExecArray | null;
  let consumed = 0;
  while ((match = re.exec(text))) {
    const args = match[2]
      .trim()
      .split(/[\s,]+/)
      .filter((s) => s !== '')
      .map(Number);
    if (args.some((n) => !Number.isFinite(n))) throw new Error(`bad transform: ${text}`);
    let m: Mat;
    switch (match[1]) {
      case 'matrix':
        if (args.length !== 6) throw new Error(`bad transform: ${text}`);
        m = args as unknown as Mat;
        break;
      case 'translate':
        m = translate(args[0] ?? 0, args[1] ?? 0);
        break;
      case 'rotate':
        m = rotate(args[0] ?? 0, args[1] ?? 0, args[2] ?? 0);
        break;
      case 'scale':
        m = [args[0] ?? 1, 0, 0, args[1] ?? args[0] ?? 1, 0, 0];
        break;
      default:
        throw new Error(`unsupported transform ${match[1]} in: ${text}`);
    }
    out = multiply(out, m);
    consumed += match[0].length;
  }
  if (consumed === 0 && text.trim() !== '') throw new Error(`bad transform: ${text}`);
  if (cache.size >= CACHE_LIMIT) cache.clear();
  cache.set(text, out);
  return out;
}

export function applyMat(m: Mat, x: number, y: number): { x: number; y: number } {
  return { x: m[0] * x + m[2] * y + m[4], y: m[1] * x + m[3] * y + m[5] };
}
