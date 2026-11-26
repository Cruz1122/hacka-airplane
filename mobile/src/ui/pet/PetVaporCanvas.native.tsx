// Native vapor Pet on Skia: react-native-svg redraws an animated Pet into a CPU bitmap every
// frame on Android (~48 ms per frame on the debug build of the reference phone), Skia draws it on
// the GPU from the same PetFrame.
import { Canvas, Picture, Skia } from '@shopify/react-native-skia';
import { useMemo } from 'react';

import { drawPet } from './drawPet';
import type { PetVaporCanvasProps } from './PetVaporCanvas';

export function PetVaporCanvas({
  config,
  frame,
  fill,
  shade,
  viewBox: v,
  width,
  height,
}: PetVaporCanvasProps) {
  const picture = useMemo(() => {
    const recorder = Skia.PictureRecorder();
    const canvas = recorder.beginRecording(Skia.XYWHRect(0, 0, width, height));
    // viewBox with the box's own aspect ratio (Pet sizes its view by it): uniform scale.
    const k = width / v.width;
    canvas.scale(k, k);
    canvas.translate(-v.x, -v.y);
    drawPet(canvas, config, frame, fill, shade);
    return recorder.finishRecordingAsPicture();
  }, [config, frame, fill, shade, v, width, height]);
  return (
    <Canvas style={{ width, height }}>
      <Picture picture={picture} />
    </Canvas>
  );
}
