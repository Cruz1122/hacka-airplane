// The guide's view of the group: a vertical line from the front guide down to the rear guide (or
// the farthest reach with one guide), one dot per visitor ON the line, placed by t and spread
// along it so dots never overlap (laneLayout.ts). Each dot is the visitor's own little Pet, whose
// face tells how they are doing: near happy, mid curious, far sad, unseen asleep. Zones also read
// without color or face: near a solid ring, mid a double ring, far a dashed ring, unseen a dotted
// grey ring with a crossed eye. An alerting dot gets an alert-red ring that pulses unless motion
// is reduced, a warning badge and a bold red name. Guides at the ends wear the guide hat.
import { memo, useEffect, useMemo, useState } from 'react';
import { Animated, Easing, Platform, StyleSheet, Text, View } from 'react-native';
import Svg, { Circle, Line } from 'react-native-svg';

import type { DotStatus, Lane } from '@/core/group/lane';
import type { GuideMember, MemberId } from '@/core/group/types';
import { fill, t } from '@/i18n';

import { Icon } from '../icons/Icon';
import type { PetAccessory, PetEmotion, PetTint } from '../pet/petCore';
import { PetStill } from '../pet/PetStill';
import { brand, fonts, spacing, type } from '../theme/tokens';
import { useReducedMotion } from '../useReducedMotion';
import { layoutLane, type PlacedDot } from './laneLayout';

/** Diameter of a lane dot. */
export const DOT = 56;
/** Space between two dots on the line. */
const DOT_GAP = 10;
/** Space between a guide marker and the nearest dot. */
const END_GAP = 12;
/** Room above the top guide and below the bottom end for the guide markers. */
const PAD = DOT / 2 + 4;
const LABEL_GAP = 8;
const LABEL_ROW = 24;
const MOVE_MS = 500;
/** Height of a lane mark's label, which sits just above its line. */
const MARK_ROW = 18;

/** The head and the hat, in Pet units: what a dot shows of its Pet. */
const FACE_CROP = { x: -175, y: -170, width: 320, height: 320 };
const HAT_CROP = { x: -190, y: -225, width: 360, height: 360 };

export const zoneLabel = (s: DotStatus) => t.group.zones[s];

const EMOTION: Record<DotStatus, PetEmotion> = {
  near: 'happy',
  mid: 'curious',
  far: 'sad',
  unseen: 'sleepy',
};

/** The ring that names the zone without color: solid, double, dashed, dotted. */
function ZoneRing({ status, size }: { status: DotStatus; size: number }) {
  const c = size / 2;
  const w = Math.max(2, size / 18);
  const r = c - w / 2;
  const muted = status === 'unseen';
  return (
    <Svg width={size} height={size} style={StyleSheet.absoluteFill} pointerEvents="none">
      <Circle
        cx={c}
        cy={c}
        r={r}
        fill="none"
        stroke={muted ? brand.inkMuted : brand.ink}
        strokeWidth={w}
        strokeDasharray={
          status === 'far' ? `${w * 3} ${w * 2}` : muted ? `${w} ${w * 1.6}` : undefined
        }
        strokeLinecap={status === 'unseen' ? 'round' : 'butt'}
      />
      {status === 'mid' && (
        <Circle
          cx={c}
          cy={c}
          r={r - w * 2}
          fill="none"
          stroke={brand.primarySoft}
          strokeWidth={w * 0.8}
        />
      )}
    </Svg>
  );
}

/** A Pet face in a teal coin with its zone ring: the lane dot and the legend's swatch. */
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
  /** Guides wear their hat and a thick ink rim; unseen visitors sit on grey. */
  guide?: boolean;
}) {
  const bg = status === 'unseen' && !guide ? brand.inkMuted : brand.primary;
  return (
    <View style={{ width: size, height: size }}>
      <View
        style={[
          styles.coin,
          { width: size, height: size, borderRadius: size / 2, backgroundColor: bg },
        ]}
      >
        <PetStill
          size={size}
          emotion={guide ? 'happy' : EMOTION[status]}
          accessory={accessory}
          tint={tint}
          crop={accessory ? HAT_CROP : FACE_CROP}
        />
      </View>
      {guide ? (
        <View style={[StyleSheet.absoluteFill, styles.guideRing, { borderRadius: size / 2 }]} />
      ) : (
        <ZoneRing status={status} size={size} />
      )}
      {status === 'unseen' && !guide && (
        <View style={[styles.badge, styles.badgeMuted]}>
          <Icon name="eyeOff" size={12} color={brand.onPrimary} strokeWidth={2.4} />
        </View>
      )}
    </View>
  );
});

