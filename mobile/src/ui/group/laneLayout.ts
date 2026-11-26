// Where each lane dot sits on screen. Every dot stays ON the line; crowding is resolved along it:
// dots keep their order by t, stand at least `gap` apart (a dot's diameter plus a margin), and a
// crowd is centred on where its dots want to be. A line too short for everyone spaces them
// evenly. Names go right of the line, and switch to the left when the name above would collide.
import type { LaneDot } from '@/core/group/lane';

export interface PlacedDot {
  dot: LaneDot;
  /** Centre of the dot, in points along the line. */
  y: number;
  /** Which side of the line its name goes. */
  side: 'left' | 'right';
}

export interface LaneBounds {
  /** Highest and lowest centre a dot may take (clear of the guide markers). */
  top: number;
  bottom: number;
  /** Minimum distance between two dot centres. */
  gap: number;
  /** Height a name needs on its side before the next name can sit there. */
  labelRow: number;
}

const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));

/** The centres along the line, in t order, at least `gap` apart and inside [top, bottom]. */
function spread(ideal: number[], top: number, bottom: number, gap: number): number[] {
  const n = ideal.length;
  if (n === 0) return [];
  if (n > 1 && (n - 1) * gap > bottom - top) {
    const step = (bottom - top) / (n - 1);
    return ideal.map((_, i) => top + i * step);
  }
  // Runs of dots that touch, each centred on the mean of where its dots want to be.
  const runs: { first: number; count: number; sum: number }[] = [];
  const startOf = (r: (typeof runs)[number]) =>
    clamp(r.sum / r.count, top, bottom - (r.count - 1) * gap);
  ideal.forEach((y, i) => {
    runs.push({ first: i, count: 1, sum: y });
    while (runs.length > 1) {
      const last = runs[runs.length - 1];
      const prev = runs[runs.length - 2];
      if (startOf(last) >= startOf(prev) + prev.count * gap) break;
      // Merged: dot k of the run sits (k - first) gaps below the run's start, so the start that
      // best fits every dot is the mean of each dot's wish minus its offset.
      prev.sum += last.sum - last.count * (last.first - prev.first) * gap;
      prev.count += last.count;
      runs.pop();
    }
  });
  return runs.flatMap((r) => {
    const start = startOf(r);
    return Array.from({ length: r.count }, (_, k) => start + k * gap);
  });
}

/** Dots in t order (ties keep join order), each with its centre and name side. */
export function layoutLane(dots: LaneDot[], b: LaneBounds): PlacedDot[] {
  const byT = dots.map((dot, i) => ({ dot, i })).sort((x, y) => x.dot.t - y.dot.t || x.i - y.i);
  const ys = spread(
    byT.map(({ dot }) => b.top + clamp(dot.t, 0, 1) * (b.bottom - b.top)),
    b.top,
    b.bottom,
    b.gap,
  );
  let lastRight = -Infinity;
  let lastLeft = -Infinity;
  return byT.map(({ dot }, k) => {
    const y = ys[k];
    // Right unless the name above on the right is too close; then whichever side has more room.
    const side: PlacedDot['side'] =
      y - lastRight >= b.labelRow || lastRight <= lastLeft ? 'right' : 'left';
    if (side === 'right') lastRight = y;
    else lastLeft = y;
    return { dot, y, side };
  });
}
