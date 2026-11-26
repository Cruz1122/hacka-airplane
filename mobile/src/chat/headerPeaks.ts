// The three nevados the chat header shows behind the Pet's circle, as plain scene objects drawn by
// the onboarding renderer (volcano + snowCap bodies). A stylized reading of the range, not a map:
// Ruiz wide and truncated, Santa Isabel long, low and glaciated, Tolima a sharp distant cone.
// Positions are layer units, tuned against chatLayout's crop: Ruiz and Santa Isabel stand above
// the sheet on every screen, Tolima from 390 pt wide (a narrower phone crops it off the right).
import { IDENTITY } from '@/onboarding/scene/preset';
import type {
  LayerId,
  RidgeBody,
  SceneDoc,
  SceneObject,
  SnowCapBody,
  Transform,
  VolcanoBody,
} from '@/onboarding/scene/types';

type PeakShape = Pick<
  VolcanoBody,
  | 'height'
  | 'baseWidth'
  | 'summitWidth'
  | 'summitOffset'
  | 'concavity'
  | 'roughness'
  | 'seed'
  | 'gullies'
>;
type PeakSnow = Pick<
  SnowCapBody,
  'coverage' | 'tongues' | 'tongueLength' | 'roughness' | 'patches' | 'seed'
>;

interface Peak {
  id: string;
  name: string;
  layer: LayerId;
  /** Base center in layer units; a tilt or stretch is part of a peak's profile. */
  at: Partial<Transform> & Pick<Transform, 'x' | 'y'>;
  shape: PeakShape;
  snow: PeakSnow;
  /** Rock colors: distant peaks take the range's haze colors. */
  fill: string;
  ash: string;
  shade: string;
}

/** Back to front within each layer; each peak draws over the ridge already in its layer. */
export const HEADER_PEAKS: Peak[] = [
  {
    id: 'peak-tolima',
    name: 'Nevado del Tolima',
    layer: 'farMountains',
    // Base below the sheet's edge on every screen: its foot would show as a pale shelf in the vapor.
    at: { x: 378, y: 532 },
    shape: {
      height: 230,
      baseWidth: 460,
      summitWidth: 24,
      summitOffset: 4,
      concavity: 0.55,
      roughness: 0.5,
      seed: 41,
      gullies: 9,
    },
    snow: {
      coverage: 0.28,
      tongues: 8,
      tongueLength: 22,
      roughness: 0.8,
      patches: 16,
      seed: 43,
    },
    fill: '$farTop',
    ash: '$farShade',
    shade: '$farShade',
  },
  {
    id: 'peak-santa-isabel',
    name: 'Nevado Santa Isabel',
    layer: 'midMountains',
    at: { x: 340, y: 480, rotation: -3, scaleX: 1.2 },
    shape: {
      height: 100,
      baseWidth: 480,
      summitWidth: 170,
      summitOffset: 10,
      concavity: 0.2,
      roughness: 0.9,
      seed: 31,
      gullies: 12,
    },
    snow: {
      coverage: 0.4,
      tongues: 8,
      tongueLength: 22,
      roughness: 1.2,
      patches: 22,
      seed: 33,
    },
    fill: '$midShade',
    ash: '$midTop',
    shade: '$midShade',
  },
  {
    id: 'peak-ruiz',
    name: 'Nevado del Ruiz',
    layer: 'midMountains',
    at: { x: 172, y: 486 },
    shape: {
      height: 146,
      baseWidth: 600,
      summitWidth: 190,
      summitOffset: -6,
      concavity: 0.55,
      roughness: 0.8,
      seed: 21,
      gullies: 15,
    },
    snow: {
      coverage: 0.3,
      tongues: 7,
      tongueLength: 26,
      roughness: 1.2,
      patches: 28,
      seed: 23,
    },
    fill: '$midShade',
    ash: '$rock',
    shade: '$rockShade',
  },
];

/**
 * The far range seen between the peaks: rockier, finer crests and a little lower, so it reads as
 * distant rock instead of a row of smooth humps competing with the summits.
 */
const RANGE_PATCHES: Record<string, Partial<RidgeBody>> = {
  'far-range': {
    roundness: 0.3,
    roughness: 1.3,
    detail: 18,
    heightScale: 0.85,
  },
};

function patchRange(o: SceneObject): SceneObject {
  const patch = RANGE_PATCHES[o.id];
  return patch && o.body.kind === 'ridge' ? { ...o, body: { ...o.body, ...patch } } : o;
}

function peakObjects(p: Peak): SceneObject[] {
  const base = { stroke: '$ravine', strokeWidth: 0, motion: null };
  return [
    {
      ...base,
      id: p.id,
      name: p.name,
      transform: { ...IDENTITY, ...p.at },
      body: {
        kind: 'volcano',
        ...p.shape,
        depth: 300,
        fill: p.fill,
        ash: p.ash,
        shade: p.shade,
        gully: '$ravine',
        haze: '$mist',
      },
    },
    {
      ...base,
      id: `${p.id}-snow`,
      name: `${p.name} (glaciar)`,
      transform: { ...IDENTITY },
      body: {
        kind: 'snowCap',
        volcano: p.id,
        ...p.snow,
        snow: '$snow',
        ice: '$ice',
      },
    },
  ];
}

/** RGB blend of two '#rrggbb' colors, `t` of the way from `a` to `b`. */
function mix(a: string, b: string, t: number): string {
  const [ca, cb] = [a, b].map((c) => parseInt(c.slice(1), 16));
  const channel = (shift: number) => {
    const x = (ca >> shift) & 255;
    return Math.round(x + (((cb >> shift) & 255) - x) * t);
  };
  return `#${[16, 8, 0].map((s) => channel(s).toString(16).padStart(2, '0')).join('')}`;
}

/**
 * The chat's ranges in natural earth instead of the onboarding's blue-violet: the scene's own
 * trunk brown greyed with its stone, washed toward the golden horizon the farther a range is.
 * Only rock keys change; sky, snow, ice and mist keep the onboarding's colors.
 */
function earthPalette(p: Record<string, string>): Record<string, string> {
  const earth = mix(p.trunk, p.stone, 0.3);
  const earthShade = mix(p.trunkShade, p.stoneShade, 0.3);
  const haze = (c: string, t: number) => mix(c, p.skyHorizon, t);
  return {
    farTop: haze(earth, 0.45),
    farBottom: haze(earth, 0.58),
    farShade: haze(earthShade, 0.4),
    midTop: haze(earth, 0.22),
    midBottom: haze(earth, 0.34),
    midShade: haze(earthShade, 0.18),
    rock: haze(earth, 0.08),
    ash: haze(earth, 0.3),
    rockShade: haze(earthShade, 0.06),
    ravine: earthShade,
  };
}

/**
 * `doc` with the header's ranges patched and repainted in earth tones, and its peaks appended to
 * their layers.
 */
export function withHeaderPeaks(doc: SceneDoc): SceneDoc {
  return {
    ...doc,
    palette: { ...doc.palette, ...earthPalette(doc.palette) },
    layers: doc.layers.map((layer) => {
      const peaks = HEADER_PEAKS.filter((p) => p.layer === layer.id).flatMap(peakObjects);
      const objects = layer.objects.map(patchRange);
      return objects.every((o, i) => o === layer.objects[i]) && peaks.length === 0
        ? layer
        : { ...layer, objects: [...objects, ...peaks] };
    }),
  };
}
