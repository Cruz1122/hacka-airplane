# Phase 1 report: Laya as System 1 on the seed knowledge base

Date: 2026-11-21. Code: `experiments/laya/` (isolated uv project). Raw outputs: `results/p1-laya/`
(git-ignored). Plan and go/no-go rule: [plan-knowledge-system.md](plan-knowledge-system.md).

## Verdict

**No-go for Laya PT/ES NLI zero-shot.** It fails both pre-registered criteria:

| Criterion (fixed before measuring) | Needed | Measured | Result |
|---|---|---|---|
| Top-1 on fresh paraphrases vs best embeddings | +5 points | −3 points (72.7 % vs 76.1 %) | Fail |
| ...or answered questions at ≤ 3 % wrong | +10 points | +13.6 points (37.5 % vs 23.9 %), but at 3.4 % wrong | Borderline fail |
| ONNX int8, 5 candidates, laptop CPU p50 | ≤ 400 ms | 663 ms | Fail |

Decision for Phase 3:

- **Embeddings only**: flat index plus a soft gateway, used to organise sections and build the candidate pool.
- **Abstention**: similarity thresholds.
- **Fallback**: router r1 when the system is unsure.
- **Laya later**: re-test after fine-tuning on the Phase 2 data.

## Setup

| Item | Value |
|---|---|
| Knowledge | `conocimiento.json` v0 → 11 sections, 44 entries, 263 examples (`data/knowledge/phase1/sections/`) |
| Eval sets | Leave-one-out 263; fresh paraphrases 88 (2 per entry); out of scope 40; near miss 20; multi-intent 15 (`data/knowledge/phase1/eval/`). Written by Claude before any model ran |
| Embedders | multilingual-e5-small, multilingual-e5-base, paraphrase-multilingual-MiniLM-L12-v2. EmbeddingGemma-300m is gated on Hugging Face (needs license acceptance + token): not tested |
| System 1 | `telepatia-ai/laya-pt-es-nli`, `laya==0.5.1`, CPU, torch 4 threads |
| Hardware | Laptop, 8 CPU threads, no GPU used |

## Results

### E1-E3: retrieval (fresh paraphrases, n = 88; Wilson 95 % CI)

| Configuration | e5-small | e5-base | MiniLM |
|---|---|---|---|
| E1 flat kNN, top-1 | 71.6 % [61, 80] | **76.1 %** [66, 84] | 68.2 % [58, 77] |
| E1 flat kNN, correct in top 5 | 94.3 % | **95.5 %** | 90.9 % |
| E2b "spider" gateway (section centroid → best entry), top-1 | 61.4 % | 64.8 % | 52.3 % |
| E2b gateway picks the right section | 68.2 % | 72.7 % | 61.4 % |
| E3 soft gateway pool (sections within 0.05 of best, ≤ 5 sections, 2 entries each), correct in pool | 94.3 % (5.4 cands) | 95.5 % (4.9 cands) | 82.9 % (2.8 cands) |
| Multi-intent: both topics in top 5 | 15/15 | 15/15 | 12/15 |
| Query embedding latency (laptop CPU) | 7.3 ms | 29.8 ms | 10.7 ms |

Leave-one-out top-1 (in-domain but terse seed phrasings): e5-small 63.5 %, e5-base 66.9 %, MiniLM 56.7 %.

**Findings:**

1. **A hard gateway loses 11 points.** Sending each query to only the best section by centroid costs
   ~11 points: the wrong section is chosen 27 % of the time. Your intuition about scalability is
   right, but routing must be **soft** (several sections) or done by max similarity over all entries.
2. **The candidate pool works.** With e5-base, the right answer is among ~5 candidates 95 % of the
   time. The remaining problem is choosing among them and knowing when to abstain.
3. **Embeddings alone abstain poorly.** In-domain vs out-of-domain AUROC is 0.89, but at ≤ 3 % wrong
   answers only **24 %** of in-domain questions get answered.

### E4-E6: Laya on the e5-base pool (paraphrases n = 88; out of scope + near miss n = 60)

| Variant | Top-1 | AUROC in vs out | Answered at ≤ 3 % wrong (2-fold CV) | Wrong rate | Multi-intent both in top 2 |
|---|---|---|---|---|---|
| E3 embeddings only | **76.1 %** | **0.888** | 23.9 % | 2.0 % | 11/15 |
| E4a NLI, hypothesis "El visitante pregunta sobre {label}." | 65.9 % | 0.744 | 13.6 % | 6.1 % | 10/15 |
| E4b NLI, hypothesis "El visitante pregunta: {closest example}" | 70.5 % | 0.796 | 18.2 % | 2.0 % | 8/15 |
| E5 one `choice` question over labels + "ninguno" | 43.2 % | 0.664 | 3.4 % | 3.4 % | 4/15 |
| E4a + embedding score | 72.7 % | 0.802 | **37.5 %** | 3.4 % | 11/15 |
| E6 "ninguno" probability as the abstention signal | — | 0.639 | 2.3 % | 4.7 % | — |

