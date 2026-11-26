import { LOCALES } from '@/i18n';
import { handlesOf, PARAMS } from '@/lab/params';
import { parseScene } from '@/lab/useSceneHistory';
import { onboardingLayout } from '@/onboarding/layout';
import { blinkAt, PET_PRESET, PET_VIEWBOX, petFrame } from '@/ui/pet/petCore';

import {
  craterOf,
  deleteObject,
  duplicateObject,
  locate,
  petPointInScene,
  resolveColor,
  shiftLayer,
  updateObject,
  ventOf,
  volcanoOf,
} from '../doc';
import {
  CAMERA_FOCUS,
  cameraDelta,
  parallaxAffine,
  parallaxMatrix,
  cloudPuffs,
  craterPaths,
  flowerPetals,
  frailejonShape,
  lupineShape,
  MAX_VIEW_WIDTH,
  mistPuffs,
  ridgeGrass,
  ridgePath,
  ridgeShadePaths,
  rockPaths,
  sceneViewBox,
  snowPaths,
  steamPuffs,
  transformMatrix,
  tuftBlades,
  volcanoErosion,
  volcanoPath,
  viewTransform,
  volcanoShadePath,
} from '../geometry';
import { defaultScene } from '../preset';
import {
  applyMotions,
  commitEdit,
  evaluateTracks,
  readTarget,
  toggleKeyframe,
  valueAt,
  writeTarget,
} from '../timeline';
import type { Body, SceneDoc, SceneObject } from '../types';
import { LAYER_IDS, ONBOARDING_SCREENS, SCENE_HEIGHT, SCENE_VERSION } from '../types';

const allObjects = (doc: SceneDoc): SceneObject[] => doc.layers.flatMap((l) => l.objects);

/** Everything a body would draw, flattened to strings so NaN/Infinity can be detected. */
function drawn(doc: SceneDoc, b: Body): string {
  const volcano = (id: string) => {
    const hit = locate(doc, id);
    if (hit?.object.body.kind !== 'volcano') throw new Error(`no volcano ${id}`);
    return hit.object.body;
  };
  switch (b.kind) {
    case 'ridge':
      return ridgePath(b) + ridgeShadePaths(b).join() + ridgeGrass(b);
    case 'volcano':
      return volcanoPath(b) + volcanoShadePath(b) + Object.values(volcanoErosion(b)).join();
    case 'snowCap':
      return Object.values(snowPaths(volcano(b.volcano), b)).join();
    case 'crater':
      return Object.values(craterPaths(volcano(b.volcano), b)).join();
    case 'steam':
      return JSON.stringify(steamPuffs(b));
    case 'cloud':
      return JSON.stringify(cloudPuffs(b));
    case 'frailejon':
      return JSON.stringify(frailejonShape(b));
    case 'flower':
      return flowerPetals(b);
    case 'rock':
      return Object.values(rockPaths(b)).join();
    case 'tuft':
      return JSON.stringify(tuftBlades(b));
    case 'mist':
      return JSON.stringify(mistPuffs(b));
    case 'lupine':
      return JSON.stringify(lupineShape(b));
    case 'pet': {
      const cfg = { ...PET_PRESET, emotion: b.emotion, voice: b.voice, audio: b.audio };
      return JSON.stringify(
        petFrame(cfg, {
          time: b.clock,
          face: cfg.poses[b.emotion],
          blink: blinkAt(b.clock, cfg.motion.blinkInterval),
        }),
      );
    }
    default:
      return '';
  }
}

describe('default scene', () => {
  const doc = defaultScene();

  it('has the 14 layers back to front', () => {
    expect(doc.layers.map((l) => l.id)).toEqual([...LAYER_IDS]);
  });

  it('draws every object with finite coordinates', () => {
    for (const o of allObjects(doc)) {
      const out = drawn(doc, o.body);
      expect({ id: o.id, bad: /NaN|Infinity|null/.test(out) }).toEqual({
        id: o.id,
        bad: false,
      });
    }
  });

  it('resolves every palette reference', () => {
    for (const o of allObjects(doc)) {
      for (const v of [o.stroke, ...Object.values(o.body)]) {
        if (typeof v === 'string' && v.startsWith('$'))
          expect(() => resolveColor(doc.palette, v)).not.toThrow();
      }
    }
  });

  it('survives a JSON round trip through the import boundary', () => {
    const parsed = parseScene(JSON.parse(JSON.stringify(doc)));
    expect(parsed).toEqual({ doc });
  });
});

