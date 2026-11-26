// Compact 22-byte BLE beacon frame (44 hex chars) carried after the 2-byte "NV" magic prefix.
// Layout (version 3):
//   [0]     version (high nibble = 3) | flags (bit0=guide, bit1=rear, bit2=syncing, bit3=nfcCard)
//   [1..2]  groupId   (uint16 BE; 0 = unpaired visitor searching)
//   [3..4]  senderId  (uint16 BE; 1..65535)
//   [5]     echoFrontRssi (int8; 0 = unheard, -127..-1 = dBm)
//   [6]     echoRearRssi  (int8; 0 = unheard, -127..-1 = dBm)
//   [7..15] name UTF-8 (9 bytes, truncated on code-point boundary, zero-padded)
//   [16]    look (uint8; 0 = absent; low 3 bits = accessory, bits 3..5 = tint)
//   [17]    alertMeters (uint8; 0 = absent; guides only)
//   [18..21] auth tag (uint32 BE; 0 until group-key signing lands)
// Version 2 had a 10-byte name in [7..16] and no look; version 1 had an 11-byte name in [7..17]
// and no alertMeters or look. Both still decode so this build hears phones running older ones.
// `nfcCard` tells NFC-capable visitors to wait for a tap instead of pairing over BLE proximity;
// decoders that predate it ignore the bit.
//
// NFC pairing record (the guide's HCE answer to SELECT AID, before the status word):
//   [0]     version (high nibble = 3) | flags (bit1=rear)
//   [1..2]  groupId      (uint16 BE; non-zero)
//   [3..4]  guide shortId (uint16 BE; non-zero)
//   [5]     alertMeters  (uint8; 0 = absent)
//   [6]     look         (uint8; 0 = absent)
//   [7]     name length N (0..PAIRING_NAME_MAX_BYTES)
//   [8..]   name UTF-8 (N bytes, truncated on code-point boundary)
// Version 2 had no look byte (name length at [6]); version 1 had neither alertMeters nor look
// (name length at [5]). Both still decode.
import { GROUP_POLICY } from './policy';
import {
  memberId,
  type GuideSlot,
  type Member,
  type MemberAccessory,
  type MemberId,
  type MemberLook,
  type MemberTint,
} from './types';

export const BEACON_VERSION = 3;
export const BEACON_BYTES = 22;
export const BEACON_NAME_MAX_BYTES = 9;
const BEACON_V2_NAME_MAX_BYTES = 10;
const BEACON_V1_NAME_MAX_BYTES = 11;
const BEACON_LOOK_INDEX = 16;
const BEACON_ALERT_METERS_INDEX = 17;

const FLAG_GUIDE = 0x01;
const FLAG_REAR = 0x02;
const FLAG_SYNCING = 0x04;
const FLAG_NFC_CARD = 0x08;

export const PAIRING_VERSION = 3;
export const PAIRING_NAME_MAX_BYTES = 32;
const PAIRING_HEADER_BYTES = 8;
const PAIRING_V2_HEADER_BYTES = 7;
const PAIRING_V1_HEADER_BYTES = 6;

const LOOK_ACCESSORIES: readonly (MemberAccessory | 'none')[] = [
  'none',
  'guideHat',
  'visitorCap',
  'beanie',
  'bandana',
  'flower',
];
const LOOK_TINTS: readonly MemberTint[] = ['ink', 'sky', 'sun', 'lupine'];

export interface BeaconFrame {
  readonly groupId: number;
  readonly senderId: number;
  readonly role: 'guide' | 'visitor';
  readonly slot: GuideSlot;
  readonly syncing: boolean;
  /** Guide only: its NFC card answers taps right now. */
  readonly nfcCard: boolean;
  readonly echoFrontRssi: number | null;
  readonly echoRearRssi: number | null;
  readonly name: string;
  /** Guide only: its alert distance in meters; absent when it set none (or a v1 frame). */
  readonly alertMeters?: number;
  /** What this phone's Pet wears; absent on v1/v2 frames or when unset. */
  readonly look?: MemberLook;
  readonly tag: number;
}

/** What a visitor needs to join a guide's group, handed over by an NFC tap. */
export interface PairingRecord {
  readonly groupId: number;
  readonly guideShortId: number;
  readonly slot: GuideSlot;
  readonly name: string;
  readonly alertMeters?: number;
  readonly look?: MemberLook;
}

const SHORT_ID_PREFIX = 'g-';

/** Deterministic MemberId for a 16-bit BLE short id (1..65535). */
export function shortIdToMemberId(shortId: number): MemberId {
  const n = shortId & 0xffff;
  return memberId(`${SHORT_ID_PREFIX}${n.toString(16).padStart(4, '0')}`);
}

