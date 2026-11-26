// The group as one phone sees it: roster plus a signal filter per radio edge, advanced by a pure
// reducer. Time enters only through sighting stamps and ticks, so a test replays any scenario.
import { GROUP_POLICY } from './policy';
import { compareZones, isFresh, observe, zoneCuts, type EdgeFilter } from './signal';
import type { Alert, GuideMember, LinkEvent, Member, MemberId, Presence, Zone } from './types';

export interface RosterEntry {
  readonly member: Member;
  readonly joinedAtMs: number;
}

export interface GroupState {
  /** This phone's member; null in a state built without one (tests, the design lab). */
  readonly self: MemberId | null;
  /** Join order; selectors keep it so the screen does not reshuffle. */
  readonly roster: readonly RosterEntry[];
  /** Keyed by `edgeKey(observer, subject)`. */
  readonly edges: ReadonlyMap<string, EdgeFilter>;
  /** Advanced by ticks only: one sighting stamped in the future must not age every edge. */
  readonly nowMs: number;
}

export type GroupInput = LinkEvent | { kind: 'tick'; nowMs: number };

export const EMPTY_GROUP: GroupState = {
  self: null,
  roster: [],
  edges: new Map(),
  nowMs: 0,
};

/** The group as `self`'s phone starts it: only itself, at `nowMs`. */
export const groupOf = (self: Member, nowMs = 0): GroupState => ({
  ...EMPTY_GROUP,
  self: self.id,
  roster: [{ member: self, joinedAtMs: nowMs }],
  nowMs,
});

const edgeKey = (observer: MemberId, subject: MemberId) => `${observer}\n${subject}`;

/** Pure: returns a new state and never mutates `state` (React may run a reducer twice). */
export function step(state: GroupState, input: GroupInput): GroupState {
  switch (input.kind) {
    case 'tick':
      return input.nowMs > state.nowMs ? { ...state, nowMs: input.nowMs } : state;
    case 'joined': {
      const { member } = input;
      const i = state.roster.findIndex((e) => e.member.id === member.id);
      const roster =
        i < 0
          ? [...state.roster, { member, joinedAtMs: state.nowMs }]
          : state.roster.map((e, j) => (j === i ? { ...e, member } : e));
      return { ...state, roster };
    }
    case 'left': {
      const prefix = `${input.id}\n`;
      const suffix = `\n${input.id}`;
      const edges = new Map(
        [...state.edges].filter(([k]) => !k.startsWith(prefix) && !k.endsWith(suffix)),
      );
      return {
        ...state,
        roster: state.roster.filter((e) => e.member.id !== input.id),
        edges,
      };
    }
    case 'sighting': {
      const { observer, subject, rssi, atMs } = input.sighting;
      const key = edgeKey(observer, subject);
      const prev = state.edges.get(key);
      const next = observe(prev, rssi, atMs, zoneCuts(alertMetersOf(state)));
      if (next === prev) return state;
      const edges = new Map(state.edges);
      edges.set(key, next);
      return { ...state, edges };
    }
  }
}

export const members = (state: GroupState): Member[] => state.roster.map((e) => e.member);

export const guides = (state: GroupState): GuideMember[] =>
  members(state).filter((m): m is GuideMember => m.role === 'guide');

const entry = (state: GroupState, id: MemberId) => state.roster.find((e) => e.member.id === id);

const { min, max, default: defaultMeters } = GROUP_POLICY.alertMeters;

/**
 * The alert distance this phone zones with: its own when it is a guide, else the front guide's
 * (or any guide's), else the default. Kept inside the policy range, since a guide's value comes
 * over the radio.
 */
export function alertMetersOf(state: GroupState): number {
  const me = state.self === null ? undefined : entry(state, state.self)?.member;
  const set = guides(state).filter((g) => g.alertMeters !== undefined);
  const meters =
    me?.role === 'guide'
      ? me.alertMeters
      : (set.find((g) => g.slot === 'front') ?? set[0])?.alertMeters;
  return Math.min(max, Math.max(min, meters ?? defaultMeters));
}

