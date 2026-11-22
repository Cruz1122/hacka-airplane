// Port of World.execute_tool (world/model.py) driven by world.json's exec table.
import type { ToolCall } from './types';
import { pyRepr, type World } from './world';

export type ToolResult =
  | { ok: true; tool: string; passage_ids: string[]; data: Record<string, unknown> }
  | { ok: false; tool: string; error: string };

// --------------------------------------------------------------------------- sha256

const K = new Uint32Array([
  0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
  0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
  0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
  0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]);

function utf8(text: string): number[] {
  const out: number[] = [];
  for (const ch of text) {
    const cp = ch.codePointAt(0)!;
    if (cp < 0x80) out.push(cp);
    else if (cp < 0x800) out.push(0xc0 | (cp >> 6), 0x80 | (cp & 63));
    else if (cp < 0x10000) out.push(0xe0 | (cp >> 12), 0x80 | ((cp >> 6) & 63), 0x80 | (cp & 63));
    else
      out.push(
        0xf0 | (cp >> 18),
        0x80 | ((cp >> 12) & 63),
        0x80 | ((cp >> 6) & 63),
        0x80 | (cp & 63),
      );
  }
  return out;
}

/** SHA-256 digest words (8 x uint32, big-endian). Pure TS: Hermes has no crypto.subtle. */
export function sha256Words(text: string): Uint32Array {
  const bytes = utf8(text);
  const bitLen = bytes.length * 8;
  bytes.push(0x80);
  while (bytes.length % 64 !== 56) bytes.push(0);
  for (let i = 7; i >= 0; i--) bytes.push(i >= 4 ? 0 : (bitLen >>> (i * 8)) & 0xff);
  const h = new Uint32Array([
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
  ]);
  const w = new Uint32Array(64);
  const rotr = (x: number, n: number) => (x >>> n) | (x << (32 - n));
  for (let off = 0; off < bytes.length; off += 64) {
    for (let i = 0; i < 16; i++) {
      const j = off + i * 4;
      w[i] = (bytes[j] << 24) | (bytes[j + 1] << 16) | (bytes[j + 2] << 8) | bytes[j + 3];
    }
    for (let i = 16; i < 64; i++) {
      const s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ (w[i - 15] >>> 3);
      const s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ (w[i - 2] >>> 10);
      w[i] = w[i - 16] + s0 + w[i - 7] + s1;
    }
    let [a, b, c, d, e, f, g, hh] = h;
    for (let i = 0; i < 64; i++) {
      const t1 =
        (hh + (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + w[i]) | 0;
      const t2 = ((rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) | 0;
      hh = g;
      g = f;
      f = e;
      e = (d + t1) | 0;
      d = c;
      c = b;
      b = a;
      a = (t1 + t2) | 0;
    }
    h[0] += a;
    h[1] += b;
    h[2] += c;
    h[3] += d;
    h[4] += e;
    h[5] += f;
    h[6] += g;
    h[7] += hh;
  }
  return h;
}

/** corpus.stable_hash: first 8 bytes of sha256(utf-8), big-endian unsigned. */
export function stableHash(text: string): bigint {
  const h = sha256Words(text);
  return (BigInt(h[0]) << 32n) | BigInt(h[1]);
}

export function letterCode(prefix: string, key: string): string {
  // Letters only: a confirmation code must never look like a corpus number.
  let h = stableHash(key);
  let letters = '';
  for (let i = 0; i < 6; i++) {
    letters += String.fromCharCode(65 + Number(h % 26n));
    h /= 26n;
  }
  return `${prefix}-${letters}`;
}

/** f"{name}|{sorted(args.items())}" with Python reprs. */
export function toolKey(name: string, args: Record<string, unknown>): string {
  const items = Object.keys(args)
    .sort((a, b) => (a < b ? -1 : a > b ? 1 : 0))
    .map((k) => `(${pyRepr(k)}, ${pyRepr(args[k])})`);
  return `${name}|[${items.join(', ')}]`;
}

// --------------------------------------------------------------------------- execute

/** Deterministic mock result; identical to Python World.execute_tool. */
export function executeTool(world: World, call: ToolCall): ToolResult {
  const errors = world.validateArguments(call.name, call.arguments);
  if (errors.length > 0) return { ok: false, tool: call.name, error: errors.join('; ') };
  const spec = world.tools.get(call.name)!;
  if (spec.near_duplicate_of !== null)
    return { ok: true, tool: call.name, passage_ids: [], data: {} };

  const ex = world.json.exec;
  const rule = ex.rules[call.name];
  if (!rule) throw new Error(`no exec rule for tool ${call.name}`);
  const a = call.arguments as Record<string, any>;
  const station: string | undefined = a.station;
  const stIds = (field: string) => world.passageIdsFor(station, field);
  const key = toolKey(call.name, a);

  let pids: string[] = [];
  if (rule.procedure_by_emergency_type) {
    for (const ref of ex.procedures[a.emergency_type])
      pids.push(...('st' in ref ? stIds(ref.st) : [ex.park_passages[ref.park]]));
  } else if (rule.item_rule) {
    pids = [ex.item_rules[a.item].passage_id];
  } else if (rule.trail_passage) {
    pids = [world.trailPassageId(a.trail_id)];
  } else if (rule.fee_by_visitor_type) {
    pids = stIds(ex.fee_field[a.visitor_type]);
  } else {
    pids = (rule.st ?? []).flatMap(stIds);
    pids.push(...(rule.park ?? []).map((k) => ex.park_passages[k]));
  }

  const data: Record<string, unknown> = {};
  const d = rule.data;
  if (d) {
    switch (d.kind) {
      case 'hash_mod4_nonzero':
        data[d.key] = stableHash(key) % 4n !== 0n;
        break;
      case 'hash_choice': {
        const choices = ex[d.choices];
        data[d.key] = choices[Number(stableHash(key) % BigInt(choices.length))];
        break;
      }
      case 'station_trail_ids':
        data[d.key] = [...(world.stations.get(station!)?.trails ?? [])];
        break;
      case 'item_allowed':
        data[d.key] = ex.item_rules[a.item].allowed;
        break;
      case 'altitude_limit':
        data[d.key] = a.target_altitude_m <= parseInt(world.getPassage(d.passage_id).values[0], 10);
        break;
      case 'letter_code':
        data[d.key] = letterCode(d.prefix, key);
        break;
    }
  }
  return { ok: true, tool: call.name, passage_ids: pids, data };
}
