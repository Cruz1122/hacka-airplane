import { router } from 'expo-router';
import { useState } from 'react';
import { StyleSheet, useWindowDimensions, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { isStationUnlocked, stationToScan, type CountedStation } from '@/core/access/parkAccess';
import { fill, t } from '@/i18n';
import { useParkAccess } from '@/state/parkAccess';
import { NAV_BAR_HEIGHT } from '@/ui/CloudNavBar';
import { InfoCard } from '@/ui/InfoCard';
import { PrimaryButton } from '@/ui/PrimaryButton';
import { SecondaryButton } from '@/ui/SecondaryButton';
import { brand, spacing } from '@/ui/theme/tokens';
import { useAccessibilityTheme } from '@/ui/useAccessibilityTheme';

import { STATION_NODES, type StationId } from './stations';
import { StationSheet } from './StationSheet';
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
  const [open, setOpen] = useState<StationId | null>(null);
  const { access } = useParkAccess();
  // The station whose QR is needed, when a locked one was pressed.
  const [needs, setNeeds] = useState<CountedStation | null>(null);
  const press = (id: StationId) => {
    if (isStationUnlocked(access, id)) {
      setNeeds(null);
      setOpen(id);
    } else {
      setNeeds(stationToScan(id as CountedStation));
    }
  };
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
        <TrailPath
          width={frame.width}
          onStationPress={press}
          isLocked={(id) => !isStationUnlocked(access, id)}
        />
      </View>
      {needs ? (
        <View style={[styles.needs, { bottom: insets.bottom + spacing.lg }]}>
          <InfoCard
            icon="lock"
            title={t.trail.locked.title}
            body={fill(t.trail.locked.needs, { name: t.trail.stations[needs].name })}
          >
            <PrimaryButton label={t.knowledge.scan} onPress={() => router.push('/validar')} />
            <SecondaryButton label={t.trail.locked.close} onPress={() => setNeeds(null)} />
          </InfoCard>
        </View>
      ) : null}
      <StationSheet
        id={open}
        bottom={insets.bottom}
        onClose={() => setOpen(null)}
        onMore={(id) => {
          setOpen(null);
          router.push(`/estacion/${id}`);
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: brand.card, overflow: 'hidden' },
  map: { position: 'absolute' },
  needs: { position: 'absolute', left: spacing.lg, right: spacing.lg },
});
