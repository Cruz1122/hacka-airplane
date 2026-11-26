// Editor metadata per object kind: which body fields the inspector shows and which on-canvas
// handles exist. One table drives both, so a new kind is one entry here.
import { steamOrigin, volcanoOf } from '@/onboarding/scene/doc';
import { frailejonShape, ridgePoints, steamTip } from '@/onboarding/scene/geometry';
import type { Body, BodyOf, Kind, SceneDoc, Vec } from '@/onboarding/scene/types';
import { PET_EMOTIONS, VOICE_STATES } from '@/ui/pet/petCore';

export type ParamSpec<F extends string = string> =
  | {
      key: F;
      label: string;
      type: 'number';
      min: number;
      max: number;
      step: number;
    }
  | { key: F; label: string; type: 'int'; min: number; max: number }
  | { key: F; label: string; type: 'color' }
  | { key: F; label: string; type: 'select'; options: readonly string[] };

type FieldsOf<K extends Kind> = Exclude<keyof BodyOf<K>, 'kind'> & string;

const num = <F extends string>(
  key: F,
  label: string,
  min: number,
  max: number,
  step = 1,
): ParamSpec<F> => ({ key, label, type: 'number', min, max, step });
const int = <F extends string>(key: F, label: string, min: number, max: number): ParamSpec<F> => ({
  key,
  label,
  type: 'int',
  min,
  max,
});
const col = <F extends string>(key: F, label: string): ParamSpec<F> => ({
  key,
  label,
  type: 'color',
});

