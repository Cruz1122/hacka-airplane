// The card's copy and page dots move with native-driven interpolations of the progress value. They
// must draw what the overlay drew when it re-rendered on every frame, for any progress.
import { Animated } from 'react-native';

import { dotScale } from '@/ui/PageDots';

import { copyMotion } from '../OnboardingOverlay';
import { ONBOARDING_SCREENS } from '../scene/types';

// The per-frame formulas the overlay and PageDots used before.
const shown = (p: number) => Math.round(p);
const copyOpacity = (p: number) => 1 - Math.min(1, Math.abs(p - shown(p)) * 2);
const copyShift = (p: number) => -(p - shown(p)) * 40;
const scaleOf = (p: number, i: number) => 0.8 + 0.2 * Math.max(0, 1 - Math.abs(p - i));

type Node = { __getValue: () => number };
const read = (node: unknown) => (node as Node).__getValue();

// Every 1/100 of a screen, skipping the midpoints, where the old copy swapped its text.
const samples = Array.from({ length: (ONBOARDING_SCREENS - 1) * 100 + 1 }, (_, i) => i / 100).filter(
  (p) => Math.abs(p - Math.floor(p) - 0.5) > 1e-9,
);

it("shows the screen's copy as before and hides the others", () => {
  for (const p of samples) {
    const value = new Animated.Value(p);
    for (let k = 0; k < ONBOARDING_SCREENS; k++) {
      const m = copyMotion(value, k);
      const opacity = read(m.opacity);
      if (k === shown(p)) {
        expect(opacity).toBeCloseTo(copyOpacity(p), 9);
        expect(read(m.transform[0].translateX)).toBeCloseTo(copyShift(p), 9);
      } else expect(opacity).toBe(0);
    }
  }
});

it('scales the page dots as before', () => {
  for (const p of samples) {
    const value = new Animated.Value(p);
    for (let i = 0; i < ONBOARDING_SCREENS; i++)
      expect(read(dotScale(value, i))).toBeCloseTo(scaleOf(p, i), 9);
  }
});