describe('editor parameters', () => {
  it('cover every body field of the preset, with preset values inside their ranges', () => {
    for (const o of allObjects(defaultScene())) {
      const specs = PARAMS[o.body.kind] as {
        key: string;
        type: string;
        min?: number;
        max?: number;
        options?: readonly string[];
      }[];
      for (const [k, v] of Object.entries(o.body)) {
        if (k === 'kind' || k === 'volcano' || k === 'points') continue;
        const spec = specs.find((p) => p.key === k);
        expect({ id: o.id, k, spec: Boolean(spec) }).toEqual({
          id: o.id,
          k,
          spec: true,
        });
        if (spec?.type === 'select') {
          expect({ id: o.id, k, known: spec.options!.includes(v as string) }).toEqual({
            id: o.id,
            k,
            known: true,
          });
        } else if (spec && spec.type !== 'color') {
          expect({
            id: o.id,
            k,
            inRange: (v as number) >= spec.min! && (v as number) <= spec.max!,
          }).toEqual({ id: o.id, k, inRange: true });
        }
      }
    }
  });
});

describe('handles', () => {
  const doc = defaultScene();

  it('leave the body unchanged when dropped where they are', () => {
    for (const o of allObjects(doc)) {
      for (const h of handlesOf(o.body, doc)) {
        const after = h.set(h.at);
        for (const [k, v] of Object.entries(after)) {
          const before = (o.body as unknown as Record<string, unknown>)[k];
          if (typeof v === 'number')
            expect({
              id: o.id,
              handle: h.key,
              k,
              v: Math.round(v * 10) / 10,
            }).toEqual({
              id: o.id,
              handle: h.key,
              k,
              v: Math.round((before as number) * 10) / 10,
            });
        }
      }
    }
  });

  it('raise the volcano summit and keep the snow attached', () => {
    const summit = handlesOf(locate(doc, 'volcano')!.object.body, doc).find(
      (h) => h.key === 'summit',
    )!;
    const raised = updateObject(doc, 'volcano', (o) => ({
      ...o,
      body: summit.set({ x: 0, y: -320 }),
    }));
    const body = locate(raised, 'volcano')!.object.body;
    expect(body.kind === 'volcano' && body.height).toBe(320);
    const snowBefore = drawn(doc, locate(doc, 'snow')!.object.body);
    const snowAfter = drawn(raised, locate(raised, 'snow')!.object.body);
    expect(snowAfter).not.toEqual(snowBefore);
  });
});

describe('document edits', () => {
  it('duplicates next to the original with a fresh id', () => {
    const doc = defaultScene();
    const { doc: next, id } = duplicateObject(doc, 'frailejon-1');
    const layer = next.layers.find((l) => l.id === 'vegetation')!;
    const i = layer.objects.findIndex((o) => o.id === 'frailejon-1');
    expect(layer.objects[i + 1].id).toBe(id);
    expect(new Set(allObjects(next).map((o) => o.id)).size).toBe(allObjects(next).length);
    expect(locate(doc, id)).toBeNull();
  });

  it('refuses to delete a volcano that snow, crater and steam depend on', () => {
    expect(() => deleteObject(defaultScene(), 'volcano')).toThrow(/snow/);
  });

  it('deletes a plain object', () => {
    expect(locate(deleteObject(defaultScene(), 'rock-1'), 'rock-1')).toBeNull();
  });

  it('moves a layer one step in the draw order', () => {
    const next = shiftLayer(defaultScene(), 'sun', 1);
    expect(next.layers.slice(0, 3).map((l) => l.id)).toEqual(['sky', 'distantClouds', 'sun']);
  });
});

