// Right panel: properties of the selection, its layer, and scene-wide camera and palette.
// It reads and edits the doc at the current progress; the Lab turns edits of keyframed
// properties into keyframes. The ◆ button next to a field adds or removes a keyframe there.
import { createContext, useContext, useId, useState, type ReactNode } from 'react';

import { locate, resolveColor, updateLayer, updateObject } from '@/onboarding/scene/doc';
import { MOTION_KINDS, targets } from '@/onboarding/scene/timeline';
import type {
  Body,
  Color,
  Motion,
  MotionKind,
  SceneDoc,
  SceneObject,
  Transform,
} from '@/onboarding/scene/types';

import { paramsOf, type ParamSpec } from './params';

export type KeyState = 'off' | 'tracked' | 'on';

interface Keying {
  keyState: (target: string) => KeyState;
  onKey: (target: string) => void;
}
const KeyingContext = createContext<Keying | null>(null);

interface InspectorProps extends Keying {
  doc: SceneDoc;
  edit: (doc: SceneDoc, key?: string) => void;
  selectedId: string | null;
}

const MOTION_LABELS: Record<MotionKind, string> = {
  drift: 'Deriva horizontal',
  bob: 'Flotar vertical',
  sway: 'Balanceo',
  breathe: 'Respirar (opacidad)',
  rise: 'Ascenso de vapor',
  live: 'Vida (Pet)',
};

export function Inspector({ doc, edit, selectedId, keyState, onKey }: InspectorProps) {
  const hit = selectedId ? locate(doc, selectedId) : null;
  return (
    <KeyingContext.Provider value={{ keyState, onKey }}>
      <div className="lab-inspector">
        {hit ? (
          <ObjectSections doc={doc} edit={edit} object={hit.object} />
        ) : (
          <p className="lab-empty">Selecciona un objeto en la escena o en las capas.</p>
        )}
        {hit && (
          <Section title={`Capa · ${hit.layer.name}`}>
            <Toggle
              label="Visible"
              value={hit.layer.visible}
              onChange={(v) => edit(updateLayer(doc, hit.layer.id, { visible: v }))}
            />
            <Toggle
              label="Bloqueada"
              value={hit.layer.locked}
              onChange={(v) => edit(updateLayer(doc, hit.layer.id, { locked: v }))}
            />
            <NumberField
              label="Profundidad (parallax)"
              value={hit.layer.parallax}
              min={0}
              max={1.5}
              step={0.01}
              onChange={(v) =>
                edit(
                  updateLayer(doc, hit.layer.id, { parallax: v }),
                  `layer:${hit.layer.id}:parallax`,
                )
              }
            />
            <NumberField
              label="Opacidad de capa"
              value={hit.layer.opacity}
              min={0}
              max={1}
              step={0.01}
              keyTarget={targets.layer(hit.layer.id)}
              onChange={(v) =>
                edit(
                  updateLayer(doc, hit.layer.id, { opacity: v }),
                  `layer:${hit.layer.id}:opacity`,
                )
              }
            />
            <NumberField
              label="Desenfoque (foco)"
              value={hit.layer.blur}
              min={0}
              max={12}
              step={0.1}
              keyTarget={targets.layer(hit.layer.id, 'blur')}
              onChange={(v) =>
                edit(updateLayer(doc, hit.layer.id, { blur: v }), `layer:${hit.layer.id}:blur`)
              }
            />
            {(hit.object.body.kind === 'snowCap' ||
              hit.object.body.kind === 'crater' ||
              hit.object.body.kind === 'steam') && (
              <p className="lab-note">
                Este objeto se mueve con el volcán: usa la profundidad de MainVolcano.
              </p>
            )}
          </Section>
        )}
        <Section title="Cámara (se anima entre pantallas)">
          {(['x', 'y', 'zoom'] as const).map((f) => (
            <NumberField
              key={f}
              label={f === 'zoom' ? 'Zoom de cámara' : `Cámara ${f.toUpperCase()}`}
              value={doc.camera[f]}
              min={f === 'zoom' ? 0.5 : -300}
              max={f === 'zoom' ? 2.5 : 300}
              step={f === 'zoom' ? 0.01 : 1}
              keyTarget={targets.camera(f)}
              onChange={(v) => edit({ ...doc, camera: { ...doc.camera, [f]: v } }, `camera:${f}`)}
            />
          ))}
        </Section>
        <Section title="Paleta">
          {Object.entries(doc.palette).map(([key, hex]) => (
            <div key={key} className="lab-field lab-palette-row">
              <span>{key}</span>
              <input
                type="color"
                value={hex}
                aria-label={`Paleta ${key}`}
                onChange={(e) =>
                  edit(
                    {
                      ...doc,
                      palette: {
                        ...doc.palette,
                        [key]: e.target.value.toUpperCase(),
                      },
                    },
                    `palette:${key}`,
                  )
                }
              />
              <code>{hex}</code>
              <KeyButton target={targets.palette(key)} />
            </div>
          ))}
        </Section>
      </div>
    </KeyingContext.Provider>
  );
}

