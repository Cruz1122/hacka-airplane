# Mobile media and vision

## Purpose

`mobile/src/core/media` picks bundled park photos to show under a chat answer. `mobile/src/vision` classifies a photo that the user attaches. Neither module imports the other.

## Start here

- `core/media/media.ts` is pure TypeScript with `parseMediaCatalog`, `withBundledPhotos`, `pickMedia`, and `asksForPicture`.
- `core/media/bundled.ts` is the only importer of `media.json` and `photos.generated.ts`. It exports `MEDIA` and `photoSource(file)`.
- `vision/matchPhoto.ts` scores a 1024-dimension vector against `assets/vision/index.json` and returns a `classes.json` entry, `mountainMatch`, or `undefined`.
- `vision/classifyPhoto.ts` runs on native with Skia and `onnxruntime-react-native`. `classifyPhoto.web.ts` uses `onnxruntime-web`. Both share `vision/pixels.ts`.

## Runtime or data flow

Photo lookup:

1. `bundled.ts` drops photos missing from `PHOTOS`, then empty items and topics.
2. `KnowledgeChat.mediaFor` in `state/knowledgeChat.ts` calls `pickMedia` once per answer. Urgent-safety replies get no photos.
3. `ui/chat/MediaGallery.tsx` resolves each file with `photoSource`.

Photo identification starts in `app/(tabs)/index.tsx`, which passes `() => classifyPhoto(uri)` to `KnowledgeChat.askPhoto`. `classifyPhoto` tries a center crop, then a padded fit frame when the long side is at least 1.25 times the short side. A class with `id` gets an inline answer from its `description`. The `persona` class gets a greeting. Other classes query the engine with `entryId`.

On web, only the Metro dev middleware in `mobile/metro.config.js` serves `/knowledge-files/vision-encoder.onnx`. A static web export is unverified.

Generated inputs:

- `experiments/media/build_media.py` writes `assets/media/*.webp`, `media.json`, and `photos.generated.ts`. Do not edit them by hand.
- `mobile/scripts/build-vision.py` writes `encoder.onnx` and `index.json` from photos outside `mobile/`. It embeds center crops only. Whether that weakens padded-frame scores was not measured.
- No script reads `mobile/scripts/vision-sources.json`. It records the source URL of each reference photo.

## Tests

- `core/media/__tests__/media.test.ts` covers the photo chances, layouts, and parser errors.
- `core/media/__tests__/bundled.test.ts` checks `media.json` against `catalog.json` and `PHOTOS`.
- `vision/__tests__/photo.test.ts` covers `askPhoto` outcomes, the minimum of 10 references per class, and the panorama frame.

## Common change paths

- To add park photos, rerun `build_media.py` and then `bundled.test.ts`.
- To add a vision class, edit `classes.json`, rerun `build-vision.py`, and tune `thresholds` in `matchPhoto.ts`.

The live checkout also has an uncommitted consumer, `mobile/src/recorrido/trailPhotos.ts`.

## Related docs

- [Mobile README, photo identification](../../../mobile/README.md#identificar-imágenes-sin-internet)
- [System map](../../system-map.md)