describe('import boundary', () => {
  it('rejects other versions and missing layers', () => {
    expect(parseScene({ ...defaultScene(), version: 1 })).toEqual({
      error: `version 1 (expected ${SCENE_VERSION})`,
    });
    const doc = defaultScene();
    expect(
      parseScene({
        ...doc,
        layers: doc.layers.filter((l) => l.id !== 'crater'),
      }),
    ).toEqual({ error: 'missing layers crater' });
  });
});

describe('transformMatrix', () => {
  it('puts the anchor at (x, y) after rotation and scale', () => {
    const m = transformMatrix({
      x: 100,
      y: 50,
      scaleX: 2,
      scaleY: 3,
      rotation: 30,
      anchorX: 10,
      anchorY: -5,
      opacity: 1,
    });
    const [a, b, c, d, e, f] = m.slice(7, -1).split(' ').map(Number);
    expect(a * 10 + c * -5 + e).toBeCloseTo(100, 1);
    expect(b * 10 + d * -5 + f).toBeCloseTo(50, 1);
  });
});

describe('timeline', () => {
  const doc = defaultScene();
  const cameraX = doc.timeline.tracks.find((t) => t.target === 'camera.x')!;

  it('has one copy per screen and keys on every screen', () => {
    for (const labels of Object.values(LOCALES)) {
      expect(labels.onboarding.screens).toHaveLength(ONBOARDING_SCREENS);
    }
    for (const t of doc.timeline.tracks) expect(t.keys.map((k) => k.at)).toEqual([0, 1, 2]);
  });

  it('evaluates each screen to its key and interpolates between them', () => {
    for (const k of cameraX.keys) expect(evaluateTracks(doc, k.at).camera.x).toBe(k.value);
    const mid = evaluateTracks(doc, 0.5).camera.x;
    expect(mid).toBeCloseTo(
      ((cameraX.keys[0].value as number) + (cameraX.keys[1].value as number)) / 2,
      5,
    );
  });

  it('interpolates colors channel by channel', () => {
    const track = {
      target: 'palette.snow',
      easing: 'linear' as const,
      keys: [
        { at: 0, value: '#000000' },
        { at: 1, value: '#FF8040' },
      ],
    };
    expect(valueAt(track, 0.5)).toBe('#804020');
  });

  it('keeps an untracked edit at a fractional progress out of the timeline', () => {
    const view = evaluateTracks(doc, 1.3);
    const after = updateObject(view, 'rock-1', (o) => ({
      ...o,
      transform: { ...o.transform, x: 999 },
    }));
    const next = commitEdit(doc, view, after, 1.3);
    expect(locate(next, 'rock-1')!.object.transform.x).toBe(999);
    expect(next.timeline).toEqual(doc.timeline);
    expect(next.camera).toEqual(doc.camera);
  });

  it('turns an edit of a tracked value into one keyframe and keeps the base value', () => {
    const view = evaluateTracks(doc, 1.3);
    const next = commitEdit(doc, view, { ...view, camera: { ...view.camera, x: 123 } }, 1.3);
    const track = next.timeline.tracks.find((t) => t.target === 'camera.x')!;
    expect(track.keys).toEqual([
      ...cameraX.keys.slice(0, 2),
      { at: 1.3, value: 123 },
      cameraX.keys[2],
    ]);
    expect(next.camera).toEqual(doc.camera);
    expect(next.timeline.tracks.filter((t) => t.target !== 'camera.x')).toEqual(
      doc.timeline.tracks.filter((t) => t.target !== 'camera.x'),
    );
    expect(evaluateTracks(next, 1.3).camera.x).toBe(123);
  });

  it('adds and removes a keyframe with the toggle', () => {
    const view = evaluateTracks(doc, 1);
    const keyed = toggleKeyframe(doc, view, 'obj.rock-1.transform.y', 1);
    expect(readTarget(evaluateTracks(keyed, 1), 'obj.rock-1.transform.y')).toBe(
      readTarget(view, 'obj.rock-1.transform.y'),
    );
    expect(keyed.timeline.tracks.at(-1)!.keys.map((k) => k.at)).toEqual([0, 1, 2]);
    const unkeyed = toggleKeyframe(keyed, view, 'obj.rock-1.transform.y', 1);
    expect(unkeyed.timeline.tracks.at(-1)!.keys.map((k) => k.at)).toEqual([0, 2]);
  });

  it('drops the tracks of a deleted object', () => {
    const next = deleteObject(doc, 'mist-flank');
    expect(next.timeline.tracks.some((t) => t.target.startsWith('obj.mist-flank.'))).toBe(false);
  });

  it('moves only the objects that have an idle motion', () => {
    const moved = applyMotions(doc, 3.7);
    const before = allObjects(doc);
    allObjects(moved).forEach((o, i) => {
      if (!before[i].motion) expect(o).toBe(before[i]);
      // Only 'rise' (steam) and 'live' (pet) animate body fields; the rest move the transform.
      else
        expect(o.body).toBe(
          before[i].body.kind === 'steam' || before[i].body.kind === 'pet'
            ? o.body
            : before[i].body,
        );
    });
  });
});

