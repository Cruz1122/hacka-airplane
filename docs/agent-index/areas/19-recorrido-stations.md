# Recorrido and station pages

## Purpose

The **Recorrido** tab draws the Brisas vehicle route as a vertical trail with five tappable stations. Each station opens a page of captioned photos and a camera button. At the time of writing, these files were untracked in the project root and are absent from commit `45a394d5`.

## Start here

- `mobile/app/(tabs)/recorrido.tsx` renders `RecorridoScreen`. `mobile/app/(tabs)/_layout.tsx` registers the tab. `ROUTE.route` in `mobile/src/ui/AppNavBar.tsx` maps the `route` nav tab to it.
- `mobile/app/estacion/[id].tsx` validates `id` with `isStationId` and redirects to `/recorrido` when the check fails. `mobile/app/_layout.tsx` registers the `estacion` stack.
- `mobile/src/recorrido/stations.ts` defines `STATION_IDS`, `StationId`, and `STATION_NODES`. Node `x` and `y` are fractions of the map box.
- `mobile/src/recorrido/TrailPath.tsx` draws the dashed SVG path and one `StationMark` per node. `mobile/src/recorrido/trailMarks.tsx` holds the animal and frailejón figures in `TrailMarkFigure`.
- `mobile/src/recorrido/StationPage.tsx` renders the station page with `MediaRowList` from `mobile/src/ui/MediaRowList.tsx`.

## Runtime or data flow

1. `RecorridoScreen` puts `TrailPath` in a `ScrollView` that is flipped with `scaleY: -1`, so station 1 shows at the bottom of the screen.
2. A tap calls `router.push('/estacion/' + id)`.
3. `StationPage` reads its text from `t.trail.pages[id]` (`subtitle` and `body`) and its title from `t.trail.stations[id].name`. Both live in `mobile/src/i18n/es.ts` and `en.ts`. The `Labels` type makes `en` match the shape of `es`.
4. `trailPhoto(id, page)` in `mobile/src/recorrido/trailPhotos.ts` maps each page to a `media.json` item and photo number. It resolves the photo through `MEDIA` and `photoSource` in `mobile/src/core/media/bundled.ts`, and it throws when the photo is not bundled.
5. The camera uses `expo-image-picker`. The photo it takes stays in component state and is not saved (verified in `StationPage`). The permission text lives in `mobile/app.json`.

## Tests

`mobile/src/recorrido/__tests__/trailPhotos.test.ts` checks that every page in `es.trail.pages` resolves to a bundled photo with an author and a license. No test covers `TrailPath`, `StationPage`, `MediaRowList`, or the route redirect.

## Common change paths

- To add a station, update `STATION_IDS` and `STATION_NODES`, then add a `TrailMarkFigure` case. The `never` check fails the type check when a case is missing. Then add `PAGES` rows in `trailPhotos.ts` and the `trail` copy in both locale files.
- To change a photo, edit `PAGES`. Only photos that `experiments/media/build_media.py` writes into `photos.generated.ts` resolve. Do not edit the generated file.

## Related docs

- [App design system](../../../.claude/skills/app-design/SKILL.md)
- [Mobile offline stack](../../../.claude/skills/mobile-offline-stack/SKILL.md)
- [System map](../../system-map.md)
