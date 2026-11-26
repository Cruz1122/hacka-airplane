// Web scene renderer: one 2D canvas per layer (canvas2d/drawScene2d.ts) in the layer views
// NevadoScene uses, so layer opacity and blur stay the browser's (CSS). The SVG renderer
// re-rendered its React tree on every frame and held the onboarding near 25 fps; here a frame
// repaints only the layers whose objects moved. NevadoScene stays the reference look (Lab, export).
// Native draws with Skia (SceneCanvas.native.tsx).
import { memo, useLayoutEffect, useMemo, useRef } from "react";
import { StyleSheet, View, type ViewStyle } from "react-native";

import {
  blinkAt,
  PET_PRESET,
  petFrame,
  type PetConfig,
} from "@/ui/pet/petCore";
import { useFaceTransition } from "@/ui/pet/useFaceTransition";
import { multiply, type Mat } from "@/ui/skia/svgTransform";
import { useReducedMotion } from "@/ui/useReducedMotion";

import {
  drawLayer,
  layoutFrame,
  type LayerFrame,
  type ScenePet,
} from "./canvas2d/drawScene2d";
import type { NevadoSceneProps } from "./NevadoScene";
import { resolveColor } from "./scene/doc";
import type { PetBody, SceneDoc } from "./scene/types";

function petOf(doc: SceneDoc): PetBody | null {
  for (const l of doc.layers) {
    if (!l.visible) continue;
    for (const o of l.objects) if (o.body.kind === "pet") return o.body;
  }
  return null;
}

const NO_PET: PetBody["emotion"] = "happy";

/** Sharp on dense screens without painting more than 3x the points, like the web Pet. */
const pixelRatio = () =>
  typeof window === "undefined"
    ? 1
    : Math.min(3, Math.max(1, window.devicePixelRatio || 1));

/**
 * Points each layer paints past the scene's edges. The SVG layers draw beyond their box, so their
 * CSS blur reaches into real scene there; cut at the edge, a blurred layer would fade to
 * transparent. The largest rack-focus blur, 3.5 scene units, is about 5 points at phone size.
 */
const BLEED = 16;

// Composited layers, so a blur or opacity change does not repaint the canvas.
const LAYER = { willChange: "transform" } as ViewStyle;

export function SceneCanvas({ doc, width, height }: NevadoSceneProps) {
  const reduced = useReducedMotion();
  const pet = petOf(doc);
  const motion = PET_PRESET.motion;
  // The emotion track steps halfway through a swipe; the face morphs like the Pet component's.
  const face = useFaceTransition(
    PET_PRESET.poses,
    pet?.emotion ?? NO_PET,
    reduced ? 0 : motion.transition,
    motion.easing,
  );
  // Values, not the body: tracks rebuild that body on every frame, but the pose holds still while
  // the camera moves with the idle clock held.
  const emotion = pet?.emotion;
  const voice = pet?.voice;
  const audio = pet?.audio;
  const clock = pet?.clock;
  const fill = pet && resolveColor(doc.palette, pet.fill);
  const shade = pet && resolveColor(doc.palette, pet.shade);
  const scenePet = useMemo((): ScenePet | null => {
    if (
      emotion === undefined ||
      voice === undefined ||
      audio === undefined ||
      clock === undefined ||
      !fill ||
      !shade
    )
      return null;
    const config: PetConfig = { ...PET_PRESET, emotion, voice, audio };
    const frame = petFrame(config, {
      time: clock,
      face,
      blink: blinkAt(clock, motion.blinkInterval),
    });
    return { config, frame, fill, shade };
  }, [emotion, voice, audio, clock, face, fill, shade, motion.blinkInterval]);

  const frame = layoutFrame(doc, width, height);
  const dpr = pixelRatio();
  return (
    <View style={{ width, height, overflow: "hidden" }}>
      {frame.layers.map((layer) => (
        <View
          key={layer.id}
          style={[
            StyleSheet.absoluteFill,
            LAYER,
            { opacity: layer.opacity },
            layer.blur > 0.05 && { filter: `blur(${layer.blur.toFixed(2)}px)` },
          ]}
        >
          <LayerCanvas
            view={frame.view}
            layer={layer}
            palette={doc.palette}
            pet={
              layer.items.some((it) => it.object.body.kind === "pet")
                ? scenePet
                : null
            }
            width={width}
            height={height}
            dpr={dpr}
          />
        </View>
      ))}
    </View>
  );
}

interface LayerCanvasProps {
  view: Mat;
  layer: LayerFrame;
  palette: Record<string, string>;
  pet: ScenePet | null;
  width: number;
  height: number;
  dpr: number;
}

const sameMat = (a: Mat, b: Mat) => a.every((v, i) => v === b[i]);

/** Same pixels: layer opacity and blur live on the view around the canvas. */
function samePaint(a: LayerCanvasProps, b: LayerCanvasProps): boolean {
  if (
    a.width !== b.width ||
    a.height !== b.height ||
    a.dpr !== b.dpr ||
    a.palette !== b.palette ||
    a.pet !== b.pet ||
    !sameMat(a.view, b.view) ||
    a.layer.items.length !== b.layer.items.length
  )
    return false;
  return a.layer.items.every((it, i) => {
    const o = b.layer.items[i];
    return (
      it.object === o.object &&
      it.host === o.host &&
      it.crater === o.crater &&
      sameMat(it.matrix, o.matrix)
    );
  });
}

// One offscreen canvas for objects with group opacity, shared by every layer (they paint in turn).
let scratch: CanvasRenderingContext2D | null = null;
function scratchSized(w: number, h: number) {
  scratch ??= document.createElement("canvas").getContext("2d");
  if (scratch && (scratch.canvas.width !== w || scratch.canvas.height !== h)) {
    scratch.canvas.width = w;
    scratch.canvas.height = h;
  }
  return scratch;
}

const LayerCanvas = memo(function LayerCanvas({
  view,
  layer,
  palette,
  pet,
  width,
  height,
  dpr,
}: LayerCanvasProps) {
  const ref = useRef<HTMLCanvasElement>(null);
  const w = width + 2 * BLEED;
  const h = height + 2 * BLEED;
  const pxW = Math.round(w * dpr);
  const pxH = Math.round(h * dpr);
  // Rendered only when its pixels change (samePaint), so every render repaints.
  useLayoutEffect(() => {
    const ctx = ref.current?.getContext("2d");
    const off = scratchSized(pxW, pxH);
    if (!ctx || !off) return;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, pxW, pxH);
    const sx = pxW / w;
    const sy = pxH / h;
    const toDevice = multiply([sx, 0, 0, sy, BLEED * sx, BLEED * sy], view);
    drawLayer(ctx, off, toDevice, layer, palette, pet);
  });
  return (
    <canvas
      ref={ref}
      width={pxW}
      height={pxH}
      style={{
        position: "absolute",
        left: -BLEED,
        top: -BLEED,
        width: w,
        height: h,
      }}
    />
  );
}, samePaint);
