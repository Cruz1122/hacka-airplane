import { es } from '@/i18n/es';

import { STATION_IDS } from '../stations';
import { conceptPhoto, trailPhoto } from '../trailPhotos';

test('every station page has a bundled, credited photo', () => {
  for (const id of STATION_IDS) {
    es.trail.pages[id].forEach((_, page) => {
      const photo = trailPhoto(id, page);
      expect(photo.source).toBeDefined();
      expect(photo.author).not.toBe('');
      expect(photo.license).not.toBe('');
    });
  }
});

test('every stop has a credited concept photo, framed inside it', () => {
  for (const id of STATION_IDS) {
    const photo = conceptPhoto(id);
    expect(photo.author).not.toBe('');
    expect(photo.license).not.toBe('');
    expect(photo.url).toMatch(/^https:\/\//);
    expect(photo.crop.zoom).toBeGreaterThanOrEqual(1);
  }
});

test('every trail photo links to its own Commons file page, not a search', () => {
  const urls = STATION_IDS.flatMap((id) => [
    conceptPhoto(id).url,
    ...es.trail.pages[id].map((_, page) => trailPhoto(id, page).url),
  ]);
  for (const url of urls) expect(url).toMatch(/^https:\/\/commons\.wikimedia\.org\/wiki\/File:/);
});