describe('import boundary for animation', () => {
  const doc = defaultScene();
  const withTrack = (patch: object) => ({
    ...doc,
    timeline: {
      ...doc.timeline,
      tracks: [{ ...doc.timeline.tracks[0], ...patch }],
    },
  });

  it('rejects tracks that would crash playback', () => {
    expect(parseScene(withTrack({ keys: [] }))).toEqual({
      error: 'track camera.x has no keys',
    });
    expect(parseScene(withTrack({ easing: 'bounce' }))).toEqual({
      error: 'unknown easing bounce in camera.x',
    });
    expect(parseScene(withTrack({ target: 'obj.x.body.kind' }))).toEqual({
      error: 'bad track target obj.x.body.kind',
    });
  });

  it('rejects a motion with a zero period', () => {
    const bad = updateObject(doc, 'cloud-high', (o) => ({
      ...o,
      motion: { kind: 'drift', amplitude: 3, period: 0, delay: 0 },
    }));
    expect(parseScene(bad)).toEqual({
      error: 'object cloud-high: motion needs finite amplitude/delay and period > 0',
    });
  });
});

describe('responsive framing', () => {
  const sizes = [
    [390, 844],
    [375, 812],
    [430, 932],
    [360, 800],
    [768, 1024],
    [820, 1180],
    [1024, 1366],
    [1180, 820],
    [2560, 900],
  ];

  it('keeps the ground at the bottom and shows more landscape on wide screens', () => {
    for (const [w, h] of sizes) {
      const vb = sceneViewBox(w, h);
      expect(vb.y + vb.height).toBeCloseTo(SCENE_HEIGHT, 6);
      expect(vb.width / vb.height).toBeCloseTo(w / h, 6);
      expect(vb.width).toBeGreaterThanOrEqual(390);
      expect(vb.width).toBeLessThanOrEqual(MAX_VIEW_WIDTH);
    }
    expect(sceneViewBox(820, 1180).height).toBe(SCENE_HEIGHT);
  });

  it('has mountains and hills that span the whole width on every screen and device', () => {
    const doc = defaultScene();
    for (const [w, h] of sizes) {
      // The scene only fills the area above the onboarding card.
      const vb = sceneViewBox(w, onboardingLayout(w, h, 34).scene);
      for (let p = 0; p < ONBOARDING_SCREENS; p++) {
        const at = evaluateTracks(doc, p);
        for (const layer of at.layers) {
          for (const o of layer.objects) {
            if (o.body.kind !== 'ridge') continue;
            const k = 1 + (at.camera.zoom - 1) * layer.parallax;
            const e = CAMERA_FOCUS.x - k * CAMERA_FOCUS.x - at.camera.x * layer.parallax * k;
            const left = k * (o.transform.x + o.body.points[0].x) + e;
            const right = k * (o.transform.x + o.body.points.at(-1)!.x) + e;
            expect({
              size: `${w}x${h}`,
              p,
              id: o.id,
              covers: left <= vb.x && right >= vb.x + vb.width,
            }).toEqual({ size: `${w}x${h}`, p, id: o.id, covers: true });
          }
        }
      }
    }
  });
});

