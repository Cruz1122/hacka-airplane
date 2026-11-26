# Repository workflow

## Purpose

This page maps the repository root: entry files, check commands, and paths that git does not track. Subsystem detail lives in the linked docs.

## Start here

- [`README.md`](../../../README.md) has the repository map table, the fresh-clone run steps, and the checks.
- [`docs/system-map.md`](../../system-map.md) lists every data flow with its script, and what to redo when one node changes.
- [`mobile/AGENTS.md`](../../../mobile/AGENTS.md) holds the rules for agents that edit the Expo app.
- `.claude/skills/` holds the project skills `app-design`, `hackathon-lean`, and `mobile-offline-stack`. `.claude/skills/add-park-knowledge` is a symlink to `.agents/skills/add-park-knowledge`.

The repository has three uv projects, and each one has its own `pyproject.toml` and `uv.lock`:

| Project | Name | Package or role |
|---|---|---|
| `pyproject.toml` | `nevados-bench` | Builds `src/nevados_bench` with hatchling. Dev group has `pytest` and `ruff`. |
| `experiments/nlu/pyproject.toml` | `nevados-nlu` | Torch and sentence-transformers for the e5 fine-tune and evaluation. |
| `experiments/laya/pyproject.toml` | `laya-exp` | The Laya track. `docs/architecture.md` runs `export_nlu.py` in this environment. |

`mobile/` is a separate npm project with its own `package.json`.

## Tests

```bash
uv run pytest                          # repo root, collects tests/ only
uv run ruff check                      # repo root, config in pyproject.toml
cd mobile && npm run typecheck && npx expo lint && npm test
```

`testpaths = ["tests"]` limits pytest to `tests/`. Fifteen files there import `nevados_bench`. `tests/test_add_park_knowledge.py` runs `.agents/skills/add-park-knowledge/scripts/knowledge.py`. The default run skips `experiments/media/test_build_media.py`. The repository has no CI configuration.

## Common change paths

- To change knowledge, use the `add-park-knowledge` skill, then follow "Changing the knowledge" in the README.
- To change `src/nevados_bench`, rerun `uv run python -m nevados_bench.export_mobile`. It writes `mobile/assets/data/world.json` and two fixtures.

A fresh clone lacks these ignored paths:

- `models/*` except `models/README.md`. Check the files with `sha256sum -c models.sha256`.
- `results/`, `data/finetune/`, `*.zip`, and `experiments/nlu/work/emb_cache/`.
- `mobile/android/` and `mobile/ios/`, which `npx expo prebuild` generates (`mobile/.gitignore`).
- `mobile/src/core/__fixtures__/*.json`, written by `uv run python -m nevados_bench.export_mobile`.
- `research_notes/dataset_final/out/` and the raw evidence folders under `research_notes/`.

Do not edit generated files by hand. The `export_mobile.py` docstring says this for its fixtures.

## Related docs

- [`docs/README.md`](../../README.md) indexes the current docs and the superseded `docs/history/`.
- [`docs/architecture.md`](../../architecture.md#regenerating-the-assets) has the asset regeneration command.
- [`mobile/README.md`](../../../mobile/README.md#prerequisites) has the toolchain table.
- [`models/README.md`](../../../models/README.md) has the model file layout.
