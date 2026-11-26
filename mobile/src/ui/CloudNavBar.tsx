// The app's top navigation: a solid card pill with a crisp edge and a soft shadow, with three small
// cloud puffs rising from its top edge. Puffs and pill are one outlined shape: every piece is drawn
// a point larger in `cardShade` first, then in `card` on top, so only the union's outline shows.
// Chat, Grupo and Recorrido are tabs.
// The bar does not navigate by itself: the route passes `onSelect`, which keeps it free of the
// router and usable on /design.
import { memo, useEffect, useState } from 'react';
import { Animated, Platform, Pressable, StyleSheet, Text, View } from 'react-native';
import Svg, { Circle, Rect } from 'react-native-svg';

import { fill, t } from '@/i18n';

import { Icon, type IconName } from './icons/Icon';
import { brand, fonts, type } from './theme/tokens';
import { useAccessibilityTheme } from './useAccessibilityTheme';
import { useReducedMotion } from './useReducedMotion';

export type NavTab = 'chat' | 'group' | 'route';
export type NavSidePanel = 'accessibility' | 'settings';

const TABS: { id: NavTab; icon: IconName; disabled?: boolean }[] = [
  { id: 'chat', icon: 'messageCircle' },
  { id: 'group', icon: 'users' },
  { id: 'route', icon: 'route' },
];

const indexOfTab = (tab: NavTab) => Math.max(0, TABS.findIndex((item) => item.id === tab));

/** Height of the compact pill. */
const BODY = 42;
/** Room above the pill for the tallest puff (3/4 of 12.5, plus its edge). */
const PUFF_UP = 11;
/** The edge's width, drawn in `cardShade`. */
const EDGE = 1;
const MAX_PILL_WIDTH = 268;
const SIDE_SIZE = 40;
const SIDE_GAP = 8;
const EDGE_MARGIN = 12;
/** Points the bar takes below its `top`: the puffs plus the pill. */
export const NAV_BAR_HEIGHT = PUFF_UP + BODY;

/** Puffs along the top edge: x as a fraction of the width, radius in points. Two on the left
 *  shoulder, one on the right, so the outline reads as a cloud without crowding the labels. */
const PUFFS = [
  { x: 0.17, r: 9 },
  { x: 0.3, r: 12.5 },
  { x: 0.76, r: 10.5 },
] as const;

const CloudShape = memo(function CloudShape({
  width,
  fillColor,
  edgeColor,
  edgeWidth,
}: {
  width: number;
  fillColor: string;
  edgeColor: string;
  edgeWidth: number;
}) {
  const shape = (grow: number, color: string) => (
    <>
      <Rect
        x={edgeWidth - grow}
        y={PUFF_UP - grow}
        width={width - 2 * edgeWidth + 2 * grow}
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
      {shape(edgeWidth, edgeColor)}
      {shape(0, fillColor)}
    </Svg>
  );
});

const TAB_H = 34;
const TAB_GAP = 4;
const PAD = (BODY - TAB_H) / 2;
const SIDE_TOP = PUFF_UP + (BODY - SIDE_SIZE) / 2;
const USE_NATIVE_DRIVER = Platform.OS !== 'web';
const SPRING = { stiffness: 320, damping: 26, mass: 0.85, useNativeDriver: USE_NATIVE_DRIVER };

function SideButton({
  icon,
  label,
  active,
  onPress,
  reduced,
}: {
  icon: IconName;
  label: string;
  active: boolean;
  onPress?: () => void;
  reduced: boolean;
}) {
  const { palette, highContrast, borderWidth } = useAccessibilityTheme();
  const [focused, setFocused] = useState(false);
  const [scale] = useState(() => new Animated.Value(1));
  const pressTo = (toValue: number) => {
    if (reduced) {
      scale.setValue(1);
      return;
    }
    Animated.spring(scale, {
      toValue,
      stiffness: 420,
      damping: 26,
      useNativeDriver: USE_NATIVE_DRIVER,
    }).start();
  };
  return (
    <Animated.View style={[styles.sideSlot, { transform: [{ scale }] }]}>
      <Pressable
        accessibilityRole="button"
        accessibilityLabel={label}
        accessibilityState={{ expanded: active }}
        hitSlop={4}
        onPress={onPress}
        onPressIn={() => pressTo(0.91)}
        onPressOut={() => pressTo(1)}
        onFocus={() => setFocused(true)}
        onBlur={() => setFocused(false)}
        style={({ pressed }) => [
          styles.sideButton,
          {
            backgroundColor: active
              ? palette.primary
              : pressed
                ? palette.cardShade
                : palette.card,
            borderColor: active ? palette.primary : highContrast ? palette.ink : palette.cardShade,
            borderWidth: highContrast ? borderWidth : EDGE,
            boxShadow: `0 4px 14px ${palette.glow}`,
            outlineColor: palette.primary,
          },
          focused && styles.sideFocused,
        ]}
      >
        <Icon
          name={icon}
          size={18}
          color={active ? palette.onPrimary : palette.ink}
          strokeWidth={active ? 2.3 : 2}
        />
      </Pressable>
    </Animated.View>
  );
}

export interface CloudNavBarProps {
  active: NavTab;
  onSelect: (tab: NavTab) => void;
  /** Distance from the screen's top, e.g. the safe-area inset plus a gap. */
  top: number;
  /** Screen width; the bar centres itself and keeps a 12 pt side gutter. */
  screenWidth: number;
  onSettings?: () => void;
  onAccessibility?: () => void;
  /** Which side panel is currently open, so its button shows an active state. */
  activeSide?: NavSidePanel | null;
}

