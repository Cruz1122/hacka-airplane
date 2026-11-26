// Trail tokens: flat vector figures in the onboarding style (lit side, lavender-shaded side, soft
// highlight), full body in side view facing right. Forms from the sources below.
// Frailejón: Espeletia — woody trunk, dead-leaf skirt, apical rosette (es.wikipedia.org/wiki/Espeletia).
// Oso: Tremarctos ornatus — large round head, small round ears, short pale muzzle, cream rings
//   around the eyes running down the cheeks (es.wikipedia.org/wiki/Tremarctos_ornatus).
// Puma: Puma concolor — round head, short erect ears dark behind, plain tawny coat, white muzzle and
//   chin, dark whisker pads (es.wikipedia.org/wiki/Puma_concolor).
// Zorro: Lycalopex culpaeus — rufous head, large pointed ears, white muzzle and throat
//   (es.wikipedia.org/wiki/Lycalopex_culpaeus).
// Cóndor: Vultur gryphus — black body, white ruff, silver-white wing patch, bare grey head, male
//   comb, hooked bill (es.wikipedia.org/wiki/Vultur_gryphus).
import Svg, { Circle, Ellipse, G, Path } from 'react-native-svg';

import { resolveColor } from '@/onboarding/scene/doc';
import { frailejonShape } from '@/onboarding/scene/geometry';
import { DEFAULT_PALETTE } from '@/onboarding/scene/preset';
import type { FrailejonBody } from '@/onboarding/scene/types';

import type { StationId } from './stations';

const pal = DEFAULT_PALETTE;
const ink = (token: string) => resolveColor(pal, token);

const FRAILEJON: FrailejonBody = {
  kind: 'frailejon',
  trunkHeight: 36,
  trunkWidth: 8,
  rosetteDiameter: 26,
  leafCount: 28,
  leafLength: 15,
  tilt: -4,
  flowers: 2,
  seed: 1,
  trunk: '$trunk',
  trunkShade: '$trunkShade',
  leaf: '$leaf',
  leafLight: '$leafLight',
  flower: '$bloom',
};

export function TrailMarkFigure({ id }: { id: StationId }) {
  switch (id) {
    case 'brisas':
      return <FrailejonFig />;
    case 'aguacerales':
      return <BearFig />;
    case 'arenales':
      return <PumaFig />;
    case 'valleLunar':
      return <FoxFig />;
    case 'valleTumbas':
      return <CondorFig />;
    default: {
      const _never: never = id;
      throw new Error(`No trail mark for ${_never}`);
    }
  }
}

function FrailejonFig() {
  const shape = frailejonShape(FRAILEJON);
  const b = FRAILEJON;
  return (
    <G>
      {shape.stalks ? (
        <Path
          d={shape.stalks}
          fill="transparent"
          stroke={ink(b.leaf)}
          strokeWidth={1.1}
          strokeLinecap="round"
        />
      ) : null}
      <Path d={shape.trunk} fill={ink(b.trunk)} />
      {shape.trunkDark ? (
        <Path
          d={shape.trunkDark}
          fill="transparent"
          stroke={ink(b.trunkShade)}
          strokeWidth={1.2}
          strokeLinecap="round"
        />
      ) : null}
      <Path d={shape.deadLeaves} fill={ink(b.trunkShade)} opacity={0.9} />
      <Path d={shape.backLeaves} fill={ink(b.leaf)} />
      <Path d={shape.frontLeaves} fill={ink(b.leafLight)} />
      {shape.heads.map((h, i) => (
        <Circle key={`${h.cx},${h.cy},${i}`} cx={h.cx} cy={h.cy} r={h.r} fill={ink(b.flower)} />
      ))}
    </G>
  );
}

/** Pupil with a catch-light, so every face reads alive at icon size. */
function Eye({ cx, cy, r, iris }: { cx: number; cy: number; r: number; iris?: string }) {
  return (
    <G>
      {iris ? <Circle cx={cx} cy={cy} r={r * 1.35} fill={ink(iris)} /> : null}
      <Circle cx={cx} cy={cy} r={r} fill={ink('$ravine')} />
      <Circle cx={cx + r * 0.35} cy={cy - r * 0.35} r={r * 0.35} fill={ink('$snow')} />
    </G>
  );
}

