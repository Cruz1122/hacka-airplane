# Decision log — depth_v1

1. 2026-11-24 — Harness: the mission runs in T3 Code, not OpenCode. Roster agents map to T3
   `delegate_task` targets instead of `.opencode/agents/*.md` (see roster.md). Same models.
2. 2026-11-24 — Evidence windows use captured `.txt` only; agent-written `.md` notes are excluded
   (T0.md, frailejón cause).
3. 2026-11-24 — Provenance classifier + purged-claims blocklist added to T0 (advisor review): a
   literal quote from an agent-written summary is not support. Expect more T3b load.
4. 2026-11-24 — User: no OpenCode subagents. Roster is nv-sonnet (claudeAgent/claude-sonnet-5-5) ↔
   nv-luna (codex/gpt-6-luna), chosen by the user. Arbitration is a fresh Luna session; with two
   families it shares the verifier's family on even shards (logged limitation).
5. 2026-11-24 — User: replies must be stochastic and hold info back on purpose, so follow-ups have
   more to give. Added R7 (fact inventory key/complement, ≤ half the complements in L0, varied
   subsets, "sigue" by unserved atoms, whole pre-approved texts only) and A13, plus task T3.0.
   R6.2/A12 relaxed from "identical facts" to "all key facts, nothing outside the inventory".
   Non-goal change: canonical L0 leaves the rotation for R7.6-eligible entries.
6. 2026-11-24 — T3.0 fixes are resolved by script in the conservative direction only (drop
   unsupported/off-topic, narrow partial to the verifier's text, apply class changes; a verifier can
   only remove or demote support, never add facts). No arbitration task is spent on these: it cannot
   change fidelity. Arbitration stays for T4/T5/T5b label disputes.
7. 2026-11-24 — Luna failed to write its output file twice (T2_w3 first try, T30_007). T30_007 reassigned to Sonnet as writer, Luna verifies. Luna briefs now say to retry failed writes.
8. 2026-11-24 — T3.0 from shard 015 on: Sonnet writes, Luna verifies (no alternation). Reason: Luna's inventories yield ~1/3 the complements of Sonnet's and Luna failed 2 file writes; R7 volume depends on complements. Cross-family rule kept. check_facts 'asked' rule now ignores topic words and words already in L0 (it was forcing every fact naming the species to key).

## 9. T2 merge rules (script) and arbitration volume
- labels_a vs labels_b: 740 exact agreements, 92 hub-only differences (union kept; strict metric
  drops hubs anyway), 872 disputes -> 10 fresh-Luna arbitration shards (arb_shards/A00-A09).
- On cont_pos/cont_neg turn 1 a null is_continuation is read as false: 86 of the 118 raw
  continuation "disagreements" were one labeler leaving the field unset on a negative.
- L10 pass b: the retry claimed 100 rows but wrote 63; the 37 missing units were relabeled as L10x.
- L00 pass b (Sonnet) read a truncated catalog and labeled mostly by id; its disputes are arbitrated
  like any other. Later Sonnet briefs say to print the shard with python3 when a read truncates.
- Arbitrated ids are filtered to the unit's candidates by script (t2_merge.py final).

## 10. A verifier "should_be: key" alone does not move a complement
- T30_038/039 (Luna verify) marked 32/45 and 45/56 complements as key with the note "directly
  requested or caution facts", for facts L0 never states (e.g. "the Ruiz is 5321 m" on the Nereidas
  entry). Applied as is, that erases R7's withheld complements.
- check_facts.py now applies a verifier key-move only when a script rule agrees (forced kind,
  steps, disclaimer, asked-by-a-question) or L0 already states >=60 % of the fact's content words.
  Otherwise it counts `verifier_key:overruled` and keeps the writer's complement. should_be
  complement is still applied; forced-key rules still win over it.
- Overruled so far: 89 facts (25 in 038, 44 in 039; the rest scattered). T30_verifier.md now says
  complement is the default for facts L0 does not state.

## 11. Codex Luna quota exhausted -> Luna via Cursor (user choice); Sonnet writes T4/T5
- 2026-11-24 ~18:30: gpt-6-luna (Codex) failed with "ChatGPT usage limit reached" (T5_001).
- User chose the same family through Cursor: `cursor / gpt-5.6-luna`, reasoning medium
  (ledger agent `nv-luna-cursor`). It takes every verify / review / arbitration role.
