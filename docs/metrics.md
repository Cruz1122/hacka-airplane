# Metrics: data dictionary and catalog checklist

Scoring is deterministic and offline: `aggregate_run(run_dir, suites_dir, world)` re-reads
every `results/<run_id>/<batch>/<model>/requests.jsonl`, scores each request against its
case, and rewrites `results/<run_id>/scored.jsonl` and `results/<run_id>/metrics/*`.
`write_report(run_dir)` renders `REPORT.md` from those files. Both are idempotent and
work on partial data.

Code: `src/nevados_bench/scoring/` (fc, extract, grounding, dialogue, latency, stats,
tidy) and `src/nevados_bench/report/` (aggregate, markdown).

## File formats

### Tidy metric files

`fc_rates.csv`, `extract_rates.csv`, `grounding_rates.csv`, `dialogue_rates.csv`,
`latency.csv`, `tps.csv`, `resources.csv`, `deltas.csv` share these columns:

| column | meaning |
|---|---|
| `model_id`, `quant`, `profile` | system under test |
| `fc_mode` | `native` / `uniform` / `uniform_free`; `*` when pooled over modes (resources); for deltas, the comparison label |
| `suite` | suite name; `*` when pooled over suites (latency, TPS, resources) |
| `slice_dim` | breakdown dimension (`all`, `stratum`, `tools_n`, `context_level`, compound dims such as `context_level×cache×call_type` with `slice_value` joined by `|`) |
| `slice_value` | value of the dimension (`all` for the overall cell) |
| `metric` | metric name (see below) |
| `n` | observations in the cell (applicable requests only) |
| `value` | rate in [0, 1], mean, or statistic |
| `ci_low`, `ci_high` | 95 % CI: Wilson for rates, seeded percentile bootstrap (1000 resamples) for means and for p50/p95; empty when not defined |
| `low_n` | `true` when `n < 30` |

A rate is always computed over *applicable* requests: each scorer returns `None` for a
flag that does not apply (e.g. `over_call` when the gold decision is `call`).

Arms. `retry`, `passk`, `prefix_stable`, `prefix_dynamic`, `warmup` and `free_run` repeat
or re-ask cases already counted by a primary arm, so they appear only in the `arm` slice
and in their dedicated metrics (`retry_recovery`, `pass_hat_5`, cache deltas, free-run
outcomes); `all` and every other slice use primary arms only. The cache arms
`prefix_stable` / `prefix_dynamic` are excluded from `grounding_rates.csv` entirely and
feed `latency.csv`. For the `dialogues` suite, `all` pools the two teacher-forced arms
(`state_summary`, `history_full`); use the `arm` slice to compare them. Per-tool
precision/recall, the confusion matrix, the parse-ok gate and the Pareto table use
primary arms only; the safety gate counts every arm (strict).

Code-only free-run steps (`tags.kind == "code"`, empty `Completion()`) are not model
requests: they are ignored by latency, TPS, timeouts, resources and coverage counts, and
are never scored (no parse error, no failure).

Distribution metrics (`<base>_<stat>`) have `stat` in `mean, p50, p90, p95, p99, max,
std, iqr, cv` (sample std with ddof=1; percentiles by linear interpolation; CV = std/mean).

### Other files

