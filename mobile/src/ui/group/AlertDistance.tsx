// The guide's alert distance: a small card like the cloud bar (solid card, crisp cardShade edge,
// soft glow) with "Distancia de alerta" and the value in a `brand.alert` pill (the color of its
// mark on the lane), a slider whose track shows the near and mid stretches and the alert zone
// past the thumb, and a caption naming both boundaries.
import { StyleSheet, Text, View } from 'react-native';

import { GROUP_POLICY } from '@/core/group/policy';
import { fill, t } from '@/i18n';

import { Slider } from '../Slider';
import { brand, fonts, radius, spacing, type } from '../theme/tokens';

const { min, max, step, nearFraction } = GROUP_POLICY.alertMeters;

export function AlertDistance({
  meters,
  onChange,
}: {
  meters: number;
  onChange: (meters: number) => void;
}) {
  const value = fill(t.group.meters, { m: meters });
  return (
    <View style={styles.card}>
      <View
        style={styles.header}
        accessibilityElementsHidden
        importantForAccessibility="no-hide-descendants"
      >
        <Text style={styles.label}>{t.group.alertDistance}</Text>
        <View style={styles.pill}>
          <Text style={styles.value}>{value}</Text>
        </View>
      </View>
      <Slider
        value={meters}
        min={min}
        max={max}
        step={step}
        split={nearFraction}
        onChange={onChange}
        label={t.group.alertDistance}
        valueText={value}
        hint={t.group.alertDistanceHint}
      />
      <Text style={styles.caption}>
        {fill(t.group.alertDistanceScale, {
          near: Math.round(nearFraction * meters),
          alert: meters,
        })}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    paddingTop: spacing.md,
    paddingBottom: spacing.sm,
    paddingHorizontal: spacing.md,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: brand.cardShade,
    backgroundColor: brand.card,
    boxShadow: `0 4px 14px ${brand.glow}`,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: spacing.xs,
  },
  label: { ...type.label, color: brand.ink },
  pill: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: radius.pill,
    backgroundColor: brand.alert,
    alignItems: 'center',
    justifyContent: 'center',
  },
  value: { ...type.label, fontFamily: fonts.bold, color: brand.onPrimary },
  caption: { ...type.caption, color: brand.inkMuted, paddingHorizontal: spacing.xs },
});
