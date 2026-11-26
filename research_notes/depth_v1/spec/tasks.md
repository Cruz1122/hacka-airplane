# Tasks — depth_v1

Execute in order. A task starts only when its dependencies have closed their gate. "Orchestrator"
tasks are scripts and integration; no subagent does them. Each task closes by writing
`decisions/Tn.md`: numbers, what failed, what was dropped.

Shard counts assume 806 entries. Re-compute them in T0 and keep the shard sizes.

## T0 — Baseline and digests (orchestrator)
Depends: none.

1. Run `git status`. List files with changes unrelated to this mission and do not touch them.
2. Snapshot the sha256 of `data/knowledge/sections/` and `data/knowledge/app/`.
3. Write `tools/digest.py` (design §7) and generate:
   - `inputs/headroom.jsonl`, one row per entry:
     - source URLs → evidence files;
     - quotes and words available that are not yet used in L0;
     - class `rich | some | none`.
   - `inputs/detail_overlap.jsonl`: the share of `answer.detail` already present in L0.
   - `inputs/followup_failures.jsonl`: the v2/v3 follow-up failures classified as `gate_miss |
     fused_wrong | label`. v3 informs the design only and is never scored.
   - `inputs/baseline.json`: per-entry counts of examples, aug and convs.
4. Find out why the frailejón facts in `flora_ecosystems.research.md` (growth of 1–2 cm/yr,
   necromass) have no corpus entry. Check `dedup_decisions.json` and the addition transactions, and
   log the cause.

**Done:** all 4 inputs exist, and `decisions/T0.md` holds the headroom histogram per section plus
the frailejón cause.

## T1 — Roster (orchestrator)
Depends: none.

1. Create `.opencode/agents/nv-go.md`, `nv-zen.md` and `nv-luna.md` following design §8.
2. Smoke-test each one with a trivial task that writes 1 JSONL row.
3. Write `decisions/roster.md` with the exact model ids.

**Done:** 3 rows exist, each with the right `by`.

## T2 — blind_v4 (BEFORE any new variant or conversation exists)
Depends: T1. Runs in parallel with T0 and T3a.

1. **Writers:** 4 shards with alternating families. Each writer sees only
   `blind_v4/brief_public.md`, which you write: a public park description of 1 page plus 8
   visitor personas. Writers never see the corpus, the labels or the system. Each shard writes:
   - 150 single-turn rows;
   - 75 multi-turn follow-up turns, in 2–4-turn conversations with topic switches;
   - 38 continuation positives in context;
   - 38 short non-continuation negatives.
2. **Labelers:** 4 shards with families different from their writers.
   - Labelers see a candidate list: the top-10 ft4 entries plus labels, by script.
   - Each assigns `acceptable_ids`, or `out_of_scope`, or `is_continuation`.
   - A second labeler from the other family checks 100% of rows, and Luna arbitrates
     disagreements.
3. **Split:** the orchestrator splits by family hash into `v4_dev` (40%) and `v4_sealed` (60%),
   writes `v4_sealed.sha256` and **never opens v4_sealed again** in this mission.
4. **Baseline:** run ft4 on v4_dev with `experiments/nlu/gguf_eval.py --blind` (single-turn and
   multi-turn).

**Done:** v4 has ≥600 single-turn rows, ≥300 multi-turn turns, and 150 + 150 continuation rows.
Baseline numbers are in `decisions/T2.md`.

## T3 — Depth layers (R3)

### T3a — Write layers from existing sources
Depends: T0, T1.

1. Shards: 8 entries each, about 97 shards. Order:
   - `flora_ecosystems`
   - `fauna`
   - `weather_volcano`
   - `health_safety`
   - `rules`
   - `geography`
   - `history_culture`
   - `activities`
   - `access`
   - `booking_fees`
   - `preparation`
   - `hours_status`
   - `services`
   - `actions`

   Skip `conversation` and `kind: chat`.
