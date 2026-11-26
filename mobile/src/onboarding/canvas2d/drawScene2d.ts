// Web renderer for a SceneDoc on 2D canvases: NevadoScene's ObjectBody (the SVG reference) call for
// call, painted without a React element or DOM node per shape. Rendering that SVG tree on every
// frame held the web onboarding near 25 fps; the browser rasterizes canvas commands off the main
// thread. The layout mirrors skia/drawScene.ts, which binds to Skia and cannot load on web.
import { drawPetCanvas2d, pathBox } from "@/ui/pet/drawPetCanvas2d";
import type { PetConfig, PetFrame } from "@/ui/pet/petCore";
import { multiply, type Mat } from "@/ui/skia/svgTransform";

import { craterOf, resolveColor, ventOf, volcanoOf } from "../scene/doc";
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
} from "../scene/geometry";
import type {
  Body,
  Color,
  CraterBody,
  SceneDoc,
  SceneObject,
  Transform,
  VolcanoBody,
} from "../scene/types";

type Ctx = CanvasRenderingContext2D;

// ---------------------------------------------------------------- primitives

const rgbCache = new Map<string, string>();

/** `#rrggbb` (or `#rgb`) with an alpha, as a CSS color. */
function rgba(hex: string, alpha = 1): string {
  let rgb = rgbCache.get(hex);
  if (!rgb) {
    const h = hex.replace("#", "");
    const full = h.length === 3 ? h.replace(/(.)/g, "$1$1") : h.slice(0, 6);
    const n = parseInt(full, 16);
    if (Number.isNaN(n) || full.length !== 6)
      throw new Error(`unsupported color ${hex}`);
    rgb = `${(n >> 16) & 255} ${(n >> 8) & 255} ${n & 255}`;
    rgbCache.set(hex, rgb);
  }
  return `rgb(${rgb} / ${alpha})`;
}

interface Stop {
  offset: number;
  color: string;
  opacity?: number;
}

function withStops<G extends CanvasGradient>(g: G, stops: Stop[]): G {
  for (const s of stops)
    g.addColorStop(s.offset, rgba(s.color, s.opacity ?? 1));
  return g;
}

/** A circle filled with SVG's default radial gradient (its box: cx, cy and r as fractions). */
function radialCircle(
  ctx: Ctx,
  cx: number,
  cy: number,
  r: number,
  stops: Stop[],
  fy = 0.5,
) {
  const gy = cy - r + fy * 2 * r;
  ctx.fillStyle = withStops(
    ctx.createRadialGradient(cx, gy, 0, cx, gy, r),
    stops,
  );
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.fill();
}