export const PARAMS: { [K in Kind]: ParamSpec<FieldsOf<K>>[] } = {
  sky: [
    col('top', 'Cielo arriba'),
    col('middle', 'Cielo medio'),
    col('bottom', 'Horizonte'),
    num('middleStop', 'Posición del medio', 0.05, 0.95, 0.01),
    num('horizon', 'Altura del horizonte', 200, 844),
  ],
  sun: [
    num('radius', 'Radio', 4, 120),
    num('haloRadius', 'Radio del halo', 0, 500),
    num('haloStrength', 'Intensidad del halo', 0, 1, 0.01),
    col('core', 'Núcleo'),
    col('halo', 'Halo'),
  ],
  cloud: [
    num('width', 'Ancho', 20, 500),
    num('height', 'Alto', 10, 200),
    int('puffs', 'Cúmulos', 2, 16),
    num('flatness', 'Base plana', 0, 1, 0.01),
    int('seed', 'Variación', 1, 999),
    col('fill', 'Luz'),
    col('shade', 'Sombra'),
  ],
  ridge: [
    num('heightScale', 'Altura de cimas', 0.2, 2.5, 0.01),
    num('roundness', 'Curvatura de pendientes', 0, 1.5, 0.01),
    num('roughness', 'Rugosidad', 0, 2, 0.01),
    num('detail', 'Tamaño del detalle', 4, 120),
    int('seed', 'Variación', 1, 999),
    num('depth', 'Profundidad de relleno', 40, 600),
    num('shadeAmount', 'Sombra', 0, 1, 0.01),
    num('grass', 'Pasto (por 100 u)', 0, 60, 0.5),
    col('top', 'Color arriba'),
    col('bottom', 'Color abajo'),
    col('shade', 'Color sombra'),
    col('grassColor', 'Color del pasto'),
  ],
  volcano: [
    num('height', 'Altura de la cumbre', 60, 600),
    num('baseWidth', 'Anchura de base', 200, 1400),
    num('summitWidth', 'Anchura de cumbre', 30, 400),
    num('summitOffset', 'Posición de la cima', -200, 200),
    num('concavity', 'Curvatura de pendientes', 0, 1, 0.01),
    num('roughness', 'Rugosidad', 0, 2, 0.01),
    int('seed', 'Variación', 1, 999),
    num('depth', 'Profundidad de relleno', 40, 600),
    int('gullies', 'Cañadas', 0, 40),
    col('fill', 'Roca'),
    col('ash', 'Ceniza (cumbre)'),
    col('shade', 'Cara en sombra'),
    col('gully', 'Cañadas'),
    col('haze', 'Bruma en la base'),
  ],
  snowCap: [
    num('coverage', 'Contorno de nieve (cobertura)', 0.08, 1, 0.01),
    int('tongues', 'Lenguas de glaciar', 0, 30),
    num('tongueLength', 'Largo de lenguas', 0, 140),
    num('roughness', 'Irregularidad del borde', 0, 2, 0.01),
    int('patches', 'Neveros sueltos', 0, 120),
    int('seed', 'Variación', 1, 999),
    col('snow', 'Nieve'),
    col('ice', 'Hielo en sombra'),
  ],
  crater: [
    num('width', 'Ancho (fracción de cumbre)', 0.1, 1, 0.01),
    num('depth', 'Profundidad', 0, 40, 0.5),
    col('inner', 'Interior'),
    col('rim', 'Borde'),
  ],
  steam: [
    num('height', 'Altura', 30, 500),
    num('width', 'Anchura', 10, 300),
    num('direction', 'Dirección (°)', -70, 70),
    num('curvature', 'Curvatura', -1.5, 1.5, 0.01),
    num('volume', 'Volumen', 0.3, 2, 0.01),
    int('filaments', 'Filamentos', 1, 6),
    num('spread', 'Dispersión', 0, 1.5, 0.01),
    num('oscillation', 'Ondulación', 0, 1, 0.01),
    num('phase', 'Fase (la anima "rise")', 0, 1, 0.01),
    col('fill', 'Vapor'),
    col('shade', 'Sombra'),
  ],
  frailejon: [
    num('trunkHeight', 'Altura de tronco', 4, 200),
    num('trunkWidth', 'Grosor de tronco', 3, 50),
    num('rosetteDiameter', 'Diámetro de roseta', 8, 120),
    int('leafCount', 'Cantidad de hojas', 3, 80),
    num('leafLength', 'Longitud de hojas', 4, 60),
    num('tilt', 'Inclinación (°)', -40, 40),
    int('flowers', 'Flores', 0, 6),
    int('seed', 'Variación', 1, 999),
    col('trunk', 'Tronco'),
    col('trunkShade', 'Hojas secas'),
    col('leaf', 'Hojas'),
    col('leafLight', 'Hojas claras'),
    col('flower', 'Flores'),
  ],
  flower: [
    num('stemHeight', 'Tallo', 0, 40),
    int('petals', 'Pétalos', 3, 12),
    num('petalSize', 'Tamaño de pétalo', 1, 16, 0.1),
    col('petal', 'Pétalos'),
    col('center', 'Centro'),
    col('stem', 'Tallo'),
  ],
  lupine: [
    num('height', 'Altura', 8, 160),
    num('width', 'Ancho de espiga', 3, 60, 0.5),
    int('florets', 'Flores', 3, 40),
    col('color', 'Flores (base)'),
    col('colorLight', 'Flores (punta)'),
    col('leaf', 'Hojas'),
    int('seed', 'Semilla', 1, 999),
  ],
  rock: [
    num('width', 'Ancho', 4, 160),
    num('height', 'Alto', 2, 120),
    int('seed', 'Variación', 1, 999),
    col('fill', 'Relleno'),
    col('shade', 'Sombra'),
    col('light', 'Luz'),
  ],
  tuft: [
    int('blades', 'Hojas', 2, 60),
    num('height', 'Altura', 4, 80),
    num('width', 'Apertura', 2, 80),
    int('seed', 'Variación', 1, 999),
    col('fill', 'Color'),
    col('shade', 'Sombra'),
  ],
  mist: [
    num('width', 'Ancho', 40, 2400),
    num('height', 'Altura', 6, 300),
    int('density', 'Densidad', 1, 30),
    num('diffusion', 'Difusión', 0, 1, 0.01),
    int('seed', 'Variación', 1, 999),
    col('fill', 'Color'),
  ],
  pet: [
    { key: 'emotion', label: 'Emoción', type: 'select', options: PET_EMOTIONS },
    { key: 'voice', label: 'Voz', type: 'select', options: VOICE_STATES },
    num('audio', 'Nivel de audio', 0, 1, 0.01),
    num('clock', 'Reloj (lo anima "live")', 0, 600, 0.1),
    col('fill', 'Vapor'),
    col('shade', 'Sombra del vapor'),
  ],
  // The card's look lives in the design tokens; the scene only toggles it.
  ui: [],
};

