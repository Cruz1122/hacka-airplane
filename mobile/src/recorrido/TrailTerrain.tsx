// The traced terrain under the trail: six chunks (trailMap.generated.ts), each its own Svg, laid
// out in the map's 2x3 grid. Colors are the scene palette's: paramo greens from its grass, ash and
// rock in the chat header's earth (trunk greyed with stone, washed toward the horizon), the
// ash-covered glacier in the lavender of its snow shadows.
import { memo } from 'react';
import { StyleSheet, View } from 'react-native';
import Svg, { G, Path, Rect } from 'react-native-svg';

import { DEFAULT_PALETTE } from '@/onboarding/scene/preset';

import { TRAIL_CLASSES, TRAIL_MAP } from './trailMap.generated';

type TerrainClass = (typeof TRAIL_CLASSES)[number];

/** RGB blend of two '#rrggbb' colors, `t` of the way from `a` to `b`. */
function mix(a: string, b: string, t: number): string {
  const [ca, cb] = [a, b].map((c) => parseInt(c.slice(1), 16));
  const channel = (shift: number) => {
    const x = (ca >> shift) & 255;
    return Math.round(x + (((cb >> shift) & 255) - x) * t);
  };
  return `#${[16, 8, 0].map((s) => channel(s).toString(16).padStart(2, '0')).join('')}`;
}

function terrainColors(p: Record<string, string>): Record<TerrainClass, string> {
  const earth = mix(p.trunk, p.stone, 0.3);
  const earthShade = mix(p.trunkShade, p.stoneShade, 0.3);
  return {
    rock: mix(earth, p.skyHorizon, 0.22),
    ash: mix(earth, p.skyHorizon, 0.5),
    ashPale: mix(p.stoneLight, p.mist, 0.35),
    // Shades stay close to their base so the map reads as terrain, not camouflage.
    rockDark: mix(earthShade, earth, 0.62),
    paramoDry: mix(p.paramo, p.hillFar, 0.3),
    paramo: mix(p.grassDark, p.paramo, 0.35),
    paramoDark: mix(p.grassDark, p.trunkShade, 0.2),
    ravine: mix(earthShade, earth, 0.4),
  };
}

const COLORS = terrainColors(DEFAULT_PALETTE);
const FILLS = TRAIL_CLASSES.map((c) => COLORS[c]);
/** The terrain's base color, for screen edges a narrowed map leaves uncovered. */
export const TRAIL_BASE_COLOR = FILLS[0];

const Chunk = memo(function Chunk({ index, size }: { index: number; size: number }) {
  const u = TRAIL_MAP.size;
  // Whole pixels plus 1 of overlap: at fractional sizes adjacent Svgs leave a hairline between them.
  const side = Math.ceil(size) + 1;
  // South-up: each chunk turns inside its own Svg and takes the mirrored grid cell. Turning the
  // whole map instead moves the chunks by fractions of a pixel and the hairlines come back.
  const col = TRAIL_MAP.cols - 1 - (index % TRAIL_MAP.cols);
  const row = TRAIL_MAP.rows - 1 - Math.floor(index / TRAIL_MAP.cols);
  return (
    <Svg
      width={side}
      height={side}
      viewBox={`0 0 ${u} ${u}`}
      style={{ position: 'absolute', left: Math.floor(col * size), top: Math.floor(row * size) }}
    >
      <G transform={`rotate(180 ${u / 2} ${u / 2})`}>
        <Rect width={u} height={u} fill={FILLS[0]} />
        {TRAIL_MAP.chunks[index].map(([k, d]) => (
          <Path key={k} d={d} fill={FILLS[k]} />
        ))}
      </G>
    </Svg>
  );
});

/** The whole map at `width`, turned 180° (south up, see stations.ts); `width * rows / cols` tall. */
export const TrailTerrain = memo(function TrailTerrain({ width }: { width: number }) {
  const size = width / TRAIL_MAP.cols;
  return (
    <View
      pointerEvents="none"
      style={[styles.map, { width, height: size * TRAIL_MAP.rows }]}
      accessibilityElementsHidden
      importantForAccessibility="no-hide-descendants"
    >
      {TRAIL_MAP.chunks.map((_, i) => (
        <Chunk key={i} index={i} size={size} />
      ))}
    </View>
  );
});

export const TRAIL_MAP_ASPECT = TRAIL_MAP.rows / TRAIL_MAP.cols;

const styles = StyleSheet.create({
  map: {
    position: 'absolute',
    left: 0,
    top: 0,
    overflow: 'hidden',
    backgroundColor: FILLS[0],
  },
});