**Findings:**

1. **On clear cases Laya is sharp.** For example, the right label scores 0.95 and the rest ~0.02.
2. **It reads topic overlap as entailment**, giving 0.95 to many wrong pairs:
   - "¿Me recomiendas un hotel en Pereira?" → "qué se puede visitar"
   - "¿Hay wifi en el centro de visitantes?" → "qué se puede visitar"
   - "hay cóndores?" → "los mamíferos del parque"
3. **Its probabilities saturate at ~0.95**, so its confidence does not separate right from wrong as
   well as cosine similarity does.
4. **The single `choice` question fails** (43 %). The model was trained on 3-way NLI only, as its
   model card states.

### E7: ONNX (5 candidates, laptop CPU, paraphrases)

| Runtime | p50 | p95 | Size | Top-1 (E4a+emb) | Same pick as torch |
|---|---|---|---|---|---|
| torch BF16 → CPU | 745 ms | 1,083 ms | 644 MB (safetensors) | 72.7 % | — |
| ONNX fp32 | 837 ms | 1,296 ms | 1,288 MB | 72.7 % | 100 % |
| ONNX dynamic int8 | 663 ms | 1,062 ms | **334 MB** | 71.6 % | 87.5 % |

- **Cost grows with candidates.** Each candidate is a separate encoder row, so cost grows linearly
  with pool size.
- **The phone will be slower.** It runs at ~0.75× the laptop or slower, which puts it well over
  the budget.

## What this means for Phase 3

1. **Embedder: multilingual-e5-base** (best accuracy), or e5-small if phone latency demands it
   (4.5 points lower, 4× faster). Both are MIT. Re-test EmbeddingGemma if the license is accepted.
2. **Gateway: soft.**
   - Each section's score is the max similarity over its entries.
   - Open every section within δ = 0.05 of the best, up to 5.
   - Sections stay separate files and indexes, so they remain independently editable. What changes
     is that routing never trusts a single gate.
3. **Decision:**
   - Answer when the top cosine and the margin clear thresholds calibrated on Phase 2 data.
   - Otherwise ask from the clarification bank of the best section.
   - Below the out-of-scope threshold, give the fallback with featured topics.
4. **Phase 2 data is the main lever.** More and more varied examples, plus hard negatives, raise
   top-1 and the abstention margin.
5. **Laya, second chance (optional):**
   - Fine-tune it with `laya.train` on Phase 2 pairs (question, label) → match / no match, with
     hard negatives.
   - Gate: same criteria as above, measured on the phone.
   - Latency rule: if it is still > 400 ms for 5 candidates, use it only for the "unsure" band, not
     for every query.

## Limitations

- **Small, single-author eval.** 44 entries and 88 paraphrases written by one author (Claude);
  CIs are wide (±9 points).
- **Noisy thresholds.** Thresholds use 2-fold CV on ~150 items, so the coverage numbers are noisy.
- **Laptop only.** Latency was measured only on the laptop CPU; nothing has been measured on the phone.
- **Some untested options:** embedder fine-tuning, BM25 hybrid and per-section thresholds.

## Incident during this phase

The Phase 2 agent (Codex) writes to `data/knowledge/sections/` in this same repo. My first
conversion wrote the seed there twice, overwriting Codex output:

| What happened | Files | Status |
|---|---|---|
| Restored by re-running Codex's own generators | rules, booking_fees, activities, geography, history_culture | Recovered |
| Removed my seed copies that had replaced Codex output | the other six | Removed |
| Lost; no generator script existed for it | `weather_volcano.json` (10 entries at 13:44) | Codex rewrote it at 14:12 with 3 entries; the other 7 need redoing |

Phase 1 data now lives only in `data/knowledge/phase1/`. Validation of the current Phase 2 output
(`uv run python kb.py validate ../../data/knowledge/sections`) reports 1 error: an example shared
by `geography.laguna_encanto` and `activities.laguna_encanto`.

## E8: prompt variants (added 2026-11-21)

Task: pick, among the e5-base top-k candidates, the entry whose curated answer best answers the
query. Paraphrases n = 88, out of scope + near miss n = 60. The right entry is in the top 3 for
92.0 % of queries and in the top 5 for 95.5 %. Code: `experiments/laya/prompts_exp.py`; raw data:
`results/p1-laya/prompt_rows.jsonl`.