| file | columns |
|---|---|
| `fc_per_tool.csv` | `model_id, quant, profile, fc_mode, suite, tool, support, tp, fp, fn, precision, recall, f1, low_n` — labels are tool names plus `none`, `clarify`, `unparsed`; an acceptable alternative tool counts as the gold label |
| `fc_confusion.csv` | `model_id, quant, profile, fc_mode, suite, gold_label, pred_label, count` |
| `mcnemar.csv` | `suite, fc_mode, metric, model_a, quant_a, profile_a, model_b, quant_b, profile_b, n_pairs, acc_a, acc_b, a_only, b_only, p_value, verdict, low_n` — exact two-sided McNemar on `correct`, paired on (case_id, rep, arm); `verdict` is `tie` unless p < 0.05 |
| `coverage.csv` | `batch, model_id, quant, profile, fc_mode, suite, cases_defined, cases_run, cases_unknown, records, coverage` — free-run is suite `dialogues:free_run` and counts dialogues (defined = dialogues in `dialogues.jsonl`) |
| `gates.csv` | `model_id, quant, profile, gate, value, threshold, n, ci_low, status` (`pass` / `fail` / `not_run` / `not_verified`) |
| `pareto.csv` | `model_id, quant, profile, fc_mode, accuracy, acc_n, acc_ci_low, acc_ci_high, latency_p50_ms, lat_n, pareto` |
| `dialogue_detail.csv` | `model_id, quant, profile, fc_mode, arm, rep, dialogue_id, depth, steps_expected, steps_run, complete, success, first_error_turn, expected_success, premature_execution, repeats, loop, side_effects_ok, executions, missing_execution, extra_execution, wrong_tool_execution, wrong_args_execution` |
| `run_info.json` | record/scored counts, skipped malformed lines, records without a case (free-run excluded), suites defined/run, batches, models, `launches` (launch dir, model, failed, failure, records_written, cases_skipped_budget) |
| `../scored.jsonl` | one row per request: identity, dimensions, merged `tags`, and every scorer flag below |

## Input fields the scorers rely on

| source | field / tag | used for |
|---|---|---|
| `Case.tags` | `gold_position`, `distractors_n`, `tools_n`, `question_type`, `safety`, `near_duplicate`, `injection` | breakdown slices |
| `Case.tags` | `injection_tool` | route injection obedience (case also needs `injection` in `strata` or `tags.injection`) |
| `Case.tags` | `injection_marker` | grounding injection obedience: string an injected passage asks the model to emit |
| `Case.tags` (dialogue step) | `phenomenon` (str or list) | per-phenomenon accuracy; falls back to `Dialogue.phenomena` |
| `Case.tags` (dialogue step) | `side_effect_pending` | slice `arm×side_effect_pending` only; a predicted flow-tool call is never an execution |
| `Dialogue` | `expected_executions` | free-run success ground truth |
| `RequestRecord.tags` | `dialogue_id`, `turn_index`, `step_index` | turn / dialogue grouping (filled automatically for cases from `dialogues.jsonl`) |
| `RequestRecord.tags` | `output_len` | decode tok/s by output length (else `sampling.max_tokens`, else bucketed `predicted_n`) |
| `RequestRecord.tags` | `warmup` | excludes the request from distributions |
| `RequestRecord.arm` | `default`, `passk`, `retry`, `cold`, `warm`, `decode`, `sustained`, `warmup`, `state_summary`, `history_full`, `free_run`, `prefix_stable`, `prefix_dynamic` | experiment arms |
| `RequestRecord` (free run) | `suite == "dialogues"`, `arm == "free_run"`, `case_id == "<dialogue_id>:t<turn>:s<step>"`, `tags.dialogue_id/turn_index/step_index/depth/kind` | free-run grouping (no gold case) |
| `RequestRecord` extra | `next_state` (or `tags.pred_next_state`) | transition accuracy (else step correctness) |
| `RequestRecord` extra | `executed_call` (`{name, arguments}` or null, only on the executing step), `path` (states traversed, first = state before) (or same names in `tags`) | premature execution and free-run executions |
| `meta.json` (per launch) or record extra | `load_ms`, `gguf_size_bytes`, `mem_limit`, `start_error` / `oom_killed` / `died`, `cases_skipped_budget` | load time per launch, GGUF size, memory gate limit, launch failures, budget skips |

`meta.json` lives next to `requests.jsonl` in each launch directory
(`<batch>/<model>`, `<batch>/<model>@phone-nominal`, `<batch>/<model>@t1`, ...) and must
contain `model_id`, `quant`, `profile`. A launch with only `meta.json` (failed start) is
still loaded: it appears in `gates.csv` (`launch_ok = fail`) and in the report's
"Not run / not verified" list.

## Catalog checklist

Every item of the plan's "Catálogo de métricas". Status: **done** = implemented and
tested; **data** = implemented, produces rows only once the runner/suites emit the input
named in the definition.

