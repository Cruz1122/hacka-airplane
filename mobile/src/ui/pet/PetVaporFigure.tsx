// The Pet drawn as vapor, for scenes where it rises out of the volcano's crater. Its geometry and
// face come from petFrame; the body stays solid and defined, a soft halo of steam-like puffs behind it
// makes the outline billow, and the tail thins into vapor at its tip. No filters, masks or clips
// (they re-rasterize every frame on Android).
import { Circle, Defs, G, LinearGradient, Path, RadialGradient, Stop } from 'react-native-svg';

import type { PetConfig, PetFrame, PetStroke } from './petCore';

export interface PetVaporFigureProps {
  config: PetConfig;
  frame: PetFrame;
  /** Vapor colors: the scene passes its mist colors so the Pet matches the sky's clouds. */
  fill: string;
  shade: string;
  /** Unique per instance: gradient ids share one namespace on web. */
  prefix: string;
}

export function PetVaporFigure({ config, frame: f, fill, shade, prefix }: PetVaporFigureProps) {
  const id = (k: string) => `${prefix}-${k}`;
  const url = (k: string) => `url(#${id(k)})`;
  const b = config.body;
  const headR = (Math.max(b.width * b.scaleX, b.height * b.scaleY) / 2) * 1.25;
  const stroke = (s: PetStroke) => (
    <Path
      d={s.d}
      transform={s.transform}
      stroke={s.color}
      strokeWidth={s.width}
      fill={s.filled ? s.color : 'none'}
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  );
  return (
    <G transform={`translate(${f.shiftX} 0)`}>
      <Defs>
        <RadialGradient id={id('halo')} cx="50%" cy="50%" r="50%">
          <Stop offset="0" stopColor={fill} stopOpacity={0.8} />
          <Stop offset="0.5" stopColor={fill} stopOpacity={0.45} />
          <Stop offset="1" stopColor={fill} stopOpacity={0} />
        </RadialGradient>
        <RadialGradient id={id('halo-shade')} cx="50%" cy="50%" r="50%">
          <Stop offset="0" stopColor={shade} stopOpacity={0.4} />
          <Stop offset="1" stopColor={shade} stopOpacity={0} />
        </RadialGradient>
        {/* Solid head; only the end of the tail thins out, where it leaves the crater. */}
        <LinearGradient id={id('core')} x1="0" y1="0" x2="0" y2="1">
          <Stop offset="0" stopColor={fill} stopOpacity={1} />
          <Stop offset="0.66" stopColor={fill} stopOpacity={0.97} />
          <Stop offset="1" stopColor={fill} stopOpacity={0} />
        </LinearGradient>
        {/* Shading ring around the head, lit from the upper left. It returns to transparent past
            the head, so the tail (which the core already fades) gets no tint. */}
        <RadialGradient
          id={id('form')}
          gradientUnits="userSpaceOnUse"
          // Follows the head when it turns (lit from the upper left, then the upper right).
          cx={f.headX - 10 * (1 - 2 * f.turn)}
          cy={b.y - 14}
          r={headR}
        >
          <Stop offset="0" stopColor={shade} stopOpacity={0} />
          <Stop offset="0.6" stopColor={shade} stopOpacity={0} />
          <Stop offset="0.86" stopColor={shade} stopOpacity={0.42} />
          <Stop offset="1" stopColor={shade} stopOpacity={0} />
        </RadialGradient>
        <RadialGradient id={id('highlight')}>
          <Stop offset="0" stopColor="#ffffff" stopOpacity={0.85} />
          <Stop offset="1" stopColor="#ffffff" stopOpacity={0} />
        </RadialGradient>
      </Defs>
      <G transform={`translate(0 ${f.float})`}>
        <G transform={f.bodyTransform}>
          {/* Halo behind the body: light first, then the shade offset down-right, so each edge of
              the halo matches the edge of the body it extends. */}
          {f.vapor.map((p, i) => (
            <Circle
              key={`f${i}`}
              cx={p.x}
              cy={p.y}
              r={p.r}
              fill={url('halo')}
              opacity={p.opacity}
            />
          ))}
          {f.vapor.map((p, i) => (
            <Circle
              key={`s${i}`}
              cx={p.x + p.r * 0.2 * (1 - 2 * f.turn)}
              cy={p.y + p.r * 0.25}
              r={p.r}
              fill={url('halo-shade')}
              opacity={p.opacity}
            />
          ))}
          <Path d={f.body} fill={url('core')} />
          <Path d={f.body} fill={url('form')} />
          <Path d={f.volume} fill={url('highlight')} opacity={f.volumeOpacity} />
        </G>
        <G transform={f.features}>
          <G transform={f.eyes}>
            {stroke(f.leftEye)}
            {stroke(f.rightEye)}
          </G>
          {stroke(f.mouth)}
        </G>
        {f.accessory && (
          <G transform={f.accessory.transform}>
            {f.accessory.shapes.map((a) => (
              <Path key={a.d} d={a.d} fill={a.fill} fillOpacity={a.opacity ?? 1} />
            ))}
          </G>
        )}
      </G>
    </G>
  );
}
