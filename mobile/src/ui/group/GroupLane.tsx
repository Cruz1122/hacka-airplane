// The guide's view of the group: a vertical line from the front guide down to the rear guide (or
// the farthest reach with one guide), one marker per visitor ON the line, placed by t and spread
// along it so markers never overlap (laneLayout.ts). Each marker shows that member's own Pet
// wearing the skin sent over the radio, with an expression for its zone (near happy, mid curious,
// far sad, unseen asleep) and an outer ring that also reads without color (solid, double, dashed,
// dotted). On a one-guide lane the dashed red alert line itself is adjustable by dragging up/down
// or tapping - / +.
import { memo, useEffect, useMemo, useRef, useState } from 'react';
import {
  Animated,
  Easing,
  Platform,
  Pressable,
  StyleSheet,
  Text,
  View,
  type AccessibilityActionEvent,
  type GestureResponderEvent,
} from 'react-native';
import Svg, { Circle, Line } from 'react-native-svg';

import type { DotStatus, Lane } from '@/core/group/lane';
import { GROUP_POLICY } from '@/core/group/policy';
import type { GuideMember, MemberId } from '@/core/group/types';
import { fill, t } from '@/i18n';
import { wornFromMember } from '@/state/petLook';

import { Icon } from '../icons/Icon';
import { PET_FACE_VIEWBOX, type PetAccessory, type PetEmotion, type PetTint } from '../pet/petCore';
import { PetStill } from '../pet/PetStill';
import { brand, fonts, radius, spacing, type } from '../theme/tokens';
import { useAccessibilityTheme } from '../useAccessibilityTheme';
import { useReducedMotion } from '../useReducedMotion';
import { layoutLane, type PlacedDot } from './laneLayout';

/** Diameter of a lane marker. */
export const DOT = 56;
/** Space between two dots on the line. */
const DOT_GAP = 14;
/** Space between a guide marker and the nearest dot. */
const END_GAP = 14;
/** Room above the top guide and below the bottom end for the guide markers (plus hat crown). */
const PAD = DOT / 2 + 10;
const LABEL_GAP = 10;
const LABEL_ROW = 24;
const MOVE_MS = 500;
/** Height of a lane mark's label, which sits just above its line. */
const MARK_ROW = 18;
/** Vertical drag pixels per alert-distance step while adjusting directly on the line. */
const DRAG_PX_PER_STEP = 14;
/** Maximum visual nudge of the alert line while the user drags it. */
const DRAG_VISUAL_CLAMP = 22;

const { min: ALERT_MIN, max: ALERT_MAX, step: ALERT_STEP } = GROUP_POLICY.alertMeters;

const clampAlert = (v: number) =>
  Math.max(ALERT_MIN, Math.min(ALERT_MAX, Math.round(v / ALERT_STEP) * ALERT_STEP));

const NATIVE_HIDDEN =
  Platform.OS === 'web'
    ? undefined
    : ({
        accessible: false,
        accessibilityElementsHidden: true,
        importantForAccessibility: 'no-hide-descendants',
      } as const);

export const zoneLabel = (s: DotStatus) => t.group.zones[s];

const EMOTION: Record<DotStatus, PetEmotion> = {
  near: 'happy',
  mid: 'curious',
  far: 'sad',
  unseen: 'sleepy',
};

