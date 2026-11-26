// The scene's Pet on Skia: PetVaporFigure (src/ui/pet) call for call, from the same PetFrame, so
// the native onboarding and the SVG renderer show the same Pet.
import {
  PaintStyle,
  Skia,
  StrokeCap,
  StrokeJoin,
  TileMode,
  type SkCanvas,
} from '@shopify/react-native-skia';

import type { PetConfig, PetFrame, PetStroke } from './petCore';

import { skColor, svgPath, toSkMatrix } from '@/ui/skia/primitives';
import { parseTransform } from '@/ui/skia/svgTransform';

const WHITE = '#ffffff';

export function drawPet(
  canvas: SkCanvas,
  config: PetConfig,
  f: PetFrame,
  fillHex: string,
  shadeHex: string,
) {
  const b = config.body;
  const headR = (Math.max(b.width * b.scaleX, b.height * b.scaleY) / 2) * 1.25;
  const paint = () => {
    const p = Skia.Paint();
    p.setAntiAlias(true);
    return p;
  };
  const drawStroke = (s: PetStroke) => {
    const p = paint();
    p.setColor(skColor(s.color));
    canvas.save();
    canvas.concat(toSkMatrix(parseTransform(s.transform)));
    if (s.filled) canvas.drawPath(svgPath(s.d), p);
    const line = p.copy();
    line.setStyle(PaintStyle.Stroke);
    line.setStrokeWidth(s.width);
    line.setStrokeCap(StrokeCap.Round);
    line.setStrokeJoin(StrokeJoin.Round);
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
  for (const p of f.vapor) {
    const q = paint();
    q.setShader(
      Skia.Shader.MakeRadialGradient(
        Skia.Point(p.x, p.y),
        p.r,
        [skColor(fillHex, 0.8), skColor(fillHex, 0.45), skColor(fillHex, 0)],
        [0, 0.5, 1],
        TileMode.Clamp,
      ),
    );
    q.setAlphaf(p.opacity);
    canvas.drawCircle(p.x, p.y, p.r, q);
  }
  for (const p of f.vapor) {
    const cx = p.x + p.r * 0.2 * turn;
    const cy = p.y + p.r * 0.25;
    const q = paint();
    q.setShader(
      Skia.Shader.MakeRadialGradient(
        Skia.Point(cx, cy),
        p.r,
        [skColor(shadeHex, 0.4), skColor(shadeHex, 0)],
        [0, 1],
        TileMode.Clamp,
      ),
    );
    q.setAlphaf(p.opacity);
    canvas.drawCircle(cx, cy, p.r, q);
  }
  const body = svgPath(f.body);
  const box = body.getBounds();
  const core = paint();
  core.setShader(
    Skia.Shader.MakeLinearGradient(
      Skia.Point(box.x, box.y),
      Skia.Point(box.x, box.y + box.height),
      [skColor(fillHex, 1), skColor(fillHex, 0.97), skColor(fillHex, 0)],
      [0, 0.66, 1],
      TileMode.Clamp,
    ),
  );
  canvas.drawPath(body, core);
  const form = paint();
  form.setShader(
    Skia.Shader.MakeRadialGradient(
      Skia.Point(f.headX - 10 * turn, b.y - 14),
      headR,
      [skColor(shadeHex, 0), skColor(shadeHex, 0), skColor(shadeHex, 0.42), skColor(shadeHex, 0)],
      [0, 0.6, 0.86, 1],
      TileMode.Clamp,
    ),
  );
  canvas.drawPath(body, form);
  // Highlight: SVG's default radial gradient over the volume path's box.
  const volume = svgPath(f.volume);
  const v = volume.getBounds();
  const center = Skia.Point(v.x + v.width / 2, v.y + v.height / 2);
  const w = Math.max(v.width, 1e-3);
  const local = Skia.Matrix()
    .translate(center.x, center.y)
    .scale(1, Math.max(v.height, 1e-3) / w)
    .translate(-center.x, -center.y);
  const hi = paint();
  hi.setShader(
    Skia.Shader.MakeRadialGradient(
      center,
      w / 2,
      [skColor(WHITE, 0.85), skColor(WHITE, 0)],
      [0, 1],
      TileMode.Clamp,
      local,
    ),
  );
  hi.setAlphaf(f.volumeOpacity);
  canvas.drawPath(volume, hi);
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