2. Each shard holds, per entry: the corpus entry, L0, related ids with their labels, the T0
   headroom row, and evidence windows of at most 30k tokens per shard.
3. **Writer:** writes L1 and L2 (design §3), every sentence with its support, plus `corpus_ops`
   for facts not yet in the corpus. If there is no support, it sets `no_headroom_reason` and
   writes no layers.
4. **Verifier** (the other family): gives a verdict per sentence, checks numbers, and checks that
   the L0 safety text is kept.
5. **Arbitration:** Luna arbitrates every `fix`. Any `unsupported` sentence is deleted.
6. **Checks:** `tools/check_depth.py` runs on 100% of rows. `health_safety` and `rules` get a
   second independent verifier on 100% of rows; other sections on ≥10%.

### T3b — Research for entries without headroom
Depends: T3a for that section.

1. **Input:** every `no_headroom` entry, plus every `none` entry from T0, in shards of 5.
2. **Researcher** (`nv-luna` or `nv-go`, alternating): looks for official or academic public
   sources: PNN, SGC, IDEAM, Humboldt, universities, GBIF/SiB, published papers. It saves the
   evidence through the `add-park-knowledge` research flow and proposes `corpus_ops` with literal
   quotes plus L1/L2.
3. **Review:** the same verification and arbitration as T3a.

### T3c — Integrate depth (orchestrator, once per section)
Depends: T3a and T3b for that section.

1. Corpus ops go through `knowledge.py stage`, then `apply`, then `validate_knowledge.py` (Errors: 0).
2. `tools/integrate.py` writes `depth_replies.json`, including `walk`.

**Done (T3):**
- `tools/coverage.py` shows L1 on ≥90% and L2 on ≥70% of non-exempt entries.
- Unsupported sentences: 0.
- The L0 hashes of `kind: safety` and `kind: rule` entries are unchanged.
- Every `no_headroom` entry has a reason.

## T4 — Query variants (R1)
Depends: T2 closed (v4 written and sealed), T1.

1. **Write shards:** 20 entries each, about 41 shards.
   - Inputs: id, label, L0, 3 current examples, the related labels as "do NOT ask these", and the
     bucket mix of R1.2.
   - Per entry, a shard writes 24 variants. The surplus absorbs drops.
