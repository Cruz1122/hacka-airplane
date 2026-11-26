// Native renderer for a SceneDoc on Skia (GPU). Same geometry, palette and transforms as the SVG
// renderer in NevadoScene.tsx, which stays the reference (Lab, web, export); this file mirrors its
// ObjectBody drawing call for call. Why it exists: react-native-svg on Android redraws a layer into a
// CPU bitmap on every change (measured on a Galaxy A24: ~65 ms per moving layer, 32 ms for the Pet
// alone), so idle motions and camera moves could not run smoothly.
//
// Every object body is recorded once into an SkPicture (cached by body, palette and host); a frame
// only replays those pictures under new matrices, so a camera move or an idle motion costs no path
// building, no gradient setup and no rasterization on the CPU.
import {
  ClipOp,
  FilterMode,
  MipmapMode,
  PaintStyle,
  Skia,
  StrokeCap,
  StrokeJoin,
  TileMode,
  type SkCanvas,
  type SkColor,
  type SkPaint,
  type SkPath,
  type SkPicture,
  type SkShader,
} from '@shopify/react-native-skia';

import { craterOf, resolveColor, ventOf, volcanoOf } from '../scene/doc';
import {
  affineValues,
  cloudPuffs,
  craterPaths,
  flowerPetals,
  flowerStem,
  frailejonShape,
  lupineShape,
  mistPuffs,
  parallaxAffine,
  ridgeGrass,
  ridgePath,
  ridgeShadePaths,
  rockPaths,
  sceneViewBox,
  snowPaths,
  steamPuffs,
  transformValues,
  tuftBlades,
  volcanoErosion,
  volcanoPath,
  volcanoShadeAxis,
  volcanoShadePath,
} from '../scene/geometry';
import type {
  Body,
  Color,
  CraterBody,
  SceneDoc,
  SceneObject,
  Transform,
  VolcanoBody,
} from '../scene/types';
import { skColor, svgPath, toSkMatrix } from '@/ui/skia/primitives';
import { multiply, type Mat } from '@/ui/skia/svgTransform';

// ---------------------------------------------------------------- primitives

function concat(canvas: SkCanvas, m: Mat) {
  canvas.concat(toSkMatrix(m));
}

interface Stop {
  offset: number;
  color: string;
  opacity?: number;
}

const colorsOf = (stops: Stop[]) => stops.map((s) => skColor(s.color, s.opacity ?? 1));
const positionsOf = (stops: Stop[]) => stops.map((s) => s.offset);

function linear(x1: number, y1: number, x2: number, y2: number, stops: Stop[]): SkShader {
  return Skia.Shader.MakeLinearGradient(
    Skia.Point(x1, y1),
    Skia.Point(x2, y2),
    colorsOf(stops),
    positionsOf(stops),
    TileMode.Clamp,
  );
}

/** SVG's default radial gradient (objectBoundingBox, cx/cy/r as fractions) over a w x h box. */
function radialBox(
  x: number,
  y: number,
  w: number,
  h: number,
  stops: Stop[],
  cx = 0.5,
  cy = 0.5,
  r = 0.5,
): SkShader {
  const center = Skia.Point(x + cx * w, y + cy * h);
  // The box maps the unit circle to an ellipse; draw a circle of radius r*w, squashed vertically.
  const local =
    w === h
      ? undefined
      : Skia.Matrix()
          .translate(center.x, center.y)
          .scale(1, h / w)
          .translate(-center.x, -center.y);
  return Skia.Shader.MakeRadialGradient(
    center,
    r * w,
    colorsOf(stops),
    positionsOf(stops),
    TileMode.Clamp,
    local,
  );
}

function radial(cx: number, cy: number, r: number, stops: Stop[]): SkShader {
  return Skia.Shader.MakeRadialGradient(
    Skia.Point(cx, cy),
    r,
    colorsOf(stops),
    positionsOf(stops),
    TileMode.Clamp,
  );
}

function fill(color: SkColor | SkShader, opacity = 1): SkPaint {
  const p = Skia.Paint();
  p.setAntiAlias(true);
  if (color instanceof Float32Array) p.setColor(color as SkColor);
  else p.setShader(color as SkShader);
  if (opacity !== 1) p.setAlphaf(opacity);
  return p;
}

