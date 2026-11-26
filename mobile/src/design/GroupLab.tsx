// Workshop lab for the group lane: fixed groups built by running the real reducer on canned
// sightings, so each sample is a state the core can actually produce.
import { useMemo, useState } from 'react';
import { StyleSheet, View } from 'react-native';

import { alerts, EMPTY_GROUP, members, step, type GroupState } from '@/core/group/groupState';
import { lane } from '@/core/group/lane';
import { GROUP_POLICY } from '@/core/group/policy';
import { dbmAtMeters } from '@/core/group/signal';
import { memberId, type GuideMember, type Member, type MemberId, type MemberLook } from '@/core/group/types';
import { fill, t } from '@/i18n';
import { EmptyLane } from '@/ui/group/EmptyLane';
import { GroupAlertBanner } from '@/ui/group/GroupAlertBanner';
import { GroupLane, laneHeightFor, ZoneLegend } from '@/ui/group/GroupLane';
import { RoleChoices } from '@/ui/group/RoleChoices';
import { SignalPulse } from '@/ui/group/SignalPulse';
import { DEFAULT_LOOKS, wornBy, type PetLooks, type PetRole } from '@/state/petLook';
import { brand, spacing } from '@/ui/theme/tokens';

import { Choices, Field, Stage, Status, type LabProps } from './chrome';

type Preset = 'one' | 'meters' | 'two' | 'alert' | 'unseen' | 'empty' | 'roles' | 'signal';
type LanePreset = Exclude<Preset, 'meters' | 'empty' | 'roles' | 'signal'>;

const SELF = memberId('lab-guide');
const REAR = memberId('lab-rear');
const guide: GuideMember = {
  id: SELF,
  role: 'guide',
  name: 'Marta',
  slot: 'front',
  look: { accessory: 'guideHat', tint: 'ink' },
};
const rear: Member = {
  id: REAR,
  role: 'guide',
  name: 'Julián',
  slot: 'rear',
  look: { accessory: 'guideHat', tint: 'sun' },
};
const NAMES = ['Ana', 'Tomás', 'Lucía', 'Sofía', 'Mateo'];
const LOOKS: MemberLook[] = [
  { accessory: 'flower', tint: 'lupine' },
  { accessory: 'beanie', tint: 'sky' },
  { accessory: 'bandana', tint: 'sun' },
  { accessory: 'visitorCap', tint: 'ink' },
  { accessory: 'flower', tint: 'sun' },
];
const V = NAMES.map((_, i) => memberId(`lab-v${i}`));
const visitors: Member[] = NAMES.map((name, i) => ({
  id: V[i],
  role: 'visitor',
  name,
  look: LOOKS[i],
}));

/** observer, subject, dBm, and the second the readings stop (default: never). */
type Feed = [MemberId, MemberId, number, number?];

function build(cast: Member[], feeds: Feed[], seconds: number): GroupState {
  let s = cast.reduce((st, member) => step(st, { kind: 'joined', member }), EMPTY_GROUP);
  for (let sec = 0; sec < seconds; sec++) {
    s = step(s, { kind: 'tick', nowMs: sec * 1000 });
    for (const [observer, subject, rssi, until] of feeds) {
      if (until === undefined || sec < until) {
        s = step(s, { kind: 'sighting', sighting: { observer, subject, rssi, atMs: sec * 1000 } });
      }
    }
  }
  return s;
}

const ONE_GUIDE: Feed[] = [-70, -84, -86, -75, -88].map((dbm, i) => [SELF, V[i], dbm]);

const PRESETS: Record<LanePreset, () => GroupState> = {
  one: () => build([guide, ...visitors], ONE_GUIDE, 30),
  two: () =>
    build(
      [guide, rear, ...visitors],
      [
        [SELF, REAR, -88],
        [REAR, SELF, -88],
        ...[-68, -80, -84, -86, -89].map((dbm, i): Feed => [SELF, V[i], dbm]),
        ...[-89, -85, -80, -76, -66].map((dbm, i): Feed => [REAR, V[i], dbm]),
      ],
      30,
    ),
  alert: () =>
    build(
      [guide, ...visitors],
      [...ONE_GUIDE.filter(([, v]) => v !== V[1]), [SELF, V[1], -96]],
      40,
    ),
  unseen: () =>
    build(
      [guide, ...visitors],
      [...ONE_GUIDE.filter(([, v]) => v !== V[2]), [SELF, V[2], -84, 10]],
      30,
    ),
};

