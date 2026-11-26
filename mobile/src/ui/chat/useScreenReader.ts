// Whether a screen reader is on: replies then show whole at once instead of typing out.
import { useEffect, useState } from 'react';
import { AccessibilityInfo } from 'react-native';

export function useScreenReader(): boolean {
  const [on, setOn] = useState(false);
  useEffect(() => {
    let alive = true;
    AccessibilityInfo.isScreenReaderEnabled().then(
      (v) => alive && setOn(v),
      (e: unknown) => console.warn('Screen reader setting unavailable; streaming replies.', e),
    );
    const sub = AccessibilityInfo.addEventListener('screenReaderChanged', setOn);
    return () => {
      alive = false;
      sub.remove();
    };
  }, []);
  return on;
}