/** Outer ring that names the zone without color: solid, double, dashed, dotted. */
function ZoneRing({
  status,
  size,
  guide = false,
}: {
  status: DotStatus;
  size: number;
  guide?: boolean;
}) {
  const { palette } = useAccessibilityTheme();
  const c = size / 2;
  const w = Math.max(1.8, size / 22);
  const r = c - w / 2;
  if (guide) {
    return (
      <Svg
        width={size}
        height={size}
        style={StyleSheet.absoluteFill}
        pointerEvents="none"
        aria-hidden
        {...NATIVE_HIDDEN}
      >
        <Circle cx={c} cy={c} r={r} fill="none" stroke={palette.ink} strokeWidth={w} />
      </Svg>
    );
  }
  const stroke =
    status === 'far' ? palette.alert : status === 'unseen' ? palette.inkMuted : palette.primary;
  return (
    <Svg
      width={size}
      height={size}
      style={StyleSheet.absoluteFill}
      pointerEvents="none"
      aria-hidden
      {...NATIVE_HIDDEN}
    >
      <Circle
        cx={c}
        cy={c}
        r={r}
        fill="none"
        stroke={stroke}
        strokeWidth={w}
        strokeDasharray={
          status === 'far'
            ? `${w * 2.4} ${w * 1.8}`
            : status === 'unseen'
              ? `${w * 0.9} ${w * 1.8}`
              : undefined
        }
        strokeLinecap={status === 'unseen' ? 'round' : 'butt'}
      />
      {status === 'mid' && (
        <Circle
          cx={c}
          cy={c}
          r={Math.max(1, r - w * 1.9)}
          fill="none"
          stroke={palette.primarySoft}
          strokeWidth={Math.max(1.2, w * 0.85)}
        />
      )}
    </Svg>
  );
}

/**
 * A Pet floating on a soft circular backdrop with an airy white gap and outer zone ring so its
 * hat/skin crowns cleanly instead of getting clipped inside a harsh dark circle.
 */
export const PetDot = memo(function PetDot({
  status,
  size,
  accessory,
  tint,
  guide = false,
}: {
  status: DotStatus;
  size: number;
  accessory?: PetAccessory;
  tint?: PetTint;
  /** Guides get an ink outer ring; unseen visitors sit on muted grey. */
  guide?: boolean;
}) {
  const { palette } = useAccessibilityTheme();
  const gap = Math.max(4, Math.round(size * 0.16));
  const disc = Math.max(16, size - gap);
  const discOffset = (size - disc) / 2;
  const petSize = disc;
  const bg = status === 'unseen' && !guide ? palette.inkMuted : palette.primary;
  const badgeSize = Math.max(14, Math.round(size * 0.34));
  return (
    <View style={[styles.petDotRoot, { width: size, height: size }]}>
      <View
        style={[
          styles.discHalo,
          {
            backgroundColor: palette.card,
            left: discOffset - 2,
            top: discOffset - 2,
            width: disc + 4,
            height: disc + 4,
            borderRadius: (disc + 4) / 2,
          },
        ]}
      />
      <ZoneRing status={status} size={size} guide={guide} />
      <View
        style={[
          styles.disc,
          {
            left: discOffset,
            top: discOffset,
            width: disc,
            height: disc,
            borderRadius: disc / 2,
            backgroundColor: bg,
          },
        ]}
      >
        <PetStill
          size={petSize}
          emotion={guide ? 'happy' : EMOTION[status]}
          accessory={accessory}
          tint={tint}
          crop={PET_FACE_VIEWBOX}
        />
      </View>
      {status === 'unseen' && !guide && (
        <View
          style={[
            styles.badge,
            {
              borderColor: palette.card,
              backgroundColor: palette.inkMuted,
              width: badgeSize,
              height: badgeSize,
              borderRadius: badgeSize / 2,
            },
          ]}
        >
          <Icon
            name="eyeOff"
            size={Math.max(8, Math.round(badgeSize * 0.56))}
            color={palette.onPrimary}
            strokeWidth={2.4}
          />
        </View>
      )}
    </View>
  );
});

