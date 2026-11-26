// Standalone animated Pet: <Pet size={180} emotion="happy" voice="speaking" audioLevel={0.6} />.
// One requestAnimationFrame loop drives time, blinking, emotion transitions and the gaze (the
// `lookAt` point, the pointer on web; otherwise it looks around on its own). Every frame comes from petFrame(), the
// same function the onboarding scene uses, and is drawn as vapor like the scene's Pet.
import { useEffect, useId, useMemo, useRef, useState } from 'react';
import {
  Dimensions,
  Platform,
  View,
  type HostInstance,
  type StyleProp,
  type ViewStyle,
} from 'react-native';

import { useReducedMotion } from '@/ui/useReducedMotion';

import { brand } from '../theme/tokens';

import { PetVaporCanvas } from './PetVaporCanvas';
import {
  applyDeadzone,
  blinkAt,
  clamp,
  copyConfig,
  DEFAULT_TRACKING,
  ease,
  lerp,
  PET_NAME,
  PET_PRESET,
  PET_VIEWBOX,
  petFrame,
  transitionFace,
  type FaceState,
  type PetConfig,
  type PetEmotion,
  type VoiceState,
} from './petCore';

export interface PetProps {
  /** Width in points; height follows the viewBox. */
  size?: number;
  emotion?: PetEmotion;
  voice?: VoiceState;
  /** 0..1, drives the speaking mouth. */
  audioLevel?: number;
  /** Freeze procedural time and blinking. */
  paused?: boolean;
  /** Force reduced effects; the system setting also applies. */
  reducedMotion?: boolean;
  /** Follow the mouse (web only; touch screens have no hover). */
  trackPointer?: boolean;
  /** Glance around now and then while nothing is being tracked. */
  lookAround?: boolean;
  /**
   * A point to look at, in window coordinates (e.g. the last character typed); it holds the gaze
   * like a resting pointer. null hands the gaze back to glancing around.
   */
  lookAt?: { x: number; y: number } | null;

  /** Vapor colors; default to the card white and its shade. */
  fill?: string;
  shade?: string;
  /** Part of the Pet to show, in Pet units; defaults to the whole PET_VIEWBOX. */
  crop?: { x: number; y: number; width: number; height: number };
  /** Full preset; defaults to PET_PRESET. */
  config?: PetConfig;
  style?: StyleProp<ViewStyle>;
}

interface Engine {
  time: number;
  last: number;
  from: FaceState;
  shown: FaceState;
  transitionStart: number;
  emotion: PetEmotion;
  gazeX: number;
  gazeY: number;
  targetX: number;
  targetY: number;
  mirrored: boolean;
  mirrorFrom: number;
  mirrorTo: number;
  mirrorStarted: number;
  mirrorDuration: number;
  mirrorProgress: number;
  /** When the pointer last moved; glancing around waits until it rests. */
  pointerAt: number;
  nextLook: number;
}

/** A pointer at rest for this long hands the gaze back to glancing around. */
const POINTER_REST_MS = 2500;

interface Snapshot {
  time: number;
  face: FaceState;
  gaze: { x: number; y: number };
  mirror: number;
}

