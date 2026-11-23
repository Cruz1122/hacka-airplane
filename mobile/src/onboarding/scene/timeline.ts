// Declarative animation: keyframed tracks over onboarding progress, plus idle motions over time.
// The renderer never animates by itself: it draws applyMotions(evaluateTracks(doc, progress), time).
import { updateLayer, updateObject } from './doc';
import type {
  EasingName,
  Keyframe,
  LayerId,
  Motion,
  MotionKind,
  SceneDoc,
  SceneObject,
  Track,
  Transform,
} from './types';
import { LAYER_IDS, ONBOARDING_SCREENS } from './types';

export const EASINGS: Record<EasingName, (t: number) => number> = {
  linear: (t) => t,
  easeIn: (t) => t * t * t,
  easeOut: (t) => 1 - (1 - t) ** 3,
  easeInOut: (t) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2),
};
export const EASING_NAMES = Object.keys(EASINGS) as EasingName[];
export const MOTION_KINDS: MotionKind[] = ['drift', 'bob', 'sway', 'breathe', 'rise', 'live'];

type Ref =
  | { kind: 'camera'; field: 'x' | 'y' | 'zoom' }
  | { kind: 'layer'; id: LayerId; field: LayerField }
  | { kind: 'transform'; id: string; field: keyof Transform }
  | { kind: 'body'; id: string; field: string }
  | { kind: 'palette'; key: string };

type LayerField = 'opacity' | 'blur';

const TRANSFORM_FIELDS = new Set<string>([
  'x',
  'y',
  'scaleX',
  'scaleY',
  'rotation',
  'anchorX',
  'anchorY',
  'opacity',
]);

export function parseTarget(target: string): Ref | null {
  const p = target.split('.');
  if (p[0] === 'camera' && p.length === 2 && (p[1] === 'x' || p[1] === 'y' || p[1] === 'zoom'))
    return { kind: 'camera', field: p[1] };
  if (
    p[0] === 'layer' &&
    p.length === 3 &&
    (LAYER_IDS as readonly string[]).includes(p[1]) &&
    (p[2] === 'opacity' || p[2] === 'blur')
  )
    return { kind: 'layer', id: p[1] as LayerId, field: p[2] };
  if (p[0] === 'obj' && p.length === 4 && p[2] === 'transform' && TRANSFORM_FIELDS.has(p[3]))
    return { kind: 'transform', id: p[1], field: p[3] as keyof Transform };
  if (p[0] === 'obj' && p.length === 4 && p[2] === 'body' && p[3] !== 'kind' && p[3] !== 'volcano')
    return { kind: 'body', id: p[1], field: p[3] };
  if (p[0] === 'palette' && p.length === 2) return { kind: 'palette', key: p[1] };
  return null;
}

export const targets = {
  camera: (field: 'x' | 'y' | 'zoom') => `camera.${field}`,
  layer: (id: LayerId, field: LayerField = 'opacity') => `layer.${id}.${field}`,
  transform: (id: string, field: keyof Transform) => `obj.${id}.transform.${field}`,
  body: (id: string, field: string) => `obj.${id}.body.${field}`,
  palette: (key: string) => `palette.${key}`,
};

type Value = Keyframe['value'];

function findObject(doc: SceneDoc, id: string): SceneObject | undefined {
  for (const l of doc.layers) {
    const o = l.objects.find((x) => x.id === id);
    if (o) return o;
  }
  return undefined;
}

/** Current value of a target, or undefined when it does not exist or is not a number/string. */
export function readTarget(doc: SceneDoc, target: string): Value | undefined {
  const ref = parseTarget(target);
  let v: unknown;
  if (!ref) return undefined;
  if (ref.kind === 'camera') v = doc.camera[ref.field];
  else if (ref.kind === 'layer') v = doc.layers.find((l) => l.id === ref.id)?.[ref.field];
  else if (ref.kind === 'palette') v = doc.palette[ref.key];
  else if (ref.kind === 'transform') v = findObject(doc, ref.id)?.transform[ref.field];
  else
    v = (findObject(doc, ref.id)?.body as unknown as Record<string, unknown> | undefined)?.[
      ref.field
    ];
  return typeof v === 'number' || typeof v === 'string' ? v : undefined;
}