- T4_001 (Codex Luna writer) is rejected: every variant templates a key fact verbatim
  ("Parce, ¿qué me cuentas de esto: <fact>?"). As in T3.0 (entry 8), Sonnet writes all T4 and T5
  shards and the Luna family reviews them; cross-family review is kept.

## 12. T5 merge: intermediate-turn example copies are kept; writers now produce 12 per entry
- T5_000 review (Cursor Luna): 181 ok, 69 drop; 59 drops were "a turn copies an example verbatim".
  24 of those copy only an intermediate (context) turn, whose label is correct: t45_merge.py keeps
  them. A copy in the labelled last turn stays dropped.
- After check_rows (18 leaks vs v4: generic short turns) T5_000 keeps 187 conversations, 12 of 25
  entries below 8. T5_writer.md now asks 12 per entry and forbids example reuse in any turn;
  entries still below 8 get the T5 top-up round.

## 13. T4 review: fragments re-reviewed; near-dup needs lexical overlap too
- T4_000 review (Cursor Luna) dropped all 80 `fragment` rows as "bare fragment, not a complete
  question", although R1.2 asks for 3 fragments of 1-4 words per entry. T4_reviewer.md now says
  fragments are search-box style by design. The 80 rows go to a fresh re-review
  (proposals/T4_000f.jsonl -> reviews/T4_000f.jsonl, which overrides those verdicts in t45_merge).