function ObjectSections({
  doc,
  edit,
  object,
}: {
  doc: SceneDoc;
  edit: InspectorProps['edit'];
  object: SceneObject;
}) {
  const id = object.id;
  const setT = (k: keyof Transform) => (v: number) =>
    edit(
      updateObject(doc, id, (o) => ({
        ...o,
        transform: { ...o.transform, [k]: v },
      })),
      `t:${id}:${k}`,
    );
  const setBody = (k: string) => (v: number | string) =>
    edit(
      updateObject(doc, id, (o) => ({
        ...o,
        body: { ...o.body, [k]: v } as Body,
      })),
      `b:${id}:${k}`,
    );
  const setMotion = (m: Motion | null, key?: string) =>
    edit(
      updateObject(doc, id, (o) => ({ ...o, motion: m })),
      key,
    );
  const t = object.transform;
  const body = object.body as unknown as Record<string, number | string>;
  const tf = (k: keyof Transform, label: string, min: number, max: number, step: number) => (
    <NumberField
      label={label}
      value={t[k]}
      min={min}
      max={max}
      step={step}
      keyTarget={targets.transform(id, k)}
      onChange={setT(k)}
    />
  );
  return (
    <>
      <Section title={`${object.name}`}>
        <label className="lab-field">
          <span>Nombre</span>
          <input
            type="text"
            value={object.name}
            onChange={(e) =>
              edit(
                updateObject(doc, id, (o) => ({ ...o, name: e.target.value })),
                `name:${id}`,
              )
            }
          />
        </label>
        <p className="lab-meta">
          id <code>{id}</code> · tipo <code>{object.body.kind}</code>
        </p>
      </Section>
      {object.body.kind !== 'ui' && (
        <Section title="Transformación">
          {tf('x', 'Posición X', -800, 1200, 0.5)}
          {tf('y', 'Posición Y', -300, 1100, 0.5)}
          {tf('scaleX', 'Escala X', 0.1, 4, 0.01)}
          {tf('scaleY', 'Escala Y', 0.1, 4, 0.01)}
          {tf('rotation', 'Rotación (°)', -180, 180, 0.5)}
          {tf('opacity', 'Opacidad', 0, 1, 0.01)}
          {tf('anchorX', 'Ancla X', -400, 400, 0.5)}
          {tf('anchorY', 'Ancla Y', -400, 400, 0.5)}
        </Section>
      )}
      <Section title="Forma y color">
        {paramsOf(object.body).map((p) => (
          <ParamField
            key={p.key}
            spec={p}
            value={body[p.key]}
            palette={doc.palette}
            keyTarget={targets.body(id, p.key)}
            onChange={setBody(p.key)}
          />
        ))}
      </Section>
      {object.body.kind !== 'ui' && (
        <Section title="Movimiento en reposo">
          <label className="lab-field lab-select-row">
            <span>Tipo</span>
            <select
              value={object.motion?.kind ?? ''}
              onChange={(e) => {
                const kind = e.target.value as MotionKind | '';
                setMotion(
                  kind
                    ? {
                        kind,
                        amplitude: object.motion?.amplitude ?? 4,
                        period: object.motion?.period ?? 6,
                        delay: object.motion?.delay ?? 0,
                      }
                    : null,
                );
              }}
            >
              <option value="">Ninguno</option>
              {MOTION_KINDS.map((k) => (
                <option key={k} value={k}>
                  {MOTION_LABELS[k]}
                </option>
              ))}
            </select>
          </label>
          {object.motion && (
            <>
              {object.motion.kind !== 'rise' && (
                <NumberField
                  label="Amplitud"
                  value={object.motion.amplitude}
                  min={0}
                  max={object.motion.kind === 'breathe' ? 1 : 60}
                  step={0.1}
                  onChange={(v) =>
                    object.motion && setMotion({ ...object.motion, amplitude: v }, `motion:${id}:a`)
                  }
                />
              )}
              <NumberField
                label="Periodo (s)"
                value={object.motion.period}
                min={0.5}
                max={60}
                step={0.1}
                onChange={(v) =>
                  object.motion && setMotion({ ...object.motion, period: v }, `motion:${id}:p`)
                }
              />
              <NumberField
                label="Desfase (s)"
                value={object.motion.delay}
                min={0}
                max={30}
                step={0.1}
                onChange={(v) =>
                  object.motion && setMotion({ ...object.motion, delay: v }, `motion:${id}:d`)
                }
              />
            </>
          )}
        </Section>
      )}
      {object.body.kind !== 'ui' && (
        <Section title="Contorno">
          <ColorField
            label="Color"
            value={object.stroke}
            palette={doc.palette}
            onChange={(v) =>
              edit(
                updateObject(doc, id, (o) => ({ ...o, stroke: v })),
                `stroke:${id}`,
              )
            }
          />
          <NumberField
            label="Grosor"
            value={object.strokeWidth}
            min={0}
            max={8}
            step={0.1}
            onChange={(v) =>
              edit(
                updateObject(doc, id, (o) => ({ ...o, strokeWidth: v })),
                `strokeW:${id}`,
              )
            }
          />
        </Section>
      )}
    </>
  );
}