/** A far-side limb: same coat, pushed back into the lavender shade. */
function FarLimb({ d, coat }: { d: string; coat: string }) {
  return (
    <G>
      <Path d={d} fill={ink(coat)} />
      <Path d={d} fill={ink('$ravine')} opacity={0.42} />
    </G>
  );
}

function BearFig() {
  return (
    <G transform="translate(-3 0)">
      <FarLimb d="M -15 -12 L -15 0 L -9.5 0 L -9.5 -12 Z" coat="$furBlack" />
      <FarLimb d="M 3 -12 L 3 0 L 8.5 0 L 8.5 -12 Z" coat="$furBlack" />
      <Circle cx={-21} cy={-21} r={2.6} fill={ink('$furBlack')} />
      <Path
        d="M -21 -18 C -22 -27 -12 -31 -2 -30 C 6 -30 12 -28 15 -24 C 17 -19 15 -12 10 -10 L -16 -10 C -20 -11 -21 -14 -21 -18 Z"
        fill={ink('$furBlack')}
      />
      <Path
        d="M -14 -28 C -8 -30.5 2 -30.5 8 -29 C 2 -27.6 -8 -26.8 -14 -28 Z"
        fill={ink('$furBlackLight')}
      />
      <Path
        d="M -20 -15 C -21 -9 -19.5 -4 -18.5 0 L -11.5 0 C -11.5 -4 -11 -8 -10 -12 Z"
        fill={ink('$furBlack')}
      />
      <Path d="M 7 -15 L 7 0 L 14 0 C 14 -4 13.4 -10 13.4 -17 Z" fill={ink('$furBlack')} />
      <Path
        d="M -19 -16 C -19.6 -10 -18.6 -5 -17.8 -1 M 8.4 -15 L 8.4 -1"
        fill="transparent"
        stroke={ink('$furBlackLight')}
        strokeWidth={1.2}
        strokeLinecap="round"
      />
      <Path
        d="M 11 -26 C 11 -33 18 -35 22 -32 C 25 -30 26 -27 27 -25 C 27 -22 24 -19 20 -19 C 15 -19 11 -21 11 -26 Z"
        fill={ink('$furBlack')}
      />
      <Circle cx={14} cy={-32} r={2.8} fill={ink('$furBlack')} />
      <Circle cx={14} cy={-32} r={1.3} fill={ink('$furBlackLight')} />
      <Path
        d="M 15.6 -30.4 C 19.4 -32.8 24.2 -30.4 27 -25.4 C 27.6 -22.2 24.2 -19.6 20.2 -19.6 C 16.8 -19.6 14.6 -21.6 14.6 -24.8 C 14.6 -27 15 -29 15.6 -30.4 Z"
        fill={ink('$snow')}
      />
      <Ellipse
        cx={19.8}
        cy={-27}
        rx={2.8}
        ry={2.3}
        fill={ink('$furBlack')}
        transform="rotate(-18 19.8 -27)"
      />
      <Circle cx={20} cy={-27.2} r={0.9} fill={ink('$furBlackLight')} />
      <Circle cx={20.3} cy={-27.6} r={0.4} fill={ink('$snow')} />
      <Circle cx={27} cy={-24.6} r={1.4} fill={ink('$furBlack')} />
      <Path
        d="M 26.6 -23.2 Q 25.4 -21.4 23.4 -21.6"
        fill="transparent"
        stroke={ink('$furBlack')}
        strokeWidth={0.8}
        strokeLinecap="round"
      />
    </G>
  );
}

