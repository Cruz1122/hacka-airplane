import { es } from '@/i18n/es';

import { STATION_IDS } from '../stations';
import { trailPhoto } from '../trailPhotos';

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