2. **Review shards:** 40 entries each, about 21 shards, by the other family. Each row gets
   `ok | fix(entry) | drop`, and the reviewer checks R1.3 (answerable by this entry's answer).
3. **Arbitration:** Luna arbitrates every `fix`.
4. **Checks:** `tools/check_rows.py` runs dedup, near-dup, bucket mix, the continuation lint and
   leaks against v4 (v4_dev and v4_sealed, in both directions). `tools/pairs.py` builds the
   pair-judgment shards (280 pairs each, alternating families).
5. **Top-up:** any entry still below 20 approved variants gets a round with a new writer of the
   other family.

**Done:** ≥20 approved variants for 100% of non-conversation entries (≥10 for conversation
entries). Leaks: 0. Every pair is judged.

## T5 — Follow-up conversations (R2)
Depends: T2 closed, T1. Runs in parallel with T4.

1. **Write shards:** 25 entries each, about 33 shards.
   - Inputs: id, label, L0, related ids with labels and L0, and 5 unrelated entries for switches.
   - Per entry, a shard writes 10 conversations of the mix in R2.2, every turn labelled.
2. **Review shards:** 40 entries each, about 21 shards, by the other family. Each turn gets a
   verdict.
3. **Arbitration:** Luna arbitrates every `fix`.
4. **Checks:** `check_rows.py` runs the same checks as T4, per turn. A conversation turn may not be
   a bare continuation cue.
5. **Top-up:** any entry below 8 approved conversations gets a top-up round.

**Done:** ≥8 approved conversations for 100% of entries. Leaks: 0.

## T5b — Reply paraphrases: same question, different answer (R6)
Depends: T1. L0 paraphrases start at once. Layer paraphrases start per section after T3c.

1. **Write shards:** 10 entries each.
   - Inputs: id, kind, canonical L0, the facts list (numbers, names and caveats extracted by
     script), and for layers the approved layer texts.
   - The writer produces 10 L0 paraphrases per entry, of which ≥8 must survive, and 5 per layer,
     of which ≥4 must survive. Every paraphrase is tagged with a structure and a register (R6.3,
     R6.4). It adds no fact and drops no caveat.
2. **Review shards:** 20 entries each, by the other family. Each paraphrase gets `same_facts`,
   `caveats_kept`, `natural` and a verdict.
   - `kind: safety` and `kind: rule` entries get 100% double review.
   - `emergency_direct` entries get a second verifier of the other family on every paraphrase.
3. **Arbitration:** Luna arbitrates every `fix`.
4. **Checks:** `tools/check_replies.py` runs on 100% of rows: facts identical, distinctness and
   structures.
5. **Top-up:** an entry below 8 L0 paraphrases, or with a layer below 4, gets a top-up round with
   a writer of the other family.
6. **Integration:** `integrate.py` writes `reply_variants.json` and the `texts` lists in
   `depth_replies.json`.

**Done:** A11 and A12 pass on the E2E. Every entry below target is either topped up or covered by
the R6.6 exceptions.

## T6 — Integrate variants and conversations (orchestrator)
Depends: T4, T5.

1. `integrate.py` writes `train_variants.json` and `train_convs.json`. Pair verdicts are applied:
   - `also_answers` becomes an extra acceptable id;
   - `query_dependent` is excluded from training.
2. **Index A/B:** with the ft4 model on v2, compare today's index against today's index plus the
   new variants.
   - Promote to `index_additions.json` only variant groups that win on v2.
   - Then check v4_dev for no regression (N4).

**Done:** both files exist with validators green, and the A/B table is in `decisions/T6.md`.

## T7 — Continuation runtime (R4)
Depends: T0. Can start at once with layers stubbed. It closes after T3c.

1. **Implementer** (one child): reads `.claude/skills/mobile-offline-stack/SKILL.md` and
   `hackathon-lean`, then implements design §6 in `export_nlu.py`, `assets.ts` and `engine.ts`,
   with jest tests and `tools/e2e_sigue.ts`.
2. **Reviewer:** another family reviews the code. A third pass by Luna checks the safety paths
   (urgent clears state, null policy = today).
3. **Checks:**
   - Mobile tests, typecheck and lint.
   - E2E "sigue ×4" over all 806 entries with the real `depth_replies.json`.
   - Detector precision and recall on v4_dev continuation rows.

   - Rotation (R6.5): same question ×8 gives 8 texts, wrap-around never repeats the last text,
     and emergency entries rotate only over their double-approved set.

**Done:** A5, A6, A7 and A11 pass.

## T8 — Ft5 package (orchestrator)
Depends: T3c, T5b, T6, T7.

1. Build the training rows (design §9): single-turn from corpus + aug + train_variants, multi-turn
   from followup_convs + train_convs, plus the batch-plan clusters and the anchor token-length
   report.
2. `tools/package.py` writes `out/NEVADOS_E5_FT5_DATASET.zip` with:
   - the rows and the batch plan;
   - v4_dev and the v4_sealed hash (not the sealed file itself);
   - validators and `MANIFEST.json`;
   - `QUALITY_REPORT.md`, `COLAB_HANDOFF.md` and `DECISION_LOG.md`.
3. Extract the ZIP to a clean directory and re-run the validators with `python -I`. A grep for local
   paths, the username and the email must find nothing.

**Done:** A10 passes.

## T9 — Final verification and report (orchestrator)
Depends: T8.

Re-run the full acceptance table A1–A12 from `requirements.md` yourself and read the real output.
Then reply with the final report format in `ORCHESTRATION_PROMPT.md`.
