# Hard-negative pair judgment brief

Read `$W/BRIEF_COMMON.md` first (short). Then judge every record of your shard file.

Each record is a pair of FAQs: `a` is the FAQ that answers the `samples` (real visitor questions
labelled with `a`), `b` is another FAQ the retriever put next to it. Training will teach the model:
"for these questions, `b` is wrong". That is only true if `b`'s answer does **not** answer them.

For each pair decide, reading `a_short` and `b_short` (open `detail`/`steps` in
`$W/inputs/kb_view.jsonl` with `jq 'select(.id=="<id>")'` only when the short is not enough):

- `distinct`: `b`'s answer does not answer the samples (it covers another aspect, place, species,
  number, rule…). `note` = what `b` lacks, ≤ 15 words.
- `also_answers`: `b`'s answer fully answers the samples too (duplicate or superset). `note` = why.
- `query_dependent`: `b` answers some samples but not others, or answers them only partly, or a
  visitor could reasonably mean either. `note` = which part.
- `mislabeled`: the samples are clearly answered by `b` and **not** by `a`. `note` = why.

Judge by the answer text, never by the label alone. Shared words do not make answers equivalent
("baños" ≠ "baños termales"; symptoms ≠ prevention). When in real doubt, use `query_dependent`
(the row is then dropped from training — that is the safe choice).

## Output `$W/judgments/pairs.<AGENT>.jsonl`

One line per input record, same order:
`{"a": "...", "b": "...", "verdict": "distinct|also_answers|query_dependent|mislabeled", "note": "...", "by": "<AGENT>/<model>"}`

Write in chunks of 40 records (append), so partial work survives. Before finishing, check by script
that every input `(a, b)` has exactly one output line and every verdict is one of the four values.
Final reply ≤ 8 lines in Spanish: counts per verdict and 3 worst examples.
