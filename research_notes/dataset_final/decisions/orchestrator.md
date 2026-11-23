# Orchestrator decision log (final dataset phase, 2026-11-22)

- Diagnosis: laya_ft_v2 rows were built without masking the originating example (gold always
  first at cosine 1.0, gateway always the gold section) and skipped 71% of rows with pools <3.
  Decision: regenerate every training row from the corpus with the self-mask applied to the gateway
  and the entry scores, plus a documented flat fill to reach 3 candidates.
- Pair review scope: decisive pairs (all candidates in none-target rows, candidates ranked above
  gold) with answer-short e5 cosine >= 0.88 and not already curated as hard negatives must be judged;
  a train row with any unjudged such pair is excluded (pending_pair_review). Pairs below 0.88 are
  `auto_low_similarity` (reported, not hidden).
- Doubt policy: query_dependent and mislabeled pair verdicts drop the row from training; also_answers
  adds the candidate to acceptable_ids (logged in label_corrections); multi-positive rows never train.
- L3 design review (REJECT, 9 findings): applied 1 (pending pairs block train regardless of review
  status), 2 (X1 routed by FAQ pair so a contrast never spans train and eval; adversarial rows still
  train because the mission asks for verified adversarial negatives in train), 3 (self-mask covers
  identical owner texts), 4 (safety/action kinds never held out), 6 (retrospective rows in the
  cross-split near-duplicate check, they win), 7 (pair_sim and pairs_todo hashed), 8 (verdict enum
  validated), 9 (historical validated, unknown ids reported). Declined 5: at inference the query is
  never in the index, so masking it in the gateway as well is the faithful simulation; the
  reference retrieval.py mask only served LOO scoring.
- Recomputed pools after the fixes: 55 unseen topics, 9,588 candidate rows, 248 new high-similarity
  pairs → shard W3 (L3).
- G2 (fees/contradictions): L1 asked to revise 9/9 ops (missing Res. 551 amounts, consultation dates,
  vehicle rows, night-entry scope, porter quote) → G2 fix round writes G2v2.json; L1 re-reviews.
- G2v2: L1 re-review 9/9 approve → applied. G1: H4 2/2 approve → applied.
- G1b: H4 approved services.mule_luggage_registered_only; geography.rios_lagunilla_recio = revise
  (attributes IDEAM "Alto Magdalena" zone to Recío; the table gives it only for Lagunilla) → left out,
  no further round (the pair is query_dependent, so its rows are already out of training); listed as
  residual in QUALITY_REPORT.
- Verifier `fix` verdicts (249) are not self-approving: arbitrated by L2/L3 together with a 30-row
  audit sample of each lenient verifier's `ok` rows (G5, G6).
- Final pair shards: W3 (L3, 248) after the L3 fixes and W4 (H2, 50) after the factual apply; 0
  pending high-similarity pairs remain, so `pending_pair_review` excludes no row.
- Factual apply: 26 ops (FINAL_APPROVED.json); left out after their last round:
  geography.rios_lagunilla_recio, access.confirm_road_before, access.stay_on_official_gate,
  services.quindio_dulima. Indexed texts (labels/examples) unchanged, so R@k before/after this
  phase is identical by construction.
- Packaging fixes: every row now carries `decision_reason`; `multi_positive` rows get `expected: {}`
  like `clarify`; retrospective ambiguous rows get outcome `clarify`; package scripts add their own
  dir to sys.path because the clean-copy checks run with `python -I`.
- Baseline without training: base Laya (pinned revision) and first-option baseline scored on every
  eval split by `scripts/predict.py` + `evaluate_predictions.py`; numbers in QUALITY_REPORT §6.
- Emergency vs clarify: ambiguous rows whose acceptable ids include an emergency_direct FAQ keep a
  direct target (flag `emergency_overrides_clarify`), because the app bypasses the menu for them
  (10 rows: calibration 4, final_test 2, retrospective 4). Rule-driven; prompts, pools and row ids
  unchanged (hash-checked), so the base-model predictions still apply.
- Error taxonomy: candidate_none (outcome), retrieval_miss / true_out_of_scope (none_cause) are row
  properties; reranking_error is per prediction, reported by evaluate_predictions.py.
