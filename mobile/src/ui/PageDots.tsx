// Step indicator: one dot per page, the active one solid. `position` may be fractional while
// pages slide, so the active dot grows and shrinks continuously.
import { Pressable, StyleSheet, View } from 'react-native';

import { fill, t } from '@/i18n';

import { brand } from './theme/tokens';

export interface PageDotsProps {
  count: number;
  /** 0..count-1, fractional between pages. */
  position: number;
  onSelect?: (index: number) => void;
}

const DOT = 10;

export function PageDots({ count, position, onSelect }: PageDotsProps) {
  const active = Math.min(count - 1, Math.max(0, Math.round(position)));
  return (
    <View style={styles.row} accessibilityRole="tablist">
      {Array.from({ length: count }, (_, i) => {
        const near = Math.max(0, 1 - Math.abs(position - i));
        return (
          <Pressable
            key={i}
            accessibilityRole="tab"
            accessibilityLabel={fill(t.pageDot, { n: i + 1, total: count })}
            accessibilityState={{ selected: i === active }}
            // 10 pt dot + 17 pt on each side = 44 pt touch target.
            hitSlop={17}
            onPress={() => onSelect?.(i)}
            style={[
              styles.dot,
              {
                backgroundColor: i === active ? brand.primary : brand.primarySoft,
                transform: [{ scale: 0.8 + 0.2 * near }],
              },
            ]}
          />
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', gap: 12, alignItems: 'center', justifyContent: 'center' },
  dot: { width: DOT, height: DOT, borderRadius: DOT / 2 },
});
