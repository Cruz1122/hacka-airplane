import { useEffect, useState } from 'react';
import { Animated, Easing, Platform, Pressable, StyleSheet, View } from 'react-native';
import Svg, { Path } from 'react-native-svg';

import { fill, t } from '@/i18n';
import { useReducedMotion } from '@/ui/useReducedMotion';
import { useAccessibilityTheme } from '@/ui/useAccessibilityTheme';

import { STATION_NODES, type StationId } from './stations';
import { FIGURE_BOX, TrailMarkSvg } from './trailMarks';
import { TRAIL_MAP_ASPECT, TrailTerrain } from './TrailTerrain';
import { sceneSky, StationScene } from './trailScenes';

/** Each stop's circle at full size (a map FULL_SIZE_MAP_W wide); narrower maps shrink it. */
const DISC = 84;
/** Never below a touch target. */
const MIN_DISC = 48;
const FULL_SIZE_MAP_W = 680;
/** The card ring around the disc, as on the Pet's circle (PetCircle). */
const RING = 4;
/** A figure's bounding box diagonal as a share of the disc's inside: it fills the circle as the
 * Pet fills hers, only the box's empty corners reaching past the edge. */
const FILL = 1.02;
/** Room under the figure's feet, in figure units, for the ground of its setting (trailScenes). */
const GROUND_ROOM = 9;
/** One pulse: the halo grows from the disc to GROWN times its size and fades. */
const PULSE_MS = 2200;
const GROWN = 1.5;
/** Stops pulse one after another, up the route, then all rest until the next round. */
const PULSE_STAGGER_MS = 320;
const PULSE_PERIOD_MS = 3800;
/** Of the pulse's reach kept clear of the screen edges; it is faint past that. */
const HALO_ROOM = 1.25;
/** Pressed: the disc sinks a little. */
const PRESSED = 0.92;

/** Height of the map drawn at `width`, from the traced chunks' grid. */
export function trailMapHeight(width: number): number {
  return width * TRAIL_MAP_ASPECT;
}

/** Diameter of a stop's circle on a map `width` wide. */
export function discSize(width: number): number {
  return Math.max(MIN_DISC, Math.min(DISC, (DISC * width) / FULL_SIZE_MAP_W));
}

/** Room a stop needs above and below its point: its circle, centred on it, and part of its pulse. */
export function markExtent(width: number): { above: number; below: number } {
  const r = (discSize(width) / 2) * HALO_ROOM;
  return { above: r, below: r };
}

/** Each animal faces the next stop, the last one the previous stop. */
function facingOf(index: number): 1 | -1 {
  const here = STATION_NODES[index]!;
  const toward = STATION_NODES[index + 1] ?? STATION_NODES[index - 1]!;
  return toward.x >= here.x ? 1 : -1;
}

type Pt = { x: number; y: number };

/** Catmull-Rom through every stop, as one cubic Bézier per leg. */
function routeLegs(w: number, h: number): { p1: Pt; c1: Pt; c2: Pt; p2: Pt }[] {
  const pts = STATION_NODES.map((n) => ({ x: n.x * w, y: n.y * h }));
  return pts.slice(0, -1).map((p1, i) => {
    const p0 = pts[Math.max(0, i - 1)]!;
    const p2 = pts[i + 1]!;
    const p3 = pts[Math.min(pts.length - 1, i + 2)]!;
    return {
      p1,
      c1: { x: p1.x + (p2.x - p0.x) / 6, y: p1.y + (p2.y - p0.y) / 6 },
      c2: { x: p2.x - (p3.x - p1.x) / 6, y: p2.y - (p3.y - p1.y) / 6 },
      p2,
    };
  });
}

/** The traced terrain with the route and its stops at their real coordinates. */
export function TrailPath({
  width,
  onStationPress,
}: {
  width: number;
  onStationPress: (id: StationId) => void;
}) {
  const { palette } = useAccessibilityTheme();
  const w = Math.max(width, 1);
  const h = trailMapHeight(w);
  const d = discSize(w);
  const legs = routeLegs(w, h);
  const route =
    `M ${legs[0]!.p1.x} ${legs[0]!.p1.y}` +
    legs.map((l) => ` C ${l.c1.x} ${l.c1.y} ${l.c2.x} ${l.c2.y} ${l.p2.x} ${l.p2.y}`).join('');
  return (
    <View style={[styles.map, { width: w, height: h }]}>
      <TrailTerrain width={w} />
      {/* A footpath: light dashes on a soft dark edge, as trails are drawn on park maps. */}
      <Svg width={w} height={h} style={StyleSheet.absoluteFill} pointerEvents="none">
        <Path
          d={route}
          fill="none"
          stroke={palette.ink}
          strokeOpacity={0.35}
          strokeWidth={7}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <Path
          d={route}
          fill="none"
          stroke={palette.card}
          strokeWidth={3.5}
          strokeDasharray="8 6"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </Svg>
      {STATION_NODES.map((node, i) => (
        <StationDisc
          key={node.id}
          id={node.id}
          index={i}
          x={node.x * w}
          y={node.y * h}
          size={d}
          onPress={onStationPress}
        />
      ))}
    </View>
  );
}

