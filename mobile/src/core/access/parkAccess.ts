// Park access: the knowledge chat opens by scanning a station QR and stays open for a window;
// station progress is kept for good. Pure (no React / RN) so the rules are tested without a device.
import { STATION_IDS, type StationId } from '@/recorrido/stations';

/** The four stations that carry a QR; Brisas is the start and needs none. */
export type CountedStation = Exclude<StationId, 'brisas'>;
export const COUNTED_STATIONS = STATION_IDS.filter((id): id is CountedStation => id !== 'brisas');

/** Fixed random tokens, so a visitor cannot guess a station's QR. Printed QRs depend on them. */
export const STATION_CODES: Record<CountedStation, string> = {
  aguacerales: 'l0bnathwky',
  arenales: 'ne30ytwizz',
  valleLunar: 'yn0d4e4yt1',
  valleTumbas: 'bdxv3xvm8z',
};

export interface ParkAccess {
  /** When the knowledge window was last opened; the expiry follows the current threshold. */
  openedAtMs: number | null;
  /** Highest counted station scanned (1..4); 0 = none. */
  reached: number;
  /** A guide entered the admin password on this phone: everything stays open, with no window. */
  guide?: boolean;
}

export const LOCKED_ACCESS: ParkAccess = { openedAtMs: null, reached: 0 };

export const DEFAULT_ACCESS_HOURS = 24;
export const MIN_ACCESS_HOURS = 1;
export const MAX_ACCESS_HOURS = 72;
export const HOUR_MS = 3_600_000;

const PREFIX = 'NEVADOS-ESTACION';

const indexOf = (station: CountedStation) => COUNTED_STATIONS.indexOf(station) + 1;

export function stationCode(station: CountedStation): string {
  return `${PREFIX}:${station}:${STATION_CODES[station]}`;
}

/** The station a scanned text belongs to; any other text, or a wrong token, is null. */
export function parseStationCode(text: string): CountedStation | null {
  const [prefix, id, token, ...rest] = text.trim().split(':');
  if (prefix !== PREFIX || rest.length > 0) return null;
  const station = COUNTED_STATIONS.find((s) => s === id);
  return station && token === STATION_CODES[station] ? station : null;
}

/** Progress is a monotonic max; every valid scan reopens the window from `nowMs`. */
export function scanStation(state: ParkAccess, station: CountedStation, nowMs: number): ParkAccess {
  return { ...state, openedAtMs: nowMs, reached: Math.max(state.reached, indexOf(station)) };
}

export function openUntilMs(state: ParkAccess, thresholdMs: number): number | null {
  return state.openedAtMs === null ? null : state.openedAtMs + thresholdMs;
}

/** A clock set back before the opening counts as closed, not as extra time. */
export function isKnowledgeOpen(state: ParkAccess, nowMs: number, thresholdMs: number): boolean {
  if (state.guide) return true;
  const until = openUntilMs(state, thresholdMs);
  return until !== null && nowMs >= (state.openedAtMs as number) && nowMs < until;
}

/** Brisas and stations 1 and 2 are always open; station N opens once station N-1 was scanned. */
export function isStationUnlocked(state: ParkAccess, id: StationId): boolean {
  if (id === 'brisas' || state.guide) return true;
  return indexOf(id) <= Math.max(2, state.reached + 1);
}

/** The station whose QR opens `id` (the one before it), for the "scan this QR" hint. */
export function stationToScan(id: CountedStation): CountedStation | null {
  return COUNTED_STATIONS[indexOf(id) - 2] ?? null;
}

/** Stored access; anything missing or damaged is locked. */
export function parseParkAccess(raw: string | null): ParkAccess {
  try {
    const v: unknown = raw ? JSON.parse(raw) : null;
    if (typeof v !== 'object' || v === null) return LOCKED_ACCESS;
    const { openedAtMs, reached, guide } = v as Record<string, unknown>;
    const opened =
      typeof openedAtMs === 'number' && Number.isFinite(openedAtMs) ? openedAtMs : null;
    const r =
      typeof reached === 'number' && Number.isInteger(reached) && reached >= 0 ? reached : 0;
    const access = { openedAtMs: opened, reached: Math.min(r, COUNTED_STATIONS.length) };
    return guide === true ? { ...access, guide: true } : access;
  } catch {
    return LOCKED_ACCESS;
  }
}

export function validAccessHours(hours: number): boolean {
  return Number.isInteger(hours) && hours >= MIN_ACCESS_HOURS && hours <= MAX_ACCESS_HOURS;
}

/** Stored threshold in hours; anything missing, damaged or out of range is the default. */
export function parseAccessHours(raw: string | null): number {
  const n = raw !== null && /^\d+$/.test(raw) ? Number(raw) : NaN;
  return validAccessHours(n) ? n : DEFAULT_ACCESS_HOURS;
}
