// Onboarding Lab (web only, served by `npx expo start --web` at /lab). Edits the same SceneDoc the
// app renders; never imported by production screens.
import { useEffect, useMemo, useRef, useState } from 'react';

import { deleteObject, duplicateObject, locate, updateObject } from '@/onboarding/scene/doc';
import { onboardingLayout } from '@/onboarding/layout';
import { sceneViewBox } from '@/onboarding/scene/geometry';
import { defaultScene } from '@/onboarding/scene/preset';
import {
  applyMotions,
  commitEdit,
  evaluateTracks,
  isTracked,
  keyAt,
  toggleKeyframe,
} from '@/onboarding/scene/timeline';
import type { SceneDoc, Vec } from '@/onboarding/scene/types';
import { ONBOARDING_SCREENS } from '@/onboarding/scene/types';
import { usePlayback } from '@/onboarding/usePlayback';

import { Icon } from './icons';
import { Inspector } from './Inspector';
import { LAB_CSS } from './labCss';
import { LayerPanel } from './LayerPanel';
import { DEVICES, Stage, type View2D } from './Stage';
import { TimelinePanel } from './TimelinePanel';
import { parseScene, useSceneHistory } from './useSceneHistory';

/** Pause on each screen while previewing the whole sequence. */
const HOLD_MS = 1200;

function download(name: string, type: string, text: string) {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  a.click();
  URL.revokeObjectURL(url);
}

