// Web scene renderer on Skia (CanvasKit over WebGL): the native renderer's layout, body pictures
// and Pet drawer (drawScene.ts, drawPet.ts) painted on a <canvas>. SceneCanvas.tsx imports this
// module only once CanvasKit is on the global object, because the Skia API binds to that global
// when its module first runs.
import { Skia, TileMode, type SkCanvas, type SkImageFilter } from '@shopify/react-native-skia';
import type {
  CanvasKit,
  GrDirectContext,
  SkPicture,
  Surface,
  WebGLContextHandle,
} from 'canvaskit-wasm';
import { useLayoutEffect, useMemo, useRef } from 'react';

import { drawPet } from '@/ui/pet/drawPet';
import { blinkAt, PET_PRESET, petFrame, type PetConfig } from '@/ui/pet/petCore';
import { useFaceTransition } from '@/ui/pet/useFaceTransition';
import { toSkMatrix } from '@/ui/skia/primitives';
import { useReducedMotion } from '@/ui/useReducedMotion';

import type { NevadoSceneProps } from '../NevadoScene';
import { resolveColor } from '../scene/doc';
import type { PetBody, SceneDoc } from '../scene/types';
import { layoutFrame, type Frame } from './drawScene';

export interface SkiaSceneWebProps extends NevadoSceneProps {
  /** Called when WebGL is missing or its context is lost; the host then draws with SVG. */
  onLost: () => void;
}

function petOf(doc: SceneDoc): PetBody | null {
  for (const l of doc.layers) {
    if (!l.visible) continue;
    for (const o of l.objects) if (o.body.kind === 'pet') return o.body;
  }
  return null;
}

const NO_PET: PetBody['emotion'] = 'happy';

/** Sharp on dense screens without painting more than 3x the points, like the web Pet. */
const pixelRatio = () =>
  typeof window === 'undefined' ? 1 : Math.min(3, Math.max(1, window.devicePixelRatio || 1));

// A recording copies a paint's state at each saveLayer, so two paints serve every frame.
const layerPaint = Skia.Paint();
const itemPaint = Skia.Paint();
const recorder = Skia.PictureRecorder();

// A full-resolution Gaussian, not native's half-resolution one (drawScene.ts): it is the browser's
// CSS blur, so the layers blur exactly as the SVG renderer's do (measured on a GPU), and
// react-native-skia's web API has no matrix-transform image filter.
const blurs = new Map<string, { sigma: number; filter: SkImageFilter }>();
function layerBlur(layerId: string, sigma: number) {
  const hit = blurs.get(layerId);
  if (hit?.sigma === sigma) return hit.filter;
  hit?.filter.dispose();
  const filter = Skia.ImageFilter.MakeBlur(sigma, sigma, TileMode.Decal, null);
  blurs.set(layerId, { sigma, filter });
  return filter;
}

/** drawScene's drawFrame with that plain blur. */
function replay(canvas: SkCanvas, frame: Frame, pet: ((c: SkCanvas) => void) | null) {
  canvas.save();
  canvas.concat(toSkMatrix(frame.view));
  for (const layer of frame.layers) {
    if (layer.opacity <= 0) continue;
    const blurred = layer.blur > 0.05;
    if (blurred || layer.opacity < 1) {
      layerPaint.setAlphaf(layer.opacity);
      // The sigma stays in scene units: Skia scales a layer's blur by the current matrix.
      layerPaint.setImageFilter(blurred ? layerBlur(layer.id, layer.blur / frame.view[0]) : null);
      canvas.saveLayer(layerPaint);
    } else canvas.save();
    for (const it of layer.items) {
      if (it.opacity <= 0) continue;
      if (it.opacity < 1) {
        itemPaint.setAlphaf(it.opacity);
        canvas.saveLayer(itemPaint);
      } else canvas.save();
      canvas.concat(toSkMatrix(it.matrix));
      if (it.pet) pet?.(canvas);
      else if (it.picture) canvas.drawPicture(it.picture);
      canvas.restore();
    }
    canvas.restore();
  }
  canvas.restore();
}

interface Gpu {
  ck: CanvasKit;
  handle: WebGLContextHandle;
  context: GrDirectContext;
  surface: Surface | null;
}

const ckPicture = (p: unknown) => (p as { ref: SkPicture }).ref;

