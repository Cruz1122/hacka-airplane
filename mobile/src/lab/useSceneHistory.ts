// Undo/redo plus local autosave for the Lab. Rapid edits with the same key (a slider drag, a
// canvas drag) coalesce into one undo step.
import { useCallback, useRef, useState } from 'react';

import { defaultScene } from '@/onboarding/scene/preset';
import { EASING_NAMES, MOTION_KINDS, parseTarget } from '@/onboarding/scene/timeline';
import {
  LAYER_IDS,
  SCENE_VERSION,
  type Motion,
  type SceneDoc,
  type Timeline,
} from '@/onboarding/scene/types';

const STORAGE_KEY = 'nevados.onboardingLab.scene';
const COALESCE_MS = 900;
const MAX_UNDO = 200;

const isNum = (v: unknown): v is number => typeof v === 'number' && Number.isFinite(v);

/** Reason the timeline would crash or corrupt playback, or null. */
function timelineError(t: Partial<Timeline> | undefined): string | null {
  if (!t || typeof t !== 'object') return 'missing timeline';
  if (!isNum(t.transitionMs) || t.transitionMs < 1)
    return 'timeline.transitionMs must be a positive number';
  if (!EASING_NAMES.includes(t.easing as never)) return `unknown easing ${String(t.easing)}`;
  if (!Array.isArray(t.tracks)) return 'timeline.tracks must be an array';
  for (const tr of t.tracks) {
    if (typeof tr?.target !== 'string' || !parseTarget(tr.target))
      return `bad track target ${String(tr?.target)}`;
    if (!EASING_NAMES.includes(tr.easing))
      return `unknown easing ${String(tr.easing)} in ${tr.target}`;
    if (!Array.isArray(tr.keys) || tr.keys.length === 0) return `track ${tr.target} has no keys`;
    for (let i = 0; i < tr.keys.length; i++) {
      const k = tr.keys[i];
      if (!isNum(k?.at) || (typeof k.value !== 'number' && typeof k.value !== 'string'))
        return `bad key in ${tr.target}`;
      if (i > 0 && k.at <= tr.keys[i - 1].at) return `keys of ${tr.target} are not sorted`;
    }
  }
  return null;
}

function motionError(m: Partial<Motion> | null | undefined, id: string): string | null {
  if (m === null) return null;
  if (!m || !MOTION_KINDS.includes(m.kind as never)) return `object ${id}: bad motion`;
  if (!isNum(m.amplitude) || !isNum(m.delay) || !isNum(m.period) || m.period <= 0)
    return `object ${id}: motion needs finite amplitude/delay and period > 0`;
  return null;
}

/** Boundary check for JSON from storage or an imported file. Returns a reason when invalid. */
export function parseScene(raw: unknown): { doc: SceneDoc } | { error: string } {
  if (typeof raw !== 'object' || raw === null) return { error: 'not an object' };
  const d = raw as Partial<SceneDoc>;
  if (d.version !== SCENE_VERSION)
    return {
      error: `version ${String(d.version)} (expected ${SCENE_VERSION})`,
    };
  if (!d.palette || typeof d.palette !== 'object') return { error: 'missing palette' };
  if (!d.camera || !isNum(d.camera.zoom) || !isNum(d.camera.x) || !isNum(d.camera.y))
    return { error: 'missing camera' };
  if (!Array.isArray(d.layers)) return { error: 'missing layers' };
  const ids = d.layers.map((l) => l?.id);
  const missing = LAYER_IDS.filter((id) => !ids.includes(id));
  if (missing.length > 0) return { error: `missing layers ${missing.join(', ')}` };
  if (d.layers.some((l) => !Array.isArray(l.objects))) return { error: 'layer without objects' };
  // The renderer turns blur into a view filter; NaN or a negative radius would break it.
  const blurry = d.layers.find((l) => !isNum(l.blur) || l.blur < 0);
  if (blurry) return { error: `layer ${String(blurry.id)}: blur must be a number >= 0` };
  for (const o of d.layers.flatMap((l) => l.objects)) {
    const err = motionError(o.motion, String(o.id));
    if (err) return { error: err };
  }
  const err = timelineError(d.timeline);
  if (err) return { error: err };
  return { doc: d as SceneDoc };
}

function loadSaved(): { doc: SceneDoc; note: string | null } {
  let text: string | null = null;
  try {
    text = window.localStorage.getItem(STORAGE_KEY);
  } catch (e) {
    return { doc: defaultScene(), note: `Autosave unavailable: ${String(e)}` };
  }
  if (!text) return { doc: defaultScene(), note: null };
  try {
    const parsed = parseScene(JSON.parse(text));
    if ('doc' in parsed) return { doc: parsed.doc, note: 'Escena restaurada del autoguardado.' };
    return {
      doc: defaultScene(),
      note: `Autoguardado ignorado (${parsed.error}); se cargó el preset.`,
    };
  } catch (e) {
    return {
      doc: defaultScene(),
      note: `Autoguardado ilegible (${String(e)}); se cargó el preset.`,
    };
  }
}

interface State {
  past: SceneDoc[];
  present: SceneDoc;
  future: SceneDoc[];
}

function persist(doc: SceneDoc): string | null {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(doc));
    return null;
  } catch (e) {
    return String(e);
  }
}

export function useSceneHistory() {
  const [initial] = useState(loadSaved);
  const [state, setState] = useState<State>({
    past: [],
    present: initial.doc,
    future: [],
  });
  // Mirror of `state` for event handlers, so each edit is computed, stored and saved in one place.
  const current = useRef(state);
  const last = useRef<{ key: string; at: number } | null>(null);
  const [saveError, setSaveError] = useState<string | null>(null);

  const commit = useCallback((next: State) => {
    if (next === current.current) return;
    const saved = next.present !== current.current.present;
    current.current = next;
    setState(next);
    if (saved) setSaveError(persist(next.present));
  }, []);

  /** Replace the doc. Pass the same `key` for a continuous gesture so it undoes as one step. */
  const apply = useCallback(
    (next: SceneDoc, key?: string) => {
      const now = Date.now();
      const coalesce =
        key !== undefined && last.current?.key === key && now - last.current.at < COALESCE_MS;
      last.current = key === undefined ? null : { key, at: now };
      const s = current.current;
      if (next === s.present) return;
      commit(
        coalesce
          ? { ...s, present: next }
          : {
              past: [...s.past, s.present].slice(-MAX_UNDO),
              present: next,
              future: [],
            },
      );
    },
    [commit],
  );

  const undo = useCallback(() => {
    last.current = null;
    const s = current.current;
    if (s.past.length > 0)
      commit({
        past: s.past.slice(0, -1),
        present: s.past[s.past.length - 1],
        future: [s.present, ...s.future],
      });
  }, [commit]);

  const redo = useCallback(() => {
    last.current = null;
    const s = current.current;
    if (s.future.length > 0)
      commit({
        past: [...s.past, s.present],
        present: s.future[0],
        future: s.future.slice(1),
      });
  }, [commit]);

  return {
    doc: state.present,
    apply,
    undo,
    redo,
    canUndo: state.past.length > 0,
    canRedo: state.future.length > 0,
    loadNote: initial.note,
    saveError,
  };
}
