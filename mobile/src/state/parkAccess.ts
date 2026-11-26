// Park access kept on the device (expo-sqlite kv-store, like verifiedOnly): the knowledge window's
// opening time, the highest station scanned, and the window length chosen in the admin screen.
import Storage from 'expo-sqlite/kv-store';
import { useEffect, useState, useSyncExternalStore } from 'react';

import {
  HOUR_MS,
  LOCKED_ACCESS,
  DEFAULT_ACCESS_HOURS,
  isKnowledgeOpen,
  openUntilMs,
  parseAccessHours,
  parseParkAccess,
  scanStation,
  validAccessHours,
  type CountedStation,
  type ParkAccess,
} from '@/core/access/parkAccess';

const ACCESS_KEY = 'park.access.v1';
const HOURS_KEY = 'park.accessHours.v1';

export interface ParkAccessState {
  access: ParkAccess;
  hours: number;
}

let state: ParkAccessState = { access: LOCKED_ACCESS, hours: DEFAULT_ACCESS_HOURS };
let loaded = false;
// Set before the saved value arrived: the visitor's change wins over the late read.
const changed = { access: false, hours: false };
const listeners = new Set<() => void>();
const emit = () => listeners.forEach((l) => l());

/** Starts reading the saved values; the chat store calls it at launch, before the first question. */
export function loadParkAccess() {
  if (loaded) return;
  loaded = true;
  Storage.getItemAsync(ACCESS_KEY).then(
    (raw) => {
      if (changed.access) return;
      state = { ...state, access: parseParkAccess(raw) };
      emit();
    },
    (e: unknown) => console.warn('Could not read the park access; the chat stays locked.', e),
  );
  Storage.getItemAsync(HOURS_KEY).then(
    (raw) => {
      if (changed.hours) return;
      state = { ...state, hours: parseAccessHours(raw) };
      emit();
    },
    (e: unknown) => console.warn('Could not read the access hours; the default applies.', e),
  );
}

export function getParkAccess(): ParkAccessState {
  loadParkAccess();
  return state;
}

/** Is the knowledge chat open right now? The chat reads it at each question. */
export function isKnowledgeOpenNow(nowMs = Date.now()): boolean {
  const { access, hours } = getParkAccess();
  return isKnowledgeOpen(access, nowMs, hours * HOUR_MS);
}

function saveAccess(access: ParkAccess): ParkAccess {
  changed.access = true;
  state = { ...state, access };
  emit();
  Storage.setItemAsync(ACCESS_KEY, JSON.stringify(access)).catch((e: unknown) =>
    console.warn('Could not save the park access; it lasts until the app closes.', e),
  );
  return access;
}

/** A valid station scan: reopens the window from now and keeps the highest station. */
export function recordStationScan(station: CountedStation, nowMs = Date.now()): ParkAccess {
  return saveAccess(scanStation(state.access, station, nowMs));
}

/** The admin password proved a guide holds this phone: the chat and every station open for good. */
export function unlockForGuide(): ParkAccess {
  return state.access.guide ? state.access : saveAccess({ ...state.access, guide: true });
}

export function setAccessHours(hours: number) {
  if (!validAccessHours(hours)) throw new RangeError(`Invalid access hours: ${hours}`);
  changed.hours = true;
  state = { ...state, hours };
  emit();
  Storage.setItemAsync(HOURS_KEY, String(hours)).catch((e: unknown) =>
    console.warn('Could not save the access hours; they last until the app closes.', e),
  );
}

const subscribe = (l: () => void) => {
  loadParkAccess();
  listeners.add(l);
  return () => {
    listeners.delete(l);
  };
};
const read = () => state;

export const useParkAccess = () => useSyncExternalStore(subscribe, read, read);

/** setTimeout's ceiling; a longer window re-checks then. */
const MAX_TIMEOUT_MS = 2 ** 31 - 1;

/** The chat's lock as a screen shows it: re-renders when a scan opens it and when it runs out. */
export function useKnowledgeOpen(): boolean {
  const { access, hours } = useParkAccess();
  const thresholdMs = hours * HOUR_MS;
  const [now, setNow] = useState(Date.now);
  const until = openUntilMs(access, thresholdMs);
  useEffect(() => {
    if (until === null) return;
    const id = setTimeout(
      () => setNow(Date.now()),
      Math.min(Math.max(0, until - Date.now()) + 50, MAX_TIMEOUT_MS),
    );
    return () => clearTimeout(id);
  }, [until]);
  // A scan after the last tick opened the window at its own "now".
  return isKnowledgeOpen(access, Math.max(now, access.openedAtMs ?? now), thresholdMs);
}