/** Alert ring around an alerting dot; pulses outward unless motion is reduced. */
function AlertRing() {
  const { palette } = useAccessibilityTheme();
  const reduced = useReducedMotion();
  const [v] = useState(() => new Animated.Value(0));
  useEffect(() => {
    if (reduced) return v.setValue(0);
    const loop = Animated.loop(
      Animated.timing(v, {
        toValue: 1,
        duration: 1200,
        easing: Easing.out(Easing.quad),
        useNativeDriver: Platform.OS !== 'web',
      }),
    );
    loop.start();
    return () => loop.stop();
  }, [reduced, v]);
  return (
    <>
      <View style={[styles.ring, { borderColor: palette.alert }]} />
      {!reduced && (
        <Animated.View
          style={[
            styles.ring,
            {
              borderColor: palette.alert,
              opacity: v.interpolate({ inputRange: [0, 1], outputRange: [0.7, 0] }),
              transform: [{ scale: v.interpolate({ inputRange: [0, 1], outputRange: [1, 1.45] }) }],
            },
          ]}
        />
      )}
    </>
  );
}

function VisitorDot({ place, cx }: { place: PlacedDot; cx: number }) {
  const { palette, scaled } = useAccessibilityTheme();
  const { dot, y, side } = place;
  const wears = wornFromMember(dot.look, 'visitor');
  const reduced = useReducedMotion();
  const [pos] = useState(() => new Animated.Value(y));
  useEffect(() => {
    if (reduced) return pos.setValue(y);
    const a = Animated.timing(pos, {
      toValue: y,
      duration: MOVE_MS,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: Platform.OS !== 'web',
    });
    a.start();
    return () => a.stop();
  }, [pos, y, reduced]);
  return (
    <Animated.View
      accessible
      accessibilityRole="text"
      accessibilityLabel={fill(dot.alerting ? t.group.dotAlert : t.group.dot, {
        name: dot.name,
        zone: zoneLabel(dot.status),
      })}
      style={[styles.row, { top: -DOT / 2, transform: [{ translateY: pos }] }]}
    >
      <View style={[styles.slot, { left: cx - DOT / 2 }]}>
        {dot.alerting && <AlertRing />}
        <PetDot
          status={dot.status}
          size={DOT}
          accessory={wears.accessory}
          tint={wears.tint}
        />
        {dot.alerting && (
          <View
            style={[
              styles.badge,
              { borderColor: palette.card, backgroundColor: palette.alert },
            ]}
          >
            <Icon name="triangleAlert" size={11} color={palette.onPrimary} strokeWidth={2.6} />
          </View>
        )}
      </View>
      <View
        style={[
          styles.label,
          side === 'right'
            ? { left: cx + DOT / 2 + LABEL_GAP, right: spacing.xs }
            : { left: spacing.xs, width: cx - DOT / 2 - LABEL_GAP - spacing.xs, alignItems: 'flex-end' },
        ]}
      >
        <Text
          numberOfLines={1}
          style={[
            styles.name,
            scaled.label,
            { color: palette.ink },
            side === 'left' && styles.nameLeft,
            dot.status === 'unseen' && { color: palette.inkMuted },
            dot.alerting && { fontFamily: fonts.bold, color: palette.alert },
          ]}
        >
          {dot.name}
        </Text>
      </View>
    </Animated.View>
  );
}

/** What a Pet wears: an accessory and its tint, both optional. */
export interface Wears {
  accessory?: PetAccessory;
  tint?: PetTint;
}

function GuideMarker({
  guide,
  selfId,
  selfWears,
  y,
  cx,
}: {
  guide: GuideMember;
  selfId: MemberId;
  selfWears?: Wears;
  y: number;
  cx: number;
}) {
  const { palette, scaled } = useAccessibilityTheme();
  const wears =
    guide.id === selfId && selfWears !== undefined
      ? selfWears
      : wornFromMember(guide.look, 'guide');
  const name = guide.id === selfId ? fill(t.group.you, { name: guide.name }) : guide.name;
  const label = fill(guide.slot === 'front' ? t.group.guideFront : t.group.guideRear, { name });
  return (
    <View
      accessible
      accessibilityRole="text"
      accessibilityLabel={label}
      style={[styles.row, { top: y - DOT / 2 }]}
    >
      <View style={[styles.slot, { left: cx - DOT / 2 }]}>
        <PetDot status="near" size={DOT} accessory={wears.accessory} tint={wears.tint} guide />
      </View>
      <View style={[styles.label, { left: cx + DOT / 2 + LABEL_GAP, right: spacing.xs }]}>
        <Text
          numberOfLines={1}
          style={[styles.guideName, scaled.label, { fontFamily: fonts.bold, color: palette.ink }]}
        >
          {name}
        </Text>
      </View>
    </View>
  );
}

