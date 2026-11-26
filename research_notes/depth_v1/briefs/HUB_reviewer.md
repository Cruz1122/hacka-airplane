# Hub short replies — reviewer

## Read only
- The shard file (`hub_id`, `reply`) and the proposals file given in the task (`pid`, `hub_id`, `text`).

## Output
Write ONLY the output path given in the task, one row per proposal row, in input order:
{"pid": "...", "verdict": "ok|drop", "note": "<= 12 words, required for drop>"}

## `ok` only if all hold, else `drop`
1. Every fact is in the hub's `reply`, with identical numbers, units, names and qualifiers; no
   softening, hardening, generalising, or moving a fact to another place.
2. Nothing added: no reason, advice, example or comparison absent from `reply`. A safety warning
   that `reply` gives for the whole topic is not dropped when the text covers that topic.
3. Answers the hub's question directly; 2-3 sentences of natural Colombian Spanish; no bullets,
   markdown or emoji; not a near-copy of a sibling text.