/** An ellipse filled with SVG's default radial gradient over its box, a circle squashed to it. */
function radialEllipse(
  ctx: Ctx,
  cx: number,
  cy: number,
  rx: number,
  ry: number,
  stops: Stop[],
) {
  ctx.save();
  ctx.translate(cx, cy);
  ctx.scale(1, ry / rx);
  ctx.fillStyle = withStops(ctx.createRadialGradient(0, 0, 0, 0, 0, rx), stops);
  ctx.beginPath();
  ctx.arc(0, 0, rx, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function ellipse(
  ctx: Ctx,
  cx: number,
  cy: number,
  rx: number,
  ry: number,
  fill: string,
) {
  ctx.fillStyle = fill;
  ctx.beginPath();
  ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2);
  ctx.fill();
}

function fillPath(
  ctx: Ctx,
  p: Path2D,
  style: string | CanvasGradient,
  opacity = 1,
) {
  ctx.globalAlpha = opacity;
  ctx.fillStyle = style;
  ctx.fill(p);
  ctx.globalAlpha = 1;
}

/** SVG stroke; `round` caps and joins, else SVG's butt caps and miter joins. */
function strokePath(
  ctx: Ctx,
  p: Path2D,
  color: string,
  width: number,
  round: boolean,
  opacity = 1,
) {
  ctx.globalAlpha = opacity;
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.lineCap = round ? "round" : "butt";
  ctx.lineJoin = round ? "round" : "miter";
  ctx.stroke(p);
  ctx.globalAlpha = 1;
}

/** `linear` with x1=0 y1=0 x2=0 y2=1 over a path's box (objectBoundingBox): top to bottom. */
function verticalBox(ctx: Ctx, d: string, stops: Stop[]) {
  const b = pathBox(d);
  return withStops(
    ctx.createLinearGradient(b.x, b.y, b.x, b.y + b.height),
    stops,
  );
}

function clipped(ctx: Ctx, clip: Path2D, draw: () => void) {
  ctx.save();
  ctx.clip(clip);
  draw();
  ctx.restore();
}

// Geometry depends only on a body (and, for volcano parts, the volcano body). Idle motions and
// tracks give objects new transforms but keep their bodies, so their paths are parsed once.
const geoCache = new WeakMap<object, { dep: object | null; value: unknown }>();
function geo<T>(body: object, dep: object | null, make: () => T): T {
  const hit = geoCache.get(body);
  if (hit && hit.dep === dep) return hit.value as T;
  const value = make();
  geoCache.set(body, { dep, value });
  return value;
}

const toPath = (d: string) => new Path2D(d);

const volcanoGeo = (v: VolcanoBody) =>
  geo(v, null, () => {
    const erosion = volcanoErosion(v);
    return {
      silhouette: toPath(volcanoPath(v)),
      shade: toPath(volcanoShadePath(v)),
      shadeAxis: volcanoShadeAxis(v),
      ravines: toPath(erosion.ravines),
      crests: toPath(erosion.crests),
    };
  });

// ---------------------------------------------------------------- bodies

interface BodyCtx {
  palette: Record<string, string>;
  stroke: Color;
  strokeWidth: number;
  host: VolcanoBody | null;
  crater: CraterBody | null;
}

/** Draws one body in its own coordinates, like NevadoScene's ObjectBody. */
function drawBody(ctx: Ctx, b: Body, bc: BodyCtx) {
  const c = (color: Color) => resolveColor(bc.palette, color);
  const outline = (p: Path2D) => {
    if (bc.strokeWidth > 0)
      strokePath(ctx, p, c(bc.stroke), bc.strokeWidth, false);
  };
  const { host } = bc;
  switch (b.kind) {
    case "sky": {
      ctx.fillStyle = withStops(ctx.createLinearGradient(0, 0, 0, b.horizon), [
        { offset: 0, color: c(b.top) },
        { offset: b.middleStop, color: c(b.middle) },
        { offset: 1, color: c(b.bottom) },
      ]);
      ctx.fillRect(-1400, -1400, 3200, 3600);
      return;
    }
    case "sun": {
      const halo = c(b.halo);
      radialCircle(ctx, 0, 0, b.haloRadius, [
        { offset: 0, color: halo, opacity: b.haloStrength },
        { offset: 0.25, color: halo, opacity: b.haloStrength * 0.45 },
        { offset: 1, color: halo, opacity: 0 },
      ]);
      const core = new Path2D();
      core.arc(0, 0, b.radius, 0, Math.PI * 2);
      fillPath(ctx, core, c(b.core));
      outline(core);
      return;
    }
    case "cloud": {
      const puffs = geo(b, null, () => cloudPuffs(b));
      const base = (1 - b.flatness) * b.height * 0.6;
      const fill = c(b.fill);
      const shade = c(b.shade);
      ctx.save();
      ctx.beginPath();
      ctx.rect(-b.width, -b.height * 3, b.width * 2, b.height * 3 + base);
      ctx.clip();
      for (const p of puffs)
        radialCircle(ctx, p.cx + p.r * 0.1, p.cy + p.r * 0.3, p.r, [
          { offset: 0, color: shade, opacity: 0.9 },
          { offset: 0.65, color: shade, opacity: 0.6 },
          { offset: 1, color: shade, opacity: 0 },
        ]);
      for (const p of puffs) {
        const r = p.r * 1.02;
        const cy = p.cy - p.r * 0.05;
        radialCircle(
          ctx,
          p.cx,
          cy,
          r,
          [
            { offset: 0, color: fill, opacity: 1 },
            { offset: 0.7, color: fill, opacity: 0.9 },
            { offset: 1, color: fill, opacity: 0 },
          ],
          0.45,
        );
        if (bc.strokeWidth > 0) {
          const ring = new Path2D();
          ring.arc(p.cx, cy, r, 0, Math.PI * 2);
          outline(ring);
        }
      }
      ctx.restore();
      return;
    }
    case "ridge": {
      const g = geo(b, null, () => {
        const body = ridgePath(b);
        const shade = ridgeShadePaths(b);
        const grass = ridgeGrass(b);
        return {
          body,
          bodyPath: toPath(body),
          shade: shade.map((d) => ({ d, path: toPath(d) })),
          grass: grass === "" ? null : toPath(grass),
        };
      });
      fillPath(
        ctx,
        g.bodyPath,
        verticalBox(ctx, g.body, [
          { offset: 0, color: c(b.top) },
          { offset: 1, color: c(b.bottom) },
        ]),
      );
      outline(g.bodyPath);
      for (const s of g.shade)
        fillPath(
          ctx,
          s.path,
          verticalBox(ctx, s.d, [
            { offset: 0, color: c(b.shade), opacity: 0.6 },
            { offset: 1, color: c(b.shade), opacity: 0.15 },
          ]),
        );
      if (g.grass) strokePath(ctx, g.grass, c(b.grassColor), 0.9, true, 0.8);
      return;
    }
    case "volcano": {
      const g = volcanoGeo(b);
      const axis = g.shadeAxis;
      fillPath(
        ctx,
        g.silhouette,
        withStops(ctx.createLinearGradient(0, -b.height, 0, 0), [
          { offset: 0, color: c(b.ash) },
          { offset: 0.55, color: c(b.fill) },
          { offset: 1, color: c(b.fill) },
        ]),
      );
      outline(g.silhouette);
      clipped(ctx, g.silhouette, () => {
        fillPath(
          ctx,
          g.shade,
          withStops(
            ctx.createLinearGradient(axis.x1, axis.y1, axis.x2, axis.y2),
            [
              { offset: 0, color: c(b.shade), opacity: 0 },
              { offset: 1, color: c(b.shade), opacity: 0.55 },
            ],
          ),
        );
        fillPath(ctx, g.ravines, c(b.gully), 0.5);
        fillPath(ctx, g.crests, c(b.ash), 0.4);
        ctx.fillStyle = withStops(
          ctx.createLinearGradient(0, -b.height * 0.45, 0, 0),
          [
            { offset: 0, color: c(b.haze), opacity: 0 },
            { offset: 1, color: c(b.haze), opacity: 0.55 },
          ],
        );
        ctx.fillRect(
          -b.baseWidth,
          -b.height * 0.45,
          b.baseWidth * 2,
          b.height * 0.45 + b.depth,
        );
      });
      return;
    }
    case "snowCap": {
      if (!host) return;
      const v = volcanoGeo(host);
      const s = geo(b, host, () => {
        const paths = snowPaths(host, b);
        return {
          patches: toPath(paths.patches),
          field: toPath(paths.field),
          outcrops: toPath(paths.outcrops),
        };
      });
      const axis = v.shadeAxis;
      clipped(ctx, v.silhouette, () => {
        fillPath(ctx, s.patches, c(b.snow), 0.8);
        fillPath(ctx, s.field, c(b.snow));
        outline(s.field);
        clipped(ctx, s.field, () => {
          fillPath(
            ctx,
            v.shade,
            withStops(
              ctx.createLinearGradient(axis.x1, axis.y1, axis.x2, axis.y2),
              [
                { offset: 0, color: c(b.ice), opacity: 0 },
                { offset: 1, color: c(b.ice), opacity: 0.9 },
              ],
            ),
          );
          fillPath(ctx, v.ravines, c(b.ice), 0.3);
          fillPath(ctx, s.outcrops, c(host.shade), 0.5);
        });
      });
      return;
    }
    case "crater": {
      if (!host) return;
      const s = geo(b, host, () => {
        const paths = craterPaths(host, b);
        return {
          mouth: toPath(paths.mouth),
          wall: toPath(paths.wall),
          lip: toPath(paths.lip),
        };
      });
      fillPath(ctx, s.mouth, c(b.inner));
      outline(s.mouth);
      fillPath(ctx, s.wall, c(b.rim), 0.3);
      strokePath(ctx, s.lip, c(b.rim), 1.4, true);
      return;
    }
    case "steam": {
      if (!host) return;
      const vent = ventOf(host, bc.crater);
      const puffs = steamPuffs(b);
      const fill = c(b.fill);
      const shade = c(b.shade);
      ctx.save();
      ctx.translate(vent.x, vent.y);
      for (const p of puffs) {
        ctx.globalAlpha = p.opacity * 0.6;
        radialCircle(ctx, p.x + p.r * 0.16, p.y + p.r * 0.2, p.r, [
          { offset: 0, color: shade, opacity: 0.45 },
          { offset: 1, color: shade, opacity: 0 },
        ]);
      }
      for (const p of puffs) {
        ctx.globalAlpha = p.opacity;
        radialCircle(ctx, p.x, p.y, p.r, [
          { offset: 0, color: fill, opacity: 0.7 },
          { offset: 0.5, color: fill, opacity: 0.35 },
          { offset: 1, color: fill, opacity: 0 },
        ]);
      }
      ctx.restore();
      return;
    }
    case "frailejon": {
      const s = geo(b, null, () => {
        const shape = frailejonShape(b);
        return {
          heads: shape.heads,
          stalks: toPath(shape.stalks),
          trunk: toPath(shape.trunk),
          trunkDark: toPath(shape.trunkDark),
          trunkLight: toPath(shape.trunkLight),
          deadLeaves: toPath(shape.deadLeaves),
          backLeaves: toPath(shape.backLeaves),
          frontLeaves: toPath(shape.frontLeaves),
        };
      });
      strokePath(ctx, s.stalks, c(b.leaf), 1.1, true);
      fillPath(ctx, s.trunk, c(b.trunk));
      outline(s.trunk);
      strokePath(ctx, s.trunkDark, c(b.trunkShade), 1.2, true);
      strokePath(ctx, s.trunkLight, c(b.leafLight), 1, true, 0.45);
      fillPath(ctx, s.deadLeaves, c(b.trunkShade), 0.9);
      fillPath(ctx, s.backLeaves, c(b.leaf));
      fillPath(ctx, s.frontLeaves, c(b.leafLight));
      for (const h of s.heads) ellipse(ctx, h.cx, h.cy, h.r, h.r, c(b.flower));
      return;
    }
    case "flower": {
      const s = geo(b, null, () => ({
        stem: toPath(flowerStem(b)),
        petals: toPath(flowerPetals(b)),
      }));
      strokePath(ctx, s.stem, c(b.stem), 1.1, true);
      fillPath(ctx, s.petals, c(b.petal));
      outline(s.petals);
      const r = b.petalSize * 0.38;
      ellipse(ctx, 0, -b.stemHeight, r, r, c(b.center));
      return;
    }
    case "lupine": {
      const s = geo(b, null, () => {
        const shape = lupineShape(b);
        return {
          florets: shape.florets,
          stem: toPath(shape.stem),
          leaves: toPath(shape.leaves),
        };
      });
      strokePath(ctx, s.stem, c(b.leaf), b.width * 0.08, true);
      fillPath(ctx, s.leaves, c(b.leaf));
      outline(s.leaves);
      const color = c(b.color);
      for (const f of s.florets) {
        ellipse(ctx, f.x, f.y, f.rx, f.ry, color);
        ellipse(
          ctx,
          f.x - f.rx * 0.15,
          f.y - f.ry * 0.2,
          f.rx * 0.8,
          f.ry * 0.75,
          rgba(c(b.colorLight), 0.25 + 0.75 * f.f),
        );
      }
      return;
    }
    case "rock": {
      const s = geo(b, null, () => {
        const paths = rockPaths(b);
        return {
          body: toPath(paths.body),
          shade: toPath(paths.shade),
          light: toPath(paths.light),
        };
      });
      fillPath(ctx, s.body, c(b.fill));
      outline(s.body);
      fillPath(ctx, s.shade, c(b.shade));
      fillPath(ctx, s.light, c(b.light), 0.8);
      return;
    }
    case "tuft": {
      const s = geo(b, null, () => {
        const blades = tuftBlades(b);
        return { dark: toPath(blades.dark), light: toPath(blades.light) };
      });
      strokePath(ctx, s.dark, c(b.shade), 1.2, true);
      strokePath(ctx, s.light, c(b.fill), 1.1, true);
      return;
    }
    case "mist": {
      const inner = Math.max(0, Math.min(0.95, (1 - b.diffusion) * 0.8));
      const color = c(b.fill);
      const stops: Stop[] = [
        { offset: 0, color, opacity: 1 },
        { offset: inner, color, opacity: 0.85 },
        { offset: 1, color, opacity: 0 },
      ];
      for (const p of geo(b, null, () => mistPuffs(b)))
        radialEllipse(ctx, p.cx, p.cy, p.rx, p.ry, stops);
      return;
    }
    case "pet":
    case "ui":
      // The Pet animates every frame; the caller draws it (drawPetCanvas2d).
      return;
  }
}

// ---------------------------------------------------------------- frame

export interface Item {
  object: SceneObject;
  /** Scene-space matrix of the object's own coordinates (camera, volcano, vent offset, transform). */
  matrix: Mat;
  host: VolcanoBody | null;
  crater: CraterBody | null;
}

export interface LayerFrame {
  id: string;
  opacity: number;
  /** Blur sigma in points. */
  blur: number;
  items: Item[];
}

export interface Frame {
  /** Points to scene units for the whole drawing. */
  view: Mat;
  layers: LayerFrame[];
}

// Keyed by transform: an object keeps its transform object until a track or an idle motion moves it.
const transformMats = new WeakMap<Transform, Mat>();

function transformMat(t: Transform): Mat {
  let m = transformMats.get(t);
  if (!m) {
    m = transformValues(t);
    transformMats.set(t, m);
  }
  return m;
}

/** drawScene.ts's layoutFrame, with each object instead of its Skia picture. */
export function layoutFrame(doc: SceneDoc, w: number, h: number): Frame {
  const vb = sceneViewBox(w, h);
  const s = w / vb.width;
  const view: Mat = [s, 0, 0, s, -vb.x * s, -vb.y * s];
  const layers: LayerFrame[] = [];
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
    if (!layer.visible || layer.id === "uiOverlay") continue;
    const items: Item[] = [];
    for (const o of layer.objects) {
      const host = volcanoOf(doc, o.body);
      const depth = host ? host.layer.parallax : layer.parallax;
      let m = cameraAt(depth);
      let crater: CraterBody | null = null;
      if (host) {
        m = multiply(m, transformMat(host.object.transform));
        if (o.body.kind === "steam" || o.body.kind === "pet")
          crater = craterOf(doc, host.object.id);
        if (o.body.kind === "pet") {
          const vent = ventOf(host.body, crater);
          m = multiply(m, [1, 0, 0, 1, vent.x, vent.y]);
        }
      }
      items.push({
        object: o,
        matrix: multiply(m, transformMat(o.transform)),
        host: host?.body ?? null,
        crater,
      });
    }
    layers.push({
      id: layer.id,
      opacity: layer.opacity,
      blur: layer.blur * s,
      items,
    });
  }
  return { view, layers };
}

