// A titled card with a glyph tile, the settings sheet's info-card look: scan results, the
// Bluetooth receiver's states, locked-station notices. Actions go in `children`, under the text.
import type { ReactNode } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { Icon, type IconName } from './icons/Icon';
import { radius, spacing } from './theme/tokens';
import { useAccessibilityTheme } from './useAccessibilityTheme';

export function InfoCard({
  icon,
  title,
  body,
  tone = 'neutral',
  children,
}: {
  icon: IconName;
  title: string;
  body?: string;
  /** `done` fills the tile with primary: something just worked. */
  tone?: 'neutral' | 'done';
  children?: ReactNode;
}) {
  const { palette, scaled, highContrast, borderWidth } = useAccessibilityTheme();
  const done = tone === 'done';
  return (
    <View
      accessibilityLiveRegion="polite"
      style={[
        styles.card,
        {
          backgroundColor: palette.card,
          borderColor: highContrast ? palette.ink : palette.cardShade,
          borderWidth,
          boxShadow: `0 2px 10px ${palette.glow}`,
        },
      ]}
    >
      <View style={styles.top}>
        <View
          style={[styles.tile, { backgroundColor: done ? palette.primary : palette.cardShade }]}
          aria-hidden
        >
          <Icon name={icon} size={20} color={done ? palette.onPrimary : palette.ink} />
        </View>
        <View style={styles.texts}>
          <Text style={[scaled.label, { color: palette.ink }]}>{title}</Text>
          {body ? <Text style={[scaled.body, { color: palette.inkMuted }]}>{body}</Text> : null}
        </View>
      </View>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: { borderRadius: radius.lg, padding: spacing.lg, gap: spacing.lg },
  top: { flexDirection: 'row', gap: spacing.md, alignItems: 'flex-start' },
  tile: {
    width: 40,
    height: 40,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
  },
  texts: { flex: 1, gap: spacing.xs },
});
