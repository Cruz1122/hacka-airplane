// Admin block (shown after the password): how long a station scan keeps the chat open, and the
// four station QRs to show or print at the park, one open at a time.
import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import {
  COUNTED_STATIONS,
  MAX_ACCESS_HOURS,
  MIN_ACCESS_HOURS,
  stationCode,
  type CountedStation,
} from '@/core/access/parkAccess';
import { fill, t } from '@/i18n';
import { setAccessHours, useParkAccess } from '@/state/parkAccess';

import { Icon } from './icons/Icon';
import { InfoCard } from './InfoCard';
import { KnowledgeQr } from './KnowledgeQr';
import { Slider } from './Slider';
import { radius, spacing } from './theme/tokens';
import { useAccessibilityTheme } from './useAccessibilityTheme';

const labels = t.parkAccess.admin;

function StationQrRow({
  station,
  open,
  onToggle,
}: {
  station: CountedStation;
  open: boolean;
  onToggle: () => void;
}) {
  const { palette, scaled, highContrast, borderWidth } = useAccessibilityTheme();
  const name = t.trail.stations[station].name;
  return (
    <View
      style={[
        styles.row,
        {
          backgroundColor: palette.card,
          borderColor: highContrast ? palette.ink : palette.cardShade,
          borderWidth,
          boxShadow: `0 2px 10px ${palette.glow}`,
        },
      ]}
    >
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={name}
        accessibilityHint={open ? labels.hideQr : labels.showQr}
        accessibilityState={{ expanded: open }}
        onPress={onToggle}
        style={styles.rowHead}
      >
        <View
          style={[styles.tile, { backgroundColor: open ? palette.primary : palette.cardShade }]}
          aria-hidden
        >
          <Icon name="scanLine" size={18} color={open ? palette.onPrimary : palette.ink} />
        </View>
        <Text style={[styles.grow, scaled.label, { color: palette.ink }]}>{name}</Text>
        <Icon
          name={open ? 'chevronsUpDown' : 'chevronRight'}
          size={18}
          color={palette.inkMuted}
          strokeWidth={2.2}
        />
      </Pressable>
      {open && <KnowledgeQr code={stationCode(station)} />}
    </View>
  );
}

export function ParkAccessAdmin() {
  const { palette, scaled } = useAccessibilityTheme();
  const { hours } = useParkAccess();
  const [shown, setShown] = useState<CountedStation | null>(null);
  const value = fill(labels.hoursValue, { hours });
  return (
    <View style={styles.list}>
      <Text accessibilityRole="header" style={[scaled.title, { color: palette.ink }]}>
        {labels.heading}
      </Text>
      <InfoCard icon="clock" title={labels.hours} body={labels.hoursBody}>
        <View style={styles.sliderHead}>
          <Text style={[scaled.label, { color: palette.ink }]}>{value}</Text>
        </View>
        <Slider
          value={hours}
          min={MIN_ACCESS_HOURS}
          max={MAX_ACCESS_HOURS}
          step={1}
          onChange={setAccessHours}
          label={labels.hours}
          valueText={value}
        />
      </InfoCard>
      <Text style={[scaled.caption, { color: palette.inkMuted }]}>{labels.qrsHint}</Text>
      {COUNTED_STATIONS.map((station) => (
        <StationQrRow
          key={station}
          station={station}
          open={shown === station}
          onToggle={() => setShown(shown === station ? null : station)}
        />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  list: { gap: spacing.md },
  row: { borderRadius: radius.lg, padding: spacing.md, gap: spacing.md },
  rowHead: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, minHeight: 44 },
  tile: {
    width: 36,
    height: 36,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  grow: { flex: 1 },
  sliderHead: { alignItems: 'flex-end' },
});
