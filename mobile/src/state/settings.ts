import Storage from 'expo-sqlite/kv-store';
import { useEffect, useState } from 'react';

export interface Settings {
  modelId: string;
  deviceStation: string | null;
  answerMode: 'extractive' | 'generate';
  // Off-topic turns get a free model reply instead of the fixed abstention.
  chat: boolean;
  backendKind: 'device' | 'http';
  httpUrl: string; // dev only: llama-server on the laptop or via adb forward
}

export const DEFAULT_SETTINGS: Settings = {
  modelId: 'gemma4-e2b',
  deviceStation: null,
  answerMode: 'extractive',
  chat: true,
  backendKind: 'device',
  httpUrl: 'http://127.0.0.1:8083',
};

const KEY = 'settings.v1';

export async function loadSettings(): Promise<Settings> {
  const raw = await Storage.getItemAsync(KEY);
  if (!raw) return DEFAULT_SETTINGS;
  try {
    return { ...DEFAULT_SETTINGS, ...(JSON.parse(raw) as Partial<Settings>) };
  } catch (e) {
    throw new Error(`Corrupt settings in kv-store: ${String(e)}`);
  }
}

export async function saveSettings(patch: Partial<Settings>): Promise<Settings> {
  const next = { ...(await loadSettings()), ...patch };
  await Storage.setItemAsync(KEY, JSON.stringify(next));
  return next;
}

// Settings screen state: loads once, writes through on every change.
export function useSettings() {
  const [settings, setSettings] = useState<Settings | null>(null);
  useEffect(() => {
    loadSettings().then(setSettings, () => setSettings(DEFAULT_SETTINGS));
  }, []);
  const update = (patch: Partial<Settings>) => {
    setSettings((s) => (s ? { ...s, ...patch } : s));
    void saveSettings(patch);
  };
  return { settings, update };
}