function PumaFig() {
  return (
    <G transform="translate(-2 0)">
      <Path
        d="M -15 -20 C -22 -17 -23 -8 -20 -3 C -18.5 -0.6 -16 -1 -15.5 -3"
        fill="transparent"
        stroke={ink('$pumaGold')}
        strokeWidth={3.2}
        strokeLinecap="round"
      />
      <Path
        d="M -19.4 -1.6 C -17.6 -0.4 -16 -1.2 -15.5 -3"
        fill="transparent"
        stroke={ink('$trunkShade')}
        strokeWidth={3.4}
        strokeLinecap="round"
      />
      <FarLimb d="M -12 -16 L -11 0 L -8 0 L -8 -14 Z" coat="$pumaGold" />
      <FarLimb d="M 7.5 -16 L 8.5 0 L 11.5 0 L 10.5 -16 Z" coat="$pumaGold" />
      <Path
        d="M -16 -17 C -17 -24 -10 -26 -2 -25 C 6 -25 12 -26 15 -23 C 17 -20 16 -15 12 -13 C 4 -11 -8 -11 -13 -12 C -15 -13 -16 -15 -16 -17 Z"
        fill={ink('$pumaGold')}
      />
      <Path
        d="M -12 -12.5 C -6 -11 4 -11 11 -13 C 6 -15 -6 -15 -12 -12.5 Z"
        fill={ink('$sunCore')}
        opacity={0.8}
      />
      <Path
        d="M -16 -17 C -15 -13 -12 -12 -8 -11.5 L 10 -12.5 C 14 -14 16 -17 16 -20 C 8 -15 -6 -14 -16 -17 Z"
        fill={ink('$ravine')}
        opacity={0.26}
      />
      <Path
        d="M -12 -24.5 C -4 -26 6 -26 12 -25.5 C 4 -24.5 -6 -24 -12 -24.5 Z"
        fill={ink('$sunGlow')}
        opacity={0.5}
      />
      <Path
        d="M -16 -18 C -18 -12 -16 -6 -15 -2 L -15 0 L -11 0 L -11 -4 C -9 -8 -8 -12 -9 -16 Z"
        fill={ink('$pumaGold')}
      />
      <Path d="M 10 -18 L 11 0 L 15 0 L 14.5 -3 L 14 -16 Z" fill={ink('$pumaGold')} />
      <Path
        d="M 11 -23 C 14 -27 17 -29 20 -28 L 19 -20 C 16 -19 13 -19 12 -20 Z"
        fill={ink('$pumaGold')}
      />
      <Path d="M 17 -31.5 C 16.5 -35.5 18.5 -36.5 20.5 -34 Z" fill={ink('$pumaGold')} />
      <Path d="M 17.6 -32 C 17.3 -34.6 18.6 -35.2 19.8 -33.8 Z" fill={ink('$trunkShade')} />
      <Path
        d="M 16 -30 C 16 -34 22 -35 24.5 -32 C 25.5 -30.5 26 -29 26 -27.5 C 26 -25.5 23.5 -24 20.5 -24.5 C 17.5 -25 16 -27 16 -30 Z"
        fill={ink('$pumaGold')}
      />
      <Path
        d="M 22.5 -27.5 C 24.5 -28 26 -27.5 26 -26.5 C 25.5 -25 23.5 -24.4 21.5 -25 Z"
        fill={ink('$sunCore')}
      />
      <Path
        d="M 22.8 -29.6 Q 23.4 -28.4 23 -27.5"
        fill="transparent"
        stroke={ink('$trunkShade')}
        strokeWidth={0.7}
        strokeLinecap="round"
      />
      <Circle cx={25.7} cy={-28.4} r={0.85} fill={ink('$ash')} />
      <Ellipse cx={22} cy={-30.2} rx={1.15} ry={0.8} fill={ink('$bloom')} />
      <Ellipse cx={22.1} cy={-30.2} rx={0.35} ry={0.7} fill={ink('$ravine')} />
    </G>
  );
}