/** Visitors at fixed meters from the guide: the slider moves the zones over them. */
const SPREAD_M = [6, 14, 22, 33, 48];

function metersPreset(alertMeters: number): GroupState {
  const feeds = SPREAD_M.map((m, i): Feed => [SELF, V[i], dbmAtMeters(m)]);
  return build([{ ...guide, alertMeters }, ...visitors], feeds, 30);
}

// Fits the workshop canvas at phone width (390 pt).
const LANE_W = 276;

export function GroupLab({ wide }: LabProps) {
  const [preset, setPreset] = useState<Preset>('one');
  const [chosen, setChosen] = useState<string | null>(null);
  // The lab's own looks, so trying them here never changes the phone's saved Pets.
  const [looks, setLooks] = useState<PetLooks>(DEFAULT_LOOKS);
  const w = t.dev.workshop;
  const preview =
    preset === 'roles' ? (
      <View style={styles.sheet}>
        <RoleChoices
          looks={looks}
          onLookChange={(role: PetRole, patch) =>
            setLooks((l) => ({ ...l, [role]: { ...l[role], ...patch } }))
          }
          onChoose={(role) => setChosen(role === 'guide' ? t.group.imGuide : t.group.imVisitor)}
          width={LANE_W}
        />
        {chosen && <Status>{fill(w.pressed, { name: chosen, count: 1 })}</Status>}
      </View>
    ) : preset === 'empty' ? (
      <View style={styles.sheet}>
        <EmptyLane
          wears={wornBy(looks.guide, 'guide')}
          onCancel={() => setChosen(t.group.cancelGuide)}
        />
        {chosen && <Status>{fill(w.pressed, { name: chosen, count: 1 })}</Status>}
      </View>
    ) : preset === 'signal' ? (
      <View style={[styles.sheet, styles.center]}>
        <SignalPulse size={160} />
      </View>
    ) : preset === 'meters' ? (
      <MetersPreview />
    ) : (
      <PresetPreview preset={preset} />
    );
  const controls = (
    <Field label={w.state}>
      <Choices
        value={preset}
        onChange={setPreset}
        options={[
          { value: 'one', label: w.groupOne },
          { value: 'meters', label: w.groupMeters },
          { value: 'two', label: w.groupTwo },
          { value: 'alert', label: w.groupAlert },
          { value: 'unseen', label: w.groupUnseen },
          { value: 'empty', label: w.groupEmpty },
          { value: 'roles', label: w.groupRoles },
          { value: 'signal', label: w.groupSignal },
        ]}
      />
    </Field>
  );
  return <Stage wide={wide} preview={preview} controls={controls} />;
}

function PresetPreview({ preset }: { preset: LanePreset }) {
  const state = useMemo(() => PRESETS[preset](), [preset]);
  return <LanePreview state={state} />;
}

/** Adjusting the alert distance directly on the lane moves the zones over fixed visitors. */
function MetersPreview() {
  const [meters, setMeters] = useState<number>(GROUP_POLICY.alertMeters.default);
  const state = useMemo(() => metersPreset(meters), [meters]);
  return <LanePreview state={state} alertMeters={meters} onAlertMetersChange={setMeters} />;
}

function LanePreview({
  state,
  alertMeters,
  onAlertMetersChange,
}: {
  state: GroupState;
  alertMeters?: number;
  onAlertMetersChange?: (meters: number) => void;
}) {
  const names = useMemo(() => new Map(members(state).map((m) => [m.id, m.name])), [state]);
  const view = lane(state, SELF);
  return (
    <View style={styles.sheet}>
      <GroupAlertBanner alerts={alerts(state, SELF)} nameOf={(a) => names.get(a.id) ?? ''} />
      <GroupLane
        lane={view}
        selfId={SELF}
        alertMeters={alertMeters}
        onAlertMetersChange={onAlertMetersChange}
        width={LANE_W}
        height={laneHeightFor(view.dots.length, view.bottom !== null)}
      />
      <ZoneLegend />
    </View>
  );
}

const styles = StyleSheet.create({
  sheet: {
    width: LANE_W + 2 * spacing.lg,
    gap: spacing.md,
    padding: spacing.lg,
    borderRadius: 28,
    backgroundColor: brand.card,
  },
  center: { alignItems: 'center' },
});
