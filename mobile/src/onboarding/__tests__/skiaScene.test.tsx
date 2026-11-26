// The native renderer on real Skia (CanvasKit wasm, loaded in this realm so its typed arrays match).
/* eslint-disable @typescript-eslint/no-require-imports -- CanvasKit has to load before Skia's
   mock and the modules that import it, so they are required after it. */
import { act } from 'react';
import { createRoot } from 'test-renderer';

import type { Mat } from '@/ui/skia/svgTransform';

import type { SceneDoc } from '../scene/types';

jest.mock('@shopify/react-native-skia', () =>
  require('@shopify/react-native-skia/lib/commonjs/mock').Mock(
    (global as unknown as { CanvasKit: unknown }).CanvasKit,
  ),
);
const mockPetFrames = { calls: 0 };
jest.mock('@/ui/pet/petCore', () => {
  const real = jest.requireActual('@/ui/pet/petCore');
  return {
    ...real,
    petFrame: (...a: unknown[]) => {
      mockPetFrames.calls++;
      return real.petFrame(...a);
    },
  };
});

let scene: SceneDoc;
let at: (p: number, time: number) => SceneDoc;

beforeAll(async () => {
  const g = global as unknown as { CanvasKit: unknown };
  g.CanvasKit = await require('canvaskit-wasm/bin/full/canvaskit')({});
  const { Skia } = require('@shopify/react-native-skia');
  // CanvasKit lacks MakeMatrixTransform: the half-resolution blur becomes a plain blur here.
  Skia.ImageFilter.MakeMatrixTransform = (_m: unknown, _f: unknown, _mm: unknown, input: unknown) =>
    input ?? Skia.ImageFilter.MakeOffset(0, 0, null);
  const { defaultScene } = require('../scene/preset');
  const { applyMotions, evaluateTracks } = require('../scene/timeline');
  scene = defaultScene();
  at = (p, time) => applyMotions(evaluateTracks(scene, p), time);
});

it('lays out every object with the matrices the SVG transform strings give', () => {
  const { layoutFrame } = require('../skia/drawScene');
  const { craterOf, ventOf, volcanoOf } = require('../scene/doc');
  const { parallaxMatrix, transformMatrix } = require('../scene/geometry');
  const { multiply, parseTransform } = require('@/ui/skia/svgTransform');
  const plus0 = (m: Mat) => m.map((v) => v + 0);
  for (const p of [0, 0.37, 1, 1.5, 2])
    for (const time of [0, 7.3]) {
      const doc = at(p, time);
      // The string round trip layoutFrame used before.
      const expected: Mat[] = [];
      for (const layer of doc.layers) {
        if (!layer.visible || layer.id === 'uiOverlay') continue;
        for (const o of layer.objects) {
          const host = volcanoOf(doc, o.body);
          let m: Mat = parseTransform(
            parallaxMatrix(doc.camera, host ? host.layer.parallax : layer.parallax),
          );
          if (host) {
            m = multiply(m, parseTransform(transformMatrix(host.object.transform)));
            if (o.body.kind === 'pet') {
              const vent = ventOf(host.body, craterOf(doc, host.object.id));
              m = multiply(m, [1, 0, 0, 1, vent.x, vent.y]);
            }
          }
          expected.push(multiply(m, parseTransform(transformMatrix(o.transform))));
        }
      }
      const frame = layoutFrame(doc, 393, 600);
      const got = frame.layers.flatMap((l: { items: { matrix: Mat }[] }) =>
        l.items.map((it) => it.matrix),
      );
      expect(got.map(plus0)).toEqual(expected.map(plus0));
    }
});

it("draws the Pet's frame once while its pose holds, though tracks rebuild its body", () => {
  const { SceneCanvas } = require('../SceneCanvas.native');
  const root = createRoot();
  const draw = (doc: SceneDoc) =>
    act(() => root.render(<SceneCanvas doc={doc} width={393} height={600} />));
  draw(at(0, 3));
  mockPetFrames.calls = 0;
  // A camera move with the idle clock held, before the emotion track switches.
  for (const p of [0.05, 0.1, 0.15, 0.2]) draw(at(p, 3));
  expect(mockPetFrames.calls).toBe(0);
  draw(at(0.2, 3 + 1 / 30)); // the next idle tick moves the Pet
  expect(mockPetFrames.calls).toBe(1);
  act(() => root.unmount());
});
