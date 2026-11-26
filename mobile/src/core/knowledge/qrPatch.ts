import { fromByteArray, toByteArray } from 'base64-js';
import { strFromU8, unzlibSync, zlibSync } from 'fflate/browser';

// Leave room below the byte capacity of a level-M QR code.
export const QR_LIMIT = 2200;
export const QR_RELATED_LIMIT = 5;
const LEGACY_LIMIT = 1500;
const MAX_INFLATED_BYTES = 32_768;
const LEGACY_PREFIX = 'NEVADOS1:';
const COMPRESSED_PREFIX = 'NEVADOS2:';
const SERIES_PREFIX = 'NEVADOS3:';
const PART_SIZE = 500;
const MAX_PARTS = 120;
const MAX_SERIES_BYTES = 262_144;

export interface QrEntry {
  section: string;
  title: string;
  answer: string;
  questions: string[];
  variants: string[];
  steps: string[];
  more: string[];
  why: string[];
  related: string[];
  sources: { label: string; url: string }[];
}

export type KnowledgePatch = { id: string; revision: number } & (
  { op: 'remove' } | { op: 'put'; entry: QrEntry }
);

const identifier = /^[a-z][a-z0-9_]*(?:[.-][a-z0-9_]+)*$/;
const object = (value: unknown): Record<string, unknown> => {
  if (!value || typeof value !== 'object' || Array.isArray(value))
    throw new Error('Formato de QR inválido.');
  return value as Record<string, unknown>;
};

function field(value: unknown, label: string, max?: number): string {
  if (
    typeof value !== 'string' ||
    !value.trim() ||
    (max !== undefined && value.length > max) ||
    /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/.test(value)
  ) {
    const message = 'Revisa el campo «' + label + '».';
    throw new Error(max === undefined ? message : message + ' Máximo ' + max + ' caracteres.');
  }
  return value.trim();
}

function id(value: unknown, label: string) {
  const result = field(value, label, 100);
  if (!identifier.test(result)) throw new Error('Identificador inválido en «' + label + '».');
  return result;
}

function list(value: unknown, label: string, count?: number, max?: number): string[] {
  if (value === undefined) return [];
  if (!Array.isArray(value)) throw new Error('Revisa el campo «' + label + '».');
  if (count !== undefined && value.length > count) {
    throw new Error('«' + label + '» admite hasta ' + count + ' líneas.');
  }
  return [...new Set(value.map((item) => field(item, label, max)))];
}

