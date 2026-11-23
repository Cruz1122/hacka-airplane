import { headerScene } from '@/chat/headerScene';
import { chatLayout } from '@/chat/chatLayout';
import { HEADER_PEAKS } from '@/chat/headerPeaks';
import { locate, petVentInScene, resolveColor, volcanoOf } from '@/onboarding/scene/doc';
import {
  applyAffine,
  applyTransform,
  parallaxAffine,
  sceneViewBox,
} from '@/onboarding/scene/geometry';
import { DEFAULT_PALETTE, defaultScene } from '@/onboarding/scene/preset';
import { evaluateTracks } from '@/onboarding/scene/timeline';
import type { VolcanoBody } from '@/onboarding/scene/types';
import { CLOUD_EDGE, VAPOR_BODY_TOP } from '@/ui/CloudCard';

const STATUS_BAR = 24;

/**
 * Where a point of a peak lands on screen in the chat header of a w x h screen; `at` picks it in
 * the volcano's own units (default: the summit).
 */
function onScreen(
  id: string,
  w: number,
  h: number,
  at: (b: VolcanoBody) => { x: number; y: number } = (b) => ({ x: b.summitOffset, y: -b.height }),
) {
  const l = chatLayout(headerScene, w, h, { top: STATUS_BAR, bottom: 34 });
  const hit = locate(headerScene, id)!;
  if (hit.object.body.kind !== 'volcano') throw new Error(`${id} is not a volcano`);
  const local = applyTransform(hit.object.transform, at(hit.object.body));
  const scene = applyAffine(parallaxAffine(headerScene.camera, hit.layer.parallax), local);
  const vb = sceneViewBox(w, l.sceneHeight);
  const toBox = l.sceneHeight / vb.height;
  return {
    l,
    x: l.sceneRect.left + l.scene.scale * (scene.x - vb.x) * toBox,
    y: l.sceneRect.top + l.scene.scale * (scene.y - vb.y) * toBox,
  };
}

describe('chat header peaks', () => {
  it('draws every peak with its glacier and keeps the hidden volcano that places the header', () => {
    for (const p of HEADER_PEAKS) {
      const snow = locate(headerScene, `${p.id}-snow`)!;
      expect(volcanoOf(headerScene, snow.object.body)?.object.id).toBe(p.id);
      expect(snow.layer.id).toBe(p.layer);
      expect(snow.layer.visible).toBe(true);
    }
    const anchor = locate(headerScene, 'volcano')!;
    expect(anchor.layer.visible).toBe(false);
    expect(petVentInScene(headerScene, 'pet')).toEqual(
      petVentInScene(evaluateTracks(defaultScene(), 2), 'pet'),
    );
  });

  it('paints every visible range and peak in warm earth, keeping sky, snow, ice and mist', () => {
    const rgb = (c: string) => {
      const n = parseInt(resolveColor(headerScene.palette, c).slice(1), 16);
      return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
    };
    const ranges = headerScene.layers.filter(
      (l) => l.visible && (l.id === 'farMountains' || l.id === 'midMountains'),
    );
    expect(ranges).toHaveLength(2);
    for (const o of ranges.flatMap((l) => l.objects)) {
      const b = o.body;
      const rock =
        b.kind === 'ridge'
          ? [b.top, b.bottom, b.shade]
          : b.kind === 'volcano'
            ? [b.fill, b.ash, b.shade, b.gully]
            : [];
      for (const c of rock) {
        const [r, g, bl] = rgb(c);
        // Brown: red over green over blue (the onboarding's violet ranges are blue-heavy).
        expect({ id: o.id, c, warm: r > g && g > bl }).toEqual({ id: o.id, c, warm: true });
      }
    }
    for (const key of ['skyTop', 'skyMid', 'skyHorizon', 'snow', 'ice', 'mist', 'cloud']) {
      expect(headerScene.palette[key]).toBe(DEFAULT_PALETTE[key]);
    }
  });

  it('leaves the onboarding scene untouched', () => {
    expect(defaultScene().palette).toEqual(DEFAULT_PALETTE);
    expect(locate(defaultScene(), 'peak-ruiz')).toBeNull();
    expect(locate(defaultScene(), 'far-range')!.object.body).toMatchObject({
      detail: 40,
    });
  });

  it.each([
    [360, 800],
    [390, 844],
    [430, 932],
    [820, 1180],
    [1280, 800],
  ])('shows Ruiz over the Pet circle and Santa Isabel beside it at %ix%i', (w, h) => {
    const ruiz = onScreen('peak-ruiz', w, h);
    const { circle, sheetTop } = ruiz.l;
    expect(Math.abs(ruiz.x - circle.x)).toBeLessThan(circle.r);
    // The plateau clears the status bar and stands well above the circle, not cut by the sheet.
    expect(ruiz.y).toBeGreaterThan(STATUS_BAR + 40);
    expect(ruiz.y).toBeLessThan(circle.y - circle.r - 60);
    const isabel = onScreen('peak-santa-isabel', w, h);
    expect(isabel.x).toBeGreaterThan(circle.x + circle.r);
    expect(isabel.x).toBeLessThan(w);
    expect(isabel.y).toBeGreaterThan(ruiz.y);
    expect(isabel.y).toBeLessThan(sheetTop + CLOUD_EDGE / 2 - 40);
  });

  it.each([
    [360, 800],
    [390, 844],
    [820, 1180],
    [1280, 800],
  ])("keeps every peak's foot under the solid sheet at %ix%i", (w, h) => {
    for (const p of HEADER_PEAKS) {
      // The silhouette runs flat 80 units past each foot (volcanoPath), so check out there.
      for (const side of [-1, 1]) {
        const foot = onScreen(p.id, w, h, (b) => ({ x: side * (b.baseWidth / 2 + 80), y: 6 }));
        if (foot.x < 0 || foot.x > w) continue;
        expect(foot.y).toBeGreaterThan(foot.l.sheetTop + VAPOR_BODY_TOP);
      }
    }
  });

  it.each([
    [390, 844],
    [820, 1180],
    [1280, 800],
  ])('raises the Tolima cone above the others, on screen, at %ix%i', (w, h) => {
    const tolima = onScreen('peak-tolima', w, h);
    expect(tolima.x).toBeGreaterThan(onScreen('peak-santa-isabel', w, h).x);
    expect(tolima.x).toBeLessThan(w);
    expect(tolima.y).toBeGreaterThan(STATUS_BAR);
    expect(tolima.y).toBeLessThan(onScreen('peak-ruiz', w, h).y);
  });
});
