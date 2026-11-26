import {
  asksForPicture,
  parseMediaCatalog,
  pickMedia,
  withBundledPhotos,
  type MediaCatalog,
  type MediaItem,
} from '../media';

const photo = (file: string) => ({ file, author: `Autor ${file}`, license: 'CC BY 2.0' });
const species = (common: string, scientific: string, ...files: string[]): MediaItem => ({
  kind: 'species',
  common,
  scientific,
  photos: files.map(photo),
});

const CATALOG: MediaCatalog = {
  items: {
    condor: species('Cóndor de los Andes', 'Vultur gryphus', 'condor.1.webp', 'condor.2.webp'),
    oso: species('Oso de anteojos', 'Tremarctos ornatus', 'oso.1.webp'),
    frailejon: species(
      'Frailejón',
      'Espeletia hartwegiana',
      'frailejon.1.webp',
      'frailejon.2.webp',
      'frailejon.3.webp',
    ),
    danta: species('Danta de montaña', 'Tapirus pinchaque', 'danta.1.webp'),
    otun: {
      kind: 'place',
      common: 'Laguna del Otún',
      scientific: null,
      photos: [photo('otun.1.webp')],
    },
  },
  topics: {
    'fauna.condor': ['condor'],
    'fauna.mammals': ['oso', 'danta'],
    'flora.paramo': ['frailejon', 'condor', 'oso', 'danta'],
    'places.otun': ['otun'],
  },
};

/** Hands out `values` in order and fails the test if the selector draws more. */
function dice(...values: number[]) {
  const rng = jest.fn(() => {
    if (!values.length) throw new Error('drew more numbers than scripted');
    return values.shift()!;
  });
  return rng;
}

const ask = (topicId: string, userText = 'háblame de eso', afterMedia = false) => ({
  topicId,
  userText,
  afterMedia,
});

describe('pickMedia', () => {
  it('shows photos on half of eligible answers', () => {
    expect(pickMedia(CATALOG, ask('fauna.condor'), dice(0.49, 0))).not.toBeNull();
    expect(pickMedia(CATALOG, ask('fauna.condor'), dice(0.51))).toBeNull();
  });

  it('drops to 0.2 right after a reply that showed photos', () => {
    expect(
      pickMedia(CATALOG, ask('fauna.condor', 'y el cóndor', true), dice(0.19, 0)),
    ).not.toBeNull();
    expect(pickMedia(CATALOG, ask('fauna.condor', 'y el cóndor', true), dice(0.21))).toBeNull();
  });

  it('always shows them when the user asks for a picture, even right after photos', () => {
    const pick = pickMedia(CATALOG, ask('fauna.condor', 'muéstrame una foto', true), dice(0.99));
    expect(pick).toMatchObject({ layout: 'single', items: [{ id: 'condor' }] });
  });

  it('never shows photos for a topic with none', () => {
    const rng = dice();
    expect(pickMedia(CATALOG, ask('access.from_manizales', 'muéstrame fotos'), rng)).toBeNull();
    expect(rng).not.toHaveBeenCalled();
  });

  it('shows one item as a single photo with the caption parts', () => {
    expect(pickMedia(CATALOG, ask('fauna.condor'), dice(0, 0.6))).toEqual({
      layout: 'single',
      items: [
        {
          id: 'condor',
          common: 'Cóndor de los Andes',
          scientific: 'Vultur gryphus',
          photo: photo('condor.2.webp'),
        },
      ],
    });
  });

  it('keeps a place without a scientific name', () => {
    expect(pickMedia(CATALOG, ask('places.otun'), dice(0, 0))?.items[0]).toMatchObject({
      common: 'Laguna del Otún',
      scientific: null,
    });
  });

  it('splits two or three items between rows and columns', () => {
    expect(pickMedia(CATALOG, ask('fauna.mammals'), dice(0, 0.49, 0, 0))?.layout).toBe('rows');
    expect(pickMedia(CATALOG, ask('fauna.mammals'), dice(0, 0.5, 0, 0))?.layout).toBe('columns');
  });

  it('shows at most the first three items, in topic order, each with its rolled photo', () => {
    const pick = pickMedia(CATALOG, ask('flora.paramo'), dice(0, 0.9, 0.99, 0.5, 0));
    expect(pick?.layout).toBe('columns');
    expect(pick?.items.map((i) => [i.id, i.photo.file])).toEqual([
      ['frailejon', 'frailejon.3.webp'],
      ['condor', 'condor.2.webp'],
      ['oso', 'oso.1.webp'],
    ]);
  });
});

describe('asksForPicture', () => {
  it.each([
    'muéstrame el cóndor',
    'Muestrame una FOTO del oso',
    '¿tienes imágenes de la laguna?',
    'enséñame el frailejón',
    '¿Cómo es el oso de anteojos?',
    'como se ve la danta',
    'show me the condor',
    'any photos of the lake?',
    'a picture please',
  ])('counts "%s"', (text) => expect(asksForPicture(text)).toBe(true));

  it.each([
    '¿qué es la fotosíntesis?',
    'hola, ¿cómo estás?',
    'fotografía nocturna',
    'cuánto cuesta',
  ])('does not count "%s"', (text) => expect(asksForPicture(text)).toBe(false));
});

describe('parseMediaCatalog', () => {
  const raw = {
    version: 1,
    items: {
      condor: {
        kind: 'species',
        common: 'Cóndor de los Andes',
        scientific: 'Vultur gryphus',
        photos: [photo('condor.1.webp')],
      },
    },
    topics: { 'fauna.condor': ['condor'] },
  };

  it('reads the generated shape', () => {
    expect(parseMediaCatalog(raw)).toEqual({ items: raw.items, topics: raw.topics });
  });

  it('rejects a topic naming an item that does not exist', () => {
    expect(() => parseMediaCatalog({ ...raw, topics: { x: ['nope'] } })).toThrow(/topics\.x\[0\]/);
  });

  it('rejects an item without photos', () => {
    const items = { condor: { ...raw.items.condor, photos: [] } };
    expect(() => parseMediaCatalog({ ...raw, items })).toThrow(/items\.condor\.photos/);
  });
});

describe('withBundledPhotos', () => {
  it('drops photos without an image, then items and topics left empty', () => {
    const bundled = new Set(['condor.2.webp', 'oso.1.webp']);
    const kept = withBundledPhotos(CATALOG, (f) => bundled.has(f));
    expect(Object.keys(kept.items)).toEqual(['condor', 'oso']);
    expect(kept.items.condor.photos).toEqual([photo('condor.2.webp')]);
    expect(kept.topics).toEqual({
      'fauna.condor': ['condor'],
      'fauna.mammals': ['oso'],
      'flora.paramo': ['condor', 'oso'],
    });
  });
});