/**
 * Minimal draggable handle sitting right on the dashed red alert line: grab the pill (or anywhere
 * along the line band) and drag up/down to change the alert distance in 5 m steps.
 */
function AlertLineDragHandle({
  meters,
  onChange,
  onDragOffset,
  y,
}: {
  meters: number;
  onChange: (next: number) => void;
  onDragOffset: (dy: number) => void;
  y: number;
}) {
  const g = t.group;
  const valueText = fill(g.meters, { m: Math.round(meters) });
  const dragStartYRef = useRef(0);
  const startMetersRef = useRef(meters);
  const lastSentRef = useRef(meters);
  const [dragging, setDragging] = useState(false);

  const onDragStart = (e: GestureResponderEvent) => {
    dragStartYRef.current = e.nativeEvent.pageY;
    startMetersRef.current = meters;
    lastSentRef.current = meters;
    setDragging(true);
  };

  const onDragMove = (e: GestureResponderEvent) => {
    const dy = e.nativeEvent.pageY - dragStartYRef.current;
    const clampedDy = Math.max(-DRAG_VISUAL_CLAMP, Math.min(DRAG_VISUAL_CLAMP, dy * 0.45));
    onDragOffset(clampedDy);
    const deltaSteps = Math.round(dy / DRAG_PX_PER_STEP);
    const next = clampAlert(startMetersRef.current + deltaSteps * ALERT_STEP);
    if (next !== lastSentRef.current) {
      lastSentRef.current = next;
      onChange(next);
    }
  };

  const onDragEnd = () => {
    setDragging(false);
    onDragOffset(0);
  };

  const onAction = (e: AccessibilityActionEvent) => {
    const delta = e.nativeEvent.actionName === 'increment' ? ALERT_STEP : -ALERT_STEP;
    const next = clampAlert(meters + delta);
    if (next !== meters) onChange(next);
  };

  return (
    <View
      onStartShouldSetResponder={() => true}
      onMoveShouldSetResponder={() => true}
      onResponderTerminationRequest={() => false}
      onResponderGrant={onDragStart}
      onResponderMove={onDragMove}
      onResponderRelease={onDragEnd}
      onResponderTerminate={onDragEnd}
      style={[styles.alertDragBand, { top: y - 18 }]}
    >
      <View
        accessible
        accessibilityRole="adjustable"
        accessibilityLabel={g.alertDistance}
        accessibilityHint={g.alertDistanceHint}
        aria-valuemin={ALERT_MIN}
        aria-valuemax={ALERT_MAX}
        aria-valuenow={meters}
        aria-valuetext={valueText}
        accessibilityActions={[{ name: 'increment' }, { name: 'decrement' }]}
        onAccessibilityAction={onAction}
        style={[styles.alertTag, dragging && styles.alertTagDragging]}
      >
        <Icon name="chevronsUpDown" size={11} color={brand.alert} strokeWidth={2.2} />
        <Text selectable={false} style={styles.alertValueText}>
          {valueText}
        </Text>
      </View>
    </View>
  );
}

