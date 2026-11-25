// The web Pet on a 2D canvas: PetVaporFigure (the SVG reference) call for call, from the same
// PetFrame. The SVG figure re-rendered about 50 React elements per frame and was what held the web
// chat under 30 fps on a throttled run; painting a canvas skips React and the DOM entirely.
import { parseTransform } from '@/ui/skia/svgTransform';

import type { PetConfig, PetFrame, PetStroke } from './petCore';

const WHITE = '#ffffff';

const rgbCache = new Map<string, [number, number, number]>();
function rgb(hex: string): [number, number, number] {
  let c = rgbCache.get(hex);
  if (!c) {
    const h = hex.replace('#', '');
    const full = h.length === 3 ? h.replace(/(.)/g, '$1$1') : h.slice(0, 6);
    const n = parseInt(full, 16);
    if (Number.isNaN(n) || full.length !== 6) throw new Error(`unsupported color ${hex}`);
    c = [(n >> 16) & 255, (n >> 8) & 255, n & 255];
    rgbCache.set(hex, c);
  }
  return c;
}
const color = (hex: string, alpha = 1) => {
  const [r, g, b] = rgb(hex);
  return `rgb(${r} ${g} ${b} / ${alpha})`;
};

const paths = new Map<string, Path2D>();
/** Geometry strings repeat across frames (eyes, mouth); a moving body makes new ones. */
function path(d: string): Path2D {
  let p = paths.get(d);
  if (!p) {
    if (paths.size >= 256) paths.clear();
    p = new Path2D(d);
    paths.set(d, p);
  }
  return p;
}

interface Box {
  x: number;
  y: number;
  width: number;
  height: number;
}

/** Extremes of one cubic coordinate on t in [0, 1]. */
function cubicRange(p0: number, p1: number, p2: number, p3: number, out: number[]) {
  out.push(p0, p3);
  const a = -p0 + 3 * p1 - 3 * p2 + p3;
  const b = 2 * (p0 - 2 * p1 + p2);
  const c = p1 - p0;
  const at = (t: number) => {
    if (t > 0 && t < 1) {
      const u = 1 - t;
      out.push(u * u * u * p0 + 3 * u * u * t * p1 + 3 * u * t * t * p2 + t * t * t * p3);
    }
  };
  if (Math.abs(a) < 1e-12) {
    if (Math.abs(b) > 1e-12) at(-c / b);
    return;
  }
  const disc = b * b - 4 * a * c;
  if (disc < 0) return;
  const s = Math.sqrt(disc);
  at((-b + s) / (2 * a));
  at((-b - s) / (2 * a));
}

/**
 * The tight box of an absolute M/L/C/Z path, as SVG's objectBoundingBox measures it (Skia's
 * getBounds uses control points, which is why the native drawer differs by a hair). The body and
 * volume paths petFrame makes use only these commands.
 */
export function pathBox(d: string): Box {
  const tokens = d.match(/-?\d*\.?\d+(?:e[-+]?\d+)?|[A-Za-z]/g) ?? [];
  const xs: number[] = [];
  const ys: number[] = [];
  let i = 0;
  let cmd = '';
  let x = 0;
  let y = 0;
  const num = () => Number(tokens[i++]);
  while (i < tokens.length) {
    if (/^[A-Za-z]$/.test(tokens[i])) cmd = tokens[i++];
    if (cmd === 'M' || cmd === 'L') {
      x = num();
      y = num();
      xs.push(x);
      ys.push(y);
    } else if (cmd === 'C') {
      const x1 = num();
      const y1 = num();
      const x2 = num();
      const y2 = num();
      const x3 = num();
      const y3 = num();
      cubicRange(x, x1, x2, x3, xs);
      cubicRange(y, y1, y2, y3, ys);
      x = x3;
      y = y3;
    } else if (cmd === 'Z' || cmd === 'z') {
      // No coordinates; the next token is a command.
    } else {
      throw new Error(`pathBox: unsupported command ${cmd} in ${d.slice(0, 40)}`);
    }
  }
  const minX = Math.min(...xs);
  const minY = Math.min(...ys);
  return { x: minX, y: minY, width: Math.max(...xs) - minX, height: Math.max(...ys) - minY };
}

const applyTransform = (ctx: CanvasRenderingContext2D, svg: string) => {
  const m = parseTransform(svg);
  ctx.transform(m[0], m[1], m[2], m[3], m[4], m[5]);
};

