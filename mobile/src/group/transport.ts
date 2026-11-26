// The seam between the group core and the BLE radio transport.
import type { GroupInput } from '@/core/group/groupState';
import type { GuideMember, Member } from '@/core/group/types';

export interface GroupTransport {
  /** True when the transport emits `{ kind: 'tick' }` from a native service (screen-off safe). */
  readonly nativeTicks?: boolean;
  /** Guides in sync mode within touching range right now. Stops early when `signal` aborts. */
  findSyncingGuides(signal?: AbortSignal): Promise<GuideMember[]>;
  /** Starts beaconing/listening as `self`; returns stop. */
  start(self: Member, onEvent: (e: GroupInput) => void): () => void;
  setSyncMode(on: boolean): void;
  /** Guide only: broadcasts the alert distance (meters) so visitors' phones use the same zones. */
  setAlertMeters?(meters: number): void;
  /** Plays an audible + tactile alert for `freshCount` newly raised alerts. */
  alert?(freshCount: number): void;
}