/** Quiet - / + stepper used only on two-guide lanes where there is no meter line to drag. */
function AlertStepper({ meters, onChange }: { meters: number; onChange: (next: number) => void }) {
  const g = t.group;
  const valueText = fill(g.meters, { m: Math.round(meters) });
  const stepBy = (delta: number) => {
    const next = clampAlert(meters + delta);
    if (next !== meters) onChange(next);
  };
  const onAction = (e: AccessibilityActionEvent) => {
    stepBy(e.nativeEvent.actionName === 'increment' ? ALERT_STEP : -ALERT_STEP);
  };
  const atMin = meters <= ALERT_MIN;
  const atMax = meters >= ALERT_MAX;
  return (
    <View
      style={styles.stepperPill}
      accessibilityRole="adjustable"
      accessibilityLabel={g.alertDistance}
      accessibilityHint={g.alertDistanceHint}
      aria-valuemin={ALERT_MIN}
      aria-valuemax={ALERT_MAX}
      aria-valuenow={meters}
      aria-valuetext={valueText}
      accessibilityActions={[{ name: 'increment' }, { name: 'decrement' }]}
      onAccessibilityAction={onAction}
    >
      <Pressable
        onPress={() => stepBy(-ALERT_STEP)}
        disabled={atMin}
        accessibilityRole="button"
        accessibilityLabel={g.alertDecrease}
        hitSlop={8}
        style={({ pressed }) => [
          styles.stepBtn,
          atMin && styles.stepBtnDisabled,
          pressed && styles.stepBtnPressed,
        ]}
      >
        <Icon name="minus" size={12} color={brand.ink} strokeWidth={2.4} />
      </Pressable>
      <Text style={styles.stepperValueText}>{valueText}</Text>
      <Pressable
        onPress={() => stepBy(ALERT_STEP)}
        disabled={atMax}
        accessibilityRole="button"
        accessibilityLabel={g.alertIncrease}
        hitSlop={8}
        style={({ pressed }) => [
          styles.stepBtn,
          atMax && styles.stepBtnDisabled,
          pressed && styles.stepBtnPressed,
        ]}
      >
        <Icon name="plus" size={12} color={brand.ink} strokeWidth={2.4} />
      </Pressable>
    </View>
  );
}

/** Lane height that fits `count` dots at full spacing, so a big group scrolls instead of piling. */
export const laneHeightFor = (count: number, twoGuides: boolean) =>
  2 * PAD + (DOT + END_GAP) * (twoGuides ? 2 : 1) + Math.max(0, count - 1) * (DOT + DOT_GAP);

export interface GroupLaneProps {
  lane: Lane;
  /** This phone's member, labelled "(tú)". */
  selfId: MemberId;
  /** What this phone's own Pet wears (optional override over `guide.look`). */
  selfWears?: Wears;
  /** Current alert distance in meters; when paired with `onAlertMetersChange`, adjustable on the lane. */
  alertMeters?: number;
  onAlertMetersChange?: (meters: number) => void;
  width: number;
  height: number;
}

