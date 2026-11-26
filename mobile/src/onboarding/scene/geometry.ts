// Pure geometry: scene parameters in, SVG path data and primitive lists out.
// No React and no react-native-svg here so the same shapes feed the app, the Lab and tests.
// Detail (grass, leaves, rock streaks) is merged into a few long paths: the element count, not
// the path length, is what costs on a phone.
import type {
  Camera,
  CloudBody,
  LupineBody,
  CraterBody,
  FlowerBody,
  FrailejonBody,
  MistBody,
  RidgeBody,
  RockBody,
  SnowCapBody,
  SteamBody,
  Transform,
  TuftBody,
  Vec,
  VolcanoBody,
} from './types';
import { SCENE_HEIGHT, SCENE_WIDTH } from './types';

const r2 = (n: number) => Math.round(n * 100) / 100;
const pt = (p: Vec) => `${r2(p.x)} ${r2(p.y)}`;
const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
const deg = (d: number) => (d * Math.PI) / 180;
const smoothstep = (a: number, b: number, x: number) => {
  const t = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
};
const poly = (points: Vec[]) => `M ${points.map(pt).join(' L ')} Z`;

/** Deterministic PRNG so the same seed always draws the same fog, rocks and grass. */
/** Lupine parts: stem, palmate leaves (one path) and florets bottom to top (f = 0..1). */
export function lupineShape(b: LupineBody) {
  const r = rng(b.seed);
  const n = Math.max(3, Math.round(b.florets));
  const spikeBase = b.height * 0.38;
  const lean = (r() - 0.5) * b.width * 0.5;
  const florets = Array.from({ length: n }, (_, i) => {
    const f = i / (n - 1);
    const half = (b.width / 2) * (1 - 0.75 * f);
    const side = i % 2 === 0 ? -1 : 1;
    return {
      x: lean * f + side * half * (0.35 + 0.25 * r()),
      y: -(spikeBase + (b.height - spikeBase) * f),
      rx: half * 0.62,
      ry: half * 0.48,
      f,
    };
  });
  const top = florets[n - 1];
  const stem = `M 0 0 Q ${r2(lean * 0.3)} ${r2(-b.height * 0.5)} ${r2(top.x)} ${r2(top.y)}`;
  let leaves = '';
  const leafY = -b.height * 0.12;
  for (let i = 0; i < 7; i++) {
    const a = deg(-80 + (160 * i) / 6 + (r() - 0.5) * 10);
    const len = b.width * (0.75 + 0.35 * r());
    const tip = { x: Math.sin(a) * len, y: leafY - Math.cos(a) * len * 0.55 };
    const nx = -Math.cos(a) * len * 0.12;
    const ny = -Math.sin(a) * len * 0.07;
    const mid = { x: tip.x * 0.5, y: (leafY + tip.y) * 0.5 };
    leaves += `M 0 ${r2(leafY)} Q ${r2(mid.x + nx)} ${r2(mid.y + ny)} ${r2(tip.x)} ${r2(tip.y)} Q ${r2(mid.x - nx)} ${r2(mid.y - ny)} 0 ${r2(leafY)} Z `;
  }
  return { stem, leaves: leaves.trim(), florets };
}

