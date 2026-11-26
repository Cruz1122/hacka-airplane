# Python scoring

## Purpose

`src/nevados_bench/scoring/` holds one module, `grounding.py`. It scores an `answer` call for grounding and hallucination against the passages that the model saw. The module docstring defines the value model and the outcome labels. Read it before you change a rule.

## Start here

- `score_answer(record, case, passages, gazetteer)` is the scorer.
- `evidence_values(text)` applies the non-evidence rule. Integers below `SMALL_NUMBER_LIMIT` (10) and list markers that match `_ENUM_LINE` or `_ENUM_PAREN` do not count as stated values.
- `index_gazetteer`, `detect_language`, and `has_ngram_loop` are helpers that `score_answer` calls.

## Runtime or data flow

Inputs are the `RequestRecord`, `Case`, `Passage`, and `GazetteerEntry` models in `src/nevados_bench/schemas.py`. The scorer reads `record.parsed.answer_text` and falls back to `record.completion.content`. It also reads `case.gold`, `case.passage_ids`, `case.language`, and `case.tags`. `generate_grounded_qa` in `src/nevados_bench/suites/grounded.py` builds `answer` cases and sets the `safety` and `injection_marker` tags.

The output is a flat dict of flags. `outcome` holds one label from the docstring list. Flags that do not apply to the case are `None`. `correct` repeats `grounded_correct`.

Consumers at HEAD:

- `score_answer` has no caller outside the tests. Commit `3af9e3de` deleted its old caller, `report/aggregate.py`.
- `src/nevados_bench/guards.py` calls `evidence_values`.
- `build_world_json` in `src/nevados_bench/export_mobile.py` exports `SMALL_NUMBER_LIMIT`, `_ENUM_LINE`, and `_ENUM_PAREN` under the `grounding` key of `world.json`.
- `mobile/src/core/values.ts` reads that key in `stripEnumerations` and `evidenceValues`. `mobile/src/core/world.ts` declares its type.

## Tests

- `tests/test_scoring_grounding.py` covers each outcome, the non-evidence rule, degenerate output, citations, language, and injection.
- `tests/test_scoring_fixtures.py` supplies `PASSAGES`, `GAZETTEER`, `ANSWER_CASES`, `answer_case`, `answer_output`, `completion`, and `record`. No other test imports its route, extract, or dialogue builders.
- `tests/test_guards.py` covers `evidence_values` through the guard.
- No test checks the exported `grounding` key. `tests/test_export_mobile.py` does not mention it.

## Common change paths

If you change the non-evidence rule or rename the private regexes, update `guards.py`, `export_mobile.py`, `values.ts`, and `world.ts` together. Then regenerate `world.json`.

## Related docs

- [Metric catalog section 5](../../history/metrics.md) describes the removed aggregate report.
- [System map](../../system-map.md) shows the `world.json` export.
- [Architecture](../../architecture.md) lists what still reads `world.json`.