export function SkiaSceneWeb({ doc, width, height, onLost }: SkiaSceneWebProps) {
  const reduced = useReducedMotion();
  const pet = petOf(doc);
  const motion = PET_PRESET.motion;
  // The emotion track steps halfway through a swipe; the face morphs like the Pet component's.
  const face = useFaceTransition(
    PET_PRESET.poses,
    pet?.emotion ?? NO_PET,
    reduced ? 0 : motion.transition,
    motion.easing,
  );
  // The Pet's pose holds still while the camera moves with the idle clock held; its frame is
  // recomputed only when the pose does.
  const emotion = pet?.emotion;
  const voice = pet?.voice;
  const audio = pet?.audio;
  const clock = pet?.clock;
  const fill = pet && resolveColor(doc.palette, pet.fill);
  const shade = pet && resolveColor(doc.palette, pet.shade);
  const drawScenePet = useMemo(() => {
    if (
      emotion === undefined ||
      voice === undefined ||
      audio === undefined ||
      clock === undefined ||
      !fill ||
      !shade
    )
      return null;
    const cfg: PetConfig = { ...PET_PRESET, emotion, voice, audio };
    const f = petFrame(cfg, { time: clock, face, blink: blinkAt(clock, motion.blinkInterval) });
    return (c: SkCanvas) => drawPet(c, cfg, f, fill, shade);
  }, [emotion, voice, audio, clock, face, fill, shade, motion.blinkInterval]);

  const ref = useRef<HTMLCanvasElement>(null);
  const gpu = useRef<Gpu | null>(null);
  const dpr = pixelRatio();
  const pxW = Math.round(width * dpr);
  const pxH = Math.round(height * dpr);

  // The WebGL context lives as long as the canvas element.
  useLayoutEffect(() => {
    const canvas = ref.current;
    const ck = (globalThis as unknown as { CanvasKit?: CanvasKit }).CanvasKit;
    // No multisampling: Skia antialiases its own paths, closer to the SVG renderer's edges than
    // MSAA (measured), and the context needs no multisampled buffer.
    const handle = canvas && ck ? ck.GetWebGLContext(canvas, { antialias: 0 }) : 0;
    const context = handle && ck ? ck.MakeWebGLContext(handle) : null;
    if (!canvas || !ck || !context) {
      if (handle && ck) ck.deleteContext(handle);
      onLost();
      return;
    }
    gpu.current = { ck, handle, context, surface: null };
    canvas.addEventListener('webglcontextlost', onLost);
    return () => {
      canvas.removeEventListener('webglcontextlost', onLost);
      const g = gpu.current;
      gpu.current = null;
      if (!g) return;
      g.surface?.delete();
      g.context.releaseResourcesAndAbandonContext();
      g.context.delete();
      // Unregistered, CanvasKit's context table would keep the canvas element alive.
      g.ck.deleteContext(g.handle);
      // Released now rather than when the canvas is collected: the browser caps live contexts
      // and loses the oldest one past it, and a lost context sends every scene to SVG.
      const gl = canvas.getContext('webgl2') ?? canvas.getContext('webgl');
      gl?.getExtension('WEBGL_lose_context')?.loseContext();
    };
  }, [onLost]);

  useLayoutEffect(() => {
    const g = gpu.current;
    if (!g) return;
    g.surface?.delete();
    g.surface = g.ck.MakeOnScreenGLSurface(g.context, pxW, pxH, g.ck.ColorSpace.SRGB);
    if (!g.surface) onLost();
  }, [pxW, pxH, onLost]);

  // Every render is a new frame: lay it out (cached pictures, new matrices), record and paint it.
  useLayoutEffect(() => {
    const g = gpu.current;
    if (!g?.surface) return;
    const frame = layoutFrame(doc, width, height);
    const recording = recorder.beginRecording(Skia.XYWHRect(0, 0, width, height));
    replay(recording, frame, drawScenePet);
    const picture = recorder.finishRecordingAsPicture();
    const canvas = g.surface.getCanvas();
    canvas.clear(g.ck.TRANSPARENT);
    canvas.save();
    canvas.scale(pxW / width, pxH / height);
    canvas.drawPicture(ckPicture(picture));
    canvas.restore();
    g.surface.flush();
    picture.dispose();
  });

  return (
    <canvas ref={ref} width={pxW} height={pxH} style={{ width, height, display: 'block' }} />
  );
}
