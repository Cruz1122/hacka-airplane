// Per-edge signal filter: one per (observer, subject) pair. Median of the last readings drops
// spikes, the moving average smooths the rest, and the zone moves with hysteresis. Pocket guard:
// a zone improves at once but degrades only after the drop lasts `degradeDwellMs`.
import { GROUP_POLICY } from './policy';
import type { Zone } from './types';

const { refDbmAt1m, pathLossExponent, hysteresisDb } = GROUP_POLICY;

/** The log-distance model, both ways: rssi = ref - 10 n log10(d). Under 1 m reads as 1 m. */
export const dbmAtMeters = (meters: number) =>
  refDbmAt1m - 10 * pathLossExponent * Math.log10(Math.max(1, meters));
export const metersAtDbm = (dbm: number) => 10 ** ((refDbmAt1m - dbm) / (10 * pathLossExponent));

/** Zone cut-offs on the smoothed RSSI: >= nearMinDbm is near, >= midMinDbm mid, below it far. */
export interface ZoneCuts {
  readonly nearMinDbm: number;
  readonly midMinDbm: number;
}

/** Near up to `nearFraction` of the alert distance, mid up to it, far beyond. */
export function zoneCuts(alertMeters: number): ZoneCuts {
  return {
    nearMinDbm: dbmAtMeters(GROUP_POLICY.alertMeters.nearFraction * alertMeters),
    midMinDbm: dbmAtMeters(alertMeters),
  };
}

export interface EdgeFilter {
  readonly readings: readonly number[];
  /** Moving average of the medians, in dBm. */
  readonly smoothed: number;
  readonly zone: Zone;
  /** The cut-offs `zone` was decided under. */
  readonly cuts: ZoneCuts;
  /** When the filtered value first asked for a worse zone; null while it does not. */
  readonly degradingSinceMs: number | null;
  readonly lastAtMs: number;
}

const RANK: Record<Zone, number> = { near: 0, mid: 1, far: 2 };

/** Negative when `a` is the better (closer) zone. */
export const compareZones = (a: Zone, b: Zone) => RANK[a] - RANK[b];

function plainZone(dbm: number, cuts: ZoneCuts): Zone {
  if (dbm >= cuts.nearMinDbm) return 'near';
  return dbm >= cuts.midMinDbm ? 'mid' : 'far';
}

/** The current zone holds while the value stays within its band, [low, high), widened by the
 *  margin. */
function zoneWithHysteresis(dbm: number, current: Zone, cuts: ZoneCuts): Zone {
  const low = current === 'near' ? cuts.nearMinDbm : current === 'mid' ? cuts.midMinDbm : -Infinity;
  const high = current === 'near' ? Infinity : current === 'mid' ? cuts.nearMinDbm : cuts.midMinDbm;
  return dbm >= low - hysteresisDb && dbm < high + hysteresisDb ? current : plainZone(dbm, cuts);
}

const sameCuts = (a: ZoneCuts, b: ZoneCuts) =>
  a.nearMinDbm === b.nearMinDbm && a.midMinDbm === b.midMinDbm;

function median(values: readonly number[]): number {
  const s = [...values].sort((a, b) => a - b);
  const mid = s.length >> 1;
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
}

/** True while the edge's last reading is within the unseen window of `nowMs`. */
export const isFresh = (edge: EdgeFilter, nowMs: number) =>
  nowMs - edge.lastAtMs <= GROUP_POLICY.unseenAfterMs;

/**
 * The filter after one reading, zoned with `cuts`. Pure. A reading older than the last one is
 * dropped; one after a gap longer than the unseen window starts over, so a member who reappears
 * far away does not keep its old zone for a dwell. When the cuts changed (the guide moved the
 * alert distance) the old zone's hysteresis no longer means anything, so the zone asked for is
 * the plain one under the new cuts; the pocket guard still delays a worse one.
 */
export function observe(
  prev: EdgeFilter | undefined,
  rssi: number,
  atMs: number,
  cuts: ZoneCuts,
): EdgeFilter {
  if (prev && atMs < prev.lastAtMs) return prev;
  if (!prev || !isFresh(prev, atMs)) {
    return {
      readings: [rssi],
      smoothed: rssi,
      zone: plainZone(rssi, cuts),
      cuts,
      degradingSinceMs: null,
      lastAtMs: atMs,
    };
  }
  const readings = [...prev.readings, rssi].slice(-GROUP_POLICY.medianWindow);
  const a = GROUP_POLICY.emaAlpha;
  const smoothed = a * median(readings) + (1 - a) * prev.smoothed;
  const wanted = sameCuts(prev.cuts, cuts)
    ? zoneWithHysteresis(smoothed, prev.zone, cuts)
    : plainZone(smoothed, cuts);
  const base = { readings, smoothed, cuts, lastAtMs: atMs };
  if (compareZones(wanted, prev.zone) <= 0)
    return { ...base, zone: wanted, degradingSinceMs: null };
  const since = prev.degradingSinceMs ?? atMs;
  return atMs - since >= GROUP_POLICY.degradeDwellMs
    ? { ...base, zone: wanted, degradingSinceMs: null }
    : { ...base, zone: prev.zone, degradingSinceMs: since };
}
