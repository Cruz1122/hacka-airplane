// Test-only module (imported by __tests__ only).
// Scenario driver for the group tests: feeds one reading per second per edge, ticks the clock with
// it and records what a guide's phone would show after every input.
import { alerts, groupOf, presence, step, type GroupInput, type GroupState } from './groupState';
import { memberId, type GuideMember, type Member, type MemberId } from './types';

export const FRONT = memberId('front');
export const REAR = memberId('rear');
export const V1 = memberId('v1');
export const V2 = memberId('v2');

export const front: GuideMember = {
  id: FRONT,
  role: 'guide',
  name: 'Front',
  slot: 'front',
};
export const rear: GuideMember = {
  id: REAR,
  role: 'guide',
  name: 'Rear',
  slot: 'rear',
};
export const visitor = (id: MemberId, name = String(id)): Member => ({
  id,
  role: 'visitor',
  name,
});

/** A group on the phone of the first member, with the others joined in order. */
export function join(self: Member, ...others: Member[]): GroupState {
  return others.reduce((s, member) => step(s, { kind: 'joined', member }), groupOf(self));
}

/** One reading of `rssi(t)` per second on each edge, t in [fromMs, toMs). */
export interface Feed {
  observer: MemberId;
  subject: MemberId;
  rssi: (atMs: number) => number;
  /** Offset inside the second, to stagger edges. */
  offsetMs?: number;
}

export interface Frame {
  atMs: number;
  state: GroupState;
}

/**
 * Runs the feeds and a tick every second from `fromMs` to `toMs`; returns the state after every
 * single input, so a one-input transient is visible.
 */
export function run(state: GroupState, feeds: Feed[], fromMs: number, toMs: number): Frame[] {
  const inputs: GroupInput[] = [];
  for (let s = fromMs; s < toMs; s += 1000) {
    const batch = feeds
      .map((f) => ({ f, atMs: s + (f.offsetMs ?? 0) }))
      .sort((a, b) => a.atMs - b.atMs);
    for (const { f, atMs } of batch) {
      inputs.push({ kind: 'tick', nowMs: atMs });
      inputs.push({
        kind: 'sighting',
        sighting: {
          observer: f.observer,
          subject: f.subject,
          rssi: f.rssi(atMs),
          atMs,
        },
      });
    }
    inputs.push({ kind: 'tick', nowMs: s + 999 });
  }
  const frames: Frame[] = [];
  let st = state;
  for (const input of inputs) {
    st = step(st, input);
    frames.push({ atMs: st.nowMs, state: st });
  }
  return frames;
}

export const last = (frames: Frame[]) => frames[frames.length - 1].state;
export const zoneOf = (s: GroupState, id: MemberId) => {
  const p = presence(s, id);
  return p.kind === 'tracked' ? p.zone : 'unseen';
};
export const alertKeys = (s: GroupState, self: MemberId) =>
  alerts(s, self).map((a) => `${a.kind}:${a.id}`);
