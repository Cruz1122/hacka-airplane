# Chat reply variants — small talk of the park assistant

An offline assistant for Parque Nacional Natural Los Nevados (Colombia) answers small talk
(greetings, thanks, "who are you", limits of the app) with one fixed text (`canonical`). A visitor
who says "hola" twice sees the same sentence. You write alternatives so replies rotate.

## Read only
- `shards/CHAT.json` (30 entries: `entry_id`, `label`, `examples`, `canonical`, `other_text`).

## Output
Write ONLY `proposals/CHAT.jsonl`, one row per text, entry by entry:
{"pid": "<entry_id>#c01", "entry_id": "...", "text": "..."}
Six texts per entry (c01..c06).

## Rules
1. Same meaning and same promises as `canonical`: every limit, instruction, channel, name, phone,
   URL and condition it states stays, exactly as written. Add no new fact, capability, place or
   advice. If `canonical` says the app cannot do something, every variant says so too.
2. Clearly different wording and sentence order from `canonical` and from each other; vary the
   opening word. Warm, brief, natural Colombian Spanish (tú). Length within ±40 % of `canonical`.
3. No emojis, no lists, no exclamation in every text.
