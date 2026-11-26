# Python benchmark suites

## Purpose

`src/nevados_bench/suites/` generates the legacy LLM benchmark cases from the world model. `data/suites/*.jsonl` holds the materialized output. No current code regenerates those files. The writer, `build_suites` in `batches.py` behind `nevados-bench build-suites`, was deleted in commit `3af9e3de`. Running the four generators today reproduces all six committed files byte for byte. This was checked on 2026-11-25 by comparing `model_dump_json()` output to each file.

## Start here

- `src/nevados_bench/schemas.py` defines `Case`, `Gold`, `ToolCall`, `Dialogue`, and `DialogueTurn`. Each line of `smoke`, `fc_core`, `fc_tools_sweep`, `fc_ctx_sweep`, and `grounded_qa` is one `Case`. Each line of `dialogues.jsonl` is one `Dialogue`, and its `turns[].steps` are `Case` objects.
- `suites/fc.py` holds the function-call cases. Hand-authored queries live in `CALL_QUERIES` (keyed by tool), `NONE_QUERIES`, and `CLARIFY_QUERIES`, each a `Query`. `core_queries()` orders them. `CORE_TOOL_SETS` holds the visible tool lists. The entry points are `generate_fc_core`, `generate_smoke` (copies of `fc_core` cases), `generate_fc_tools_sweep`, and `generate_fc_ctx_sweep`. The sweeps use `sweep_queries()`.
- `suites/dialogues.py` holds the dialogue cases. `SCRIPTS` holds 36 scripts built from the turn types `Ask`, `Start`, `Fill`, `Correct`, `Confirm`, and `Cancel`. `_Sim` mirrors `fsm.driver` and turns each script into step cases. `simulate()` returns traces and `generate_dialogues()` returns `Dialogue` objects.
- `suites/grounded.py` holds `QUESTIONS`, `INJECTIONS`, `build_bundles`, and `generate_grounded_qa`.
- `suites/speed.py` holds `text_source`, the filler text for the deleted `runner.speed` protocol.

## Runtime or data flow

`nevados_bench.world.load_world()` feeds the generators. The committed JSONL files have these readers:

- `export_mobile.build_prompts` reads `fc_core`, `smoke`, `dialogues`, and `grounded_qa`. `export_mobile.build_replays` also reads `dialogues.jsonl`.
- `finetune/generate.py:suite_texts` reads every file in `data/suites/` so that held-out benchmark texts are dropped from training data.

## Tests

`tests/test_suites_fc.py`, `test_suites_dialogues.py`, `test_suites_grounded.py`, and `test_suites_speed.py` call the generators in memory. They never read `data/suites/`. A stale JSONL file therefore passes every test.

## Common change paths

1. Edit a query table or a script in the module.
2. Regenerate the JSONL. No script exists for this step. The deleted `build_suites` wrote one `model_dump_json()` line per item.
3. Rerun `python -m nevados_bench.export_mobile`, because its fixtures derive from these files.

## Related docs

- [System map, legacy export path](../../system-map.md)
- [Metric and tag definitions](../../history/metrics.md)
- [Project context and run history](../../history/project-context.md)
