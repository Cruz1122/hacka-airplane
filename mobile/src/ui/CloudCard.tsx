// Cloud card: the white panel that holds onboarding copy and actions. Its top is vapor, drawn
// like the Pet in the scene: puffs with a solid centre and a soft rim billow over the card's
// body, so the edge reads as steam instead of hard hills. The edge (CLOUD_EDGE points tall)
// overlaps whatever sits above the card.
import { memo, useId, useMemo, type ReactNode } from 'react';
import { StyleSheet, View, type StyleProp, type ViewStyle } from 'react-native';
import Svg, {
  Circle,
  Defs,
  Ellipse,
  LinearGradient,
  RadialGradient,
  Rect,
  Stop,
} from 'react-native-svg';

import { brand } from './theme/tokens';

/** Height of the vapor edge above the card's solid body, in points. */
export const CLOUD_EDGE = 52;

/**
 * Top of the solid body. It never drops below the edge, because the scene drawing above the
 * card ends there.
 */
export const VAPOR_BODY_TOP = CLOUD_EDGE * 0.76;

/** A billow of the edge: an ellipse, wider than tall, so few of them still cover the edge. */
export interface VaporPuff {
  x: number;
  y: number;
  rx: number;
  ry: number;
}

const hash01 = (n: number) => {
  const s = Math.sin(n * 127.1 + 311.7) * 43758.5453;
  return s - Math.floor(s);
};

/**
 * Billows along the body's top. Their solid centres reach above the body, so the billows, not
 * the body's straight line, make the silhouette. One extra billow past each side keeps the edge
 * continuous; none rises past y = 0, where the Svg would clip it flat.
 */
export function vaporPuffs(width: number): VaporPuff[] {
  const n = Math.max(4, Math.round(width / 56));
  const step = width / n;
  const puffs: VaporPuff[] = [];
  for (let i = -1; i <= n; i++) {
    const x = (i + 0.5 + (hash01(i) - 0.5) * 0.4) * step;
    const ry = 22 + 14 * hash01(i + 7);
    // Alternate billows sit a little higher, so the line rolls instead of running flat.
    const lift = i % 2 === 0 ? 0.08 * ry : 0.3 * ry;
    puffs.push({ x, y: Math.max(ry, VAPOR_BODY_TOP + lift), rx: ry * 1.8, ry });
  }
  return puffs;
}

/**
 * Depth of the card's bottom tint and of its corner puffs, in points from the top. Fixed, not a
 * fraction of the height, so a taller surface (the chat sheet the card rises into) keeps the same
 * top and only continues the tint below.
 */
const TINT_DEPTH = 330;
const PUFF_LEFT_Y = 272;
const PUFF_RIGHT_Y = 227;

/** Card surface; memoized because the card's content re-renders on every transition frame. */
const CloudSurface = memo(function CloudSurface({
  width,
  height,
}: {
  width: number;
  height: number;
}) {
  const puffs = useMemo(() => vaporPuffs(width), [width]);
  // Gradient ids share one namespace on web; two surfaces on a page must not collide.
  const prefix = `cc${useId().replace(/[^a-zA-Z0-9]/g, '')}`;
  const id = (k: string) => `${prefix}-${k}`;
  const url = (k: string) => `url(#${id(k)})`;
  return (
    <Svg width={width} height={height} style={StyleSheet.absoluteFill}>
      <Defs>
        <RadialGradient id={id('halo')} cx="50%" cy="50%" r="50%">
          <Stop offset="0" stopColor={brand.card} stopOpacity={1} />
          <Stop offset="0.52" stopColor={brand.card} stopOpacity={1} />
          <Stop offset="0.76" stopColor={brand.card} stopOpacity={0.5} />
          <Stop offset="1" stopColor={brand.card} stopOpacity={0} />
        </RadialGradient>
        <RadialGradient id={id('halo-shade')} cx="50%" cy="50%" r="50%">
          <Stop offset="0" stopColor={brand.cardShade} stopOpacity={0.45} />
          <Stop offset="1" stopColor={brand.cardShade} stopOpacity={0} />
        </RadialGradient>
        {/* Starts at the edge's foot, so the puffs above it carry no tint seam. */}
        <LinearGradient
          id={id('shade')}
          gradientUnits="userSpaceOnUse"
          x1={0}
          y1={CLOUD_EDGE}
          x2={0}
          y2={CLOUD_EDGE + TINT_DEPTH}
        >
          <Stop offset="0" stopColor={brand.cardShade} stopOpacity={0} />
          <Stop offset="1" stopColor={brand.cardShade} stopOpacity={0.7} />
        </LinearGradient>
        <RadialGradient id={id('puff')} cx="50%" cy="50%" r="50%">
          <Stop offset="0" stopColor={brand.cardShade} stopOpacity={0.9} />
          <Stop offset="1" stopColor={brand.cardShade} stopOpacity={0} />
        </RadialGradient>
      </Defs>
      {/* Opaque body: the card must hide whatever art runs underneath it. */}
      <Rect y={VAPOR_BODY_TOP} width={width} height={height} fill={brand.card} />
      <Rect y={VAPOR_BODY_TOP} width={width} height={height} fill={url('shade')} />
      {/* Billows over the body: light first, then the shade offset down-right, as on the Pet. */}
      {puffs.map((p, i) => (
        <Ellipse key={`l${i}`} cx={p.x} cy={p.y} rx={p.rx} ry={p.ry} fill={url('halo')} />
      ))}
      {puffs.map((p, i) => (
        <Ellipse
          key={`s${i}`}
          cx={p.x + p.rx * 0.15}
          cy={p.y + p.ry * 0.25}
          rx={p.rx}
          ry={p.ry}
          fill={url('halo-shade')}
        />
      ))}
      <Circle cx={width * 0.04} cy={PUFF_LEFT_Y} r={width * 0.22} fill={url('puff')} />
      <Circle cx={width * 0.98} cy={PUFF_RIGHT_Y} r={width * 0.2} fill={url('puff')} />
    </Svg>
  );
});

export interface CloudCardProps {
  width: number;
  height: number;
  children: ReactNode;
  style?: StyleProp<ViewStyle>;
}

export function CloudCard({ width, height, children, style }: CloudCardProps) {
  return (
    <View style={[{ width, height }, style]}>
      <CloudSurface width={width} height={height} />
      {children}
    </View>
  );
}
