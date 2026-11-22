# Round 2 brief (Phase 2 completion) — binding together with EVIDENCE_PROTOCOL.md

Today is 2026-11-21. Phase 2 target (docs/plan-knowledge-system.md): about 900 entries and at least 9,000
examples over 15 sections, every fact from a read source. v1 has 564 entries / 7,053 examples.
Padding is worse than a gap: stop when official sources run out and log the gap.

`N` = `research_notes/Conocimiento turístico de Los Nevados`, `S` = your section id.

## How your section is built (changed in round 2)

`N/coordination/builders.py` names the canonical builder of every section.

- Generator sections (health_safety, weather_volcano, booking_fees, preparation, rules, fauna,
  flora_ecosystems, history_culture): edit the generator or its entry modules under `N/S/`, run it.
- Snapshot sections (actions, access, hours_status, activities, services, geography, conversation):
  `N/S/source/S.v1.json` is frozen. Write every change in `N/S/source/overlay.py`, which defines
  `apply(section: dict) -> dict` and is run by `python3 N/coordination/build_from_snapshot.py S` on a
  fresh copy of the snapshot. Upsert/remove entries by id; keep it deterministic. The old generators
  in those folders refuse to run on purpose; do not re-enable them.

After building always run `python3 N/coordination/coordinator_fixes.py` (it applies cross-section
moves, wording patches and merges; it is lock-serialized, safe with other agents) and then
`python3 N/coordination/validate_knowledge.py`. Never edit `data/knowledge/sections/*.json` directly and
never run `N/coordination/regen_test.py`.

## Your two jobs, in this order

1. **Audit what exists.** For every current entry whose answer has a fact (number, name, date, rule,
   place), make sure a verbatim quote from a raw downloaded file supports it, recorded in
   `N/S/evidence/quotes.md` and passing `N/S/check_quotes.py` (create both if missing; follow the format
   of `N/rules/check_quotes.py` and `N/rules/evidence/quotes.md`). Reuse raw files already in `N/*/evidence/`
   when they contain the text. An entry you cannot support: rewrite it to what the source says, or remove
   it and list it in your research log. Generic advice without figures (for example "drink water")
   still needs a source if it is a safety instruction.
2. **Expand toward the target** with new entries backed the same way. Topic boundaries below. Before
   adding, search every `data/knowledge/sections/*.json` (labels and examples) for the same topic; if
   another section already covers it, do not add it (link it in `related` instead).

## Topic boundaries (who owns what)

| Section | Owns | Does not own |
|---|---|---|
| access | roads, origin cities, gates, transport, parking, distances | fees, hours |
| booking_fees | fees by visitor type, payment, booking channels, requirements, insurance, guides, groups | hours |
| hours_status | opening hours, closures, how to check status, pico y placa | fees |
| activities | trails, viewpoints, camping, photography, birding, what each sector offers | rules |
| preparation | clothing, gear, food/water, fitness, children, what to bring | medical symptoms |
| weather_volcano | weather by season, volcanic alert levels, ash, what alerts mean for a visitor | history of eruptions |
| health_safety | altitude sickness, hypothermia, sun, emergency numbers, lost, wildlife encounters (safety side) | gear lists |
| rules | pets, drones, fire, trash, off-trail, collecting, noise, sanctions, hunting/feeding wildlife | species facts |
| fauna | species by group, where/when to see them, protected status, behaviour | prohibitions (rules), encounter safety (health_safety) |
| flora_ecosystems | páramo, superpáramo, frailejones, wetlands, glaciers, water cycle, conservation | peaks/heights |
| geography | peaks, lakes, heights, departments, sectors, park vs volcano | glacier retreat (flora_ecosystems) |
| history_culture | Armero 1985, lahars, Indigenous names, park creation, communities, legends | current alert level |
| services | visitor centres, toilets, food, signal, first aid, accessibility, lodging | fees |
| conversation | greetings, thanks, goodbyes, what the app can do, language switch | park facts |
| actions | register a visit, report an emergency (FSM hand-off) | anything else |

## Rules that the validator will not catch

- `hard_negatives`: copy exact existing examples of other entries (any section). Do not invent them.
  Your section must not add new `hard_negative_review` flags in the validator output.
- Examples ≥ 12 per entry, varied (short, full, colloquial, no accents, 1-2 English), no near-copies,
  "parce"/"porfa" in at most 1 example per entry. Do not write examples that ask about another entry's topic.
- `answer.short` 1-3 sentences, ≤ ~320 chars, "tú", ends with the action. Changeable data says it can
  change and names the official channel. Conflicting sources: give both with their source, log it.
- `last_verified: "2026-11-21"` on every entry with a digit in the answer.

## Done when

1. Builder → coordinator_fixes → validator: `Errors: 0`.
2. `python3 N/S/check_quotes.py` passes and covers every entry with a fact.
3. You appended a dated "Round 2" section to `N/S.research.md`: entries before→after, removed or rewritten
   ids with reason, raw files fetched (URL + file), gaps where no official source exists.
4. Final reply in Spanish, short: counts before→after, check_quotes last line, validator last line, top gaps.
