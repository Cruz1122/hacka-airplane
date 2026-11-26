// Center of the Lab: the production scene inside a phone frame, with direct manipulation.
// All coordinate conversion goes through the browser's SVG CTMs, so the editor never re-implements
// the scene's transform math.
import {
  useEffect,
  useLayoutEffect,
  useRef,
  useState,
  type PointerEvent as ReactPointerEvent,
} from 'react';
import { StyleSheet, View } from 'react-native';
import { SafeAreaInsetsContext } from 'react-native-safe-area-context';

import { onboardingLayout } from '@/onboarding/layout';
import { NevadoScene } from '@/onboarding/NevadoScene';
import { OnboardingOverlay } from '@/onboarding/OnboardingOverlay';
import { locate, updateObject } from '@/onboarding/scene/doc';
import { sceneViewBox } from '@/onboarding/scene/geometry';
import type { Body, SceneDoc, Vec } from '@/onboarding/scene/types';

import { handlesOf } from './params';

export interface Device {
  id: string;
  label: string;
  w: number;
  h: number;
  insets: { top: number; bottom: number; left: number; right: number };
}

export const DEVICES: Device[] = [
  {
    id: '390x844',
    label: '390 × 844 (referencia)',
    w: 390,
    h: 844,
    insets: { top: 47, bottom: 34, left: 0, right: 0 },
  },
  {
    id: '375x812',
    label: '375 × 812',
    w: 375,
    h: 812,
    insets: { top: 44, bottom: 34, left: 0, right: 0 },
  },
  {
    id: '430x932',
    label: '430 × 932',
    w: 430,
    h: 932,
    insets: { top: 59, bottom: 34, left: 0, right: 0 },
  },
  {
    id: '360x800',
    label: '360 × 800 (Android)',
    w: 360,
    h: 800,
    insets: { top: 24, bottom: 16, left: 0, right: 0 },
  },
  {
    id: '768x1024',
    label: 'Tablet 768 × 1024',
    w: 768,
    h: 1024,
    insets: { top: 24, bottom: 20, left: 0, right: 0 },
  },
  {
    id: '820x1180',
    label: 'Tablet 820 × 1180',
    w: 820,
    h: 1180,
    insets: { top: 24, bottom: 20, left: 0, right: 0 },
  },
  {
    id: '1024x1366',
    label: 'Tablet 1024 × 1366',
    w: 1024,
    h: 1366,
    insets: { top: 24, bottom: 20, left: 0, right: 0 },
  },
  {
    id: '1180x820',
    label: 'Tablet horizontal 1180 × 820',
    w: 1180,
    h: 820,
    insets: { top: 24, bottom: 20, left: 0, right: 0 },
  },
];

export interface View2D {
  zoom: number;
  panX: number;
  panY: number;
}

interface StageProps {
  /** Editing truth: the doc at the current progress without idle motions. */
  doc: SceneDoc;
  /** What is drawn: `doc` plus idle motions while they run. */
  display: SceneDoc;
  edit: (doc: SceneDoc, key?: string) => void;
  /** False during sequence playback: only pan and zoom, no selection or drags. */
  interactive: boolean;
  selectedId: string | null;
  onSelect: (id: string | null) => void;
  device: Device;
  view: View2D;
  onView: (v: View2D) => void;
  guides: boolean;
  progress: number;
  /** A transition is running: the scene follows the camera with view transforms. */
  moving: boolean;
  onGo: (screen: number) => void;
  onCursor: (p: Vec | null) => void;
}

type Drag =
  | { kind: 'move'; id: string; inv: DOMMatrix; start: Vec; origin: Vec }
  | { kind: 'handle'; id: string; key: string; inv: DOMMatrix }
  | { kind: 'pan'; startX: number; startY: number; origin: View2D };

interface SelectionGeometry {
  corners: Vec[];
  anchor: Vec;
  handles: { key: string; label: string; x: number; y: number }[];
}

const toPoint = (m: DOMMatrix, x: number, y: number): Vec => {
  const p = new DOMPoint(x, y).matrixTransform(m);
  return { x: p.x, y: p.y };
};
const round1 = (n: number) => Math.round(n * 10) / 10;

/** Normalized radius inside which a gradient-filled puff counts as a click on it. */
const SOFT_CORE = 0.55;

/**
 * Browsers hit-test a gradient fill on its whole geometry, even where it fades to transparent, so
 * mist puffs, glows and halos would swallow clicks meant for the objects behind them. Such shapes
 * only count near their visible core.
 */