/** Alert ring around an alerting dot; pulses outward unless motion is reduced. */
function AlertRing() {
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
      <View style={styles.ring} />
      {!reduced && (
        <Animated.View
          style={[
            styles.ring,
            {
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
  const { dot, y, side } = place;
  const reduced = useReducedMotion();
  const [pos] = useState(() => new Animated.Value(y));
  useEffect(() => {
    if (reduced) return pos.setValue(y);
    const a = Animated.timing(pos, {
      toValue: y,
      duration: MOVE_MS,
      easing: Easing.out(Easing.cubic),
      useNativeDriver: true,
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
        <PetDot status={dot.status} size={DOT} />
        {dot.alerting && (
          <View style={[styles.badge, styles.badgeAlert]}>
            <Icon name="triangleAlert" size={12} color={brand.onPrimary} strokeWidth={2.6} />
          </View>
        )}
      </View>
      <View
        style={[
          styles.label,
          side === 'right'
            ? { left: cx + DOT / 2 + LABEL_GAP, right: 0 }
            : { left: 0, width: cx - DOT / 2 - LABEL_GAP, alignItems: 'flex-end' },
        ]}
      >
        <Text
          numberOfLines={1}
          style={[
            styles.name,
            side === 'left' && styles.nameLeft,
            dot.status === 'unseen' && styles.nameUnseen,
            dot.alerting && styles.nameAlert,
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

const GUIDE_WEARS: Wears = { accessory: 'guideHat' };

function GuideMarker({
  guide,
  selfId,
  selfWears,
  y,
  cx,
}: {
  guide: GuideMember;
  selfId: MemberId;
  selfWears: Wears;
  y: number;
  cx: number;
}) {
  const wears = guide.id === selfId ? selfWears : GUIDE_WEARS;
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
      <View style={[styles.label, { left: cx + DOT / 2 + LABEL_GAP, right: 0 }]}>
        <Text numberOfLines={1} style={styles.guideName}>
          {name}
        </Text>
      </View>
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
  /** What this phone's own Pet wears (its owner's choice); other guides wear the guide hat. */
  selfWears?: Wears;
  width: number;
  height: number;
}

export function GroupLane({
  lane,
  selfId,
  selfWears = GUIDE_WEARS,
  width,
  height,
}: GroupLaneProps) {
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
    y: bounds.top + m.t * (bounds.bottom - bounds.top),
  }));
  return (
    <View style={{ width, height }} accessibilityRole="summary" accessibilityLabel={t.group.lane}>
      <Svg
        width={width}
        height={height}
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
        {marks.map((m) => (
          <Line
            key={m.kind}
            x1={spacing.sm}
            x2={width - spacing.sm}
            y1={m.y}
            y2={m.y}
            stroke={m.kind === 'alert' ? brand.alert : brand.cardShade}
            strokeWidth={m.kind === 'alert' ? 2 : 1.5}
            strokeDasharray={m.kind === 'alert' ? '8 6' : '2 6'}
          />
        ))}
        <Line
          x1={cx}
          x2={cx}
          y1={top}
          y2={bottom}
          stroke={brand.primarySoft}
          strokeWidth={6}
          strokeLinecap="round"
        />
        {!lane.bottom && <Circle cx={cx} cy={bottom} r={6} fill={brand.primarySoft} />}
      </Svg>
      {marks.map((m) => (
        <Text
          key={m.kind}
          accessibilityLabel={fill(t.group.laneMark, {
            zone: zoneLabel(m.kind === 'alert' ? 'mid' : 'near'),
            m: Math.round(m.meters),
          })}
          style={[styles.mark, m.kind === 'alert' && styles.markAlert, { top: m.y - MARK_ROW }]}
        >
          {fill(t.group.meters, { m: Math.round(m.meters) })}
        </Text>
      ))}
      {lane.top && (
        <GuideMarker guide={lane.top} selfId={selfId} selfWears={selfWears} cx={cx} y={top} />
      )}
      {lane.bottom && (
        <GuideMarker guide={lane.bottom} selfId={selfId} selfWears={selfWears} cx={cx} y={bottom} />
      )}
      {placed.map((p) => (
        <VisitorDot key={p.dot.id} place={p} cx={cx} />
      ))}
    </View>
  );
}

/** What each ring and face means, so no one has to learn it from color. */
export function ZoneLegend() {
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
          <View aria-hidden accessibilityElementsHidden importantForAccessibility="no-hide-descendants">
            <PetDot status={s} size={32} />
          </View>
          <Text style={styles.legendText}>{zoneLabel(s)}</Text>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  coin: { overflow: 'hidden', alignItems: 'center', justifyContent: 'center' },
  guideRing: { borderWidth: 4, borderColor: brand.ink },
  badge: {
    position: 'absolute',
    top: -2,
    right: -2,
    width: 22,
    height: 22,
    borderRadius: 11,
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
    borderWidth: 3,
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
  legend: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md, justifyContent: 'center' },
  legendItem: { flexDirection: 'row', alignItems: 'center', gap: spacing.xs },
  legendText: { ...type.caption, color: brand.inkMuted },
});
