// The Settings switch "Solo información verificada por UTON": the knowledge chat answers only from
// entries taken from the official UTON guion. Kept on the device (expo-sqlite kv-store, like the
// alert distance) and off by default.
import Storage from 'expo-sqlite/kv-store';
import { useSyncExternalStore } from 'react';

const KEY = 'knowledge.verifiedOnly.v1';

/** Reads the stored switch; anything missing or damaged is off. */
export const parseVerifiedOnly = (raw: string | null) => raw === 'true';

let on = false;
let loaded = false;
let changed = false; // set before the saved value arrived: the visitor's choice wins
const listeners = new Set<() => void>();
const emit = () => listeners.forEach((l) => l());

/** Starts reading the saved value; the chat store calls it at launch, before the first question. */
export function loadVerifiedOnly() {
  if (loaded) return;
  loaded = true;
  Storage.getItemAsync(KEY).then(
    (raw) => {
      if (changed) return;
      on = parseVerifiedOnly(raw);
      emit();
    },
    (e: unknown) => console.warn('Could not read the verified-only setting; it stays off.', e),
  );
}

/** The switch as it is now (the chat reads it at each question). */
export function getVerifiedOnly(): boolean {
  loadVerifiedOnly();
  return on;
}

export function setVerifiedOnly(next: boolean) {
  changed = true;
  if (next === on) return;
  on = next;
  emit();
  Storage.setItemAsync(KEY, String(next)).catch((e: unknown) =>
    console.warn('Could not save the verified-only setting; it lasts until the app closes.', e),
  );
}

const subscribe = (l: () => void) => {
  loadVerifiedOnly();
  listeners.add(l);
  return () => {
    listeners.delete(l);
  };
};
const read = () => on;

export const useVerifiedOnly = () => useSyncExternalStore(subscribe, read, read);