- R1.4 near-dup in the ft4 space: ft4 pulls an entry's queries together, so cos >= 0.93 alone
  removed differently worded variants (e.g. "q ecosistemas protege el parque nevados" vs "qué más
  hay por allá aparte de montaña, ¿qué ecosistemas protegen?", cos 0.935). check_rows.py now calls
  a near-dup cos >= 0.93 AND content-word Jaccard >= 0.5. T4_000: near-dups 48 -> 16.

## 14. T3.0: document numbers from the capture file name (2026-11-24)
- check_facts rejected facts like "La Resolución 207 de 2023 fija el ingreso a Laguna Verde…"
  because 207/2023 sit in the capture file name (`resolucion_207_2023.txt`), not in the quote.
  The file name is set at capture time and the script checks the file exists, so it identifies
  the document. check_facts now adds the capture file stem to the support text for the
  numbers rule. All resolved T30 shards were re-resolved; 53 number rejections remain.
- T4 shards already emitted were not rebuilt (t4_shards never rewrites); the change mostly adds
  complements, which feed T3a depth layers, not T4.
- Audit (2026-11-25): every (file stem, number) pair that rescued a fact is a document number,
  a year or a bulletin date range (e.g. `resolucion-207-2023`, `sgc-ruiz-boletin-2026-11-10-16`
  -> "boletín del 10 al 16 de noviembre de 2026"). No incidental digits passed.

## 15. T5b: numbers in the canonical L0 count as key (2026-11-25)
- 14 entries have numbers in `natural_replies` that no inventory fact carries
  (`inputs/inventory_holes.json`; e.g. 1985/1988/1989 rejected in T30_041x). "Key facts are
  implied in every L0" (Part B 5b), so check_replies requires every L0 number in each paraphrase
  (list markers "1." excluded) and allows only L0 numbers plus those of the atoms it tags.

## 16. T5b: goal 8 kept for safety/rule entries (user, 2026-11-25)
- Pilot T5b_P00 after the full chain (write, review, arbitration, second review, check_replies):
  62/100 kept, 5/10 entries below goal; safety/emergency entries kept 1-3 of 10 (second review
  drops reordered actions, added details and moved responsibilities; R6.3 drops near-copies).
- User chose to keep R6.1 (>=8) for all non-exempt entries. R6.6 still applies to the 39
  emergency entries (>=3 emergency_ok or canonical). Entries below goal get top-up rounds
  (writer of the other family, T5b step 5) until they pass.
- Second-review brief: only action order is fixed; caveats/context sentences may move.
- check_replies: canonical compared only when it stays in rotation (R7.6); greedy keep by fewest
  conflicts instead of input order.
- Correction (2026-11-25): a canonical number that only a complement fact carries (e.g. "2006"
  in T5b_004 `otun_pajonal_espeletia`) is required only when the text tags that complement;
  requiring it forced the complement into every text, so nothing could be held back. Fixed in
  check_replies and t5b_shards; undispatched shards T5b_013-077 were regenerated.

## 17. T5b: R6.3 similarity measured without key-fact words (user, 2026-11-25)
- Deviation from R6.3 as written. Data: on 7 reviewed shards (70 entries) only 32 reached 8
  distinct texts with whole-text trigram Jaccard < 0.55; top-ups kept 31 of 107 new texts. Every
  paraphrase must repeat the key facts' names, places and numbers, so short or name-dense entries
  saturate the metric even when the wording differs.
- Now: content words (len > 3) of the entry's key facts are removed from both texts before the
  char-trigram Jaccard; threshold 0.55, first-4-words rule and goal 8 unchanged. User approved.
- Effect on resolved shards 000-010 (before pending arbitrations): entries below goal 39 -> 15.
  Near-copies still fail (pilot pair sharing a whole sentence: 0.71 -> 0.57, rejected).

## 18. T5b: hard length cap in check_replies (2026-11-25)
- Writers fighting the old similarity rule inflated texts (T5b_012 median 2.5x the canonical,
  T5b_010 1.7x; padding with filler). The brief asked ~1x (explained <= 1.5x) but nothing enforced it.
- check_replies now rejects a text longer than 2.0 x (canonical length + length of the complement
  facts it tags). The brief keeps 1.5x as guidance. Reviewers mark padded `brief` texts as fix.
- Effect: 005 below-goal 2 -> 4, 006 1 -> 1, 010 0 -> 1, 012 0 -> 6 (32 of 100 too long).

## 19. Arbitration re-run with entry facts in the queue (2026-11-25)
- The arbitration tasks for T5b_008, 011, 013-017 and U01r-U03r named no shard path, so the
  arbiter judged `fixed_text` without `canonical_L0` / key facts (one arbiter said so). Earlier
  arbitrations (P00, 000-010) did name the shard and stand.
- Fix: t5b_merge.py now writes `entry` (canonical_L0, key_facts, complements) into every
  arb_queue row; the arbiter brief requires judging against it. The 110 affected rows are
  re-arbitrated; the old verdicts are kept in arb_out/no_facts/ for comparison, not used.

## 20. Writer rule 8: no unsupported reasons in rule entries (2026-11-25)
- First review of T5b_026-028 (all `rules`) marked 25-36 of 100 rows `fix`, almost all
  "removes unsupported explanation / contextual claim / advice". Writer brief rule 8 now forbids
  adding a reason, consequence, example or advice the canonical does not give. Applies to shards
  written after this point (034+); 026-033 are corrected through review and arbitration.

## 21. Length cap base: longer of canonical L0 and the key facts (2026-11-25)
- In 128 of 776 entries the key facts together exceed 2x `canonical_L0` (e.g.
  `fauna.spotting_sector_brisas`: L0 137 chars, key facts 683). Reviewers require every key fact,
  so every correct text was "too long" and those entries lost all rows in the final check, top-up
  after top-up. `check_replies.py` now caps at 2x (max(len L0, sum of key-fact lengths) + tagged
  complements); writer brief rule 6 says so. The change only loosens the cap, so earlier
  shards can only gain rows; their finals are re-run.

## 22. Second-review rows carry the entry facts (2026-11-25)
- The second reviews of T5b_U09r, U10r and U11r were dispatched without the shard path, so the
  reviewer judged without `canonical_L0`/`key_facts` (U11r said so). `t5b_second.py` now embeds
  `entry{canonical_L0,key_facts,complements}` in every row and `briefs/T5b_second.md` points to
  it. Those three reviews are re-run; the old ones are in `reviews/no_facts/`. Every other
  second review had the shard path.

## 23. Partial T5b integration into the app (2026-11-25)
- User: "Así quedamos bien" → integrate what exists: shards 000-053 only (054-077 not written),
  the rule action-order rule unchanged (held rule second reviews stay out).
- `tools/integrate_replies.py` re-runs `t5b_final.py`, then writes `reply_variants.json` from
  `resolved/T5b_NNN.final.jsonl` only. It fails on an entry in two finals, on a safety/rule/emergency
  row without an ok second review, and never writes an empty list. Canonical first only below 2
  complements (R7.6), never `emergency_ok`.
- Top-ups number pids from `#u01`, so two top-ups of one entry collided (10 pids). `t5b_final.py`
  now tags rows with `src` and suffixes top-up pids with `@<src>`; the second-review guard looks up
  (src, pid).
- `depth_replies.json` is written as `{}` (T3 layers not done) because `export_nlu.py` emits
  `depth.json` and `policy.continuation` only when all three files exist. Effect: L0 rotation runs;
  "sigue" has no layers or walk yet and answers the exhausted text.
- First run: 531 entries, 5208 texts, 457 entries at >=8, 43 below (38 rules), 31 emergency entries
  all with >=3 `emergency_ok`, 275 entries without texts (240 in 054-077, chat/action exempt).
  A11 does not pass yet.

## 24. Second review: independent rule steps may move (2026-11-25)
- User: "tienes libertad con tal de cumplir con el objetivo y mantener coherencia y naturalidad".
  148 second-review drops were for action order alone, mostly rule entries listing independent
  duties (e.g. "don't feed animals; keep your distance"). Brief rule 1 now keeps the order only of
  steps that depend on each other; independent steps may move if the text stays coherent and
  natural. `emergency_ok` is unchanged: 100 % of the steps of `canonical_L0`, in order.
- Re-judged: the 148 order drops, the 13 held U11r/U15r rule rows, and the never-run second
  reviews of 033, 045, 047-051, 053 (queues `second_queue/R24_{sonnet,luna}*.jsonl`; old verdicts
  kept in `reviews/order_strict/`).
- Result (applied by `tools/r24_apply.py`): 245 re-judged, 167 ok. 159 order-drop rows had been
  queued without `entry` (old proposals predate decision 22); facts were added and those rows
  re-run, the blind verdicts discarded. Integration: 539 entries, 5406 texts, 478 at >=8, 30 below,
  emergency all >=3. Top-up round T5b_U17-U21 (45 entries, 236 texts) started for the rest.

## 25. Integrator caps texts without complements at 7 for R7.6-eligible entries (2026-11-25)
- A13 kept failing for `wax_palm_threat_table` after a targeted top-up (T5b_U22, 4 texts with one
  complement each): 15 of its 20 texts carry no complement, so the seeded rotation can serve 8 of
  them in a row (one subset across x8). A text may carry at most half the complements, so more
  complement texts alone cannot guarantee it. `integrate_replies.py` now keeps at most 7 texts
  without complements for entries with >=2 complements, only when the entry keeps >=8 texts.
  14 entries affected; each keeps 9-14 texts. Top-up rounds U17-U21 (45 entries) and U22 were
  written by Luna, reviewed by Sonnet, arbitrated and second-reviewed by fresh Sonnet.

## 26. Step C (T3) built from verified complements, plus the walk (2026-11-25)
- User: finish 054-077 and Step C "ASAP". Fast path that adds no new fact:
  - walk (R4.2, Part B §5) by script: `tools/integrate_depth.py`, related then 2-hop, e5 label
    cosine, no `actions.*`/chat, emergency entries only to health_safety/actions, max 6.
    777 of 783 non-chat entries get a walk.
  - layers (R3) only from the entry's own fact_inventory complements (verified with support in
    T3.0), so R3.5 holds and no corpus op or index change is needed. Entries with 2-3 complements
    get one layer, >=4 get L1 (why|how) + L2 (specifics), two texts each, disjoint atoms.
    Writer Luna (`briefs/T3L_writer.md`), verifier Sonnet (`briefs/T3L_verifier.md`, ok|drop, no
    fix round), script `tools/check_layers.py`, merge `tools/t3l_final.py`.
- Known gap against R3.4: only 485 of 776 non-exempt entries have >= 2 complements (62 %), so L1
  cannot reach 90 % this way; the 263 with none (all-key safety/rule/action entries among them)
  get walk only. T3b research and layer paraphrases (T5b layers) are not done.