export function GroupLane({
  lane,
  selfId,
  selfWears,
  alertMeters,
  onAlertMetersChange,
  width,
  height,
}: GroupLaneProps) {
  const { palette, scaled } = useAccessibilityTheme();
  const [dragDy, setDragDy] = useState(0);
  const cx = width / 2;
  const top = PAD;
  const bottom = height - PAD;
  const bounds = useMemo(
    () => ({
      top: top + DOT + END_GAP,
      bottom: lane.bottom ? bottom - DOT - END_GAP : bottom,
      gap: DOT + DOT_GAP,
      labelRow: LABEL_ROW,
    }),
    [lane.bottom, top, bottom],
  );
  const placed = useMemo(() => layoutLane(lane.dots, bounds), [lane.dots, bounds]);
  // One guide: the line is meters, so mark the near boundary and the alert distance where a dot
  // at that distance would sit.
  const marks = (lane.scale?.marks ?? []).map((m) => ({
    ...m,
    y: bounds.top + m.t * (bounds.bottom - bounds.top) + (m.kind === 'alert' ? dragDy : 0),
  }));
  const adjustable = onAlertMetersChange !== undefined && alertMeters !== undefined;

  return (
    <View>
      <View style={{ width, height }} accessibilityRole="summary" accessibilityLabel={t.group.lane}>
        <Svg
          width={width}
          height={height}
          style={StyleSheet.absoluteFill}
          pointerEvents="none"
          aria-hidden
          {...NATIVE_HIDDEN}
        >
          {marks.map((m) => (
            <Line
              key={m.kind}
              x1={spacing.sm}
              x2={width - spacing.sm}
              y1={m.y}
              y2={m.y}
              stroke={m.kind === 'alert' ? palette.alert : palette.cardShade}
              strokeWidth={1.5}
              strokeDasharray={m.kind === 'alert' ? '6 6' : '2 6'}
            />
          ))}
          <Line
            x1={cx}
            x2={cx}
            y1={top}
            y2={bottom}
            stroke={palette.primarySoft}
            strokeWidth={6}
            strokeLinecap="round"
          />
          {!lane.bottom && <Circle cx={cx} cy={bottom} r={6} fill={palette.primarySoft} />}
        </Svg>
        {marks.map((m) =>
          m.kind === 'alert' && adjustable ? (
            <AlertLineDragHandle
              key={m.kind}
              meters={alertMeters}
              onChange={onAlertMetersChange}
              onDragOffset={setDragDy}
              y={m.y}
            />
          ) : (
            <Text
              key={m.kind}
              accessibilityLabel={fill(t.group.laneMark, {
                zone: zoneLabel(m.kind === 'alert' ? 'mid' : 'near'),
                m: Math.round(m.meters),
              })}
              style={[
                styles.mark,
                scaled.caption,
                { color: palette.inkMuted },
                m.kind === 'alert' && { fontFamily: fonts.bold, color: palette.alert },
                { top: m.y - MARK_ROW },
              ]}
            >
              {fill(t.group.meters, { m: Math.round(m.meters) })}
            </Text>
          ),
        )}
        {lane.top && (
          <GuideMarker guide={lane.top} selfId={selfId} selfWears={selfWears} cx={cx} y={top} />
        )}
        {lane.bottom && (
          <GuideMarker
            guide={lane.bottom}
            selfId={selfId}
            selfWears={selfWears}
            cx={cx}
            y={bottom}
          />
        )}
        {placed.map((p) => (
          <VisitorDot key={p.dot.id} place={p} cx={cx} />
        ))}
      </View>
      {lane.bottom !== null && adjustable && (
        <View style={[styles.twoGuideAlertRow, { borderColor: palette.cardShade }]}>
          <Text style={[styles.twoGuideAlertLabel, scaled.caption, { color: palette.inkMuted }]}>
            {t.group.alertDistance}
          </Text>
          <AlertStepper meters={alertMeters} onChange={onAlertMetersChange} />
        </View>
      )}
    </View>
  );
}

/** Distinct shape/icon swatch per zone so color never carries state alone. */
function ZoneDot({ status }: { status: DotStatus }) {
  const { palette } = useAccessibilityTheme();
  const size = 12;
  const c = size / 2;
  if (status === 'near') {
    return (
      <Svg width={size} height={size} pointerEvents="none" aria-hidden {...NATIVE_HIDDEN}>
        <Circle cx={c} cy={c} r={4.2} fill={palette.primary} />
      </Svg>
    );
  }
  if (status === 'mid') {
    return (
      <Svg width={size} height={size} pointerEvents="none" aria-hidden {...NATIVE_HIDDEN}>
        <Circle cx={c} cy={c} r={4} fill="none" stroke={palette.primary} strokeWidth={2} />
      </Svg>
    );
  }
  if (status === 'far') {
    return <Icon name="triangleAlert" size={13} color={palette.alert} strokeWidth={2.4} />;
  }
  return <Icon name="eyeOff" size={13} color={palette.inkMuted} strokeWidth={2.2} />;
}