function stroke(color: SkColor, width: number, opacity = 1, round = true): SkPaint {
  const p = fill(color, opacity);
  p.setStyle(PaintStyle.Stroke);
  p.setStrokeWidth(width);
  if (round) {
    p.setStrokeCap(StrokeCap.Round);
    p.setStrokeJoin(StrokeJoin.Round);
  }
  return p;
}

/**
 * Box of a path for SVG's objectBoundingBox gradients. react-native-svg on Android uses the control
 * points' bounds (Path.computeBounds), not the tight ones; matching it keeps the same gradients.
 */
function boxOf(path: SkPath) {
  const b = path.getBounds();
  return { x: b.x, y: b.y, w: Math.max(b.width, 1e-3), h: Math.max(b.height, 1e-3) };
}

/** `linear` with x1=0 y1=0 x2=0 y2=1 over a path's box: top to bottom. */
function verticalBox(path: SkPath, stops: Stop[]): SkShader {
  const b = boxOf(path);
  return linear(b.x, b.y, b.x, b.y + b.h, stops);
}

function clipped(canvas: SkCanvas, clip: SkPath, draw: () => void) {
  canvas.save();
  canvas.clipPath(clip, ClipOp.Intersect, true);
  draw();
  canvas.restore();
}

// ---------------------------------------------------------------- bodies

interface BodyCtx {
  palette: Record<string, string>;
  stroke: Color;
  strokeWidth: number;
  host: VolcanoBody | null;
  crater: CraterBody | null;
}

