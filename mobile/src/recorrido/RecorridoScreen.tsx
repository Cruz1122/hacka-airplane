import { router } from 'expo-router';
import { useState } from 'react';
import { StyleSheet, useWindowDimensions, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { t } from '@/i18n';
import { NAV_BAR_HEIGHT } from '@/ui/CloudNavBar';
import { brand, spacing } from '@/ui/theme/tokens';
import { useAccessibilityTheme } from '@/ui/useAccessibilityTheme';

import { STATION_NODES } from './stations';
import { markExtent, trailMapHeight, TrailPath } from './TrailPath';
import { TRAIL_BASE_COLOR } from './TrailTerrain';

const xs = STATION_NODES.map((n) => n.x);
const ys = STATION_NODES.map((n) => n.y);
/** The route's extent, 0..1 of the map. */
const ROUTE = {
  left: Math.min(...xs),
  right: Math.max(...xs),
  top: Math.min(...ys),
  bottom: Math.max(...ys),
};

/** Least room between a stop's circle (with its pulse) and the screen's side; the route sits well
 * inside the screen with terrain all around it. */
const PAD = spacing.xl * 3;

export interface TrailFrame {
  /** Map width. */
  width: number;
  /** Map's top-left on the screen. */
  x: number;
  y: number;
}

/**
 * Sizes and places the map so the whole route fits between the top bar and the bottom margin:
 * the widest map that still fits, bottom-anchored (Brisas just above the margin) so the map runs
 * down to the edge. Phones fit it at or above their width; a screen too short for that gets a
 * narrower map, centred.
 */
export function trailFrame(
  vw: number,
  vh: number,
  top: number,
  bottom: number,
  side = 0,
): TrailFrame {
  const span = ROUTE.bottom - ROUTE.top;
  const fits = (w: number) => {
    const { above, below } = markExtent(w);
    const tall = top + above + span * trailMapHeight(w) + below + bottom;
    const wide = side * 2 + above * 2 + (ROUTE.right - ROUTE.left) * w;
    return tall <= vh && wide <= vw;
  };
  let lo = vw / 8;
  let hi = vw * 4;
  for (let i = 0; i < 40; i++) {
    const mid = (lo + hi) / 2;
    if (fits(mid)) lo = mid;
    else hi = mid;
  }
  const width = lo;
  const h = trailMapHeight(width);
  const { below } = markExtent(width);
  const centred = vw / 2 - ((ROUTE.left + ROUTE.right) / 2) * width;
  const x = width >= vw ? Math.min(0, Math.max(vw - width, centred)) : (vw - width) / 2;
  const y = Math.max(vh - bottom - below - ROUTE.bottom * h, vh - h);
  return { width, x, y };
}

export function RecorridoScreen() {
  const { palette } = useAccessibilityTheme();
  const window = useWindowDimensions();
  const insets = useSafeAreaInsets();
  const [size, setSize] = useState<{ w: number; h: number } | null>(null);
  const vw = size?.w ?? window.width;
  const vh = size?.h ?? window.height;
  // The tab navigator draws the cloud bar over the top; the route starts below it.
  const top = insets.top + NAV_BAR_HEIGHT + spacing.xl * 3;
  const frame = trailFrame(vw, vh, top, insets.bottom + spacing.xl * 4, PAD);
  return (
    <View
      style={[styles.root, { backgroundColor: palette.card }]}
      accessibilityLabel={t.trail.title}
      onLayout={(e) =>
        setSize({
          w: e.nativeEvent.layout.width,
          h: e.nativeEvent.layout.height,
        })
      }
    >
      {frame.width < vw ? (
        <View style={[StyleSheet.absoluteFill, { backgroundColor: TRAIL_BASE_COLOR }]} />
      ) : null}
      <View style={[styles.map, { left: frame.x, top: frame.y }]}>
        <TrailPath width={frame.width} onStationPress={(id) => router.push(`/estacion/${id}`)} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: brand.card, overflow: 'hidden' },
  map: { position: 'absolute' },
});
