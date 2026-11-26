# Curation v2 — final report

Date: 2026-11-22. Hackathon: 2026-11-26. Written by the orchestrator (Claude Opus 5.5): the director
task (agent 1, GPT-6 Luna) was cancelled after more than an hour without output, at the user's
request for speed. All counts below were recomputed by script from the artifacts named.
Timeline and every arbitration: `decisions/orchestrator.md`.

## 1. Improved KB

- 347 `update` ops applied through `knowledge.py apply` in contract order; 0 add, 0 delete
  (`reports/integration.md`, transaction IDs there). 806 entries before and after.
- 159 ops change the answer or sources; 39 more change only dates (`last_verified`/`valid_until`):
  198 factual ops by the PLAN.md definition (matches the structural audit). 149 are metadata only
  (labels, examples, hard negatives, related). 200 ops carry evidence items.
- Checks after integration: `validate_knowledge.py` `Errors: 0; review flags: 0`; `regen_test.py full`
  15/15 OK (deterministic rebuild); `kb.py validate` 0 errors; `taxonomy_audit` 0 errors.
- Hashes: `snapshots/sections_before.sha256.json` → `snapshots/sections_after.sha256.json`.

| Section | Entries | Applied | Answer/sources changed | Other | Proposed, left out |
|---|---:|---:|---:|---:|---:|
| actions | 10 | 10 | 10 | 0 | 0 |
| health_safety | 70 | 59 | 33 | 26 | 3 |
| weather_volcano | 54 | 27 | 9 | 18 | 4 |
| access | 78 | 11 | 0 | 11 | 21 |
| booking_fees | 67 | 43 | 41 | 2 | 16 |
| hours_status | 40 | 37 | 37 | 0 | 3 |
| preparation | 34 | 7 | 6 | 1 | 27 |
| activities | 70 | 5 | 5 | 0 | 21 |
| rules | 73 | 40 | 8 | 32 | 33 |
| services | 26 | 22 | 0 | 22 | 4 |
| fauna | 69 | 31 | 0 | 31 | 17 |
| flora_ecosystems | 65 | 18 | 6 | 12 | 10 |
| geography | 61 | 6 | 0 | 6 | 30 |
| history_culture | 59 | 3 | 0 | 3 | 56 |
| conversation | 30 | 28 | 4 | 24 | 2 |
| **total** | **806** | **347** | **159** | **188** | **247** |

(Entry counts per section are from `snapshots/sections_before/`.)

## 2. FAQ inventory

- Adds 0, deletes 0, merges 0. The 2 merges and 3 moves in `findings/taxonomy.json` were **not
  implemented**: no curator proposed adds or deletes in either round, and the fix brief made a move
  an `add` in the target section. Duplicates after: 0 identical labels, answers or shared examples
  (`reports/structural/structural_audit.md`).
- 247 proposed ops were left out (they keep the before text). Reasons, from the reviews: claim not
  in the quote (partial entailment), stylistic label churn (Laya was trained on the current labels),
  removed examples that no longer route, unsourced `valid_until`, refetch not confirmed. Per-op
  verdicts: `reviews/<S>.review.json`, `reviews/<S>.rereview.json`.
- Inventory before/after: `audit/inventory_before/`, `audit/inventory_after/`. LOO top-1 0.4664 →
  0.4756, confusable pairs 693 → 694 (a locator, not a target).

## 3. Sources and vigencia

Final status per entry = latest reviewer judgment (re-review where present, else round 1), never
the curator's claim: **full 341, partial 418, none 20, n/a 27** (conversation, no factual claim).
Grok-curated sections carry most `full` (health_safety 65/70, weather_volcano 44/54); Gemini
sections are mostly partial (history_culture 3 full / 55 partial, geography 12 / 48).