function drawStroke(ctx: CanvasRenderingContext2D, s: PetStroke) {
  ctx.save();
  applyTransform(ctx, s.transform);
  const p = path(s.d);
  const c = color(s.color);
  if (s.filled) {
    ctx.fillStyle = c;
    ctx.fill(p);
  }
  ctx.strokeStyle = c;
  ctx.lineWidth = s.width;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.stroke(p);
  ctx.restore();
}

/** Draws one frame in Pet units; the caller sets the viewBox transform and clears the canvas. */
export function drawPetCanvas2d(
  ctx: CanvasRenderingContext2D,
  config: PetConfig,
  f: PetFrame,
  fillHex: string,
  shadeHex: string,
) {
  const b = config.body;
  const headR = (Math.max(b.width * b.scaleX, b.height * b.scaleY) / 2) * 1.25;
  const turn = 1 - 2 * f.turn;
  // The puffs' halo gradients on the unit circle; each puff scales the canvas onto it.
  const light = ctx.createRadialGradient(0, 0, 0, 0, 0, 1);
  light.addColorStop(0, color(fillHex, 0.8));
  light.addColorStop(0.5, color(fillHex, 0.45));
  light.addColorStop(1, color(fillHex, 0));
  const shadeHalo = ctx.createRadialGradient(0, 0, 0, 0, 0, 1);
  shadeHalo.addColorStop(0, color(shadeHex, 0.4));
  shadeHalo.addColorStop(1, color(shadeHex, 0));
  const puff = (x: number, y: number, r: number, opacity: number) => {
    ctx.save();
    ctx.globalAlpha = opacity;
    ctx.translate(x, y);
    ctx.scale(r, r);
    ctx.beginPath();
    ctx.arc(0, 0, 1, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  };

  ctx.save();
  ctx.translate(f.shiftX, f.float);
  ctx.save();
  applyTransform(ctx, f.bodyTransform);
  // Halo behind the body, light then shade offset down-right.
  ctx.fillStyle = light;
  for (const p of f.vapor) puff(p.x, p.y, p.r, p.opacity);
  ctx.fillStyle = shadeHalo;
  for (const p of f.vapor) puff(p.x + p.r * 0.2 * turn, p.y + p.r * 0.25, p.r, p.opacity);

  const body = path(f.body);
  const box = pathBox(f.body);
  const core = ctx.createLinearGradient(box.x, box.y, box.x, box.y + box.height);
  core.addColorStop(0, color(fillHex, 1));
  core.addColorStop(0.66, color(fillHex, 0.97));
  core.addColorStop(1, color(fillHex, 0));
  ctx.fillStyle = core;
  ctx.fill(body);
  const cx = f.headX - 10 * turn;
  const cy = b.y - 14;
  const form = ctx.createRadialGradient(cx, cy, 0, cx, cy, headR);
  form.addColorStop(0, color(shadeHex, 0));
  form.addColorStop(0.6, color(shadeHex, 0));
  form.addColorStop(0.86, color(shadeHex, 0.42));
  form.addColorStop(1, color(shadeHex, 0));
  ctx.fillStyle = form;
  ctx.fill(body);

  // Highlight: SVG's default radial gradient over the volume path's box, an ellipse filling it.
  const v = pathBox(f.volume);
  const w = Math.max(v.width, 1e-3);
  const k = Math.max(v.height, 1e-3) / w;
  const vx = v.x + v.width / 2;
  const vy = v.y + v.height / 2;
  const volume = new Path2D();
  // The path in the ellipse's space (y squashed by 1/k about the center), drawn with y scaled by k.
  volume.addPath(path(f.volume), new DOMMatrix([1, 0, 0, 1 / k, 0, vy - vy / k]));
  ctx.save();
  ctx.globalAlpha = f.volumeOpacity;
  ctx.translate(0, vy);
  ctx.scale(1, k);
  ctx.translate(0, -vy);
  const glow = ctx.createRadialGradient(vx, vy, 0, vx, vy, w / 2);
  glow.addColorStop(0, color(WHITE, 0.85));
  glow.addColorStop(1, color(WHITE, 0));
  ctx.fillStyle = glow;
  ctx.fill(volume);
  ctx.restore();
  ctx.restore();

  ctx.save();
  applyTransform(ctx, f.features);
  ctx.save();
  applyTransform(ctx, f.eyes);
  drawStroke(ctx, f.leftEye);
  drawStroke(ctx, f.rightEye);
  ctx.restore();
  drawStroke(ctx, f.mouth);
  ctx.restore();
  ctx.restore();
}