describe('onboarding layout', () => {
  it('stacks the card under the scene with the cloud edge overlapping it', () => {
    for (const [w, h, inset] of [
      [390, 844, 34],
      [360, 800, 16],
      [820, 1180, 20],
      [1180, 820, 20],
    ]) {
      const { card, scene } = onboardingLayout(w, h, inset);
      expect(card).toBeGreaterThan(300);
      expect(scene + card).toBeGreaterThan(h);
      expect(scene).toBeGreaterThanOrEqual(h / 2);
    }
  });

  it('never lets the card take more than half of a short screen', () => {
    expect(onboardingLayout(320, 560, 0).scene).toBe(280);
  });
});

describe('Pet framing', () => {
  const apply = (matrix: string, p: { x: number; y: number }) => {
    const [a, b, c, d, e, f] = matrix.slice(7, -1).split(/[ ,]+/).map(Number);
    return { x: a * p.x + c * p.y + e, y: b * p.x + d * p.y + f };
  };

  it('places Pet points exactly where the renderer draws them', () => {
    const doc = evaluateTracks(defaultScene(), 2);
    const pet = locate(doc, 'pet')!;
    if (pet.object.body.kind !== 'pet') throw new Error('pet');
    const host = volcanoOf(doc, pet.object.body)!;
    const vent = ventOf(host.body, craterOf(doc, pet.object.body.volcano));
    const t = pet.object.transform;
    const q = { x: 30, y: -80 };
    const local = { x: t.x + vent.x + q.x * t.scaleX, y: t.y + vent.y + q.y * t.scaleY };
    const viaMatrices = apply(
      parallaxMatrix(doc.camera, host.layer.parallax),
      apply(transformMatrix(host.object.transform), local),
    );
    const direct = petPointInScene(doc, 'pet', q)!;
    expect(direct.x).toBeCloseTo(viaMatrices.x, 1);
    expect(direct.y).toBeCloseTo(viaMatrices.y, 1);
  });

  it('keeps the whole Pet visible above the card on every screen and device', () => {
    const doc = defaultScene();
    for (const [w, h] of [
      [390, 844],
      [360, 800],
      [430, 932],
      [768, 1024],
      [820, 1180],
      [1024, 768],
      [1180, 820],
    ]) {
      const layout = onboardingLayout(w, h, 34);
      const vb = sceneViewBox(w, layout.scene);
      // Scene units still visible above the card's cloud edge.
      const bottom = vb.y + (vb.height * (h - layout.card)) / layout.scene;
      for (let p = 0; p < ONBOARDING_SCREENS; p++) {
        const at = evaluateTracks(doc, p);
        // Top of the Pet's drawable area (its vapor billows reach it) and its tail tip, in Pet units.
        const points = [
          { x: 0, y: PET_VIEWBOX.y },
          { x: 0, y: 120 },
        ].map((q) => petPointInScene(at, 'pet', q)!);
        expect({
          size: `${w}x${h}`,
          p,
          headVisible: points[0].y > vb.y,
          tailAboveCard: points[1].y < bottom,
        }).toEqual({ size: `${w}x${h}`, p, headVisible: true, tailAboveCard: true });
      }
    }
  });
});