- Every applied factual op: `verify_evidence.py` fail [] on all 15 finals; quotes literal in local
  files whose bytes are hashed (fetched with meta, or pinned legacy). Refetch by non-authors; the
  funcionpublica.gov.co refetch needed a verified CA chain (wrong intermediate served; fixed with
  Let's Encrypt YR1 + ISRG Root YR cross-signed by ISRG Root X1, no `-k`).
- Temporal (structural audit heuristic): 119 IDs flagged; 57 are applied ops, 62 kept their before
  text. Worst before-text case: `access.cocora_registration` ("Hoy el punto es…", 2023 source).
- The 57 applied-op flags were read one by one (orchestrator): 56 are false positives. They are
  explicit disclaimers ("no es el de hoy", "no confirma la cobertura de hoy"), physical terms
  ("herida abierta", "zonas abiertas") or menu words ("horarios"). **1 real error shipped:**
  `hours_status.park_open_today` says the SGC bulletin index "no muestra el nivel de alerta"; the
  critical review found the live index does show a dated level (the same sentence was removed
  from `volcanic_alert_closures` in round 3c). Fix next.
- Caveat: for left-out ops, the re-reviewer judged audit support against the v2 answer that did not
  ship, so those entries' support counts are approximate.

## 4. Ambiguous-label audit

`audit/label_audit.jsonl`, `audit/label_audit_summary.md`: 750 train-side `none` rows judged.
A retrieval miss 649, B reranking risk 70, C true none 0, D ambiguous 31. 101/750 (13%) of the
training `none` targets are wrong or ambiguous; training jsonl were not edited, `ft_data_v2` uses
`acceptable_ids` instead.

## 5. Contrastive / hard-negative dataset

`data/knowledge/laya_ft_v2/` (MANIFEST.json): 1,878 rows (train 1,784, dev 94), 891 verified and 987
synthetic, built from train-side data only with the app reference config (e5-base, gateway k=5,
δ=0.05, ≤5 sections), single `choice` with 3–5 options + "ninguna de estas opciones",
`acceptable_ids` from the arbiter. Leak check vs test_blind: 0 matches. Not trained.
sha256 train `ec090c87…`, dev `d8b802f1…`.

## 6. Reproducible splits

`data/knowledge/eval_v2/` (MANIFEST.json, seed 20261122). Sealed set: written by two adversarial
Grok agents from an answers-only view outside the checkout, labels verified by the Luna arbiter
(740 rows: 739 kept with 38 corrected, 1 dropped `B-0389`). Leak check excluded 111 rows (exact or
e5 cosine ≥ 0.93 against corpus examples before/after; 76 also against train-side). Family-disjoint:
`dev_gate` 162 (thresholds only, sha256 `d36266a5…`), `test_blind` 466 (report only, `e7195efa…`).

## 7. Before / after benchmark

`reports/bench/before_after.md` (+ .json): same test_blind, thresholds fit on dev_gate per corpus.

| Gateway reference | Before | After |
|---|---|---|
| R@5 | 86.2% [82.0, 89.5] | 87.1% [83.0, 90.3] |
| e5+Laya+cos top-1 | 63.7% [58.3, 68.7] | 64.9% [59.6, 69.9] |
| Coverage (target > 36.5%) | 1.5% | 0.0% |
| Wrong among answered (target ≤ 3%) | 14.3% (n=7) | n/a (n=0) |
| R@3 | 82.2% [77.6, 85.9] | 83.7% [79.3, 87.3] |
| None rejection | 99.2% | 100% |

- Before/after differences are **within noise** (overlapping 95% Wilson intervals). The curation
  did not measurably move retrieval on the sealed set.
- **The acceptance target is not met by either corpus.** The single-threshold policy was fit to 0
  wrong on 162 dev rows, which accepts only 1–9 dev rows; on test that is near-zero coverage. 
  Inference (not tested): the bottleneck is the acceptance policy and Laya's calibration (trained on
  the before labels), not the KB. Even the strictest threshold shows 14–18% wrong on test, so
  loosening it will not reach ≤ 3%. Gateway R@3 after is 83.7%, so a top-3 choice UI has room a
  single answer does not.
- Not measured: an unseen-topics slice (no FAQ was added, so there were no new topics to hold out).
- Per section and per scenario tables, and miss categories (e5 top-5 misses, ambiguous not
  clarified), are in the report. Legacy 1,790-row eval: `reports/bench/before_legacy.md`, legacy,
  not blind, chose nothing.

## 8. Phone RAM / latency

**Not measured**: no adb device on 2026-11-22. LAPTOP CPU, warm, excluding query embedding and
startup: gateway p50/p95 316/472 ms before, 316/480 ms after.

## 9. Subagents

| Role | Model | Result |
|---|---|---|
| 15 section curators (2 rounds) | Gemini 3.8 Flash ×10, Grok 4.7 ×5 | proposals v1/v2, audits, logs |
| Reviewers round 1 + 5 re-reviewers + examples | Claude Haiku 5.5 | `reviews/` |
| Taxonomy, arbiter, critical lead, eval architect, integrator | GPT-6 Luna | findings, label audit, critical reviews, bench, integration |
| Contradictions + eval authors A/B | Grok 4.7 | `findings/contradictions.json`, sealed eval |
| Label specialist, structural auditor | Claude Haiku 5.5 | `findings/labels.json`, structural audit |
| Director | GPT-6 Luna | cancelled; report by orchestrator |

