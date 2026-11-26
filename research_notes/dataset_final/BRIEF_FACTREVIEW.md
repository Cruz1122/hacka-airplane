# Factual proposal review brief

Read `$W/BRIEF_COMMON.md` and `$W/BRIEF_FACTUAL.md` (the standard the author followed). You did not
write these proposals. Input: `$W/work/factual_diff.<P>.json`: per op the changed fields (before /
after) and its evidence records (`url`, `path`, `quote`). Open each cited evidence file (`path`,
relative to `$R`) with `grep -n` around the quote to read context; do not read whole files.

For every op judge:
1. Every factual claim in the new `answer` (short, variants, detail, steps) is supported by a quoted
   passage (or by text that was already there and was already sourced). Numbers, prices, dates,
   places, distances: exact match with the source.
2. Dated facts are presented as dated (source + date), never as today's state; conflicting official
   sources are both shown, none picked as current.
3. Nothing implies the app/phone contacts rescue, sends location or registers anything.
4. Emergency guidance stays immediate; nothing safety-relevant was removed without reason.
5. The change fixes what its `reason` says and does not degrade the answer for a visitor.

Verdicts: `approve`, `revise` (name the exact claim and fix), `reject`.
Output `$W/reviews/<P>.review.<AGENT>.json`: `{"proposal": "<P>", "ops": [{"id", "verdict", "note"}], "summary"}`.
Write skeleton first. Final reply ≤ 8 lines in Spanish.