/** Copy-on-write set; a missing target, or one already at `value`, leaves the doc as is. */
export function writeTarget(doc: SceneDoc, target: string, value: Value): SceneDoc {
  const ref = parseTarget(target);
  // Flat or text tracks (the Pet's emotion, voice, audio) hold one value through most of a
  // transition; keeping the object's identity lets memoized renderers skip it.
  if (!ref || readTarget(doc, target) === value) return doc;
  switch (ref.kind) {
    case 'camera':
      return { ...doc, camera: { ...doc.camera, [ref.field]: value } };
    case 'layer':
      return updateLayer(doc, ref.id, { [ref.field]: Number(value) });
    case 'palette':
      return { ...doc, palette: { ...doc.palette, [ref.key]: String(value) } };
    case 'transform':
      return updateObject(doc, ref.id, (o) => ({
        ...o,
        transform: { ...o.transform, [ref.field]: value },
      }));
    case 'body':
      return updateObject(doc, ref.id, (o) => ({
        ...o,
        body: { ...o.body, [ref.field]: value } as SceneObject['body'],
      }));
  }
}

const HEX = /^#[0-9a-f]{6}$/i;

function mix(a: Value, b: Value, t: number): Value {
  if (typeof a === 'number' && typeof b === 'number') return a + (b - a) * t;
  if (typeof a === 'string' && typeof b === 'string' && HEX.test(a) && HEX.test(b)) {
    const ca = parseInt(a.slice(1), 16);
    const cb = parseInt(b.slice(1), 16);
    const ch = (shift: number) => {
      const x = (ca >> shift) & 255;
      return Math.round(x + (((cb >> shift) & 255) - x) * t);
    };
    return `#${[16, 8, 0]
      .map((s) => ch(s).toString(16).padStart(2, '0'))
      .join('')
      .toUpperCase()}`;
  }
  return t < 0.5 ? a : b;
}

/** Keys must be sorted by `at` and non-empty (parseScene and setKeyframe guarantee it). */
export function valueAt(track: Track, p: number): Value {
  const keys = track.keys;
  if (p <= keys[0].at) return keys[0].value;
  const last = keys[keys.length - 1];
  if (p >= last.at) return last.value;
  let i = 0;
  while (keys[i + 1].at < p) i++;
  const a = keys[i];
  const b = keys[i + 1];
  return mix(a.value, b.value, EASINGS[track.easing]((p - a.at) / (b.at - a.at)));
}

/** The doc at onboarding progress p (0 = first screen, ONBOARDING_SCREENS - 1 = last). */
export function evaluateTracks(doc: SceneDoc, p: number): SceneDoc {
  let out = doc;
  for (const track of doc.timeline.tracks) out = writeTarget(out, track.target, valueAt(track, p));
  return out;
}

function applyMotion(o: SceneObject, m: Motion, time: number): SceneObject {
  const wave = Math.sin((2 * Math.PI * (time - m.delay)) / m.period);
  const t = o.transform;
  switch (m.kind) {
    case 'drift':
      return { ...o, transform: { ...t, x: t.x + m.amplitude * wave } };
    case 'bob':
      return { ...o, transform: { ...t, y: t.y + m.amplitude * wave } };
    case 'sway':
      return {
        ...o,
        transform: { ...t, rotation: t.rotation + m.amplitude * wave },
      };
    case 'breathe':
      return {
        ...o,
        transform: {
          ...t,
          opacity: t.opacity * (1 - m.amplitude * (0.5 + 0.5 * wave)),
        },
      };
    case 'rise':
      if (o.body.kind !== 'steam') return o;
      return {
        ...o,
        body: {
          ...o.body,
          phase: ((((time - m.delay) / m.period) % 1) + 1) % 1,
        },
      };
    case 'live':
      // The pet runs its own procedural animation; period 1 = real time, 2 = half speed.
      if (o.body.kind !== 'pet') return o;
      return { ...o, body: { ...o.body, clock: (time - m.delay) / m.period } };
  }
}