/** The scene's Pet in its own coordinates. */
export interface ScenePet {
  config: PetConfig;
  frame: PetFrame;
  fill: string;
  shade: string;
}

/**
 * Paints one layer's objects onto `ctx`; `toDevice` maps scene units to its pixels. An object
 * with opacity below 1 is painted on `scratch` (same size) first and composited, as SVG's group
 * opacity does where its shapes overlap.
 */
export function drawLayer(
  ctx: Ctx,
  scratch: Ctx,
  toDevice: Mat,
  layer: LayerFrame,
  palette: Record<string, string>,
  pet: ScenePet | null,
) {
  for (const it of layer.items) {
    const opacity = it.object.transform.opacity;
    if (opacity <= 0) continue;
    const target = opacity < 1 ? scratch : ctx;
    if (target === scratch) {
      scratch.setTransform(1, 0, 0, 1, 0, 0);
      scratch.clearRect(0, 0, scratch.canvas.width, scratch.canvas.height);
    }
    const m = multiply(toDevice, it.matrix);
    target.setTransform(m[0], m[1], m[2], m[3], m[4], m[5]);
    target.miterLimit = 4;
    const o = it.object;
    if (o.body.kind === "pet") {
      if (pet)
        drawPetCanvas2d(target, pet.config, pet.frame, pet.fill, pet.shade);
    } else
      drawBody(target, o.body, {
        palette,
        stroke: o.stroke,
        strokeWidth: o.strokeWidth,
        host: it.host,
        crater: it.crater,
      });
    if (target === scratch) {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.globalAlpha = opacity;
      ctx.drawImage(scratch.canvas, 0, 0);
      ctx.globalAlpha = 1;
    }
  }
}
