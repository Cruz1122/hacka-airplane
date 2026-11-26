// The generated media.json against the knowledge catalog and the bundled images.
import catalog from '@/../assets/data/knowledge/catalog.json';
import raw from '@/../assets/data/knowledge/media.json';

import { MEDIA } from '../bundled';
import { MAX_MEDIA_ITEMS, parseMediaCatalog } from '../media';
import { PHOTOS } from '../photos.generated';

const parsed = parseMediaCatalog(raw);

describe('bundled media', () => {
  it('maps only topics the knowledge catalog has', () => {
    const ids = new Set(catalog.map((e) => e.id));
    expect(Object.keys(parsed.topics).filter((id) => !ids.has(id))).toEqual([]);
  });

  it('bundles every photo it names, so the app drops none', () => {
    const files = Object.values(parsed.items).flatMap((i) => i.photos.map((p) => p.file));
    expect(files.filter((f) => !Object.hasOwn(PHOTOS, f))).toEqual([]);
    expect(MEDIA).toEqual(parsed);
  });

  it('names at most three items per topic', () => {
    const over = Object.entries(parsed.topics).filter(([, ids]) => ids.length > MAX_MEDIA_ITEMS);
    expect(over).toEqual([]);
  });
});
