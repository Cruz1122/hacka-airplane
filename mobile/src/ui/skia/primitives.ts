// Small Skia helpers shared by the native renderers (scene and Pet): SVG path strings, hex colors
// and SVG-style matrices, so they can reuse the strings the SVG geometry already produces.
import { Skia, type SkColor, type SkPath } from '@shopify/react-native-skia';

import type { Mat } from './svgTransform';

const pathCache = new Map<string, SkPath>();
const PATH_CACHE_LIMIT = 2000;

/** SVG path data as a Skia path; geometry strings repeat across frames, so they are parsed once. */
export function svgPath(d: string): SkPath {
  let p = pathCache.get(d);
  if (!p) {
    const made = Skia.Path.MakeFromSVGString(d);
    if (!made) throw new Error(`invalid SVG path: ${d.slice(0, 60)}`);
    if (pathCache.size >= PATH_CACHE_LIMIT) pathCache.clear();
    pathCache.set(d, made);
    p = made;
  }
  return p;
}

const hexCache = new Map<string, [number, number, number]>();

/** `#rrggbb` (or `#rgb`) with an alpha, as a Skia color. */
export function skColor(hex: string, alpha = 1): SkColor {
  let rgb = hexCache.get(hex);
  if (!rgb) {
    const h = hex.replace('#', '');
    const full = h.length === 3 ? h.replace(/(.)/g, '$1$1') : h.slice(0, 6);
    const n = parseInt(full, 16);
    if (Number.isNaN(n) || full.length !== 6) throw new Error(`unsupported color ${hex}`);
    rgb = [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
    hexCache.set(hex, rgb);
  }
  return Float32Array.of(rgb[0], rgb[1], rgb[2], alpha) as unknown as SkColor;
}

export const toSkMatrix = (m: Mat) => Skia.Matrix([m[0], m[2], m[4], m[1], m[3], m[5], 0, 0, 1]);