export function rng(seed: number): () => number {
  let s = seed >>> 0 || 1;
  return () => {
    s = (s + 0x6d2b79f5) >>> 0;
    let t = s;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function hash(n: number, seed: number): number {
  const x = Math.sin(n * 127.1 + seed * 311.7) * 43758.5453;
  return x - Math.floor(x);
}

/** 1D value noise in [-1, 1]. */
function vnoise(x: number, seed: number): number {
  const i = Math.floor(x);
  const f = x - i;
  const u = f * f * (3 - 2 * f);
  return lerp(hash(i, seed), hash(i + 1, seed), u) * 2 - 1;
}

/** Fractal noise: octaves of value noise, roughly in [-1, 1]. */
export function fbm(x: number, seed: number, octaves = 4): number {
  let sum = 0;
  let amp = 1;
  let freq = 1;
  let norm = 0;
  for (let o = 0; o < octaves; o++) {
    sum += amp * vnoise(x * freq, seed + o * 17);
    norm += amp;
    amp *= 0.5;
    freq *= 2.03;
  }
  return sum / norm;
}

// ---------------------------------------------------------------- viewport and transforms

/** Widest window the preset's bleed covers (layers span about x -620..1010 at zoom 1). */
export const MAX_VIEW_WIDTH = 1500;

/**
 * Visible scene window for a screen of w x h. Narrow screens keep the reference width and show
 * more sky; wide screens (tablets) keep the reference height and show more landscape on both
 * sides, up to MAX_VIEW_WIDTH, past which the top of the sky is cropped instead. The bottom edge is
 * always the scene's bottom, so the ground and the text area never drift.
 */
export function sceneViewBox(
  w: number,
  h: number,
): { x: number; y: number; width: number; height: number } {
  if (!(w > 0 && h > 0)) return { x: 0, y: 0, width: SCENE_WIDTH, height: SCENE_HEIGHT };
  const aspect = w / h;
  let width = SCENE_WIDTH;
  let height = SCENE_WIDTH / aspect;
  if (aspect >= SCENE_WIDTH / SCENE_HEIGHT) {
    width = SCENE_HEIGHT * aspect;
    height = SCENE_HEIGHT;
    if (width > MAX_VIEW_WIDTH) {
      width = MAX_VIEW_WIDTH;
      height = MAX_VIEW_WIDTH / aspect;
    }
  }
  return {
    x: SCENE_WIDTH / 2 - width / 2,
    y: SCENE_HEIGHT - height,
    width,
    height,
  };
}

/** SVG matrix for: translate(x, y) rotate(rotation) scale(sx, sy) translate(-anchor). */
export function transformMatrix(t: Transform): string {
  const c = Math.cos(deg(t.rotation));
  const s = Math.sin(deg(t.rotation));
  const a = c * t.scaleX;
  const b = s * t.scaleX;
  const cc = -s * t.scaleY;
  const d = c * t.scaleY;
  const e = t.x - (a * t.anchorX + cc * t.anchorY);
  const f = t.y - (b * t.anchorX + d * t.anchorY);
  return `matrix(${[a, b, cc, d, e, f].map((n) => r2(n * 1000) / 1000).join(' ')})`;
}

/** The point `transformMatrix(t)` maps `p` to. */
export function applyTransform(t: Transform, p: Vec): Vec {
  const c = Math.cos(deg(t.rotation));
  const s = Math.sin(deg(t.rotation));
  const x = (p.x - t.anchorX) * t.scaleX;
  const y = (p.y - t.anchorY) * t.scaleY;
  return { x: t.x + c * x - s * y, y: t.y + s * x + c * y };
}

/** Point the camera zooms toward: horizontal center, just above the ground line. */
export const CAMERA_FOCUS: Vec = { x: SCENE_WIDTH / 2, y: SCENE_HEIGHT * 0.62 };

/**
 * Parallax: a layer with factor p moves p times the camera pan and gets p of the camera zoom.
 * p = 0 is fixed (sky), p = 1 tracks the camera exactly, p > 1 overshoots (foreground).
 */
export function parallaxMatrix(camera: Camera, parallax: number): string {
  return affineMatrix(parallaxAffine(camera, parallax));
}

/** Uniform scale plus translation: p -> k * p + (e, f). Every camera move has this shape. */
export interface Affine {
  k: number;
  e: number;
  f: number;
}

export function parallaxAffine(camera: Camera, parallax: number): Affine {
  const k = 1 + (camera.zoom - 1) * parallax;
  return {
    k,
    e: CAMERA_FOCUS.x - k * CAMERA_FOCUS.x - camera.x * parallax * k,
    f: CAMERA_FOCUS.y - k * CAMERA_FOCUS.y - camera.y * parallax * k,
  };
}

export const applyAffine = (a: Affine, p: Vec): Vec => ({ x: a.k * p.x + a.e, y: a.k * p.y + a.f });

export function affineMatrix(a: Affine): string {
  const k = r2(a.k * 1000) / 1000;
  return `matrix(${k} 0 0 ${k} ${r2(a.e)} ${r2(a.f)})`;
}

/** `a` applied after `b`. */
export function composeAffine(a: Affine, b: Affine): Affine {
  return { k: a.k * b.k, e: a.k * b.e + a.e, f: a.k * b.f + a.f };
}

export function invertAffine(a: Affine): Affine {
  return { k: 1 / a.k, e: -a.e / a.k, f: -a.f / a.k };
}

/** Camera move of a layer from the camera its SVG was drawn with (`baked`) to `camera`. */
export function cameraDelta(camera: Camera, baked: Camera, parallax: number): Affine {
  return composeAffine(
    parallaxAffine(camera, parallax),
    invertAffine(parallaxAffine(baked, parallax)),
  );
}

/**
 * `delta` (scene units) as a view transform in points for a w x h view showing `vb`, written for
 * transform-origin at the view center (the React Native and CSS default):
 * translate(translateX, translateY) scale(scale).
 */
export function viewTransform(
  delta: Affine,
  vb: { x: number; y: number; width: number },
  w: number,
  h: number,
): { translateX: number; translateY: number; scale: number } {
  const s = w / vb.width;
  const k = delta.k;
  return {
    translateX: s * (delta.e + (k - 1) * vb.x) + ((k - 1) * w) / 2,
    translateY: s * (delta.f + (k - 1) * vb.y) + ((k - 1) * h) / 2,
    scale: k,
  };
}

// ---------------------------------------------------------------- curves

interface Seg {
  c1: Vec;
  c2: Vec;
  p: Vec;
}

/** Catmull-Rom through points as cubic segments; tension 0 = polyline, 1 = full smoothing. */
function smoothSegments(points: Vec[], tension: number): Seg[] {
  const segs: Seg[] = [];
  for (let i = 0; i < points.length - 1; i++) {
    const p0 = points[Math.max(0, i - 1)];
    const p1 = points[i];
    const p2 = points[i + 1];
    const p3 = points[Math.min(points.length - 1, i + 2)];
    const k = tension / 6;
    segs.push({
      c1: { x: p1.x + (p2.x - p0.x) * k, y: p1.y + (p2.y - p0.y) * k },
      c2: { x: p2.x - (p3.x - p1.x) * k, y: p2.y - (p3.y - p1.y) * k },
      p: p2,
    });
  }
  return segs;
}

function cubicAt(p0: Vec, c1: Vec, c2: Vec, p1: Vec, t: number): Vec {
  const u = 1 - t;
  return {
    x: u * u * u * p0.x + 3 * u * u * t * c1.x + 3 * u * t * t * c2.x + t * t * t * p1.x,
    y: u * u * u * p0.y + 3 * u * u * t * c1.y + 3 * u * t * t * c2.y + t * t * t * p1.y,
  };
}

function sampleCubic(p0: Vec, c1: Vec, c2: Vec, p1: Vec, n: number): Vec[] {
  return Array.from({ length: n }, (_, i) => cubicAt(p0, c1, c2, p1, (i + 1) / n));
}

/** y of a polyline sorted by x, at x (clamped to its ends). */
function yAt(samples: Vec[], x: number): number {
  if (x <= samples[0].x) return samples[0].y;
  let lo = 0;
  let hi = samples.length - 1;
  if (x >= samples[hi].x) return samples[hi].y;
  while (hi - lo > 1) {
    const mid = (lo + hi) >> 1;
    if (samples[mid].x <= x) lo = mid;
    else hi = mid;
  }
  const a = samples[lo];
  const b = samples[hi];
  return lerp(a.y, b.y, (x - a.x) / (b.x - a.x || 1));
}

// ---------------------------------------------------------------- ridges and hills

export function ridgePoints(b: RidgeBody): Vec[] {
  return b.points.map((p) => ({ x: p.x, y: p.y * b.heightScale }));
}

/** Skyline through the control points plus fractal detail. Sorted by x. */
export function ridgeSkyline(b: RidgeBody): Vec[] {
  const pts = ridgePoints(b);
  const segs = smoothSegments(pts, b.roundness);
  const step = Math.max(2.5, b.detail / 10);
  const out: Vec[] = [pts[0]];
  let prev = pts[0];
  for (const s of segs) {
    const n = Math.max(2, Math.ceil(Math.abs(s.p.x - prev.x) / step));
    out.push(...sampleCubic(prev, s.c1, s.c2, s.p, n));
    prev = s.p;
  }
  const amp = b.detail * 0.45 * b.roughness;
  if (amp <= 0) return out;
  return out.map((p) => ({
    x: p.x,
    y: p.y + amp * fbm(p.x / b.detail, b.seed),
  }));
}

export function ridgePath(b: RidgeBody): string {
  const sky = ridgeSkyline(b);
  const first = sky[0];
  const last = sky[sky.length - 1];
  return poly([{ x: first.x, y: b.depth }, ...sky, { x: last.x, y: b.depth }]);
}

/**
 * Shadow faces east of every control peak: a ragged spur down from the peak on one side and the
 * valley's crease on the other, which leans away from the peak as it falls (a straight drop from
 * the valley read as a cut once the volcano stopped covering it, as in the chat header).
 */
export function ridgeShadePaths(b: RidgeBody): string[] {
  if (b.shadeAmount <= 0) return [];
  const pts = ridgePoints(b);
  const sky = ridgeSkyline(b);
  const out: string[] = [];
  for (let i = 1; i < pts.length - 1; i++) {
    const peak = pts[i];
    if (!(peak.y < pts[i - 1].y && peak.y <= pts[i + 1].y)) continue;
    const valley = pts[i + 1];
    const face = sky.filter((p) => p.x >= peak.x && p.x <= valley.x);
    if (face.length < 2) continue;
    const top = face[0];
    const foot = lerp(peak.x, valley.x, 1 - b.shadeAmount);
    const spur: Vec[] = [];
    for (let k = 10; k >= 0; k--) {
      const s = k / 10;
      const y = lerp(top.y, b.depth, s);
      const wobble = b.detail * 0.35 * b.roughness * fbm(y / (b.detail * 0.6), b.seed + 7 + i);
      // Leans most near the crest, where the face is seen; the base is mostly under mist.
      spur.push({ x: lerp(top.x, foot, 1 - (1 - s) ** 2) + wobble * s, y });
    }
    const bottom = face[face.length - 1];
    const crease: Vec[] = [];
    for (let k = 1; k <= 10; k++) {
      const s = k / 10;
      const y = lerp(bottom.y, b.depth, s);
      const wobble = b.detail * 0.3 * b.roughness * fbm(y / (b.detail * 0.6), b.seed + 31 + i);
      const lean = (valley.x - peak.x) * 0.45 * (1 - (1 - s) ** 2);
      crease.push({ x: bottom.x + lean + wobble * s, y });
    }
    out.push(poly([...face, ...crease, ...spur]));
  }
  return out;
}

/** Short grass strokes scattered just below the skyline, as one path. */
export function ridgeGrass(b: RidgeBody): string {
  if (b.grass <= 0) return '';
  const sky = ridgeSkyline(b);
  const x0 = sky[0].x;
  const x1 = sky[sky.length - 1].x;
  const n = Math.round((b.grass * (x1 - x0)) / 100);
  const rand = rng(b.seed * 13 + 5);
  const parts: string[] = [];
  for (let i = 0; i < n; i++) {
    const x = lerp(x0, x1, rand());
    const y = yAt(sky, x) + 2 + Math.pow(rand(), 1.5) * b.depth * 0.9;
    const h = 3 + rand() * 5;
    parts.push(`M ${r2(x)} ${r2(y)} l ${r2((rand() - 0.5) * 3)} ${r2(-h)}`);
  }
  return parts.join(' ');
}

// ---------------------------------------------------------------- volcano

interface VolcanoFrame {
  leftBase: Vec;
  leftShoulder: Vec;
  rightShoulder: Vec;
  rightBase: Vec;
  summitY: number;
  leftC1: Vec;
  leftC2: Vec;
  rightC1: Vec;
  rightC2: Vec;
}

function volcanoFrame(b: VolcanoBody): VolcanoFrame {
  const half = b.baseWidth / 2;
  const sHalf = b.summitWidth / 2;
  const top = -b.height;
  const c = b.concavity;
  const leftShoulder = { x: b.summitOffset - sHalf, y: top + b.height * 0.1 };
  const rightShoulder = { x: b.summitOffset + sHalf, y: top + b.height * 0.1 };
  const leftBase = { x: -half, y: 0 };
  const rightBase = { x: half, y: 0 };
  const dl = leftShoulder.x - leftBase.x;
  const dr = rightBase.x - rightShoulder.x;
  const foot = -b.height * (0.03 + 0.1 * (1 - c));
  // Concave stratovolcano profile: flared base (first control low and inward), diagonal near the
  // summit so the shoulder rounds smoothly into the plateau.
  return {
    leftBase,
    leftShoulder,
    rightShoulder,
    rightBase,
    summitY: top,
    leftC1: { x: lerp(leftBase.x, leftShoulder.x, 0.2 + 0.4 * c), y: foot },
    leftC2: {
      x: leftShoulder.x - dl * (0.22 + 0.1 * c),
      y: leftShoulder.y + b.height * (0.28 + 0.1 * c),
    },
    rightC1: {
      x: rightShoulder.x + dr * (0.22 + 0.1 * c),
      y: rightShoulder.y + b.height * (0.28 + 0.1 * c),
    },
    rightC2: { x: lerp(rightShoulder.x, rightBase.x, 0.8 - 0.4 * c), y: foot },
  };
}

/** Smooth profile from left base to right base, then roughened (less on the snowy dome). */
export function volcanoProfile(b: VolcanoBody): Vec[] {
  const f = volcanoFrame(b);
  // The summit is one broad dome, tangent to both flanks so there is no corner at the shoulders.
  // Its crest stays where the old plateau was (summitY - 0.9% of height), so the crater, the vent,
  // the steam and the Pet keep their positions.
  const crest = f.summitY - b.height * SUMMIT_CREST;
  // With both controls at one height, the cubic's mid-point is 0.25 * end + 0.75 * control.
  const ctrlY = (crest - 0.25 * f.leftShoulder.y) / 0.75;
  const control = (shoulder: Vec, from: Vec): Vec => {
    const dx = shoulder.x - from.x;
    const dy = shoulder.y - from.y;
    const len = Math.hypot(dx, dy) || 1;
    const t = Math.min(
      (ctrlY - shoulder.y) / (dy / len),
      (b.summitWidth * 0.45 * len) / Math.abs(dx || 1),
    );
    return { x: shoulder.x + (dx / len) * t, y: shoulder.y + (dy / len) * t };
  };
  const pts: Vec[] = [f.leftBase];
  pts.push(...sampleCubic(f.leftBase, f.leftC1, f.leftC2, f.leftShoulder, 60));
  pts.push(
    ...sampleCubic(
      f.leftShoulder,
      control(f.leftShoulder, f.leftC2),
      control(f.rightShoulder, f.rightC1),
      f.rightShoulder,
      36,
    ),
  );
  pts.push(...sampleCubic(f.rightShoulder, f.rightC1, f.rightC2, f.rightBase, 60));
  return pts.map((p) => roughen(b, p));
}

/** Height of the dome's crest above the summit line, as a fraction of the volcano's height. */
const SUMMIT_CREST = 0.009;

/** Profile roughness: weaker on the snowy dome than on the lower slopes. */
function roughen(b: VolcanoBody, p: Vec): Vec {
  if (b.roughness <= 0) return p;
  const hf = Math.min(1, Math.max(0, -p.y / b.height));
  const amp = b.roughness * 9 * (1 - 0.75 * hf);
  return { x: p.x, y: Math.min(0, p.y + amp * fbm(p.x / 26, b.seed)) };
}

export function volcanoPath(b: VolcanoBody): string {
  const prof = volcanoProfile(b);
  const l = prof[0];
  const r = prof[prof.length - 1];
  return poly([
    { x: l.x - 80, y: b.depth },
    { x: l.x - 80, y: 6 },
    ...prof,
    { x: r.x + 80, y: 6 },
    { x: r.x + 80, y: b.depth },
  ]);
}

/** East-facing shadow face; drawn inside the silhouette clip, so it can overshoot. */
export function volcanoShadePath(b: VolcanoBody): string {
  const top = -b.height - 20;
  const x0 = b.summitOffset + b.summitWidth * 0.12;
  const footX = b.summitOffset + b.baseWidth * 0.2;
  const edge: Vec[] = [];
  for (let k = 0; k <= 24; k++) {
    const s = k / 24;
    const base = cubicAt(
      { x: x0, y: top },
      { x: x0 + b.summitWidth * 0.18, y: -b.height * 0.75 },
      { x: b.summitOffset + b.baseWidth * 0.15, y: -b.height * 0.3 },
      { x: footX, y: 0 },
      s,
    );
    edge.push({
      x: base.x + b.roughness * 10 * s * fbm(base.y / 30, b.seed + 3),
      y: base.y,
    });
  }
  return poly([
    { x: b.baseWidth, y: top },
    ...edge,
    { x: footX, y: b.depth },
    { x: b.baseWidth, y: b.depth },
  ]);
}

/**
 * Gradient axis (volcano-local) across the shadow terminator of volcanoShadePath: 0 just on the
 * lit side of the edge, 1 fully in shade. A slanted linear gradient softens the edge for free;
 * a blur filter would re-rasterize every frame.
 */
export function volcanoShadeAxis(b: VolcanoBody): {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
} {
  const top = -b.height - 20;
  const x0 = b.summitOffset + b.summitWidth * 0.12;
  const footX = b.summitOffset + b.baseWidth * 0.2;
  const dx = footX - x0;
  const dy = -top;
  const len = Math.hypot(dx, dy) || 1;
  // Unit normal pointing into the shade (right of the edge, which runs top-left to bottom-right).
  const nx = dy / len;
  const ny = -dx / len;
  const mx = (x0 + footX) / 2;
  const my = top / 2;
  // Start a little on the lit side: the real edge bows and wiggles around the straight chord.
  const back = 6 + b.roughness * 6;
  const width = b.baseWidth * 0.09;
  return {
    x1: mx - nx * back,
    y1: my - ny * back,
    x2: mx + nx * width,
    y2: my + ny * width,
  };
}

/**
 * Radial drainage: ravines fanning from below the summit to the base (dark), and the spur crests
 * between them (light). Each set is one path.
 */
export function volcanoErosion(b: VolcanoBody): {
  ravines: string;
  crests: string;
} {
  const n = Math.max(0, Math.round(b.gullies));
  const rand = rng(b.seed * 7 + 1);
  const ravines: string[] = [];
  const crests: string[] = [];
  for (let i = 0; i < n; i++) {
    const t = (i + 0.5) / n;
    const xTop = b.summitOffset + (t - 0.5) * b.summitWidth * 1.4 + (rand() - 0.5) * 8;
    const yTop = -b.height * (0.78 + rand() * 0.12);
    const xBot = (t - 0.5) * b.baseWidth * 0.86 + (rand() - 0.5) * 30;
    const yBot = -b.height * (0.03 + rand() * 0.09);
    const wBot = 2.5 + rand() * 3.5;
    const build = (offset: number, widthScale: number) => {
      const left: Vec[] = [];
      const right: Vec[] = [];
      for (let k = 0; k <= 12; k++) {
        const s = k / 12;
        const x =
          lerp(xTop, xBot, Math.pow(s, 1.12)) +
          5 * b.roughness * fbm(s * 4 + i * 3.1, b.seed + i) +
          offset * s;
        const y = lerp(yTop, yBot, s);
        const w = lerp(0.4, wBot, s) * widthScale;
        left.push({ x: x - w / 2, y });
        right.push({ x: x + w / 2, y });
      }
      return poly([...left, ...right.reverse()]);
    };
    ravines.push(build(0, 1));
    crests.push(build(-wBot * 1.6 - 3, 0.6));
  }
  return { ravines: ravines.join(' '), crests: crests.join(' ') };
}

/** Half-width point of the volcano at height y (negative up), on the left slope. */
function volcanoXAt(f: VolcanoFrame, y: number): number {
  let lo = 0;
  let hi = 1;
  for (let i = 0; i < 24; i++) {
    const mid = (lo + hi) / 2;
    const p = cubicAt(f.leftBase, f.leftC1, f.leftC2, f.leftShoulder, mid);
    if (p.y > y) lo = mid;
    else hi = mid;
  }
  return cubicAt(f.leftBase, f.leftC1, f.leftC2, f.leftShoulder, lo).x;
}

export interface SnowShape {
  field: string;
  /** Snow streaks in the gullies below the main ice line. */
  patches: string;
  /** Dark rock ribs poking through the glacier. */
  outcrops: string;
}

/** A thin slanted streak (snow or rock) running down the slope from (x, y), widest at the top. */
function streak(
  x: number,
  y: number,
  w: number,
  h: number,
  slant: number,
  rand: () => number,
): string {
  const left: Vec[] = [];
  const right: Vec[] = [];
  for (let k = 0; k <= 5; k++) {
    const t = k / 5;
    const half = (w / 2) * Math.pow(1 - t, 0.8) * (0.75 + rand() * 0.5) * Math.min(1, t * 6 + 0.3);
    const cx = x + slant * h * t + (rand() - 0.5) * w * 0.4;
    left.push({ x: cx - half, y: y + h * t });
    right.push({ x: cx + half, y: y + h * t });
  }
  return poly([...left, ...right.reverse()]);
}

/**
 * Glacier field with an irregular lower edge and tongues down the gullies, rock ribs inside it,
 * and loose snow streaks below. Everything is clipped to the volcano silhouette by the renderer.
 */
export function snowPaths(v: VolcanoBody, s: SnowCapBody): SnowShape {
  const f = volcanoFrame(v);
  const lineY = -v.height * (1 - s.coverage);
  const leftEdge = volcanoXAt(f, Math.max(lineY, f.leftShoulder.y));
  const rightEdge = 2 * v.summitOffset - leftEdge;
  const span = rightEdge - leftEdge;
  const rand = rng(s.seed);
  // Streaks, tongues and ribs lean outward like the gullies they sit in.
  const slantAt = (x: number) => ((x - v.summitOffset) / (v.baseWidth / 2)) * 0.9;
  const n = Math.max(0, Math.round(s.tongues));
  // Snow runs down the gullies (tongues) and melts off the ribs between them (negative length).
  // Heavy-tailed lengths: a few tongues reach far down, most stay short, so the margin never
  // reads as a row of evenly spaced drips.
  const tongues = Array.from({ length: n }, (_, k) => {
    const x = leftEdge + (span * (k + 0.5)) / n + (rand() - 0.5) * (span / Math.max(1, n)) * 0.8;
    const rib = rand() < 0.3;
    const len = rib
      ? -s.tongueLength * (0.15 + 0.3 * rand())
      : s.tongueLength * (0.2 + 1.6 * Math.pow(rand(), 2));
    const half = (span / Math.max(1, n)) * (0.12 + rand() * 0.25);
    // The tip follows the fall line instead of hanging straight down.
    const tip = x + Math.max(-0.8, Math.min(0.8, (slantAt(x) * Math.abs(len)) / half)) * half;
    return { x, len, half, tip };
  });
  const tongueDepth = (t: (typeof tongues)[number], x: number) => {
    const a = t.x - t.half;
    const b = t.x + t.half;
    if (x <= a || x >= b) return 0;
    const f = x < t.tip ? (x - a) / (t.tip - a) : (b - x) / (b - t.tip);
    return t.len * Math.pow(f, 1.3);
  };
  const wide = v.baseWidth;
  const edge: Vec[] = [];
  for (let x = wide / 2; x >= -wide / 2; x -= 2) {
    let y =
      lineY +
      30 * s.roughness * fbm(x / 120, s.seed + 1) +
      9 * s.roughness * fbm(x / 24, s.seed + 2) +
      3 * s.roughness * fbm(x / 6, s.seed + 4);
    for (const t of tongues) {
      const d = tongueDepth(t, x);
      if (d !== 0) y += d * (0.8 + 0.4 * fbm(x / 7, s.seed + 3));
    }
    edge.push({ x, y });
  }
  const field = poly([
    { x: wide / 2, y: f.summitY - 60 },
    ...edge,
    { x: -wide / 2, y: f.summitY - 60 },
  ]);

  // Snow left in the gullies just below the margin: denser and longer near the line.
  const patches: string[] = [];
  for (let i = 0; i < Math.round(s.patches); i++) {
    const x = lerp(leftEdge - span * 0.35, rightEdge + span * 0.35, rand());
    const y = lineY + 8 + Math.pow(rand(), 2.2) * v.height * 0.35;
    patches.push(streak(x, y, 1.5 + rand() * 2.5, 8 + rand() * 24, slantAt(x), rand));
  }
  // Rock ribs: most rise out of the snow margin (negative height, widest at the bottom), a few
  // break through near the summit.
  const outcrops: string[] = [];
  for (let i = 0; i < Math.round(s.patches / 3); i++) {
    const x = lerp(leftEdge + span * 0.08, rightEdge - span * 0.08, rand());
    if (rand() < 0.7) {
      outcrops.push(streak(x, lineY + 12, 2 + rand() * 3.5, -(14 + rand() * 30), slantAt(x), rand));
    } else {
      const y = lerp(f.summitY + v.height * 0.1, lineY, 0.1 + rand() * 0.4);
      outcrops.push(streak(x, y, 1.5 + rand() * 2.5, 6 + rand() * 14, slantAt(x), rand));
    }
  }
  return { field, patches: patches.join(' '), outcrops: outcrops.join(' ') };
}

export interface CraterShape {
  /** The dark opening. */
  mouth: string;
  /** Far inner wall, the crescent just inside the back edge of the opening. */
  wall: string;
  /** Near edge of the opening. */
  lip: string;
}

/**
 * The crater is an opening in the summit dome, seen slightly from above. Its back edge stays a
 * few units below the skyline, so snow frames it on every side and nothing sticks out above the
 * silhouette.
 */
function craterMouth(v: VolcanoBody, c: CraterBody) {
  const crest = roughen(v, { x: v.summitOffset, y: -v.height * (1 + SUMMIT_CREST) }).y;
  const rx = (v.summitWidth * c.width) / 2;
  const ry = Math.max(1.5, c.depth);
  return { cx: v.summitOffset, cy: crest + ry + 3 + c.depth * 0.25, rx, ry };
}

/** Vent position in volcano-local coordinates: the centre of the crater's opening. */
export function craterVent(v: VolcanoBody, c: CraterBody): Vec {
  const m = craterMouth(v, c);
  return { x: m.cx, y: m.cy };
}

export function craterPaths(v: VolcanoBody, c: CraterBody): CraterShape {
  const { cx, cy, rx, ry } = craterMouth(v, c);
  const l = `${r2(cx - rx)} ${r2(cy)}`;
  const r = `${r2(cx + rx)} ${r2(cy)}`;
  const arc = (h: number, sweep: 0 | 1, to: string) => `A ${r2(rx)} ${r2(h)} 0 0 ${sweep} ${to}`;
  return {
    mouth: `M ${l} ${arc(ry, 1, r)} ${arc(ry, 1, l)} Z`,
    wall: `M ${l} ${arc(ry, 1, r)} ${arc(ry * 0.45, 0, l)} Z`,
    lip: `M ${l} ${arc(ry, 0, r)}`,
  };
}

// ---------------------------------------------------------------- steam

export interface Puff {
  x: number;
  y: number;
  r: number;
  opacity: number;
}

/** Plume tip in steam-local coordinates (origin = vent). */
export function steamTip(b: SteamBody): Vec {
  return {
    x: Math.sin(deg(b.direction)) * b.height,
    y: -Math.cos(deg(b.direction)) * b.height,
  };
}

/**
 * Soft puffs flowing from the vent to the tip. `phase` (0..1) slides every puff one slot along
 * the plume; size and opacity depend only on position, so phase 1 looks exactly like phase 0 and
 * the loop is seamless.
 */
export function steamPuffs(b: SteamBody): Puff[] {
  const tip = steamTip(b);
  const nx = -tip.y / b.height;
  const ny = tip.x / b.height;
  const ctrl = {
    x: tip.x * 0.5 + nx * b.curvature * b.height * 0.35,
    y: tip.y * 0.5 + ny * b.curvature * b.height * 0.35,
  };
  const filaments = Math.max(1, Math.round(b.filaments));
  const perFilament = 12;
  const phase = ((b.phase % 1) + 1) % 1;
  const puffs: Puff[] = [];
  for (let f = 0; f < filaments; f++) {
    const lateral = filaments === 1 ? 0 : (f / (filaments - 1) - 0.5) * 2;
    for (let i = 0; i < perFilament; i++) {
      const t = (i + phase) / perFilament;
      const u = 1 - t;
      const cx = 2 * u * t * ctrl.x + t * t * tip.x;
      const cy = 2 * u * t * ctrl.y + t * t * tip.y;
      const wobble =
        b.oscillation * b.width * 0.35 * Math.sin(Math.PI * 2 * (t * 1.4 + f * 0.37)) * t;
      const side = lateral * b.spread * b.width * 0.45 * t + wobble;
      const r =
        lerp(b.width * 0.13, b.width * 0.55, Math.pow(t, 0.75)) *
        b.volume *
        (filaments > 1 ? 0.82 : 1) *
        (1 + 0.1 * Math.sin(Math.PI * 2 * (t * 2.3 + f * 0.5)));
      const opacity = smoothstep(0, 0.1, t) * (1 - smoothstep(0.45, 1, t)) * 0.9;
      puffs.push({ x: cx + nx * side, y: cy + ny * side, r, opacity });
    }
  }
  // Oldest (widest, highest) puffs first, so fresh steam near the vent reads on top.
  return puffs.sort((a, b) => b.r - a.r);
}

// ---------------------------------------------------------------- clouds

/** Cumulus puffs: a base row plus smaller cauliflower puffs on top. Local origin = base center. */
export function cloudPuffs(b: CloudBody): { cx: number; cy: number; r: number }[] {
  const rand = rng(b.seed);
  const n = Math.max(2, Math.round(b.puffs));
  const base = [];
  const usable = b.width - b.height * 0.6;
  for (let i = 0; i < n; i++) {
    const u = (i + 0.5) / n + ((rand() - 0.5) * 0.5) / n;
    const bell = Math.sin(Math.PI * Math.min(1, Math.max(0, u)));
    const r = b.height * (0.2 + 0.3 * bell) * (0.85 + rand() * 0.3);
    const lift = Math.max(0, b.height - 2 * r) * bell * (0.55 + rand() * 0.45);
    base.push({ cx: (u - 0.5) * usable, cy: -r - lift * 0.6, r });
  }
  const tops = [];
  for (let j = 0; j < Math.round(n * 0.7); j++) {
    const p = base[Math.floor(rand() * base.length)];
    tops.push({
      cx: p.cx + (rand() - 0.5) * p.r,
      cy: p.cy - p.r * (0.35 + rand() * 0.3),
      r: p.r * (0.45 + rand() * 0.25),
    });
  }
  return [...base, ...tops];
}

// ---------------------------------------------------------------- vegetation

export interface FrailejonShape {
  trunk: string;
  trunkDark: string;
  trunkLight: string;
  deadLeaves: string;
  backLeaves: string;
  frontLeaves: string;
  stalks: string;
  heads: { cx: number; cy: number; r: number }[];
  crown: Vec;
}

function leafPath(
  origin: Vec,
  angleDeg: number,
  length: number,
  width: number,
  bend: number,
): string {
  const a = deg(angleDeg);
  const dx = Math.cos(a);
  const dy = Math.sin(a);
  const px = -dy;
  const py = dx;
  const at = (along: number, across: number) => ({
    x: origin.x + dx * along + px * across,
    y: origin.y + dy * along + py * across + bend * (along / length) ** 2,
  });
  return `M ${pt(origin)} C ${pt(at(length * 0.25, width))} ${pt(at(length * 0.75, width * 0.7))} ${pt(at(length, 0))} C ${pt(at(length * 0.75, -width * 0.7))} ${pt(at(length * 0.25, -width))} ${pt(origin)} Z`;
}

/**
 * Frailejón (Espeletia): a column wrapped in dry marcescent leaves, topped by a dense rosette of
 * narrow silver-green leaves and a few yellow flower stalks. Local origin = trunk base.
 */
export function frailejonShape(b: FrailejonBody): FrailejonShape {
  const rand = rng(b.seed);
  const th = b.trunkHeight;
  const tw = b.trunkWidth;
  const crown = {
    x: Math.sin(deg(b.tilt)) * th,
    y: -Math.cos(deg(b.tilt)) * th,
  };
  const centerAt = (s: number) => ({ x: crown.x * s * s, y: crown.y * s });
  const widthAt = (s: number) => tw * lerp(0.92, 1.08, s) * (1 + 0.05 * fbm(s * 6, b.seed));
  const left: Vec[] = [];
  const right: Vec[] = [];
  for (let k = 0; k <= 10; k++) {
    const s = k / 10;
    const c = centerAt(s);
    const w = widthAt(s) / 2;
    left.push({ x: c.x - w, y: c.y });
    right.push({ x: c.x + w, y: c.y });
  }
  const trunk = poly([...left, ...right.reverse()]);

  // Dry leaves hanging on the trunk: short downward strokes, darker on the shaded right side.
  const dark: string[] = [];
  const light: string[] = [];
  const rows = Math.max(3, Math.round(th / 3.2));
  for (let r = 0; r < rows; r++) {
    const s = (r + 0.5) / rows;
    const c = centerAt(s);
    const w = widthAt(s) / 2;
    const count = Math.max(2, Math.round(w / 1.8));
    for (let k = 0; k < count; k++) {
      const u = (k + rand() * 0.6) / count;
      const x = c.x - w + 2 * w * u;
      const stroke = `M ${r2(x)} ${r2(c.y - 1)} l ${r2((rand() - 0.5) * 1.6)} ${r2(3 + rand() * 3)}`;
      if (u > 0.55 || rand() < 0.25) dark.push(stroke);
      else light.push(stroke);
    }
  }

  const n = Math.max(3, Math.round(b.leafCount));
  const back: string[] = [];
  const front: string[] = [];
  const dead: string[] = [];
  const ring = b.rosetteDiameter * 0.12;
  for (let i = 0; i < n; i++) {
    const t = (i + rand() * 0.8) / n;
    const angle = lerp(-178, -2, t) + b.tilt * 0.5;
    const o = {
      x: crown.x + Math.cos(deg(angle)) * ring,
      y: crown.y + Math.sin(deg(angle)) * ring * 0.4,
    };
    const len = b.leafLength * (0.8 + rand() * 0.35) * (0.75 + 0.25 * Math.sin(Math.PI * t));
    back.push(leafPath(o, angle, len, len * 0.11, len * 0.12));
  }
  const m = Math.max(2, Math.round(n * 0.55));
  for (let i = 0; i < m; i++) {
    const t = (i + rand() * 0.8) / m;
    const angle = lerp(-158, -22, t) + b.tilt * 0.5;
    const len = b.leafLength * 0.7 * (0.8 + rand() * 0.3);
    front.push(leafPath({ x: crown.x, y: crown.y + 1.5 }, angle, len, len * 0.12, len * 0.08));
  }
  for (const angle of [-200, -190, 10, 20]) {
    const len = b.leafLength * 0.7;
    dead.push(
      leafPath(
        { x: crown.x, y: crown.y + 2 },
        angle + (rand() - 0.5) * 8,
        len,
        len * 0.1,
        len * 0.35,
      ),
    );
  }

  const stalks: string[] = [];
  const heads: { cx: number; cy: number; r: number }[] = [];
  for (let i = 0; i < Math.round(b.flowers); i++) {
    const angle = -90 + (rand() - 0.5) * 70 + b.tilt * 0.5;
    const len = b.leafLength * (1.3 + rand() * 0.5);
    const end = {
      x: crown.x + Math.cos(deg(angle)) * len,
      y: crown.y + Math.sin(deg(angle)) * len,
    };
    stalks.push(
      `M ${pt(crown)} Q ${r2(lerp(crown.x, end.x, 0.2))} ${r2(lerp(crown.y, end.y, 0.7))} ${pt(end)}`,
    );
    const hr = Math.max(1.4, b.leafLength * 0.075);
    heads.push({ cx: end.x, cy: end.y, r: hr });
    heads.push({ cx: end.x - hr * 1.8, cy: end.y + hr * 1.6, r: hr * 0.8 });
    heads.push({ cx: end.x + hr * 1.7, cy: end.y + hr * 1.9, r: hr * 0.75 });
  }
  return {
    trunk,
    trunkDark: dark.join(' '),
    trunkLight: light.join(' '),
    deadLeaves: dead.join(' '),
    backLeaves: back.join(' '),
    frontLeaves: front.join(' '),
    stalks: stalks.join(' '),
    heads,
    crown,
  };
}

export function flowerPetals(b: FlowerBody): string {
  const n = Math.max(3, Math.round(b.petals));
  const center = { x: 0, y: -b.stemHeight };
  return Array.from({ length: n }, (_, i) =>
    leafPath(center, (360 / n) * i - 90, b.petalSize, b.petalSize * 0.42, 0),
  ).join(' ');
}

export function flowerStem(b: FlowerBody): string {
  return `M 0 0 Q ${r2(b.stemHeight * 0.18)} ${r2(-b.stemHeight * 0.5)} 0 ${r2(-b.stemHeight)}`;
}

/** Faceted boulder: outline, shadowed east facet, lit west facet. Local origin = bottom center. */
export function rockPaths(b: RockBody): {
  body: string;
  shade: string;
  light: string;
} {
  const rand = rng(b.seed);
  const w = b.width / 2;
  const top: Vec[] = [];
  for (let k = 0; k <= 7; k++) {
    const a = Math.PI + (k / 7) * Math.PI;
    top.push({
      x: Math.cos(a) * w * (0.85 + rand() * 0.25),
      y: Math.min(0, Math.sin(a) * b.height * (0.75 + rand() * 0.35)),
    });
  }
  top[0].y = 0;
  top[7].y = 0;
  const ridge = { x: top[4].x * 0.6, y: top[4].y * 0.55 };
  return {
    body: poly(top),
    shade: poly([top[4], top[5], top[6], top[7], { x: ridge.x + w * 0.1, y: 0 }, ridge]),
    light: poly([top[1], top[2], top[3], ridge, { x: top[1].x * 0.5, y: top[1].y * 0.6 }]),
  };
}

/** Pajonal tussock blades split into light and dark strokes. Local origin = base center. */
export function tuftBlades(b: TuftBody): { light: string; dark: string } {
  const n = Math.max(2, Math.round(b.blades));
  const rand = rng(b.seed);
  const light: string[] = [];
  const dark: string[] = [];
  for (let i = 0; i < n; i++) {
    const t = n === 1 ? 0.5 : i / (n - 1);
    const x0 = (t - 0.5) * b.width * 0.35 + (rand() - 0.5) * 2;
    const lean = (t - 0.5) * b.width * (0.9 + rand() * 0.5);
    const h = b.height * (0.55 + 0.45 * Math.sin(Math.PI * t)) * (0.8 + rand() * 0.35);
    const d = `M ${r2(x0)} 0 Q ${r2(x0 + lean * 0.25)} ${r2(-h * 0.6)} ${r2(x0 + lean)} ${r2(-h + Math.abs(lean) * 0.25)}`;
    if (rand() < 0.4) dark.push(d);
    else light.push(d);
  }
  return { light: light.join(' '), dark: dark.join(' ') };
}

// ---------------------------------------------------------------- mist

export function mistPuffs(b: MistBody): { cx: number; cy: number; rx: number; ry: number }[] {
  const n = Math.max(1, Math.round(b.density));
  const rand = rng(b.seed);
  return Array.from({ length: n }, (_, i) => {
    const slot = b.width / n;
    return {
      cx: -b.width / 2 + slot * (i + 0.5) + (rand() - 0.5) * slot * 0.6,
      cy: (rand() - 0.5) * b.height * 0.35,
      rx: slot * (1 + rand() * 0.8),
      ry: b.height * (0.3 + rand() * 0.22),
    };
  });
}
