// Scene document: the single serializable source for the onboarding, the Lab and SVG export.
//
// Coordinate system (shared by every layer):
// - Scene units = points of the 390 x 844 reference phone. Origin top-left, y grows down.
// - The visible window adapts to the screen (see sceneViewBox): narrower screens keep the 390
//   width and reveal more sky; wider screens (tablets, landscape) keep the 844 height and reveal
//   more landscape on both sides. The ground line always stays at the bottom.
// - Layers draw far outside [0, 390] (bleed to about -620..1010) so wide screens and camera moves
//   never expose gaps.
// - Every object has a local frame. `transform` places the local anchor at (x, y) in its layer,
//   then rotates (degrees) and scales around that anchor.
// - Objects that belong to the volcano (snow, crater, steam, pet) render in the volcano's frame:
//   volcano parallax, then the volcano transform, then their own transform. The pet's frame also
//   starts at the crater vent, so its transform is an offset from the vent.
// - The ruizMascot layer holds the Pet (src/ui/pet), the character designed in its own lab.

import type { PetEmotion, VoiceState } from '@/ui/pet/petCore';

export const SCENE_WIDTH = 390;
export const SCENE_HEIGHT = 844;
/**
 * Bump on any change to the shape of SceneDoc or a Body. The Lab's import boundary rejects other
 * versions, so an old autosave falls back to the preset instead of crashing the renderer.
 */
export const SCENE_VERSION = 5;

/** '#rrggbb' or a palette reference '$key'. */
export type Color = string;

export interface Vec {
  x: number;
  y: number;
}

export interface Transform {
  x: number;
  y: number;
  scaleX: number;
  scaleY: number;
  rotation: number;
  anchorX: number;
  anchorY: number;
  opacity: number;
}

export interface Camera {
  x: number;
  y: number;
  zoom: number;
}

export const LAYER_IDS = [
  'sky',
  'sun',
  'distantClouds',
  'farMountains',
  'midMountains',
  'mainVolcano',
  'snowCap',
  'crater',
  'volcanicSteam',
  'hills',
  'vegetation',
  'foregroundMist',
  'ruizMascot',
  'uiOverlay',
] as const;
export type LayerId = (typeof LAYER_IDS)[number];

export interface SkyBody {
  kind: 'sky';
  top: Color;
  middle: Color;
  bottom: Color;
  middleStop: number;
  /** Scene y where the gradient reaches `bottom`; below it the color holds. */
  horizon: number;
}

export interface SunBody {
  kind: 'sun';
  radius: number;
  core: Color;
  halo: Color;
  haloRadius: number;
  haloStrength: number;
}

/** Cumulus built from shaded puffs. Local origin = base center. */
export interface CloudBody {
  kind: 'cloud';
  width: number;
  height: number;
  puffs: number;
  seed: number;
  /** 0 = round bottom, 1 = flat cumulus base. */
  flatness: number;
  fill: Color;
  shade: Color;
}

/** Skyline through `points` (local, y negative = up from the baseline), filled down to `depth`. */
export interface RidgeBody {
  kind: 'ridge';
  points: Vec[];
  roundness: number;
  heightScale: number;
  /** Fractal jaggedness added between the control points. */
  roughness: number;
  /** Feature size of that jaggedness in scene units. */
  detail: number;
  seed: number;
  depth: number;
  top: Color;
  bottom: Color;
  shade: Color;
  shadeAmount: number;
  /** Grass strokes per 100 units of width (0 = bare rock). */
  grass: number;
  grassColor: Color;
}

/** Local origin = base center. The summit plateau sits at y = -height. */
export interface VolcanoBody {
  kind: 'volcano';
  height: number;
  baseWidth: number;
  summitWidth: number;
  summitOffset: number;
  concavity: number;
  roughness: number;
  seed: number;
  depth: number;
  gullies: number;
  fill: Color;
  ash: Color;
  shade: Color;
  gully: Color;
  /** Atmospheric haze over the lower slopes. */
  haze: Color;
}

export interface SnowCapBody {
  kind: 'snowCap';
  volcano: string;
  coverage: number;
  tongues: number;
  tongueLength: number;
  roughness: number;
  patches: number;
  seed: number;
  snow: Color;
  ice: Color;
}

export interface CraterBody {
  kind: 'crater';
  volcano: string;
  width: number;
  depth: number;
  inner: Color;
  rim: Color;
}

/** Local origin = the vent. `direction` leans the plume (degrees from vertical). */
export interface SteamBody {
  kind: 'steam';
  volcano: string;
  height: number;
  width: number;
  direction: number;
  curvature: number;
  volume: number;
  filaments: number;
  spread: number;
  oscillation: number;
  /** 0..1 position of the rising puffs; animated by a 'rise' motion. */
  phase: number;
  fill: Color;
  shade: Color;
}

/** Local origin = trunk base. */
export interface FrailejonBody {
  kind: 'frailejon';
  trunkHeight: number;
  trunkWidth: number;
  rosetteDiameter: number;
  leafCount: number;
  leafLength: number;
  tilt: number;
  flowers: number;
  seed: number;
  trunk: Color;
  trunkShade: Color;
  leaf: Color;
  leafLight: Color;
  flower: Color;
}

