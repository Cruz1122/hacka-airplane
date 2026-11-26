import Storage from 'expo-sqlite/kv-store';
import { useSyncExternalStore } from 'react';

const KEY = 'performance.monitor.v1';
const listeners = new Set<() => void>();
let enabled = false;
let loaded = false;
let changed = false;

function update(value: boolean) {
  if (value === enabled) return;
  enabled = value;
  listeners.forEach((notify) => notify());
}

function subscribe(notify: () => void) {
  listeners.add(notify);
  if (!loaded) {
    loaded = true;
    void Storage.getItemAsync(KEY).then(
      (value) => { if (!changed) update(value === 'true'); },
      (error: unknown) => console.warn('Could not read the performance monitor setting.', error),
    );
  }
  return () => { listeners.delete(notify); };
}

export function setPerformanceMonitor(value: boolean) {
  changed = true;
  update(value);
  void Storage.setItemAsync(KEY, String(value)).catch((error: unknown) =>
    console.warn('Could not save the performance monitor setting.', error),
  );
}

const snapshot = () => enabled;
export const usePerformanceMonitor = () => useSyncExternalStore(subscribe, snapshot, () => false);
