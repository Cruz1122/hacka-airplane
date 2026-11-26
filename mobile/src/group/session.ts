// The group screen's flow as one value: choosing a role, guiding, or visiting.
import type { GuideMember, MemberId, VisitorMember } from '@/core/group/types';
import { randomShortId, shortIdToMemberId } from '@/core/group/wire';

export type Session =
  | { kind: 'choosing' }
  | { kind: 'guide'; self: GuideMember; syncing: boolean }
  | { kind: 'visitor'; self: VisitorMember; link: 'searching' | 'paired' };

/** A per-launch id that matches the 16-bit BLE beacon sender id; never persisted. */
export const newMemberId = (): MemberId => shortIdToMemberId(randomShortId());

/**
 * Becoming a guide: with no other guide syncing nearby this phone creates the group at the front;
 * with one, it joins as the second guide in the slot that one left free. A new group starts in
 * sync mode so visitors can pair right away.
 */
export function guideSession(name: string, id: MemberId, syncing: GuideMember[]): Session {
  const slot = syncing.some((g) => g.slot === 'front') ? 'rear' : 'front';
  return { kind: 'guide', self: { id, role: 'guide', name, slot }, syncing: true };
}

export function visitorSession(name: string, id: MemberId): Session {
  return { kind: 'visitor', self: { id, role: 'visitor', name }, link: 'searching' };
}
