// The vapor Pet in a box of `width` x `height` showing `viewBox` (Pet units). Web paints a 2D
// canvas (drawPetCanvas2d, the SVG figure call for call); native draws the same frame with Skia
// (PetVaporCanvas.native.tsx). A new frame repaints the canvas straight from the frame store,
// without a React render: the SVG figure's per-frame render held the web chat under 30 fps.
import { useLayoutEffect, useRef } from 'react';

import { drawPetCanvas2d } from './drawPetCanvas2d';
import type { FrameStore } from './frameLoop';
import type { PetConfig } from './petCore';

export interface PetVaporCanvasProps {
  config: PetConfig;
  frames: FrameStore;
  fill: string;
  shade: string;
  prefix: string;
  viewBox: { x: number; y: number; width: number; height: number };
  width: number;
  height: number;
}

/** Sharp on dense screens without painting more than 3x the points. */
const pixelRatio = () =>
  typeof window === 'undefined' ? 1 : Math.min(3, Math.max(1, window.devicePixelRatio || 1));

export function PetVaporCanvas({
  config,
  frames,
  fill,
  shade,
  viewBox: v,
  width,
  height,
}: PetVaporCanvasProps) {
  const ref = useRef<HTMLCanvasElement>(null);
  const dpr = pixelRatio();
  useLayoutEffect(() => {
    const canvas = ref.current;
    const ctx = canvas?.getContext('2d');
    if (!canvas || !ctx) return;
    const k = (width / v.width) * dpr;
    const paint = () => {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.setTransform(k, 0, 0, k, -v.x * k, -v.y * k);
      drawPetCanvas2d(ctx, config, frames.get(), fill, shade);
    };
    paint();
    return frames.subscribe(paint);
  }, [config, frames, fill, shade, v, width, height, dpr]);
  return (
    <canvas
      ref={ref}
      width={Math.round(width * dpr)}
      height={Math.round(height * dpr)}
      style={{ width: '100%', height: '100%', display: 'block' }}
    />
  );
}
