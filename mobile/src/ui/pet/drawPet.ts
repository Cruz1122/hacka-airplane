// The scene's Pet on Skia: PetVaporFigure (src/ui/pet) call for call, from the same PetFrame, so
// the native onboarding and the SVG renderer show the same Pet.
import {
  PaintStyle,
  Skia,
  StrokeCap,
  StrokeJoin,
  TileMode,
  type SkCanvas,
  type SkPaint,
  type SkShader,
} from '@shopify/react-native-skia';

import type { PetConfig, PetFrame, PetStroke } from './petCore';

import { skColor, svgPath, toSkMatrix } from '@/ui/skia/primitives';
import { parseTransform } from '@/ui/skia/svgTransform';

const WHITE = '#ffffff';

// Every Skia object is a JSI host object the GC has to finalize, and a frame used to make about
// 90 (a paint and a gradient per puff). Paints are reused: a recording copies a paint's state at
// each draw. The puffs' gradients differ only in place and size, so each color gets one on the
// unit circle and the canvas transform scales it onto each puff.
interface Paints {
  puff: SkPaint;
  body: SkPaint;
  fill: SkPaint;
  line: SkPaint;
}
let paints: Paints | null = null;
function getPaints(): Paints {
  if (paints) return paints;
  const make = () => {
    const p = Skia.Paint();
    p.setAntiAlias(true);
    return p;
  };
  const line = make();
  line.setStyle(PaintStyle.Stroke);
  line.setStrokeCap(StrokeCap.Round);
  line.setStrokeJoin(StrokeJoin.Round);
  paints = { puff: make(), body: make(), fill: make(), line };
  return paints;
}

const halos = new Map<string, { light: SkShader; shade: SkShader }>();
/** PetVaporFigure's halo / halo-shade gradients on the unit circle. */
function haloShaders(fillHex: string, shadeHex: string) {
  const key = `${fillHex} ${shadeHex}`;
  let h = halos.get(key);
  if (!h) {
    const o = Skia.Point(0, 0);
    h = {
      light: Skia.Shader.MakeRadialGradient(
        o,
        1,
        [skColor(fillHex, 0.8), skColor(fillHex, 0.45), skColor(fillHex, 0)],
        [0, 0.5, 1],
        TileMode.Clamp,
      ),
      shade: Skia.Shader.MakeRadialGradient(
        o,
        1,
        [skColor(shadeHex, 0.4), skColor(shadeHex, 0)],
        [0, 1],
        TileMode.Clamp,
      ),
    };
    // The app passes a handful of colors; the Lab's pickers could pass many.
    if (halos.size >= 16) halos.clear();
    halos.set(key, h);
  }
  return h;
}

function drawPuff(canvas: SkCanvas, paint: SkPaint, x: number, y: number, r: number) {
  canvas.save();
  canvas.translate(x, y);
  canvas.scale(r, r);
  canvas.drawCircle(0, 0, 1, paint);
  canvas.restore();
}

export function drawPet(
  canvas: SkCanvas,
  config: PetConfig,
  f: PetFrame,
  fillHex: string,
  shadeHex: string,
) {
  const b = config.body;
  const headR = (Math.max(b.width * b.scaleX, b.height * b.scaleY) / 2) * 1.25;
  const { puff, body: shaded, fill, line } = getPaints();
  const drawStroke = (s: PetStroke) => {
    const color = skColor(s.color);
    canvas.save();
    canvas.concat(toSkMatrix(parseTransform(s.transform)));
    if (s.filled) {
      fill.setColor(color);
      canvas.drawPath(svgPath(s.d), fill);
    }
    line.setColor(color);
    line.setStrokeWidth(s.width);
    canvas.drawPath(svgPath(s.d), line);
    canvas.restore();
  };
  const turn = 1 - 2 * f.turn;

  canvas.save();
  canvas.translate(f.shiftX, 0);
  canvas.translate(0, f.float);
  canvas.save();
  canvas.concat(toSkMatrix(parseTransform(f.bodyTransform)));
  // Halo behind the body, light then shade (PetVaporFigure's halo / halo-shade gradients).
  const halo = haloShaders(fillHex, shadeHex);
  puff.setShader(halo.light);
  for (const p of f.vapor) {
    puff.setAlphaf(p.opacity);
    drawPuff(canvas, puff, p.x, p.y, p.r);
  }
  puff.setShader(halo.shade);
  for (const p of f.vapor) {
    puff.setAlphaf(p.opacity);
    drawPuff(canvas, puff, p.x + p.r * 0.2 * turn, p.y + p.r * 0.25, p.r);
  }
  const body = svgPath(f.body);
  const box = body.getBounds();
  shaded.setAlphaf(1);
  shaded.setShader(
    Skia.Shader.MakeLinearGradient(
      Skia.Point(box.x, box.y),
      Skia.Point(box.x, box.y + box.height),
      [skColor(fillHex, 1), skColor(fillHex, 0.97), skColor(fillHex, 0)],
      [0, 0.66, 1],
      TileMode.Clamp,
    ),
  );
  canvas.drawPath(body, shaded);
  shaded.setShader(
    Skia.Shader.MakeRadialGradient(
      Skia.Point(f.headX - 10 * turn, b.y - 14),
      headR,
      [skColor(shadeHex, 0), skColor(shadeHex, 0), skColor(shadeHex, 0.42), skColor(shadeHex, 0)],
      [0, 0.6, 0.86, 1],
      TileMode.Clamp,
    ),
  );
  canvas.drawPath(body, shaded);
  // Highlight: SVG's default radial gradient over the volume path's box.
  const volume = svgPath(f.volume);
  const v = volume.getBounds();
  const center = Skia.Point(v.x + v.width / 2, v.y + v.height / 2);
  const w = Math.max(v.width, 1e-3);
  const local = Skia.Matrix()
    .translate(center.x, center.y)
    .scale(1, Math.max(v.height, 1e-3) / w)
    .translate(-center.x, -center.y);
  shaded.setShader(
    Skia.Shader.MakeRadialGradient(
      center,
      w / 2,
      [skColor(WHITE, 0.85), skColor(WHITE, 0)],
      [0, 1],
      TileMode.Clamp,
      local,
    ),
  );
  shaded.setAlphaf(f.volumeOpacity);
  canvas.drawPath(volume, shaded);
  canvas.restore();
  canvas.save();
  canvas.concat(toSkMatrix(parseTransform(f.features)));
  canvas.save();
  canvas.concat(toSkMatrix(parseTransform(f.eyes)));
  drawStroke(f.leftEye);
  drawStroke(f.rightEye);
  canvas.restore();
  drawStroke(f.mouth);
  canvas.restore();
  canvas.restore();
}
