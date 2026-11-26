// The guide's alert distance (the slider on Grupo), in meters. Kept on the device (expo-sqlite
// kv-store, like the Pet looks) and shared by every screen through one module store.
import Storage from 'expo-sqlite/kv-store';
import { useSyncExternalStore } from 'react';

import { GROUP_POLICY } from '@/core/group/policy';

const { min, max, step, default: DEFAULT_METERS } = GROUP_POLICY.alertMeters;
const KEY = 'group.alertMeters.v1';

/** On the policy's step, inside its range. */
export const snapAlertMeters = (meters: number) =>
  Math.min(max, Math.max(min, min + Math.round((meters - min) / step) * step));

/** Reads the stored distance; anything missing or damaged is the default. */
export function parseAlertMeters(raw: string | null): number {
  const n = raw === null ? NaN : Number(raw);
  return Number.isFinite(n) ? snapAlertMeters(n) : DEFAULT_METERS;
}

let meters: number = DEFAULT_METERS;
let loaded = false;
const listeners = new Set<() => void>();
const emit = () => listeners.forEach((l) => l());

function load() {
  if (loaded) return;
  loaded = true;
  Storage.getItemAsync(KEY).then(
    (raw) => {
      meters = parseAlertMeters(raw);
      emit();
    },
    (e: unknown) => console.warn('Could not read the saved alert distance; using the default.', e),
  );
}

export function setAlertDistance(next: number) {
  const snapped = snapAlertMeters(next);
  if (snapped === meters) return;
  meters = snapped;
  emit();
  Storage.setItemAsync(KEY, String(snapped)).catch((e: unknown) =>
    console.warn('Could not save the alert distance; it lasts until the app closes.', e),
  );
}

const subscribe = (l: () => void) => {
  load();
  listeners.add(l);
  return () => {
    listeners.delete(l);
  };
};
const read = () => meters;

export const useAlertDistance = () => useSyncExternalStore(subscribe, read, read);