/** Draws one body in its own coordinates, like NevadoScene's ObjectBody. */
function drawBody(canvas: SkCanvas, b: Body, ctx: BodyCtx) {
  const c = (color: Color) => resolveColor(ctx.palette, color);
  const outline = (path: SkPath) => {
    if (ctx.strokeWidth > 0)
      canvas.drawPath(path, stroke(skColor(c(ctx.stroke)), ctx.strokeWidth, 1, false));
  };
  const { host } = ctx;
  switch (b.kind) {
    case 'sky': {
      const shader = linear(0, 0, 0, b.horizon, [
        { offset: 0, color: c(b.top) },
        { offset: b.middleStop, color: c(b.middle) },
        { offset: 1, color: c(b.bottom) },
      ]);
      canvas.drawRect(Skia.XYWHRect(-1400, -1400, 3200, 3600), fill(shader));
      return;
    }
    case 'sun': {
      const halo = c(b.halo);
      canvas.drawCircle(
        0,
        0,
        b.haloRadius,
        fill(
          radial(0, 0, b.haloRadius, [
            { offset: 0, color: halo, opacity: b.haloStrength },
            { offset: 0.25, color: halo, opacity: b.haloStrength * 0.45 },
            { offset: 1, color: halo, opacity: 0 },
          ]),
        ),
      );
      canvas.drawCircle(0, 0, b.radius, fill(skColor(c(b.core))));
      if (ctx.strokeWidth > 0)
        canvas.drawCircle(0, 0, b.radius, stroke(skColor(c(ctx.stroke)), ctx.strokeWidth, 1, false));
      return;
    }
    case 'cloud': {
      const puffs = cloudPuffs(b);
      const base = (1 - b.flatness) * b.height * 0.6;
      const fillC = c(b.fill);
      const shadeC = c(b.shade);
      canvas.save();
      canvas.clipRect(
        Skia.XYWHRect(-b.width, -b.height * 3, b.width * 2, b.height * 3 + base),
        ClipOp.Intersect,
        true,
      );
      for (const p of puffs) {
        const cx = p.cx + p.r * 0.1;
        const cy = p.cy + p.r * 0.3;
        canvas.drawCircle(
          cx,
          cy,
          p.r,
          fill(
            radial(cx, cy, p.r, [
              { offset: 0, color: shadeC, opacity: 0.9 },
              { offset: 0.65, color: shadeC, opacity: 0.6 },
              { offset: 1, color: shadeC, opacity: 0 },
            ]),
          ),
        );
      }
      for (const p of puffs) {
        const r = p.r * 1.02;
        const cy = p.cy - p.r * 0.05;
        // cy="45%" of the circle's box: 0.1 r above its center.
        canvas.drawCircle(
          p.cx,
          cy,
          r,
          fill(
            radial(p.cx, cy - 0.1 * r, r, [
              { offset: 0, color: fillC, opacity: 1 },
              { offset: 0.7, color: fillC, opacity: 0.9 },
              { offset: 1, color: fillC, opacity: 0 },
            ]),
          ),
        );
      }
      canvas.restore();
      return;
    }
    case 'ridge': {
      const body = svgPath(ridgePath(b));
      canvas.drawPath(
        body,
        fill(
          verticalBox(body, [
            { offset: 0, color: c(b.top) },
            { offset: 1, color: c(b.bottom) },
          ]),
        ),
      );
      outline(body);
      for (const d of ridgeShadePaths(b)) {
        const shade = svgPath(d);
        canvas.drawPath(
          shade,
          fill(
            verticalBox(shade, [
              { offset: 0, color: c(b.shade), opacity: 0.6 },
              { offset: 1, color: c(b.shade), opacity: 0.15 },
            ]),
          ),
        );
      }
      const grass = ridgeGrass(b);
      if (grass !== '') canvas.drawPath(svgPath(grass), stroke(skColor(c(b.grassColor)), 0.9, 0.8));
      return;
    }
    case 'volcano': {
      const silhouette = svgPath(volcanoPath(b));
      const axis = volcanoShadeAxis(b);
      const erosion = volcanoErosion(b);
      canvas.drawPath(
        silhouette,
        fill(
          linear(0, -b.height, 0, 0, [
            { offset: 0, color: c(b.ash) },
            { offset: 0.55, color: c(b.fill) },
            { offset: 1, color: c(b.fill) },
          ]),
        ),
      );
      outline(silhouette);
      clipped(canvas, silhouette, () => {
        canvas.drawPath(
          svgPath(volcanoShadePath(b)),
          fill(
            linear(axis.x1, axis.y1, axis.x2, axis.y2, [
              { offset: 0, color: c(b.shade), opacity: 0 },
              { offset: 1, color: c(b.shade), opacity: 0.55 },
            ]),
          ),
        );
        canvas.drawPath(svgPath(erosion.ravines), fill(skColor(c(b.gully)), 0.5));
        canvas.drawPath(svgPath(erosion.crests), fill(skColor(c(b.ash)), 0.4));
        canvas.drawRect(
          Skia.XYWHRect(-b.baseWidth, -b.height * 0.45, b.baseWidth * 2, b.height * 0.45 + b.depth),
          fill(
            linear(0, -b.height * 0.45, 0, 0, [
              { offset: 0, color: c(b.haze), opacity: 0 },
              { offset: 1, color: c(b.haze), opacity: 0.55 },
            ]),
          ),
        );
      });
      return;
    }
    case 'snowCap': {
      if (!host) return;
      const silhouette = svgPath(volcanoPath(host));
      const axis = volcanoShadeAxis(host);
      const s = snowPaths(host, b);
      const field = svgPath(s.field);
      clipped(canvas, silhouette, () => {
        canvas.drawPath(svgPath(s.patches), fill(skColor(c(b.snow)), 0.8));
        canvas.drawPath(field, fill(skColor(c(b.snow))));
        outline(field);
        clipped(canvas, field, () => {
          canvas.drawPath(
            svgPath(volcanoShadePath(host)),
            fill(
              linear(axis.x1, axis.y1, axis.x2, axis.y2, [
                { offset: 0, color: c(b.ice), opacity: 0 },
                { offset: 1, color: c(b.ice), opacity: 0.9 },
              ]),
            ),
          );
          canvas.drawPath(svgPath(volcanoErosion(host).ravines), fill(skColor(c(b.ice)), 0.3));
          canvas.drawPath(svgPath(s.outcrops), fill(skColor(c(host.shade)), 0.5));
        });
      });
      return;
    }
    case 'crater': {
      if (!host) return;
      const s = craterPaths(host, b);
      const mouth = svgPath(s.mouth);
      canvas.drawPath(mouth, fill(skColor(c(b.inner))));
      outline(mouth);
      canvas.drawPath(svgPath(s.wall), fill(skColor(c(b.rim)), 0.3));
      canvas.drawPath(svgPath(s.lip), stroke(skColor(c(b.rim)), 1.4));
      return;
    }
    case 'steam': {
      if (!host) return;
      const vent = ventOf(host, ctx.crater);
      canvas.save();
      canvas.translate(vent.x, vent.y);
      const puffs = steamPuffs(b);
      for (const p of puffs) {
        const cx = p.x + p.r * 0.16;
        const cy = p.y + p.r * 0.2;
        canvas.drawCircle(
          cx,
          cy,
          p.r,
          fill(
            radial(cx, cy, p.r, [
              { offset: 0, color: c(b.shade), opacity: 0.45 },
              { offset: 1, color: c(b.shade), opacity: 0 },
            ]),
            p.opacity * 0.6,
          ),
        );
      }
      for (const p of puffs) {
        canvas.drawCircle(
          p.x,
          p.y,
          p.r,
          fill(
            radial(p.x, p.y, p.r, [
              { offset: 0, color: c(b.fill), opacity: 0.7 },
              { offset: 0.5, color: c(b.fill), opacity: 0.35 },
              { offset: 1, color: c(b.fill), opacity: 0 },
            ]),
            p.opacity,
          ),
        );
      }
      canvas.restore();
      return;
    }
    case 'frailejon': {
      const s = frailejonShape(b);
      canvas.drawPath(svgPath(s.stalks), stroke(skColor(c(b.leaf)), 1.1));
      const trunk = svgPath(s.trunk);
      canvas.drawPath(trunk, fill(skColor(c(b.trunk))));
      outline(trunk);
      canvas.drawPath(svgPath(s.trunkDark), stroke(skColor(c(b.trunkShade)), 1.2));
      canvas.drawPath(svgPath(s.trunkLight), stroke(skColor(c(b.leafLight)), 1, 0.45));
      canvas.drawPath(svgPath(s.deadLeaves), fill(skColor(c(b.trunkShade)), 0.9));
      canvas.drawPath(svgPath(s.backLeaves), fill(skColor(c(b.leaf))));
      canvas.drawPath(svgPath(s.frontLeaves), fill(skColor(c(b.leafLight))));
      const flower = fill(skColor(c(b.flower)));
      for (const h of s.heads) canvas.drawCircle(h.cx, h.cy, h.r, flower);
      return;
    }
    case 'flower': {
      canvas.drawPath(svgPath(flowerStem(b)), stroke(skColor(c(b.stem)), 1.1));
      const petals = svgPath(flowerPetals(b));
      canvas.drawPath(petals, fill(skColor(c(b.petal))));
      outline(petals);
      canvas.drawCircle(0, -b.stemHeight, b.petalSize * 0.38, fill(skColor(c(b.center))));
      return;
    }
    case 'lupine': {
      const s = lupineShape(b);
      canvas.drawPath(svgPath(s.stem), stroke(skColor(c(b.leaf)), b.width * 0.08));
      const leaves = svgPath(s.leaves);
      canvas.drawPath(leaves, fill(skColor(c(b.leaf))));
      outline(leaves);
      const color = fill(skColor(c(b.color)));
      for (const f of s.florets) {
        canvas.drawOval(Skia.XYWHRect(f.x - f.rx, f.y - f.ry, f.rx * 2, f.ry * 2), color);
        const rx = f.rx * 0.8;
        const ry = f.ry * 0.75;
        const x = f.x - f.rx * 0.15;
        const y = f.y - f.ry * 0.2;
        canvas.drawOval(
          Skia.XYWHRect(x - rx, y - ry, rx * 2, ry * 2),
          fill(skColor(c(b.colorLight)), 0.25 + 0.75 * f.f),
        );
      }
      return;
    }
    case 'rock': {
      const s = rockPaths(b);
      const body = svgPath(s.body);
      canvas.drawPath(body, fill(skColor(c(b.fill))));
      outline(body);
      canvas.drawPath(svgPath(s.shade), fill(skColor(c(b.shade))));
      canvas.drawPath(svgPath(s.light), fill(skColor(c(b.light)), 0.8));
      return;
    }
    case 'tuft': {
      const s = tuftBlades(b);
      canvas.drawPath(svgPath(s.dark), stroke(skColor(c(b.shade)), 1.2));
      canvas.drawPath(svgPath(s.light), stroke(skColor(c(b.fill)), 1.1));
      return;
    }
    case 'mist': {
      const inner = Math.max(0, Math.min(0.95, (1 - b.diffusion) * 0.8));
      const color = c(b.fill);
      const stops: Stop[] = [
        { offset: 0, color, opacity: 1 },
        { offset: inner, color, opacity: 0.85 },
        { offset: 1, color, opacity: 0 },
      ];
      for (const p of mistPuffs(b)) {
        canvas.drawOval(
          Skia.XYWHRect(p.cx - p.rx, p.cy - p.ry, p.rx * 2, p.ry * 2),
          fill(radialBox(p.cx - p.rx, p.cy - p.ry, p.rx * 2, p.ry * 2, stops)),
        );
      }
      return;
    }
    case 'pet':
    case 'ui':
      // The Pet animates every frame; SceneCanvas draws it separately (drawPet.ts).
      return;
  }
}

