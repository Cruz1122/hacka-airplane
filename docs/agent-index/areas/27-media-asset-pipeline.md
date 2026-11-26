# Media asset pipeline

## Purpose

`experiments/media/build_media.py` turns the operator's photo export into the photos that the chat shows under species and place answers. The committed output has 38 items, 101 WebP files, and 171 mapped topics.

## Start here

- `build_media.py`. `build()` runs the pipeline. `SPECIES` holds the hand-curated species photos and crops. `PLACES`, `PLACE_SKIP`, and `PLACE_FOCUS` hold the place rules. `check_invariants()` enforces the output contract and a 12 MiB budget.
- `experiments/media/places.json` rates each landscape photo. The landscape classifier that writes it is not in this repo.
- `mobile/src/core/media/media.ts` parses the manifest and picks photos with `pickMedia`.
- `mobile/src/core/media/bundled.ts` exports `MEDIA` and `photoSource`. It is the only module that imports the generated files.

## Runtime or data flow

1. The build reads the export root (`--src`), `places.json`, and `mobile/assets/data/knowledge/catalog.json`.
2. It keeps CC or public-domain photos with a named author, at most three per item.
3. `map_topics` matches item aliases in topic text, at most three items per topic.
4. `write_outputs` writes `mobile/assets/media/*.webp`, `mobile/assets/data/knowledge/media.json`, and `mobile/src/core/media/photos.generated.ts`. Never hand-edit them.
5. In the app, `knowledgeChat.ts` calls `pickMedia`, and `MediaGallery.tsx` renders each photo through `photoSource`.

To regenerate, install Pillow, which `pyproject.toml` does not declare, and run:

```sh
python3 -I experiments/media/build_media.py --src <export root> \
	--places experiments/media/places.json --review-dir <tmp dir>
```

A test proves that the same inputs give byte-identical outputs. The export is not in the repo, so you cannot regenerate without a copy of it.

## Tests

- `experiments/media/test_build_media.py` builds a synthetic fixture end to end. A bare `pytest` run skips it because `testpaths = ["tests"]`. Run `uv run --with pytest --with pillow python -m pytest experiments/media -q`.
- `mobile/src/core/media/__tests__/media.test.ts` covers `pickMedia` and the manifest parser.
- `mobile/src/core/media/__tests__/bundled.test.ts` checks the committed manifest against `catalog.json` and `PHOTOS`.

## Common change paths

- To change a species photo or crop, edit `SPECIES` and rebuild.
- To change how often photos show, edit `MEDIA_CHANCE` or `PICTURE_ASK` in `media.ts`.
- Uncommitted `mobile/src/recorrido/trailPhotos.ts` in the main checkout pins photo numbers per place. A rebuild that reorders place photos can break it.

## Related docs

- [Knowledge contract](../../knowledge-contract.md) defines the topic ids and sections that `map_topics` reads.
