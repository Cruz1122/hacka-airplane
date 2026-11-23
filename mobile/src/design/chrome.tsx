// Building blocks of the /design workshop: the nav, the stage (preview canvas + controls panel)
// and the small controls the labs share. Workshop-only; app screens use src/ui.
import { useEffect, useState, type ReactNode } from 'react';
import { Animated, Easing, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { t } from '@/i18n';
import { Icon, type IconName } from '@/ui/icons/Icon';
import { brand, radius, spacing, type } from '@/ui/theme/tokens';

import { WORKSHOP_ITEMS, type WorkshopId } from './registry';

/** What every lab receives from the workshop screen. */
export interface LabProps {
  wide: boolean;
  /** System setting or the workshop's own toggle. */
  reducedMotion: boolean;
}

export function WorkshopNav({
  selected,
  onSelect,
  vertical,
}: {
  selected: WorkshopId;
  onSelect: (id: WorkshopId) => void;
  vertical: boolean;
}) {
  const items = WORKSHOP_ITEMS.map((item) => {
    const on = item.id === selected;
    return (
      <Pressable
        key={item.id}
        onPress={() => onSelect(item.id)}
        accessibilityRole="tab"
        accessibilityLabel={item.label}
        accessibilityState={{ selected: on }}
        style={({ pressed }) => [
          styles.navItem,
          vertical ? styles.navItemVertical : styles.navItemPill,
          on && styles.navItemOn,
          pressed && !on && styles.navItemPressed,
        ]}
      >
        <Icon name={item.icon} size={18} color={on ? brand.primary : brand.inkMuted} />
        <Text style={[styles.navIndex, on && styles.navTextOn]}>{item.index}</Text>
        <Text style={[styles.navLabel, on && styles.navTextOn]} numberOfLines={1}>
          {item.label}
        </Text>
      </Pressable>
    );
  });
  if (vertical) {
    return (
      <View
        style={styles.navColumn}
        accessibilityRole="tablist"
        accessibilityLabel={t.dev.workshop.nav}
      >
        {items}
      </View>
    );
  }
  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      contentContainerStyle={styles.navRow}
      accessibilityRole="tablist"
      accessibilityLabel={t.dev.workshop.nav}
    >
      {items}
    </ScrollView>
  );
}

/** Preview canvas beside (wide) or above (narrow) the controls panel. */
export function Stage({
  wide,
  preview,
  controls,
}: {
  wide: boolean;
  preview: ReactNode;
  controls: ReactNode;
}) {
  return (
    <View style={[styles.stage, wide && styles.stageWide]}>
      <View style={[styles.canvas, wide && styles.canvasWide]}>{preview}</View>
      <View style={[styles.panel, wide && styles.panelWide]}>
        <Text style={styles.panelTitle}>{t.dev.workshop.controls}</Text>
        {controls}
      </View>
    </View>
  );
}

/** A phone-sized chat sheet: the surface the chat components really sit on. */
export function PhoneFrame({ height, children }: { height: number; children: ReactNode }) {
  return <View style={[styles.phone, { height }]}>{children}</View>;
}

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <View style={styles.field}>
      <Text style={styles.fieldLabel}>{label}</Text>
      {children}
    </View>
  );
}

export interface Choice<T extends string> {
  value: T;
  label: string;
}

/** One-of choice as a wrapping row of pills. */
export function Choices<T extends string>({
  options,
  value,
  onChange,
}: {
  options: Choice<T>[];
  value: T;
  onChange: (value: T) => void;
}) {
  return (
    <View style={styles.choices} accessibilityRole="radiogroup">
      {options.map((o) => {
        const on = o.value === value;
        return (
          <Pressable
            key={o.value}
            onPress={() => onChange(o.value)}
            accessibilityRole="radio"
            accessibilityLabel={o.label}
            accessibilityState={{ checked: on }}
            hitSlop={4}
            style={({ pressed }) => [
              styles.choice,
              on && styles.choiceOn,
              pressed && !on && styles.choicePressed,
            ]}
          >
            <Text style={[styles.choiceText, on && styles.choiceTextOn]}>{o.label}</Text>
          </Pressable>
        );
      })}
    </View>
  );
}

export function Toggle({
  label,
  value,
  onChange,
}: {
  label: string;
  value: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <Pressable
      onPress={() => onChange(!value)}
      accessibilityRole="switch"
      accessibilityLabel={label}
      accessibilityState={{ checked: value }}
      style={styles.toggle}
    >
      <Text style={styles.toggleLabel}>{label}</Text>
      <View style={[styles.track, value && styles.trackOn]}>
        <View style={[styles.knob, value && styles.knobOn]} />
      </View>
    </Pressable>
  );
}

