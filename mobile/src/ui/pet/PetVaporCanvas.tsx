// The vapor Pet in a box of `width` x `height` showing `viewBox` (Pet units). Web draws SVG;
// native draws the same frame with Skia (PetVaporCanvas.native.tsx). Both subscribe to the Pet's
// frames, so a new frame re-renders the canvas and nothing above it.
import Svg from 'react-native-svg';

import { useFrame, type FrameStore } from './frameLoop';
import type { PetConfig } from './petCore';
import { PetVaporFigure } from './PetVaporFigure';

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

export function PetVaporCanvas({ viewBox: v, frames, ...figure }: PetVaporCanvasProps) {
  const frame = useFrame(frames);
  return (
    <Svg width="100%" height="100%" viewBox={`${v.x} ${v.y} ${v.width} ${v.height}`}>
      <PetVaporFigure
        config={figure.config}
        frame={frame}
        fill={figure.fill}
        shade={figure.shade}
        prefix={figure.prefix}
      />
    </Svg>
  );
}