export function CloudNavBar({
  active,
  onSelect,
  top,
  screenWidth,
  onSettings,
  onAccessibility,
  activeSide = null,
}: CloudNavBarProps) {
  const { palette, highContrast, borderWidth } = useAccessibilityTheme();
  const [focusedTab, setFocusedTab] = useState<NavTab | null>(null);
  const reduced = useReducedMotion();
  const activeIdx = indexOfTab(active);
  const [pillIndex] = useState(() => new Animated.Value(activeIdx));

  useEffect(() => {
    if (reduced) {
      pillIndex.setValue(activeIdx);
      return;
    }
    const anim = Animated.spring(pillIndex, { toValue: activeIdx, ...SPRING });
    anim.start();
    return () => anim.stop();
  }, [activeIdx, pillIndex, reduced]);

  const pillWidth = Math.max(
    180,
    Math.min(MAX_PILL_WIDTH, screenWidth - 2 * EDGE_MARGIN - 2 * SIDE_SIZE - 2 * SIDE_GAP),
  );
  const totalWidth = pillWidth + 2 * SIDE_SIZE + 2 * SIDE_GAP;
  const innerWidth = pillWidth - 2 * PAD;
  const slotWidth = (innerWidth - TAB_GAP * (TABS.length - 1)) / TABS.length;
  const step = slotWidth + TAB_GAP;
  const translateX = pillIndex.interpolate({
    inputRange: [0, 1, 2],
    outputRange: [0, step, step * 2],
  });

  const handleSelect = (id: NavTab) => {
    if (id === active) return;
    onSelect(id);
  };

  return (
    <View
      style={[styles.row, { top, width: totalWidth, left: (screenWidth - totalWidth) / 2 }]}
      pointerEvents="box-none"
    >
      <SideButton
        icon="accessibility"
        label={t.nav.accessibility}
        active={activeSide === 'accessibility'}
        onPress={onAccessibility}
        reduced={reduced}
      />
      <View style={[styles.pill, { width: pillWidth }]} accessibilityRole="tablist">
        {/* Carries the shadow: the pill's own box, under the drawn shape. */}
        <View
          style={[
            styles.shadow,
            { backgroundColor: palette.card, boxShadow: `0 4px 14px ${palette.glow}` },
          ]}
        />
        <CloudShape
          width={pillWidth}
          fillColor={palette.card}
          edgeColor={highContrast ? palette.ink : palette.cardShade}
          edgeWidth={highContrast ? borderWidth : EDGE}
        />
        <View style={styles.tabs}>
          <Animated.View
            pointerEvents="none"
            style={[
              styles.activePill,
              {
                width: slotWidth,
                backgroundColor: palette.primary,
                transform: [{ translateX }],
              },
            ]}
          />
          {TABS.map(({ id, icon, disabled }) => {
            const on = id === active;
            const ink = on ? palette.onPrimary : palette.ink;
            return (
              <Pressable
                key={id}
                accessibilityRole="tab"
                accessibilityLabel={
                  disabled ? fill(t.nav.disabled, { tab: t.nav[id] }) : t.nav[id]
                }
                accessibilityState={{ selected: on, disabled: !!disabled }}
                disabled={disabled}
                onPress={() => handleSelect(id)}
                onFocus={() => setFocusedTab(id)}
                onBlur={() => setFocusedTab((f) => (f === id ? null : f))}
                style={({ pressed }) => [
                  styles.tab,
                  { outlineColor: palette.primary },
                  !on && pressed && { backgroundColor: palette.cardShade },
                  focusedTab === id && styles.tabFocused,
                  disabled && styles.tabDisabled,
                ]}
              >
                <Icon name={icon} size={15} color={ink} strokeWidth={on ? 2.4 : 2} />
                <Text style={[styles.label, { color: ink }]} numberOfLines={1}>
                  {t.nav[id]}
                </Text>
              </Pressable>
            );
          })}
        </View>
      </View>
      <SideButton
        icon="settings"
        label={t.nav.settings}
        active={activeSide === 'settings'}
        onPress={onSettings}
        reduced={reduced}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    position: 'absolute',
    height: NAV_BAR_HEIGHT,
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: SIDE_GAP,
  },
  sideSlot: { marginTop: SIDE_TOP },
  sideButton: {
    width: SIDE_SIZE,
    height: SIDE_SIZE,
    borderRadius: SIDE_SIZE / 2,
    backgroundColor: brand.card,
    borderWidth: EDGE,
    borderColor: brand.cardShade,
    boxShadow: `0 4px 14px ${brand.glow}`,
    alignItems: 'center',
    justifyContent: 'center',
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 2,
  },
  sidePressed: { backgroundColor: brand.cardShade },
  sideFocused: { outlineWidth: 2 },
  pill: { height: NAV_BAR_HEIGHT },
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
  activePill: {
    position: 'absolute',
    top: 0,
    left: 0,
    height: TAB_H,
    borderRadius: TAB_H / 2,
    backgroundColor: brand.primary,
  },
  tab: {
    flex: 1,
    height: TAB_H,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 4,
    paddingHorizontal: 4,
    borderRadius: TAB_H / 2,
    outlineColor: brand.primary,
    outlineStyle: 'solid',
    outlineWidth: 0,
    outlineOffset: 2,
  },
  tabPressed: { backgroundColor: brand.cardShade },
  tabFocused: { outlineWidth: 2 },
  tabDisabled: { opacity: 0.5 },
  label: { ...type.caption, fontFamily: fonts.semibold, fontSize: 12, lineHeight: 16 },
});
