// Persisted accessibility preferences shared across the app via one external store.
// Stored locally in expo-sqlite/kv-store; defaults preserve the original brand palette,
// system text size, and system reduced-motion setting.
import Storage from 'expo-sqlite/kv-store';
import { useSyncExternalStore } from 'react';

const KEY = 'accessibility.prefs.v1';

export const COLOR_VISION_MODES = ['none', 'protanopia', 'deuteranopia', 'tritanopia'] as const;
export type ColorVisionMode = (typeof COLOR_VISION_MODES)[number];

export const TEXT_SCALE_STEPS = [1, 1.15, 1.3, 1.45] as const;
export type TextScale = (typeof TEXT_SCALE_STEPS)[number];

export interface AccessibilityPrefs {
  textScale: TextScale;
  highContrast: boolean;
  reduceMotion: boolean;
  colorVision: ColorVisionMode;
}

export const DEFAULT_ACCESSIBILITY: AccessibilityPrefs = {
  textScale: 1,
  highContrast: false,
  reduceMotion: false,
  colorVision: 'none',
};

const COLOR_VISION_SET = new Set<string>(COLOR_VISION_MODES);

/** Snaps any numeric value to the closest supported text scale step. */
export function snapTextScale(value: number): TextScale {
  if (!Number.isFinite(value)) return DEFAULT_ACCESSIBILITY.textScale;
  let best: TextScale = TEXT_SCALE_STEPS[0];
  let bestDiff = Math.abs(value - best);
  for (const step of TEXT_SCALE_STEPS) {
    const diff = Math.abs(value - step);
    if (diff < bestDiff) {
      best = step;
      bestDiff = diff;
    }
  }
  return best;
}

export function textScaleIndex(scale: TextScale): number {
  const idx = TEXT_SCALE_STEPS.indexOf(scale);
  return idx >= 0 ? idx : 0;
}

export function textScaleFromIndex(index: number): TextScale {
  const clamped = Math.max(0, Math.min(TEXT_SCALE_STEPS.length - 1, Math.round(index)));
  return TEXT_SCALE_STEPS[clamped];
}

export function isDefaultAccessibility(p: AccessibilityPrefs): boolean {
  return (
    p.textScale === DEFAULT_ACCESSIBILITY.textScale &&
    p.highContrast === DEFAULT_ACCESSIBILITY.highContrast &&
    p.reduceMotion === DEFAULT_ACCESSIBILITY.reduceMotion &&
    p.colorVision === DEFAULT_ACCESSIBILITY.colorVision
  );
}

/** Parses stored JSON defensively; malformed or missing fields fall back to defaults. */
export function parseAccessibility(raw: string | null): AccessibilityPrefs {
  if (!raw) return DEFAULT_ACCESSIBILITY;
  try {
    const parsed: unknown = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object') return DEFAULT_ACCESSIBILITY;
    const row = parsed as Record<string, unknown>;
    const textScale =
      typeof row.textScale === 'number'
        ? snapTextScale(row.textScale)
        : DEFAULT_ACCESSIBILITY.textScale;
    const highContrast =
      typeof row.highContrast === 'boolean' ? row.highContrast : DEFAULT_ACCESSIBILITY.highContrast;
    const reduceMotion =
      typeof row.reduceMotion === 'boolean' ? row.reduceMotion : DEFAULT_ACCESSIBILITY.reduceMotion;
    const colorVision =
      typeof row.colorVision === 'string' && COLOR_VISION_SET.has(row.colorVision)
        ? (row.colorVision as ColorVisionMode)
        : DEFAULT_ACCESSIBILITY.colorVision;
    return { textScale, highContrast, reduceMotion, colorVision };
  } catch {
    return DEFAULT_ACCESSIBILITY;
  }
}

let prefs: AccessibilityPrefs = DEFAULT_ACCESSIBILITY;
let loaded = false;
let mutated = false;
const listeners = new Set<() => void>();
const emit = () => listeners.forEach((l) => l());

function load() {
  if (loaded) return;
  loaded = true;
  Storage.getItemAsync(KEY).then(
    (raw) => {
      if (!mutated) {
        prefs = parseAccessibility(raw);
        emit();
      }
    },
    (e: unknown) => console.warn('Could not read accessibility preferences; using defaults.', e),
  );
}

function persist(next: AccessibilityPrefs) {
  mutated = true;
  prefs = next;
  emit();
  Storage.setItemAsync(KEY, JSON.stringify(next)).catch((e: unknown) =>
    console.warn('Could not save accessibility preferences.', e),
  );
}

export function setAccessibility(patch: Partial<AccessibilityPrefs>) {
  const next: AccessibilityPrefs = {
    textScale: patch.textScale !== undefined ? snapTextScale(patch.textScale) : prefs.textScale,
    highContrast: patch.highContrast ?? prefs.highContrast,
    reduceMotion: patch.reduceMotion ?? prefs.reduceMotion,
    colorVision: patch.colorVision ?? prefs.colorVision,
  };
  if (
    next.textScale === prefs.textScale &&
    next.highContrast === prefs.highContrast &&
    next.reduceMotion === prefs.reduceMotion &&
    next.colorVision === prefs.colorVision
  ) {
    return;
  }
  persist(next);
}

export function resetAccessibility() {
  if (isDefaultAccessibility(prefs)) return;
  persist(DEFAULT_ACCESSIBILITY);
}

/** Test helper to reset module state between suites. */
export function resetAccessibilityForTest() {
  prefs = DEFAULT_ACCESSIBILITY;
  loaded = true;
  mutated = false;
  emit();
}

const subscribe = (l: () => void) => {
  load();
  listeners.add(l);
  return () => {
    listeners.delete(l);
  };
};

const read = (): AccessibilityPrefs => prefs;

export const useAccessibility = (): AccessibilityPrefs => useSyncExternalStore(subscribe, read, read);