/** A stop: its animal in its setting, in a circle with a card ring, centred on the stop, like the
 * Pet's circle. */
function StationDisc({
  id,
  index,
  x,
  y,
  size,
  onPress,
}: {
  id: StationId;
  index: number;
  x: number;
  y: number;
  size: number;
  onPress: (id: StationId) => void;
}) {
  const { palette } = useAccessibilityTheme();
  const inner = size - RING * 2;
  const box = FIGURE_BOX[id];
  const facing = facingOf(index);
  const boxH = box.h + GROUND_ROOM;
  const scale = (inner * FILL) / Math.hypot(box.w, boxH);
  // Centre the box: mirroring flips x about the feet, so the offset flips with it.
  const cx = inner / 2 - facing * (box.x + box.w / 2) * scale;
  const ground = inner / 2 - (box.y + boxH / 2) * scale;
  return (
    <View
      pointerEvents="box-none"
      style={[styles.slot, { left: x - size / 2, top: y - size / 2, width: size, height: size }]}
    >
      <Halo color={sceneSky(id)} delay={index * PULSE_STAGGER_MS} radius={size / 2} />
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={fill(t.trail.stationA11y, {
          n: index + 1,
          name: t.trail.stations[id].name,
          mark: t.trail.marks[id],
        })}
        onPress={() => onPress(id)}
        style={({ pressed }) => [
          styles.disc,
          {
            borderRadius: size / 2,
            borderColor: palette.card,
            transform: [{ scale: pressed ? PRESSED : 1 }],
          },
        ]}
      >
        <StationScene id={id} size={inner} ground={ground} />
        {/* Positioned like the scene: on web an absolute sibling stacks over one in normal flow. */}
        <View style={StyleSheet.absoluteFill} pointerEvents="none">
          <TrailMarkSvg
            id={id}
            width={inner}
            height={inner}
            sink={{ dy: 0, sy: 1, cx, ground, scale }}
            facing={facing}
          />
        </View>
      </Pressable>
    </View>
  );
}

/** The disc's pulse: a halo of its color growing out from behind it. None under reduced motion. */
function Halo({ color, delay, radius }: { color: string; delay: number; radius: number }) {
  const reduced = useReducedMotion();
  const [clock] = useState(() => new Animated.Value(0));
  useEffect(() => {
    if (reduced) return;
    // One plain loop per halo; its stop's offset lives in the interpolation below. A loop around
    // a sequence with delays runs once and stops on web.
    const loop = Animated.loop(
      Animated.timing(clock, {
        toValue: 1,
        duration: PULSE_PERIOD_MS,
        easing: Easing.linear,
        useNativeDriver: Platform.OS !== 'web',
      }),
    );
    loop.start();
    return () => loop.stop();
  }, [reduced, clock]);
  if (reduced) return null;
  const start = delay / PULSE_PERIOD_MS;
  const end = start + PULSE_MS / PULSE_PERIOD_MS;
  const inputRange = [0, start, end, 1];
  return (
    <Animated.View
      pointerEvents="none"
      style={[
        StyleSheet.absoluteFill,
        {
          borderRadius: radius,
          backgroundColor: color,
          opacity: clock.interpolate({ inputRange, outputRange: [0, 0.6, 0, 0] }),
          transform: [
            {
              scale: clock.interpolate({
                inputRange,
                outputRange: [1, 1, GROWN, GROWN],
                easing: Easing.out(Easing.quad),
              }),
            },
          ],
        },
      ]}
    />
  );
}

const styles = StyleSheet.create({
  map: { position: 'relative', overflow: 'hidden' },
  slot: { position: 'absolute' },
  disc: { flex: 1, overflow: 'hidden', borderWidth: RING },
});
