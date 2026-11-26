/**
 * Pet: the app's mist-spirit mascot. Pure geometry and preset, no React and no DOM.
 *
 * Ported verbatim from the RuizAvatar v3.3 drop-in (adapted from Cruz1122/fleibo-face,
 * https://github.com/Cruz1122/fleibo-face). Only exported names changed (Ruiz -> Pet) and the
 * preset starts at rest instead of mid-speech. The upstream DOM mount (innerHTML, window
 * listeners) is replaced by `petFrame` + PetVaporFigure (SVG) or drawPet (Skia) so the same drawing runs on Android, iOS and web.
 */
import { brand } from '../theme/tokens';

export type EasingName = 'linear' | 'easeInOutCubic' | 'easeOutCubic';
export interface FaceState {
  faceX: number;
  faceY: number;
  faceWidth: number;
  faceHeight: number;
  faceRadius: number;
  faceRotation: number;
  leftEyeX: number;
  leftEyeY: number;
  leftEyeWidth: number;
  leftEyeHeight: number;
  leftEyeRadius: number;
  leftEyeRotation: number;
  rightEyeX: number;
  rightEyeY: number;
  rightEyeWidth: number;
  rightEyeHeight: number;
  rightEyeRadius: number;
  rightEyeRotation: number;
  mouthX: number;
  mouthY: number;
  mouthWidth: number;
  mouthCurve: number;
  mouthLeftOffset: number;
  mouthRightOffset: number;
  mouthControlSpread: number;
  mouthStroke: number;
  mouthRotation: number;
}
export interface TrackingConfig {
  enabled: boolean;
  mirrorEnabled: boolean;
  maxMoveX: number;
  maxMoveY: number;
  eyeVerticalBoost: number;
  smoothing: number;
  deadzone: number;
  mirrorEnter: number;
  mirrorExit: number;
  mirrorDuration: number;
}
export const DEFAULT_TRACKING: TrackingConfig = {
  enabled: true,
  mirrorEnabled: true,
  maxMoveX: 6,
  maxMoveY: 4,
  eyeVerticalBoost: 3,
  smoothing: 0.1,
  deadzone: 0.07,
  mirrorEnter: 0.38,
  mirrorExit: 0.1,
  mirrorDuration: 520,
};
export const clamp = (n: number, a: number, b: number) => Math.min(b, Math.max(a, n));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export function ease(name: EasingName, t: number) {
  const x = clamp(t, 0, 1);
  switch (name) {
    case 'linear':
      return x;
    case 'easeOutCubic':
      return 1 - (1 - x) ** 3;
    default:
      return x < 0.5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2;
  }
}
export function formatNumber(value: number) {
  if (!Number.isFinite(value)) return '0';
  return Number.isInteger(value)
    ? String(value)
    : value.toFixed(4).replace(/0+$/, '').replace(/\.$/, '');
}
export function roundedRectPath(
  cx: number,
  cy: number,
  width: number,
  height: number,
  radius: number,
) {
  const w = Math.max(0.001, Math.abs(width)),
    h = Math.max(0.001, Math.abs(height));
  const r = clamp(Math.abs(radius), 0, Math.min(w / 2, h / 2));
  const x = cx - w / 2,
    y = cy - h / 2,
    x2 = x + w,
    y2 = y + h;
  if (!r) return `M ${x} ${y} H ${x2} V ${y2} H ${x} Z`;
  return `M ${formatNumber(x + r)} ${formatNumber(y)} H ${formatNumber(x2 - r)} A ${r} ${r} 0 0 1 ${x2} ${y + r} V ${y2 - r} A ${r} ${r} 0 0 1 ${x2 - r} ${y2} H ${x + r} A ${r} ${r} 0 0 1 ${x} ${y2 - r} V ${y + r} A ${r} ${r} 0 0 1 ${x + r} ${y} Z`;
}
export const rotationTransform = (a: number, x: number, y: number) =>
  `rotate(${formatNumber(a)} ${formatNumber(x)} ${formatNumber(y)})`;
export function mouthPath(s: FaceState) {
  const half = s.mouthWidth / 2,
    x1 = s.mouthX - half,
    x2 = s.mouthX + half,
    leftY = s.mouthY + s.mouthLeftOffset,
    rightY = s.mouthY + s.mouthRightOffset,
    spread = s.mouthWidth * s.mouthControlSpread;
  return `M ${formatNumber(x1)} ${formatNumber(leftY)} C ${formatNumber(x1 + spread)} ${formatNumber(leftY + s.mouthCurve)} ${formatNumber(x2 - spread)} ${formatNumber(rightY + s.mouthCurve)} ${formatNumber(x2)} ${formatNumber(rightY)}`;
}
export function interpolateFaceState(from: FaceState, to: FaceState, t: number): FaceState {
  const out = {} as FaceState;
  for (const key of FACE_STATE_KEYS) out[key] = lerp(from[key], to[key], t) as never;
  return out;
}
export const applyDeadzone = (v: number, d: number) =>
  Math.abs(v) <= d ? 0 : Math.sign(v) * clamp((Math.abs(v) - d) / Math.max(0.0001, 1 - d), 0, 1);
