// Group-sync domain: who is in the group and what the radio heard. Pure data; the BLE transport
// turns radio traffic into `LinkEvent`s.

export type MemberId = string & { readonly __brand: 'MemberId' };

/** The only way to make a `MemberId`; call it where an id enters the app (transport, session). */
export const memberId = (raw: string): MemberId => raw as MemberId;

export type GuideSlot = 'front' | 'rear';

export type Member =
  | {
      id: MemberId;
      role: 'guide';
      name: string;
      slot: GuideSlot;
      /** The guide's alert distance in meters (slider). Absent: `GROUP_POLICY.alertMeters.default`.
       *  A transport re-emits `joined` for a guide whose distance changes. */
      alertMeters?: number;
    }
  | { id: MemberId; role: 'visitor'; name: string };

export type GuideMember = Extract<Member, { role: 'guide' }>;
export type VisitorMember = Extract<Member, { role: 'visitor' }>;

/**
 * One radio observation: `observer` heard `subject` at `rssi` dBm. How it reached this phone
 * (own scan, a visitor echoing what it hears of each guide, a guide-to-guide relay) is the
 * transport's business, not the core's. `atMs` is on the receiving phone's clock: phones have no
 * shared time offline, so a relayed sighting is stamped when it arrives, not when it was heard.
 */
export interface Sighting {
  observer: MemberId;
  subject: MemberId;
  rssi: number;
  atMs: number;
}

export type LinkEvent =
  | { kind: 'joined'; member: Member }
  | { kind: 'left'; id: MemberId }
  | { kind: 'sighting'; sighting: Sighting };

export type Zone = 'near' | 'mid' | 'far';

/** "Not heard" is a state of its own, never a synonym of far. */
export type Presence = { kind: 'tracked'; zone: Zone } | { kind: 'unseen'; sinceMs: number };

export type Alert =
  /** Best zone over reachable guides is far, sustained. */
  | { kind: 'visitorFar'; id: MemberId }
  /** Was tracked, now unseen by every reachable guide. */
  | { kind: 'visitorLost'; id: MemberId }
  /** The other guide is unreachable from this phone. */
  | { kind: 'guideLost'; id: MemberId };