export function paramsOf(body: Body): ParamSpec[] {
  return PARAMS[body.kind] as ParamSpec[];
}

// ---------------------------------------------------------------- handles

/** A draggable point in object-local coordinates that edits the body. */
export interface Handle {
  key: string;
  label: string;
  at: Vec;
  set: (p: Vec) => Body;
}

const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));
const degOf = (rad: number) => (rad * 180) / Math.PI;

type HandleFactory<K extends Kind> = (b: BodyOf<K>, doc: SceneDoc) => Handle[];

const HANDLES: { [K in Kind]?: HandleFactory<K> } = {
  volcano: (b) => [
    {
      key: 'summit',
      label: 'Cumbre',
      at: { x: b.summitOffset, y: -b.height },
      set: (p) => ({
        ...b,
        height: clamp(-p.y, 60, 600),
        summitOffset: clamp(p.x, -200, 200),
      }),
    },
    {
      key: 'summitEdge',
      label: 'Ancho de cumbre',
      at: { x: b.summitOffset + b.summitWidth / 2, y: -b.height * 0.93 },
      set: (p) => ({
        ...b,
        summitWidth: clamp(2 * (p.x - b.summitOffset), 30, 400),
      }),
    },
    {
      key: 'base',
      label: 'Base',
      at: { x: b.baseWidth / 2, y: 0 },
      set: (p) => ({ ...b, baseWidth: clamp(2 * Math.abs(p.x), 200, 1400) }),
    },
  ],
  ridge: (b) =>
    ridgePoints(b).map((pt, i) => ({
      key: `p${i}`,
      label: `Punto ${i + 1}`,
      at: pt,
      set: (p) => ({
        ...b,
        points: b.points.map((q, j) =>
          j === i ? { x: Math.round(p.x), y: Math.round(p.y / b.heightScale) } : q,
        ),
      }),
    })),
  frailejon: (b) => {
    const crown = frailejonShape(b).crown;
    return [
      {
        key: 'top',
        label: 'Altura y inclinación',
        at: crown,
        set: (p) => ({
          ...b,
          trunkHeight: clamp(Math.hypot(p.x, p.y), 4, 200),
          tilt: clamp(degOf(Math.atan2(p.x, -p.y)), -40, 40),
        }),
      },
      {
        key: 'rosette',
        label: 'Roseta',
        at: { x: crown.x + b.rosetteDiameter / 2, y: crown.y },
        set: (p) => ({
          ...b,
          rosetteDiameter: clamp(2 * (p.x - crown.x), 8, 120),
        }),
      },
      {
        key: 'leaf',
        label: 'Largo de hojas',
        at: { x: crown.x, y: crown.y - b.leafLength },
        set: (p) => ({ ...b, leafLength: clamp(crown.y - p.y, 4, 60) }),
      },
    ];
  },
  steam: (b, doc) => {
    const o = steamOrigin(doc, b);
    if (!o) return [];
    const tip = steamTip(b);
    return [
      {
        key: 'tip',
        label: 'Altura y dirección',
        at: { x: o.x + tip.x, y: o.y + tip.y },
        set: (p) => ({
          ...b,
          height: clamp(Math.hypot(p.x - o.x, p.y - o.y), 30, 500),
          direction: clamp(degOf(Math.atan2(p.x - o.x, -(p.y - o.y))), -70, 70),
        }),
      },
      {
        key: 'width',
        label: 'Anchura',
        at: { x: o.x + tip.x + b.width / 2, y: o.y + tip.y },
        set: (p) => ({ ...b, width: clamp(2 * (p.x - o.x - tip.x), 10, 300) }),
      },
    ];
  },
  snowCap: (b, doc) => {
    const host = volcanoOf(doc, b);
    if (!host) return [];
    const v = host.body;
    const lineY = -v.height * (1 - b.coverage);
    return [
      {
        key: 'line',
        label: 'Línea de nieve',
        at: { x: v.summitOffset - v.summitWidth, y: lineY },
        set: (p) => ({ ...b, coverage: clamp(1 + p.y / v.height, 0.08, 1) }),
      },
      {
        key: 'tongue',
        label: 'Lenguas',
        at: { x: v.summitOffset, y: lineY + b.tongueLength },
        set: (p) => ({ ...b, tongueLength: clamp(p.y - lineY, 0, 140) }),
      },
    ];
  },
  crater: (b, doc) => {
    const host = volcanoOf(doc, b);
    if (!host) return [];
    const v = host.body;
    return [
      {
        key: 'width',
        label: 'Ancho',
        at: { x: v.summitOffset + (v.summitWidth * b.width) / 2, y: -v.height },
        set: (p) => ({
          ...b,
          width: clamp((2 * (p.x - v.summitOffset)) / v.summitWidth, 0.1, 1),
        }),
      },
    ];
  },
  cloud: (b) => [
    {
      key: 'width',
      label: 'Ancho',
      at: { x: b.width / 2, y: -b.height * 0.2 },
      set: (p) => ({ ...b, width: clamp(2 * Math.abs(p.x), 20, 500) }),
    },
    {
      key: 'height',
      label: 'Alto',
      at: { x: 0, y: -b.height },
      set: (p) => ({ ...b, height: clamp(-p.y, 10, 200) }),
    },
  ],
  mist: (b) => [
    {
      key: 'width',
      label: 'Ancho',
      at: { x: b.width / 2, y: 0 },
      set: (p) => ({ ...b, width: clamp(2 * Math.abs(p.x), 40, 2400) }),
    },
    {
      key: 'height',
      label: 'Altura',
      at: { x: 0, y: -b.height / 2 },
      set: (p) => ({ ...b, height: clamp(-2 * p.y, 6, 300) }),
    },
  ],
  sun: (b) => [
    {
      key: 'radius',
      label: 'Radio',
      at: { x: b.radius, y: 0 },
      set: (p) => ({ ...b, radius: clamp(Math.hypot(p.x, p.y), 4, 120) }),
    },
    {
      key: 'halo',
      label: 'Halo',
      at: { x: 0, y: -b.haloRadius },
      set: (p) => ({ ...b, haloRadius: clamp(Math.hypot(p.x, p.y), 0, 500) }),
    },
  ],
  rock: (b) => [
    {
      key: 'size',
      label: 'Tamaño',
      at: { x: b.width / 2, y: -b.height },
      set: (p) => ({
        ...b,
        width: clamp(2 * Math.abs(p.x), 4, 160),
        height: clamp(-p.y, 2, 120),
      }),
    },
  ],
  tuft: (b) => [
    {
      key: 'height',
      label: 'Altura',
      at: { x: 0, y: -b.height },
      set: (p) => ({ ...b, height: clamp(-p.y, 4, 80) }),
    },
  ],
  flower: (b) => [
    {
      key: 'stem',
      label: 'Tallo',
      at: { x: 0, y: -b.stemHeight },
      set: (p) => ({ ...b, stemHeight: clamp(-p.y, 0, 40) }),
    },
  ],
  sky: (b) => [
    {
      key: 'horizon',
      label: 'Horizonte',
      at: { x: 195, y: b.horizon },
      set: (p) => ({ ...b, horizon: clamp(p.y, 200, 844) }),
    },
    {
      key: 'middle',
      label: 'Color medio',
      at: { x: 195, y: b.horizon * b.middleStop },
      set: (p) => ({ ...b, middleStop: clamp(p.y / b.horizon, 0.05, 0.95) }),
    },
  ],
};

export function handlesOf(body: Body, doc: SceneDoc): Handle[] {
  const factory = HANDLES[body.kind] as HandleFactory<Kind> | undefined;
  return factory ? factory(body as never, doc) : [];
}
