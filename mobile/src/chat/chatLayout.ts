// Chat screen split: the Nevado on top, the vapor sheet with the conversation below, and the
// Pet's circle on the sheet's edge. The header is the onboarding's last scene frame, drawn larger
// and moved so the crater's spot sits centered over the circle (the chat hides the volcano itself,
// so this frames the ranges behind it).
import { onboardingLayout } from '@/onboarding/layout';
import { petVentInScene } from '@/onboarding/scene/doc';
import { sceneViewBox } from '@/onboarding/scene/geometry';
import type { SceneDoc } from '@/onboarding/scene/types';
import { VAPOR_BODY_TOP } from '@/ui/CloudCard';

export const PET_CIRCLE_RADIUS = 50;
/** Room between the crater's spot and the top of the circle, so the ranges show above it. */
const CRATER_GAP = 40;
/** The header shows the volcano closer than the onboarding does, as in the chat mock. */
const SCENE_ZOOM = 1.3;

export interface ChatLayout {
  /** The onboarding scene box (width x sceneHeight). */
  sceneHeight: number;
  /**
   * Moves and zooms that box (about its center, as view transforms do) so the crater's spot sits
   * centered just above the circle: screen = center + offset + scale * (point - center).
   */
  scene: { x: number; y: number; scale: number };
  /**
   * The same placement as a box drawn at the zoomed size (how the chat draws it, crisp), where
   * the handoff animates `scene` as a view transform of the onboarding's box.
   */
  sceneRect: { left: number; top: number; width: number; height: number };
  /** Top of the sheet's vapor edge. */
  sheetTop: number;
  circle: { x: number; y: number; r: number };
  /** Where the conversation starts, under the circle. */
  listTop: number;
  /**
   * How far the vapor sheet, the circle and the conversation rise while the keyboard is open: the
   * mist covers the ranges and the circle stops just under the status bar, giving the messages
   * the room the keyboard takes.
   */
  keyboardLift: number;
}

/** Room left between the status bar and the circle's top while the keyboard is open. */
const LIFTED_GAP = 12;

export function chatLayout(
  doc: SceneDoc,
  width: number,
  height: number,
  insets: { top: number; bottom: number },
): ChatLayout {
  const sceneHeight = onboardingLayout(width, height, insets.bottom).scene;
  // From the width, never the height: the keyboard must not move the header.
  const sheetTop = insets.top + Math.min(240, Math.max(170, width * 0.5));
  const r = PET_CIRCLE_RADIUS;
  const circle = { x: width / 2, y: sheetTop + VAPOR_BODY_TOP, r };
  const vb = sceneViewBox(width, sceneHeight);
  const toBox = sceneHeight / vb.height;
  const vent = petVentInScene(doc, 'pet') ?? { x: vb.x + vb.width / 2, y: vb.y };
  const v = { x: (vent.x - vb.x) * toBox, y: (vent.y - vb.y) * toBox };
  const c = { x: width / 2, y: sceneHeight / 2 };
  const k = SCENE_ZOOM;
  const scene = {
    x: circle.x - c.x - k * (v.x - c.x),
    y: circle.y - r - CRATER_GAP - c.y - k * (v.y - c.y),
    scale: k,
  };
  return {
    sceneHeight,
    scene,
    sceneRect: {
      left: c.x * (1 - k) + scene.x,
      top: c.y * (1 - k) + scene.y,
      width: width * k,
      height: sceneHeight * k,
    },
    sheetTop,
    circle,
    listTop: circle.y + r + 12,
    keyboardLift: Math.max(0, circle.y - r - insets.top - LIFTED_GAP),
  };
}
