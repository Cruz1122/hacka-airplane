// System "reduce motion" setting; animations must stop or jump when it is on.
import { createContext, useContext, useEffect, useState } from 'react';
import { AccessibilityInfo } from 'react-native';

export const ReducedMotionOverride = createContext(false);

export function useReducedMotion(): boolean {
  const override = useContext(ReducedMotionOverride);
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
  return reduced || override;
}
