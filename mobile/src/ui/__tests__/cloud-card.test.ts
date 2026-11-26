import { EMBLEM_TOP } from '@/onboarding/layout';
import { CLOUD_EDGE, VAPOR_BODY_TOP, vaporPuffs } from '@/ui/CloudCard';

const WIDTHS = [320, 360, 390, 430, 820, 1180];

describe('cloud card vapor edge', () => {
  it.each(WIDTHS)('keeps every billow inside the drawing at %i pt', (width) => {
    expect(vaporPuffs(width).filter((p) => p.y - p.ry < 0)).toEqual([]);
  });

  it.each(WIDTHS)('covers the whole width with billows at %i pt', (width) => {
    const puffs = [...vaporPuffs(width)].sort((a, b) => a.x - b.x);
    expect(puffs[0].x - puffs[0].rx).toBeLessThan(0);
    expect(puffs[puffs.length - 1].x + puffs[puffs.length - 1].rx).toBeGreaterThan(width);
    // Neighbours overlap, so no gap shows the body's straight top between them.
    for (let i = 1; i < puffs.length; i++) {
      expect(puffs[i].x - puffs[i].rx).toBeLessThan(puffs[i - 1].x + puffs[i - 1].rx);
    }
  });

  it('starts the solid body above the end of the scene and the emblem', () => {
    // Below CLOUD_EDGE the scene drawing has ended: an uncovered gap would show the bare sky.
    expect(VAPOR_BODY_TOP).toBeLessThanOrEqual(CLOUD_EDGE);
    // The emblem's transparent corners must not show the scene through the vapor.
    expect(VAPOR_BODY_TOP).toBeLessThanOrEqual(EMBLEM_TOP);
  });
});
