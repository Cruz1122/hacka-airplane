// The guide's alert: who triggered it, on the alert surface, with a warning glyph that pulses
// unless motion is reduced. Shows the first alert and counts the rest.
import { useEffect, useState } from 'react';
import { Animated, Platform, StyleSheet, Text, View } from 'react-native';

import type { Alert } from '@/core/group/types';
import { fill, t } from '@/i18n';

import { Icon } from '../icons/Icon';
import { brand, spacing, type } from '../theme/tokens';
import { useReducedMotion } from '../useReducedMotion';

const ALERT_COPY: Record<Alert['kind'], string> = {
  visitorFar: t.group.alertFar,
  visitorLost: t.group.alertLost,
  guideLost: t.group.alertGuideLost,
};

export const alertText = (a: Alert, name: string) => fill(ALERT_COPY[a.kind], { name });

export interface GroupAlertBannerProps {
  /** Most urgent first, as `alerts()` orders them. */
  alerts: Alert[];
  nameOf: (a: Alert) => string;
}

export function GroupAlertBanner({ alerts, nameOf }: GroupAlertBannerProps) {
  const reduced = useReducedMotion();
  const [glow] = useState(() => new Animated.Value(1));
  const active = alerts.length > 0;
  useEffect(() => {
    if (reduced || !active) return glow.setValue(1);
    const native = Platform.OS !== 'web';
    const loop = Animated.loop(
      Animated.sequence([
        Animated.timing(glow, { toValue: 0.35, duration: 600, useNativeDriver: native }),
        Animated.timing(glow, { toValue: 1, duration: 600, useNativeDriver: native }),
      ]),
    );
    loop.start();
    return () => loop.stop();
  }, [reduced, active, glow]);
  if (!active) return null;
  const [first, ...rest] = alerts;
  return (
    <View style={styles.root} accessibilityRole="alert" accessibilityLiveRegion="assertive">
      <Animated.View style={[styles.icon, { opacity: glow }]}>
        <Icon name="triangleAlert" size={22} color={brand.onPrimary} />
      </Animated.View>
      <View style={styles.texts}>
        <Text style={styles.title}>{alertText(first, nameOf(first))}</Text>
        {rest.length > 0 && (
          <Text style={styles.more}>{fill(t.group.alertsMore, { n: rest.length })}</Text>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  root: {
    alignSelf: 'stretch',
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    minHeight: 56,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    borderRadius: 17,
    borderWidth: 1,
    borderColor: brand.alert,
    backgroundColor: brand.alert,
  },
  icon: { width: 24, alignItems: 'center' },
  texts: { flex: 1, gap: 2 },
  title: { ...type.label, color: brand.onPrimary },
  more: { ...type.caption, color: brand.onPrimary },
});