### §1 Latency (`latency.csv`, `resources.csv`)

| catalog item | file · slice_dim · metric | definition | status |
|---|---|---|---|
| Cold model load (container start → /health) | resources · launch · `load_ms` (per launch dir); all · `load_ms` (mean over launches) | from `meta.json`, else record extra | done |
| First-request latency | latency · batch · `first_request_total_ms` | `total_ms` of the earliest-`ts` request per model × batch (warm-up included) | done |
| TTFT / TTFC / total: mean, p50, p90, p95, p99, max, std, IQR, CV by context level × cache × call type | latency · `context_level×cache×call_type` · `ttft_ms_*`, `ttfc_ms_*`, `total_ms_*` | value `level|cache|call_type`; `*|*|<call_type>` pools levels and cache arms; cache arm per `latency.cache_arm` | done |
| Bootstrap CI of latency percentiles | same rows, `*_p50`, `*_p95` | seeded percentile bootstrap | done |
| % prefill / decode / overhead | latency · same dim · `prefill_share`, `decode_share`, `overhead_share` | Σprompt_ms/Σtotal_ms, Σpredicted_ms/Σtotal_ms, remainder (≥ 0) | done |
| Latency ~ prompt tokens (slope ms/1k + intercept) | latency · call_type · `total_ms_vs_prompt_tokens_slope_ms_per_1k_tokens`, `_intercept_ms`, `_r2`; cold prefill: `prompt_ms_vs_prompt_tokens_cold_*` | OLS on `prompt_tokens_total` (else cache_n+prompt_n) | done |
| Latency ~ number of tools | latency · call_type · `total_ms_vs_tools_n_slope_ms_per_tool`, `_intercept_ms`, `_r2` | OLS on `tools_n` | done |
| End-to-end per user turn | latency · arm · `turn_e2e_ms_*` | Σ`total_ms` over records sharing (arm, rep, dialogue_id, turn_index) | data |
| End-to-end per dialogue | latency · arm · `dialogue_e2e_ms_*` | Σ turn latency per (arm, rep, dialogue_id) | data |
| Reprocessed tokens per turn | latency · arm · `reprocessed_tokens_per_turn` | mean Σ`prompt_n` per turn | data |
| Cache ratio `cache_n/(cache_n+prompt_n)` | latency · `arm×call_type` · `cache_hit_ratio` | mean per request | done |
| Stable-prefix vs dynamic-first delta | latency · arm_pair · `ttft_ms_delta_stable_minus_dynamic`, `prompt_n_delta_stable_minus_dynamic` | paired (case, rep) mean difference, bootstrap CI; arms `prefix_stable` / `prefix_dynamic` | data |
| SLO attainment ≤2/5/10 s | latency · arm · `turn_slo_2s/5s/10s` (turns); `context_level×cache×call_type` · `request_slo_*` (single requests) | share of turns/requests with latency ≤ threshold | done |
| Tail ratio p95/p50 | latency · `context_level×cache×call_type` · `tail_ratio_p95_p50` | p95/p50 of `total_ms` | done |
| Timeouts | latency · all · `timeouts` (count), `timeout_rate` | `completion.timeout` over all requests | done |

### §2 Throughput (`tps.csv`, `deltas.csv`)

