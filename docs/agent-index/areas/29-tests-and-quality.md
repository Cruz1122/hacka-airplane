# Tests and quality

## Purpose

Find the test that guards a behavior, and the command that runs it.

## Start here

- `mobile/package.json`: `npm test` runs Jest with the `jest-expo` preset in Node. `npm run typecheck` runs `tsc --noEmit`. `npm run lint` runs `expo lint`.
- `pyproject.toml`: `uv run pytest` collects only `tests/` (`testpaths`).

## Runtime or data flow

Knowledge tests read the bundled JSON in `mobile/assets/data/knowledge/` through `loadAssets()` in `mobile/src/core/knowledge/__fixtures__/load.ts`. Five of them also call `loadVectors()`: `engine`, `retrieve`, `retrieve_sims`, `retrieve_topk`, and `e2e_sigue`. That function reads the side-loaded `models/knowledge/index.f32.bin`, or the path in `KNOWLEDGE_VECTORS`. It throws with the regenerate command when the file is missing or its sha256 differs. `mobile/src/core/__tests__/driver.test.ts` reads `src/core/__fixtures__/replays.json`, which git ignores and `nevados_bench` export generates.

## Tests

| Behavior | Tests |
| --- | --- |
| Top-1 answer, retrieval parity with the Python export, continuation cue | `mobile/src/core/knowledge/__tests__/` |
| Safety rule detection and text folding | `safety.test.ts`, `safety_blind.test.ts` |
| Group radio reducer, lane layout, BLE wire codec, transport pairing | `mobile/src/core/group/__tests__/`, `mobile/src/group/__tests__/` |
| Chat state, preload at launch, message sources | `mobile/src/state/__tests__/` |
| Photo label kept internal, media picks | `mobile/src/vision/__tests__/photo.test.ts`, `mobile/src/core/media/__tests__/` |
| Raw colors, font names, `fontWeight`, or literal copy in UI files | `mobile/src/ui/__tests__/design-guard.test.ts` |
| Knowledge add, update, delete, and replay tool | `tests/test_add_park_knowledge.py` |
| Legacy `nevados_bench` world, FSM, guards, scoring, suites, and `export_mobile` | the other files in `tests/` |

Two benches skip unless you set an environment variable. `frameCost.bench.test.tsx` needs `BENCH=1`. `pet.bench.test.tsx` needs `PET_BENCH=1`.

Pytest skips `experiments/laya/test_retrieval_v2.py` and `experiments/media/test_build_media.py`. The media file names its own command.

## Common change paths

- Knowledge export or `policy.json`: run `npm test` in `mobile/`. Knowledge tests fail without the side-loaded vectors.
- `.agents/skills/add-park-knowledge/scripts/knowledge.py`: run `uv run pytest tests/test_add_park_knowledge.py`.
- UI files under `app/`, `src/ui/`, or `src/chat/`: the design guard scans them. `EXEMPT` skips `app/lab`, `src/ui/pet/`, and `src/ui/theme/`.

`mobile/README.md` reports that `BubblesLab.test.tsx` fails on a stale fixture. This page did not run it.

## Related docs

- [Repository checks](../../../README.md)
- [Mobile checks and known limits](../../../mobile/README.md)
- [Change paths per artifact](../../system-map.md)
