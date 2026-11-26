// Photos under an answer about a species or a place. Pure TS (no React/RN): the catalog is injected,
// so the chat decides once per reply and tests script the dice. Data: assets/data/knowledge/media.json
// (generated, never hand-edited), joined with its bundled images in ./bundled.ts.

export interface MediaPhoto {
  file: string;
  author: string;
  license: string;
}

export interface MediaItem {
  kind: 'species' | 'place';
  common: string;
  /** null for places. */
  scientific: string | null;
  /** Never empty once parsed. */
  photos: MediaPhoto[];
}

export interface MediaCatalog {
  items: Readonly<Record<string, MediaItem>>;
  /** Catalog topic id -> item ids, in order of first mention in the answer. */
  topics: Readonly<Record<string, readonly string[]>>;
}

/** One photo of one item, as the gallery shows it. */
export interface MediaPickItem {
  id: string;
  common: string;
  scientific: string | null;
  photo: MediaPhoto;
}

/** `single` holds exactly one item; `rows` and `columns` two or three. */
export type MediaPick =
  | { layout: 'single'; items: [MediaPickItem] }
  | {
      layout: 'rows' | 'columns';
      items: [MediaPickItem, MediaPickItem] | [MediaPickItem, MediaPickItem, MediaPickItem];
    };

export const MEDIA_CHANCE = 0.5;
/** Right after a reply that showed photos, so they stay a surprise. */
export const MEDIA_CHANCE_AFTER_MEDIA = 0.2;
export const MAX_MEDIA_ITEMS = 3;

const PICTURE_ASK =
  /\b(?:fotos?|imagen(?:es)?|muestrame|ensename|como es|como se ve|pictures?|photos?|show me)\b/;

/** The user asked to see it. Accent- and case-insensitive, whole words only. */
export function asksForPicture(text: string): boolean {
  // NFD then drop the marks: JS `\b` only knows ASCII letters, so "muéstrame" must become ASCII.
  const plain = text.normalize('NFD').replace(/\p{M}/gu, '').toLowerCase();
  return PICTURE_ASK.test(plain);
}

export interface MediaQuery {
  /** The answer's catalog entry id. */
  topicId: string;
  /** The question the answer replies to. */
  userText: string;
  /** The previous assistant reply showed photos. */
  afterMedia: boolean;
}

/**
 * Whether this answer shows photos, and which. `rng` is drawn in this order, and only for a
 * decision actually taken: the chance (once per eligible answer), then the layout (only with 2-3
 * items: below 0.5 rows, else columns), then one photo variant per item, in topic order.
 */
export function pickMedia(
  catalog: MediaCatalog,
  { topicId, userText, afterMedia }: MediaQuery,
  rng: () => number,
): MediaPick | null {
  if (!Object.hasOwn(catalog.topics, topicId)) return null;
  const items = catalog.topics[topicId]
    .filter((id) => Object.hasOwn(catalog.items, id))
    .slice(0, MAX_MEDIA_ITEMS);
  if (items.length === 0) return null;
  const chance = asksForPicture(userText)
    ? 1
    : afterMedia
      ? MEDIA_CHANCE_AFTER_MEDIA
      : MEDIA_CHANCE;
  if (chance < 1 && rng() >= chance) return null;
  const layout = items.length === 1 ? 'single' : rng() < 0.5 ? 'rows' : 'columns';
  const picked = items.map((id): MediaPickItem => {
    const { common, scientific, photos } = catalog.items[id];
    const photo = photos[Math.min(photos.length - 1, Math.floor(rng() * photos.length))];
    return { id, common, scientific, photo };
  });
  const [a, b, c] = picked;
  if (layout === 'single') return { layout, items: [a] };
  return { layout, items: c ? [a, b, c] : [a, b] };
}

/** media.json as generated; throws with the offending path so a bad export fails loudly. */
export function parseMediaCatalog(raw: unknown): MediaCatalog {
  const fail = (path: string, what: string): never => {
    throw new Error(`media.json: ${path} ${what}`);
  };
  const record = (v: unknown, path: string) =>
    typeof v === 'object' && v !== null && !Array.isArray(v)
      ? (v as Record<string, unknown>)
      : fail(path, 'is not an object');
  const text = (v: unknown, path: string) =>
    typeof v === 'string' && v.trim() !== '' ? v : fail(path, 'is not a non-empty string');

  const root = record(raw, '(root)');
  if (root.version !== 1) fail('version', `is ${String(root.version)}, expected 1`);
  const items: Record<string, MediaItem> = {};
  for (const [id, value] of Object.entries(record(root.items, 'items'))) {
    const at = `items.${id}`;
    const item = record(value, at);
    if (item.kind !== 'species' && item.kind !== 'place')
      fail(`${at}.kind`, 'is not species|place');
    const photos = Array.isArray(item.photos) ? item.photos : fail(`${at}.photos`, 'is not a list');
    if (photos.length === 0) fail(`${at}.photos`, 'is empty');
    items[id] = {
      kind: item.kind as MediaItem['kind'],
      common: text(item.common, `${at}.common`),
      scientific: item.scientific === null ? null : text(item.scientific, `${at}.scientific`),
      photos: photos.map((p, i) => {
        const photo = record(p, `${at}.photos[${i}]`);
        return {
          file: text(photo.file, `${at}.photos[${i}].file`),
          author: text(photo.author, `${at}.photos[${i}].author`),
          license: text(photo.license, `${at}.photos[${i}].license`),
        };
      }),
    };
  }
  const topics: Record<string, string[]> = {};
  for (const [topic, value] of Object.entries(record(root.topics, 'topics'))) {
    const ids = Array.isArray(value) ? value : fail(`topics.${topic}`, 'is not a list');
    topics[topic] = ids.map((id, i) => {
      const itemId = text(id, `topics.${topic}[${i}]`);
      return Object.hasOwn(items, itemId)
        ? itemId
        : fail(`topics.${topic}[${i}]`, `names no item (${itemId})`);
    });
  }
  return { items, topics };
}

/** Keeps only photos with a bundled image, and items that still have one. */
export function withBundledPhotos(
  catalog: MediaCatalog,
  bundled: (file: string) => boolean,
): MediaCatalog {
  const items: Record<string, MediaItem> = {};
  for (const [id, item] of Object.entries(catalog.items)) {
    const photos = item.photos.filter((p) => bundled(p.file));
    if (photos.length) items[id] = { ...item, photos };
  }
  const topics: Record<string, string[]> = {};
  for (const [topic, ids] of Object.entries(catalog.topics)) {
    const kept = ids.filter((id) => Object.hasOwn(items, id));
    if (kept.length) topics[topic] = kept;
  }
  return { items, topics };
}