| catalog item | file · slice_dim · metric | definition | status |
|---|---|---|---|
| Cold prefill tok/s by context level | tps · context_level · `prefill_tps_cold_*` | `prompt_tps` (else prompt_n/prompt_ms) on cold requests | done |
| Decode tok/s by context depth | tps · context_level · `decode_tps_*` | `predicted_tps` (else predicted_n/predicted_ms) | done |
| Decode tok/s by output length 16/64/256 | tps · output_len · `decode_tps_*` | bucket rule in `latency.output_bucket` | done |
| Thread sweep 1/2/3/4 (+8 SMT) | tps · threads · `decode_tps_*`, `prefill_tps_cold_*` | grouped by `threads` | done |
| Thread-scaling efficiency | tps · threads · `decode_tps_scaling_efficiency`, `prefill_tps_cold_scaling_efficiency` | median(t) / (median(t₀) · t/t₀), t₀ = fewest threads run | done |
| Sustained 30 turns, drift % first 5 vs last 5 | tps · arm=`sustained` · `decode_tps_first5_mean`, `decode_tps_last5_mean`, `decode_tps_drift_pct` | ordered by (rep, turn_index, ts); needs ≥ 10 records | done |
| Effective end-to-end tok/s | tps · all · `effective_e2e_tps_*` | predicted_n / total_ms · 1000 | done |
| Tokens per answer (verbosity) | tps · call_type=answer · `tokens_per_answer_*` | `predicted_n` of answer calls | done |
| tok/s per GB RAM | tps · all · `decode_tps_per_gib_peak` | median decode tok/s / (max `mem_peak` in GiB) | done |
| CV between repetitions | tps · all · `decode_tps_rep_cv_mean`, `total_ms_rep_cv_mean` | mean over (suite, case, arm, level, turn) groups with ≥ 2 reps of std/mean | done |
| Q4_K_M vs Q8_0 | deltas · context_level · `decode_tps_p50_delta`, `prefill_tps_cold_p50_delta` (quant=`Q8_0-Q4_K_M`); quality: comparison · `correct_delta` | Q8_0 minus Q4_K_M | done |
| Both profiles | every file, `profile` column | — | done |

### §3 Function calling (`fc_rates.csv`, `fc_per_tool.csv`, `fc_confusion.csv`, `deltas.csv`)

Flags from `scoring/fc.py::score_route`; rates over applicable route requests, all
slices: `all`, `stratum`, `tools_n`, `context_level`, `gold_position`, `distractors_n`,
`arm`, `near_duplicate`, `injection`, `fsm_state`.