function ParamField({
  spec,
  value,
  palette,
  keyTarget,
  onChange,
}: {
  spec: ParamSpec;
  value: number | string;
  palette: Record<string, string>;
  keyTarget: string;
  onChange: (v: number | string) => void;
}) {
  if (spec.type === 'color')
    return (
      <ColorField
        label={spec.label}
        value={String(value)}
        palette={palette}
        keyTarget={keyTarget}
        onChange={onChange}
      />
    );
  if (spec.type === 'select')
    return (
      <label className="lab-field lab-select-row">
        <span>{spec.label}</span>
        <select value={String(value)} onChange={(e) => onChange(e.target.value)}>
          {spec.options.map((o) => (
            <option key={o} value={o}>
              {o}
            </option>
          ))}
        </select>
      </label>
    );
  if (spec.type === 'int')
    return (
      <NumberField
        label={spec.label}
        value={Number(value)}
        min={spec.min}
        max={spec.max}
        step={1}
        keyTarget={keyTarget}
        onChange={(v) => onChange(Math.round(v))}
      />
    );
  return (
    <NumberField
      label={spec.label}
      value={Number(value)}
      min={spec.min}
      max={spec.max}
      step={spec.step}
      keyTarget={keyTarget}
      onChange={onChange}
    />
  );
}

function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <details className="lab-section" open>
      <summary>{title}</summary>
      <div className="lab-section-body">{children}</div>
    </details>
  );
}

const KEY_TITLES: Record<KeyState, string> = {
  off: 'Animar: añadir keyframe aquí',
  tracked: 'Animado: añadir keyframe aquí',
  on: 'Quitar el keyframe de aquí',
};

function KeyButton({ target }: { target?: string }) {
  const keying = useContext(KeyingContext);
  if (!keying || !target) return null;
  const state = keying.keyState(target);
  return (
    <button
      type="button"
      className={`lab-key is-${state}`}
      title={KEY_TITLES[state]}
      aria-label={`${KEY_TITLES[state]} (${target})`}
      aria-pressed={state === 'on'}
      onClick={() => keying.onKey(target)}
    >
      {state === 'on' ? '◆' : '◇'}
    </button>
  );
}

export function NumberField({
  label,
  value,
  min,
  max,
  step,
  keyTarget,
  onChange,
}: {
  label: string;
  value: number;
  min: number;
  max: number;
  step: number;
  keyTarget?: string;
  onChange: (v: number) => void;
}) {
  const id = useId();
  // While typing, intermediate text like "-" or "" is not a number; keep it locally instead of
  // snapping the field back to the stored value.
  const [draft, setDraft] = useState<string | null>(null);
  const shown = String(Math.round(value * 1000) / 1000);
  const commit = (raw: string) => {
    const v = Number(raw);
    if (raw.trim() !== '' && Number.isFinite(v)) onChange(v);
  };
  return (
    <div className="lab-field lab-number">
      <label htmlFor={id}>{label}</label>
      <KeyButton target={keyTarget} />
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={Math.min(max, Math.max(min, value))}
        onChange={(e) => commit(e.target.value)}
        aria-label={label}
      />
      <input
        id={id}
        type="number"
        step={step}
        value={draft ?? shown}
        onFocus={() => setDraft(shown)}
        onBlur={() => setDraft(null)}
        onChange={(e) => {
          setDraft(e.target.value);
          commit(e.target.value);
        }}
      />
    </div>
  );
}

function ColorField({
  label,
  value,
  palette,
  keyTarget,
  onChange,
}: {
  label: string;
  value: Color;
  palette: Record<string, string>;
  keyTarget?: string;
  onChange: (v: Color) => void;
}) {
  const token = value.startsWith('$') ? value.slice(1) : '';
  let resolved: string;
  try {
    resolved = resolveColor(palette, value);
  } catch {
    // A dangling palette reference (only possible from a hand-edited import) shows as magenta.
    resolved = '#FF00FF';
  }
  return (
    <div className="lab-field lab-color">
      <span>{label}</span>
      <input
        type="color"
        value={resolved.slice(0, 7)}
        onChange={(e) => onChange(e.target.value.toUpperCase())}
        aria-label={label}
      />
      <select
        value={token}
        onChange={(e) => onChange(e.target.value ? `$${e.target.value}` : resolved)}
        aria-label={`${label}: color de paleta`}
      >
        <option value="">propio</option>
        {Object.keys(palette).map((k) => (
          <option key={k} value={k}>
            ${k}
          </option>
        ))}
      </select>
      <KeyButton target={keyTarget} />
    </div>
  );
}

function Toggle({
  label,
  value,
  onChange,
}: {
  label: string;
  value: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <label className="lab-field lab-toggle">
      <input type="checkbox" checked={value} onChange={(e) => onChange(e.target.checked)} />
      <span>{label}</span>
    </label>
  );
}
