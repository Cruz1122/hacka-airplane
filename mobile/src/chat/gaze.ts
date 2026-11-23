// Where the Pet looks while the visitor types: the last character of the draft, in window
// coordinates. A tiny store so each keystroke re-renders the Pet's circle, not the chat list.
import { useSyncExternalStore } from 'react';

export interface GazePoint {
  x: number;
  y: number;
}

export class GazeChannel {
  private point: GazePoint | null = null;
  private listeners = new Set<() => void>();

  set = (point: GazePoint | null) => {
    const p = this.point;
    if (p === point || (p && point && p.x === point.x && p.y === point.y)) return;
    this.point = point;
    this.listeners.forEach((l) => l());
  };

  get = () => this.point;

  subscribe = (listener: () => void) => {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  };
}

export function useGaze(channel: GazeChannel | undefined): GazePoint | null {
  return useSyncExternalStore(
    channel?.subscribe ?? noSubscribe,
    channel?.get ?? noPoint,
    channel?.get ?? noPoint,
  );
}

const noSubscribe = () => () => {};
const noPoint = () => null;
