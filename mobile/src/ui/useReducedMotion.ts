// System "reduce motion" setting + app accessibility preference; animations must stop or jump when either is on.
import { createContext, useContext, useEffect, useState } from 'react';
import { AccessibilityInfo } from 'react-native';

import { useAccessibility } from '@/state/accessibility';

export const ReducedMotionOverride = createContext(false);

export function useSystemReducedMotion(): boolean {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    let alive = true;
    AccessibilityInfo.isReduceMotionEnabled().then(
      (v) => alive && setReduced(v),
      (e: unknown) => console.warn('Reduce-motion setting unavailable; animating normally.', e),
    );
    const sub = AccessibilityInfo.addEventListener('reduceMotionChanged', setReduced);
    return () => {
      alive = false;
      sub.remove();
    };
  }, []);
  return reduced;
}

export function useReducedMotion(): boolean {
  const override = useContext(ReducedMotionOverride);
  const system = useSystemReducedMotion();
  const { reduceMotion } = useAccessibility();
  return system || reduceMotion || override;
}