export default function Lab() {
  const history = useSceneHistory();
  const { doc, apply, undo, redo } = history;
  const [playing, setPlaying] = useState(false);
  const [ambient, setAmbient] = useState(true);
  const [reduced, setReduced] = useState(false);
  const play = usePlayback({
    transitionMs: doc.timeline.transitionMs,
    easing: doc.timeline.easing,
    ambient,
    reduced,
  });
  const { progress, goTo, scrub, progressNow, animating } = play;
  // Panels read and edit `current` (the doc at this progress, motions frozen); `display` is drawn.
  const current = useMemo(() => evaluateTracks(doc, progress), [doc, progress]);
  const display = play.time === null ? current : applyMotions(current, play.time);
  /** Every panel edit goes through here, so keyframed properties become keyframes. */
  const edit = (next: SceneDoc, key?: string) => {
    setPlaying(false);
    // Stop a running transition where the user sees it, or each frame would get its own keyframe.
    if (animating) scrub(progress);
    apply(commitEdit(doc, current, next, progress), key);
  };
  const [pickedId, setSelectedId] = useState<string | null>(null);
  // A selection can outlive its object (undo past a duplicate, import, reset); treat it as none.
  const selectedId = pickedId && locate(doc, pickedId) ? pickedId : null;
  const [deviceId, setDeviceId] = useState(DEVICES[0].id);
  const device = DEVICES.find((d) => d.id === deviceId) ?? DEVICES[0];
  const [view, setView] = useState<View2D>({ zoom: 0.85, panX: 0, panY: 0 });
  const [guides, setGuides] = useState(false);
  const [cursor, setCursor] = useState<Vec | null>(null);
  const [message, setMessage] = useState<string | null>(history.loadNote);
  const fileRef = useRef<HTMLInputElement>(null);
  const stageBox = useRef<HTMLDivElement>(null);

  const fit = () => {
    const box = stageBox.current?.getBoundingClientRect();
    if (!box) return;
    setView({
      zoom: Math.min(1.5, (box.height - 48) / device.h, (box.width - 48) / device.w),
      panX: 0,
      panY: 0,
    });
  };
  // Fit on mount, when the device changes and when the stage is resized (window, timeline panel).
  useEffect(() => {
    const el = stageBox.current;
    if (!el) return;
    const observer = new ResizeObserver(() => fit());
    observer.observe(el);
    return () => observer.disconnect();
  }, [deviceId]); // eslint-disable-line react-hooks/exhaustive-deps

  // Sequence preview: hold on a screen, move to the next, cut back to the first after the last.
  useEffect(() => {
    if (!playing || animating) return;
    const id = setTimeout(() => {
      const at = Math.round(progressNow());
      if (at >= ONBOARDING_SCREENS - 1) scrub(0);
      else goTo(at + 1);
    }, HOLD_MS);
    return () => clearTimeout(id);
  }, [playing, animating, progress, goTo, scrub, progressNow]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const t = e.target;
      if (t instanceof HTMLElement && /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName)) return;
      const mod = e.ctrlKey || e.metaKey;
      if (mod && e.key.toLowerCase() === 'z') {
        e.preventDefault();
        if (e.shiftKey) redo();
        else undo();
      } else if (mod && e.key.toLowerCase() === 'y') {
        e.preventDefault();
        redo();
      } else if (selectedId && mod && e.key.toLowerCase() === 'd') {
        e.preventDefault();
        const r = duplicateObject(current, selectedId);
        edit(r.doc);
        setSelectedId(r.id);
      } else if (selectedId && (e.key === 'Delete' || e.key === 'Backspace')) {
        try {
          edit(deleteObject(current, selectedId));
          setSelectedId(null);
        } catch (err) {
          setMessage(err instanceof Error ? err.message : String(err));
        }
      } else if (e.key === 'Escape') {
        setSelectedId(null);
      } else if (selectedId && e.key.startsWith('Arrow')) {
        e.preventDefault();
        const d = e.shiftKey ? 10 : 1;
        const dx = e.key === 'ArrowLeft' ? -d : e.key === 'ArrowRight' ? d : 0;
        const dy = e.key === 'ArrowUp' ? -d : e.key === 'ArrowDown' ? d : 0;
        edit(
          updateObject(current, selectedId, (o) => ({
            ...o,
            transform: {
              ...o.transform,
              x: o.transform.x + dx,
              y: o.transform.y + dy,
            },
          })),
          `nudge:${selectedId}`,
        );
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  });

  const exportSvg = () => {
    // The scene draws one <svg> per layer; the file merges them back into one, with the layer
    // opacity and blur (view styles on screen) written as SVG attributes.
    const groups = [
      ...(stageBox.current?.querySelectorAll<SVGGElement>(
        '.lab-screen svg:not(.lab-overlay) > g[id^="layer-"]',
      ) ?? []),
    ];
    const first = groups[0]?.ownerSVGElement;
    if (!first) {
      setMessage('No se encontró el SVG de la escena.');
      return;
    }
    const NS = 'http://www.w3.org/2000/svg';
    const clone = first.cloneNode(false) as SVGSVGElement;
    const defs = document.createElementNS(NS, 'defs');
    clone.appendChild(defs);
    for (const g of groups) {
      const copy = g.cloneNode(true) as SVGGElement;
      const layer = current.layers.find((l) => `layer-${l.id}` === g.id);
      if (layer && layer.opacity !== 1) copy.setAttribute('opacity', String(layer.opacity));
      if (layer && layer.blur > 0) {
        const filter = document.createElementNS(NS, 'filter');
        filter.setAttribute('id', `${g.id}-blur`);
        const blur = document.createElementNS(NS, 'feGaussianBlur');
        blur.setAttribute('stdDeviation', String(layer.blur));
        filter.appendChild(blur);
        defs.appendChild(filter);
        copy.setAttribute('filter', `url(#${g.id}-blur)`);
      }
      clone.appendChild(copy);
    }
    clone.setAttribute('xmlns', NS);
    const vb = sceneViewBox(
      device.w,
      onboardingLayout(device.w, device.h, device.insets.bottom).scene,
    );
    clone.setAttribute('width', String(Math.round(vb.width)));
    clone.setAttribute('height', String(Math.round(vb.height)));
    clone.removeAttribute('style');
    download(
      'nevado-scene.svg',
      'image/svg+xml',
      `<?xml version="1.0" encoding="UTF-8"?>\n${clone.outerHTML}`,
    );
  };

  const importJson = async (file: File) => {
    try {
      const parsed = parseScene(JSON.parse(await file.text()));
      if ('error' in parsed) {
        setMessage(`Importación rechazada: ${parsed.error}`);
        return;
      }
      apply(parsed.doc);
      setSelectedId(null);
      setMessage(`Importado ${file.name}.`);
    } catch (e) {
      setMessage(`Importación fallida: ${String(e)}`);
    }
  };

  const copyJson = async () => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(doc, null, 2));
      setMessage('JSON copiado al portapapeles.');
    } catch (e) {
      setMessage(`No se pudo copiar: ${String(e)}`);
    }
  };

  const selected = selectedId ? locate(doc, selectedId) : null;

  return (
    <div className="lab-root">
      <style>{LAB_CSS}</style>
      <header className="lab-toolbar">
        <strong className="lab-brand">Onboarding Lab</strong>
        <span className="lab-sep" />
        <button
          type="button"
          className="lab-btn"
          onClick={undo}
          disabled={!history.canUndo}
          title="Deshacer (Ctrl+Z)"
        >
          <Icon name="undo" /> Deshacer
        </button>
        <button
          type="button"
          className="lab-btn"
          onClick={redo}
          disabled={!history.canRedo}
          title="Rehacer (Ctrl+Shift+Z)"
        >
          <Icon name="redo" /> Rehacer
        </button>
        <span className="lab-sep" />
        <label className="lab-inline">
          Dispositivo
          <select value={deviceId} onChange={(e) => setDeviceId(e.target.value)}>
            {DEVICES.map((d) => (
              <option key={d.id} value={d.id}>
                {d.label}
              </option>
            ))}
          </select>
        </label>
        <button
          type="button"
          className="lab-btn"
          onClick={() => setView({ ...view, zoom: Math.max(0.25, view.zoom / 1.2) })}
          aria-label="Alejar"
        >
          −
        </button>
        <span className="lab-zoom">{Math.round(view.zoom * 100)}%</span>
        <button
          type="button"
          className="lab-btn"
          onClick={() => setView({ ...view, zoom: Math.min(4, view.zoom * 1.2) })}
          aria-label="Acercar"
        >
          +
        </button>
        <button type="button" className="lab-btn" onClick={fit}>
          Ajustar
        </button>
        <label className="lab-inline">
          <input type="checkbox" checked={guides} onChange={(e) => setGuides(e.target.checked)} />{' '}
          Guías
        </label>
        <span className="lab-grow" />
        <button
          type="button"
          className="lab-btn"
          onClick={() =>
            download('nevado-scene.json', 'application/json', JSON.stringify(doc, null, 2))
          }
        >
          Exportar JSON
        </button>
        <button type="button" className="lab-btn" onClick={() => fileRef.current?.click()}>
          Importar JSON
        </button>
        <button type="button" className="lab-btn" onClick={copyJson}>
          Copiar JSON
        </button>
        <button type="button" className="lab-btn" onClick={exportSvg}>
          Exportar SVG
        </button>
        <button
          type="button"
          className="lab-btn lab-danger"
          onClick={() => {
            if (
              window.confirm('¿Descartar los cambios y volver al preset? (Deshacer lo recupera)')
            ) {
              apply(defaultScene());
              setSelectedId(null);
            }
          }}
        >
          Preset
        </button>
        <input
          ref={fileRef}
          type="file"
          accept="application/json,.json"
          hidden
          onChange={(e) => {
            const f = e.target.files?.[0];
            if (f) void importJson(f);
            e.target.value = '';
          }}
        />
      </header>
      <aside className="lab-left" aria-label="Capas">
        <h2 className="lab-panel-title">Capas</h2>
        <LayerPanel
          doc={current}
          apply={edit}
          selectedId={selectedId}
          onSelect={setSelectedId}
          onError={setMessage}
        />
      </aside>
      <main className="lab-center" ref={stageBox}>
        <Stage
          doc={current}
          display={display}
          edit={edit}
          interactive={!playing}
          selectedId={selectedId}
          onSelect={setSelectedId}
          device={device}
          view={view}
          onView={setView}
          guides={guides}
          progress={progress}
          moving={play.moving}
          onGo={goTo}
          onCursor={setCursor}
        />
      </main>
      <aside className="lab-right" aria-label="Inspector">
        <h2 className="lab-panel-title">Inspector</h2>
        <Inspector
          doc={current}
          edit={edit}
          selectedId={selectedId}
          keyState={(target) =>
            keyAt(doc, target, progress) ? 'on' : isTracked(doc, target) ? 'tracked' : 'off'
          }
          onKey={(target) => {
            setPlaying(false);
            if (animating) scrub(progress);
            apply(toggleKeyframe(doc, current, target, progress));
          }}
        />
      </aside>
      <TimelinePanel
        doc={doc}
        view={current}
        apply={apply}
        progress={progress}
        playing={playing}
        onPlay={setPlaying}
        onScrub={(p) => {
          setPlaying(false);
          scrub(p);
        }}
        onGo={goTo}
        ambient={ambient}
        onAmbient={setAmbient}
        reduced={reduced}
        onReduced={setReduced}
        selectedId={selectedId}
        onSelect={setSelectedId}
      />
      <footer className="lab-status">
        <span className="lab-coords">
          {cursor ? `x ${cursor.x.toFixed(1)} · y ${cursor.y.toFixed(1)}` : 'x — · y —'}
        </span>
        <span>
          {selected ? `${selected.layer.name} › ${selected.object.name}` : 'Sin selección'}
        </span>
        <span className="lab-grow" />
        {message && (
          <button
            type="button"
            className="lab-message"
            onClick={() => setMessage(null)}
            title="Cerrar"
          >
            {message} ✕
          </button>
        )}
        <span className={history.saveError ? 'lab-error' : 'lab-muted'}>
          {history.saveError ? `Autoguardado falló: ${history.saveError}` : 'Autoguardado local'}
        </span>
        <span className="lab-muted">Espacio + arrastrar o rueda: mover · Ctrl + rueda: zoom</span>
      </footer>
    </div>
  );
}