function isSoftEdgeHit(el: Element, x: number, y: number): boolean {
  const circle = el instanceof SVGCircleElement;
  if (!circle && !(el instanceof SVGEllipseElement)) return false;
  if (!(el.getAttribute('fill') ?? '').startsWith('url(')) return false;
  const ctm = (el as SVGGraphicsElement).getScreenCTM();
  if (!ctm) return false;
  const p = new DOMPoint(x, y).matrixTransform(ctm.inverse());
  const cx = circle ? el.cx.baseVal.value : (el as SVGEllipseElement).cx.baseVal.value;
  const cy = circle ? el.cy.baseVal.value : (el as SVGEllipseElement).cy.baseVal.value;
  const rx = circle ? el.r.baseVal.value : (el as SVGEllipseElement).rx.baseVal.value;
  const ry = circle ? el.r.baseVal.value : (el as SVGEllipseElement).ry.baseVal.value;
  return Math.hypot((p.x - cx) / rx, (p.y - cy) / ry) > SOFT_CORE;
}

export function Stage({
  doc,
  display,
  edit,
  interactive,
  selectedId,
  onSelect,
  device,
  view,
  onView,
  guides,
  progress,
  moving,
  onGo,
  onCursor,
}: StageProps) {
  const stageRef = useRef<HTMLDivElement>(null);
  const screenRef = useRef<HTMLDivElement>(null);
  const overlayRef = useRef<SVGSVGElement>(null);
  const drag = useRef<Drag | null>(null);
  const [spaceDown, setSpaceDown] = useState(false);
  const [sel, setSel] = useState<SelectionGeometry | null>(null);

  const objectEl = (id: string) =>
    screenRef.current?.querySelector<SVGGraphicsElement>(`[id="obj-${id}"]`) ?? null;

  // Selection outline and handles, measured from the rendered DOM after every change.
  useLayoutEffect(() => {
    const hit = selectedId ? locate(doc, selectedId) : null;
    const el = selectedId ? objectEl(selectedId) : null;
    const overlay = overlayRef.current;
    const elCtm = el?.getScreenCTM();
    const overlayCtm = overlay?.getScreenCTM();
    if (!hit || !el || !elCtm || !overlayCtm) {
      setSel(null);
      return;
    }
    const m = overlayCtm.inverse().multiply(elCtm);
    const bb = el.getBBox();
    const t = hit.object.transform;
    setSel({
      corners: [
        toPoint(m, bb.x, bb.y),
        toPoint(m, bb.x + bb.width, bb.y),
        toPoint(m, bb.x + bb.width, bb.y + bb.height),
        toPoint(m, bb.x, bb.y + bb.height),
      ],
      anchor: toPoint(m, t.anchorX, t.anchorY),
      handles: hit.layer.locked
        ? []
        : handlesOf(hit.object.body, doc).map((h) => ({
            key: h.key,
            label: h.label,
            ...toPoint(m, h.at.x, h.at.y),
          })),
    });
    // view, device and idle motions move the DOM without changing the doc, so they re-measure too.
  }, [doc, display, selectedId, view, device]);

  // Wheel: ctrl/cmd zooms at the cursor, plain wheel pans. Needs a non-passive listener.
  useEffect(() => {
    const el = stageRef.current;
    if (!el) return;
    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      if (e.ctrlKey || e.metaKey) {
        const rect = el.getBoundingClientRect();
        const cx = e.clientX - rect.left - rect.width / 2;
        const cy = e.clientY - rect.top - rect.height / 2;
        const zoom = Math.min(4, Math.max(0.25, view.zoom * Math.exp(-e.deltaY * 0.0015)));
        const k = zoom / view.zoom;
        onView({
          zoom,
          panX: cx - (cx - view.panX) * k,
          panY: cy - (cy - view.panY) * k,
        });
      } else {
        onView({
          ...view,
          panX: view.panX - e.deltaX,
          panY: view.panY - e.deltaY,
        });
      }
    };
    el.addEventListener('wheel', onWheel, { passive: false });
    return () => el.removeEventListener('wheel', onWheel);
  }, [view, onView]);

  useEffect(() => {
    const isTyping = (t: EventTarget | null) =>
      t instanceof HTMLElement && /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName);
    const down = (e: KeyboardEvent) => {
      if (e.code === 'Space' && !isTyping(e.target)) {
        e.preventDefault();
        setSpaceDown(true);
      }
    };
    const up = (e: KeyboardEvent) => e.code === 'Space' && setSpaceDown(false);
    window.addEventListener('keydown', down);
    window.addEventListener('keyup', up);
    return () => {
      window.removeEventListener('keydown', down);
      window.removeEventListener('keyup', up);
    };
  }, []);

  const scenePoint = (e: { clientX: number; clientY: number }): Vec | null => {
    const ctm = overlayRef.current?.getScreenCTM();
    return ctm ? toPoint(ctm.inverse(), e.clientX, e.clientY) : null;
  };

  /** Topmost unlocked, visible object under the pointer; locked layers are clicked through. */
  const pick = (x: number, y: number): string | 'ui-control' | null => {
    for (const el of document.elementsFromPoint(x, y)) {
      if (!screenRef.current?.contains(el)) continue;
      if (isSoftEdgeHit(el, x, y)) continue;
      if (el.closest('#lab-ui-overlay')) {
        if (el.closest('[role="button"],[role="tab"]')) return 'ui-control';
        const ui = locate(doc, 'ui');
        if (ui && !ui.layer.locked) return 'ui';
        continue;
      }
      const g = el.closest('[id^="obj-"]');
      if (!g) continue;
      const id = g.id.slice(4);
      const hit = locate(doc, id);
      if (hit && !hit.layer.locked && hit.layer.visible) return id;
    }
    return null;
  };

  const startPan = (e: ReactPointerEvent) => {
    drag.current = {
      kind: 'pan',
      startX: e.clientX,
      startY: e.clientY,
      origin: view,
    };
    stageRef.current?.setPointerCapture(e.pointerId);
  };

  const onStagePointerDown = (e: ReactPointerEvent<HTMLDivElement>) => {
    if (drag.current) return;
    // Leave text fields so keyboard shortcuts (undo, nudge, delete) reach the Lab, not the input.
    if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
    if (e.button === 1 || spaceDown || !screenRef.current?.contains(e.target as Node)) {
      e.preventDefault();
      startPan(e);
      if (!screenRef.current?.contains(e.target as Node) && e.button === 0 && !spaceDown)
        onSelect(null);
      return;
    }
    if (e.button !== 0) return;
    if (!interactive) {
      startPan(e);
      return;
    }
    const id = pick(e.clientX, e.clientY);
    if (id === 'ui-control') return;
    onSelect(id);
    if (!id || id === 'ui') return;
    const el = objectEl(id);
    const parent = el?.parentNode as SVGGraphicsElement | null;
    const ctm = parent?.getScreenCTM();
    const hit = locate(doc, id);
    if (!ctm || !hit) return;
    const inv = ctm.inverse();
    drag.current = {
      kind: 'move',
      id,
      inv,
      start: toPoint(inv, e.clientX, e.clientY),
      origin: { x: hit.object.transform.x, y: hit.object.transform.y },
    };
    stageRef.current?.setPointerCapture(e.pointerId);
  };

  const onHandlePointerDown = (e: ReactPointerEvent, key: string) => {
    e.stopPropagation();
    if (!selectedId) return;
    const ctm = objectEl(selectedId)?.getScreenCTM();
    if (!ctm) return;
    drag.current = { kind: 'handle', id: selectedId, key, inv: ctm.inverse() };
    stageRef.current?.setPointerCapture(e.pointerId);
  };

  const onPointerMove = (e: ReactPointerEvent<HTMLDivElement>) => {
    onCursor(scenePoint(e));
    const d = drag.current;
    if (!d) return;
    if (d.kind === 'pan') {
      onView({
        ...d.origin,
        panX: d.origin.panX + e.clientX - d.startX,
        panY: d.origin.panY + e.clientY - d.startY,
      });
    } else if (d.kind === 'move') {
      const p = toPoint(d.inv, e.clientX, e.clientY);
      edit(
        updateObject(doc, d.id, (o) => ({
          ...o,
          transform: {
            ...o.transform,
            x: round1(d.origin.x + p.x - d.start.x),
            y: round1(d.origin.y + p.y - d.start.y),
          },
        })),
        `move:${d.id}`,
      );
    } else {
      const hit = locate(doc, d.id);
      const handle = hit && handlesOf(hit.object.body, doc).find((h) => h.key === d.key);
      if (!hit || !handle) return;
      const before = hit.object.body as unknown as Record<string, unknown>;
      const raw = handle.set(toPoint(d.inv, e.clientX, e.clientY)) as unknown as Record<
        string,
        unknown
      >;
      // Round only what the handle changed: rounding an untouched (possibly keyframed) field would
      // look like an edit and create a spurious keyframe.
      const body = Object.fromEntries(
        Object.entries(raw).map(([k, v]) => [
          k,
          typeof v === 'number' && v !== before[k] ? Math.round(v * 100) / 100 : v,
        ]),
      ) as unknown as Body;
      edit(
        updateObject(doc, d.id, (o) => ({ ...o, body })),
        `handle:${d.id}:${d.key}`,
      );
    }
  };

  const endDrag = (e: ReactPointerEvent<HTMLDivElement>) => {
    if (drag.current && stageRef.current?.hasPointerCapture(e.pointerId))
      stageRef.current.releasePointerCapture(e.pointerId);
    drag.current = null;
  };

  const sceneH = onboardingLayout(device.w, device.h, device.insets.bottom).scene;
  const vb = sceneViewBox(device.w, sceneH);
  // Handles keep a constant on-screen size whatever the Lab zoom and the device's scene scale.
  const unit = vb.width / device.w / view.zoom;
  const handleR = 7 * unit;
  const grid = [];
  if (guides) {
    for (let x = Math.ceil(vb.x / 50) * 50; x <= vb.x + vb.width; x += 50)
      grid.push(<line key={`x${x}`} x1={x} y1={vb.y} x2={x} y2={vb.y + vb.height} />);
    for (let y = Math.ceil(vb.y / 50) * 50; y <= vb.y + vb.height; y += 50)
      grid.push(<line key={`y${y}`} x1={vb.x} y1={y} x2={vb.x + vb.width} y2={y} />);
  }

  return (
    <div
      ref={stageRef}
      className={`lab-stage${spaceDown ? ' is-panning' : ''}`}
      onPointerDown={onStagePointerDown}
      onPointerMove={onPointerMove}
      onPointerUp={endDrag}
      onPointerCancel={endDrag}
      onPointerLeave={() => onCursor(null)}
    >
      <div
        className="lab-frame"
        style={{
          width: device.w,
          height: device.h,
          transform: `translate(-50%, -50%) translate(${view.panX}px, ${view.panY}px) scale(${view.zoom})`,
        }}
      >
        <div ref={screenRef} className="lab-screen">
          <NevadoScene doc={display} width={device.w} height={sceneH} moving={moving} />
          <SafeAreaInsetsContext.Provider value={device.insets}>
            <View
              nativeID="lab-ui-overlay"
              style={StyleSheet.absoluteFill}
              pointerEvents="box-none"
            >
              <OnboardingOverlay
                doc={display}
                progress={progress}
                width={device.w}
                cardHeight={onboardingLayout(device.w, device.h, device.insets.bottom).card}
                onGo={onGo}
                onDone={() => onGo(0)}
              />
            </View>
          </SafeAreaInsetsContext.Provider>
          {guides && (
            <>
              <div
                className="lab-safe"
                style={{ top: 0, height: device.insets.top }}
                title="Safe area superior"
              />
              <div
                className="lab-safe"
                style={{ bottom: 0, height: device.insets.bottom }}
                title="Safe area inferior"
              />
            </>
          )}
          <svg
            ref={overlayRef}
            className="lab-overlay"
            style={{ height: sceneH, bottom: 'auto' }}
            viewBox={`${vb.x} ${vb.y} ${vb.width} ${vb.height}`}
            preserveAspectRatio="xMidYMax slice"
          >
            {guides && (
              <g className="lab-grid" strokeWidth={0.5 * unit}>
                {grid}
              </g>
            )}
            {sel && (
              <>
                <polygon
                  className="lab-bbox"
                  points={sel.corners.map((p) => `${p.x},${p.y}`).join(' ')}
                  strokeWidth={1.2 * unit}
                  strokeDasharray={`${4 * unit} ${3 * unit}`}
                />
                <path
                  className="lab-anchor"
                  d={`M ${sel.anchor.x - handleR} ${sel.anchor.y} H ${sel.anchor.x + handleR} M ${sel.anchor.x} ${sel.anchor.y - handleR} V ${sel.anchor.y + handleR}`}
                  strokeWidth={1.2 * unit}
                />
                {interactive &&
                  sel.handles.map((h) => (
                    <circle
                      key={h.key}
                      className="lab-handle"
                      cx={h.x}
                      cy={h.y}
                      r={handleR}
                      strokeWidth={1.6 * unit}
                      onPointerDown={(e) => onHandlePointerDown(e, h.key)}
                    >
                      <title>{h.label}</title>
                    </circle>
                  ))}
              </>
            )}
          </svg>
        </div>
      </div>
    </div>
  );
}
