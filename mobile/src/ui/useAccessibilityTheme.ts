// Reactive accessibility theme hook: combines the persisted accessibility store with the
// design-token palettes and typography scale so screens update immediately on any change.
import { useMemo } from 'react';

import { useAccessibility, type AccessibilityPrefs } from '@/state/accessibility';

import { resolveBrand, type, type BrandPalette } from './theme/tokens';

type ScaledEntry<T extends { fontSize: number; lineHeight: number }> = Omit<
  T,
  'fontSize' | 'lineHeight'
> & {
  fontSize: number;
  lineHeight: number;
};

export type ScaledType = {
  [K in keyof typeof type]: ScaledEntry<(typeof type)[K]>;
};

export function scaleSize(base: number, scale: number): number {
  return Math.round(base * scale);
}

export function buildScaledType(scale: number): ScaledType {
  const s = <T extends { fontSize: number; lineHeight: number }>(tStyle: T): ScaledEntry<T> => ({
    ...tStyle,
    fontSize: scaleSize(tStyle.fontSize, scale),
    lineHeight: scaleSize(tStyle.lineHeight, scale),
  });
  return {
    display: s(type.display),
    title: s(type.title),
    body: s(type.body),
    label: s(type.label),
    caption: s(type.caption),
  };
}

export interface AccessibilityTheme extends AccessibilityPrefs {
  palette: BrandPalette;
  scaled: ScaledType;
  /** Thicker crisp outlines in high-contrast mode for outdoor glare. */
  borderWidth: number;
}

export function useAccessibilityTheme(): AccessibilityTheme {
  const prefs = useAccessibility();
  const palette = useMemo(
    () => resolveBrand(prefs.colorVision, prefs.highContrast),
    [prefs.colorVision, prefs.highContrast],
  );
  const scaled = useMemo(() => buildScaledType(prefs.textScale), [prefs.textScale]);
  return useMemo(
    () => ({
      ...prefs,
      palette,
      scaled,
      borderWidth: prefs.highContrast ? 1.5 : 1,
    }),
    [prefs, palette, scaled],
  );
}