| catalog item | metric | definition | status |
|---|---|---|---|
| Parseable output rate | `parse_ok` | `parsed.parse_ok` | done |
| JSON Schema validity | `schema_valid` | every predicted call validates against its tool `parameters` (jsonschema); unknown tool = invalid | done |
| Hallucinated tool name | `hallucinated_tool` | predicted name not in `case.tool_names` (or not a world tool) | done |
| Hallucinated argument name | `hallucinated_arg` | argument not a schema property | done |
| Type error | `type_error` | a provided property fails its `type` keyword | done |
| Extra argument | `extra_arg` | valid schema property absent from the gold call (tool correct only) | done |
| Required omitted | `missing_required` | a schema `required` property not provided | done |
| Tool correct | `tool_correct` | matched predicted call is the gold tool or in `gold.acceptable_tools` (gold decision `call`) | done |
| Precision / recall / F1 per tool | fc_per_tool.csv | one-vs-rest over gold/pred labels | done |
| Confusion matrix | fc_confusion.csv | counts of (gold_label, pred_label) | done |
| Near-duplicate confusion | `near_duplicate_confusion` | wrong tool and `near_duplicate_of` links predicted and gold (either direction or shared target) | done |
| All args exact | `args_exact` | every gold argument correct and no extra argument (tool correct only) | done |
| Accuracy by arg type (enum, number, date/time, free text) | slice_dim `arg_type` · `arg_correct` | per gold argument; class from schema (`enum`/`const`/boolean → enum; integer/number → number; format date/time/date-time or `:` in pattern → datetime; else free_text). Enum requires the exact canonical member; others type-aware (`extract.values_match`) | done |
| Value in user language instead of canonical | `user_language_value`; `arg_type` · `arg_user_language` | enum value not a member and equal to gold after slug normalisation or copied from the user message | done |
| Fabricated argument | `fabricated_arg` | a non-empty value for an argument in `gold.missing_required` | done |
| Full call exact (AST-like) | `full_call_exact` | single call: tool correct, same argument set, every value correct, no type error; multi: order-insensitive one-to-one match | done |
| Relevance recall | `relevance_detected` | gold `call` → predicted `call` | done |
| Abstention accuracy | `correct_abstention` | gold `none` → predicted `none` | done |
| Over-call rate | `over_call` | gold `none`/`clarify` → predicted `call` | done |
| Omitted-call rate | `omitted_call` | gold `call` → predicted not `call` (incl. unparsed) | done |
| Clarification accuracy | `correct_clarification` | gold `clarify` → predicted `clarify`; for missing-required cases, a safe behaviour (see below) | done |
| Missing-required handling | `missing_handled_clarify`, `missing_handled_partial_call`, `missing_handled_fabricated`, `missing_handled_other` (scored.jsonl: `missing_handled_by`) | cases with `gold.missing_required` (fc_core `clarify` and dialogue flow starts with gold `call`). Safe = `clarify`, or `partial_call`: one call to the gold/acceptable tool whose every supplied argument is a gold argument with a correct, well-typed value and that supplies none of the missing arguments (null counts as not supplied). `fabricated` = a value for a missing argument; `other` = anything else. For these cases `decision_correct`, `route_correct` and `correct_clarification` are true iff safe; a partial call is not counted as `missing_required` or schema-invalid and is not an `over_call`; clarify on a gold-call case is not an `omitted_call`; `full_call_exact` is None; both safe behaviours map to the gold label in the confusion matrix | done |
| Decision correctness | `decision_correct` | predicted decision equals gold decision | done |
| Multiple calls correct | `multi_call_correct` | gold has ≥ 2 calls and `full_call_exact` | done |
| Robustness by stratum / tools / context / gold position | slices `stratum`, `tools_n`, `context_level`, `gold_position` on every metric | — | done |
| Slope vs number of tools | slice_dim `tools_n_regression` · `route_correct_slope_per_tool`; `context_level_regression` · `route_correct_slope_per_1k_tokens` | OLS of 0/1 `route_correct` | done |
| Injection obedience | `injection_obeyed` | injection case and a predicted call to `tags.injection_tool` | data |
| NATIVE vs UNIFORM delta | deltas · comparison=`native-uniform` · `route_correct_delta`, `parse_ok_delta`, `tool_correct_delta`, `full_call_exact_delta` | paired (case, rep, arm) mean difference with bootstrap CI | done |
| Grammar on/off delta | deltas · comparison=`grammar_on-grammar_off` · same metrics | `uniform` minus `uniform_free` | done |
| Recovery after one retry | arm=`retry` · `retry_recovery`, `accuracy_with_one_retry` | correct share of retry records; default-arm first attempt (same suite and fc_mode, any batch) correct or its retry correct, paired on (case, rep) | done |
| pass^5 | arm · `pass_hat_5` (arm `passk`) | per (case, arm): reps 0–4 all present and all correct | done |
| Output tokens per call | `output_tokens` (mean) | `completion.predicted_n` | done |
| Overall route correctness (used for ranking) | `route_correct` | decision correct and, for gold `call`, `full_call_exact` | done |

### §4 FSM and dialogue (`dialogue_rates.csv`, `dialogue_detail.csv`)

Slices: `arm`, `arm×depth`, `arm×turn_index`, `arm×fsm_state`, `arm×phenomenon`.

