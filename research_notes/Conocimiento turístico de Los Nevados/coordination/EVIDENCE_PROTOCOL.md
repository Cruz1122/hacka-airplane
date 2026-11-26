# Evidence and delivery protocol (binding for every research agent)

Context: 100% offline tourist assistant for Parque Nacional Natural Los Nevados (Colombia). Today is 2026-11-21. Runtime has no free generation: an embedder matches the tourist question against `examples`, a decider picks one entry, and the curated `answer.short` plus its source is shown verbatim. A wrong fact reaches a tourist, so evidence comes first and padding is worse than a gap.

Working dir: `/home/cruz1122/dev/hacka-airplane`. `N` = `research_notes/Conocimiento turístico de Los Nevados`. `S` = your section id.

## Read first
- `docs/knowledge-contract.md`, `docs/schemas/knowledge-section.schema.json` (mandatory format).
- `data/knowledge/sections/S.json`, the generator(s) under `N/S/`, `N/S.research.md`, `N/coordination/S.review.json` and `.final-review.json` if present, `N/S/correction-receipt.md` if present.
- Finished reference: `data/knowledge/sections/weather_volcano.json`, `N/weather_volcano/generate_weather_volcano.py`, `N/weather_volcano/evidence/`.
- Real raw pages already downloaded that you may reuse: `N/services/evidence/pnn_nevados.html` + `.txt` (PNN Los Nevados official page, modified 2026-10-31: hours, closures, fees 2026, reservations), `N/activities/evidence/resolucion-207-2023.txt` (Res. 207 de 2023, park regulation), `N/rules/evidence/pnn.html`.

## Evidence (mandatory)
1. Every source is a specific deep URL (page/PDF/dataset), never a homepage like `https://www.humboldt.org.co/`.
2. Fetch it for real (curl/wget/fetch). Save the raw download under `N/S/evidence/raw/` (PDF: also save `pdftotext` output next to it).
3. `N/S/evidence/quotes.md`: for each claim, URL, access date, raw file name, and the VERBATIM sentence copied from the raw file.
4. `N/S/check_quotes.py`: verifies every quote in `quotes.md` appears in its raw file (whitespace-normalized). It must pass. The coordinator reruns it and greps every number/legal citation of your answers in your raw files; entries that fail are removed.
5. No quote → no claim. No official figure → answer without it and log the gap. Conflicts → most official and recent source, log it. Changeable data (prices, closures, alerts) → say it may change and point to the official channel.

## Entries
- One entry = one question a real tourist asks. `label` 3-8 words, specific, distinct from every label in all sections.
- `examples` >= 12: short query, full question, Colombian colloquial vocabulary ("toca llevar guía?", "cuánto vale la entrada", "qué vía cojo"), no accents/typos ("cuanto bale"), 1-2 in English. No near-copies. "parce"/"porfa" in at most 1 example per entry. No example identical (case/accent-insensitive) to any example in any `data/knowledge/sections/*.json` (check with a script).
- `hard_negatives` 2-4, each an existing example of another entry (contract rule).
- `answer.short` 1-3 sentences (<= ~320 chars), "tú", kind, concrete, ending with the action to take; answer directly, do not narrate the source ("la página dice…"); one short attribution only when the data is changeable or disputed. `variants` 1-2.
- `kind`, `audience`, `entities`, `needs` per contract; each `needs` key has a `clarification.slot_questions` entry. `id` = `S.<snake_case>`, new and globally unique. `related` 1-3 existing ids. `last_verified: "2026-11-21"` on entries with numbers.
- Section: keep `retrieval.profile`; `clarification` 4-8 questions, `between_entries`, `slot_questions`, friendly `fallback`; `featured` 3-5 ids.

## Write boundaries
Write ONLY `data/knowledge/sections/S.json`, `N/S.research.md` (add a dated section; keep older content), and files under `N/S/`. The canonical builder of each section is listed in `N/coordination/builders.py`; snapshot sections change only through `N/S/source/overlay.py` (see `ROUND2_BRIEF.md`). Never edit the JSON in place. Other agents work in parallel on other sections. Do not commit.

## Done when
1. Generator → `python3 "N/coordination/coordinator_fixes.py"` → `python3 "N/coordination/validate_knowledge.py"` prints `Errors: 0`; global example uniqueness: 0 duplicates.
2. `python3 "N/S/check_quotes.py"` passes.
3. Final reply in Spanish, short: entries/examples before→after, new/removed ids, raw files fetched, top gaps, last line of the validator and of check_quotes.
