import { useEffect, useState } from 'react';
import { Animated, Easing, Platform, Pressable, StyleSheet, View } from 'react-native';
import Svg, { Path } from 'react-native-svg';

import { fill, t } from '@/i18n';
import { DEFAULT_PALETTE } from '@/onboarding/scene/preset';
import { brand } from '@/ui/theme/tokens';
import { useReducedMotion } from '@/ui/useReducedMotion';

import { STATION_NODES, type StationId } from './stations';
import { TrailMarkSvg } from './trailMarks';

const MAP_H = 720;
const W = 108;
const H = 108;
const CX = 54;
const GROUND = 96;
const SCALE = 1.58;
const REST = 0;
const DOWN_Y = 5;
const DOWN_S = 0.9;
const PULSE_W = 54;
const PULSE_H = 16;
const PULSE_MS = 1800;
const TILT = 9;

const pal = DEFAULT_PALETTE;

/**
 * Each animal faces the next stop and leans up the trail; the last one looks back down at it.
 * The frailejón stays upright.
 */
function poseOf(index: number): { facing: 1 | -1; tilt: number } {
  if (index === 0) return { facing: 1, tilt: 0 };
  const here = STATION_NODES[index]!;
  const next = STATION_NODES[index + 1];
  if (!next) {
    const prev = STATION_NODES[index - 1]!;
    const facing = prev.x >= here.x ? 1 : -1;
    return { facing, tilt: TILT * facing };
  }
  const facing = next.x >= here.x ? 1 : -1;
  return { facing, tilt: -TILT * facing };
}

function Pulse({ delay }: { delay: number }) {
  const reduced = useReducedMotion();
  const [p] = useState(() => new Animated.Value(0));
  useEffect(() => {
    if (reduced) {
      p.setValue(0.4);
      return;
    }
    p.setValue(0);
    const loop = Animated.loop(
      Animated.timing(p, {
        toValue: 1,
        duration: PULSE_MS,
        easing: Easing.out(Easing.quad),
        useNativeDriver: Platform.OS !== 'web',
      }),
    );
    const start = setTimeout(() => loop.start(), delay);
    return () => {
      clearTimeout(start);
      loop.stop();
    };
  }, [p, reduced, delay]);
  return (
    <Animated.View
      pointerEvents="none"
      style={[
        styles.pulse,
        {
          opacity: p.interpolate({ inputRange: [0, 0.15, 1], outputRange: [0, 0.9, 0] }),
          transform: [{ scale: p.interpolate({ inputRange: [0, 1], outputRange: [0.5, 1.5] }) }],
        },
      ]}
    />
  );
}

function trailSegments(w: number, h: number): string[] {
  const pts = STATION_NODES.map((n) => ({ x: n.x * w, y: n.y * h }));
  const segs: string[] = [];
  for (let i = 1; i < pts.length; i++) {
    const a = pts[i - 1]!;
    const b = pts[i]!;
    const cx = (a.x + b.x) / 2;
    segs.push(`M ${a.x} ${a.y} Q ${cx} ${a.y} ${b.x} ${b.y}`);
  }
  return segs;
}

export function TrailPath({
  width,
  onStationPress,
}: {
  width: number;
  onStationPress: (id: StationId) => void;
}) {
  const w = Math.max(width, 1);
  return (
    <View style={[styles.map, { height: MAP_H }]}>
      <Svg width={w} height={MAP_H} style={StyleSheet.absoluteFill} pointerEvents="none">
        {trailSegments(w, MAP_H).map((d) => (
          <Path
            key={d}
            d={d}
            fill="transparent"
            stroke={pal.paramo}
            strokeWidth={3}
            strokeLinecap="round"
            strokeDasharray="5 9"
          />
        ))}
      </Svg>
      {STATION_NODES.map((node, i) => (
        <StationMark
          key={node.id}
          id={node.id}
          index={i}
          x={node.x * w}
          y={node.y * MAP_H}
          onPress={onStationPress}
        />
      ))}
    </View>
  );
}

function StationMark({
  id,
  index,
  x,
  y,
  onPress,
}: {
  id: StationId;
  index: number;
  x: number;
  y: number;
  onPress: (id: StationId) => void;
}) {
  const copy = t.trail.stations[id];
  const n = index + 1;
  const reduced = useReducedMotion();
  const [held, setHeld] = useState(false);
  const [press] = useState(() => new Animated.Value(0));
  const [k, setK] = useState(0);
  useEffect(() => {
    const sub = press.addListener(({ value }) => setK(value));
    return () => press.removeListener(sub);
  }, [press]);
  useEffect(() => {
    press.stopAnimation();
    if (reduced) {
      press.setValue(held ? 1 : 0);
      return;
    }
    Animated.timing(press, {
      toValue: held ? 1 : 0,
      duration: 220,
      easing: Easing.inOut(Easing.cubic),
      useNativeDriver: false,
    }).start();
  }, [held, press, reduced]);
  const dy = REST + (DOWN_Y - REST) * k;
  const sy = 1 + (DOWN_S - 1) * k;
  const pose = poseOf(index);
  return (
    <View style={[styles.stop, { top: y - GROUND, left: x - CX }]}>
      <Pulse delay={index * 260} />
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={fill(t.trail.stationA11y, {
          n,
          name: copy.name,
          mark: t.trail.marks[id],
        })}
        onPress={() => onPress(id)}
        onPressIn={() => setHeld(true)}
        onPressOut={() => setHeld(false)}
        style={styles.hit}
      >
        <TrailMarkSvg
          id={id}
          width={W}
          height={H}
          sink={{ dy, sy, cx: CX, ground: GROUND, scale: SCALE }}
          facing={pose.facing}
          tilt={pose.tilt}
        />
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  map: { width: '100%', position: 'relative', overflow: 'visible' },
  stop: { position: 'absolute', width: W, height: H },
  hit: { width: W, height: H },
  pulse: {
    position: 'absolute',
    left: CX - PULSE_W / 2,
    top: GROUND - PULSE_H / 2,
    width: PULSE_W,
    height: PULSE_H,
    borderRadius: PULSE_H,
    borderWidth: 2,
    borderColor: brand.primary,
    backgroundColor: brand.glow,
  },
});