export function ActionButton({
  icon,
  label,
  onPress,
}: {
  icon: IconName;
  label: string;
  onPress: () => void;
}) {
  return (
    <Pressable
      onPress={onPress}
      accessibilityRole="button"
      accessibilityLabel={label}
      style={({ pressed }) => [styles.action, pressed && styles.actionPressed]}
    >
      <Icon name={icon} size={16} color={brand.ink} />
      <Text style={styles.actionText}>{label}</Text>
    </Pressable>
  );
}

/** One line saying what the demo just did. */
export function Status({ children }: { children: string }) {
  return (
    <Text style={styles.status} accessibilityLiveRegion="polite">
      {children}
    </Text>
  );
}

/**
 * Fades and lifts its content in on mount; remount it (new `key`) to replay. 180 ms, native
 * driver; instant under reduced motion.
 */
export function Entrance({
  reducedMotion,
  lift = 12,
  children,
}: {
  reducedMotion: boolean;
  lift?: number;
  children: ReactNode;
}) {
  const [v] = useState(() => new Animated.Value(reducedMotion ? 1 : 0));
  useEffect(() => {
    if (reducedMotion) return v.setValue(1);
    const anim = Animated.timing(v, {
      toValue: 1,
      duration: 180,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: true,
    });
    anim.start();
    return () => anim.stop();
  }, [reducedMotion, v]);
  return (
    <Animated.View
      style={{
        opacity: v,
        transform: [{ translateY: v.interpolate({ inputRange: [0, 1], outputRange: [lift, 0] }) }],
      }}
    >
      {children}
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  navColumn: { gap: spacing.xs, width: 216 },
  navRow: { gap: spacing.sm, paddingVertical: spacing.xs },
  navItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    minHeight: 44,
    outlineColor: brand.primary,
  },
  navItemVertical: { paddingHorizontal: spacing.md, borderRadius: radius.md },
  navItemPill: {
    paddingHorizontal: spacing.lg,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: brand.cardShade,
  },
  navItemOn: { backgroundColor: brand.cardShade, borderColor: brand.cardShade },
  navItemPressed: { backgroundColor: brand.cardShade },
  navIndex: { ...type.caption, color: brand.inkMuted, fontVariant: ['tabular-nums'] },
  navLabel: { ...type.caption, color: brand.inkMuted, flexShrink: 1 },
  navTextOn: { color: brand.ink },
  stage: { gap: spacing.lg },
  stageWide: { flexDirection: 'row', alignItems: 'flex-start' },
  canvas: {
    backgroundColor: brand.cardShade,
    borderRadius: 28,
    padding: spacing.lg,
    alignItems: 'center',
    gap: spacing.lg,
  },
  canvasWide: { flex: 1, padding: 40 },
  panel: {
    gap: spacing.lg,
    padding: spacing.lg,
    borderRadius: radius.lg,
    borderWidth: 1,
    borderColor: brand.cardShade,
    backgroundColor: brand.card,
  },
  panelWide: { width: 300 },
  panelTitle: { ...type.label, color: brand.ink },
  phone: {
    width: '100%',
    maxWidth: 390,
    borderRadius: 32,
    overflow: 'hidden',
    backgroundColor: brand.card,
  },
  field: { gap: spacing.sm },
  fieldLabel: { ...type.caption, color: brand.inkMuted },
  choices: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  choice: {
    outlineColor: brand.primary,
    minHeight: 44,
    paddingHorizontal: 14,
    justifyContent: 'center',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: brand.cardShade,
    backgroundColor: brand.card,
  },
  choiceOn: { backgroundColor: brand.ink, borderColor: brand.ink },
  choicePressed: { backgroundColor: brand.cardShade },
  choiceText: { ...type.caption, color: brand.ink },
  choiceTextOn: { color: brand.onPrimary },
  toggle: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: spacing.md,
    outlineColor: brand.primary,
    minHeight: 44,
  },
  toggleLabel: { ...type.caption, color: brand.ink, flexShrink: 1 },
  track: {
    width: 40,
    height: 24,
    borderRadius: 12,
    padding: 3,
    backgroundColor: brand.cardShade,
  },
  trackOn: { backgroundColor: brand.primary },
  knob: { width: 18, height: 18, borderRadius: 9, backgroundColor: brand.card },
  knobOn: { transform: [{ translateX: 16 }] },
  action: {
    flexDirection: 'row',
    alignItems: 'center',
    alignSelf: 'flex-start',
    gap: spacing.sm,
    outlineColor: brand.primary,
    minHeight: 44,
    paddingHorizontal: 14,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: brand.cardShade,
    backgroundColor: brand.card,
  },
  actionPressed: { backgroundColor: brand.cardShade },
  actionText: { ...type.caption, color: brand.ink },
  status: { ...type.caption, color: brand.inkMuted },
});
