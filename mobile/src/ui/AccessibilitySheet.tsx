// Accessibility bottom-sheet panel opened from the left button of CloudNavBar.
// Minimal, breathable layout for text size (with live preview), high contrast, reduce motion,
// auto-speak of new chat replies, and color-vision palettes.
import { useEffect, useState } from 'react';
import { Animated, Platform, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import { fill, t } from '@/i18n';
import {
  COLOR_VISION_MODES,
  isDefaultAccessibility,
  resetAccessibility,
  setAccessibility,
  TEXT_SCALE_STEPS,
  textScaleFromIndex,
  textScaleIndex,
  type ColorVisionMode,
  type TextScale,
} from '@/state/accessibility';

import { BottomSheet } from './BottomSheet';
import { Icon } from './icons/Icon';
import { Slider } from './Slider';
import { brand, fonts, radius, resolveBrand, spacing, type } from './theme/tokens';
import { scaleSize, useAccessibilityTheme } from './useAccessibilityTheme';
import { useReducedMotion, useSystemReducedMotion } from './useReducedMotion';

const copy = t.accessibilityPanel;
const USE_NATIVE_DRIVER = Platform.OS !== 'web';
const SWITCH_TRAVEL = 20;

const LEVEL_KEY: Record<TextScale, keyof typeof copy.textSize.levels> = {
  1: 'normal',
  1.15: 'large',
  1.3: 'larger',
  1.45: 'extra',
};

export interface AccessibilitySheetProps {
  open: boolean;
  onClose: () => void;
  bottom?: number;
  reducedMotion?: boolean;
}

export function AccessibilitySheet({
  open,
  onClose,
  bottom = 0,
  reducedMotion = false,
}: AccessibilitySheetProps) {
  return (
    <BottomSheet open={open} onClose={onClose} bottom={bottom} reducedMotion={reducedMotion}>
      {(close) => <AccessibilityContent onClose={close} reducedMotion={reducedMotion} />}
    </BottomSheet>
  );
}

/** A labelled on/off row (`accessibilityRole="switch"`); the settings sheet reuses it. */
export function SwitchRow({
  title,
  body,
  note,
  value,
  onToggle,
  reduced,
}: {
  title: string;
  body?: string;
  note?: string;
  value: boolean;
  onToggle: () => void;
  reduced: boolean;
}) {
  const { palette, scaled } = useAccessibilityTheme();
  const [knobX] = useState(() => new Animated.Value(value ? SWITCH_TRAVEL : 0));

  useEffect(() => {
    const target = value ? SWITCH_TRAVEL : 0;
    if (reduced) {
      knobX.setValue(target);
      return;
    }
    const anim = Animated.spring(knobX, {
      toValue: target,
      stiffness: 420,
      damping: 28,
      mass: 0.7,
      useNativeDriver: USE_NATIVE_DRIVER,
    });
    anim.start();
    return () => anim.stop();
  }, [knobX, reduced, value]);

  return (
    <Pressable
      onPress={onToggle}
      accessibilityRole="switch"
      accessibilityLabel={title}
      accessibilityHint={body}
      accessibilityState={{ checked: value }}
      aria-checked={value}
      style={({ pressed }) => [styles.switchRow, pressed && { backgroundColor: palette.cardShade }]}
    >
      <View style={styles.switchTexts}>
        <Text style={[styles.sectionTitle, scaled.label, { color: palette.ink }]}>{title}</Text>
        {body ? (
          <Text style={[styles.sectionBody, scaled.caption, { color: palette.inkMuted }]}>
            {body}
          </Text>
        ) : null}
        {note ? (
          <Text style={[styles.note, scaled.caption, { color: palette.primary }]}>{note}</Text>
        ) : null}
      </View>
      <View
        style={[
          styles.switchTrack,
          {
            backgroundColor: value ? palette.primary : palette.cardShade,
            borderColor: value ? palette.primary : palette.primarySoft,
          },
        ]}
        pointerEvents="none"
      >
        <Animated.View
          style={[
            styles.switchKnob,
            {
              backgroundColor: palette.onPrimary,
              borderColor: value ? palette.primary : palette.inkMuted,
              transform: [{ translateX: knobX }],
            },
          ]}
        />
      </View>
    </Pressable>
  );
}

function AccessibilityContent({
  onClose,
  reducedMotion,
}: {
  onClose: () => void;
  reducedMotion: boolean;
}) {
  const {
    palette,
    scaled,
    textScale,
    highContrast,
    reduceMotion,
    autoSpeakReplies,
    colorVision,
    borderWidth,
  } = useAccessibilityTheme();
  const reduced = useReducedMotion() || reducedMotion;
  const systemReduced = useSystemReducedMotion();

  const stepIndex = textScaleIndex(textScale);
  const pct = Math.round(textScale * 100);
  const levelName = copy.textSize.levels[LEVEL_KEY[textScale]];
  const pctLabel = fill(copy.textSize.percent, { pct });
  const isDefault = isDefaultAccessibility({
    textScale,
    highContrast,
    reduceMotion,
    autoSpeakReplies,
    colorVision,
  });

  const canDecrease = stepIndex > 0;
  const canIncrease = stepIndex < TEXT_SCALE_STEPS.length - 1;
  const dividerColor = highContrast ? palette.ink : palette.cardShade;

  const setStep = (idx: number) => {
    setAccessibility({ textScale: textScaleFromIndex(idx) });
  };

  return (
    <>
      <View style={styles.header}>
        <Text
          style={[styles.title, scaled.title, { color: palette.ink }]}
          accessibilityRole="header"
        >
          {copy.title}
        </Text>
        <View style={styles.headerActions}>
          {!isDefault && (
            <Pressable
              onPress={resetAccessibility}
              hitSlop={6}
              accessibilityRole="button"
              accessibilityLabel={copy.reset}
              accessibilityHint={copy.resetHint}
              style={({ pressed }) => [
                styles.resetButton,
                pressed && { backgroundColor: palette.cardShade },
              ]}
            >
              <Icon name="rotateCcw" size={14} color={palette.primary} strokeWidth={2.2} />
              <Text style={[styles.resetText, { color: palette.primary }]}>{copy.reset}</Text>
            </Pressable>
          )}
          <Pressable
            onPress={onClose}
            accessibilityRole="button"
            accessibilityLabel={copy.close}
            style={({ pressed }) => [
              styles.close,
              { outlineColor: palette.primary },
              pressed && { backgroundColor: palette.cardShade },
            ]}
          >
            <Icon name="x" size={20} color={palette.ink} />
          </Pressable>
        </View>
      </View>

      <ScrollView
        style={styles.list}
        contentContainerStyle={styles.listContent}
        showsVerticalScrollIndicator={false}
      >
        {/* 1. Text size + live preview */}
        <View style={[styles.section, styles.firstSection]}>
          <View style={styles.sectionHead}>
            <View style={styles.sectionHeadText}>
              <Text style={[styles.sectionTitle, scaled.label, { color: palette.ink }]}>
                {copy.textSize.title}
              </Text>
              <Text style={[styles.sectionBody, scaled.caption, { color: palette.inkMuted }]}>
                {copy.textSize.body}
              </Text>
            </View>
            <Text style={[styles.valueText, { color: palette.inkMuted }]}>{pctLabel}</Text>
          </View>

          <View style={styles.sliderRow}>
            <Pressable
              onPress={() => canDecrease && setStep(stepIndex - 1)}
              disabled={!canDecrease}
              hitSlop={4}
              accessibilityRole="button"
              accessibilityLabel={copy.textSize.decrease}
              accessibilityState={{ disabled: !canDecrease }}
              style={({ pressed }) => [
                styles.stepBtn,
                {
                  backgroundColor: pressed ? palette.cardShade : palette.card,
                  borderColor: highContrast ? palette.ink : palette.cardShade,
                  borderWidth,
                },
                !canDecrease && styles.stepBtnDisabled,
              ]}
            >
              <Icon name="minus" size={16} color={palette.ink} strokeWidth={2.2} />
            </Pressable>
            <View style={styles.sliderFlex}>
              <Slider
                value={stepIndex}
                min={0}
                max={TEXT_SCALE_STEPS.length - 1}
                step={1}
                onChange={setStep}
                label={copy.textSize.title}
                valueText={`${levelName} ${pctLabel}`}
                hint={copy.textSize.sliderHint}
              />
            </View>
            <Pressable
              onPress={() => canIncrease && setStep(stepIndex + 1)}
              disabled={!canIncrease}
              hitSlop={4}
              accessibilityRole="button"
              accessibilityLabel={copy.textSize.increase}
              accessibilityState={{ disabled: !canIncrease }}
              style={({ pressed }) => [
                styles.stepBtn,
                {
                  backgroundColor: pressed ? palette.cardShade : palette.card,
                  borderColor: highContrast ? palette.ink : palette.cardShade,
                  borderWidth,
                },
                !canIncrease && styles.stepBtnDisabled,
              ]}
            >
              <Icon name="plus" size={16} color={palette.ink} strokeWidth={2.2} />
            </Pressable>
          </View>

          <View
            style={[
              styles.segmented,
              {
                backgroundColor: palette.cardShade,
                borderColor: highContrast ? palette.ink : palette.cardShade,
                borderWidth: highContrast ? borderWidth : 0,
              },
            ]}
            accessibilityRole="radiogroup"
            accessibilityLabel={copy.textSize.title}
          >
            {TEXT_SCALE_STEPS.map((scale, idx) => {
              const on = idx === stepIndex;
              const label = copy.textSize.levels[LEVEL_KEY[scale]];
              return (
                <Pressable
                  key={scale}
                  onPress={() => setStep(idx)}
                  hitSlop={4}
                  accessibilityRole="radio"
                  accessibilityLabel={label}
                  accessibilityState={{ checked: on }}
                  style={({ pressed }) => [
                    styles.segment,
                    on && { backgroundColor: palette.primary },
                    !on && pressed && { backgroundColor: palette.card },
                  ]}
                >
                  <Text
                    style={[styles.segmentText, { color: on ? palette.onPrimary : palette.ink }]}
                    numberOfLines={1}
                  >
                    {label}
                  </Text>
                </Pressable>
              );
            })}
          </View>

          {/* Live text preview */}
          <View
            style={[
              styles.previewBox,
              {
                backgroundColor: palette.cardShade,
                borderColor: palette.ink,
                borderWidth: highContrast ? borderWidth : 0,
              },
            ]}
          >
            <Text
              style={[
                styles.previewTitle,
                {
                  color: palette.ink,
                  fontSize: scaleSize(type.label.fontSize, textScale),
                  lineHeight: scaleSize(type.label.lineHeight, textScale),
                },
              ]}
            >
              {copy.textSize.previewTitle}
            </Text>
            <Text
              style={[
                styles.previewBody,
                {
                  color: palette.inkMuted,
                  fontSize: scaleSize(14, textScale),
                  lineHeight: scaleSize(20, textScale),
                },
              ]}
            >
              {copy.textSize.previewBody}
            </Text>
          </View>
        </View>

        <View style={[styles.divider, { backgroundColor: dividerColor }]} />

        {/* 2. High contrast */}
        <SwitchRow
          title={copy.highContrast.title}
          body={copy.highContrast.body}
          value={highContrast}
          onToggle={() => setAccessibility({ highContrast: !highContrast })}
          reduced={reduced}
        />

        <View style={[styles.divider, { backgroundColor: dividerColor }]} />

        {/* 3. Reduce motion */}
        <SwitchRow
          title={copy.reduceMotion.title}
          body={copy.reduceMotion.body}
          note={systemReduced ? copy.reduceMotion.systemActive : undefined}
          value={reduceMotion}
          onToggle={() => setAccessibility({ reduceMotion: !reduceMotion })}
          reduced={reduced}
        />

        <View style={[styles.divider, { backgroundColor: dividerColor }]} />

        <SwitchRow
          title={copy.autoSpeakReplies.title}
          body={copy.autoSpeakReplies.body}
          value={autoSpeakReplies}
          onToggle={() => setAccessibility({ autoSpeakReplies: !autoSpeakReplies })}
          reduced={reduced}
        />

        <View style={[styles.divider, { backgroundColor: dividerColor }]} />

        {/* 4. Color vision palettes + icon/text status strip */}
        <View style={[styles.section, styles.lastSection]}>
          <View style={styles.sectionHeadText}>
            <Text style={[styles.sectionTitle, scaled.label, { color: palette.ink }]}>
              {copy.colorVision.title}
            </Text>
            <Text style={[styles.sectionBody, scaled.caption, { color: palette.inkMuted }]}>
              {copy.colorVision.body}
            </Text>
          </View>

          <View
            style={styles.visionList}
            accessibilityRole="radiogroup"
            accessibilityLabel={copy.colorVision.title}
          >
            {COLOR_VISION_MODES.map((mode: ColorVisionMode) => {
              const on = colorVision === mode;
              const info = copy.colorVision.modes[mode];
              const swatchPalette = resolveBrand(mode, highContrast);
              return (
                <Pressable
                  key={mode}
                  onPress={() => setAccessibility({ colorVision: mode })}
                  accessibilityRole="radio"
                  accessibilityLabel={info.label}
                  accessibilityHint={info.hint}
                  accessibilityState={{ checked: on }}
                  style={({ pressed }) => [
                    styles.visionOption,
                    {
                      backgroundColor: on || pressed ? palette.cardShade : palette.card,
                      borderColor: on
                        ? palette.primary
                        : highContrast
                          ? palette.ink
                          : palette.cardShade,
                      borderWidth: on || highContrast ? 1.5 : 1,
                    },
                  ]}
                >
                  <View style={styles.swatches} aria-hidden>
                    <View style={[styles.swatchDot, { backgroundColor: swatchPalette.primary }]} />
                    <View style={[styles.swatchDot, { backgroundColor: swatchPalette.online }]} />
                    <View style={[styles.swatchDot, { backgroundColor: swatchPalette.alert }]} />
                  </View>
                  <View style={styles.visionTexts}>
                    <Text style={[styles.visionLabel, scaled.body, { color: palette.ink }]}>
                      {info.label}
                    </Text>
                    <Text style={[styles.visionHint, scaled.caption, { color: palette.inkMuted }]}>
                      {info.hint}
                    </Text>
                  </View>
                  <View
                    style={[
                      styles.radioCircle,
                      {
                        backgroundColor: on ? palette.primary : palette.card,
                        borderColor: on ? palette.primary : palette.primarySoft,
                      },
                    ]}
                    aria-hidden
                  >
                    {on && (
                      <Icon name="check" size={12} color={palette.onPrimary} strokeWidth={2.8} />
                    )}
                  </View>
                </Pressable>
              );
            })}
          </View>

          {/* Status chips proving color + icon + text always travel together */}
          <View style={styles.statusRow}>
            <View
              style={[
                styles.statusChip,
                { backgroundColor: palette.cardShade, borderColor: palette.primary },
              ]}
            >
              <Icon name="circleCheck" size={14} color={palette.primary} strokeWidth={2.2} />
              <Text style={[styles.statusText, { color: palette.ink }]}>
                {copy.colorVision.statuses.near}
              </Text>
            </View>
            <View
              style={[
                styles.statusChip,
                { backgroundColor: palette.alert, borderColor: palette.alert },
              ]}
            >
              <Icon name="triangleAlert" size={14} color={palette.onPrimary} strokeWidth={2.2} />
              <Text style={[styles.statusText, { color: palette.onPrimary }]}>
                {copy.colorVision.statuses.alert}
              </Text>
            </View>
            <View
              style={[
                styles.statusChip,
                styles.statusChipDashed,
                { backgroundColor: palette.card, borderColor: palette.inkMuted },
              ]}
            >
              <Icon name="eyeOff" size={14} color={palette.inkMuted} strokeWidth={2.2} />
              <Text style={[styles.statusText, { color: palette.inkMuted }]}>
                {copy.colorVision.statuses.unseen}
              </Text>
            </View>
          </View>
        </View>
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingLeft: 20,
    paddingRight: 10,
    paddingBottom: spacing.md,
    gap: spacing.sm,
  },
  title: {
    ...type.title,
    color: brand.ink,
    flexShrink: 1,
  },
  headerActions: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
  },
  resetButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
    minHeight: 36,
    paddingHorizontal: 10,
    borderRadius: radius.pill,
  },
  resetText: {
    ...type.caption,
    fontFamily: fonts.semibold,
  },
  close: {
    width: 44,
    height: 44,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
  },
  list: { flexGrow: 0 },
  listContent: {
    paddingHorizontal: 20,
    paddingTop: spacing.xs,
    paddingBottom: spacing.lg,
  },
  section: {
    paddingVertical: spacing.lg,
    gap: spacing.md,
  },
  firstSection: {
    paddingTop: spacing.xs,
  },
  lastSection: {
    paddingBottom: spacing.xs,
  },
  divider: {
    height: 1,
  },
  sectionHead: {
    flexDirection: 'row',
    alignItems: 'baseline',
    justifyContent: 'space-between',
    gap: spacing.md,
  },
  sectionHeadText: {
    flex: 1,
    gap: 2,
  },
  sectionTitle: {
    ...type.label,
    color: brand.ink,
  },
  sectionBody: {
    ...type.caption,
    color: brand.inkMuted,
  },
  note: {
    ...type.caption,
    fontFamily: fonts.semibold,
    marginTop: spacing.xs,
  },
  valueText: {
    ...type.caption,
    fontFamily: fonts.semibold,
    fontVariant: ['tabular-nums'],
  },
  sliderRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
  },
  sliderFlex: {
    flex: 1,
  },
  stepBtn: {
    width: 36,
    height: 36,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
  },
  stepBtnDisabled: {
    opacity: 0.35,
  },
  segmented: {
    flexDirection: 'row',
    padding: 3,
    borderRadius: radius.md,
    gap: 3,
  },
  segment: {
    flex: 1,
    minHeight: 36,
    paddingHorizontal: 6,
    borderRadius: radius.md - 2,
    alignItems: 'center',
    justifyContent: 'center',
  },
  segmentText: {
    ...type.caption,
    fontFamily: fonts.semibold,
    fontSize: 12,
    lineHeight: 16,
  },
  previewBox: {
    borderRadius: radius.md,
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    gap: spacing.xs,
  },
  previewTitle: {
    fontFamily: fonts.bold,
  },
  previewBody: {
    fontFamily: fonts.regular,
  },
  switchRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.lg,
    marginHorizontal: -spacing.sm,
    paddingHorizontal: spacing.sm,
    borderRadius: radius.md,
    gap: spacing.lg,
  },
  switchTexts: {
    flex: 1,
    gap: 2,
  },
  switchTrack: {
    width: 48,
    height: 28,
    borderRadius: 14,
    borderWidth: 1,
    padding: 2,
    justifyContent: 'center',
  },
  switchKnob: {
    width: 22,
    height: 22,
    borderRadius: 11,
    borderWidth: 1,
  },
  visionList: {
    gap: spacing.sm,
  },
  visionOption: {
    minHeight: 52,
    borderRadius: radius.md,
    paddingHorizontal: spacing.md,
    paddingVertical: 10,
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
  },
  swatches: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
  },
  swatchDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
  },
  visionTexts: {
    flex: 1,
    gap: 1,
  },
  visionLabel: {
    fontFamily: fonts.semibold,
  },
  visionHint: {
    ...type.caption,
  },
  radioCircle: {
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 1.5,
    alignItems: 'center',
    justifyContent: 'center',
  },
  statusRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: spacing.sm,
    paddingTop: spacing.xs,
  },
  statusChip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 5,
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderRadius: radius.pill,
    borderWidth: 1,
  },
  statusChipDashed: {
    borderStyle: 'dashed',
  },
  statusText: {
    ...type.caption,
    fontFamily: fonts.semibold,
  },
});
