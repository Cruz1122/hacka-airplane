// When the Pet's loop draws, and how a drawn frame reaches the one component that paints it. The
// loop ticks every display frame (cheap: a few numbers), but a frame costs a petFrame() and a
// redraw on the JS thread the chat shares with typing, the streamed reply and the model, so it
// only draws when the picture would change enough to see.
import { useSyncExternalStore } from 'react';

import { DEFAULT_TRACKING, type FaceState, type PetFrame } from './petCore';

/** What petFrame() turns into a picture; equal inputs draw the same picture. */
export interface FrameInputs {
  time: number;
  face: FaceState;
  blink: number;
  gazeX: number;
  gazeY: number;
  mirror: number;
}

/**
 * Rate of the slow procedural motion: breathing, floating, vapor, tail, the speaking mouth and a
 * gaze easing toward its target. A blink, a face morph and the turn draw every display frame.
 */
export const AMBIENT_HZ = 30;
/**
 * Vsyncs land a little early or late. Without slack, 30 Hz on a 90 Hz screen would wait for
 * every 4th vsync (22.5 Hz); with it, every 3rd at 90 Hz, 2nd at 60 Hz and 4th at 120 Hz.
 */
const VSYNC_SLACK_MS = 4;
/**
 * Eye travel since the last drawn frame, in Pet units, that is drawn at once instead of waiting
 * for the ambient rate: a glance starts fast, typing moves the gaze a fraction of this per key.
 */
export const GAZE_STEP = 0.5;

export function shouldDraw(last: FrameInputs | null, next: FrameInputs, sinceLastMs: number) {
  if (!last) return true;
  if (next.face !== last.face || next.blink !== last.blink || next.mirror !== last.mirror) {
    return true;
  }
  const t = DEFAULT_TRACKING;
  const travel = Math.max(
    Math.abs(next.gazeX - last.gazeX) * t.maxMoveX,
    Math.abs(next.gazeY - last.gazeY) * t.maxMoveY * t.eyeVerticalBoost,
  );
  if (travel >= GAZE_STEP) return true;
  if (travel === 0 && next.time === last.time) return false;
  return sinceLastMs >= 1000 / AMBIENT_HZ - VSYNC_SLACK_MS;
}

/** The latest drawn frame. Only the canvas subscribes, so a new frame re-renders nothing else. */
export class FrameStore {
  private listeners = new Set<() => void>();

  constructor(private frame: PetFrame) {}

  set = (frame: PetFrame) => {
    this.frame = frame;
    this.listeners.forEach((l) => l());
  };

  get = () => this.frame;

  subscribe = (listener: () => void) => {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  };
}

export const useFrame = (store: FrameStore) =>
  useSyncExternalStore(store.subscribe, store.get, store.get);