// ---------------------------------------------------------------- pictures

interface CacheKey {
  palette: Record<string, string>;
  host: VolcanoBody | null;
  crater: CraterBody | null;
  stroke: Color;
  strokeWidth: number;
  picture: SkPicture;
}

// Bodies and the Pet live around their own origin, with negative coordinates; the recorder's
// default cull rect is (0, 0, 2e6, 2e6), and a picture whose cull rect misses the clip is skipped
// whole.
const BODY_BOUNDS = Skia.XYWHRect(-1e5, -1e5, 2e5, 2e5);

// Keyed by body: idle motions and tracks give objects new transforms but keep their bodies.
const pictures = new WeakMap<Body, CacheKey>();

export function bodyPicture(
  o: SceneObject,
  ctx: Omit<BodyCtx, 'stroke' | 'strokeWidth'>,
): SkPicture {
  const hit = pictures.get(o.body);
  if (
    hit &&
    hit.palette === ctx.palette &&
    hit.host === ctx.host &&
    hit.crater === ctx.crater &&
    hit.stroke === o.stroke &&
    hit.strokeWidth === o.strokeWidth
  )
    return hit.picture;
  const picture = recordPicture((canvas) =>
    drawBody(canvas, o.body, { ...ctx, stroke: o.stroke, strokeWidth: o.strokeWidth }),
  );
  pictures.set(o.body, { ...ctx, stroke: o.stroke, strokeWidth: o.strokeWidth, picture });
  return picture;
}