| Variant (best k) | Prompt | Top-1 | AUROC | Answered at ≤ 3 % wrong (wrong) | Laptop p50, k = 5 |
|---|---|---|---|---|---|
| Embeddings only | — | 76.1 % | 0.887 | 23.9 % (2.0 %) | 30 ms |
| `nli_label`, k=3 | state = query; hyp "El visitante pregunta sobre {label}." | 69.3 % | 0.745 | 14.8 % | 1,204 ms |
| `nli_label` + emb, k=3 | same, plus cosine | **77.3 %** | 0.808 | 37.5 % (5.4 %) | 1,204 ms |
| `nli_quiere_saber` + emb, k=3 | hyp "El visitante quiere saber {label}." | 70.5 % | 0.812 | 37.5 % (3.4 %) | 1,172 ms |
| `nli_answer_premise`, k=3 | state = answer; hyp "Este texto responde la pregunta «{q}»." | 70.5 % | 0.872 | 28.4 % (2.0 %) | 1,943 ms |
| `nli_answer_premise` + emb, k=3 | same, plus cosine | 75.0 % | **0.891** | 27.3 % (3.4 %) | 1,943 ms |
| `nli_qa_pair` + emb, k=3 | state = "Pregunta… Respuesta…"; hyp "La respuesta contesta lo que pregunta el visitante." | 73.9 % | 0.891 | 19.3 % | 2,188 ms |
| `noul_answers` + emb, k=3 | yes/no "¿La respuesta candidata contesta la pregunta?" | 61.4 % | 0.862 | 18.2 % | 1,950 ms |
| `noul_label` + emb, k=3 | yes/no "¿La pregunta trata exactamente de este tema?" | 44.3 % | 0.738 | 17.1 % | 1,660 ms |
| `score_answer` + emb, k=3 | 4 levels, from "no relation" to "answers exactly" | 47.7 % | 0.794 | 5.7 % | 2,472 ms |
| `score_label` + emb, k=3 | 4 levels on the topic | 42.0 % | 0.688 | 5.7 % | 2,208 ms |
| `choice_label` + emb, k=3 | one question, labels + "ninguna" | 59.1 % | 0.743 | 6.8 % | 313 ms (k=3) |
| `choice_answer` + emb, k=3 | one question, label + first sentence of the answer | 46.6 % | 0.657 | 3.4 % | 530 ms (k=3) |

### Findings

1. **The prompt moves top-1 by up to 13 points** among the NLI variants. None beats embeddings by
   the +5 points the rule asks for; the best (`nli_label` + emb, k = 3) is +1.2 points, inside the noise.
2. **The answer-as-premise variant gives the best confidence signal.** It is the only one whose
   AUROC matches or beats cosine (0.89), and it is the closest to "does this answer fit the query".
3. **`score` and `noul` do not work with this checkpoint.** The score probabilities come out almost
   flat (0.35 / 0.33 / 0.32), and noul saturates at 0 or 1. The PT/ES fine-tune trained only the
   3-way `choice` head.
4. **Only `choice` meets the latency budget** (313 ms at k = 3), and it is the least accurate.
5. **These latencies are higher than in E7:** 1,204 ms vs 745 ms for the same `nli_label` k = 5.
   The Phase 2 agents were using the CPU at the same time. Read them as relative, not absolute.

**Verdict unchanged:** no prompt makes zero-shot Laya pass. The way forward is fine-tuning Laya on
Phase 2 data:

- format: (query, candidate answer) pairs, with hard negatives taken from the e5 top 5;
- head: `choice` or NLI, the head this checkpoint already trained.

## E9: Laya fine-tune setup on the Phase 2 corpus (2026-11-22)

**New baseline: e5-base alone on the full corpus.**

| Item | Value |
|---|---|
| Corpus | 806 entries, 10,068 examples |
| Eval | Phase 2 clean subset: 1,630 paraphrases, 80 near miss, 80 out of scope |
| Top-1 | 63.3 % |
| Correct in top 3 | 82.2 % |
| Correct in top 5 | 87.6 % |
| Answered at ≤ 3 % wrong, cosine threshold | 16.9 % (3.1 % of out-of-domain answered) |
| Answered at ≤ 3 % wrong, margin threshold | 26.5 % |

Raw numbers are in `results/p1-laya/p2_baseline.json`.

**Gate for the fine-tuned Laya, measured on ONNX int8 on the laptop CPU:**

- top-1 ≥ 68.3 %, or ≥ 36.5 % answered at ≤ 3 % wrong;
- p50 ≤ 400 ms at k = 5.

**Format:**

- one listwise `choice` question;
- options are the e5 top-k labels plus `ninguna de estas opciones`;
- pool size k is 3-5 during training, and options are shuffled each epoch.