/** Maps any MemberId to a non-zero 16-bit short id; round-trips `shortIdToMemberId`. */
export function memberIdToShortId(id: MemberId): number {
  const match = /^g-([0-9a-f]{4})$/i.exec(id);
  if (match) {
    const parsed = parseInt(match[1], 16);
    if (parsed > 0) return parsed;
  }
  // FNV-1a 32-bit folded to non-zero 16-bit.
  let h = 0x811c9dc5;
  for (let i = 0; i < id.length; i++) {
    h ^= id.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  const folded = ((h >>> 16) ^ (h & 0xffff)) & 0xffff;
  return folded === 0 ? 1 : folded;
}

/** Random non-zero 16-bit identifier for a session or group. */
export function randomShortId(): number {
  return 1 + Math.floor(Math.random() * 0xfffe);
}

/** Snaps an alert distance to the policy's step and range; the one place that bounds it. */
export function clampAlertMeters(meters: number): number {
  const { min, max, step } = GROUP_POLICY.alertMeters;
  return Math.max(min, Math.min(max, Math.round(meters / step) * step));
}

/** Builds a domain Member from a decoded beacon frame. */
export function memberFromBeacon(frame: BeaconFrame, fallbackName: string): Member {
  const id = shortIdToMemberId(frame.senderId);
  const name = frame.name || fallbackName;
  return frame.role === 'guide'
    ? {
        id,
        role: 'guide',
        name,
        slot: frame.slot,
        ...withAlertMeters(frame.alertMeters),
        ...withLook(frame.look),
      }
    : { id, role: 'visitor', name, ...withLook(frame.look) };
}

/** Spread into a guide Member so an absent distance leaves no `alertMeters` key behind. */
export function withAlertMeters(meters: number | undefined): {
  alertMeters?: number;
} {
  return meters === undefined ? {} : { alertMeters: meters };
}

/** Spread into a Member/frame so an absent look leaves no `look` key behind. */
export function withLook(look: MemberLook | undefined): { look?: MemberLook } {
  if (!look || (look.accessory === undefined && look.tint === undefined)) return {};
  return { look };
}

export function sameLook(a: MemberLook | undefined, b: MemberLook | undefined): boolean {
  return a?.accessory === b?.accessory && a?.tint === b?.tint;
}

function encodeLook(look: MemberLook | undefined): number {
  if (!look) return 0;
  const accIdx = look.accessory ? LOOK_ACCESSORIES.indexOf(look.accessory) + 1 : 0;
  const tintIdx =
    look.accessory !== 'none' && look.tint ? LOOK_TINTS.indexOf(look.tint) + 1 : 0;
  return (accIdx & 0x07) | ((tintIdx & 0x07) << 3);
}

function decodeLook(byte: number): MemberLook | undefined {
  if (byte === 0) return undefined;
  const accCode = byte & 0x07;
  const tintCode = (byte >>> 3) & 0x07;
  const accessory = accCode > 0 ? LOOK_ACCESSORIES[accCode - 1] : undefined;
  const tint = tintCode > 0 ? LOOK_TINTS[tintCode - 1] : undefined;
  if (!accessory && !tint) return undefined;
  if (accessory === 'none') return { accessory: 'none' };
  return {
    ...(accessory ? { accessory } : {}),
    ...(tint ? { tint } : {}),
  };
}

function encodeAlertMeters(meters: number | undefined): number {
  return meters === undefined || !Number.isFinite(meters) ? 0 : clampAlertMeters(meters);
}

/** The byte comes off the air: anything non-zero is snapped into the policy range. */
function decodeAlertMeters(byte: number): number | undefined {
  return byte === 0 ? undefined : clampAlertMeters(byte);
}

function encodeRssi(rssi: number | null): number {
  if (rssi === null || !Number.isFinite(rssi)) return 0;
  const clamped = Math.max(-127, Math.min(-1, Math.round(rssi)));
  return clamped & 0xff;
}

function decodeRssi(byte: number): number | null {
  if (byte === 0) return null;
  const signed = byte > 127 ? byte - 256 : byte;
  return signed < 0 ? signed : null;
}

/** Pure UTF-8 encoder truncated cleanly at code-point boundaries to at most `maxBytes`. */
function encodeUtf8Bounded(text: string, maxBytes: number): number[] {
  const out: number[] = [];
  for (const ch of text.trim()) {
    const cp = ch.codePointAt(0)!;
    const seq: number[] =
      cp <= 0x7f
        ? [cp]
        : cp <= 0x7ff
          ? [0xc0 | (cp >> 6), 0x80 | (cp & 0x3f)]
          : cp <= 0xffff
            ? [0xe0 | (cp >> 12), 0x80 | ((cp >> 6) & 0x3f), 0x80 | (cp & 0x3f)]
            : [
                0xf0 | (cp >> 18),
                0x80 | ((cp >> 12) & 0x3f),
                0x80 | ((cp >> 6) & 0x3f),
                0x80 | (cp & 0x3f),
              ];
    if (out.length + seq.length > maxBytes) break;
    out.push(...seq);
  }
  return out;
}

/** Pure UTF-8 decoder stopping at the first zero pad byte; replaces invalid sequences safely. */
function decodeUtf8Bytes(bytes: Uint8Array): string {
  let end = bytes.length;
  for (let i = 0; i < bytes.length; i++) {
    if (bytes[i] === 0) {
      end = i;
      break;
    }
  }
  let out = '';
  let i = 0;
  while (i < end) {
    const b0 = bytes[i];
    if (b0 < 0x80) {
      out += String.fromCharCode(b0);
      i += 1;
    } else if ((b0 & 0xe0) === 0xc0 && i + 1 < end && (bytes[i + 1] & 0xc0) === 0x80) {
      const cp = ((b0 & 0x1f) << 6) | (bytes[i + 1] & 0x3f);
      out += cp >= 0x80 ? String.fromCodePoint(cp) : '';
      i += 2;
    } else if (
      (b0 & 0xf0) === 0xe0 &&
      i + 2 < end &&
      (bytes[i + 1] & 0xc0) === 0x80 &&
      (bytes[i + 2] & 0xc0) === 0x80
    ) {
      const cp = ((b0 & 0x0f) << 12) | ((bytes[i + 1] & 0x3f) << 6) | (bytes[i + 2] & 0x3f);
      out += cp >= 0x800 && (cp < 0xd800 || cp > 0xdfff) ? String.fromCodePoint(cp) : '';
      i += 3;
    } else if (
      (b0 & 0xf8) === 0xf0 &&
      i + 3 < end &&
      (bytes[i + 1] & 0xc0) === 0x80 &&
      (bytes[i + 2] & 0xc0) === 0x80 &&
      (bytes[i + 3] & 0xc0) === 0x80
    ) {
      const cp =
        ((b0 & 0x07) << 18) |
        ((bytes[i + 1] & 0x3f) << 12) |
        ((bytes[i + 2] & 0x3f) << 6) |
        (bytes[i + 3] & 0x3f);
      out += cp >= 0x10000 && cp <= 0x10ffff ? String.fromCodePoint(cp) : '';
      i += 4;
    } else {
      i += 1;
    }
  }
  return out.trim();
}

export function encodeBeacon(frame: BeaconFrame): string {
  const buf = new Uint8Array(BEACON_BYTES);
  let flags = 0;
  if (frame.role === 'guide') {
    flags |= FLAG_GUIDE;
    if (frame.slot === 'rear') flags |= FLAG_REAR;
    if (frame.syncing) flags |= FLAG_SYNCING;
    if (frame.nfcCard) flags |= FLAG_NFC_CARD;
  }
  buf[0] = (BEACON_VERSION << 4) | flags;
  buf[1] = (frame.groupId >>> 8) & 0xff;
  buf[2] = frame.groupId & 0xff;
  buf[3] = (frame.senderId >>> 8) & 0xff;
  buf[4] = frame.senderId & 0xff;
  buf[5] = encodeRssi(frame.echoFrontRssi);
  buf[6] = encodeRssi(frame.echoRearRssi);

  const nameBytes = encodeUtf8Bounded(frame.name, BEACON_NAME_MAX_BYTES);
  for (let i = 0; i < nameBytes.length; i++) buf[7 + i] = nameBytes[i];
  buf[BEACON_LOOK_INDEX] = encodeLook(frame.look);
  buf[BEACON_ALERT_METERS_INDEX] =
    frame.role === 'guide' ? encodeAlertMeters(frame.alertMeters) : 0;

  const tag = frame.tag >>> 0;
  buf[18] = (tag >>> 24) & 0xff;
  buf[19] = (tag >>> 16) & 0xff;
  buf[20] = (tag >>> 8) & 0xff;
  buf[21] = tag & 0xff;
  return bytesToHex(buf);
}

export function decodeBeacon(payloadHex: string): BeaconFrame | null {
  if (payloadHex.length !== BEACON_BYTES * 2) return null;
  const buf = hexToBytes(payloadHex);
  if (!buf) return null;
  const version = buf[0] >>> 4;
  if (version !== BEACON_VERSION && version !== 2 && version !== 1) return null;
  const flags = buf[0] & 0x0f;
  const isGuide = (flags & FLAG_GUIDE) !== 0;
  const groupId = (buf[1] << 8) | buf[2];
  const senderId = (buf[3] << 8) | buf[4];
  if (senderId === 0) return null;

  const tag = ((buf[18] << 24) | (buf[19] << 16) | (buf[20] << 8) | buf[21]) >>> 0;
  const nameBytes =
    version === 1
      ? BEACON_V1_NAME_MAX_BYTES
      : version === 2
        ? BEACON_V2_NAME_MAX_BYTES
        : BEACON_NAME_MAX_BYTES;
  const look = version >= 3 ? decodeLook(buf[BEACON_LOOK_INDEX]) : undefined;
  const alertMeters =
    version === 1 || !isGuide ? undefined : decodeAlertMeters(buf[BEACON_ALERT_METERS_INDEX]);
  return {
    groupId,
    senderId,
    role: isGuide ? 'guide' : 'visitor',
    slot: isGuide && (flags & FLAG_REAR) !== 0 ? 'rear' : 'front',
    syncing: isGuide && (flags & FLAG_SYNCING) !== 0,
    nfcCard: isGuide && (flags & FLAG_NFC_CARD) !== 0,
    echoFrontRssi: decodeRssi(buf[5]),
    echoRearRssi: decodeRssi(buf[6]),
    name: decodeUtf8Bytes(buf.subarray(7, 7 + nameBytes)),
    ...withAlertMeters(alertMeters),
    ...withLook(look),
    tag,
  };
}

export function encodePairing(record: PairingRecord): string {
  const name = encodeUtf8Bounded(record.name, PAIRING_NAME_MAX_BYTES);
  const buf = new Uint8Array(PAIRING_HEADER_BYTES + name.length);
  buf[0] = (PAIRING_VERSION << 4) | (record.slot === 'rear' ? FLAG_REAR : 0);
  buf[1] = (record.groupId >>> 8) & 0xff;
  buf[2] = record.groupId & 0xff;
  buf[3] = (record.guideShortId >>> 8) & 0xff;
  buf[4] = record.guideShortId & 0xff;
  buf[5] = encodeAlertMeters(record.alertMeters);
  buf[6] = encodeLook(record.look);
  buf[7] = name.length;
  buf.set(name, PAIRING_HEADER_BYTES);
  return bytesToHex(buf);
}

/** Parses an NFC pairing record (v1, v2, or v3); null for anything malformed. */
export function decodePairing(hex: string): PairingRecord | null {
  const buf = hexToBytes(hex);
  if (!buf || buf.length === 0) return null;
  const version = buf[0] >>> 4;
  if (version !== PAIRING_VERSION && version !== 2 && version !== 1) return null;
  const header =
    version === 1
      ? PAIRING_V1_HEADER_BYTES
      : version === 2
        ? PAIRING_V2_HEADER_BYTES
        : PAIRING_HEADER_BYTES;
  if (buf.length < header) return null;
  const groupId = (buf[1] << 8) | buf[2];
  const guideShortId = (buf[3] << 8) | buf[4];
  const nameLength = buf[header - 1];
  if (groupId === 0 || guideShortId === 0) return null;
  if (nameLength > PAIRING_NAME_MAX_BYTES || buf.length !== header + nameLength) return null;
  return {
    groupId,
    guideShortId,
    slot: (buf[0] & FLAG_REAR) !== 0 ? 'rear' : 'front',
    name: decodeUtf8Bytes(buf.subarray(header)),
    ...withAlertMeters(version === 1 ? undefined : decodeAlertMeters(buf[5])),
    ...withLook(version >= 3 ? decodeLook(buf[6]) : undefined),
  };
}

function bytesToHex(buf: Uint8Array): string {
  let hex = '';
  for (let i = 0; i < buf.length; i++) hex += buf[i].toString(16).padStart(2, '0');
  return hex;
}

function hexToBytes(hex: string): Uint8Array | null {
  if (hex.length % 2 !== 0) return null;
  const buf = new Uint8Array(hex.length / 2);
  for (let i = 0; i < buf.length; i++) {
    const hi = hexNibble(hex.charCodeAt(i * 2));
    const lo = hexNibble(hex.charCodeAt(i * 2 + 1));
    if (hi < 0 || lo < 0) return null;
    buf[i] = (hi << 4) | lo;
  }
  return buf;
}

function hexNibble(code: number): number {
  if (code >= 48 && code <= 57) return code - 48;
  if (code >= 97 && code <= 102) return code - 87;
  if (code >= 65 && code <= 70) return code - 55;
  return -1;
}