function FoxFig() {
  return (
    <G transform="translate(-2 0)">
      <Path
        d="M -11 -17 C -16 -20 -22 -16 -24 -9 C -24 -6 -21 -5 -18 -7 C -15 -9 -12 -12 -11 -13 Z"
        fill={ink('$furGrey')}
      />
      <Path
        d="M -12 -16.5 C -16 -18.6 -20.6 -15.6 -22.6 -10.6 C -19 -14 -15.4 -15.6 -12 -15 Z"
        fill={ink('$furGreyLight')}
      />
      <Path
        d="M -24 -9 C -24 -6 -21 -5 -19 -6.5 C -21 -7.5 -22.5 -9 -23 -11.5 Z"
        fill={ink('$ravine')}
      />
      <FarLimb d="M -9 -13 L -8 0 L -6 0 L -6.5 -13 Z" coat="$furRufous" />
      <FarLimb d="M 7 -13 L 8 0 L 10 0 L 9.5 -13 Z" coat="$furRufous" />
      <Path
        d="M -12 -14 C -13 -20 -6 -22 0 -21.5 C 6 -21 11 -21 13 -18 C 14 -15 12 -12 9 -11.5 C 3 -10.5 -6 -10.5 -10 -11.5 C -11.5 -12 -12 -13 -12 -14 Z"
        fill={ink('$furGrey')}
      />
      <Path
        d="M -12 -14 C -11 -12.4 -8 -11.6 -4 -11.4 L 9 -11.6 C 12 -12.4 13.6 -14.6 13.4 -16.6 C 6 -13.6 -4 -13.2 -12 -14 Z"
        fill={ink('$trunkShade')}
        opacity={0.35}
      />
      <Path
        d="M -8 -11.2 C -2 -10.4 4 -10.4 9 -11.6 C 4 -13 -3 -13 -8 -11.2 Z"
        fill={ink('$snow')}
        opacity={0.9}
      />
      <Path
        d="M -9 -19.8 C -3 -21.4 6 -21.2 11.5 -19.4 C 5 -17.8 -3 -17.8 -9 -19.8 Z"
        fill={ink('$furGreyLight')}
      />
      <Path
        d="M -9.5 -21 C -3 -22.4 5 -22.2 11.5 -20.6"
        fill="transparent"
        stroke={ink('$trunkShade')}
        strokeWidth={1.6}
        strokeLinecap="round"
      />
      <Path
        d="M -12 -15 C -13 -10 -11 -5 -10.5 0 L -8 0 L -8 -5 C -7 -8 -6.5 -11 -7 -13 Z"
        fill={ink('$furRufous')}
      />
      <Path d="M 9 -14 L 10 0 L 12.5 0 L 12 -14 Z" fill={ink('$furRufous')} />
      <Path
        d="M 10 -19 C 12 -22 15 -24 17 -23.5 L 17 -17 C 14.5 -15 12 -14 10.5 -15 Z"
        fill={ink('$furRufous')}
      />
      <Path d="M 15 -21 C 18 -20 18.5 -17 16 -15 C 14 -16 13.5 -19 15 -21 Z" fill={ink('$snow')} />
      <Path d="M 17.5 -27.5 L 19.5 -33.5 L 20.5 -27 Z" fill={ink('$trunkShade')} />
      <Path
        d="M 14 -25 C 14 -28 18 -29 20 -27.5 C 22 -26.5 24.5 -24.5 26 -23 C 25 -22 22 -21.5 19 -21.5 C 16 -21.5 14 -22.5 14 -25 Z"
        fill={ink('$furRufous')}
      />
      <Path d="M 15 -27 L 15.5 -34 L 19 -28 Z" fill={ink('$furRufous')} />
      <Path d="M 15.8 -27.8 L 16 -31.8 L 18 -28.3 Z" fill={ink('$stoneLight')} />
      <Path
        d="M 19 -22 C 22 -22.2 24.5 -22.6 26 -23 C 24 -21.4 21 -21 19 -21.5 Z"
        fill={ink('$snow')}
      />
      <Circle cx={25.8} cy={-23.1} r={0.85} fill={ink('$ravine')} />
      <Ellipse cx={19.6} cy={-25.4} rx={1} ry={0.65} fill={ink('$bloom')} />
      <Ellipse cx={19.7} cy={-25.4} rx={0.32} ry={0.6} fill={ink('$ravine')} />
    </G>
  );
}

