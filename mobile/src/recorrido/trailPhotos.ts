// Photos keyed to each station paragraph by Wikimedia title in creditos_los_nevados.json.
import type { ImageSourcePropType } from 'react-native';

import type { StationId } from './stations';

export type TrailPhoto = {
  source: ImageSourcePropType;
  author: string;
  url: string;
};

const PHOTOS: Record<StationId, readonly TrailPhoto[]> = {
  brisas: [
    {
      source: require('../../assets/images/imagenes_los_nevados/Guía visitantes.jpg'),
      author: 'Jose David Niño Velasquez',
      url: 'https://upload.wikimedia.org/wikipedia/commons/4/49/Gu%C3%ADa_visitantes.jpg',
    },
    {
      source: require('../../assets/images/imagenes_los_nevados/Cordillera del Ruiz en la vía Murillo, zona de alta montaña.jpg'),
      author: 'Argumero',
      url: 'https://upload.wikimedia.org/wikipedia/commons/7/76/Cordillera_del_Ruiz_en_la_v%C3%ADa_Murillo%2C_zona_de_alta_monta%C3%B1a.jpg',
    },
    {
      source: require('../../assets/images/imagenes_los_nevados/Ingreso al Parque Nacional Natural Los Nevados.jpg'),
      author: 'Msolerg',
      url: 'https://upload.wikimedia.org/wikipedia/commons/7/75/Ingreso_al_Parque_Nacional_Natural_Los_Nevados.jpg',
    },
  ],
  aguacerales: [
    {
      source: require('../../assets/images/imagenes_los_nevados/Pared de musgo - PNN.jpg'),
      author: 'Msolerg',
      url: 'https://upload.wikimedia.org/wikipedia/commons/b/b5/Pared_de_musgo_-_PNN.jpg',
    },
    {
      source: require('../../assets/images/imagenes_los_nevados/Frailejones del nevado del Ruiz.jpg'),
      author: 'The GEGM',
      url: 'https://upload.wikimedia.org/wikipedia/commons/c/c7/Frailejones_del_nevado_del_Ruiz.jpg',
    },
    {
      source: require('../../assets/images/imagenes_los_nevados/Colchones de agua, fuentes de agua parque natural los nevados.jpg'),
      author: 'Jose David Niño Velasquez',
      url: 'https://upload.wikimedia.org/wikipedia/commons/4/4e/Colchones_de_agua%2C_fuentes_de_agua_parque_natural_los_nevados.jpg',
    },
  ],
  arenales: [
    {
      source: require('../../assets/images/imagenes_los_nevados/Arenales del Ruiz.jpg'),
      author: 'Wikimedia Commons',
      url: 'https://upload.wikimedia.org/wikipedia/commons/3/33/Arenales_del_Ruiz.jpg',
    },
    {
      source: require('../../assets/images/imagenes_los_nevados/Crater de La Olleta (712781090).jpg'),
      author: 'Edgar Jiménez from Porto, Portugal',
      url: 'https://upload.wikimedia.org/wikipedia/commons/6/61/Crater_de_La_Olleta_%28712781090%29.jpg',
    },
    {
      source: require('../../assets/images/imagenes_los_nevados/Cenizas volcanicas.jpg'),
      author: 'Jose David Niño Velasquez',
      url: 'https://upload.wikimedia.org/wikipedia/commons/f/f3/Cenizas_volcanicas.jpg',
    },
  ],
  valleLunar: [
    {
      source: require('../../assets/images/imagenes_los_nevados/Paisaje lunar - parque natural los nevados.jpg'),
      author: 'Jose David Niño Velasquez',
      url: 'https://upload.wikimedia.org/wikipedia/commons/f/f3/Paisaje_lunar_-_parque_natural_los_nevados.jpg',
    },
    {
      source: require('../../assets/images/imagenes_los_nevados/Valle lunar, al fondo pico nevado del Ruiz.jpg'),
      author: 'Wikimedia Commons',
      url: 'https://upload.wikimedia.org/wikipedia/commons/d/da/Valle_lunar%2C_al_fondo_pico_nevado_del_Ruiz.jpg',
    },
    {
      source: require('../../assets/images/imagenes_los_nevados/Flora nativa - Valle Lunar.jpg'),
      author: 'Msolerg',
      url: 'https://upload.wikimedia.org/wikipedia/commons/d/d3/Flora_nativa_-_Valle_Lunar.jpg',
    },
  ],
  valleTumbas: [
    {
      source: require('../../assets/images/imagenes_los_nevados/El valle de las tumbas.jpg'),
      author: 'Msolerg',
      url: 'https://upload.wikimedia.org/wikipedia/commons/b/b2/El_valle_de_las_tumbas.jpg',
    },
    {
      source: require('../../assets/images/imagenes_los_nevados/Lugar de paz para brindar agradecimiento a la Pachamama (Madre Tierra).jpg'),
      author: 'Jose David Niño Velasquez',
      url: 'https://upload.wikimedia.org/wikipedia/commons/3/3b/Lugar_de_paz_para_brindar_agradecimiento_a_la_Pachamama_%28Madre_Tierra%29.jpg',
    },
    {
      source: require('../../assets/images/imagenes_los_nevados/Nevado del Ruiz 1985.jpg'),
      author: 'U.S. Geological Survey',
      url: 'https://upload.wikimedia.org/wikipedia/commons/0/0c/Nevado_del_Ruiz_1985.jpg',
    },
  ],
};

/** The Commons file page (author, license) instead of the raw upload the credits JSON lists. */
function commonsPage(upload: string): string {
  const file = upload.split('/').pop()!;
  return `https://commons.wikimedia.org/wiki/File:${file}`;
}

export function trailPhoto(id: StationId, page: number): TrailPhoto {
  const row = PHOTOS[id];
  const photo = row[page] ?? row[0]!;
  return { ...photo, url: commonsPage(photo.url) };
}
