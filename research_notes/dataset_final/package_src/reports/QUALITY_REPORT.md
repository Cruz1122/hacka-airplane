# Quality report: Los Nevados Laya dataset (final phase, 2026-11-22)

This report covers only what was measured. It states unreviewed and unmeasured items explicitly.
Laya was **not retrained**, and no phone benchmark was run in this phase.

## 1. Contents

| Split | Rows | positive | none | multi_positive | clarify |
|---|---:|---:|---:|---:|---:|
| train | 8,275 | 5,997 | 2,278 | 0 | 0 |
| checkpoint_selection | 121 | 84 | 37 | 0 | 0 |
| calibration | 292 | 109 | 100 | 45 | 38 |
| unseen_topics | 229 | 166 | 44 | 10 | 9 |
| adversarial | 211 | 95 | 103 | 13 | 0 |
| final_test_SEALED | 294 | 185 | 61 | 20 | 28 |
| retrospective (READ_ONLY) | 628 | 356 | 216 | 38 | 18 |
| historical (READ_ONLY) | 1,790 | verbatim legacy copy | | | |

- Knowledge: 806 FAQs, 15 sections and 10,297 visitor examples.
- Train covers 749 distinct gold FAQs.
- 55 FAQs are held out as unseen topics: 8% stratified by section. Sections `actions` and
  `conversation` and kinds `safety` and `action` are never held out.
- `none_cause` in train: 2,192 `retrieval_miss` (an in-scope query whose acceptable FAQ was not
  retrieved) and 86 `true_out_of_scope`.
- Train provenance: 8,027 corpus examples, 143 synthetic rows and 105 adversarial rows. All 248
  authored train rows were verified cross-model.
- Pool size in train: 5 candidates in 5,846 rows, 4 in 555 and 3 in 1,874. 1,279 train rows used the
  flat fill.
- **Position bias**: 4,234 of 5,997 positive train targets (71%) are option 1, because options
  follow e5 order. Train with `shuffle_options=("choice",)` and always report the first-option
  baseline.

## 2. How rows were built

- **Self-mask.** Each corpus example is used as a query. Its own vector, and any identical text of
  the same FAQ, is masked in both the gateway and the entry scores. This simulates inference, where
  the query is never in the index. The earlier `laya_ft_v2` rows were built without the mask: gold
  was always first at cosine 1.0, and 71% of rows were dropped for pools under 3. Every row here
  was regenerated.
- **Flat fill.** It brings the pool to at least 3 candidates, matching the app contract in
  `knowledge/sections.json`.
- **Labels.** The target is the single acceptable FAQ in the pool. When no acceptable FAQ is in
  the pool, the target is `ninguna de estas opciones`. Rows with more than one acceptable FAQ in the
  pool never go to train; they go to eval as `multi_positive`.
- **Decisive pairs.** These are, in none-target rows, every candidate; in positive rows, the
  candidates ranked above gold. A pair whose answer-short e5 cosine is at least 0.88, and that is
  not a curated hard negative, needed an independent judgment.
  - 2,540 such pairs were judged: 1,746 distinct, 588 query_dependent, 197 also_answers and 9
    mislabeled (`audit/split_manifest.json → inputs_sha256.pair_judgments`).
  - `also_answers` adds the candidate to the acceptable ids.
  - `query_dependent` and `mislabeled` drop the row from train.
  - A train row with any unjudged high-similarity pair is excluded. Zero such pairs remain.
- **Authored rows.** 1,504 rows were authored: 7 batches across Gemini and Grok. Each was verified
  by another model, and every `fix` verdict (249) was arbitrated by L2 or L3 (Luna).

### Train review status (honest share)

| review_status | rows | meaning |
|---|---:|---|
| no_decisive_pair | 4,069 | gold ranked first and no candidate above it; label follows from corpus ownership, **not individually reviewed** |
| auto_low_similarity | 2,734 | every decisive pair is below 0.88 answer similarity; **not individually reviewed** |
| pairs_verified | 839 | every high-similarity decisive pair judged by an independent reviewer |
| label_audit | 385 | covered by the curation-v2 label audit |
| verified:ok / verified:fix | 219 / 29 | authored rows, cross-model verified (and arbitrated when `fix`) |

