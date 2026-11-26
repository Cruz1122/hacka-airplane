// One frame of the Pet as react-native-svg elements, in the upstream viewBox coordinates
// (PET_VIEWBOX). Used inside a standalone <Pet> and inside the onboarding scene.
import {
  ClipPath,
  Defs,
  Ellipse,
  FeGaussianBlur,
  Filter,
  G,
  LinearGradient,
  Mask,
  Path,
  RadialGradient,
  Rect,
  Stop,
} from 'react-native-svg';

import type { PetConfig, PetFrame, PetStroke } from './petCore';

const safe = (s: string) => (/^#[0-9a-fA-F]{6}$/.test(s) ? s : '#ffffff');

export interface PetFigureProps {
  config: PetConfig;
  frame: PetFrame;
  /** Unique per instance: gradient, mask and filter ids share one namespace on web. */
  prefix: string;
}

export function PetFigure({ config: c, frame: f, prefix }: PetFigureProps) {
  const id = (k: string) => `${prefix}-${k}`;
  const url = (k: string) => `url(#${id(k)})`;
  const smoke = (front: boolean) =>
    f.smoke.map((s, i) =>
      s.front === front ? (
        <Path
          key={i}
          d={s.d}
          fill="none"
          stroke={url('smoke')}
          strokeWidth={s.width}
          strokeLinecap="round"
          opacity={c.smoke.opacity}
        />
      ) : null,
    );
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
    <G>
      <Defs>
        <RadialGradient id={id('body')} cx="34%" cy="22%" r="84%">
          <Stop offset="0" stopColor={safe(c.body.highlightColor)} />
          <Stop offset="0.48" stopColor={safe(c.body.color)} />
          <Stop offset="0.78" stopColor="#edf5ff" />
          <Stop offset="1" stopColor={safe(c.body.shadowColor)} stopOpacity={0.45} />
        </RadialGradient>
        <LinearGradient id={id('fade')} x1="0" y1="0" x2="0" y2="1">
          <Stop offset="0" stopColor="white" />
          <Stop offset="0.62" stopColor="white" />
          <Stop offset="1" stopColor="black" />
        </LinearGradient>
        <Mask id={id('tail')} maskUnits="userSpaceOnUse" x={-200} y={-175} width={400} height={410}>
          <Rect x={-200} y={-175} width={400} height={410} fill={url('fade')} />
        </Mask>
        <RadialGradient id={id('highlight')}>
          <Stop offset="0" stopColor="#ffffff" stopOpacity={0.85} />
          <Stop offset="1" stopColor="#ffffff" stopOpacity={0} />
        </RadialGradient>
        <LinearGradient id={id('smoke')}>
          <Stop offset="0" stopColor="#e6ecff" stopOpacity={0.18} />
          <Stop offset="0.5" stopColor="#d3dfff" stopOpacity={0.7} />
          <Stop offset="1" stopColor="#ffffff" stopOpacity={0.03} />
        </LinearGradient>
        <ClipPath id={id('clip')}>
          <Path d={f.body} />
        </ClipPath>
        <Filter id={id('mist')} x="-32%" y="-32%" width="164%" height="164%">
          <FeGaussianBlur stdDeviation={f.mist} />
        </Filter>
        <Filter id={id('soft')} x="-15%" y="-15%" width="130%" height="130%">
          <FeGaussianBlur stdDeviation={f.soft} />
        </Filter>
      </Defs>
      <G transform={`translate(0 ${f.float})`}>
        <G filter={url('mist')}>{smoke(false)}</G>
        <G transform={f.bodyTransform}>
          <Path d={f.body} fill="#c8ddff" opacity={0.15} filter={url('soft')} mask={url('tail')} />
          <Path
            d={f.body}
            fill="none"
            stroke={safe(c.body.shadowColor)}
            strokeWidth={2.6}
            opacity={c.body.outline}
            mask={url('tail')}
          />
          <Path d={f.body} fill={url('body')} mask={url('tail')} opacity={c.body.opacity} />
          <Path
            d={f.volume}
            fill={url('highlight')}
            opacity={f.volumeOpacity}
            filter={url('soft')}
            mask={url('tail')}
          />
          <G mask={url('tail')} clipPath={url('clip')}>
            <Ellipse
              cx={f.vaporShadow.cx}
              cy={f.vaporShadow.cy}
              rx={34}
              ry={48}
              fill={safe(c.body.shadowColor)}
              opacity={f.vaporShadow.opacity}
              filter={url('soft')}
            />
            <Ellipse
              cx={f.vaporLight.cx}
              cy={f.vaporLight.cy}
              rx={40}
              ry={32}
              fill="#ffffff"
              opacity={f.vaporLight.opacity}
              filter={url('soft')}
            />
          </G>
          <Ellipse
            cx={f.shade.cx}
            cy={f.shade.cy}
            rx={53}
            ry={71}
            fill={safe(c.body.shadowColor)}
            opacity={0.075}
            filter={url('soft')}
          />
        </G>
        <G filter={url('mist')}>{smoke(true)}</G>
        <G transform={f.features}>
          <G transform={f.eyes}>
            {stroke(f.leftEye)}
            {stroke(f.rightEye)}
          </G>
          {stroke(f.mouth)}
        </G>
      </G>
    </G>
  );
}
