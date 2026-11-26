# Chat reply variants — reviewer

## Read only
- `shards/CHAT.json` (entries with `canonical`) and `proposals/CHAT.jsonl` (rows `pid`, `entry_id`, `text`).

## Output
Write ONLY `reviews/CHAT.jsonl`, one row per proposal row, in input order:
{"pid": "...", "verdict": "ok|drop", "note": "<= 12 words, required for drop>"}

## `ok` only if all hold, else `drop`
1. Same meaning as `canonical`: keeps every limit, instruction, channel, name, phone, URL and
   condition; adds no fact, capability, place or advice; promises nothing the canonical does not.
2. Natural, warm Colombian Spanish; no emoji; not a near-copy of `canonical` or of a sibling text.