That makes 6,803 of 8,275 train rows (82%) carry labels derived by rule from FAQ ownership plus
the similarity screen, without a per-row review. That is the main residual label risk.

## 3. Corrections and exclusions

- **Label corrections:** 735 (`audit/label_corrections.jsonl`), from also_answers judgments,
  label-audit fixes and authored-row fixes.
- **Excluded rows:** 1,890 (`audit/excluded_examples.jsonl`).

| Reason | Rows |
|---|---:|
| pair_query_dependent | 1,337 |
| leak_vs_train (eval row too close to train) | 241 |
| multi_positive_in_pool (train) | 209 |
| near_duplicate_across_eval | 64 |
| verifier_drop | 17 |
| label_audit_case_D | 16 |
| leak_vs_retrospective_sealed | 6 |

- **Unresolved ambiguities:** 1,663 (`audit/unresolved_ambiguities.jsonl`). These rows were kept
  out of train and are listed for later review.

## 4. Split separation and leakage

Splits are separated by FAQ id (unseen topics), by family (each paraphrase family or X1 contrast
pair goes to one split) and by text. They are **not** separated by provenance.

- Train keeps 105 verified adversarial-provenance rows (X1 and X3 families routed to train) so
  that the model sees verified adversarial negatives.
- Those families never appear in an eval split.
- This departs from L3's finding 2, which asked to keep all adversarial provenance out of train.
  It was applied partially (X1 routed by pair) and is logged in `reports/DECISION_LOG.md`.

Each of these passes on the extracted ZIP:

- `validate_splits.py`:
  - No unseen FAQ id appears in train gold or acceptable ids.
  - No unseen gold appears in selection or calibration.
  - No family spans two splits (1,095 families checked).
  - No normalised text appears in two splits (9,422 texts).
- `check_leakage.py`: zero exact matches and zero trigram-Jaccard ≥0.8 matches between train and any
  eval split.
- Build-time semantic filter (e5 cosine ≥0.93):
  - Eval rows too close to train were dropped (241).
  - Train rows too close to the sealed retrospective set were dropped.
  - Cross-eval near-duplicates were removed. Priority for keeping a row: retrospective, then final,
    adversarial, unseen, calibration, checkpoint.
  - `check_leakage.py --semantic` re-runs the e5 check. It needs the e5 download.
- Routing by family hash, with seed 20261126:
  - Each contrastive X1 pair goes to one split.
  - Ambiguous authored rows go only to calibration or eval.
  - Rows whose gold is held out go to `unseen_topics`.

## 5. Retrieval recall (e5 contract, no training needed)

Recall@k: an acceptable FAQ is among the first k candidates of the app pool.

| Split (n) | before curation v2 R@1/3/5 | after final phase R@1/3/5 |
|---|---|---|
| checkpoint_selection (98) | 0.622 / 0.796 / 0.847 | 0.653 / 0.806 / 0.857 |
| calibration (175) | 0.686 / 0.863 / 0.897 | 0.709 / 0.846 / 0.880 |
| final_test (239) | 0.619 / 0.820 / 0.854 | 0.636 / 0.837 / 0.858 |
| adversarial (122) | 0.615 / 0.828 / 0.869 | 0.639 / 0.836 / 0.885 |
| retrospective (451) | 0.597 / 0.820 / 0.865 | 0.610 / 0.838 / 0.874 |

Rows: answerable rows with outcome positive, multi_positive, or candidate_none with a known
acceptable FAQ. Clarify rows are excluded (`scripts/build/stats.py --recall`).

- The final-phase factual operations changed answers and sources only, not labels or examples. So
  recall before and after this phase is identical; this was verified as 0 indexed-text diffs.
- Calibration lost some R@3 and R@5 against the pre-curation corpus.
- About 11–15% of answerable queries never reach Laya with their FAQ in the pool. That is the
  ceiling for any retrained Laya. The rows carry `none_cause=retrieval_miss` so abstention on them
  is measured separately.

