// Trail tokens: flat vector figures in the onboarding style (lit side, lavender-shaded side, soft
// highlight), standing on the ground at 0,0. Brisas, which the guion gives no icon, draws a windsock for
// its name and the wind at the park's entrance; the other stops draw the node icons of the UTON guion
// (Guion ecoturístico zona norte, 2024, "Los Nodos del Diagrama"): Aguacerales, a water drop over a frailejón; Arenales, an hourglass; Valle Lunar, a fractured rock
// with a geologist's hammer; Valle de las Tumbas, an indigenous pictogram and a volcanic warning
// triangle. Frailejón: Espeletia, woody trunk, dead-leaf skirt, apical rosette
// (es.wikipedia.org/wiki/Espeletia).
import Svg, { Circle, G, Path } from 'react-native-svg';

import { resolveColor } from '@/onboarding/scene/doc';
import { frailejonShape } from '@/onboarding/scene/geometry';
import { DEFAULT_PALETTE } from '@/onboarding/scene/preset';
import type { FrailejonBody } from '@/onboarding/scene/types';

import type { StationId } from './stations';

const pal = DEFAULT_PALETTE;
const ink = (token: string) => resolveColor(pal, token);

/** Aguacerales' frailejón: short and flowerless, so the drop above it carries the icon. */
const SMALL_FRAILEJON: FrailejonBody = {
  kind: 'frailejon',
  trunkHeight: 18,
  trunkWidth: 8,
  rosetteDiameter: 24,
  leafCount: 26,
  leafLength: 13,
  tilt: 3,
  flowers: 0,
  seed: 3,
  trunk: '$trunk',
  trunkShade: '$trunkShade',
  leaf: '$leaf',
  leafLight: '$leafLight',
  flower: '$bloom',
};

export function TrailMarkFigure({ id }: { id: StationId }) {
  switch (id) {
    case 'brisas':
      return <WindsockFig />;
    case 'aguacerales':
      return <DropFig />;
    case 'arenales':
      return <HourglassFig />;
    case 'valleLunar':
      return <RockHammerFig />;
    case 'valleTumbas':
      return <PictogramWarningFig />;
    default: {
      const _never: never = id;
      throw new Error(`No trail mark for ${_never}`);
    }
  }
}