// ---------------------------------------------------------------- frame

export interface PetSlot {
  /** Scene-space matrix of the Pet's own coordinates (camera, volcano, vent offset, transform). */
  matrix: Mat;
  opacity: number;
  layerIndex: number;
}

export interface Frame {
  /** Points to scene units for the whole drawing. */
  view: Mat;
  layers: {
    id: string;
    opacity: number;
    /** Blur sigma in points. */
    blur: number;
    items: { matrix: Mat; opacity: number; picture: SkPicture | null; pet: boolean }[];
  }[];
}

// Keyed by transform: an object keeps its transform object until a track or an idle motion moves
// it, so a frame computes the matrices of moving objects only.
const transformMats = new WeakMap<Transform, Mat>();

function transformMat(t: Transform): Mat {
  let m = transformMats.get(t);
  if (!m) {
    m = transformValues(t);
    transformMats.set(t, m);
  }
  return m;
}

/**
 * Lays out one frame of `doc` for a w x h canvas: the matrix and picture of every visible object,
 * in draw order. Pure apart from the picture and matrix caches, so it can run on every frame.
 * Matrices carry the same rounded values as the SVG renderer's transform strings.
 */
export function layoutFrame(doc: SceneDoc, w: number, h: number): Frame {
  const vb = sceneViewBox(w, h);
  const s = w / vb.width;
  const view: Mat = [s, 0, 0, s, -vb.x * s, -vb.y * s];
  const layers: Frame['layers'] = [];
  // One camera matrix per depth and frame, shared by every object at that depth.
  const cameras = new Map<number, Mat>();
  const cameraAt = (depth: number) => {
    let m = cameras.get(depth);
    if (!m) {
      m = affineValues(parallaxAffine(doc.camera, depth));
      cameras.set(depth, m);
    }
    return m;
  };
  for (const layer of doc.layers) {
    if (!layer.visible || layer.id === 'uiOverlay') continue;
    const items: Frame['layers'][number]['items'] = [];
    for (const o of layer.objects) {
      const host = volcanoOf(doc, o.body);
      const depth = host ? host.layer.parallax : layer.parallax;
      let m = cameraAt(depth);
      let crater: CraterBody | null = null;
      if (host) {
        m = multiply(m, transformMat(host.object.transform));
        if (o.body.kind === 'steam' || o.body.kind === 'pet')
          crater = craterOf(doc, host.object.id);
        if (o.body.kind === 'pet') {
          const vent = ventOf(host.body, crater);
          m = multiply(m, [1, 0, 0, 1, vent.x, vent.y]);
        }
      }
      m = multiply(m, transformMat(o.transform));
      const pet = o.body.kind === 'pet';
      items.push({
        matrix: m,
        opacity: o.transform.opacity,
        pet,
        picture: pet
          ? null
          : bodyPicture(o, { palette: doc.palette, host: host?.body ?? null, crater }),
      });
    }
    layers.push({ id: layer.id, opacity: layer.opacity, blur: layer.blur * s, items });
  }
  return { view, layers };
}