## 6. Base model, before training

Scored on every eval split with the pinned base checkpoint (`scripts/predict.py` on CPU, then
`scripts/evaluate_predictions.py`). These are **untrained baselines**, not results. No build
decision was changed after these numbers were seen.

Accuracy with Wilson 95% intervals. A row counts as correct when Laya picks an acceptable FAQ, or
picks `ninguna` when no acceptable FAQ is in the pool.

| Split (n) | base Laya, all rows | first option (= e5 top-1), all rows | base Laya, none rows | base Laya, positive rows |
|---|---|---|---|---|
| checkpoint_selection (121) | 41.3% [32.9, 50.2] | 52.9% [44.0, 61.6] | 29.7% | 46.4% |
| calibration (292) | 41.1% [35.6, 46.8] | 49.7% [44.0, 55.4] | 22.0% | 47.7% |
| unseen_topics (229) | 42.8% [36.6, 49.3] | 59.8% [53.4, 66.0] | 15.9% | 47.0% |
| adversarial (211) | 35.5% [29.4, 42.2] | 37.0% [30.7, 43.7] | 28.2% | 43.2% |
| final_test_SEALED (294) | 43.9% [38.3, 49.6] | 57.1% [51.4, 62.7] | 21.3% | 50.3% |
| retrospective (628) | 34.6% [30.9, 38.4] | 45.1% [41.2, 49.0] | 13.4% | 44.4% |

- The first-option baseline is right on positive rows about 69–77% of the time, and right on
  none rows never, by construction.
- Base Laya is below e5 top-1 on every split. It abstains correctly on only 13–30% of none rows.
- The fine-tune must beat **first option** on positive rows and lift none-row accuracy. Matching
  the base model is not enough.
- Top-3 by base Laya probability contains an acceptable FAQ in 71–92% of `clarify` and
  `multi_positive` rows (final_test 70.8% of 48). This number comes from Laya's probabilities, so
  it is identical in the baseline run.
- Full breakdowns, by outcome, `none_cause`, scenario and provenance, are reproducible with
  section 6 of `COLAB_HANDOFF.md` run on the base checkpoint.

### Error taxonomy (mission 6.1)

The four result types are kept apart. Two are row properties stored in `meta`; one is a property
of a decision, computed by `evaluate_predictions.py` (`error=` lines).

| Type | Where | Definition |
|---|---|---|
| `candidate_none` | `meta.outcome` | no acceptable FAQ among the candidates; target `ninguna` |
| `retrieval_miss` | `meta.none_cause` of a candidate_none row | an acceptable FAQ exists in the base but was not retrieved |
| `true_out_of_scope` | `meta.none_cause` of a candidate_none row | no FAQ covers the query, or it asks for a function the app does not have |
| `reranking_error` | evaluator, per prediction | an acceptable FAQ is in the pool but the decider chose another option or `ninguna` |

The evaluator also reports `false_answer:<none_cause>`: an FAQ was picked on a candidate_none row.

Errors of the untrained base, as a share of all rows:

| Split | reranking_error | false answer, retrieval_miss | false answer, out of scope |
|---|---|---|---|
| final_test_SEALED | 37.4% | 11.6% | 7.1% |
| unseen_topics | 41.0% | 16.2% | 0% |
| adversarial | 29.4% | 4.3% | 30.8% |

Base Laya's main failure is reranking: it picks the wrong FAQ when the right one is present.
First option makes about half as many reranking errors (14–21%). Both answer most out-of-scope
queries with an FAQ.

## 7. Factual corrections in this phase

26 knowledge operations were reviewed and applied through the `add-park-knowledge` pipeline
(`knowledge.py`); no section file was hand-edited. An operation was applied only if the latest
review that saw its exact content approved it.

- `hours_status.park_open_today`: removed a false claim about the SGC bulletin index. Bulletins
  and the PNN page are now dated, and the official channel is kept.
- 6 high-priority contradictions (fees, Res. 551 amounts, vehicle categories, night entry,
  porters). L1 sent all 9 operations back for revision, then approved the revised round.
