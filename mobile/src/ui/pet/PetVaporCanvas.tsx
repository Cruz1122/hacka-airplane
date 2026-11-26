// The vapor Pet in a box of `width` x `height` showing `viewBox` (Pet units). Web draws SVG;
// native draws the same frame with Skia (PetVaporCanvas.native.tsx).
import Svg from 'react-native-svg';

import type { PetConfig, PetFrame } from './petCore';
import { PetVaporFigure } from './PetVaporFigure';

export interface PetVaporCanvasProps {
  config: PetConfig;
  frame: PetFrame;
  fill: string;
  shade: string;
  prefix: string;
  viewBox: { x: number; y: number; width: number; height: number };
  width: number;
  height: number;
}

export function PetVaporCanvas({ viewBox: v, ...figure }: PetVaporCanvasProps) {
  return (
    <Svg width="100%" height="100%" viewBox={`${v.x} ${v.y} ${v.width} ${v.height}`}>
      <PetVaporFigure
        config={figure.config}
        frame={figure.frame}
        fill={figure.fill}
        shade={figure.shade}
        prefix={figure.prefix}
      />
    </Svg>
  );
}