export interface FlowerBody {
  kind: 'flower';
  stemHeight: number;
  petals: number;
  petalSize: number;
  petal: Color;
  center: Color;
  stem: Color;
}

/** Lupine: a spike of florets over a fan of palmate leaves. Local origin = stem base. */
export interface LupineBody {
  kind: 'lupine';
  height: number;
  /** Spike width at its base. */
  width: number;
  florets: number;
  /** Floret color at the bottom of the spike; it fades to colorLight at the tip. */
  color: Color;
  colorLight: Color;
  leaf: Color;
  seed: number;
}

/** Faceted boulder. Local origin = bottom center. */
export interface RockBody {
  kind: 'rock';
  width: number;
  height: number;
  seed: number;
  fill: Color;
  shade: Color;
  light: Color;
}

/** Pajonal tussock. Local origin = base center. */
export interface TuftBody {
  kind: 'tuft';
  blades: number;
  height: number;
  width: number;
  seed: number;
  fill: Color;
  shade: Color;
}

/** Soft horizontal bank of fog built from radial-gradient puffs. Local origin = center. */
export interface MistBody {
  kind: 'mist';
  width: number;
  height: number;
  density: number;
  diffusion: number;
  seed: number;
  fill: Color;
}

/** The Pet rising from the crater; drawn by src/ui/pet with its own fixed character colors. */
export interface PetBody {
  kind: 'pet';
  /** Volcano whose crater vent the pet rises from (like steam). */
  volcano: string;
  emotion: PetEmotion;
  voice: VoiceState;
  /** 0..1, drives the speaking mouth. */
  audio: number;
  /** Seconds of the pet's own animation (mist, tail, blink); written by the 'live' motion. */
  clock: number;
  /** Vapor colors (default: the scene's mist), so the Pet reads as the crater's steam. */
  fill: Color;
  shade: Color;
}

/**
 * Marks the React Native card (text, dots, button) drawn over the scene. Its look comes from the
 * design tokens (src/ui/theme/tokens.ts), not from the scene, so there is one source of truth.
 */
export interface UiBody {
  kind: 'ui';
}

export type Body =
  | SkyBody
  | SunBody
  | CloudBody
  | RidgeBody
  | VolcanoBody
  | SnowCapBody
  | CraterBody
  | SteamBody
  | FrailejonBody
  | FlowerBody
  | LupineBody
  | RockBody
  | TuftBody
  | MistBody
  | PetBody
  | UiBody;

export type Kind = Body['kind'];
export type BodyOf<K extends Kind> = Extract<Body, { kind: K }>;

/** Idle loop driven by wall-clock time (never by the onboarding progress). */
export type MotionKind = 'drift' | 'bob' | 'sway' | 'breathe' | 'rise' | 'live';
export interface Motion {
  kind: MotionKind;
  /** Units: scene units (drift, bob), degrees (sway), opacity fraction (breathe), unused (rise, live). */
  amplitude: number;
  /** Seconds per cycle. */
  period: number;
  /** Seconds of phase offset. */
  delay: number;
}

export interface SceneObject {
  id: string;
  name: string;
  transform: Transform;
  stroke: Color;
  strokeWidth: number;
  motion: Motion | null;
  body: Body;
}

export interface Layer {
  id: LayerId;
  name: string;
  visible: boolean;
  locked: boolean;
  /** 0 = pinned to the sky, 1 = moves with the camera. */
  parallax: number;
  opacity: number;
  /**
   * Out-of-focus blur radius in scene units (0 = sharp). Keyed per screen it makes the focus
   * shift between depths (rack focus); it is a view filter, so it costs no SVG redraw.
   */
  blur: number;
  objects: SceneObject[];
}

export type EasingName = 'linear' | 'easeIn' | 'easeOut' | 'easeInOut';

/** `at` is onboarding progress: 0 = screen 1, 1 = screen 2, 2 = screen 3. */
export interface Keyframe {
  at: number;
  value: number | string;
}

/**
 * One animated property. Target grammar:
 *   camera.x | camera.y | camera.zoom
 *   layer.<layerId>.opacity
 *   obj.<objectId>.transform.<field> | obj.<objectId>.body.<field>
 *   palette.<key>                       (color, interpolated in RGB)
 */
export interface Track {
  target: string;
  easing: EasingName;
  keys: Keyframe[];
}

/** Onboarding screens; progress runs from 0 (first) to ONBOARDING_SCREENS - 1 (last). */
export const ONBOARDING_SCREENS = 3;

export interface Timeline {
  /** Duration of one screen-to-screen transition. */
  transitionMs: number;
  /** Easing of the progress value during a transition. */
  easing: EasingName;
  tracks: Track[];
}

export interface SceneDoc {
  version: typeof SCENE_VERSION;
  palette: Record<string, string>;
  camera: Camera;
  layers: Layer[];
  timeline: Timeline;
}
