// Lookups and immutable edits on a SceneDoc. Every Lab action goes through these.
import { applyAffine, applyTransform, craterVent, parallaxAffine } from './geometry';
import type {
  Body,
  Color,
  CraterBody,
  Layer,
  LayerId,
  SceneDoc,
  SceneObject,
  SteamBody,
  UiBody,
  Vec,
  VolcanoBody,
} from './types';

export function resolveColor(palette: Record<string, string>, c: Color): string {
  if (!c.startsWith('$')) return c;
  const hex = palette[c.slice(1)];
  if (hex === undefined) throw new Error(`Unknown palette color ${c}`);
  return hex;
}

export interface Located {
  layer: Layer;
  object: SceneObject;
  index: number;
}

export function locate(doc: SceneDoc, objectId: string): Located | null {
  for (const layer of doc.layers) {
    const index = layer.objects.findIndex((o) => o.id === objectId);
    if (index >= 0) return { layer, object: layer.objects[index], index };
  }
  return null;
}

/** Snow, crater and steam point at a volcano; this is that volcano or null if the link is broken. */
export function volcanoOf(
  doc: SceneDoc,
  body: Body,
): { object: SceneObject; body: VolcanoBody; layer: Layer } | null {
  if (
    body.kind !== 'snowCap' &&
    body.kind !== 'crater' &&
    body.kind !== 'steam' &&
    body.kind !== 'pet'
  )
    return null;
  const hit = locate(doc, body.volcano);
  if (!hit || hit.object.body.kind !== 'volcano') return null;
  return { object: hit.object, body: hit.object.body, layer: hit.layer };
}

/** The crater that belongs to the same volcano as `body`, if any. */
export function craterOf(doc: SceneDoc, volcanoId: string): CraterBody | null {
  for (const layer of doc.layers) {
    for (const o of layer.objects) {
      if (o.body.kind === 'crater' && o.body.volcano === volcanoId) return o.body;
    }
  }
  return null;
}

/** Where a steam plume starts, in volcano-local units: the crater vent, or the summit center. */
export function ventOf(volcano: VolcanoBody, crater: CraterBody | null): Vec {
  return crater ? craterVent(volcano, crater) : { x: volcano.summitOffset, y: -volcano.height };
}

/**
 * Where the Pet draws a point given in its own units (PET_VIEWBOX), in scene units: through its
 * offset from the crater vent, its volcano's transform and the camera parallax of that layer.
 */
export function petPointInScene(doc: SceneDoc, petId: string, q: Vec): Vec | null {
  const at = petPlacement(doc, petId);
  if (!at) return null;
  const t = at.transform;
  return at.toScene({ x: t.x + at.vent.x + q.x * t.scaleX, y: t.y + at.vent.y + q.y * t.scaleY });
}

/** The crater vent the Pet rises from, in scene units. */
export function petVentInScene(doc: SceneDoc, petId: string): Vec | null {
  const at = petPlacement(doc, petId);
  return at && at.toScene(at.vent);
}

function petPlacement(doc: SceneDoc, petId: string) {
  const pet = locate(doc, petId);
  if (!pet || pet.object.body.kind !== 'pet') return null;
  const host = volcanoOf(doc, pet.object.body);
  if (!host) return null;
  const camera = parallaxAffine(doc.camera, host.layer.parallax);
  return {
    transform: pet.object.transform,
    vent: ventOf(host.body, craterOf(doc, pet.object.body.volcano)),
    /** Volcano-local units to scene units. */
    toScene: (p: Vec) => applyAffine(camera, applyTransform(host.object.transform, p)),
  };
}

export function steamOrigin(doc: SceneDoc, body: SteamBody): Vec | null {
  const host = volcanoOf(doc, body);
  return host ? ventOf(host.body, craterOf(doc, body.volcano)) : null;
}

/** Styling of the text layer, or null when the UIOverlay layer is hidden or empty. */
export function uiStyleOf(doc: SceneDoc): UiBody | null {
  const layer = doc.layers.find((l) => l.id === 'uiOverlay');
  const body = layer?.objects[0]?.body;
  if (!layer || !layer.visible || body?.kind !== 'ui') return null;
  return body;
}