export const VOICE_STATES = ['idle', 'listening', 'thinking', 'speaking'] as const;
export const PET_EMOTIONS = [
  'idle',
  'happy',
  'curious',
  'surprised',
  'thinking',
  'listening',
  'speaking',
  'sleepy',
  'sad',
  'excited',
  'default-happy',
  'intimidated',
  'angry',
] as const;
export type PetEmotion = (typeof PET_EMOTIONS)[number];
export type EyeShape = 'oval' | 'dot' | 'arc' | 'half' | 'closed';
export type MouthShape = 'smile' | 'neutral' | 'open' | 'surprise' | 'sad';
export type VoiceState = (typeof VOICE_STATES)[number];
export interface PetConfig {
  version: 2;
  emotion: PetEmotion;
  poses: Record<PetEmotion, FaceState>;
  body: {
    x: number;
    y: number;
    width: number;
    height: number;
    scaleX: number;
    scaleY: number;
    rotation: number;
    tailLength: number;
    tailCurl: number;
    tailMotion: number;
    tailSpeed: number;
    asymmetry: number;
    sideCurve: number;
    softness: number;
    opacity: number;
    volume: number;
    noise: number;
    noiseSpeed: number;
    outline: number;
    color: string;
    shadowColor: string;
    highlightColor: string;
  };
  eyes: {
    leftShape: EyeShape;
    rightShape: EyeShape;
    sync: boolean;
    leftOpen: number;
    rightOpen: number;
    color: string;
  };
  mouth: { shape: MouthShape; open: number; control1: number; control2: number };
  smoke: {
    count: number;
    length: number;
    width: number;
    originX: number;
    originY: number;
    direction: number;
    curve: number;
    speed: number;
    sway: number;
    turbulence: number;
    opacity: number;
    blur: number;
    spread: number;
    motion: number;
    offsets: { x: number; y: number }[];
  };
  motion: {
    enabled: boolean;
    duration: number;
    breathing: number;
    floating: number;
    blinkInterval: number;
    tracking: number;
    transition: number;
    easing: EasingName;
    speechReaction: number;
    speed: number;
    reducedEffects: boolean;
  };
  voice: VoiceState;
  audio: number;
  /** Something the Pet wears on its head (the group roles); none by default. */
  accessory?: PetAccessory;
  /** The accessory's colors; its own default when absent. */
  accessoryTint?: PetTint;
}
export const PET_PRESET: PetConfig = {
  version: 2,
  emotion: 'idle',
  poses: {
    idle: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12.347119569778442,
      leftEyeY: -17.077198028564453,
      leftEyeWidth: 12,
      leftEyeHeight: 19,
      leftEyeRadius: 8,
      leftEyeRotation: -3,
      rightEyeX: 51,
      rightEyeY: -27,
      rightEyeWidth: 12,
      rightEyeHeight: 19,
      rightEyeRadius: 8,
      rightEyeRotation: 3,
      mouthX: 20,
      mouthY: 17,
      mouthWidth: 29,
      mouthCurve: 9,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 0,
    },
    happy: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -25,
      leftEyeWidth: 12,
      leftEyeHeight: 16,
      leftEyeRadius: 8,
      leftEyeRotation: -3,
      rightEyeX: 52,
      rightEyeY: -25,
      rightEyeWidth: 12,
      rightEyeHeight: 16,
      rightEyeRadius: 8,
      rightEyeRotation: 3,
      mouthX: 20,
      mouthY: 14,
      mouthWidth: 44,
      mouthCurve: 20,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 0,
    },
    curious: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -29,
      leftEyeWidth: 12,
      leftEyeHeight: 19,
      leftEyeRadius: 8,
      leftEyeRotation: -10,
      rightEyeX: 52,
      rightEyeY: -23,
      rightEyeWidth: 12,
      rightEyeHeight: 19,
      rightEyeRadius: 8,
      rightEyeRotation: 5,
      mouthX: 20,
      mouthY: 17,
      mouthWidth: 23,
      mouthCurve: 4,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 8,
    },
    surprised: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -25,
      leftEyeWidth: 15,
      leftEyeHeight: 23,
      leftEyeRadius: 8,
      leftEyeRotation: -3,
      rightEyeX: 52,
      rightEyeY: -25,
      rightEyeWidth: 15,
      rightEyeHeight: 23,
      rightEyeRadius: 8,
      rightEyeRotation: 3,
      mouthX: 20,
      mouthY: 17,
      mouthWidth: 16,
      mouthCurve: 0,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 0,
    },
    thinking: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -25,
      leftEyeWidth: 12,
      leftEyeHeight: 13,
      leftEyeRadius: 8,
      leftEyeRotation: -3,
      rightEyeX: 52,
      rightEyeY: -30,
      rightEyeWidth: 12,
      rightEyeHeight: 19,
      rightEyeRadius: 8,
      rightEyeRotation: -15,
      mouthX: 20,
      mouthY: 23,
      mouthWidth: 23,
      mouthCurve: -2,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: -8,
    },
    listening: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -25,
      leftEyeWidth: 12,
      leftEyeHeight: 21,
      leftEyeRadius: 8,
      leftEyeRotation: -3,
      rightEyeX: 52,
      rightEyeY: -25,
      rightEyeWidth: 12,
      rightEyeHeight: 21,
      rightEyeRadius: 8,
      rightEyeRotation: 3,
      mouthX: 20,
      mouthY: 20,
      mouthWidth: 21,
      mouthCurve: 7,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 0,
    },
    speaking: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -25,
      leftEyeWidth: 12,
      leftEyeHeight: 18,
      leftEyeRadius: 8,
      leftEyeRotation: -3,
      rightEyeX: 52,
      rightEyeY: -25,
      rightEyeWidth: 12,
      rightEyeHeight: 18,
      rightEyeRadius: 8,
      rightEyeRotation: 3,
      mouthX: 20,
      mouthY: 19,
      mouthWidth: 21,
      mouthCurve: 0,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 0,
    },
    sleepy: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -25,
      leftEyeWidth: 12,
      leftEyeHeight: 5,
      leftEyeRadius: 8,
      leftEyeRotation: -3,
      rightEyeX: 52,
      rightEyeY: -25,
      rightEyeWidth: 12,
      rightEyeHeight: 5,
      rightEyeRadius: 8,
      rightEyeRotation: 3,
      mouthX: 20,
      mouthY: 19,
      mouthWidth: 28,
      mouthCurve: 5,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 0,
    },
    sad: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -23,
      leftEyeWidth: 12,
      leftEyeHeight: 19,
      leftEyeRadius: 8,
      leftEyeRotation: -3,
      rightEyeX: 52,
      rightEyeY: -23,
      rightEyeWidth: 12,
      rightEyeHeight: 19,
      rightEyeRadius: 8,
      rightEyeRotation: 3,
      mouthX: 20,
      mouthY: 34,
      mouthWidth: 35,
      mouthCurve: -13,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 0,
    },
    excited: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -25,
      leftEyeWidth: 12,
      leftEyeHeight: 15,
      leftEyeRadius: 8,
      leftEyeRotation: -3,
      rightEyeX: 52,
      rightEyeY: -25,
      rightEyeWidth: 12,
      rightEyeHeight: 15,
      rightEyeRadius: 8,
      rightEyeRotation: 3,
      mouthX: 20,
      mouthY: 9,
      mouthWidth: 53,
      mouthCurve: 24,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 0,
    },
    'default-happy': {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -25,
      leftEyeWidth: 12,
      leftEyeHeight: 19,
      leftEyeRadius: 8,
      leftEyeRotation: -3,
      rightEyeX: 52,
      rightEyeY: -25,
      rightEyeWidth: 12,
      rightEyeHeight: 19,
      rightEyeRadius: 8,
      rightEyeRotation: 3,
      mouthX: 20,
      mouthY: 17,
      mouthWidth: 44,
      mouthCurve: 20,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 0,
    },
    intimidated: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -25,
      leftEyeWidth: 12,
      leftEyeHeight: 9,
      leftEyeRadius: 8,
      leftEyeRotation: -3,
      rightEyeX: 52,
      rightEyeY: -25,
      rightEyeWidth: 12,
      rightEyeHeight: 9,
      rightEyeRadius: 8,
      rightEyeRotation: 3,
      mouthX: 20,
      mouthY: 17,
      mouthWidth: 18,
      mouthCurve: 2,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 0,
    },
    angry: {
      faceX: 0,
      faceY: 0,
      faceWidth: 200,
      faceHeight: 200,
      faceRadius: 100,
      faceRotation: 0,
      leftEyeX: -12,
      leftEyeY: -25,
      leftEyeWidth: 12,
      leftEyeHeight: 19,
      leftEyeRadius: 8,
      leftEyeRotation: -46,
      rightEyeX: 52,
      rightEyeY: -25,
      rightEyeWidth: 12,
      rightEyeHeight: 19,
      rightEyeRadius: 8,
      rightEyeRotation: 46,
      mouthX: 20,
      mouthY: 28,
      mouthWidth: 27,
      mouthCurve: -12,
      mouthLeftOffset: 0,
      mouthRightOffset: 0,
      mouthControlSpread: 0.29,
      mouthStroke: 5,
      mouthRotation: 0,
    },
  },
  body: {
    x: -32,
    y: -8.91,
    width: 206,
    height: 202,
    scaleX: 1,
    scaleY: 1,
    rotation: -1,
    tailLength: 112,
    tailCurl: 80,
    tailMotion: 1.3,
    tailSpeed: 1.15,
    asymmetry: 33,
    sideCurve: 23,
    softness: 12,
    opacity: 0.97,
    volume: 0.93,
    noise: 0.55,
    outline: 0.4,
    color: '#f8fcff',
    shadowColor: '#b5c7ed',
    highlightColor: '#ffffff',
    noiseSpeed: 2.1,
  },
  eyes: {
    leftShape: 'oval',
    rightShape: 'oval',
    sync: false,
    leftOpen: 1,
    rightOpen: 1,
    color: '#23314d',
  },
  mouth: { shape: 'smile', open: 0, control1: 0.29, control2: 0.29 },
  smoke: {
    count: 20,
    length: 36,
    width: 19,
    originX: -25,
    originY: -15,
    direction: 52,
    curve: 84,
    speed: 1.95,
    sway: 40,
    turbulence: 0.93,
    opacity: 0.37,
    blur: 9,
    spread: 0,
    motion: 1.14,
    offsets: [
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
      { x: 0, y: 0 },
    ],
  },
  motion: {
    enabled: true,
    duration: 7.2,
    breathing: 1.6,
    floating: 5.5,
    blinkInterval: 4.2,
    tracking: 1,
    transition: 360,
    easing: 'easeInOutCubic',
    speechReaction: 0.9,
    speed: 1,
    reducedEffects: false,
  },
  voice: 'idle',
  audio: 0,
};
export const copyConfig = (c: PetConfig): PetConfig => JSON.parse(JSON.stringify(c)) as PetConfig;
const n = (v: number) => Math.round(v * 100) / 100;
const safeColor = (s: string) => (/^#[0-9a-fA-F]{6}$/.test(s) ? s : '#ffffff');
export function bodyPath(config: PetConfig, t = 0): string {
  const b = config.body,
    cx = b.x + b.asymmetry * 0.07,
    cy = b.y - 4;
  const rx = Math.max(30, b.width * b.scaleX * 0.5),
    ry = Math.max(30, b.height * b.scaleY * 0.5);
  const Point = (x: number, y: number) => ({ x, y });
  type Point2 = ReturnType<typeof Point>;
  const points: Point2[] = [];
  const intensity = clamp(b.noise, 0, 2);
  const speed = Math.max(0, b.noiseSpeed ?? 0.95);
  const waveTime = t * speed;
  const leftAngle = 2.0,
    rightAngle = Math.PI * 2 + 1.14;
  const wrap = (angle: number) => ((angle % (Math.PI * 2)) + Math.PI * 2) % (Math.PI * 2);
  const arcDist = (a: number, b: number) => Math.atan2(Math.sin(a - b), Math.cos(a - b));
  const packets = (angle: number, time: number) => {
    const a = wrap(0.55 + time * 0.32),
      d1 = arcDist(angle, a);
    const b2 = wrap(3.85 + time * 0.23),
      d2 = arcDist(angle, b2);
    const c = wrap(5.75 - time * 0.18),
      d3 = arcDist(angle, c);
    return (
      1.12 * Math.exp((-d1 * d1) / (2 * 0.33 * 0.33)) -
      0.78 * Math.exp((-d2 * d2) / (2 * 0.43 * 0.43)) +
      0.66 * Math.exp((-d3 * d3) / (2 * 0.29 * 0.29))
    );
  };
  const samples = 54;
  for (let i = 0; i <= samples; i++) {
    const u = i / samples,
      angle = leftAngle + (rightAngle - leftAngle) * u;
    // Apply a smooth edge fade only at the root of the tail, not on the head.
    const edgeFade = Math.min(1, u * 13, (1 - u) * 13);
    const window = edgeFade * edgeFade * (3 - 2 * edgeFade);
    const traveling =
      0.47 * Math.sin(4 * angle - waveTime * 0.82 + 1.0) +
      0.35 * Math.sin(7 * angle - waveTime * 1.31 - 0.45) +
      0.18 * Math.sin(11 * angle + waveTime * 0.63 + 2.1) +
      0.43 * packets(angle, waveTime);
    const radiusDelta = (3.3 + 6.6 * intensity) * intensity * 0.65 * traveling * window;
    // A few-pixel breathing ripple at all angles, independent from the tail.
    const x = cx + (rx + radiusDelta) * Math.cos(angle) + b.sideCurve * 0.075 * Math.sin(angle * 2);
    const y = cy + (ry + radiusDelta) * Math.sin(angle);
    points.push(Point(x, y));
  }
  const leftRoot = points[0],
    rightRoot = points[points.length - 1];
  const rootX = (leftRoot.x + rightRoot.x) * 0.5;
  const rootY = (leftRoot.y + rightRoot.y) * 0.5;
  const rootHalf = Math.max(8, (rightRoot.x - leftRoot.x) * 0.5);
  const rootLength = Math.max(16, b.tailLength);
  const endY = rootY + rootLength * 0.9 + 12;
  const tailStrength = clamp(b.tailMotion ?? 1.3, 0, 3);
  const tailSpeed = Math.max(0, b.tailSpeed ?? 1.15);
  const flameT = t * tailSpeed;
  const tipOffset =
    (Math.sin(flameT * 1.5 + 1.1) + 0.37 * Math.sin(flameT * 3.2 + 0.25)) * tailStrength * 10;
  const waveX = (u: number) => {
    const fade = u * u * (3 - 2 * u);
    // The parameters at u=0 are exactly zero: the head remains attached.
    const trail =
      (Math.sin(flameT * 1.7 - u * 2.75) - Math.sin(flameT * 1.7)) * tailStrength * 11 * u * u;
    const secondary =
      (Math.sin(flameT * 3.1 - u * 5.2 + 0.5) - Math.sin(flameT * 3.1 + 0.5)) *
      tailStrength *
      3.6 *
      u *
      u;
    return b.tailCurl * 0.57 * fade + tipOffset * fade + trail + secondary;
  };
  const centerX = (u: number) => rootX + waveX(u);
  const centerY = (u: number) =>
    rootY + (endY - rootY) * u + Math.sin(flameT * 2.0 - u * 3.8) * tailStrength * 2.4 * u * u;
  const halfWidth = (u: number) =>
    rootHalf *
    Math.pow(1 - u, 1.22) *
    (1 + 0.13 * tailStrength * Math.sin(flameT * 2.4 - u * 4.3) * u);
  // Right half of the flame, from the lower cheek to the moving tip.
  const tailSamples = 17;
  for (let i = 1; i <= tailSamples; i++) {
    const u = i / tailSamples;
    points.push(Point(centerX(u) + halfWidth(u), centerY(u)));
  }
  // Left half of the flame, travelling back toward the left cheek.
  for (let i = tailSamples - 1; i > 0; i--) {
    const u = i / tailSamples;
    points.push(Point(centerX(u) - halfWidth(u), centerY(u)));
  }
  // The final left root is the first point; closing below preserves continuity.
  const count = points.length;
  let path = `M ${n(points[0].x)} ${n(points[0].y)}`;
  for (let i = 0; i < count; i++) {
    const before = points[(i + count - 1) % count],
      a = points[i],
      b2 = points[(i + 1) % count],
      after = points[(i + 2) % count];
    // Uniform point count and cubic interpolation prevent path snapping.
    const c1x = a.x + (b2.x - before.x) / 6,
      c1y = a.y + (b2.y - before.y) / 6;
    const c2x = b2.x - (after.x - a.x) / 6,
      c2y = b2.y - (after.y - a.y) / 6;
    path += ` C ${n(c1x)} ${n(c1y)} ${n(c2x)} ${n(c2y)} ${n(b2.x)} ${n(b2.y)}`;
  }
  return path + ' Z';
}
export function volumePath(c: PetConfig): string {
  const b = c.body,
    x = b.x,
    y = b.y,
    w = (b.width * b.scaleX) / 2,
    h = (b.height * b.scaleY) / 2,
    noise = Math.max(0, b.noise) * 0.7;
  const sw1 = 1.1 * noise,
    sw2 = -0.75 * noise; // Stable volume geometry.
  return `M ${n(x - w * 0.72 - sw1 * 0.16)} ${n(y - 20 - sw2 * 0.2)} C ${n(x - w * 0.77 - sw1 * 0.22)} ${n(y - h * 0.8 - sw2 * 0.3)} ${n(x - w * 0.28)} ${n(y - h * 0.93 - sw1 * 0.25)} ${n(x + 13 + sw2 * 0.5)} ${n(y - h * 0.85 - sw1 * 0.2)} C ${n(x + w * 0.76 + sw1 * 0.18)} ${n(y - h * 0.8 - sw2 * 0.18)} ${n(x + w * 0.75 + sw2 * 0.2)} ${n(y + 18 + sw1 * 0.3)} ${n(x + w * 0.47 + sw1 * 0.12)} ${n(y + 58 + sw2 * 0.3)} C ${n(x + w * 0.1 + sw2 * 0.2)} ${n(y + 87 + sw1 * 0.15)} ${n(x - w * 0.48 - sw1 * 0.12)} ${n(y + 62 + sw2 * 0.18)} ${n(x - w * 0.72 - sw1 * 0.16)} ${n(y - 20 - sw2 * 0.2)} Z`;
}
export function filamentPath(c: PetConfig, index: number, t = 0): string {
  const s = c.smoke,
    count = Math.max(1, Math.round(s.count)),
    side = index % 2 === 0 ? -1 : 1;
  const lane = Math.floor(index / 2),
    ratio = (lane + 1) / (Math.ceil(count / 2) + 1);
  const speed = Math.max(0, s.speed) * Math.max(0.1, s.motion);
  const flow = t * speed * 0.44,
    phase = index * 1.33 + flow;
  const turbulence = Math.max(0, s.turbulence);
  const orbit = flow * 0.55 + index * 1.75;
  const driftX = Math.cos(orbit) * turbulence * 3.6;
  const driftY = Math.sin(orbit) * turbulence * 3.0;
  const osc = Math.sin(phase) * s.sway * s.motion;
  const jitter =
    (Math.sin(phase * 1.37 + index * 0.7) + 0.35 * Math.sin(flow * 0.83 - index * 2.1)) *
    turbulence *
    8;
  const offset = s.offsets?.[index] || { x: 0, y: 0 };
  const rootBase = c.body.width * (0.16 + 0.08 * ratio),
    rootSpread = s.spread * (0.14 + 0.13 * ratio);
  const ox = c.body.x + side * (rootBase + rootSpread) + s.originX + offset.x + driftX;
  const oy = c.body.y + s.originY + lane * 4 + offset.y + driftY;
  const length = s.length * (0.72 + (index % 3) * 0.11),
    bend = side * s.curve * (0.75 + 0.12 * ratio);
  const neckX = ox + side * (8 + rootSpread * 0.12) + osc * 0.06;
  const neckY = oy - length * 0.18;
  const x2 = ox + side * (14 + length * 0.21) + s.direction * 0.45 + osc * 0.28 + jitter;
  const y2 = oy - length + Math.cos(flow + index * 0.44) * turbulence * 2.7;
  return `M ${n(ox)} ${n(oy)} C ${n(neckX + bend * 0.1)} ${n(neckY)} ${n(ox + bend * 0.52 + osc * 0.26)} ${n(oy - length * 0.46)} ${n(x2 - bend * 0.4)} ${n(oy - length * 0.78)} S ${n(x2 + side * (3 + jitter * 0.15))} ${n(y2 + length * 0.06)} ${n(x2)} ${n(y2)}`;
}
interface MirrorEye {
  x: number;
  y: number;
  width: number;
  height: number;
  radius: number;
  rotation: number;
}
function eyePose(side: 'left' | 'right', state: FaceState): MirrorEye {
  const prefix = side === 'left' ? 'leftEye' : 'rightEye';
  return {
    x: state[`${prefix}X`],
    y: state[`${prefix}Y`],
    width: state[`${prefix}Width`],
    height: state[`${prefix}Height`],
    radius: state[`${prefix}Radius`],
    rotation: state[`${prefix}Rotation`],
  };
}
function mirroredEyeTarget(counterpart: MirrorEye, state: FaceState): MirrorEye {
  return {
    x: 2 * state.faceX - counterpart.x,
    y: counterpart.y,
    width: counterpart.width,
    height: counterpart.height,
    radius: counterpart.radius,
    rotation: -counterpart.rotation,
  };
}
function interpolateEye(from: MirrorEye, to: MirrorEye, t: number): MirrorEye {
  return {
    x: lerp(from.x, to.x, t),
    y: lerp(from.y, to.y, t),
    width: lerp(from.width, to.width, t),
    height: lerp(from.height, to.height, t),
    radius: lerp(from.radius, to.radius, t),
    rotation: lerp(from.rotation, to.rotation, t),
  };
}
export function eyePath(
  s: FaceState,
  side: 'left' | 'right',
  shape: EyeShape,
  openFactor: number,
): string {
  const key = side === 'left' ? 'leftEye' : 'rightEye';
  const x = s[`${key}X`],
    y = s[`${key}Y`],
    w = Math.max(2, s[`${key}Width`]),
    h = Math.max(1, s[`${key}Height`] * openFactor),
    radius = s[`${key}Radius`];
  if (shape === 'closed' || shape === 'arc')
    return `M ${n(x - w * 0.65)} ${n(y)} Q ${n(x)} ${n(y + (shape === 'arc' ? -h : h) * 0.85)} ${n(x + w * 0.65)} ${n(y)}`;
  if (shape === 'half')
    return roundedRectPath(x, y, w, Math.max(2, h * 0.33), Math.min(radius, h * 0.16));
  if (shape === 'dot') return roundedRectPath(x, y, w * 0.83, w * 0.83, w / 2);
  return roundedRectPath(x, y, w, h, radius);
}
export function mouthDrawPath(
  s: FaceState,
  shape: MouthShape,
  open: number,
  a: number,
  b: number,
): string {
  if (shape === 'surprise' || shape === 'open' || open > 0.1) {
    const w = Math.max(6, s.mouthWidth * (shape === 'surprise' ? 0.66 : 0.83));
    const h = Math.max(5, 7 + open * 20 + (shape === 'surprise' ? 7 : 0));
    return `M ${n(s.mouthX - w / 2)} ${n(s.mouthY)} C ${n(s.mouthX - w / 2)} ${n(s.mouthY - h * 0.54)} ${n(s.mouthX + w / 2)} ${n(s.mouthY - h * 0.54)} ${n(s.mouthX + w / 2)} ${n(s.mouthY)} C ${n(s.mouthX + w / 2)} ${n(s.mouthY + h)} ${n(s.mouthX - w / 2)} ${n(s.mouthY + h)} ${n(s.mouthX - w / 2)} ${n(s.mouthY)} Z`;
  }
  const curve = shape === 'sad' ? -Math.abs(s.mouthCurve) : shape === 'neutral' ? 0 : s.mouthCurve;
  // Preserve Fleibo's exact Bézier generator when the two control points agree.
  if (Math.abs(a - b) < 0.0001)
    return mouthPath({ ...s, mouthCurve: curve, mouthControlSpread: a });
  const half = s.mouthWidth / 2,
    x1 = s.mouthX - half,
    x2 = s.mouthX + half;
  return `M ${n(x1)} ${n(s.mouthY + s.mouthLeftOffset)} C ${n(x1 + s.mouthWidth * a)} ${n(s.mouthY + curve)} ${n(x2 - s.mouthWidth * b)} ${n(s.mouthY + curve)} ${n(x2)} ${n(s.mouthY + s.mouthRightOffset)}`;
}
export function speakingMouthPath(s: FaceState, amplitude: number, t: number): string {
  const talk = clamp(amplitude, 0, 1.4),
    vowel = (Math.sin(t * 10.6) + 1) / 2,
    smile = (Math.sin(t * 5.1 + 0.9) + 1) / 2;
  const w = Math.max(10, s.mouthWidth * (0.78 + vowel * 0.32 + talk * 0.18));
  const h = Math.max(4, 4.5 + talk * 19 + Math.sin(t * 13.4) * talk * 2.8);
  const y = s.mouthY + Math.sin(t * 8.8) * talk * 1.8;
  const x1 = s.mouthX - w / 2,
    x2 = s.mouthX + w / 2;
  const skew = Math.sin(t * 7.7 + 0.35) * talk * 4.2;
  const pinch = Math.cos(t * 9.2 + 0.4) * talk * 0.12;
  const topY = y - h * (0.5 + 0.18 * vowel) - smile * talk * 1.2;
  const bottomY = y + h * (0.76 + 0.1 * (1 - vowel)) + smile * talk * 1.5;
  const c1x = x1 + w * (0.17 + pinch),
    c2x = x2 - w * (0.17 - pinch);
  return `M ${n(x1)} ${n(y - skew * 0.08)} C ${n(x1)} ${n(topY)} ${n(x2)} ${n(topY - skew * 0.16)} ${n(x2)} ${n(y + skew * 0.08)} C ${n(c2x)} ${n(bottomY)} ${n(c1x)} ${n(bottomY + skew * 0.22)} ${n(x1)} ${n(y - skew * 0.08)} Z`;
}

/** The character's display name; one place, because the name is provisional. */
export const PET_NAME = 'Pet';
/** viewBox of a standalone Pet, from the upstream renderer. */
export const PET_VIEWBOX = { x: -162, y: -147, width: 324, height: 357 } as const;
export const FACE_STATE_KEYS = Object.keys(PET_PRESET.poses.idle) as (keyof FaceState)[];

const BLINK_SECONDS = 0.17;
const hash01 = (k: number) => {
  const s = Math.sin(k * 12.9898 + 78.233) * 43758.5453;
  return s - Math.floor(s);
};

/**
 * Eye openness (1 = open) at `time`. Deterministic, so a host that only knows the clock (the
 * onboarding scene) blinks the same way on every render; one blink per interval at a jittered offset.
 */
export function blinkAt(time: number, interval: number): number {
  const period = Math.max(0.8, interval);
  const k = Math.floor(time / period);
  const elapsed = time - (k + 0.15 + 0.6 * hash01(k)) * period;
  if (elapsed < 0 || elapsed >= BLINK_SECONDS) return 1;
  return Math.max(0.045, Math.abs((elapsed / BLINK_SECONDS) * 2 - 1));
}

export interface PetFrameInput {
  /** Procedural seconds (mist, tail, smoke, speech); frozen when motion is off. */
  time: number;
  /** Face pose being shown (mid-transition poses are interpolated by the host). */
  face: FaceState;
  /** Eye openness multiplier from blinkAt; 1 = open. */
  blink: number;
  /** Smoothed gaze in -1..1 (pointer tracking); 0 = straight ahead. */
  gaze?: { x: number; y: number };
  /** 0..1 progress of the Fleibo mirror (the pet turning to look left). */
  mirror?: number;
  /** Reduced motion or effects: no procedural motion and light blur. */
  reduced?: boolean;
}

export interface PetStroke {
  d: string;
  transform: string;
  color: string;
  width: number;
  filled: boolean;
}

/** A soft round puff (radial gradient) used by the vapor look. */
export interface PetPuff {
  x: number;
  y: number;
  r: number;
  opacity: number;
}

/**
 * Vapor look: puffs that blur the Pet's outline the way the volcano's steam is drawn. Rim puffs
 * drift slowly around the head; tail puffs climb from the tip to the head and loop, so the vapor
 * seems to feed the Pet. Pure function of time, so it loops seamlessly.
 */
export function petVaporPuffs(cfg: PetConfig, time: number, mirror = 0): PetPuff[] {
  const b = cfg.body;
  const x = lerp(b.x, -b.x, mirror);
  const cx = x + lerp(b.asymmetry, -b.asymmetry, mirror) * 0.07;
  const cy = b.y - 4;
  const rx = Math.max(30, b.width * b.scaleX * 0.5);
  const ry = Math.max(30, b.height * b.scaleY * 0.5);
  const puffs: PetPuff[] = [];
  const rim = 14;
  for (let i = 0; i < rim; i++) {
    const a = (i / rim) * Math.PI * 2 + time * 0.12;
    // 1 at the bottom of the head (SVG y grows down), where the tail takes over.
    const bottom = Math.max(0, Math.sin(a));
    const k = hash01(i + 3);
    // Billows breathe out of phase, so the outline keeps changing like a real plume.
    const breathe = 1 + 0.08 * Math.sin(time * 0.9 + i * 2.3);
    // Centred just inside the outline: drawn behind the body, only a soft billowy rim shows.
    puffs.push({
      x: cx + Math.cos(a) * rx * 0.82,
      y: cy + Math.sin(a) * ry * 0.82,
      r: rx * (0.22 + 0.12 * k) * (1 - 0.4 * bottom) * breathe,
      opacity: 0.7 * (1 - 0.5 * bottom),
    });
  }
  const rootY = cy + ry * 0.78;
  const tip = {
    x: cx + lerp(b.tailCurl, -b.tailCurl, mirror) * 0.57,
    y: rootY + b.tailLength * 0.9 + 12,
  };
  const tail = 7;
  const flow = (((time * 0.22) % 1) + 1) % 1;
  for (let j = 0; j < tail; j++) {
    const u = (j + flow) / tail;
    const ease = u * u * (3 - 2 * u);
    puffs.push({
      // Wobble keyed on u, not j: when `flow` wraps, puff j takes puff j+1's slot seamlessly.
      x: lerp(tip.x, cx, ease) + Math.sin(time * 1.3 + u * 6) * 4 * (1 - u),
      y: lerp(tip.y, rootY, u),
      r: rx * (0.14 + 0.32 * u),
      // Fade in at the tip and out where the puff merges into the head.
      opacity: 0.55 * Math.sin(Math.PI * u),
    });
  }
  return puffs;
}

/** Everything the upstream paint() wrote into the DOM for one frame, as plain data. */
export interface PetFrame {
  float: number;
  bodyTransform: string;
  body: string;
  volume: string;
  volumeOpacity: number;
  vaporShadow: { cx: number; cy: number; opacity: number };
  vaporLight: { cx: number; cy: number; opacity: number };
  shade: { cx: number; cy: number };
  soft: number;
  mist: number;
  smoke: { d: string; width: number; front: boolean }[];
  features: string;
  eyes: string;
  leftEye: PetStroke;
  rightEye: PetStroke;
  mouth: PetStroke;
  /** Outline-breaking puffs for the vapor look. */
  vapor: PetPuff[];
  /**
   * Horizontal move of the whole figure. The mirror reflects the body about the face (faceX), but
   * the body's center sits off it (head asymmetry and tail), so turning would slide the Pet
   * sideways; this moves it back so the turn happens in place, about the body's own center.
   */
  shiftX: number;
  /** The (mirrored) head center the shading is drawn around, before shiftX. */
  headX: number;
  /** 0..1 mirror progress: lighting offsets flip with the body. */
  turn: number;
  /** The head accessory, absent when the config has none. Drawn last, inside shiftX and float. */
  accessory?: PetAccessoryFrame;
}

export function petFrame(cfg: PetConfig, input: PetFrameInput): PetFrame {
  const reduced = !!input.reduced || cfg.motion.reducedEffects;
  const displayed = input.face;
  const mirrorProgress = input.mirror ?? 0;
  const gaze = input.gaze ?? { x: 0, y: 0 };
  const blinkFactor = reduced ? 1 : input.blink;
  const t = cfg.motion.enabled && !reduced ? input.time : 0;
  const float = cfg.motion.enabled && !reduced ? Math.sin(t * 1.16) * cfg.motion.floating : 0;
  const speaking = cfg.voice === 'speaking' ? cfg.audio * cfg.motion.speechReaction : 0;
  // The body follows the directional state by morphing positions and asymmetry, NOT by flipping the SVG.
  const base = cfg.body;
  const oriented: PetConfig = {
    ...cfg,
    body: {
      ...base,
      x: lerp(base.x, 2 * displayed.faceX - base.x, mirrorProgress),
      rotation: lerp(base.rotation, -base.rotation, mirrorProgress),
      tailCurl: lerp(base.tailCurl, -base.tailCurl, mirrorProgress),
      asymmetry: lerp(base.asymmetry, -base.asymmetry, mirrorProgress),
    },
  };
  const breathVolume =
    cfg.motion.enabled && !reduced
      ? Math.sin((t * 2 * Math.PI) / Math.max(0.6, cfg.motion.duration)) *
        cfg.motion.breathing *
        0.035
      : 0;
  // Shading travels on an ellipse inside the shell; the geometry is never scaled.
  const circulation = t * Math.max(0, cfg.body.noiseSpeed ?? 0.95) * 0.48;
  const rx = cfg.body.width * cfg.body.scaleX * 0.34;
  const ry = cfg.body.height * cfg.body.scaleY * 0.31;
  const count = clamp(Math.round(cfg.smoke.count), 0, 20);
  const smoke = Array.from({ length: count }, (_, i) => ({
    d: filamentPath(oriented, i, reduced ? 0 : t),
    width: cfg.smoke.width * (i % 3 === 0 ? 0.85 : 1),
    front: i % 3 === 0,
  }));
  const tx = gaze.x * DEFAULT_TRACKING.maxMoveX * cfg.motion.tracking;
  const ty = gaze.y * DEFAULT_TRACKING.maxMoveY * cfg.motion.tracking;
  const extraEyeY =
    gaze.y *
    DEFAULT_TRACKING.maxMoveY *
    Math.max(0, DEFAULT_TRACKING.eyeVerticalBoost - 1) *
    cfg.motion.tracking;
  const leftBase = eyePose('left', displayed);
  const rightBase = eyePose('right', displayed);
  const left = interpolateEye(leftBase, mirroredEyeTarget(rightBase, displayed), mirrorProgress);
  const right = interpolateEye(rightBase, mirroredEyeTarget(leftBase, displayed), mirrorProgress);
  const eyeColor = safeColor(cfg.eyes.color);
  const eye = (side: 'left' | 'right'): PetStroke => {
    const key = side === 'left' ? 'leftEye' : 'rightEye';
    let shape = side === 'left' ? cfg.eyes.leftShape : cfg.eyes.rightShape;
    let openness = side === 'left' ? cfg.eyes.leftOpen : cfg.eyes.rightOpen;
    if (cfg.eyes.sync && side === 'right') {
      shape = cfg.eyes.leftShape;
      openness = cfg.eyes.leftOpen;
    }
    const factor = Math.max(0.03, openness * blinkFactor);
    const pose = side === 'left' ? left : right;
    const mirroredState: FaceState = {
      ...displayed,
      [`${key}X`]: pose.x,
      [`${key}Y`]: pose.y,
      [`${key}Width`]: pose.width,
      [`${key}Height`]: pose.height,
      [`${key}Radius`]: pose.radius,
      [`${key}Rotation`]: pose.rotation,
    };
    return {
      d: eyePath(mirroredState, side, shape, factor),
      transform: rotationTransform(pose.rotation, pose.x, pose.y),
      color: eyeColor,
      width: Math.max(2, displayed[`${key}Width`] * 0.24),
      filled: !(shape === 'arc' || shape === 'closed'),
    };
  };
  const shape: MouthShape =
    cfg.emotion === 'surprised'
      ? 'surprise'
      : cfg.emotion === 'sad'
        ? 'sad'
        : cfg.emotion === 'sleepy'
          ? 'neutral'
          : cfg.mouth.shape;
  const talking = cfg.voice === 'speaking';
  const spoken = talking
    ? Math.max(
        cfg.mouth.open,
        Math.min(1.2, speaking * (0.72 + 0.28 * Math.abs(Math.sin(t * 8.6)))),
      )
    : cfg.mouth.open;
  const opened = cfg.emotion === 'speaking' && !talking ? Math.max(spoken, 0.18) : spoken;
  // Fleibo mirrors the mouth center, endpoint offsets and rotation separately.
  const mouthState = {
    ...displayed,
    mouthX: lerp(displayed.mouthX, 2 * displayed.faceX - displayed.mouthX, mirrorProgress),
    mouthY: displayed.mouthY + (talking ? Math.sin(t * 9.3) * spoken * 1.4 : 0),
    mouthRotation:
      lerp(displayed.mouthRotation, -displayed.mouthRotation, mirrorProgress) +
      (talking ? Math.sin(t * 5.2 + 0.3) * spoken * 5 : 0),
    mouthLeftOffset:
      lerp(displayed.mouthLeftOffset, displayed.mouthRightOffset, mirrorProgress) +
      (talking ? Math.sin(t * 7.1) * spoken * 2.2 : 0),
    mouthRightOffset:
      lerp(displayed.mouthRightOffset, displayed.mouthLeftOffset, mirrorProgress) -
      (talking ? Math.sin(t * 6.6 + 0.8) * spoken * 1.5 : 0),
  };
  return {
    float,
    bodyTransform: frameBodyTransform(oriented),
    body: bodyPath(oriented, t),
    volume: volumePath(oriented),
    volumeOpacity: clamp(cfg.body.volume * (1 + breathVolume), 0, 1),
    vaporShadow: {
      cx: oriented.body.x + Math.cos(circulation) * rx,
      cy: oriented.body.y + Math.sin(circulation) * ry,
      opacity: clamp(cfg.body.noise * 0.1, 0, 0.24),
    },
    vaporLight: {
      cx: oriented.body.x - Math.cos(circulation) * rx * 0.87,
      cy: oriented.body.y - Math.sin(circulation) * ry * 0.87,
      opacity: clamp(cfg.body.noise * 0.16, 0, 0.32),
    },
    shade: { cx: oriented.body.x + 32, cy: oriented.body.y + 24 },
    soft: reduced ? 0.5 : cfg.body.softness,
    mist: reduced ? 0.2 : cfg.smoke.blur,
    smoke,
    features: `translate(${n(tx)} ${n(ty)})`,
    eyes: `translate(0 ${n(extraEyeY)})`,
    leftEye: eye('left'),
    rightEye: eye('right'),
    vapor: petVaporPuffs(cfg, t, mirrorProgress),
    shiftX: 2 * (base.x - displayed.faceX) * mirrorProgress,
    headX: oriented.body.x,
    turn: mirrorProgress,
    ...(cfg.accessory && {
      accessory: accessoryFrame(
        cfg.accessory,
        cfg,
        oriented,
        mirrorProgress,
        frameBodyTransform(oriented),
        t,
        gaze,
        { tx, ty },
      ),
    }),
    mouth: {
      d: talking
        ? speakingMouthPath(mouthState, Math.max(opened, spoken), t)
        : mouthDrawPath(mouthState, shape, opened, cfg.mouth.control1, cfg.mouth.control2),
      transform: rotationTransform(mouthState.mouthRotation, mouthState.mouthX, mouthState.mouthY),
      color: eyeColor,
      width: displayed.mouthStroke,
      filled: talking || shape === 'open' || shape === 'surprise' || opened > 0.1,
    },
  };
}

/** Pose shown `elapsedMs` into a transition from `from` to the config's emotion. */
export function transitionFace(cfg: PetConfig, from: FaceState, elapsedMs: number): FaceState {
  const to = cfg.poses[cfg.emotion];
  const ratio = clamp(elapsedMs / Math.max(1, cfg.motion.transition), 0, 1);
  return ratio >= 1 ? to : interpolateFaceState(from, to, ease(cfg.motion.easing, ratio));
}

const frameBodyTransform = (oriented: PetConfig) =>
  `rotate(${n(oriented.body.rotation)} ${n(oriented.body.x)} ${n(oriented.body.y)})`;

/** What the Pet can wear on its head. */
export const PET_ACCESSORIES = ['guideHat', 'visitorCap', 'beanie', 'bandana', 'flower'] as const;
export type PetAccessory = (typeof PET_ACCESSORIES)[number];

/** Color sets an accessory can take; each accessory has its own default. */
// No teal: the Pet always sits on a teal circle, where a teal accessory would vanish.
export const PET_TINTS = ['ink', 'sky', 'sun', 'lupine'] as const;
export type PetTint = (typeof PET_TINTS)[number];

/** main: the accessory's body; accent: bands, bills, knots; light: lit edges and highlights. */
type Tone = 'main' | 'accent' | 'light' | 'shade' | 'leaf';

const TINTS: Record<PetTint, Record<'main' | 'accent' | 'light', string>> = {
  ink: { main: brand.ink, accent: brand.primarySoft, light: brand.primary },
  sky: { main: brand.sky, accent: brand.ink, light: brand.card },
  sun: { main: brand.sun, accent: brand.ink, light: brand.card },
  lupine: { main: brand.lupine, accent: brand.ink, light: brand.primarySoft },
};

/** The swatch a picker shows for a tint. */
export const tintColor = (tint: PetTint) => TINTS[tint].main;

/** One filled shape of an accessory; `opacity` < 1 for shading laid over the head or the hat. */
export interface PetAccessoryShape {
  d: string;
  fill: string;
  opacity?: number;
}

export interface PetAccessoryFrame {
  /** Places the shapes on the head: body rotation, head top, gaze, sway, mirror. */
  transform: string;
  shapes: PetAccessoryShape[];
}

interface ToneShape {
  d: string;
  tone: Tone;
  opacity?: number;
}

/** A near-circle as one closed cubic path (absolute C only, like every accessory path). */
function roundPath(x: number, y: number, rx: number, ry = rx): string {
  const k = 1.33;
  return `M ${n(x - rx)} ${n(y)} C ${n(x - rx)} ${n(y - k * ry)} ${n(x + rx)} ${n(y - k * ry)} ${n(x + rx)} ${n(y)} C ${n(x + rx)} ${n(y + k * ry)} ${n(x - rx)} ${n(y + k * ry)} ${n(x - rx)} ${n(y)} Z`;
}

/** A pointed petal or leaf from (x, y) out `len` along `deg`, `w` wide at its middle. */
function petalPath(x: number, y: number, deg: number, len: number, w: number): string {
  const a = (deg * Math.PI) / 180;
  const ux = Math.cos(a);
  const uy = Math.sin(a);
  const px = -uy * w;
  const py = ux * w;
  const tx = x + ux * len;
  const ty = y + uy * len;
  const m = (k: number) => [x + ux * len * k, y + uy * len * k];
  const [m1x, m1y] = m(0.25);
  const [m2x, m2y] = m(0.75);
  return `M ${n(x)} ${n(y)} C ${n(m1x + px)} ${n(m1y + py)} ${n(m2x + px)} ${n(m2y + py)} ${n(tx)} ${n(ty)} C ${n(m2x - px)} ${n(m2y - py)} ${n(m1x - px)} ${n(m1y - py)} ${n(x)} ${n(y)} Z`;
}

/** The frailejón flower tucked on the back of the head: yellow rays round a dark heart. */
const FLOWER_AT = { x: -60, y: 22 };
const flowerShapes = (): ToneShape[] => [
  ...[200, 250].map((deg) => ({
    d: petalPath(FLOWER_AT.x, FLOWER_AT.y + 6, deg, 60, 12),
    tone: 'leaf' as Tone,
  })),
  ...Array.from({ length: 12 }, (_, i) => ({
    d: petalPath(FLOWER_AT.x, FLOWER_AT.y, i * 30 - 90, 42, 8),
    tone: 'main' as Tone,
  })),
  { d: roundPath(FLOWER_AT.x, FLOWER_AT.y, 14), tone: 'accent' },
  { d: roundPath(FLOWER_AT.x - 4, FLOWER_AT.y - 4, 5), tone: 'light', opacity: 0.6 },
];

/**
 * Accessory shapes in Pet units, with the origin on the head's top centre (y grows down) and the
 * Pet facing right (+x), the way its face looks before a mirror. The head narrows toward its top:
 * about 140 wide 20 below it and 170 wide 45 below it (measured on the outline). Each hat sits
 * that low and that wide, its lower edge sagging in the middle as a rim seen from the front
 * does, so it wraps the head instead of perching on it. No outlines: shaded like the Pet (lit
 * from the upper left), and brims cast a soft shade on the head. Absolute M/L/C/Z only: the web
 * canvas and Skia parse the same strings.
 */
const ACCESSORY_SHAPES: Record<PetAccessory, { tint: PetTint; shapes: ToneShape[] }> = {
  guideHat: {
    tint: 'ink',
    shapes: [
      // The brim's shade on the head, under everything else.
      { d: 'M -80 50 C -40 64 30 64 62 50 C 30 74 -40 74 -80 50 Z', tone: 'shade', opacity: 0.9 },
      // Crown, as wide as the head at the band, with a soft dent on top.
      {
        d: 'M -66 40 C -70 0 -52 -28 -16 -32 C -6 -26 6 -26 16 -32 C 52 -28 70 0 66 40 Z',
        tone: 'main',
      },
      {
        d: 'M -54 20 C -58 -2 -46 -20 -22 -24 C -36 -12 -44 2 -44 22 Z',
        tone: 'light',
        opacity: 0.7,
      },
      // Band, following the brim's curve.
      { d: 'M -67 40 C -24 48 24 48 67 40 L 66 22 C 24 30 -24 30 -66 22 Z', tone: 'accent' },
      // Wide brim: a lens seen from the front, its near edge lower, and its lit top edge.
      { d: 'M -118 40 C -80 26 80 26 118 40 C 80 60 -80 60 -118 40 Z', tone: 'main' },
      { d: 'M -108 39 C -72 30 72 30 108 39 C 72 36 -72 36 -108 39 Z', tone: 'light' },
    ],
  },
  visitorCap: {
    tint: 'sky',
    shapes: [
      // The bill's shade on the forehead.
      { d: 'M 10 66 C 40 70 76 66 96 58 C 76 76 36 80 10 74 Z', tone: 'shade', opacity: 0.9 },
      // Dome hugging the head down to its rim, and its light.
      {
        d: 'M -90 56 C -96 0 -56 -28 0 -28 C 56 -28 96 0 90 56 C 46 68 -46 68 -90 56 Z',
        tone: 'main',
      },
      {
        d: 'M -72 26 C -72 -2 -46 -18 -12 -20 C -44 -8 -60 8 -62 30 Z',
        tone: 'light',
        opacity: 0.55,
      },
      // Front seam, turned toward the face, and the button on top.
      {
        d: 'M 4 -28 C 18 -8 28 24 30 62 L 37 62 C 35 24 25 -8 10 -28 Z',
        tone: 'accent',
        opacity: 0.3,
      },
      { d: roundPath(4, -30, 8, 6), tone: 'accent' },
      // Bill reaching forward from the rim, the way the Pet faces.
      { d: 'M 40 58 C 76 48 118 54 134 66 C 112 78 68 76 40 66 Z', tone: 'accent' },
    ],
  },
  beanie: {
    tint: 'lupine',
    shapes: [
      // Knit dome down to a folded cuff, ribbed, with a pompom on top.
      { d: 'M -84 50 C -92 0 -54 -30 0 -30 C 54 -30 92 0 84 50 Z', tone: 'main' },
      {
        d: 'M -66 20 C -68 -4 -44 -20 -14 -22 C -42 -10 -56 4 -58 24 Z',
        tone: 'light',
        opacity: 0.5,
      },
      {
        d: 'M -40 -16 C -48 6 -50 28 -50 44 L -44 44 C -44 28 -42 6 -34 -18 Z',
        tone: 'accent',
        opacity: 0.3,
      },
      {
        d: 'M -2 -30 C -4 0 -4 24 -4 44 L 2 44 C 2 24 2 0 4 -30 Z',
        tone: 'accent',
        opacity: 0.3,
      },
      {
        d: 'M 36 -18 C 44 6 46 28 46 44 L 52 44 C 52 28 50 6 42 -16 Z',
        tone: 'accent',
        opacity: 0.3,
      },
      { d: 'M -92 40 C -40 52 40 52 92 40 L 94 64 C 40 76 -40 76 -94 64 Z', tone: 'main' },
      {
        d: 'M -92 40 C -40 52 40 52 92 40 L 92 46 C 40 58 -40 58 -92 46 Z',
        tone: 'light',
        opacity: 0.45,
      },
      { d: roundPath(0, -38, 17), tone: 'accent' },
      { d: roundPath(-5, -43, 6), tone: 'light', opacity: 0.5 },
    ],
  },
  bandana: {
    tint: 'ink',
    shapes: [
      // A band round the forehead, knotted at the back with two loose tails.
      { d: 'M -86 54 C -108 44 -124 50 -134 38 C -130 62 -112 68 -90 66 Z', tone: 'main' },
      { d: 'M -88 64 C -106 74 -116 88 -128 84 C -118 96 -100 88 -86 74 Z', tone: 'main' },
      { d: 'M -96 46 C -40 60 40 60 92 44 L 92 70 C 40 86 -40 86 -98 72 Z', tone: 'main' },
      {
        d: 'M -94 49 C -40 63 40 63 90 47 C 40 68 -40 68 -94 56 Z',
        tone: 'light',
        opacity: 0.45,
      },
      ...[-56, -18, 20, 56].map((x) => ({
        d: roundPath(x, 68 - Math.abs(x) * 0.08, 4.5),
        tone: 'light' as Tone,
        opacity: 0.8,
      })),
      { d: roundPath(-96, 60, 11, 13), tone: 'accent' },
    ],
  },
  flower: { tint: 'sun', shapes: flowerShapes() },
};

/** The tint an accessory wears when none is picked. */
export const defaultTint = (kind: PetAccessory): PetTint => ACCESSORY_SHAPES[kind].tint;

function resolveShapes(kind: PetAccessory, tint: PetTint | undefined): PetAccessoryShape[] {
  const set = TINTS[tint ?? ACCESSORY_SHAPES[kind].tint];
  const color: Record<Tone, string> = { ...set, shade: brand.cardShade, leaf: brand.primary };
  return ACCESSORY_SHAPES[kind].shapes.map((s) => ({
    d: s.d,
    fill: color[s.tone],
    ...(s.opacity !== undefined && { opacity: s.opacity }),
  }));
}
/** Resolved shapes per accessory and tint, built once: a frame reuses the same arrays. */
const resolved = new Map<string, PetAccessoryShape[]>();
function shapesFor(kind: PetAccessory, tint: PetTint | undefined): PetAccessoryShape[] {
  const key = `${kind}:${tint ?? ''}`;
  let out = resolved.get(key);
  if (!out) {
    out = resolveShapes(kind, tint);
    resolved.set(key, out);
  }
  return out;
}

/** Degrees the hat tips per unit of the float's speed, and per unit of gaze. */
const HAT_SWAY_DEG = 3;
const HAT_GAZE_DEG = 4;

/**
 * The accessory placed on this frame's head. It rides the head (body rotation and float) and
 * follows its life: it tips a little as the Pet bobs (with the float's speed, so it lags the
 * motion like something resting on top) and leans with the gaze, sliding a fraction of the
 * face's own shift. A turn mirrors it about the head without squashing it to a line.
 */
function accessoryFrame(
  kind: PetAccessory,
  cfg: PetConfig,
  oriented: PetConfig,
  mirror: number,
  bodyTransform: string,
  t: number,
  gaze: { x: number; y: number },
  face: { tx: number; ty: number },
): PetAccessoryFrame {
  const b = oriented.body;
  const facing = 1 - 2 * mirror;
  const flip = (facing < 0 ? -1 : 1) * Math.max(0.3, Math.abs(facing));
  // Same centre and radii as bodyPath: the head's top is ry above its centre.
  // The outline's highest point sits a little toward the face from the head's centre.
  const cx = b.x + b.asymmetry * 0.07 + 5 * facing + face.tx * 0.4;
  const top = b.y - 4 - Math.max(30, b.height * b.scaleY * 0.5) + face.ty * 0.25;
  const bob = cfg.motion.enabled ? Math.cos(t * 1.16) * Math.min(1, cfg.motion.floating / 6) : 0;
  const tilt = HAT_SWAY_DEG * bob + HAT_GAZE_DEG * gaze.x;
  return {
    transform: `${bodyTransform} translate(${n(cx)} ${n(top)}) rotate(${n(tilt)}) scale(${n(flip)} 1)`,
    shapes: shapesFor(kind, cfg.accessoryTint),
  };
}

/** PET_VIEWBOX with room above the head for an accessory's crown. */
export const PET_ACCESSORY_VIEWBOX = { x: -162, y: -190, width: 324, height: 400 } as const;
