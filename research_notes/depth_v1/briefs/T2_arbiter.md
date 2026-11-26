# T2 arbiter — blind_v4 label disputes

An offline park assistant answers each visitor message with ONE curated entry (top-1). Two
independent labelers disagreed on the units in your shard. You decide the gold label. These labels
are the exam the system is graded on, so be exact, not generous.

## Read only
- The arbitration shard given in the task. Nothing else. No web.

## Each unit has
- `turns`: the conversation so far. Label only the LAST turn, using earlier turns as context.
- `candidates`: the only ids you may choose. Look each up in the shard's `catalog` (label, start of
  the answer).
- `both`: ids both labelers accepted. `disputed`: ids only one labeler accepted.
- `A`, `B`: the two labels (acceptable_ids, out_of_scope, is_continuation). They are not ranked; either
  may be wrong.

## Output
Write ONLY the output path given in the task: JSONL, one row per unit, in shard order, appended as
you go. Reply with one line: "<output path> <rows>".

{"uid": "...", "acceptable_ids": ["<candidate id>", ...], "out_of_scope": false, "is_continuation": null, "note": "<short reason>"}

## Rules
1. `acceptable_ids`: every candidate whose answer would correctly and directly answer the last turn in
   context. Judge each id in `both` and `disputed` on its catalog text. An id that only touches the
   topic, or answers a neighbouring question, is NOT acceptable. Hubs (`hub.*`) only when the question
   is broad.
2. `out_of_scope: true` with `acceptable_ids: []` when the message is outside the park or no candidate
   answers it. Off-topic chatter: `["conversation.off_topic_question"]` if that candidate is present.
3. `is_continuation` (only for `cont_pos`/`cont_neg` units at turn 1; null otherwise): true when the
   last turn asks to continue or expand the previous answer ("sigue", "cuéntame más", "¿por qué?");
   false for thanks, yes/no, a new elliptic question, or "¿sigue abierto?". If true, `acceptable_ids: []`.
4. Always write a `note` (≤15 words) saying why you dropped or kept the disputed ids.