function mapLayers(doc: SceneDoc, fn: (layer: Layer) => Layer): SceneDoc {
  return { ...doc, layers: doc.layers.map(fn) };
}

export function updateLayer(
  doc: SceneDoc,
  id: LayerId,
  patch: Partial<Omit<Layer, 'id' | 'objects'>>,
): SceneDoc {
  return mapLayers(doc, (l) => (l.id === id ? { ...l, ...patch } : l));
}

export function updateObject(
  doc: SceneDoc,
  id: string,
  fn: (o: SceneObject) => SceneObject,
): SceneDoc {
  return mapLayers(doc, (l) =>
    l.objects.some((o) => o.id === id)
      ? { ...l, objects: l.objects.map((o) => (o.id === id ? fn(o) : o)) }
      : l,
  );
}

function uniqueId(doc: SceneDoc, base: string): string {
  const taken = new Set(doc.layers.flatMap((l) => l.objects.map((o) => o.id)));
  const stem = base.replace(/-copy\d*$/, '');
  for (let i = 1; ; i++) {
    const id = `${stem}-copy${i}`;
    if (!taken.has(id)) return id;
  }
}

/** Copy placed right after the original, nudged so it is visible. Returns the new doc and id. */
export function duplicateObject(doc: SceneDoc, id: string): { doc: SceneDoc; id: string } {
  const hit = locate(doc, id);
  if (!hit) throw new Error(`No object ${id}`);
  const newId = uniqueId(doc, id);
  const copy: SceneObject = {
    ...(JSON.parse(JSON.stringify(hit.object)) as SceneObject),
    id: newId,
    name: `${hit.object.name} (copia)`,
  };
  copy.transform.x += 14;
  copy.transform.y += 6;
  const objects = [...hit.layer.objects];
  objects.splice(hit.index + 1, 0, copy);
  return {
    doc: mapLayers(doc, (l) => (l.id === hit.layer.id ? { ...l, objects } : l)),
    id: newId,
  };
}

/** Deleting a volcano would orphan its snow, crater and steam, so that is refused. */
export function deleteObject(doc: SceneDoc, id: string): SceneDoc {
  const dependents = doc.layers
    .flatMap((l) => l.objects)
    .filter((o) => volcanoOf(doc, o.body)?.object.id === id);
  if (dependents.length > 0) {
    throw new Error(`${id} is used by ${dependents.map((o) => o.id).join(', ')}`);
  }
  const next = mapLayers(doc, (l) => ({
    ...l,
    objects: l.objects.filter((o) => o.id !== id),
  }));
  // Tracks of a deleted object would linger invisibly in the timeline and in exports.
  return {
    ...next,
    timeline: {
      ...next.timeline,
      tracks: next.timeline.tracks.filter((t) => !t.target.startsWith(`obj.${id}.`)),
    },
  };
}

/** Move an object one step toward the front (+1) or back (-1) within its layer. */
export function shiftObject(doc: SceneDoc, id: string, step: 1 | -1): SceneDoc {
  const hit = locate(doc, id);
  if (!hit) return doc;
  const to = hit.index + step;
  if (to < 0 || to >= hit.layer.objects.length) return doc;
  const objects = [...hit.layer.objects];
  [objects[hit.index], objects[to]] = [objects[to], objects[hit.index]];
  return mapLayers(doc, (l) => (l.id === hit.layer.id ? { ...l, objects } : l));
}

/** Move a layer one step toward the front (+1) or back (-1) in the draw order. */
export function shiftLayer(doc: SceneDoc, id: LayerId, step: 1 | -1): SceneDoc {
  const i = doc.layers.findIndex((l) => l.id === id);
  const to = i + step;
  if (i < 0 || to < 0 || to >= doc.layers.length) return doc;
  const layers = [...doc.layers];
  [layers[i], layers[to]] = [layers[to], layers[i]];
  return { ...doc, layers };
}