const HALF = Skia.Matrix().scale(0.5, 0.5);
const DOUBLE = Skia.Matrix().scale(2, 2);

/**
 * Gaussian blur computed at half resolution: shrink, blur by sigma / 2, grow back. A blur hides
 * the lost detail, and it runs on a quarter of the pixels with half the kernel taps; full-size
 * layer blurs took ~30 ms of GPU per frame on the reference phone (Galaxy A24).
 */
function halfResBlur(sigma: number) {
  const { ImageFilter } = Skia;
  const down = ImageFilter.MakeMatrixTransform(HALF, FilterMode.Linear, MipmapMode.None, null);
  const blur = ImageFilter.MakeBlur(sigma / 2, sigma / 2, TileMode.Decal, down);
  return ImageFilter.MakeMatrixTransform(DOUBLE, FilterMode.Linear, MipmapMode.None, blur);
}

// The blur a layer used last: rack-focus sigmas hold still between transitions, and each filter is
// three native objects.
const blurs = new Map<string, { sigma: number; filter: ReturnType<typeof halfResBlur> }>();

function layerBlur(layerId: string, sigma: number) {
  const hit = blurs.get(layerId);
  if (hit?.sigma === sigma) return hit.filter;
  const filter = halfResBlur(sigma);
  blurs.set(layerId, { sigma, filter });
  return filter;
}

/** Records `draw` (in its own coordinates, any sign) as a picture to replay under a matrix. */
export function recordPicture(draw: (canvas: SkCanvas) => void): SkPicture {
  const recorder = Skia.PictureRecorder();
  draw(recorder.beginRecording(BODY_BOUNDS));
  return recorder.finishRecordingAsPicture();
}

/** Replays a laid-out frame; `drawPet` draws the Pet in its own coordinates. */
export function drawFrame(canvas: SkCanvas, frame: Frame, drawPet: (canvas: SkCanvas) => void) {
  canvas.save();
  concat(canvas, frame.view);
  for (const layer of frame.layers) {
    if (layer.opacity <= 0) continue;
    const blurred = layer.blur > 0.05;
    if (blurred || layer.opacity < 1) {
      const p = Skia.Paint();
      if (layer.opacity < 1) p.setAlphaf(layer.opacity);
      // Skia scales a layer's blur by the current matrix, so the sigma stays in scene units here
      // (the view scale is already applied), matching the points the SVG renderer converts to.
      const sigma = layer.blur / frame.view[0];
      if (blurred) p.setImageFilter(layerBlur(layer.id, sigma));
      canvas.saveLayer(p);
    } else canvas.save();
    for (const it of layer.items) {
      if (it.opacity <= 0) continue;
      if (it.opacity < 1) {
        const p = Skia.Paint();
        p.setAlphaf(it.opacity);
        canvas.saveLayer(p);
      } else canvas.save();
      concat(canvas, it.matrix);
      if (it.pet) drawPet(canvas);
      else if (it.picture) canvas.drawPicture(it.picture);
      canvas.restore();
    }
    canvas.restore();
  }
  canvas.restore();
}
