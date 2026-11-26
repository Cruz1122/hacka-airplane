// The guide's picture of the group: a vertical line from the front guide (t = 0) to the rear
// guide or, with one guide, 1.5 alert distances (t = 1), one dot per visitor.
import {
  alerts,
  alertMetersOf,
  guides,
  lastTracking,
  link,
  members,
  presence,
  type GroupState,
} from './groupState';
import { GROUP_POLICY } from './policy';
import { metersAtDbm, type EdgeFilter } from './signal';
import type { GuideMember, MemberId, MemberLook, Zone } from './types';

export type DotStatus = Zone | 'unseen';

export interface LaneDot {
  id: MemberId;
  name: string;
  /** 0 = top guide, 1 = bottom guide or farthest. */
  t: number;
  status: DotStatus;
  alerting: boolean;
  /** What this visitor's Pet wears over the radio, when sent. */
  look?: MemberLook;
}

/** A labelled distance on a one-guide line. */
export interface LaneMark {
  kind: 'near' | 'alert';
  meters: number;
  t: number;
}

export interface Lane {
  /** The front guide, or the only guide. */
  top: GuideMember | null;
  /** The rear guide when two guide the group. */
  bottom: GuideMember | null;
  /** One per visitor, in join order. */
  dots: LaneDot[];
  /** One guide: the line is meters from the guide, 0 at t = 0 to `meters` at t = 1, with the
   *  zone boundaries marked. Two guides: null, the line is the stretch between them. */
  scale: { meters: number; marks: LaneMark[] } | null;
}

/** A one-guide line spans this many alert distances, so the alert mark sits at t = 2/3. */
const SPAN = 1.5;

const clamp = (x: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, x));

function scaleFor(alertMeters: number) {
  const meters = SPAN * alertMeters;
  const near = GROUP_POLICY.alertMeters.nearFraction * alertMeters;
  return {
    meters,
    marks: [
      { kind: 'near' as const, meters: near, t: near / meters },
      { kind: 'alert' as const, meters: alertMeters, t: alertMeters / meters },
    ],
  };
}

type Scale = ReturnType<typeof scaleFor>;

/** Distance from one guide's end, linear in meters, kept inside the edge's own zone band so a dot
 *  never sits in a band its zone (held by hysteresis or the dwell) contradicts. */
function oneGuideT(edge: EdgeFilter, scale: Scale): number {
  const [near, alert] = scale.marks.map((m) => m.t);
  const band = { near: [0, near], mid: [near, alert], far: [alert, 1] }[edge.zone];
  return clamp(metersAtDbm(edge.smoothed) / scale.meters, band[0], band[1]);
}

function placement(
  state: GroupState,
  visitor: MemberId,
  top: GuideMember,
  bottom: GuideMember | null,
  scale: Scale,
  asOfMs: number,
): number | null {
  const a = link(state, top.id, visitor, asOfMs);
  const b = bottom ? link(state, bottom.id, visitor, asOfMs) : null;
  if (a && b) {
    const da = metersAtDbm(a.smoothed);
    return da / (da + metersAtDbm(b.smoothed));
  }
  // One end only: its distance on the one-guide scale, from that end.
  if (a) return oneGuideT(a, scale);
  if (b) return 1 - oneGuideT(b, scale);
  return null;
}

export function lane(state: GroupState, self: MemberId): Lane {
  const gs = guides(state);
  const front = gs.find((g) => g.slot === 'front');
  const rear = gs.find((g) => g.slot === 'rear');
  const top = front ?? rear ?? null;
  const bottom = front && rear ? rear : null;
  const scale = scaleFor(alertMetersOf(state));
  const alerting = new Set(alerts(state, self).map((a) => a.id));
  const dots: LaneDot[] = [];
  for (const m of members(state)) {
    if (m.role !== 'visitor') continue;
    const p = presence(state, m.id);
    // An unseen dot stays where it was last drawn: the state just before its window ran out.
    const last = lastTracking(state, m.id);
    const asOf =
      p.kind === 'tracked' ? state.nowMs : last ? last.atMs + GROUP_POLICY.unseenAfterMs : null;
    const t = top && asOf !== null ? placement(state, m.id, top, bottom, scale, asOf) : null;
    dots.push({
      id: m.id,
      name: m.name,
      // Never heard yet: it joined by touching a guide's phone, so it starts at the top.
      t: t ?? 0,
      status: p.kind === 'tracked' ? p.zone : 'unseen',
      alerting: alerting.has(m.id),
      ...(m.look ? { look: m.look } : {}),
    });
  }
  return { top, bottom, dots, scale: bottom ? null : scale };
}