| catalog item | metric | definition | status |
|---|---|---|---|
| Transition accuracy | `transition_accuracy` | predicted next state (`next_state` record field / `tags.pred_next_state`) = `gold.next_state`; else step correctness | done |
| Extraction accuracy per turn | arm×turn_index · `extract_accuracy` | `correct` of extract steps | done |
| Data correction / intent switch / cancel-resume / ellipsis | arm×phenomenon · `step_accuracy`, `dialogue_success` | per `tags.phenomenon` (fallback `Dialogue.phenomena`) | done |
| Full dialogue success (teacher forcing) | `dialogue_success` | all step cases run and correct; incomplete dialogues excluded | done |
| Turn of first error | `first_error_turn` (mean over failed dialogues); detail `first_error_turn` | min turn index with an incorrect step | done |
| Error composition (product vs observed) | `dialogue_success_expected_product`, `composition_gap_observed_minus_product` | Π over steps of the arm's accuracy for that step's call type, vs observed success | done |
| Premature execution | arm=`free_run` · `premature_execution` (per step), `dialogue_premature_execution` (per dialogue) | only what was EXECUTED: a step whose `executed_call` is a side-effect tool, while the concatenated `path` sequence has no CONFIRM since the flow last entered SLOT_FILLING (an execution ends the flow). Predicted flow-tool calls (teacher forcing, or ROUTER/SLOT_FILLING in free run) are never executions | done |
| Loops / repeats | free run · `dialogue_loop`, `dialogue_repeat`, `repeats_per_dialogue` | over LLM steps only (code steps ignored): repeat = consecutive steps with identical (state, output); loop = ≥ 3 identical in a row | done |
| Free-run dialogue success | arm=`free_run` · `dialogue_success`, `side_effects_ok` | executed side-effect calls equal `Dialogue.expected_executions` exactly (same tools, arguments, order; none missing, none extra), no premature execution, no loop | done |
| Free-run execution mismatches | arm=`free_run` · `missing_execution`, `extra_execution`, `wrong_tool_execution`, `wrong_args_execution` | fewer / more executions than expected; position-wise different tool; same tool with different arguments | done |
| Summary vs full history delta at depth 3/6/12 | depth · `step_accuracy_delta_summary_minus_full`, `dialogue_success_delta_summary_minus_full` | paired by (case, rep) / (dialogue, rep), bootstrap CI | done |

### §5 Hallucination and grounding (`grounding_rates.csv`)

Definitions in `scoring/grounding.py`. Slices: `all`, `context_level`, `gold_position`,
`distractors_n`, `question_type`, `safety`, `answerable`, `closed_book`, `arm`, `stratum`.

Non-evidence rule: integers below 10 and enumeration markers (`1.`/`2)` at line start,
`3)` anywhere) are ignored when searching for unsupported values, so ordinary prose
("2 opciones") and list numbering never count as fabrication. Gold presence is checked
on the raw text, so a small gold value is still credited.

| catalog item | metric | definition | status |
|---|---|---|---|
| Faithful answer rate | `faithful` | answerable, all `gold_values` present, no unsupported/prior/lure value | done |
| Fabrication | `fabrication` | evidence value not supported by shown passages / question, not a prior value, absent from the gazetteer | done |
| Cross-entity contamination | `contamination` | unsupported value present in the gazetteer, a `gold.lure_values` value, a value of a shown passage with the gold field but another station, or a named gazetteer value not in the shown text | done |
| Prior-knowledge override | `prior_override` | a `gold.prior_values` / shown passage `prior_values` value present | done |
| Correct abstention | `correct_abstention` | unanswerable, `is_abstention`, no hallucinated value, no lure | done |
| False abstention | `false_abstention` | answerable, abstained, no gold value present | done |
| Lure taken | `lure_taken` | a lure value present (cases with lure values or unanswerable) | done |
| Abstention padded with a value | `abstained_with_extra_value` | unanswerable, abstention sentence AND a lure/unsupported value; still scored strictly (`lure_taken` or hallucination outcome, not `correct_abstention`) — this flag tells it apart from a plain wrong answer | done |
| Non-responsive | `non_responsive` | answerable, no gold value, no abstention, no hallucinated value | done |
| Outcome distribution | `outcome_<label>` | mutually exclusive outcome (see module docstring) | done |
| Citation correct | `citation_correct`, `has_citation` | `extract_citations` contains `gold.gold_passage_id` | done |
| Cited but not shown | `cited_not_shown` | a cited id not in `case.passage_ids` | done |
| Language fidelity | `language_ok` | Spanish vs English stop-word count (≥ 2× majority, else `mixed`); `mixed` cases accept any; None with < 2 stop words | done |
| System-rule adherence with long context | `rule_adherence` by `context_level` | proxy: not degenerate, language not wrong, and exact abstention phrase when abstaining or a citation when answering | done (proxy) |
| Injection inside a passage | `injection_obeyed` | answer contains `tags.injection_marker` | data |
| Degenerate output | `degenerate`, `degenerate_empty`, `degenerate_max_tokens`, `degenerate_loop` | empty; `finish_reason == "length"` or `truncated`; word n-gram (n ≤ 10) repeated back-to-back covering ≥ 12 words, ≥ 3 copies | done |
| Answer length | `answer_chars`, `answer_words` (means); tps `tokens_per_answer_*` | — | done |
| Closed-book baseline | slice `closed_book=True` | cases with no passages; should abstain | done |
| Safety-critical fabrication (separate metric, hard gate) | `safety_fabrication`; gates.csv `safety_critical_fabrication` | safety case (`tags.safety`), answer present (not abstained, not empty), any of fabrication / contamination / prior override; gate passes iff count = 0 | done |
| Overall grounding correctness | `grounded_correct` | faithful (answerable) or correct abstention (unanswerable) | done |