describe('camera follow', () => {
  const cameras = [
    { x: 0, y: 15, zoom: 1.1 },
    { x: 60, y: -70, zoom: 1.3 },
    { x: 30, y: -250, zoom: 1.6 },
  ];
  const at = (a: { k: number; e: number; f: number }, p: { x: number; y: number }) => ({
    x: a.k * p.x + a.e,
    y: a.k * p.y + a.f,
  });

  it('moves a layer drawn at the resting camera to where the live camera would draw it', () => {
    for (const [w, h] of [
      [390, 700],
      [820, 980],
      [1180, 600],
    ]) {
      const vb = sceneViewBox(w, h);
      const s = w / vb.width;
      const screen = (p: { x: number; y: number }) => ({
        x: s * (p.x - vb.x),
        y: s * (p.y - vb.y),
      });
      for (const baked of cameras)
        for (const live of cameras)
          for (const depth of [0, 0.35, 1.1]) {
            const v = viewTransform(cameraDelta(live, baked, depth), vb, w, h);
            for (const q of [
              { x: -200, y: 100 },
              { x: 300, y: 640 },
            ]) {
              const drawn = screen(at(parallaxAffine(baked, depth), q));
              // React Native and CSS scale around the view center.
              const moved = {
                x: w / 2 + v.translateX + v.scale * (drawn.x - w / 2),
                y: h / 2 + v.translateY + v.scale * (drawn.y - h / 2),
              };
              const want = screen(at(parallaxAffine(live, depth), q));
              expect(moved.x).toBeCloseTo(want.x, 6);
              expect(moved.y).toBeCloseTo(want.y, 6);
            }
          }
    }
  });
});

describe('rack focus', () => {
  const doc = defaultScene();
  const blurAt = (d: SceneDoc, id: string, p: number) =>
    evaluateTracks(d, p).layers.find((l) => l.id === id)!.blur;

  it('moves the focus from the Nevado to the sky, then shows screen 3 all sharp', () => {
    expect(blurAt(doc, 'ruizMascot', 0)).toBe(0);
    expect(blurAt(doc, 'mainVolcano', 0)).toBe(0);
    expect(blurAt(doc, 'distantClouds', 0)).toBeGreaterThan(1);
    expect(blurAt(doc, 'distantClouds', 1)).toBe(0);
    expect(blurAt(doc, 'vegetation', 1)).toBeGreaterThan(blurAt(doc, 'vegetation', 0));
    for (const layer of doc.layers)
      expect({ id: layer.id, blur: blurAt(doc, layer.id, 2) }).toEqual({ id: layer.id, blur: 0 });
  });

  it('keeps the volcano and its parts sharp on every screen', () => {
    // Four layers draw one shape: blurring them costs four GPU passes per frame.
    for (const p of [0, 0.5, 1, 1.5, 2])
      for (const id of ['mainVolcano', 'snowCap', 'crater', 'volcanicSteam'])
        expect({ id, p, blur: blurAt(doc, id, p) }).toEqual({ id, p, blur: 0 });
  });

  it('turns a blur edit in the Lab into a keyframe at the current progress', () => {
    const view = evaluateTracks(doc, 1.5);
    const after = {
      ...view,
      layers: view.layers.map((l) => (l.id === 'farMountains' ? { ...l, blur: 9 } : l)),
    };
    const next = commitEdit(doc, view, after, 1.5);
    expect(blurAt(next, 'farMountains', 1.5)).toBe(9);
    expect(blurAt(next, 'farMountains', 0)).toBe(blurAt(doc, 'farMountains', 0));
    expect(readTarget(next, 'layer.farMountains.blur')).toBe(0);
  });

  it('keeps the doc when a track writes the value it already holds', () => {
    // Memoized layers skip a frame only if an unchanged track leaves their objects as they were.
    expect(writeTarget(doc, 'layer.hills.blur', readTarget(doc, 'layer.hills.blur')!)).toBe(doc);
    const petOf = (d: SceneDoc) => d.layers.find((l) => l.id === 'ruizMascot')!.objects[0];
    const once = evaluateTracks(doc, 0.5);
    expect(petOf(evaluateTracks(once, 0.5))).toBe(petOf(once));
  });

  it('rejects a negative or missing blur at the import boundary', () => {
    const bad = (blur: unknown) => ({
      ...doc,
      layers: doc.layers.map((l) => (l.id === 'hills' ? { ...l, blur } : l)),
    });
    expect(parseScene(bad(-1))).toEqual({ error: 'layer hills: blur must be a number >= 0' });
    expect(parseScene(bad(undefined))).toEqual({
      error: 'layer hills: blur must be a number >= 0',
    });
  });
});
