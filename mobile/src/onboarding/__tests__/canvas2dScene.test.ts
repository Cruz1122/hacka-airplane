// The web scene renderer (canvas2d/drawScene2d.ts) against the native one (skia/drawScene.ts): the
// same layout, and every body of the shipped scenes painted on a 2D context.
/* eslint-disable @typescript-eslint/no-require-imports -- CanvasKit has to load before Skia's
   mock and the modules that import it, so they are required after it. */
import type { SceneDoc } from "../scene/types";

jest.mock("@shopify/react-native-skia", () =>
  require("@shopify/react-native-skia/lib/commonjs/mock").Mock(
    (global as unknown as { CanvasKit: unknown }).CanvasKit,
  ),
);

let at: (p: number, time: number) => SceneDoc;

beforeAll(async () => {
  const g = global as unknown as { CanvasKit: unknown };
  g.CanvasKit = await require("canvaskit-wasm/bin/full/canvaskit")({});
  const { defaultScene } = require("../scene/preset");
  const { applyMotions, evaluateTracks } = require("../scene/timeline");
  const scene = defaultScene();
  at = (p, time) => applyMotions(evaluateTracks(scene, p), time);
});

it("lays out every object as the native renderer does", () => {
  const native = require("../skia/drawScene");
  const web = require("../canvas2d/drawScene2d");
  for (const p of [0, 0.37, 1, 1.5, 2])
    for (const time of [0, 7.3]) {
      const doc = at(p, time);
      const a = native.layoutFrame(doc, 393, 600);
      const b = web.layoutFrame(doc, 393, 600);
      expect(b.view).toEqual(a.view);
      expect(b.layers.map((l: { id: string }) => l.id)).toEqual(
        a.layers.map((l: { id: string }) => l.id),
      );
      b.layers.forEach(
        (
          layer: { opacity: number; blur: number; items: unknown[] },
          i: number,
        ) => {
          expect(layer.opacity).toBe(a.layers[i].opacity);
          expect(layer.blur).toBe(a.layers[i].blur);
          const items = layer.items as {
            matrix: number[];
            object: { transform: { opacity: number }; body: { kind: string } };
          }[];
          expect(items.map((it) => it.matrix)).toEqual(
            a.layers[i].items.map((it: { matrix: number[] }) => it.matrix),
          );
          expect(items.map((it) => it.object.transform.opacity)).toEqual(
            a.layers[i].items.map((it: { opacity: number }) => it.opacity),
          );
        },
      );
    }
});

/** A 2D context that records what was painted, and the opacity scratch canvases were drawn at. */
function recordingContext() {
  const calls: string[] = [];
  const composites: number[] = [];
  const gradient = { addColorStop: () => {} };
  const ctx: Record<string, unknown> = {
    canvas: { width: 100, height: 100 },
    globalAlpha: 1,
    createLinearGradient: () => gradient,
    createRadialGradient: () => gradient,
    drawImage: () => composites.push(ctx.globalAlpha as number),
  };
  const recorded = new Proxy(ctx, {
    get(target, key: string) {
      if (key in target) return target[key];
      return () => {
        calls.push(key);
      };
    },
    set(target, key: string, value) {
      target[key] = value;
      return true;
    },
  });
  return {
    ctx: recorded as unknown as CanvasRenderingContext2D,
    calls,
    composites,
  };
}

it("paints every layer of the onboarding and chat scenes", () => {
  (global as unknown as { Path2D: unknown }).Path2D = class {
    addPath() {}
    arc() {}
  };
  (global as unknown as { DOMMatrix: unknown }).DOMMatrix = class {};
  const { drawLayer, layoutFrame } = require("../canvas2d/drawScene2d");
  const { headerScene } = require("@/chat/headerScene");
  const { PET_PRESET, petFrame } = require("@/ui/pet/petCore");
  const config = { ...PET_PRESET, emotion: "happy", voice: "idle", audio: 0 };
  const pet = {
    config,
    frame: petFrame(config, {
      time: 1,
      face: PET_PRESET.poses.happy,
      blink: 0,
    }),
    fill: "#ffffff",
    shade: "#a0a0d0",
  };
  for (const doc of [at(0, 0), at(0.5, 3.1), at(2, 9), headerScene]) {
    const frame = layoutFrame(doc, 393, 600);
    for (const layer of frame.layers) {
      const main = recordingContext();
      const scratch = recordingContext();
      drawLayer(main.ctx, scratch.ctx, frame.view, layer, doc.palette, pet);
      const translucent = layer.items
        .map(
          (it: { object: { transform: { opacity: number } } }) =>
            it.object.transform.opacity,
        )
        .filter((o: number) => o > 0 && o < 1);
      // Group opacity: each translucent object is painted apart, then laid down at its opacity.
      expect(main.composites).toEqual(translucent);
      const painted = [...main.calls, ...scratch.calls].filter((c) =>
        ["fill", "stroke", "fillRect"].includes(c),
      );
      if (layer.items.length > 0) expect(painted.length).toBeGreaterThan(0);
    }
  }
});
