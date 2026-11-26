// The app's photo catalog: media.json joined with the images bundled in photos.generated.ts. The
// only module that imports either, so everything else takes a MediaCatalog and tests inject theirs.
import raw from '@/../assets/data/knowledge/media.json';

import { parseMediaCatalog, withBundledPhotos, type MediaCatalog } from './media';
import { PHOTOS } from './photos.generated';

export const MEDIA: MediaCatalog = withBundledPhotos(parseMediaCatalog(raw), (file) =>
  Object.hasOwn(PHOTOS, file),
);

/** The bundled image of a photo file (a `require` id), or undefined when it is not bundled. */
export function photoSource(file: string): number | undefined {
  return Object.hasOwn(PHOTOS, file) ? PHOTOS[file] : undefined;
}
