import { chatLayout } from '@/chat/chatLayout';
import { petVentInScene } from '@/onboarding/scene/doc';
import { sceneViewBox } from '@/onboarding/scene/geometry';
import { defaultScene } from '@/onboarding/scene/preset';
import { evaluateTracks } from '@/onboarding/scene/timeline';
import { CLOUD_EDGE } from '@/ui/CloudCard';

const SIZES = [
  [360, 800],
  [390, 844],
  [430, 932],
  [820, 1180],
  [1180, 820],
];

describe('chat layout', () => {
  const doc = evaluateTracks(defaultScene(), 2);

  /** Where a point of the scene box lands on screen after the header's move and zoom. */
  function onScreen(l: ReturnType<typeof chatLayout>, w: number, p: { x: number; y: number }) {
    const c = { x: w / 2, y: l.sceneHeight / 2 };
    return {
      x: c.x + l.scene.x + l.scene.scale * (p.x - c.x),
      y: c.y + l.scene.y + l.scene.scale * (p.y - c.y),
    };
  }

  it.each(SIZES)('covers the header and the whole vapor edge with the scene at %ix%i', (w, h) => {
    const l = chatLayout(doc, w, h, { top: 24, bottom: 34 });
    // Outside the scene only the bare screen color would show, through the vapor too.
    const topLeft = onScreen(l, w, { x: 0, y: 0 });
    const bottomRight = onScreen(l, w, { x: w, y: l.sceneHeight });
    expect(topLeft.x).toBeLessThanOrEqual(0);
    expect(topLeft.y).toBeLessThanOrEqual(0);
    expect(bottomRight.x).toBeGreaterThanOrEqual(w);
    expect(bottomRight.y).toBeGreaterThanOrEqual(l.sheetTop + CLOUD_EDGE);
  });

  it.each(SIZES)('the keyboard lift covers the ranges and keeps the circle under the status bar at %ix%i', (w, h) => {
    const insets = { top: 24, bottom: 34 };
    const l = chatLayout(doc, w, h, insets);
    const circleTop = l.circle.y - l.circle.r - l.keyboardLift;
    expect(circleTop).toBeGreaterThanOrEqual(insets.top);
    expect(circleTop).toBeLessThanOrEqual(insets.top + 16);
    // The raised vapor edge sits higher than the crater spot the ranges are framed around.
    expect(l.sheetTop - l.keyboardLift).toBeLessThan(l.circle.y - l.circle.r - 40);
  });

  it.each(SIZES)('centers the crater spot just above the Pet circle at %ix%i', (w, h) => {
    const l = chatLayout(doc, w, h, { top: 24, bottom: 34 });
    const vb = sceneViewBox(w, l.sceneHeight);
    const vent = petVentInScene(doc, 'pet')!;
    const k = l.sceneHeight / vb.height;
    const at = onScreen(l, w, { x: (vent.x - vb.x) * k, y: (vent.y - vb.y) * k });
    expect(at.x).toBeCloseTo(l.circle.x, 5);
    expect(at.y).toBeLessThan(l.circle.y - l.circle.r);
    expect(at.y).toBeGreaterThan(l.circle.y - l.circle.r - 60);
    // Below the status bar, so the summit is never cut.
    expect(at.y).toBeGreaterThan(24 + 40);
  });

  it.each(SIZES)(
    'ends the handoff transform exactly where the chat draws the scene at %ix%i',
    (w, h) => {
      const l = chatLayout(doc, w, h, { top: 24, bottom: 34 });
      const topLeft = onScreen(l, w, { x: 0, y: 0 });
      const bottomRight = onScreen(l, w, { x: w, y: l.sceneHeight });
      expect(topLeft.x).toBeCloseTo(l.sceneRect.left, 6);
      expect(topLeft.y).toBeCloseTo(l.sceneRect.top, 6);
      expect(bottomRight.x).toBeCloseTo(l.sceneRect.left + l.sceneRect.width, 6);
      expect(bottomRight.y).toBeCloseTo(l.sceneRect.top + l.sceneRect.height, 6);
    },
  );

  it('keeps the sheet and the circle in place when the keyboard shortens the screen', () => {
    const full = chatLayout(doc, 390, 844, { top: 24, bottom: 34 });
    const typing = chatLayout(doc, 390, 500, { top: 24, bottom: 34 });
    expect(typing.sheetTop).toBe(full.sheetTop);
    expect(typing.circle).toEqual(full.circle);
  });
});
