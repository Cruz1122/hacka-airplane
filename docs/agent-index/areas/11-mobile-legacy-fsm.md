# Mobile legacy FSM

## Purpose

`mobile/src/core/*.ts`, outside `group/`, `knowledge/`, and `media/`, is a TypeScript port of the Python `nevados_bench` dialogue FSM. The chat no longer runs it. Each file names its Python source in its first line comment, for example `src/nevados_bench/fsm/driver.py`.

## Start here

- `driver.ts`: `DialogueRun.turn()` handles one user message. `runDialogue()` replays a scripted dialogue. `StepResult` records each step.
- `states.ts`: state names, `TRANSITIONS`, `FLOW_STATE`, `REQUIRED_SLOTS`, `visibleTools()`, and `toolTopic()`.
- `world.ts`: `loadWorld()` caches a `World` built from `mobile/assets/data/world.json`. The class has a JSON Schema subset validator in `validateArguments()`.
- `prompts.ts` has `buildRequest()`. `parse.ts` has `parseOutput()`, which never throws.
- `guards.ts` has `guardRoute()` and `guardAnswer()`. Guards only remove answers or arguments.
- `tools.ts`: `executeTool()` returns deterministic mock results, with a pure-TS SHA-256 in `stableHash()`.
- `values.ts`: text normalization and value extraction for the guards.
- `types.ts`: `LLMBackend`, `PromptRequest`, `Completion`, and the benchmark `Case` shape.

## Runtime or data flow

`turn()` routes from a boundary state (`ROUTER`, `ANSWER`, `OUT_OF_SCOPE`, `CLARIFY`) or continues `SLOT_FILLING` or `CONFIRM`. Each model call goes through `buildRequest`, `LLMBackend.complete`, and `parseOutput`. When `guards` is set, `guardRoute` checks the call. A flow tool enters slot filling. Other tools run through `executeTool` and an answer step.

Verified callers outside `core/`:

- `app/settings.tsx` reads `loadWorld().json.stations`. It also uses `modelManager`.
- `src/llm/{llamaRn,fake,modelManager}.ts` import `LLMBackend` and related types from `core/types`.
- `src/state/messageSources.ts` takes a `World`. Its only non-test caller is `src/design/fixtures.ts`.
- `src/ui/DebugPanel.tsx` imports the `StepResult` type. No file imports `DebugPanel`.

No app code constructs `DialogueRun`. Only tests do. `mobile/README.md` still says the debug panel uses these types, and that claim is stale.

## Tests

`mobile/src/core/__tests__/`:

- `driver.test.ts` replays `__fixtures__/replays.json` and ports `tests/test_guards.py`.
- `prompts.test.ts` checks `buildRequest` against `__fixtures__/prompts.json`, plus `parseOutput`.
- `tools.test.ts` checks `executeTool` against the replays and checks the values parity.
- `chat.test.ts` covers chat mode with `FakeBackend`.

Both fixtures are gitignored. A fresh checkout fails `driver`, `prompts`, and `tools` tests until you run `uv run python -m nevados_bench.export_mobile`. `src/core/knowledge/__tests__/engine.test.ts` fails if any knowledge module imports these files.

## Common change paths

- Data or constant change: edit the Python source and rerun `export_mobile`. Never edit `world.json` or the fixtures by hand.
- Removal: the settings screen controls go first, as `docs/architecture.md` says.

## Related docs

- [Architecture, Legacy](../../architecture.md#legacy)
- [System map, flow 8](../../system-map.md#8-legacy-llm-era-still-wired-to-one-screen)
- [Mobile README](../../../mobile/README.md)
