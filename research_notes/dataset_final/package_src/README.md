# LOS_NEVADOS_LAYA_FINAL_DATASET

Self-contained dataset for retraining **Laya** (`telepatia-ai/laya-pt-es-nli`, `laya==0.5.1`) as the
FAQ selector of the Los Nevados offline visitor assistant. It needs no access to the source
repository. Start with [`reports/COLAB_HANDOFF.md`](reports/COLAB_HANDOFF.md). The quality evidence
and the residual risks are in [`reports/QUALITY_REPORT.md`](reports/QUALITY_REPORT.md).

## What Laya decides

```
visitor query
  -> e5-base retrieval ("query: " prefix; gateway keeps <=5 of 15 sections, delta 0.05)
  -> 3..5 candidate FAQs (flat fill up to 3 when the gateway yields fewer)
  -> Laya `choice` over the candidate labels + "ninguna de estas opciones"
  -> prewritten answer | top-3 clarification menu | abstention
```

Laya only picks one option. Answers are prewritten in `knowledge/faq_catalog.json`, and nothing is
generated. The exact retrieval parameters are in `knowledge/sections.json` under
`retrieval_contract`. Every row in this package was built with that contract, and the app must use
the same one at inference.

## Layout

| Path | Rows | Use |
|---|---|---|
| `train/train.jsonl` | 8,275 | training (Laya choice rows) |
| `train/metadata.jsonl` | 8,275 | per-row traceability for train, joined by `meta.row_id` |
| `validation/checkpoint_selection.jsonl` | 121 | `eval_data` for epoch/checkpoint choice only |
| `validation/calibration.jsonl` | 292 | confidence thresholds, abstention and clarification only |
| `validation/unseen_topics.jsonl` | 229 | 55 FAQs whose examples are absent from train |
| `evaluation/adversarial.jsonl` | 211 | adversarial and contrastive queries, evaluated once |
| `evaluation/final_test_SEALED.jsonl` | 294 | new sealed final test, evaluated once at the end |
| `evaluation/retrospective_test_blind_READ_ONLY.jsonl` | 628 | earlier eval_v2 (dev_gate 162 + test_blind 466), rebuilt pools, for comparison only |
| `evaluation/historical_READ_ONLY.jsonl` | 1,790 | legacy rows copied verbatim, never edited, comparison only |
| `knowledge/` | | FAQ catalog (806 FAQs, 15 sections), clarification labels, confusable sets, answer policy, source manifest |
| `audit/` | | label corrections, excluded rows, unresolved ambiguities, leakage drops, safety issues, split manifest |
| `scripts/` | | validators, prediction and evaluation (standard library, apart from `--laya`/`predict.py`) |
| `scripts/build/` | | the generators that produced this package (for traceability; they need the source repo to run) |
| `MANIFEST.json` | | SHA-256, size and row count of every file |

## Row format (laya 0.5.1 choice)

```json
{"state": "<visitor query>",
 "questions": {"topic": {"type": "choice", "instructions": "...",
                         "criteria": ["<label 1>", "...", "<label k>", "ninguna de estas opciones"]}},
 "expected": {"topic": "<one criterion>"},
 "meta": {"row_id": "...", "pool": ["<faq id 1>", "..."], "gold": ["<acceptable faq ids>"], "...": "..."}}
```

- `criteria[i]` is the label of `meta.pool[i]`, and the last criterion is always `ninguna de estas opciones`.
- `meta.gold` lists every acceptable FAQ id. The target is `ninguna de estas opciones` when no
  acceptable id is in the pool.
- Laya ignores `meta`. The trace fields (`canonical_id`, `acceptable_ids`, `candidate_ids`,
  `candidate_cosines`, `gate_sections`, `pool_source`, `provenance`, `review_status`, `outcome`,
  `none_cause`, `decision_reason`, `family`) are inline in eval rows and in `train/metadata.jsonl`
  for train rows.
- Eval rows with outcome `multi_positive` or `clarify` have `expected: {}`. Laya's trainer skips
  those rows, and `evaluate_predictions.py` scores them against `meta.gold`.

## Verify before use

```bash
python scripts/verify_manifest.py      # hashes and row counts
python scripts/validate_dataset.py     # contract, ids, labels, traceability
python scripts/validate_splits.py      # split separation by FAQ id, family and text
python scripts/check_leakage.py        # exact and near-duplicate leakage
```

Each script exits non-zero on any failure.