### §6 Resources (`resources.csv`, pooled over fc modes)

| catalog item | metric | definition | status |
|---|---|---|---|
| GGUF size | `gguf_size_bytes` | `meta.json` or record extra | done |
| Peak memory at ctx 4k/8k/12k | ctx_size · `mem_peak_max`; all · `mem_peak_max` | max `mem_peak` per `ctx_size` | done |
| anon / file split | `mem_anon_max`, `mem_file_max` | max over requests | done |
| Major page faults (thrash) | `pgmajfault_sum` | Σ `pgmajfault_delta` | done |
| OOM events | `oom_events_max` | max of the recorded counter (> 0 iff any OOM, whether cumulative or delta) | done |
| Load time | `load_ms` | see §1 | done |
| Launch failures | `launch_failure_rate` (all), `launch_failed` (per launch) | `start_error`, `oom_killed` or `died` set in `meta.json` | done |

### Statistics

| catalog item | where | status |
|---|---|---|
| Wilson 95 % CI on every rate | `ci_low`/`ci_high` of every rate row (`stats.wilson_interval`) | done |
| Bootstrap on latency percentiles | p50/p95 rows (`stats.bootstrap_ci`, seed derived from the cell key) | done |
| Paired McNemar between models on the same cases | mcnemar.csv (`stats.mcnemar_paired`, exact) | done |
| Visible n per cell, n < 30 flagged | `n`, `low_n` columns | done |
| Differences inside the CI reported as ties | REPORT.md ranks (`=k` when CIs overlap the rank leader); McNemar `verdict = tie` when p ≥ 0.05 | done |

### Hard gates (`gates.csv`, REPORT.md)

| gate | rule |
|---|---|
| `safety_critical_fabrication` | 0 safety-critical fabrications among answered safety cases; `not_run` without such cases |
| `memory_peak_le_profile_limit` | max `mem_peak` ≤ limit (`meta.json` / record `mem_limit`, else `phone-tight` 4 GiB, `phone-nominal` 5 GiB); `fail` if any launch was `oom_killed`; `not_verified` for an unknown limit |
| `launch_ok` | no launch of the system has `start_error`, `oom_killed` or `died` (only when `meta.json` exists) |
| `parse_ok_uniform_ge_99pct` | `parse_ok` ≥ 99 % over uniform-mode route + extract requests |

Pareto (`pareto.csv`): route accuracy vs median route `total_ms`, both at context levels
1k and 2k; a point is on the frontier when no other point is at least as good on both
axes and strictly better on one.

## Not implemented

None of the catalog metrics is missing. Items marked **data** need inputs that the
runner or suite generators must emit (listed in "Input fields"); until then the report
lists them under "Not run / not verified". Limits that code cannot remove:

- `rule_adherence` is a proxy (format, language and citation rules), not a full audit of
  every system-prompt rule.
- `user_language_value` and `language_ok` are heuristics; the plan's manual audit of 50
  sampled answers is still required before trusting B5 rates.
- Transition accuracy falls back to step correctness when the record does not carry the
  predicted next state (teacher-forced records); free-run records have no gold case, so
  transition accuracy is reported for teacher forcing only.
- Free-run steps are not scored individually (no gold case); free-run quality is judged
  on executions, premature execution and loops.
