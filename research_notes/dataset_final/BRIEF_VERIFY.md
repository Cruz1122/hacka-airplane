# Authored-query verification brief

Read `$W/BRIEF_COMMON.md` first. You verify questions **another model wrote**; you did not write
them. Each record of your shard has the question `q`, the author's label (`case`, `gold`,
`acceptable`, `near_ids`, `why`), the 3–5 FAQs the app's retriever really returns
(`retrieved_pool`), and the label + short answer of every FAQ involved (`faqs`). Open
`detail`/`steps` in `$W/inputs/kb_view.jsonl` (`jq 'select(.id=="<id>")'`) only when the short is not
enough to decide.

For every record decide:

1. Is the question something a real visitor would write, and not a copy of a label? If it is
   nonsense, duplicates another record, or leaks the answer → `drop`.
2. `answerable`: does `gold`'s answer really answer it? Does any **other** FAQ in `faqs` (pool
   included) also fully answer it? Then it belongs in `acceptable`. Is any `near_ids` FAQ actually
   answering it? Then it must leave `near_ids` (and go to `acceptable` if it fully answers).
3. `none`: does any FAQ in `faqs` answer it after all? Then it is `answerable` (fix) or `drop`.
   For prompt-injection / requests the app cannot do, `none` is right.
4. `ambiguous`: are the listed FAQs really the plausible readings (2–3), and is the question really
   under-specified? If one FAQ clearly answers it, fix to `answerable`.
5. `emergency` rows: is `gold` the FAQ with the immediate, concrete guidance?

Verdicts: `ok` (label correct as written), `fix` (you give the corrected `case`, `gold`,
`acceptable`), `drop` (unusable or you cannot decide — doubt means drop).

## Output `$W/judgments/authored_verify.<AGENT>.jsonl`

One line per record, same order:
`{"qid": "...", "verdict": "ok|fix|drop", "case": "...", "gold": "...|null", "acceptable": [...],
"near_ids_ok": [...], "note": "≤ 20 words", "by": "<AGENT>/<model>"}`
- Always write `near_ids_ok`: the subset of `near_ids` you confirm does **not** answer `q`.
- For `ok`, copy `case`/`gold`/`acceptable` unchanged; for `fix`, give the corrected ones (IDs must
  exist in `faqs` or `kb_catalog.jsonl`).

Read the shard in chunks of 30 lines (`sed -n`), append output per chunk. Before finishing, check
by script: one output line per input qid, verdict values valid, every ID exists in
`$W/inputs/kb_catalog.jsonl`, `gold ∈ acceptable` for answerable rows. Final reply ≤ 8 lines in
Spanish: counts per verdict, the 3 worst problems.
