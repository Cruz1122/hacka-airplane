// The setting behind each stop's icon, inside its circle: a flat sky, one far landform and the
// ground the figure stands on, in the scene palette (the onboarding art's colors). Each one is the
// stop's landscape: páramo hills at Brisas, the wet páramo and its ponds at Aguacerales, the ash
// plain under the Nevado del Ruiz at Arenales, the grey field of angular, frost-split rock of the
// Valle Lunar, and the jagged ridges and fallen blocks of the Valle de las Tumbas.
import Svg, { Ellipse, Path, Rect } from 'react-native-svg';

import { DEFAULT_PALETTE } from '@/onboarding/scene/preset';

import type { StationId } from './stations';

const p = DEFAULT_PALETTE;

type Far = 'hills' | 'volcano' | 'peaks' | 'ridge';
type Detail = 'tufts' | 'pond' | 'stones' | 'blocks';

const SCENES: Record<
  StationId,
  { sky: string; far: Far; farColor: string; ground: string; detail: Detail; detailColor: string }
> = {
  brisas: {
    sky: p.skyMid,
    far: 'hills',
    farColor: p.hillFar,
    ground: p.grassDark,
    detail: 'tufts',
    detailColor: p.paramo,
  },
  aguacerales: {
    sky: p.skyTop,
    far: 'hills',
    farColor: p.hillMid,
    ground: p.paramo,
    detail: 'pond',
    detailColor: p.ice,
  },
  arenales: {
    sky: p.skyHorizon,
    far: 'volcano',
    farColor: p.midTop,
    ground: p.ash,
    detail: 'stones',
    detailColor: p.stoneShade,
  },
  valleLunar: {
    sky: p.cloudShade,
    far: 'ridge',
    farColor: p.rockShade,
    ground: p.stoneLight,
    detail: 'blocks',
    detailColor: p.stone,
  },
  valleTumbas: {
    sky: p.sunGlow,
    far: 'peaks',
    farColor: p.midShade,
    ground: p.rock,
    detail: 'blocks',
    detailColor: p.rockShade,
  },
};

/** The stop's sky color, for its pulse. */
export function sceneSky(id: StationId): string {
  return SCENES[id].sky;
}

/** The far landform, on the horizon at `g` in a `s`-wide square. */
function farPath(far: Far, s: number, g: number): string {
  switch (far) {
    case 'hills':
      return `M 0 ${g} L 0 ${g - s * 0.16} Q ${s * 0.25} ${g - s * 0.3} ${s * 0.5} ${g - s * 0.14} T ${s} ${g - s * 0.2} L ${s} ${g} Z`;
    case 'volcano':
      return `M ${-s * 0.1} ${g} L ${s * 0.36} ${g - s * 0.42} L ${s * 0.58} ${g - s * 0.42} L ${s * 1.1} ${g} Z`;
    case 'peaks':
      return `M 0 ${g} L 0 ${g - s * 0.18} L ${s * 0.16} ${g - s * 0.36} L ${s * 0.3} ${g - s * 0.22} L ${s * 0.52} ${g - s * 0.48} L ${s * 0.74} ${g - s * 0.24} L ${s * 0.88} ${g - s * 0.34} L ${s} ${g - s * 0.2} L ${s} ${g} Z`;
    case 'ridge':
      return `M 0 ${g} L 0 ${g - s * 0.14} Q ${s * 0.3} ${g - s * 0.22} ${s * 0.52} ${g - s * 0.17} Q ${s * 0.76} ${g - s * 0.12} ${s} ${g - s * 0.24} L ${s} ${g} Z`;
  }
}

/** Snow on the volcano's summit, matching farPath('volcano'). */
function snowCap(s: number, g: number): string {
  const top = g - s * 0.42;
  return `M ${s * 0.27} ${top + s * 0.08} L ${s * 0.36} ${top} L ${s * 0.58} ${top} L ${s * 0.68} ${top + s * 0.09} Q ${s * 0.6} ${top + s * 0.13} ${s * 0.52} ${top + s * 0.07} Q ${s * 0.42} ${top + s * 0.14} ${s * 0.27} ${top + s * 0.08} Z`;
}

function DetailShapes({
  detail,
  color,
  s,
  g,
}: {
  detail: Detail;
  color: string;
  s: number;
  g: number;
}) {
  switch (detail) {
    case 'tufts':
      return [0.14, 0.8, 0.9].map((x, i) => (
        <Ellipse
          key={i}
          cx={s * x}
          cy={g + s * (0.06 + i * 0.04)}
          rx={s * 0.06}
          ry={s * 0.022}
          fill={color}
        />
      ));
    case 'pond':
      return <Ellipse cx={s * 0.2} cy={g + s * 0.08} rx={s * 0.17} ry={s * 0.035} fill={color} />;
    case 'stones':
      return [
        [0.16, 0.08, 0.035],
        [0.84, 0.12, 0.028],
      ].map(([x, y, r], i) => (
        <Ellipse key={i} cx={s * x!} cy={g + s * y!} rx={s * r!} ry={s * r! * 0.6} fill={color} />
      ));
    case 'blocks':
      return [
        [0.1, 0.06, 0.09],
        [0.8, 0.09, 0.11],
      ].map(([x, y, w], i) => (
        <Path
          key={i}
          d={`M ${s * x!} ${g + s * y!} L ${s * (x! + w! * 0.2)} ${g + s * (y! - w! * 0.7)} L ${s * (x! + w!)} ${g + s * (y! - w! * 0.55)} L ${s * (x! + w! * 1.1)} ${g + s * y!} Z`}
          fill={color}
        />
      ));
  }
}

/**
 * The stop's setting in a `size` square, its ground at `ground` (where the icon stands).
 * A wider `width` stretches the landscape sideways; the flat shapes take it, the icon is drawn apart.
 */
export function StationScene({
  id,
  size: s,
  ground: g,
  width = s,
}: {
  id: StationId;
  size: number;
  ground: number;
  width?: number;
}) {
  const scene = SCENES[id];
  const horizon = g - s * 0.04;
  return (
    <Svg
      width={width}
      height={s}
      viewBox={`0 0 ${s} ${s}`}
      preserveAspectRatio="none"
      style={{ position: 'absolute' }}
      pointerEvents="none"
    >
      <Rect width={s} height={s} fill={scene.sky} />
      <Path d={farPath(scene.far, s, horizon)} fill={scene.farColor} />
      {scene.far === 'volcano' ? <Path d={snowCap(s, horizon)} fill={p.snow} /> : null}
      <Path
        d={`M 0 ${horizon} Q ${s * 0.5} ${g - s * 0.08} ${s} ${horizon} L ${s} ${s} L 0 ${s} Z`}
        fill={scene.ground}
      />
      <DetailShapes detail={scene.detail} color={scene.detailColor} s={s} g={g} />
    </Svg>
  );
}
