# Python benchmark package (`src/nevados_bench`)

## Purpose

`nevados_bench` is the legacy Python package from the LLM era. Today its one live output is `mobile/assets/data/world.json`, plus the parity fixtures for the legacy Jest tests. The knowledge chat does not read any of it. See [`system-map.md`](../../system-map.md) and [`architecture.md`](../../architecture.md).

## Start here

- `pyproject.toml` defines the `nevados-bench` package for Python 3.12 or later. Hatchling builds `src/nevados_bench`. Dev tools are `pytest` and `ruff` with line length 100. `testpaths` is `["tests"]`.
- `schemas.py` holds the shared pydantic contracts, such as `Case`, `Dialogue`, `ToolCall`, `PromptRequest`, and the `LLMBackend` protocol.
- `world/` builds the synthetic park in code. `load_world()` reads no files.
- `fsm/` contains `states`, `prompts`, `parse`, and `driver.run_dialogue`. `guards.py` and `values.py` do the deterministic checks and value normalization.
- `suites/` returns cases from functions such as `generate_fc_core`, `generate_dialogues`, and `generate_grounded_qa`. `scoring/grounding.py` scores `answer` calls.

## Runtime or data flow

The package has no console script. It runs as three `python -m` modules.

1. `uv run python -m nevados_bench.export_mobile` writes `assets/data/world.json` and `src/core/__fixtures__/{prompts,replays}.json` under `--out-dir`, which defaults to `mobile`. It reads `--suites-dir`, which defaults to `data/suites`. Git ignores the fixtures and tracks `world.json`.
2. `finetune.generate` replays scripted dialogues through `run_dialogue` and writes JSONL. The default output is `data/finetune/examples.jsonl`, and that directory does not exist in the repo. The docstring says `--out data/finetune`, but the code treats `--out` as a file path.
3. `finetune.render` posts each row to llama-server `/apply-template` and splits the rows into `train.jsonl` and `dev.jsonl`.

The `schemas.py` and `suites/speed.py` docstrings still mention `runner` and `report` packages. Commit `3af9e3de` deleted them. No code in the repo writes `data/suites/*.jsonl` (inferred from grep).

## Tests

Run `uv run pytest` from the repo root. Most modules have a `tests/test_<area>_<module>.py` file, such as `test_fsm_driver.py`. No test imports `finetune` directly. `tests/test_export_mobile.py` covers part of it, because `export_mobile` calls `G.ScriptBuilder`, `G._TrainSim`, and `G.single_turn`.

## Common change paths

- A world or FSM constant changes. Edit the source module, rerun `export_mobile`, and check `mobile/src/core/__tests__/`.
- A new contract field goes into `schemas.py` first, because every subpackage imports it.

## Related docs

- [`system-map.md`](../../system-map.md), rows for `src/nevados_bench/`
- [`README.md`](../../../README.md)
- [`history/metrics.md`](../../history/metrics.md)
