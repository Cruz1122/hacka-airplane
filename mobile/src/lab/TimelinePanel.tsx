// Bottom panel: play the three screens, scrub the progress, and edit tracks and their keyframes.
import { locate } from '@/onboarding/scene/doc';
import { EASING_NAMES, keyAt, parseTarget, toggleKeyframe } from '@/onboarding/scene/timeline';
import type { EasingName, SceneDoc } from '@/onboarding/scene/types';
import { ONBOARDING_SCREENS } from '@/onboarding/scene/types';

const LAST = ONBOARDING_SCREENS - 1;

const EASING_LABELS: Record<EasingName, string> = {
  linear: 'Lineal',
  easeIn: 'Acelera',
  easeOut: 'Frena',
  easeInOut: 'Suave',
};

interface TimelinePanelProps {
  /** Base doc: tracks and timing are edited here directly. */
  doc: SceneDoc;
  /** Doc at the current progress, for the value a new keyframe takes. */
  view: SceneDoc;
  apply: (doc: SceneDoc, key?: string) => void;
  progress: number;
  playing: boolean;
  onPlay: (playing: boolean) => void;
  onScrub: (p: number) => void;
  onGo: (screen: number) => void;
  ambient: boolean;
  onAmbient: (on: boolean) => void;
  reduced: boolean;
  onReduced: (on: boolean) => void;
  selectedId: string | null;
  onSelect: (id: string) => void;
}

function trackLabel(
  doc: SceneDoc,
  target: string,
): { owner: string; field: string; objectId: string | null } {
  const ref = parseTarget(target);
  if (!ref) return { owner: '?', field: target, objectId: null };
  if (ref.kind === 'camera') return { owner: 'Cámara', field: ref.field, objectId: null };
  if (ref.kind === 'palette') return { owner: 'Paleta', field: ref.key, objectId: null };
  if (ref.kind === 'layer')
    return {
      owner: `Capa ${ref.id}`,
      field: ref.field === 'blur' ? 'desenfoque' : 'opacidad',
      objectId: null,
    };
  return {
    owner: locate(doc, ref.id)?.object.name ?? ref.id,
    field: ref.field,
    objectId: ref.id,
  };
}

/** "Pantalla 1 → 2 · 42 %" for a fractional progress, "Pantalla 2" on a screen. */
function describe(p: number): string {
  const from = Math.floor(p + 1e-6);
  const frac = p - from;
  if (frac < 0.005) return `Pantalla ${from + 1}`;
  return `Pantalla ${from + 1} → ${from + 2} · ${Math.round(frac * 100)} %`;
}

