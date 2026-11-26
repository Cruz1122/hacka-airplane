// One bundled place photo per station page, reusing the chat's media catalog (assets/media) so the
// trail ships no images of its own. Author and license come from media.json.
import { MEDIA, photoSource } from '@/core/media/bundled';

import type { StationId } from './stations';

export type TrailPhoto = {
  source: number;
  author: string;
  license: string;
};

/** Catalog item and photo number per page, in the order of `t.trail.pages[id]`. */
const PAGES: Record<StationId, readonly (readonly [item: string, n: number])[]> = {
  brisas: [
    ['place.frailejonal', 1],
    ['place.nevado_ruiz', 3],
    ['place.nevado_santa_isabel', 3],
  ],
  aguacerales: [
    ['place.frailejonal', 3],
    ['place.frailejonal', 2],
    ['place.glaciar', 1],
  ],
  arenales: [
    ['place.nevado_ruiz', 1],
    ['place.crater_arenas', 1],
    ['place.nevado_ruiz', 2],
  ],
  valleLunar: [
    ['place.glaciar', 3],
    ['place.nevado_tolima', 1],
    ['place.nevado_santa_isabel', 1],
  ],
  valleTumbas: [
    ['place.valle_tumbas', 1],
    ['place.valle_tumbas', 2],
    ['place.valle_tumbas', 3],
  ],
};

/** The photo of a station page; throws when the mapping names a photo the build did not bundle. */
export function trailPhoto(id: StationId, page: number): TrailPhoto {
  const rows = PAGES[id];
  const [item, n] = rows[page] ?? rows[0]!;
  const file = `${item}.${n}.webp`;
  const credit = MEDIA.items[item]?.photos.find((p) => p.file === file);
  const source = photoSource(file);
  if (!credit || source === undefined) throw new Error(`trail photo ${file} is not bundled`);
  return { source, author: credit.author, license: credit.license };
}
