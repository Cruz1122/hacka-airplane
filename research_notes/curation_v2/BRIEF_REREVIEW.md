# Re-review brief (wave 4, fresh reviewers)

Read `BRIEF_COMMON.md` and `BRIEF_REVIEWER.md` first; the same checks and standards apply. You did
not write these proposals. Write boundary: `$W/reviews/S.rereview.json` (+ `S.rerefetch.json`) for
your sections. Change no proposal, audit CSV or corpus file.

## Scope per section S

1. **Ops:** only the IDs in `$W/reviews/S.rereview_queue.json`. Read them in
   `$W/proposals/S.v2.json`, the round-1 record in `$W/reviews/S.review.json` (what was asked), and
   `$W/decisions/S.fix.md` (what the curator says it did). Run
   `python3 $W/tools/verify_evidence.py --proposal $W/proposals/S.v2.json --refetch > $W/reviews/S.rerefetch.json`.
   Judge each queued op with checks 1–7 of `BRIEF_REVIEWER.md`. An op whose `required_change` was
   not done is `revise` (it is then left out of the corpus).
2. **Audit rows:** every row of `$W/audit/S.csv` that still claims `primary_ok`/`secondary_only`
   and was judged `partial` or `none` in round 1 (`audit_rows` of `S.review.json`). Open
   `evidence_ref`, judge whether the current `evidence_excerpt` supports the entry's **current**
   answer (`$W/proposals/S.v2.json` if the entry has an op there, else
   `$W/snapshots/sections_before/S.json`): `full`, `partial` (name the unsupported claim) or `none`.
   Rows judged `full` in round 1 are not re-judged.

## Output `$W/reviews/S.rereview.json`

Same shape as `S.review.json`: `ops` (one record per queued ID) and `audit_rows` (one record per
row in scope 2, plus `"excerpt_changed": true|false` against the round-1 note), and `summary`.
Final reply: at most 10 lines in Spanish with the counts per section and the worst problems.