export function Pet({
  size = 180,
  emotion = 'idle',
  voice = 'idle',
  audioLevel = 0,
  paused = false,
  reducedMotion,
  trackPointer = true,
  lookAround = true,
  lookAt = null,
  fill = brand.card,
  shade = brand.cardShade,
  crop = PET_VIEWBOX,
  config = PET_PRESET,
  style,
}: PetProps) {
  const prefix = `pet${useId().replace(/[^a-zA-Z0-9]/g, '')}`;
  const systemReduced = useReducedMotion();
  const reduced = reducedMotion ?? systemReduced;
  const cfg = useMemo(() => {
    const next = copyConfig(config);
    next.emotion = emotion;
    next.voice = voice;
    next.audio = clamp(audioLevel, 0, 1);
    next.motion.reducedEffects = next.motion.reducedEffects || reduced;
    return next;
  }, [config, emotion, voice, audioLevel, reduced]);
  const [snap, setSnap] = useState<Snapshot>(() => ({
    time: 0,
    face: cfg.poses[cfg.emotion],
    gaze: { x: 0, y: 0 },
    mirror: 0,
  }));
  const engine = useRef<Engine | null>(null);
  const host = useRef<HostInstance>(null);

  // Emotion changes start a transition from whatever pose is on screen now.
  useEffect(() => {
    const e = engine.current;
    if (!e || e.emotion === cfg.emotion) return;
    e.from = e.shown;
    e.transitionStart = performance.now();
    e.emotion = cfg.emotion;
  }, [cfg.emotion]);

  useEffect(() => {
    engine.current ??= {
      time: 0,
      last: 0,
      from: cfg.poses[cfg.emotion],
      shown: cfg.poses[cfg.emotion],
      transitionStart: -Infinity,
      emotion: cfg.emotion,
      gazeX: 0,
      gazeY: 0,
      targetX: 0,
      targetY: 0,
      mirrored: false,
      mirrorFrom: 0,
      mirrorTo: 0,
      mirrorStarted: 0,
      mirrorDuration: DEFAULT_TRACKING.mirrorDuration,
      mirrorProgress: 0,
      pointerAt: -Infinity,
      nextLook: 0,
    };
    const e = engine.current;
    // Reduced motion: a still pose, no loop at all.
    if (reduced) return;
    let raf = 0;
    const tick = (now: number) => {
      const dt = Math.min(0.06, e.last ? (now - e.last) / 1000 : 0);
      e.last = now;
      if (!paused) e.time += dt * cfg.motion.speed;
      e.shown = transitionFace(cfg, e.from, now - e.transitionStart);
      if (lookAround && now >= e.nextLook && now - e.pointerAt > POINTER_REST_MS) {
        // Glance somewhere, or back at the viewer about a third of the time, then hold it.
        const center = Math.random() < 0.35;
        e.targetX = center ? 0 : (Math.random() * 2 - 1) * 0.7;
        e.targetY = center ? 0 : (Math.random() * 2 - 1) * 0.4;
        e.nextLook = now + 1400 + Math.random() * 2600;
      }
      const smoothing = clamp(DEFAULT_TRACKING.smoothing, 0.001, 1);
      e.gazeX += (e.targetX - e.gazeX) * smoothing;
      e.gazeY += (e.targetY - e.gazeY) * smoothing;
      if (e.mirrorProgress !== e.mirrorTo) {
        const raw = clamp((now - e.mirrorStarted) / Math.max(1, e.mirrorDuration), 0, 1);
        e.mirrorProgress = lerp(e.mirrorFrom, e.mirrorTo, ease('easeInOutCubic', raw));
        if (raw >= 1) e.mirrorProgress = e.mirrorTo;
      }
      setSnap({
        time: e.time,
        face: e.shown,
        gaze: { x: e.gazeX, y: e.gazeY },
        mirror: e.mirrorProgress,
      });
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [cfg, paused, reduced, lookAround]);

  // Fleibo gaze: pointer position normalized against the whole viewport around the pet's center.
  useEffect(() => {
    if (Platform.OS !== 'web' || !trackPointer) return;
    const onMove = (event: PointerEvent) => {
      const e = engine.current;
      const node = host.current as unknown as HTMLElement | null;
      if (!e || !node) return;
      const rect = node.getBoundingClientRect();
      aim(e, event.clientX, event.clientY, rect, window.innerWidth, window.innerHeight);
    };
    window.addEventListener('pointermove', onMove, { passive: true });
    return () => window.removeEventListener('pointermove', onMove);
  }, [trackPointer]);

  // The same gaze toward a given point (native and web), measured from where the Pet is now.
  const lookX = lookAt?.x;
  const lookY = lookAt?.y;
  useEffect(() => {
    if (lookX === undefined || lookY === undefined) return;
    const node = host.current;
    if (!node) return;
    const view = Dimensions.get('window');
    node.measureInWindow((left, top, width, height) => {
      const e = engine.current;
      if (e) aim(e, lookX, lookY, { left, top, width, height }, view.width, view.height);
    });
  }, [lookX, lookY]);

  const frame = petFrame(cfg, {
    time: snap.time,
    face: reduced ? cfg.poses[cfg.emotion] : snap.face,
    blink: paused ? 1 : blinkAt(snap.time, cfg.motion.blinkInterval),
    gaze: snap.gaze,
    mirror: snap.mirror,
    reduced,
  });
  const v = crop;
  return (
    <View
      ref={host}
      style={[{ width: size, aspectRatio: v.width / v.height }, style]}
      accessibilityRole="image"
      accessibilityLabel={PET_NAME}
    >
      <PetVaporCanvas
        config={cfg}
        frame={frame}
        fill={fill}
        shade={shade}
        prefix={prefix}
        viewBox={v}
        width={size}
        height={(size * v.height) / v.width}
      />
    </View>
  );
}

/** Points the engine's gaze at (px, py), normalized against the viewport around the Pet's box. */
function aim(
  e: Engine,
  px: number,
  py: number,
  box: { left: number; top: number; width: number; height: number },
  viewWidth: number,
  viewHeight: number,
) {
  e.pointerAt = performance.now();
  const cx = box.left + box.width / 2;
  const cy = box.top + box.height / 2;
  const spanX = px < cx ? Math.max(1, cx) : Math.max(1, viewWidth - cx);
  const spanY = py < cy ? Math.max(1, cy) : Math.max(1, viewHeight - cy);
  const rawX = clamp((px - cx) / spanX, -1, 1);
  const rawY = clamp((py - cy) / spanY, -1, 1);
  const enter = !e.mirrored && rawX <= -Math.abs(DEFAULT_TRACKING.mirrorEnter);
  const exit = e.mirrored && rawX >= -Math.abs(DEFAULT_TRACKING.mirrorExit);
  if (DEFAULT_TRACKING.mirrorEnabled && (enter || exit)) {
    e.mirrored = enter;
    e.mirrorFrom = e.mirrorProgress;
    e.mirrorTo = enter ? 1 : 0;
    e.mirrorStarted = performance.now();
    e.mirrorDuration = Math.max(
      80,
      DEFAULT_TRACKING.mirrorDuration * Math.abs(e.mirrorTo - e.mirrorFrom),
    );
  }
  const deadzone = clamp(DEFAULT_TRACKING.deadzone, 0, 0.95);
  e.targetX = applyDeadzone(rawX, deadzone);
  e.targetY = applyDeadzone(rawY, deadzone);
}