/** Both directions between a guide and a visitor: the guide's scan and the visitor's echo. */
function linkEdges(state: GroupState, guide: MemberId, visitor: MemberId) {
  return [
    state.edges.get(edgeKey(guide, visitor)),
    state.edges.get(edgeKey(visitor, guide)),
  ].filter((e): e is EdgeFilter => e !== undefined);
}

/** One guide's link to a visitor: its best fresh edge, or null. */
export function link(
  state: GroupState,
  guide: MemberId,
  visitor: MemberId,
  asOfMs = state.nowMs,
): EdgeFilter | null {
  let best: EdgeFilter | null = null;
  for (const e of linkEdges(state, guide, visitor)) {
    if (!isFresh(e, asOfMs)) continue;
    if (
      !best ||
      compareZones(e.zone, best.zone) < 0 ||
      (e.zone === best.zone && e.smoothed > best.smoothed)
    )
      best = e;
  }
  return best;
}

/** Last time any guide heard the visitor (either direction), and which guide. */
export function lastTracking(
  state: GroupState,
  visitor: MemberId,
): { guide: MemberId; atMs: number } | null {
  let last: { guide: MemberId; atMs: number } | null = null;
  for (const g of guides(state)) {
    for (const e of linkEdges(state, g.id, visitor)) {
      if (!last || e.lastAtMs > last.atMs) last = { guide: g.id, atMs: e.lastAtMs };
    }
  }
  return last;
}

/** Best over guides: tracked beats unseen, near beats mid beats far. */
export function presence(state: GroupState, visitor: MemberId): Presence {
  let best: Zone | null = null;
  for (const g of guides(state)) {
    const e = link(state, g.id, visitor);
    if (e && (best === null || compareZones(e.zone, best) < 0)) best = e.zone;
  }
  if (best) return { kind: 'tracked', zone: best };
  const last = lastTracking(state, visitor);
  // Never heard: unseen since it joined (pairing happens phone to phone).
  return {
    kind: 'unseen',
    sinceMs: last?.atMs ?? entry(state, visitor)?.joinedAtMs ?? 0,
  };
}

/** Latest evidence that `guide` is on air for `self`: what it reports, or `self` hearing it. */
function guideLastHeardMs(state: GroupState, self: MemberId, guide: MemberId): number | null {
  let last: number | null = null;
  for (const [k, e] of state.edges) {
    const [observer, subject] = k.split('\n');
    if (observer === guide || (observer === self && subject === guide)) {
      if (last === null || e.lastAtMs > last) last = e.lastAtMs;
    }
  }
  return last;
}

/** Another guide is reachable while a fresh sighting has it as observer or `self` hears it. */
export function isReachable(state: GroupState, self: MemberId, guide: MemberId): boolean {
  const last = guideLastHeardMs(state, self, guide);
  return last !== null && state.nowMs - last <= GROUP_POLICY.unseenAfterMs;
}

/**
 * What `self` (a guide) must be told now, guide losses first, then visitors in join order. A
 * visitor phone gets none. A visitor last tracked by another guide is reported lost only once that
 * guide is heard after the visitor's window ran out: if the guide itself went silent, its
 * visitors fade with it and the one `guideLost` speaks for them.
 */
export function alerts(state: GroupState, self: MemberId): Alert[] {
  if (entry(state, self)?.member.role !== 'guide') return [];
  const out: Alert[] = [];
  for (const g of guides(state)) {
    if (g.id === self) continue;
    if (guideLastHeardMs(state, self, g.id) !== null && !isReachable(state, self, g.id)) {
      out.push({ kind: 'guideLost', id: g.id });
    }
  }
  for (const m of members(state)) {
    if (m.role !== 'visitor') continue;
    const p = presence(state, m.id);
    if (p.kind === 'tracked') {
      if (p.zone === 'far') out.push({ kind: 'visitorFar', id: m.id });
      continue;
    }
    const last = lastTracking(state, m.id);
    if (!last) continue;
    if (last.guide !== self) {
      const heard = guideLastHeardMs(state, self, last.guide);
      const expiredAt = last.atMs + GROUP_POLICY.unseenAfterMs;
      if (heard === null || heard <= expiredAt || !isReachable(state, self, last.guide)) continue;
    }
    out.push({ kind: 'visitorLost', id: m.id });
  }
  return out;
}