/** Quiet, borderless inline strip naming the four ring states under the lane. */
export function ZoneLegend() {
  const { palette, scaled } = useAccessibilityTheme();
  const items: DotStatus[] = ['near', 'mid', 'far', 'unseen'];
  return (
    <View style={styles.legend}>
      {items.map((s) => (
        <View
          key={s}
          style={styles.legendItem}
          accessible
          accessibilityRole="text"
          accessibilityLabel={zoneLabel(s)}
        >
          <ZoneDot status={s} />
          <Text style={[styles.legendText, scaled.caption, { color: palette.inkMuted }]} numberOfLines={1}>
            {zoneLabel(s)}
          </Text>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  petDotRoot: { alignItems: 'center', justifyContent: 'center' },
  discHalo: { position: 'absolute', backgroundColor: brand.card },
  disc: {
    position: 'absolute',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
  },
  badge: {
    position: 'absolute',
    top: -2,
    right: -2,
    width: 20,
    height: 20,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: brand.card,
    alignItems: 'center',
    justifyContent: 'center',
  },
  badgeAlert: { backgroundColor: brand.alert },
  badgeMuted: { backgroundColor: brand.inkMuted },
  ring: {
    position: 'absolute',
    left: -6,
    top: -6,
    width: DOT + 12,
    height: DOT + 12,
    borderRadius: (DOT + 12) / 2,
    borderWidth: 2.5,
    borderColor: brand.alert,
  },
  row: { position: 'absolute', left: 0, right: 0, height: DOT },
  slot: { position: 'absolute', top: 0, width: DOT, height: DOT },
  label: { position: 'absolute', top: 0, bottom: 0, justifyContent: 'center' },
  name: { ...type.label, color: brand.ink },
  nameLeft: { textAlign: 'right' },
  nameAlert: { fontFamily: fonts.bold, color: brand.alert },
  nameUnseen: { color: brand.inkMuted },
  guideName: { ...type.label, fontFamily: fonts.bold, color: brand.ink },
  mark: { ...type.caption, position: 'absolute', left: spacing.sm, color: brand.inkMuted },
  markAlert: { fontFamily: fonts.bold, color: brand.alert },
  alertDragBand: {
    position: 'absolute',
    left: 0,
    right: 0,
    height: 36,
    justifyContent: 'center',
    alignItems: 'flex-start',
    paddingLeft: spacing.sm,
    ...(Platform.OS === 'web' ? ({ cursor: 'ns-resize', userSelect: 'none' } as object) : {}),
  },
  alertTag: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    height: 26,
    paddingHorizontal: spacing.sm,
    borderRadius: radius.pill,
    borderWidth: 1,
    borderColor: brand.wineSoft,
    backgroundColor: brand.card,
    boxShadow: `0 1px 4px ${brand.glow}`,
  },
  alertTagDragging: {
    borderColor: brand.alert,
    backgroundColor: brand.wineSoft,
  },
  alertValueText: { ...type.caption, fontFamily: fonts.semibold, color: brand.alert },
  stepperPill: {
    flexDirection: 'row',
    alignItems: 'center',
    height: 28,
    borderRadius: radius.pill,
    borderWidth: 1,
    borderColor: brand.cardShade,
    backgroundColor: brand.card,
    overflow: 'hidden',
  },
  stepBtn: {
    width: 26,
    height: 26,
    alignItems: 'center',
    justifyContent: 'center',
  },
  stepBtnDisabled: { opacity: 0.3 },
  stepBtnPressed: { backgroundColor: brand.cardShade },
  stepperValueText: {
    ...type.caption,
    fontFamily: fonts.semibold,
    color: brand.ink,
    paddingHorizontal: spacing.xs,
  },
  twoGuideAlertRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderTopWidth: 1,
    borderColor: brand.cardShade,
  },
  twoGuideAlertLabel: { ...type.caption, color: brand.inkMuted },
  legend: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'center',
    alignItems: 'center',
    columnGap: spacing.md,
    rowGap: spacing.xs,
    paddingHorizontal: spacing.xs,
  },
  legendItem: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  legendText: { ...type.caption, color: brand.inkMuted },
});
