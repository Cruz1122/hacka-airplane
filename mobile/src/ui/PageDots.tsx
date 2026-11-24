// Step indicator: one dot per page, the active one solid. `position` may be fractional while
// pages slide, so the active dot grows and shrinks continuously.
import { useLayoutEffect, useMemo, useState } from 'react';
import { Animated, Pressable, StyleSheet, View } from 'react-native';

import { fill, t } from '@/i18n';

import { brand } from './theme/tokens';

/**
 * A page position animated outside React: `value` is fractional while pages slide and is set every
 * frame (native-driven styles read it with no render); `index` is the page it rounds to, so the
 * owner re-renders only when that changes.
 */
export interface PagePosition {
  value: Animated.Value;
  index: number;
}

/** `position` as an Animated.Value: the one given, or one that follows a plain number. */
export function usePagePosition(position: number | PagePosition): PagePosition {
  const plain = typeof position === 'number' ? position : null;
  const [own] = useState(() => new Animated.Value(plain ?? 0));
  useLayoutEffect(() => {
    if (plain !== null) own.setValue(plain);
  }, [own, plain]);
  return typeof position === 'number' ? { value: own, index: Math.round(position) } : position;
}

/** Scale of dot `i`: 1 on its page, 0.8 a page or more away, linear in between. */
export const dotScale = (value: Animated.Value, i: number) =>
  value.interpolate({ inputRange: [i - 1, i, i + 1], outputRange: [0.8, 1, 0.8], extrapolate: 'clamp' });

export interface PageDotsProps {
  count: number;
  /** 0..count-1, fractional between pages. */
  position: number | PagePosition;
  onSelect?: (index: number) => void;
}

const DOT = 10;

export function PageDots({ count, position, onSelect }: PageDotsProps) {
  const { value, index } = usePagePosition(position);
  const active = Math.min(count - 1, Math.max(0, index));
  // Built once per value: a render when the page changes mid-move must not rebuild native nodes.
  const scales = useMemo(
    () => Array.from({ length: count }, (_, i) => dotScale(value, i)),
    [value, count],
  );
  return (
    <View style={styles.row} accessibilityRole="tablist">
      {Array.from({ length: count }, (_, i) => (
        <Pressable
          key={i}
          accessibilityRole="tab"
          accessibilityLabel={fill(t.pageDot, { n: i + 1, total: count })}
          accessibilityState={{ selected: i === active }}
          // 10 pt dot + 17 pt on each side = 44 pt touch target.
          hitSlop={17}
          onPress={() => onSelect?.(i)}
          style={styles.slot}
        >
          <Animated.View
            style={[
              styles.dot,
              {
                backgroundColor: i === active ? brand.primary : brand.primarySoft,
                transform: [{ scale: scales[i] }],
              },
            ]}
          />
        </Pressable>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', gap: 12, alignItems: 'center', justifyContent: 'center' },
  slot: { width: DOT, height: DOT },
  dot: { width: DOT, height: DOT, borderRadius: DOT / 2 },
});
