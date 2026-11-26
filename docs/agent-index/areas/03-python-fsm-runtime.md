# Python FSM runtime

## Purpose

`src/nevados_bench/fsm/` runs a free-run dialogue. The model's own outputs move the FSM state, and code validates tool calls, asks for missing slots, and confirms side-effect tools. This code is legacy Python. Outside tests, only `export_mobile.py` and `finetune/generate.py` run the driver. `suites/fc.py`, `suites/grounded.py`, and `suites/dialogues.py` import `states` or `prompts`.

## Start here

- `driver.py`: `_Run` (public alias `DialogueRun`) and `run_dialogue`. Every step is a `StepResult`.
- `states.py`: state names, `TRANSITIONS`, `REQUIRED_SLOTS`, `SLOT_QUESTIONS`, and `visible_tools`.
- `prompts.py`: `build_request` turns a `Case` into a `PromptRequest`.
- `parse.py`: `parse_output` turns a `Completion` into a `ParsedOutput` and never raises.

## Runtime or data flow

1. `_Run.turn` dispatches on `self.state`. `ROUTER`, `ANSWER`, `CLARIFY`, and `OUT_OF_SCOPE` go to `_turn_router`. `SLOT_FILLING` and `CONFIRM` have their own handlers.
2. `_call` runs `build_request`, then `backend.complete`, then `parse_output`.
3. `_dispatch` starts a flow for tools in `FLOW_STATE`. For other tools it runs `world.execute_tool`, then `_answer`.
4. `_record` calls `check_path`, so an illegal transition raises `ValueError`.
5. `CONFIRM` executes in code only. `is_affirmative`, `is_cancel`, and `is_plain_negative` decide the turn.

With `guards=True`, `_guard_call`, `_is_correction`, and `_answer` call `nevados_bench.guards` (`guard_route`, `guard_answer`, `grounded_args`).

## Tests

- `tests/test_fsm_states.py`: transition table and required slots against tool schemas.
- `tests/test_fsm_parse.py`: native, uniform, and malformed outputs.
- `tests/test_fsm_prompts.py`: request shapes, prefix caching, and the pinned `DEFAULT_PROMPTS_SHA256`.
- `tests/test_fsm_driver.py`: scripted dialogues with `ScriptedBackend` and `SlotAwareBackend`.
- `tests/test_suites_dialogues.py` replays gold traces through `run_dialogue`.

## Common change paths

- Parsing: edit `parse.py` and `tests/test_fsm_parse.py`.
- Transitions: edit `TRANSITIONS` and the driver path that records the new edge.
- Prompts: the default prompts must stay byte-identical because fine-tuning data comes from them. Add an opt-in option, as `ExtractLayout` does.
- Guards: logic lives in `src/nevados_bench/guards.py`. The driver only decides when to call it.
- Code reply strings: `suites/dialogues.py` copies the cancel replies, so update both files.

After any change, regenerate the fixtures with `uv run python -m nevados_bench.export_mobile`. The TypeScript port in `mobile/src/core/` must match.

Gap: no benchmark entry point in `src/` runs the driver against a real model.

## Related docs

- [System map, legacy flow](../../system-map.md)
- [Architecture](../../architecture.md)
