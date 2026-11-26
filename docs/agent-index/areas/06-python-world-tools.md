# Python world tools

## Purpose

`src/nevados_bench/world/` builds the fictional four-station park "Sierra de Aldara" that the benchmark suites, the FSM, and the guards use. `src/nevados_bench/export_mobile.py` serializes that world and the Python FSM constants to JSON for the legacy TypeScript port in `mobile/src/core/`. The current knowledge chat does not read these files. See [system-map.md](../../system-map.md).

## Start here

- `world/corpus.py`: `STATIONS`, `TRAILS`, `build_passages()` (IDs `EST-<code>-NN`, `PAR-NN`, and injection `INJ-NN`), `build_filler()` (`INF-NNN`, digit-free), `stable_hash()`, and `INJECTION_FIELD`.
- `world/tools.py`: `build_tools()` returns 24 base tools from `_BASE` and 24 clones from `_CLONES`.
- `world/model.py`: `World`, `load_world()` (cached with `functools.cache`), and `World.execute_tool()`, a mock dispatcher that returns passage IDs plus `data`.
- `export_mobile.py`: `build_world_json()`, `build_prompts()`, `build_replays()`, and `export()`.

## Runtime or data flow

1. Run `uv run python -m nevados_bench.export_mobile`. It calls `load_world()`, then reads `data/suites/{fc_core,smoke,dialogues,grounded_qa}.jsonl`.
2. It writes `mobile/assets/data/world.json`. The `exec` block holds `_EXEC_RULES`, a table form of `World.execute_tool`. It also holds `model._PARK`, `_ITEM_RULES`, and `hash_vectors` for `stable_hash` parity.
3. It writes `mobile/src/core/__fixtures__/prompts.json` and `replays.json`. `.gitignore` ignores both files.
4. `mobile/src/core/world.ts` imports `world.json`. `tools.ts`, `states.ts`, `prompts.ts`, and `driver.ts` read it. At runtime only `mobile/app/settings.tsx` and `src/design/fixtures.ts` call `loadWorld()`.

`build_world_json()` raises `RuntimeError` when a base tool has no `_EXEC_RULES` entry. This page does not trace which code writes `data/suites/*.jsonl`.

## Tests

- `tests/test_world_corpus.py`: counts, value uniqueness, and the rule that injection passages are never indexed.
- `tests/test_world_tools.py`: 24 base and 24 clone tools, argument validation, and letter-only codes.
- `tests/test_export_mobile.py`: `_interpret()` reads the `exec` table and must equal `execute_tool` for every enum combination.
- TS parity: `mobile/src/core/__tests__/{prompts,driver,tools}.test.ts` read the ignored fixtures, so run the export first.

## Common change paths

- New or changed base tool: edit `tools.py` `_BASE`, the `match` in `model.py`, and `_EXEC_RULES`. Then mirror the change in `mobile/src/core/tools.ts`. That last step is inferred from `tools.ts` line 1.
- Corpus value: edit `corpus.py` `_STATION_VALUES` or `_PARK_ROWS`. Then re-export.

## Related docs

- [architecture.md](../../architecture.md) lists the legacy modules.
- [mobile/assets/data/README.md](../../../mobile/assets/data/README.md) lists the generated files.
- [mobile-offline-stack skill](../../../.claude/skills/mobile-offline-stack/SKILL.md) covers the export contract.