function readEntry(value: unknown): QrEntry {
  const row = object(value);
  const sources = row.sources ?? [];
  if (!Array.isArray(sources) || sources.length > 3) throw new Error('Incluye hasta tres fuentes.');
  const questions = list(row.questions, 'Preguntas', 8, 180);
  if (!questions.length) throw new Error('Escribe al menos una pregunta para el buscador.');
  return {
    section: id(row.section, 'Sección'),
    title: field(row.title, 'Título', 100),
    answer: field(row.answer, 'Respuesta', 650),
    questions,
    variants: list(row.variants, 'Variantes'),
    steps: list(row.steps, 'Pasos', 5, 240),
    more: list(row.more, 'Información adicional', 5, 400),
    why: list(row.why, 'Razón', 3, 400),
    related: list(row.related, 'Temas relacionados', QR_RELATED_LIMIT, 100).map((item) =>
      id(item, 'Temas relacionados'),
    ),
    sources: sources.map((item) => {
      const source = object(item);
      const url = field(source.url, 'URL de fuente', 220);
      if (!/^https:\/\/[a-z0-9.-]+\.[a-z]{2,}(?:[/?#][^\s]*)?$/i.test(url)) {
        throw new Error('Las fuentes requieren una URL HTTPS.');
      }
      return { label: field(source.label, 'Nombre de fuente', 100), url };
    }),
  };
}

export function utf8Bytes(text: string): Uint8Array {
  const hex = encodeURIComponent(text);
  const bytes = [];
  for (let i = 0; i < hex.length; i++) {
    if (hex[i] === '%') {
      bytes.push(parseInt(hex.slice(i + 1, i + 3), 16));
      i += 2;
    } else bytes.push(hex.charCodeAt(i));
  }
  return Uint8Array.from(bytes);
}

export function qrBytes(text: string): number {
  return encodeURIComponent(text).replace(/%[0-9A-F]{2}/g, 'x').length;
}

export function validateKnowledgePatch(payload: unknown): KnowledgePatch {
  const row = object(payload);
  const entryId = id(row.id, 'ID de la ficha');
  const revision = row.revision;
  if (typeof revision !== 'number' || !Number.isSafeInteger(revision) || revision <= 0) {
    throw new Error('La revisión del QR es inválida.');
  }
  if (row.op === 'remove') return { op: row.op, id: entryId, revision };
  if (row.op === 'put') return { op: row.op, id: entryId, revision, entry: readEntry(row.entry) };
  throw new Error('Operación de actualización desconocida.');
}

function unpackCode(value: string, maxBytes = MAX_INFLATED_BYTES): string {
  if (!/^[A-Za-z0-9_-]+$/.test(value) || value.length % 4 === 1) {
    throw new Error('Invalid QR transport encoding');
  }
  const base64 = value.replace(/-/g, '+').replace(/_/g, '/');
  const compressed = toByteArray(base64 + '='.repeat((4 - (base64.length % 4)) % 4));
  // A fixed buffer caps inflation even for a crafted code. Outputs that fill it are rejected.
  const bytes = unzlibSync(compressed, { out: new Uint8Array(maxBytes + 1) });
  if (bytes.length > maxBytes) throw new Error('Inflated QR is too large');
  // fflate inflates the stream without checking its zlib trailer.
  let low = 1;
  let high = 0;
  for (const byte of bytes) {
    low = (low + byte) % 65_521;
    high = (high + low) % 65_521;
  }
  const trailer = new DataView(compressed.buffer, compressed.byteOffset, compressed.byteLength);
  if (high * 65_536 + low !== trailer.getUint32(compressed.length - 4)) {
    throw new Error('Invalid QR checksum');
  }
  return strFromU8(bytes);
}

export function parseKnowledgePatch(text: string): KnowledgePatch {
  const legacy = text.startsWith(LEGACY_PREFIX);
  if (!legacy && !text.startsWith(COMPRESSED_PREFIX)) {
    throw new Error('Este código no es una actualización de Los Nevados.');
  }
  const limit = legacy ? LEGACY_LIMIT : QR_LIMIT;
  if (text.length > limit || qrBytes(text) > limit)
    throw new Error('El QR supera el tamaño permitido.');
  let payload: unknown;
  try {
    const json = legacy
      ? text.slice(LEGACY_PREFIX.length)
      : unpackCode(text.slice(COMPRESSED_PREFIX.length));
    payload = JSON.parse(json);
  } catch {
    throw new Error('El código está incompleto o dañado.');
  }
  return validateKnowledgePatch(payload);
}

function compactJson(value: unknown): string {
  return JSON.stringify(value, (key, field: unknown) =>
    key !== '' && Array.isArray(field) && !field.length ? undefined : field,
  );
}

function packCode(json: string, maxBytes: number): string {
  const bytes = utf8Bytes(json);
  if (bytes.length > maxBytes) throw new Error('Hay demasiado contenido para compartir en una sola actualización.');
  return fromByteArray(zlibSync(bytes, { level: 9 }))
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

export function encodeKnowledgePatch(patch: KnowledgePatch): string {
  const json = compactJson(validateKnowledgePatch(patch));
  const compressed = packCode(json, MAX_INFLATED_BYTES);
  const packed = COMPRESSED_PREFIX + compressed;
  const legacy = LEGACY_PREFIX + json;
  const legacySize = qrBytes(legacy);
  if (legacySize <= LEGACY_LIMIT && legacySize <= packed.length) return legacy;
  if (packed.length > QR_LIMIT) {
    throw new Error(
      'La ficha no cabe en un solo QR incluso comprimida. Acorta las variantes o la información adicional.',
    );
  }
  return packed;
}

export interface KnowledgeQrSeries {
  id: string;
  total: number;
  parts: ReadonlyMap<number, string>;
}

function seriesId(packed: string): string {
  // The series label prevents mixing parts from different transfers.
  let hash = 0x811c9dc5;
  for (let i = 0; i < packed.length; i++) hash = Math.imul(hash ^ packed.charCodeAt(i), 0x01000193);
  return (hash >>> 0).toString(16).padStart(8, '0') + packed.length.toString(16).padStart(8, '0');
}

export function encodeKnowledgeQrSeries(patches: readonly KnowledgePatch[]): string[] {
  if (!patches.length) throw new Error('Todavía no hay cambios guardados para compartir.');
  const payload = packCode(compactJson(patches.map(validateKnowledgePatch)), MAX_SERIES_BYTES);
  const total = Math.ceil(payload.length / PART_SIZE);
  if (total > MAX_PARTS) {
    throw new Error('La actualización supera el tamaño de una serie. Comparte las fichas por separado.');
  }
  const id = seriesId(payload);
  return Array.from({ length: total }, (_, i) =>
    [SERIES_PREFIX + id, i + 1, total, payload.slice(i * PART_SIZE, (i + 1) * PART_SIZE)].join(':'),
  );
}

export function collectKnowledgeQr(
  code: string,
  previous?: KnowledgeQrSeries,
): { series: KnowledgeQrSeries } | { patches: KnowledgePatch[] } {
  if (!code.startsWith(SERIES_PREFIX)) {
    if (previous) throw new Error('Termina la serie en curso o cancélala para escanear otro QR.');
    return { patches: [parseKnowledgePatch(code)] };
  }
  if (code.length > PART_SIZE + 40) throw new Error('Este QR es demasiado grande.');
  const match = /^NEVADOS3:([0-9a-f]{16}):([1-9][0-9]{0,2}):([1-9][0-9]{0,2}):([A-Za-z0-9_-]+)$/.exec(code);
  if (!match) throw new Error('El código está incompleto o dañado.');
  const [, id, index, count, data] = match;
  const number = Number(index);
  const total = Number(count);
  if (total > MAX_PARTS || number > total || data.length > PART_SIZE ||
      (number < total && data.length !== PART_SIZE)) {
    throw new Error('Una parte de la actualización es inválida.');
  }
  if (previous && (previous.id !== id || previous.total !== total)) {
    throw new Error('Este QR pertenece a otra actualización. Continúa con la misma serie.');
  }
  const parts = new Map(previous?.parts);
  if (parts.has(number) && parts.get(number) !== data) throw new Error('Hay dos versiones de la misma parte.');
  parts.set(number, data);
  if (parts.size < total) return { series: { id, total, parts } };

  const payload = Array.from({ length: total }, (_, i) => parts.get(i + 1)).join('');
  if (seriesId(payload) !== id) throw new Error('La serie está incompleta o dañada.');
  let entries: unknown;
  try {
    entries = JSON.parse(unpackCode(payload, MAX_SERIES_BYTES));
  } catch {
    throw new Error('La serie está incompleta o dañada.');
  }
  if (!Array.isArray(entries) || !entries.length) throw new Error('La serie no contiene fichas.');
  const patches = entries.map(validateKnowledgePatch);
  if (new Set(patches.map(({ id }) => id)).size !== patches.length) {
    throw new Error('La serie contiene fichas repetidas.');
  }
  return { patches };
}
