// One bundled place photo per station page, reusing the chat's media catalog (assets/media) so the
// trail ships no images of its own. Author and license come from media.json.
import { MEDIA, photoSource } from '@/core/media/bundled';
import { photoSourceUrl } from '@/ui/chat/MediaGallery';

import type { StationId } from './stations';

export type TrailPhoto = {
  source: number;
  author: string;
  license: string;
  /** The photo's source page, as the chat's gallery links it. */
  url: string;
};

/**
 * Each trail photo's Commons file page. The catalog (media.json) has no source links, so the chat
 * falls back to a Commons search, which for these photos lands on unrelated files. Found on
 * 2026-11-26 by searching Commons for each author and matching thumbnails to the bundled crop; the
 * author and licence of every page agree with media.json. Regenerating the catalog with links from
 * the operator's export (build_media.py drops its url column) would make this table redundant.
 */
const SOURCE_URL: Readonly<Record<string, string>> = {
  'place.crater_arenas.1.webp':
    'https://commons.wikimedia.org/wiki/File:Fuente_visual_comparativa_Vista_a%C3%A9rea_del_%E2%80%9CCrater_Arenas%E2%80%9D.jpg',
  'place.frailejonal.1.webp': 'https://commons.wikimedia.org/wiki/File:Gigante_ancestral.jpg',
  'place.frailejonal.2.webp':
    'https://commons.wikimedia.org/wiki/File:Ladera_alta_llena_de_Fraiilejones_en_el_Nevado_del_Ruiz.jpg',
  'place.frailejonal.3.webp':
    'https://commons.wikimedia.org/wiki/File:Parque_Nacional_Natural_Los_Nevados_y_Nevado_del_Ruiz_(39072).jpg',
  'place.glaciar.1.webp':
    'https://commons.wikimedia.org/wiki/File:Cascada_de_deshielo_sobre_paredes_rocosas_del_Nevado_del_Ruiz.jpg',
  'place.glaciar.3.webp':
    'https://commons.wikimedia.org/wiki/File:Nevado_Ruiz_Nacimiento_rio_Chinchina.JPG',
  'place.nevado_ruiz.1.webp':
    'https://commons.wikimedia.org/wiki/File:Crater_Origen_de_la_Avalancha_de_Armero_Quind%C3%ADo_13_Nov_1985.JPG',
  'place.nevado_ruiz.2.webp': 'https://commons.wikimedia.org/wiki/File:Cumanday_(712781536).jpg',
  'place.nevado_ruiz.3.webp': 'https://commons.wikimedia.org/wiki/File:El_ruiz_Volcano.jpg',
  'place.nevado_santa_isabel.1.webp':
    'https://commons.wikimedia.org/wiki/File:Bosque_de_Frailejones_V%C3%ADa_Laguna_el_Ot%C3%BAn.JPG',
  'place.nevado_santa_isabel.3.webp':
    'https://commons.wikimedia.org/wiki/File:Vista_Panor%C3%A1mica_del_Nevado_Santa_Isabel.JPG',
  'place.nevado_tolima.1.webp':
    'https://commons.wikimedia.org/wiki/File:Parque_Nacional_Natural_Los_Nevados_y_Nevado_del_Ruiz_(47118).jpg',
  'place.valle_tumbas.1.webp':
    'https://commons.wikimedia.org/wiki/File:Arenales_de_P%C3%A1ramo_Nevado_del_Ruiz.JPG',
  'place.valle_tumbas.2.webp': 'https://commons.wikimedia.org/wiki/File:Cenizas_volcanicas.jpg',
  'place.valle_tumbas.3.webp':
    'https://commons.wikimedia.org/wiki/File:Contraste_cambio_clim%C3%A1tico.jpg',
  'species.espeletia_hartwegiana.1.webp':
    'https://commons.wikimedia.org/wiki/File:Espeletia_hartwegiana_o.jpg',
  'species.puma_concolor.2.webp':
    'https://commons.wikimedia.org/wiki/File:Mountain_Lion_in_Glacier_National_Park.jpg',
  'species.tremarctos_ornatus.2.webp':
    'https://commons.wikimedia.org/wiki/File:2018-09-01_AT_Wien_13_Hietzing,_Tiergarten_Sch%C3%B6nbrunn,_Tremarctos_ornatus_(50790951717).jpg',
  'species.vultur_gryphus.1.webp':
    'https://commons.wikimedia.org/wiki/File:Andean_condor_at_the_Hoenderdaell_animal_park_in_Anna_Paulowna.jpg',
};

/** A bundled photo with its credit; throws when the catalog or the build lacks it. */
function bundled(item: string, n: number): TrailPhoto {
  const file = `${item}.${n}.webp`;
  const entry = MEDIA.items[item];
  const photo = entry?.photos.find((p) => p.file === file);
  const source = photoSource(file);
  if (!entry || !photo || source === undefined)
    throw new Error(`trail photo ${file} is not bundled`);
  const url =
    SOURCE_URL[file] ??
    photoSourceUrl({
      id: item,
      common: entry.common,
      scientific: entry.scientific,
      photo,
    });
  return { source, author: photo.author, license: photo.license, url };
}

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
  return bundled(item, n);
}

/** Where to frame a photo in a square: its centre as 0..1 of the photo, and how far to zoom in. */
export type PhotoCrop = { x: number; y: number; zoom: number };

export type SpeciesPhoto = TrailPhoto & {
  /** Height over width of the photo file. */
  aspect: number;
  crop: PhotoCrop;
};

/** Catalog photos are 640x800 (experiments/media/build_media.py). */
const CATALOG_ASPECT = 1.25;

/**
 * The real photo of each stop's species for its sheet, framed by eye: the park's own frailejón, the
 * bear's face with its markings, the whole puma, the condor's head, ruff and wing. The culpeo is not
 * in the chat's catalog, so its photo ships with the trail (Wikimedia Commons, cropped square on
 * the fox).
 */
const SPECIES: Record<StationId, () => SpeciesPhoto> = {
  brisas: () => catalogSpecies('species.espeletia_hartwegiana', 1, { x: 0.5, y: 0.4, zoom: 1 }),
  aguacerales: () => catalogSpecies('species.tremarctos_ornatus', 2, { x: 0.5, y: 0.42, zoom: 1 }),
  arenales: () => catalogSpecies('species.puma_concolor', 2, { x: 0.5, y: 0.45, zoom: 1 }),
  valleLunar: () => ({
    source: require('../../assets/images/trail/culpeo.webp') as number,
    author: 'Diego Delso',
    license: 'CC BY-SA 4.0',
    url: 'https://commons.wikimedia.org/wiki/File:Zorro_andino_(Lycalopex_culpaeus_andinus),_Laguna_Colorada,_Bolivia,_2016-02-02,_DD_101.JPG',
    aspect: 1,
    crop: { x: 0.5, y: 0.5, zoom: 1 },
  }),
  valleTumbas: () => catalogSpecies('species.vultur_gryphus', 1, { x: 0.4, y: 0.42, zoom: 1.25 }),
};

function catalogSpecies(item: string, n: number, crop: PhotoCrop): SpeciesPhoto {
  return { ...bundled(item, n), aspect: CATALOG_ASPECT, crop };
}

/** The stop's species photo; throws when it maps to a photo the build did not bundle. */
export function speciesPhoto(id: StationId): SpeciesPhoto {
  return SPECIES[id]();
}
