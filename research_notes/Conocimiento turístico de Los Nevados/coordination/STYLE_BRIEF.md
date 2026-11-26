# Final style pass — binding brief (no new facts)

Offline retrieval-only tourist assistant for PNN Los Nevados: the tourist's question is matched against each
entry's `examples`; the entry's `answer.short` is shown verbatim. You improve wording only.

Working dir `/home/cruz1122/dev/hacka-airplane`. `N` = `research_notes/Conocimiento turístico de Los Nevados`.
Read entries from `data/knowledge/sections/<section>.json`. READ ONLY there. Write only
`N/coordination/style/<section>.json` for your sections.

## Patch format

```json
{"<entry id>": {"short_from": "<exact current answer.short>", "short": "<new short>",
                "examples": {"<exact current example>": "<new example>"}}}
```
Omit `short`/`short_from` when the short is fine; omit `examples` when they are fine; omit entries that need nothing.
The coordinator applies a short only while the current text equals `short_from`, rejects a short that adds or
changes any number (it may drop citation dates), and rejects an example that already exists anywhere.

## What to fix in `answer.short`

1. Source narration: "La norma del 4 de agosto de 2023 nombra…", "Según la ficha Ramsar…", "El plan de manejo dice…".
   Say the fact directly. Keep one short attribution only when the data is disputed, dated or changeable
   (e.g. "(dato de 2024)", "según el IDEAM"). Keep legal citations only when the user needs them (a rule's
   resolution may stay once, briefly).
2. More than 3 sentences or > 320 characters → shorten to 1-3 sentences without losing any fact a tourist needs.
3. Must use "tú", be kind and concrete, and end with the action to take.
4. NEVER add a fact, number, place, species or date that is not already in the current short. Never change a
   figure. If a conflict is presented (two sources), keep both values.

## What to fix in `examples`

Replace (old → new) examples that are not something a tourist would type:
- restating the answer ("1036 especies, 463 generos y 197 familias", "la carta de 2026 también cubre el filo de hielo",
  "deber de permanecer unidos…"), legal/document vocabulary, statements instead of questions or requests;
- asking another entry's topic (e.g. an emergency question inside a flora entry).
New examples: real phone phrasing, Colombian colloquial or plain, some without accents, ~1 in 10 English, varied
(no shared template), one topic, ≥ 3 words or a clear keyword query. "parce"/"porfa" at most once per entry.
Keep each entry's count unchanged (swap 1:1). Check that the new text is not already an example anywhere
(case/accent-insensitive) — the coordinator rejects duplicates.

## Done

Write the style file(s), then run `python3 N/coordination/coordinator_fixes.py` and read
`N/coordination/polish/rejections.json` for your ids: fix every rejection (duplicate → other wording; "short differs
from patch base" → your short_from is stale, re-copy it; numbers changed → you altered a figure). Run
`python3 N/coordination/validate_knowledge.py` (must stay `Errors: 0`). Do not commit.
Final reply in Spanish: per section, shorts rewritten / examples swapped / rejections left (should be 0).