Decision logs per agent (acceptance criterion):

| Agents | Log / output |
|---|---|
| 15 curators | `decisions/<S>.curator.md` (round 1), `decisions/<S>.fix.md` (round 2): 30/30 present |
| 5 reviewers, 5 re-reviewers, examples specialist | `reviews/<S>.review.json`, `<S>.rereview.json`, `_examples.json` (verdict + reason per op; no separate .md) |
| Taxonomy, critical lead, contradictions, label specialist | `findings/{taxonomy,critical,contradictions,labels}.json` |
| Arbiter | `audit/label_audit_summary.md`; sealed: `nevados_sealed_eval/verification_report.md` |
| Eval authors A/B | notes in `nevados_sealed_eval/` |
| Eval architect, integrator, structural auditor | `reports/bench/`, `reports/integration.md`, `reports/structural/` |
| Critical second reviews | `reviews/critical_second.review.json`, `critical_r3{,b,c}.review.json` |
| Director | **gap**: no log (cancelled) |
| Orchestrator | `decisions/orchestrator.md` |

- Substitution: Grok ran as `cursor/grok-4.7` by user instruction (OpenCode Grok 4.6 "Model not
  found"; Cursor has no 4.6).
- No self-approval: authors and reviewers are always different models; ops the orchestrator wrote
  (critical rounds r3/r3b/r3c) were approved only by the Luna critical lead.
- Conflicts arbitrated (details in `decisions/orchestrator.md`):
  1. Gemini marked sources `primary_ok` without reading them, then used topic-only excerpts →
     `audit_check.py`, row-by-row reviewer support, final status = reviewer support.
  2. 3 critical items (2 hypothermia, ash on roofs) and the camping contradiction were left at
     `revise` → critical round 3. Res. 207/2023 names two different "Arenales" (Brisas, restricted;
     near the Nevado del Tolima, transitional), now separated.
  3. Critical review asked to remove the 123 citing PLAN.md; declined: that line meant phone
     benchmarks, not telephone numbers (wording fixed). CPR order and a false SGC-index claim were
     accepted.
  4. 36 rules ops blocked by a TLS failure → verified CA chain; 20 ops whose only condition was the
     refetch promoted (`reviews/rules.rereview.addendum.json`).
  5. Arbiter misclassified 2 rows (C→B), fixed with its own evidence.

## 10. Recommendations for the hackathon (ranked)

1. **Change the answer policy.** A single threshold gives 0–5% coverage and still 14–18% wrong on
   the few accepted. Show the top 3 options as a choice (gateway R@3 83.7%) and answer directly only
   after Laya is retrained and re-fit; a larger dev_gate is needed to fit any threshold reliably.
2. **Fix `hours_status.park_open_today`** (false claim about the SGC index) through the skill.
3. **Fix the 62 before-text temporal entries**, starting with `access.cocora_registration`; any
   "hoy/actualmente" without a date must go.
4. **Resolve the 6 high contradictions still open** (park area, the four admission fees, vehicle
   fee, night entry, porter luggage, Brisas guide price): state both official figures with dates, never one as current.
5. **Measure on the phone** (adb): RAM and p50/p95 of e5 + Laya; laptop numbers do not transfer.
6. **Retrain Laya on `laya_ft_v2`** in Colab (322M full FT does not fit the local GTX 1650 4 GB);
   evaluate only on test_blind, choose on dev_gate.
7. Implement the 2 taxonomy merges and 3 moves (`findings/taxonomy.json`) with `replace_with`.
8. Re-source the Gemini sections' partial rows (history_culture 55, geography 48, access 54) before
   trusting them as cited.

## Residual risks and what was not verified

- Phone RAM/latency: not measured.
- 1 applied answer carries a known false claim (`hours_status.park_open_today`).
- Contradictions: 0 critical open; 6 high open (critical review list minus the yellow-alert item
  fixed in round 3c).
- 418 entries have only partial support for their answer; 20 have none.
- 247 proposed corrections were not applied; their before text ships, including known issues
  (`hours_status.pico_y_placa` incomplete, `night_entry_prohibition` overstated).
- The sealed eval is adversarial (confusable, near-miss, temporal heavy); natural-query performance
  is in the per-scenario table, not the headline.
- Nothing was committed. Untracked/modified by this work: `data/knowledge/sections/*`, the registry
  `coordination/knowledge_additions.json`, `data/knowledge/eval_v2/`, `data/knowledge/laya_ft_v2/`,
  `research_notes/curation_v2/`, `experiments/laya/*_v2.py`, `.gitignore` (`.cache/`).