**Data:** `uv run python ft_data.py build` writes everything to `data/knowledge/laya_ft/`.

| Item | Value |
|---|---|
| Training rows | 8,618 |
| Rows whose target is "ninguna" | 2,393 (28 %, natural pool misses only) |
| Dev rows | 450 |
| Eval rows | 1,790 |

- **Masking:** each training pool comes from e5 with the query's own vector masked.
- **Held-out entries:** 81 entries (10 %) never appear in training. 162 eval rows target them, which
  measures whether new topics need a retrain.

**Chain verified locally on CPU** (`ft_smoke.py`, plus a tiny run through `eval_ft.py`):

- dry_run, finetune, `laya.load`, 6-option predict, ONNX fp32 export and int8 all run;
- fp32 ONNX gives the same probabilities as torch;
- int8 changed a pick on the 1-epoch smoke model, so the gate runs both fp32 and int8.

**Training:** in Colab, `notebooks/finetune_laya.ipynb`.

1. A 200-row GPU smoke runs first.
2. The full run uses grad_accum 1, which gives ~2,150 optimizer updates.
3. The checkpoint (~650 MB) is zipped without the duplicate `checkpoint_latest/`, copied to Drive
   and downloaded **before** evaluation.

**Gate:** `uv run python eval_ft.py <checkpoint dir>`. It reports e5 (cosine and margin), Laya and
Laya + cosine, each for all rows and for held-out entries, at k = 5 and k = 3, with per-row
predictions on disk.

## E10: fine-tuned Laya results (2026-11-22)

Checkpoint `models/laya_ft_A`: run A, started from `laya-pt-es-nli`, trained in Colab. It was
evaluated on the 1,790 Phase 2 eval rows on the laptop CPU, idle except for the browser. Raw numbers:
`results/p1-laya/laya_ft_gate_laya_ft_A.json` and `quant_sweep_laya_ft_A.json`.

| Runtime | Size | p50 / p95 | Top-1 Laya | Top-1 Laya + cos | Top-1, never-trained entries (Laya + cos) | Answered at ≤ 3 % wrong (Laya + cos) | Out-of-domain says "ninguna" |
|---|---|---|---|---|---|---|---|
| e5-base alone (baseline) | — | ~30 ms | 63.3 % | — | 64.8 % | 16.9 % cosine / 26.5 % margin | — |
| ONNX int8 (all ops), k = 5 | 334 MB | 76 / 279 ms | 63.3 % | 65.0 % | 58.6 % | 23.2 % | 45.6 % |
| ONNX int8 (all ops), k = 3 | 334 MB | 59 / 283 ms | 66.4 % | 67.0 % | 66.7 % | 26.8 % | 58.1 % |
| ONNX fp32, k = 5 | 1,288 MB | 151 / 461 ms | 68.0 % | **69.3 %** | 60.5 % | 30.2 % | 55.0 % |
| **ONNX int8 embeddings only (Gather), fp32 layers, k = 5** | **699 MB** | **114 / 463 ms** | 67.7 % | **69.3 %** | 60.5 % | **30.2 %** | 55.0 % |
| ONNX int8 per-channel (all variants) | 334-924 MB | 71-86 ms | ~21 % | ~63 % | — | ≤ 15 % | — |

**Verdict: pass on the top-1 rule, with embedding-only int8.**

- Laya + cosine reaches 69.3 %, +6.0 points over e5 (the bar was ≥ 68.3 %).
- p50 is 114 ms, under the 400 ms bar.
- The coverage rule is not met: 30.2 % vs the 36.5 % bar.

**Caveats:**

1. **Quantization matters.**
   - Full int8 loses ~4-6 points and no longer beats e5 at k = 5.
   - Per-channel int8 breaks the model.
   - Quantizing only the vocabulary table keeps fp32 accuracy at about half the fp32 size.
2. **New topics need retraining.** On the 81 entries never seen in training, Laya + cos is 4.3
   points *below* e5 (60.5 % vs 64.8 %). Adding a section or entry is safe for e5 alone but needs a
   Laya retrain to keep the gain.
3. **Out-of-domain rejection is weak.** "ninguna" fires on only 55 % of out-of-domain questions,
   so a cosine floor must stay in front of Laya.
4. **Phone memory is tight.**
   - 699 MB resident for Laya on top of e5 and router r1, with ~1.5 GB free at idle.
   - Phone latency and RAM are not measured.
5. **Choice and a possible next run.** A single run with a fixed config. The k = 3 int8 result
   (67.0 %) suggests that a retrain at k = 3 with int8-aware choices could get close at 334 MB. Not tested.
