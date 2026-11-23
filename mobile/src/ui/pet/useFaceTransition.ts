// The Pet's own emotion change (fleibo-face), for hosts that draw single frames: when the emotion
// changes, the face morphs from whatever is on screen to the new pose over `ms` with `easing`,
// in real time, exactly like the Pet component's engine (`transitionFace`).
import { useEffect, useRef, useState } from 'react';

import {
  transitionFace,
  type EasingName,
  type FaceState,
  type PetConfig,
  type PetEmotion,
} from './petCore';

export function useFaceTransition(
  poses: PetConfig['poses'],
  emotion: PetEmotion,
  ms: number,
  easing: EasingName,
): FaceState {
  const [face, setFace] = useState(() => poses[emotion]);
  // The face last put on screen, so a change mid-morph starts from there instead of jumping.
  const shown = useRef(face);
  useEffect(() => {
    const from = shown.current;
    if (from === poses[emotion]) return;
    const cfg = { poses, emotion, motion: { transition: ms, easing } } as PetConfig;
    const start = performance.now();
    let raf = 0;
    // One clock for start and steps; the rAF timestamp's origin differs between hosts.
    const step = () => {
      const next = transitionFace(cfg, from, performance.now() - start);
      shown.current = next;
      setFace(next);
      if (next !== poses[emotion]) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
  }, [poses, emotion, ms, easing]);
  return face;
}
