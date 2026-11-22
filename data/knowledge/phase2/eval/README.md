# Phase 2 evaluation set — PNN Los Nevados

Questions written by Grok 4.7 (non-Claude) from each entry's id, label and `answer.short` only
(`coordination/eval_tools.py dump`); the writers never saw the training `examples`.

| File | Rows | Expected |
|---|---|---|
| `paraphrase.<section>.jsonl` | 1,752 | the entry id(s) that answer the question (≥ 2 rows per entry, all 806 entries) |
| `near_miss.jsonl` | 80 | `[]` (park question with no data in the corpus → fallback), except 3 rows re-pointed on 2026-11-21 to entries that now answer them |
| `out_of_scope.jsonl` | 80 | `[]` (not about the park) |

Row fields: `q`, `expected` (list; more than one id means any of them is correct). Optional:

- `near_copy: true` — the question turned out to be a near-copy (e5-base cosine ≥ 0.95) of a training example
  of its own entry. Kept for reference; report accuracy on the clean subset (rows without `near_copy`) and on
  this subset separately.
- `replaces_near_copy: "<question>"` — the replacement row written for that near-copy.

Known bias: the questions were written from the answers, so they reuse answer vocabulary; real tourist
phrasing will be harder. Checks: `python3 coordination/eval_tools.py check` (ids, duplicates, exact example
matches) and `cd experiments/laya && uv run python <N>/coordination/eval_leakage.py` (0 in the clean subset).
