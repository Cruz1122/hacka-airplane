import type { LaneDot } from '@/core/group/lane';
import { memberId } from '@/core/group/types';

import { layoutLane, type LaneBounds } from '../laneLayout';

const dot = (id: string, t: number): LaneDot => ({
  id: memberId(id),
  name: id,
  t,
  status: 'mid',
  alerting: false,
});

const B: LaneBounds = { top: 50, bottom: 450, gap: 64, labelRow: 24 };
const ids = (ps: ReturnType<typeof layoutLane>) => ps.map((p) => p.dot.id);
const gaps = (ps: ReturnType<typeof layoutLane>) => ps.slice(1).map((p, i) => p.y - ps[i].y);

describe('layoutLane', () => {
  it('puts a lone dot where its t says', () => {
    expect(layoutLane([dot('a', 0.5)], B)).toEqual([{ dot: dot('a', 0.5), y: 250, side: 'right' }]);
  });

  it('keeps the order by t, ties in join order', () => {
    const placed = layoutLane([dot('c', 0.9), dot('a', 0.1), dot('b', 0.5), dot('b2', 0.5)], B);
    expect(ids(placed)).toEqual(['a', 'b', 'b2', 'c']);
  });

  it('keeps crowded dots a gap apart, centred on where they want to be', () => {
    const placed = layoutLane([dot('a', 0.5), dot('b', 0.5), dot('c', 0.52)], B);
    for (const g of gaps(placed)) expect(g).toBeCloseTo(B.gap, 6);
    const mean = placed.reduce((s, p) => s + p.y, 0) / placed.length;
    const wanted = (250 + 250 + 258) / 3;
    expect(mean).toBeCloseTo(wanted, 6);
  });

  it('never leaves the line ends (the guide markers)', () => {
    const placed = layoutLane([dot('a', 0), dot('b', 0), dot('c', 1), dot('d', 1)], B);
    expect(placed[0].y).toBe(B.top);
    expect(placed.at(-1)!.y).toBe(B.bottom);
    for (const g of gaps(placed)) expect(g).toBeGreaterThanOrEqual(B.gap - 1e-9);
  });

  it('spaces dots evenly when the line is too short for all of them', () => {
    const many = Array.from({ length: 9 }, (_, i) => dot(`v${i}`, 0.4 + i * 0.001));
    const placed = layoutLane(many, B);
    expect(placed[0].y).toBe(B.top);
    expect(placed.at(-1)!.y).toBe(B.bottom);
    for (const g of gaps(placed)) expect(g).toBeCloseTo((B.bottom - B.top) / 8, 6);
  });

  it('moves a name to the other side only when the one above would collide', () => {
    const roomy = layoutLane([dot('a', 0.1), dot('b', 0.6)], B);
    expect(roomy.map((p) => p.side)).toEqual(['right', 'right']);
    const tight = layoutLane(
      Array.from({ length: 30 }, (_, i) => dot(`v${i}`, 0.5)),
      B,
    );
    // 400 pt for 30 dots: 13.8 pt apart, under one name row, so names alternate.
    expect(tight.slice(0, 4).map((p) => p.side)).toEqual(['right', 'left', 'right', 'left']);
  });
});