function CondorFig() {
  return (
    <G>
      <Path
        d="M -2 0 L -1 -11 M 5 0 L 5 -11 M -5 0 L 1 0 M 2 0 L 8 0"
        fill="transparent"
        stroke={ink('$furGreyLight')}
        strokeWidth={2}
        strokeLinecap="round"
      />
      <Path d="M -12 -14 L -24 -2 L -15 -5 Z" fill={ink('$furBlack')} />
      <Path
        d="M -14 -12 C -18 -26 -10 -36 2 -36 C 10 -36 14 -28 12 -18 C 10 -12 4 -10 -2 -10 C -8 -10 -12 -10 -14 -12 Z"
        fill={ink('$furBlack')}
      />
      <Path
        d="M -17 -14 C -19 -28 -6 -35 7 -31 C 3 -22 -6 -15 -17 -14 Z"
        fill={ink('$furBlackLight')}
      />
      <Path
        d="M -11 -21 C -6 -28 2 -31 7 -31 C 3 -26 -4 -22 -11 -19 Z"
        fill={ink('$snow')}
        opacity={0.82}
      />
      <Path d="M -17 -14 L -21 -10 L -13 -12 Z" fill={ink('$furBlackLight')} />
      <Path d="M 1 -34 C 2 -41 15 -41 15 -34 C 12 -30 4 -30 1 -34 Z" fill={ink('$snow')} />
      <Path
        d="M 9 -38 C 9 -41 10 -43 12 -44"
        fill="transparent"
        stroke={ink('$condorSkin')}
        strokeWidth={3.4}
        strokeLinecap="round"
      />
      <Path
        d="M 10 -42 C 10 -47.5 19 -48.5 20 -43 C 20 -40 15 -39 10 -42 Z"
        fill={ink('$furGrey')}
      />
      <Path
        d="M 10 -42 C 10 -46 12.6 -47.6 15 -47.2 C 13.2 -45.4 12.6 -42.6 13.2 -40.2 C 11.6 -40.2 10.4 -40.8 10 -42 Z"
        fill={ink('$condorSkin')}
      />
      <Path d="M 12 -46 C 12 -50 18 -50.5 18 -46.5 Z" fill={ink('$furBlackLight')} />
      <Path
        d="M 19 -44.5 L 25 -43.5 C 26.4 -42.4 25.6 -40.2 23.4 -40.4 L 19 -41.4 Z"
        fill={ink('$sunCore')}
      />
      <Path
        d="M 24.4 -43.4 C 26.6 -42.4 26.2 -40 24 -39.6"
        fill="transparent"
        stroke={ink('$furGreyLight')}
        strokeWidth={1.2}
        strokeLinecap="round"
      />
      <Eye cx={15.5} cy={-43.6} r={1} />
    </G>
  );
}

/**
 * Each figure's drawn extent in its own units (feet at 0,0, facing right), measured with getBBox
 * in the browser. Redo it when a figure's geometry changes.
 */
export const FIGURE_BOX: Record<StationId, { x: number; y: number; w: number; h: number }> = {
  brisas: { x: -18.3, y: -59.6, w: 31.7, h: 61.8 },
  aguacerales: { x: -26.6, y: -34.8, w: 52, h: 34.8 },
  arenales: { x: -23.6, y: -35.4, w: 48.1, h: 35.4 },
  valleLunar: { x: -26, y: -34, w: 50.7, h: 34 },
  valleTumbas: { x: -24, y: -49.3, w: 49.9, h: 49.3 },
};

export function TrailMarkSvg({
  id,
  width,
  height,
  sink,
  facing = 1,
  tilt = 0,
}: {
  id: StationId;
  width: number;
  height: number;
  sink: { dy: number; sy: number; cx: number; ground: number; scale: number };
  /** 1 draws the figure facing right, -1 mirrors it. */
  facing?: 1 | -1;
  /** Degrees about the feet; negative lifts a right-facing head. */
  tilt?: number;
}) {
  return (
    <Svg width={width} height={height} pointerEvents="none">
      <G
        transform={`translate(${sink.cx} ${sink.ground + sink.dy}) rotate(${tilt}) scale(${sink.scale * facing} ${sink.scale * sink.sy})`}
      >
        <TrailMarkFigure id={id} />
      </G>
    </Svg>
  );
}