function FrailejonFig({ body: b }: { body: FrailejonBody }) {
  const shape = frailejonShape(b);
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

/** Génesis hídrica: a drop of the fog the páramo catches, hanging over a frailejón. */
function DropFig() {
  return (
    <G>
      <FrailejonFig body={SMALL_FRAILEJON} />
      <G transform="translate(1 -44)">
        <Path
          d="M 0 -19 C 2.5 -14 8.5 -8 8.5 -2 A 8.5 8.5 0 0 1 -8.5 -2 C -8.5 -8 -2.5 -14 0 -19 Z"
          fill={ink('$ice')}
        />
        <Path
          d="M 8.5 -2 A 8.5 8.5 0 0 1 -1 6.4 C 4 4.6 6.6 1 6.8 -4.6 C 7.8 -3.8 8.5 -3 8.5 -2 Z"
          fill={ink('$skyMid')}
        />
        <Path
          d="M -3.2 -10.5 C -5 -7.6 -6 -5 -6 -2.4 C -6 0.4 -4.8 2.4 -3 3.4 C -4.2 0.6 -4.4 -4 -3.2 -10.5 Z"
          fill={ink('$cloud')}
        />
        <Circle cx={-3.4} cy={-12.6} r={0.9} fill={ink('$snow')} />
      </G>
    </G>
  );
}

/** La puerta de entrada: a striped windsock filled by the breeze the station is named for. */
function WindsockFig() {
  return (
    <G>
      <Path
        d="M -17 0 C -16 -3 -13 -4.4 -10.4 -4.4 C -7.8 -4.4 -4.8 -3 -3.8 0 Z"
        fill={ink('$stone')}
      />
      <Path d="M -11.2 -57 L -10.4 -57 L -10.4 -3.6 L -11.2 -3.6 Z" fill={ink('$stoneLight')} />
      <Path d="M -10.4 -57 L -9.6 -57 L -9.6 -3.6 L -10.4 -3.6 Z" fill={ink('$stoneShade')} />
      <Circle cx={-10.4} cy={-57.6} r={1.6} fill={ink('$stoneShade')} />
      <Path d="M -8.8 -54 L -2.1 -52.6 L -2.1 -43.1 L -8.8 -43 Z" fill={ink('$furRufous')} />
      <Path d="M -2.1 -52.6 L 4.6 -51.3 L 4.6 -43.3 L -2.1 -43.1 Z" fill={ink('$snow')} />
      <Path d="M 4.6 -51.3 L 11.3 -49.9 L 11.3 -43.4 L 4.6 -43.3 Z" fill={ink('$furRufous')} />
      <Path
        d="M 11.3 -49.9 L 17.4 -48.6 Q 18.6 -48.4 18.6 -47.2 L 18.6 -44.8 Q 18.6 -43.5 17.4 -43.5 L 11.3 -43.4 Z"
        fill={ink('$snow')}
      />
      <Path
        d="M -8.8 -46.3 L 18.6 -45 L 18.6 -44.8 Q 18.6 -43.5 17.4 -43.5 L -8.8 -43 Z"
        fill={ink('$ravine')}
        opacity={0.2}
      />
      <Path d="M -9.6 -54.4 L -8.2 -54.4 L -8.2 -42.6 L -9.6 -42.6 Z" fill={ink('$stoneShade')} />
      <Path
        d="M 2 -36 C 8 -37.5 13 -34.5 19 -36 M -4 -29 C 3 -30.5 8 -27.5 14 -29"
        fill="transparent"
        stroke={ink('$snow')}
        strokeWidth={1.3}
        strokeLinecap="round"
        opacity={0.85}
      />
    </G>
  );
}

/** Memoria y cambio climático: an hourglass of volcanic sand running out. */
function HourglassFig() {
  return (
    <G>
      <Path
        d="M -7.5 -40 L 7.5 -40 C 7.5 -31 1.7 -26 1.3 -22 C 1.7 -18 7.5 -13 7.5 -4 L -7.5 -4 C -7.5 -13 -1.7 -18 -1.3 -22 C -1.7 -26 -7.5 -31 -7.5 -40 Z"
        fill={ink('$ice')}
      />
      <Path
        d="M -5.9 -31 L 5.9 -31 C 4.3 -27.5 1.6 -25 1.3 -22.4 L -1.3 -22.4 C -1.6 -25 -4.3 -27.5 -5.9 -31 Z"
        fill={ink('$ash')}
      />
      <Path
        d="M 0 -22.4 L 0 -10"
        fill="transparent"
        stroke={ink('$ash')}
        strokeWidth={1}
        strokeLinecap="round"
      />
      <Path d="M -7.4 -4 C -6 -8 -2.6 -10.4 0 -10.4 C 2.6 -10.4 6 -8 7.4 -4 Z" fill={ink('$ash')} />
      <Path
        d="M -5.4 -4 C -4.4 -6.8 -2.4 -8.8 -0.6 -9.6 C -1.8 -7.4 -2.4 -5.8 -2.6 -4 Z"
        fill={ink('$stoneLight')}
      />
      <Path
        d="M -5.2 -38 C -5.2 -34 -3.6 -31 -2 -28.6 M -5.2 -6.2 C -5 -9.6 -3.8 -12.6 -2.4 -15"
        fill="transparent"
        stroke={ink('$snow')}
        strokeWidth={1.1}
        strokeLinecap="round"
        opacity={0.85}
      />
      <Path d="M -10.4 -40 L -8 -40 L -8 -4 L -10.4 -4 Z" fill={ink('$trunk')} />
      <Path d="M 8 -40 L 10.4 -40 L 10.4 -4 L 8 -4 Z" fill={ink('$trunkShade')} />
      <Path
        d="M -11 -44.5 L 11 -44.5 Q 12.5 -44.5 12.5 -43 L 12.5 -41.5 Q 12.5 -40 11 -40 L -11 -40 Q -12.5 -40 -12.5 -41.5 L -12.5 -43 Q -12.5 -44.5 -11 -44.5 Z"
        fill={ink('$trunk')}
      />
      <Path
        d="M -11 -4.5 L 11 -4.5 Q 12.5 -4.5 12.5 -3 L 12.5 -1.5 Q 12.5 0 11 0 L -11 0 Q -12.5 0 -12.5 -1.5 L -12.5 -3 Q -12.5 -4.5 -11 -4.5 Z"
        fill={ink('$trunk')}
      />
      <Path
        d="M -12.5 -1.6 Q -12.5 0 -11 0 L 11 0 Q 12.5 0 12.5 -1.6 Z"
        fill={ink('$trunkShade')}
      />
      <Path
        d="M -12.5 -41.6 Q -12.5 -40 -11 -40 L 11 -40 Q 12.5 -40 12.5 -41.6 Z"
        fill={ink('$trunkShade')}
      />
    </G>
  );
}

/** Fuerzas geológicas: a boulder split by frost, rusted where its iron oxidised, and the hammer. */
function RockHammerFig() {
  return (
    <G>
      <Path
        d="M -23 0 L -21 -14 L -14 -22 L -3 -24.5 L -0.5 -17 L -3.5 -10 L -1.5 0 Z"
        fill={ink('$rock')}
      />
      <Path d="M -21 -14 L -14 -22 L -3 -24.5 L -6 -18 L -13 -15.5 Z" fill={ink('$stone')} />
      {/* Rust: the palette's rufous, for the iron that oxidises in the andesite. */}
      <Path
        d="M -20.5 -9 C -16 -11.5 -11 -10.5 -6 -12 C -7 -9.5 -10 -7.6 -14 -7.4 C -16.5 -7.2 -18.6 -6.6 -21 -5 Z"
        fill={ink('$furRufous')}
        opacity={0.85}
      />
      <Path
        d="M 1.5 0 L 0.5 -9 L 3 -16.5 L 1 -23.5 L 10 -21.5 L 17.5 -12 L 20 0 Z"
        fill={ink('$rockShade')}
      />
      <Path d="M 1 -23.5 L 10 -21.5 L 17.5 -12 L 9 -13.5 L 3 -16.5 Z" fill={ink('$rock')} />
      <Path
        d="M -1.5 0 L -3.5 -10 L -0.5 -17 L -3 -24.5 M 1.5 0 L 0.5 -9 L 3 -16.5 L 1 -23.5"
        fill="transparent"
        stroke={ink('$ravine')}
        strokeWidth={1.4}
        strokeLinejoin="round"
      />
      <G transform="translate(6 -31) rotate(-40)">
        <Path
          d="M 0.4 1.4 L 3 1.4 L 3 23 Q 3 24.4 1.7 24.4 Q 0.4 24.4 0.4 23 Z"
          fill={ink('$paramo')}
        />
        <Path d="M 1.9 1.4 L 3 1.4 L 3 23 Q 3 24.4 1.9 24.4 Z" fill={ink('$trunk')} />
        <Path
          d="M 0.4 15 L 3 15 L 3 23 Q 3 24.4 1.7 24.4 Q 0.4 24.4 0.4 23 Z"
          fill={ink('$ravine')}
        />
        <Path
          d="M -9.5 1.2 C -6 -0.6 -3 -1.8 -0.5 -2 L 6 -2 Q 7 -2 7 -1 L 7 1 Q 7 2 6 2 L -0.5 2 C -3.4 2 -6.4 1.8 -9.5 1.2 Z"
          fill={ink('$stoneShade')}
        />
        <Path
          d="M -6.5 -0.2 C -4 -1.2 -2 -1.6 0 -1.6 L 6 -1.6 L 6 -0.4 L -0.5 -0.4 Z"
          fill={ink('$stoneLight')}
        />
      </G>
    </G>
  );
}

/** Respeto y riesgo: a standing slab with a painted spiral, and the volcanic warning sign. */
function PictogramWarningFig() {
  return (
    <G>
      <Path
        d="M -24.5 0 L -24 -27 C -24 -30.5 -21 -32.5 -17.5 -32 L -10.5 -31 C -8.6 -30.6 -8 -29.4 -8 -27.5 L -8 0 Z"
        fill={ink('$stone')}
      />
      <Path
        d="M -11 -30.6 L -10.5 -31 C -8.6 -30.6 -8 -29.4 -8 -27.5 L -8 0 L -11 0 Z"
        fill={ink('$stoneShade')}
      />
      {/* A spiral of half-turns that widen by 2.5 units, so its lines stay apart at icon size. */}
      <Path
        d="M -17.5 -17 A 1.25 1.25 0 0 1 -15 -17 A 2.5 2.5 0 0 1 -20 -17 A 3.75 3.75 0 0 1 -12.5 -17 A 5 5 0 0 1 -22.5 -17"
        fill="transparent"
        stroke={ink('$snow')}
        strokeWidth={1.4}
        strokeLinecap="round"
      />
      <Path d="M 8.3 -12 L 10.7 -12 L 10.7 0 L 8.3 0 Z" fill={ink('$ravine')} />
      <Path
        d="M 9.5 -40 L 23.5 -13 L -4.5 -13 Z"
        fill={ink('$bloom')}
        stroke={ink('$ravine')}
        strokeWidth={2.6}
        strokeLinejoin="round"
      />
      <Path d="M 2 -16.5 L 6.6 -24.5 L 12.4 -24.5 L 17 -16.5 Z" fill={ink('$ravine')} />
      <Circle cx={9.5} cy={-27.6} r={1.7} fill={ink('$ravine')} />
      <Circle cx={11.2} cy={-30.6} r={1.2} fill={ink('$ravine')} />
    </G>
  );
}

/**
 * Each figure's drawn extent in its own units (feet at 0,0), measured with getBBox in the browser.
 * Redo it when a figure's geometry changes.
 */
export const FIGURE_BOX: Record<StationId, { x: number; y: number; w: number; h: number }> = {
  brisas: { x: -17, y: -59.2, w: 36, h: 59.2 },
  aguacerales: { x: -12.7, y: -63, w: 28, h: 65 },
  arenales: { x: -12.5, y: -44.5, w: 25, h: 44.5 },
  valleLunar: { x: -23, y: -37, w: 50, h: 37 },
  valleTumbas: { x: -24.5, y: -40, w: 48, h: 40 },
};

export function TrailMarkSvg({
  id,
  width,
  height,
  cx,
  ground,
  scale,
}: {
  id: StationId;
  width: number;
  height: number;
  /** Where the figure's 0,0 (its feet) lands, and its units per point. */
  cx: number;
  ground: number;
  scale: number;
}) {
  return (
    <Svg width={width} height={height} pointerEvents="none">
      <G transform={`translate(${cx} ${ground}) scale(${scale})`}>
        <TrailMarkFigure id={id} />
      </G>
    </Svg>
  );
}
