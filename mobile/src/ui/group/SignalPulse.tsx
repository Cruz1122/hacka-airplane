// The visitor's "bring your phone close" signal: a broadcast glyph (a dot and three arcs, drawn
// with react-native-svg) whose arcs light up one after another from the dot outward. Each arc is
// its own Animated.View so only opacity animates, on the native driver off web (react-native-web
// stops `Animated.loop` after one iteration when `useNativeDriver: true` is passed). Reduced motion
// shows the glyph still and fully lit.
import { useEffect, useState } from 'react';
import { Animated, Easing, Platform, StyleSheet, View } from 'react-native';
import Svg, { Circle, Path } from 'react-native-svg';

import { brand } from '../theme/tokens';
import { useReducedMotion } from '../useReducedMotion';

const CYCLE_MS = 1600;
/** Arc radii as fractions of half the size; the dot sits at the bottom centre. */
const ARCS = [0.3, 0.55, 0.8] as const;
/** Half-angle of each arc, from straight up. */
const SPREAD = (48 * Math.PI) / 180;

/** An arc centred straight up from (c, base), radius r. Absolute commands only. */
function arcPath(c: number, base: number, r: number): string {
  const dx = Math.sin(SPREAD) * r;
  const dy = Math.cos(SPREAD) * r;
  return `M ${c - dx} ${base - dy} A ${r} ${r} 0 0 1 ${c + dx} ${base - dy}`;
}

export function SignalPulse({ size = 160 }: { size?: number }) {
  const reduced = useReducedMotion();
  const [phase] = useState(() => new Animated.Value(0));
  useEffect(() => {
    if (reduced) return phase.setValue(0);
    const loop = Animated.loop(
      Animated.timing(phase, {
        toValue: 1,
        duration: CYCLE_MS,
        easing: Easing.linear,
        useNativeDriver: Platform.OS !== 'web',
      }),
    );
    loop.start();
    return () => loop.stop();
  }, [phase, reduced]);

  const c = size / 2;
  // The dot sits low so the arcs fan upward and the whole glyph is centred in the box.
  const base = size * 0.78;
  const half = size / 2;
  const stroke = Math.max(6, size / 16);
  const layer = (children: React.ReactNode) => (
    <Svg width={size} height={size} style={StyleSheet.absoluteFill} pointerEvents="none" aria-hidden>
      {children}
    </Svg>
  );
  return (
    <View
      style={{ width: size, height: size }}
      aria-hidden
      accessibilityElementsHidden
      importantForAccessibility="no-hide-descendants"
    >
      {/* Dim arcs underneath, so the glyph reads whole between waves. */}
      {layer(
        ARCS.map((k) => (
          <Path
            key={k}
            d={arcPath(c, base, k * half * 1.5)}
            stroke={brand.primarySoft}
            strokeWidth={stroke}
            strokeLinecap="round"
            fill="none"
          />
        )),
      )}
      {ARCS.map((k, i) => {
        // Each arc lights up after the one inside it and fades before the loop restarts, so the
        // wave always travels smoothly outward.
        const on = 0.04 + i * 0.24;
        const lit = reduced
          ? 1
          : phase.interpolate({
              inputRange: [0, on, on + 0.16, on + 0.44, 1],
              outputRange: [0, 0, 1, 0, 0],
              extrapolate: 'clamp',
            });
        return (
          <Animated.View key={k} style={[StyleSheet.absoluteFill, { opacity: lit }]}>
            {layer(
              <Path
                d={arcPath(c, base, k * half * 1.5)}
                stroke={brand.primary}
                strokeWidth={stroke}
                strokeLinecap="round"
                fill="none"
              />,
            )}
          </Animated.View>
        );
      })}
      {layer(<Circle cx={c} cy={base} r={stroke * 1.1} fill={brand.primary} />)}
    </View>
  );
}
