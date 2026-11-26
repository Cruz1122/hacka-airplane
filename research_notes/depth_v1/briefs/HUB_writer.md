# Hub short replies — first answer to broad questions

An offline assistant for Parque Nacional Natural Los Nevados (Colombia) answers broad questions
("qué fauna hay", "a qué altura queda") with a hub: a long overview (`reply`, markdown with
bullets). It is too long for a first answer and never varies. You write short first answers; the
visitor can say "sigue" to go deeper (the app handles that part).

## Read only
- The shard file given in the task (`hub_id`, `label`, `examples`, `reply`).

## Output
Write ONLY the output path given in the task, one row per text, hub by hub:
{"pid": "<hub_id>#h01", "hub_id": "...", "text": "..."}
Six texts per hub (h01..h06).

## Rules
1. Only facts from `reply`, stated exactly: numbers, units, names and qualifiers as written. Add
   NOTHING (no reason, advice, example or comparison that `reply` does not give). Keep any safety
   warning of `reply` that applies to the whole topic.
2. Short: 2-3 sentences, 30-60 words, plain prose (no bullets, no markdown, no emoji). Answer the
   question directly first, then the 2-3 most useful facts. Each text picks a different subset or
   order of facts where `reply` has enough of them.
3. Natural Colombian Spanish (tú), clearly different wording and opening between the six texts.
   No bridge phrases like "si quieres saber más" (the app adds those).
