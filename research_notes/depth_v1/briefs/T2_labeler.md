# T2 labeler — blind_v4 gold labels

An offline park assistant answers each visitor message with ONE curated entry (top-1). You label
which entries correctly answer each message. These labels are the exam the system is graded on.

## Read only
- The label shard given in the task. Nothing else. No web.

## Output
- Write ONLY the output path given in the task: JSONL, one row per unit, in shard order, appended as
  you go. Reply with one line: "<output path> <rows>".

## Row schema
{"uid": "...", "acceptable_ids": ["<candidate id>", ...], "out_of_scope": false, "is_continuation": null, "note": "<short, optional>"}

## Rules
1. Each unit gives the conversation so far (`turns`; label only the LAST turn, using earlier turns as
   context) and `candidates` (ids). Look up each id in the shard's `catalog` (label, start of the
   answer).
2. `acceptable_ids`: every candidate whose answer would correctly and directly answer the last turn in
   context. Usually 1-3. Hubs (`hub.*`) are acceptable when the question is broad. Choose ONLY from
   the candidates.
3. `out_of_scope: true` and `acceptable_ids: []` when the message is outside the park (other places,
   cooking, homework...) or nothing in the candidates answers it. Off-topic messages:
   `acceptable_ids: ["conversation.off_topic_question"]` if that candidate is present, else [].
4. `is_continuation`: for units of type `cont_pos` / `cont_neg` with turn 1 ONLY: true if the last
   turn asks to continue/expand the previous answer ("sigue", "cuéntame más", "¿por qué?"...), false
   otherwise (thanks, yes/no, a new elliptic question, "¿sigue abierto?"). If true, set
   `acceptable_ids: []`. For every other unit leave it null.
5. Do not guess: if two candidates are equally right, list both. If none is right, use [] and say so
   in `note`.