// A transition rebuilds the doc every frame while the idle clock ticks slower; reusing the
// moved objects for the same clock keeps their identity, so memoized renderers skip them.
const moved = new WeakMap<SceneObject[], { time: number; objects: SceneObject[] }>();

/**
 * Idle loops at `time` seconds. Only objects with a motion get new references, so memoized
 * renderers keep every static body (and its geometry) untouched between frames.
 */
export function applyMotions(doc: SceneDoc, time: number): SceneDoc {
  return {
    ...doc,
    layers: doc.layers.map((l) => {
      if (!l.objects.some((o) => o.motion)) return l;
      let hit = moved.get(l.objects);
      if (hit?.time !== time) {
        hit = {
          time,
          objects: l.objects.map((o) => (o.motion ? applyMotion(o, o.motion, time) : o)),
        };
        moved.set(l.objects, hit);
      }
      return { ...l, objects: hit.objects };
    }),
  };
}

const SAME_KEY = 0.005;

/** Insert or replace the key at progress `at`. A new track starts with the base value on every screen. */
export function setKeyframe(doc: SceneDoc, target: string, value: Value, at: number): SceneDoc {
  const tracks = doc.timeline.tracks;
  const existing = tracks.find((t) => t.target === target);
  let track = existing;
  if (!track) {
    const base = readTarget(doc, target);
    if (base === undefined) throw new Error(`${target} cannot be keyframed`);
    track = {
      target,
      easing: 'linear',
      keys: Array.from({ length: ONBOARDING_SCREENS }, (_, i) => ({
        at: i,
        value: base,
      })),
    };
  }
  const keys = track.keys.filter((k) => Math.abs(k.at - at) > SAME_KEY);
  keys.push({ at: Math.round(at * 1000) / 1000, value });
  keys.sort((a, b) => a.at - b.at);
  const next = { ...track, keys };
  return {
    ...doc,
    timeline: {
      ...doc.timeline,
      tracks: existing ? tracks.map((t) => (t === existing ? next : t)) : [...tracks, next],
    },
  };
}

/** Remove one key; a track loses itself with its last key and the base value shows again. */
export function deleteKeyframe(doc: SceneDoc, target: string, at: number): SceneDoc {
  const tracks = doc.timeline.tracks
    .map((t) =>
      t.target === target
        ? { ...t, keys: t.keys.filter((k) => Math.abs(k.at - at) > SAME_KEY) }
        : t,
    )
    .filter((t) => t.keys.length > 0);
  return { ...doc, timeline: { ...doc.timeline, tracks } };
}

export function keyAt(doc: SceneDoc, target: string, at: number): Keyframe | undefined {
  return doc.timeline.tracks
    .find((t) => t.target === target)
    ?.keys.find((k) => Math.abs(k.at - at) <= SAME_KEY);
}

export function isTracked(doc: SceneDoc, target: string): boolean {
  return doc.timeline.tracks.some((t) => t.target === target);
}

/**
 * Turn an edit of the evaluated view back into a base-doc change. Editors read and write the view
 * (base + tracks at `progress`); a tracked value they changed becomes a keyframe at `progress`,
 * tracked values they did not change are restored from the base, everything else is a base edit.
 */
export function commitEdit(
  base: SceneDoc,
  before: SceneDoc,
  after: SceneDoc,
  progress: number,
): SceneDoc {
  let next = after;
  for (const track of after.timeline.tracks) {
    const was = readTarget(before, track.target);
    const now = readTarget(after, track.target);
    const original = readTarget(base, track.target);
    if (original !== undefined) next = writeTarget(next, track.target, original);
    if (now !== undefined && now !== was) next = setKeyframe(next, track.target, now, progress);
  }
  return next;
}

/** Add a keyframe at `at` holding the current value from `view`, or remove the key already there. */
export function toggleKeyframe(
  base: SceneDoc,
  view: SceneDoc,
  target: string,
  at: number,
): SceneDoc {
  if (keyAt(base, target, at)) return deleteKeyframe(base, target, at);
  const value = readTarget(view, target);
  if (value === undefined) throw new Error(`${target} has no value to keyframe`);
  return setKeyframe(base, target, value, at);
}