export function TimelinePanel(props: TimelinePanelProps) {
  const { doc, view, apply, progress, playing, onPlay, onScrub, onGo, selectedId } = props;
  const t = doc.timeline;
  const pct = (at: number) => `${(at / LAST) * 100}%`;
  const setTrackEasing = (target: string, easing: EasingName) =>
    apply({
      ...doc,
      timeline: {
        ...t,
        tracks: t.tracks.map((tr) => (tr.target === target ? { ...tr, easing } : tr)),
      },
    });
  const removeTrack = (target: string) =>
    apply({
      ...doc,
      timeline: { ...t, tracks: t.tracks.filter((tr) => tr.target !== target) },
    });

  return (
    <section className="lab-timeline" aria-label="Línea de tiempo">
      <div className="lab-timeline-bar">
        <button
          type="button"
          className="lab-btn lab-play"
          onClick={() => onPlay(!playing)}
          aria-pressed={playing}
        >
          {playing ? '❚❚ Pausa' : '▶ Reproducir'}
        </button>
        <span className="lab-inline">
          Pantalla
          {Array.from({ length: ONBOARDING_SCREENS }, (_, i) => (
            <button
              key={i}
              type="button"
              className={`lab-step${Math.abs(progress - i) < 0.005 ? ' is-active' : ''}`}
              onClick={() => onGo(i)}
            >
              {i + 1}
            </button>
          ))}
        </span>
        <input
          className="lab-scrub"
          type="range"
          min={0}
          max={LAST}
          step={0.005}
          value={progress}
          onChange={(e) => onScrub(Number(e.target.value))}
          aria-label="Progreso del onboarding"
          aria-valuetext={describe(progress)}
        />
        <span className="lab-progress">{describe(progress)}</span>
        <label className="lab-inline">
          Duración
          <input
            type="number"
            className="lab-small-num"
            min={100}
            max={6000}
            step={50}
            value={t.transitionMs}
            onChange={(e) => {
              const v = Number(e.target.value);
              if (Number.isFinite(v) && v >= 100)
                apply({ ...doc, timeline: { ...t, transitionMs: Math.round(v) } }, 'timeline:ms');
            }}
          />
          ms
        </label>
        <label className="lab-inline">
          Curva
          <select
            value={t.easing}
            onChange={(e) =>
              apply({
                ...doc,
                timeline: { ...t, easing: e.target.value as EasingName },
              })
            }
          >
            {EASING_NAMES.map((n) => (
              <option key={n} value={n}>
                {EASING_LABELS[n]}
              </option>
            ))}
          </select>
        </label>
        <label className="lab-inline">
          <input
            type="checkbox"
            checked={props.ambient}
            onChange={(e) => props.onAmbient(e.target.checked)}
          />{' '}
          Movimiento ambiental
        </label>
        <label className="lab-inline">
          <input
            type="checkbox"
            checked={props.reduced}
            onChange={(e) => props.onReduced(e.target.checked)}
          />{' '}
          Movimiento reducido
        </label>
      </div>
      <div className="lab-tracks">
        {t.tracks.length === 0 && (
          <p className="lab-empty">
            Sin pistas. Usa ◇ junto a una propiedad del inspector para animarla.
          </p>
        )}
        {t.tracks.map((tr) => {
          const label = trackLabel(doc, tr.target);
          const here = keyAt(doc, tr.target, progress);
          return (
            <div
              key={tr.target}
              className={`lab-track${label.objectId && label.objectId === selectedId ? ' is-selected' : ''}`}
            >
              <button
                type="button"
                className="lab-track-name"
                title={tr.target}
                onClick={() => label.objectId && props.onSelect(label.objectId)}
              >
                <strong>{label.owner}</strong> · {label.field}
              </button>
              <select
                value={tr.easing}
                onChange={(e) => setTrackEasing(tr.target, e.target.value as EasingName)}
                aria-label={`Curva de ${tr.target}`}
              >
                {EASING_NAMES.map((n) => (
                  <option key={n} value={n}>
                    {EASING_LABELS[n]}
                  </option>
                ))}
              </select>
              <div className="lab-lane">
                {Array.from({ length: ONBOARDING_SCREENS }, (_, i) => (
                  <span key={i} className="lab-lane-tick" style={{ left: pct(i) }} />
                ))}
                {tr.keys.map((k) => (
                  <button
                    key={k.at}
                    type="button"
                    className={`lab-diamond${Math.abs(k.at - progress) < 0.005 ? ' is-current' : ''}`}
                    style={{ left: pct(k.at) }}
                    title={`${k.at.toFixed(3)} → ${String(k.value)}`}
                    aria-label={`Keyframe en ${k.at.toFixed(2)}: ${String(k.value)}`}
                    onClick={() => onScrub(k.at)}
                  />
                ))}
                <span className="lab-playhead" style={{ left: pct(progress) }} />
              </div>
              <button
                type="button"
                className={`lab-key is-${here ? 'on' : 'tracked'}`}
                onClick={() => apply(toggleKeyframe(doc, view, tr.target, progress))}
                title={here ? 'Quitar keyframe aquí' : 'Añadir keyframe aquí'}
              >
                {here ? '◆' : '◇'}
              </button>
              <button
                type="button"
                className="lab-icon-btn"
                onClick={() => removeTrack(tr.target)}
                title="Eliminar pista"
                aria-label={`Eliminar pista ${tr.target}`}
              >
                ✕
              </button>
            </div>
          );
        })}
      </div>
    </section>
  );
}