- Temporal entries are dated, for example `access.cocora_registration`, which had "Hoy el punto
  es…" from a 2023 source.
- `actions.report_hypothermia` and `actions.report_lost_person` now give immediate,
  unconditional care steps. 123 is conditioned on signal.
- Capability audit: no answer text claims that the app contacts rescue, reports or registers a
  visit.
- 40 FAQs carry `emergency_direct` in `knowledge/answer_policy.json`. The app must answer them
  without a clarification menu.
- No eval row expects a clarification menu when an acceptable FAQ is `emergency_direct`.
  - 10 ambiguous authored and retrospective rows were affected: calibration 4, final_test 2 and
    retrospective 4.
  - They keep a direct target and carry `meta.emergency_overrides_clarify`.
  - `validate_dataset.py` enforces the rule.

## 8. Residual issues (not blockers for training; see `audit/safety_issues.json`)

1. **Access-mode source conflict (medium).** The PNN portal and Res. 207 require a REPSE
   guide/operator. Another PNN line says access is "de manera propia o coordinada". Only
   `access.no_official_travel_time` states both, so an answer may still imply that self-guided
   entry is possible.
2. **Four operations left out after their final review:**
   - `access.confirm_road_before`
   - `access.stay_on_official_gate`
   - `services.quindio_dulima`
   - `geography.rios_lagunilla_recio`

   The current texts are low risk. The rivers pair is `query_dependent`, so its rows are out of
   train.
3. **Eight entries whose cited excerpt does not support the answer:**
   - `access.bus_or_van_entry`
   - `access.stay_on_official_gate`
   - `access.confirm_road_before`
   - `activities.quindio_summit_ask`
   - `activities.unlisted_activities`
   - `fauna.epigeal_beetles_spiders`
   - `history_culture.minor_19th_century`
   - `services.quindio_dulima`

   For four of them, supporting quotes were located by script but not re-judged.
4. **406 FAQs have partial source support.** 365 are full and 27 are n/a. Answers were not
   rewritten for these.
5. **82% of train labels were not individually reviewed** (section 2). 1,663 ambiguous rows are
   held out of train, unresolved.

## 9. Reviewers (nobody approved their own work)

| Agent | Model (exact id) | Work |
|---|---|---|
| L1 | codex `gpt-6-luna`, reasoning high | review and re-review of the G2 contradiction fixes |
| L2 | codex `gpt-6-luna`, reasoning high | 280 pair judgments; verified X1 (112); arbitrated 154 fixes |
| L3 | codex `gpt-6-luna`, reasoning high | builder design review (9 findings: 7 applied, 1 partial, 1 declined); 248 pair judgments; arbitrated 155 fixes |
| G1–G3 | antigravity `gemini-3.8-flash`, thinking high | factual proposals: temporal entries, contradictions, actions/unsupported claims, answer policy |
| G4–G6 | antigravity `gemini-3.8-flash`, thinking high | authored 240 rows each; verified X4, X2, X3 |
| H1–H5 | claudeAgent `claude-haiku-5-5`, effort high | 2,012 pair judgments; H4 reviewed G1/G1b/G3; H2 reviewed 190 clarification labels; H5 verified X1 |
| X1–X4 | cursor `grok-4.7`, reasoning_effort high | authored 224/240/220/100 rows (contrastive, paraphrase, adversarial, ambiguous); X4 drafted clarification labels; X2–X4 verified G4–G6 |

The integrator (orchestrator) applied all approved knowledge operations in one phase and built
the dataset by script. The decision log is `reports/DECISION_LOG.md`. The generators are in `scripts/build/`, and
`audit/split_manifest.json` holds the input hashes.

## 10. Not done

- No retraining and no phone benchmark, as instructed.
- No Laya evaluation of a fine-tuned checkpoint. Only the base model and the first-option
  baseline were scored (section 6).
- Answer texts with partial support were not rewritten.
- The 1,790 historical rows are copied verbatim. Their ids all exist in the current catalog, but
  their pools come from an older corpus.
