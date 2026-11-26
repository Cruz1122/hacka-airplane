// The app's top navigation: a solid card pill with a crisp edge and a soft shadow, with three small
// cloud puffs rising from its top edge. Puffs and pill are one outlined shape: every piece is drawn
// a point larger in `cardShade` first, then in `card` on top, so only the union's outline shows.
// Chat, Grupo and Recorrido are tabs; Recorrido is not built yet, so it is shown disabled.
// The bar does not navigate by itself: the route passes `onSelect`, which keeps it free of the
// router and usable on /design.
import { memo, useState } from 'react';
import { Platform, Pressable, StyleSheet, Text, View } from 'react-native';
import Svg, { Circle, Rect } from 'react-native-svg';

import { fill, t } from '@/i18n';

import { Icon, type IconName } from './icons/Icon';
import { brand, fonts, type } from './theme/tokens';

export type NavTab = 'chat' | 'group' | 'route';

const TABS: { id: NavTab; icon: IconName; disabled?: boolean }[] = [
  { id: 'chat', icon: 'messageCircle' },
  { id: 'group', icon: 'users' },
  { id: 'route', icon: 'route', disabled: true },
];

/** Height of the pill. */
const BODY = 52;
/** Room above the pill for the tallest puff (3/4 of 16, plus its edge). */
const PUFF_UP = 14;
/** The edge's width, drawn in `cardShade`. */
const EDGE = 1;
const MAX_WIDTH = 340;
/** Points the bar takes below its `top`: the puffs plus the pill. */
export const NAV_BAR_HEIGHT = PUFF_UP + BODY;

/** Puffs along the top edge: x as a fraction of the width, radius in points. Two on the left
 *  shoulder, one on the right, so the outline reads as a cloud without crowding the labels. */
const PUFFS = [
  { x: 0.17, r: 11 },
  { x: 0.3, r: 16 },
  { x: 0.75, r: 13 },
] as const;

const CloudShape = memo(function CloudShape({ width }: { width: number }) {
  const shape = (grow: number, color: string) => (
    <>
      <Rect
        x={EDGE - grow}
        y={PUFF_UP - grow}
        width={width - 2 * EDGE + 2 * grow}
        height={BODY + 2 * grow}
        rx={BODY / 2 + grow}
        fill={color}
      />
      {PUFFS.map((p) => (
        // Each puff's centre sits a quarter of its radius under the edge, so it rises 3/4 r.
        <Circle key={p.x} cx={width * p.x} cy={PUFF_UP + p.r * 0.25} r={p.r + grow} fill={color} />
      ))}
    </>
  );
  return (
    <Svg
      width={width}
      height={NAV_BAR_HEIGHT}
      style={StyleSheet.absoluteFill}
      pointerEvents="none"
      aria-hidden
      {...(Platform.OS === 'web'
        ? undefined
        : {
            accessible: false,
            accessibilityElementsHidden: true,
            importantForAccessibility: 'no-hide-descendants' as const,
          })}
    >
      {shape(EDGE, brand.cardShade)}
      {shape(0, brand.card)}
    </Svg>
  );
});

const TAB_H = 44;
const TAB_GAP = 4;

export interface CloudNavBarProps {
  active: NavTab;
  onSelect: (tab: NavTab) => void;
  /** Distance from the screen's top, e.g. the safe-area inset plus a gap. */
  top: number;
  /** Screen width; the bar centres itself and keeps a 16 pt side gutter. */
  screenWidth: number;
}

export function CloudNavBar({ active, onSelect, top, screenWidth }: CloudNavBarProps) {
  const [focused, setFocused] = useState<NavTab | null>(null);
  const width = Math.min(MAX_WIDTH, screenWidth - 32);
  return (
    <View
      style={[styles.bar, { top, width, left: (screenWidth - width) / 2 }]}
      accessibilityRole="tablist"
    >
      {/* Carries the shadow: the pill's own box, under the drawn shape. */}
      <View style={styles.shadow} />
      <CloudShape width={width} />
      <View style={styles.tabs}>
        {TABS.map(({ id, icon, disabled }) => {
          const on = id === active;
          const ink = on ? brand.onPrimary : brand.ink;
          return (
            <Pressable
              key={id}
              accessibilityRole="tab"
              accessibilityLabel={disabled ? fill(t.nav.disabled, { tab: t.nav[id] }) : t.nav[id]}
              accessibilityState={{ selected: on, disabled: !!disabled }}
              disabled={disabled}
              onPress={() => !on && onSelect(id)}
              onFocus={() => setFocused(id)}
              onBlur={() => setFocused((f) => (f === id ? null : f))}
              style={({ pressed }) => [
                styles.tab,
                on ? styles.tabOn : pressed && styles.tabPressed,
                focused === id && styles.tabFocused,
                disabled && styles.tabDisabled,
              ]}
            >
              <Icon name={icon} size={18} color={ink} strokeWidth={on ? 2.4 : 2} />
              <Text style={[styles.label, { color: ink }]} numberOfLines={1}>
                {t.nav[id]}
              </Text>
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}

const PAD = (BODY - TAB_H) / 2;

const styles = StyleSheet.create({
  bar: { position: 'absolute', height: NAV_BAR_HEIGHT },
  shadow: {
    position: 'absolute',
    top: PUFF_UP,
    left: 0,
    right: 0,
    height: BODY,
    borderRadius: BODY / 2,
    backgroundColor: brand.card,
    boxShadow: `0 4px 14px ${brand.glow}`,
  },
  tabs: {
    position: 'absolute',
    top: PUFF_UP + PAD,
    left: PAD,
    right: PAD,
    height: TAB_H,
    flexDirection: 'row',
    gap: TAB_GAP,
  },
  tab: {
    flex: 1,
    height: TAB_H,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    borderRadius: TAB_H / 2,
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 2,
  },
  tabOn: { backgroundColor: brand.primary },
  tabPressed: { backgroundColor: brand.cardShade },
  tabFocused: { outlineWidth: 2 },
  tabDisabled: { opacity: 0.5 },
  label: { ...type.caption, fontFamily: fonts.semibold },
});
