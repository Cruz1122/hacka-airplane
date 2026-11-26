# Arbitration brief (authored-query labels)

Read `$W/BRIEF_COMMON.md` and `$W/BRIEF_VERIFY.md` (the standard both sides followed). Each record
is one visitor question with the author's label (`author`) and an independent verifier's verdict
(`verifier`). `kind: fix` = the verifier changed the label; `kind: ok_sample` = a random sample of
rows the verifier approved unchanged (you audit whether "ok" was right). `faqs` has label + short
of every FAQ involved; open `detail`/`steps` in `$W/inputs/kb_view.jsonl` (jq by id) when needed.

Decide the final label; you are the tie-breaker. Judge by answer text, not labels.
- `accept_fix`: the verifier's label is right.
- `keep_author`: the author's original label is right (the fix was wrong / ok was right).
- `final_fix`: both are wrong; you give the correct `case`, `gold`, `acceptable`, `near_ids_ok`.
- `drop`: real doubt, or the question is unusable. Doubt means drop.

Output `$W/judgments/authored_arbitration.<AGENT>.jsonl`, one line per record, same order:
`{"qid", "decision": "accept_fix|keep_author|final_fix|drop", "verdict": "ok|fix|drop",
"case", "gold", "acceptable", "near_ids_ok", "note": "≤ 20 words", "by": "<AGENT>/<model>"}`
where `verdict`/`case`/`gold`/`acceptable`/`near_ids_ok` are the FINAL label (`verdict: ok` with the
author's fields for keep_author; `fix` with the final fields for accept_fix/final_fix; `drop`).
Append per 30 records. Check by script before finishing (one line per qid, ids in
`$W/inputs/kb_catalog.jsonl`, gold ∈ acceptable for answerable). Reply ≤ 8 lines in Spanish:
decision counts, ok_sample error rate per verifier, 3 worst cases.
