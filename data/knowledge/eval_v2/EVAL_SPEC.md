# Sealed evaluation v2 — authoring spec

This directory is outside the repository on purpose. Section curators never see it. It is copied
into the repo only after the corpus is frozen (wave 4).

## What you may read

- `kb_view_before.jsonl` here: one line per visitor FAQ with `id`, `section`, `label`, `kind`,
  `short`, `detail`, `steps`, dates and source URLs. **No `examples`.**
- `docs/knowledge-contract.md` in the repo (section scopes).
- Do **not** open `data/knowledge/sections/*.json`, `data/knowledge/phase2/eval/`,
  `data/knowledge/laya_ft/`, or `research_notes/` in the repo. Your questions must not echo the
  stored example phrasings; a leak check (exact + cosine ≥ 0.93 against all corpus examples) drops
  rows that do.

## Row format (JSONL, one file per author: `author_A.jsonl`, `author_B.jsonl`)

```json
{"qid": "A-0001", "q": "toca pagar parqueadero en brisas o eso va incluido",
 "family": "A-f001", "scenario": "confusable", "case": "answerable",
 "gold": "booking_fees.vehicle_entry_fee", "acceptable": ["booking_fees.vehicle_entry_fee"],
 "clarify_section": null, "author": "A", "why": "parking fee vs entry fee", "temporal": false}
```

- `family`: one tourist intent. Write 1–3 surface forms per family (same family id). Splits are
  family-disjoint, so forms of one intent never land in both dev and test.
- `case`: `answerable` (gold = the FAQ whose `short` answers it; `acceptable` = every FAQ whose
  answer also fully answers it, gold included), `none` (no FAQ answers it: check by searching the
  view, and say which near FAQ you rejected in `why`), `ambiguous` (needs a clarification question;
  `acceptable` lists the plausible FAQs, `clarify_section` the section whose bank should ask).
- Judge by the answer text, not by the label. If the `short` does not answer it, it is not gold.
- `temporal: true` when the question asks about the current state (open today, alert now, price
  this week). The right behavior is the dated answer plus the official channel; gold may still be
  the FAQ that gives the dated information.
- Spanish as Colombian tourists write it; English only in the `english` scenario. No real personal
  data.

## Scenario mix (fixed)

| Author | scenario | rows |
|---|---|---|
| A | `confusable` (two close FAQs, often across sections: route vs rule vs safety vs logistics) | 120 |
| A | `near_miss` (looks like an FAQ but asks something it does not answer → usually `none`) | 60 |
| A | `out_of_scope` (park-adjacent or unrelated, `none`) | 80 |
| A | `temporal` (current state, dates, prices, alerts) | 60 |
| A | `compound` (two questions in one; gold = the main one, acceptable = both) | 30 |
| B | `natural` (plain, how a tourist asks; the reference slice) | 150 |
| B | `colloquial` (Colombian slang, indirect) | 60 |
| B | `typo` (no accents, misspellings, missing words) | 50 |
| B | `short` (1–3 words) | 40 |
| B | `long` (long, with context or a story) | 40 |
| B | `clarification` (`ambiguous`: under-specified, several FAQs fit) | 30 |
| B | `english` | 20 |

Spread answerable rows over all 15 sections roughly by section size; at least 8 per section.
