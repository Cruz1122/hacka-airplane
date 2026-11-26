# UTON guion entries: authoring rules

The UT Operación Nevados guion (2024) is the source the app marks as verified. Entries taken
whole from it carry `"verified_by_uton": true` and cite only the guion. Every other entry is
unverified. The app's "Solo información verificada" setting answers only from verified entries.

## Sources in this folder

| File | What it is |
|---|---|
| `guion_ecoturistico_uton_2024.txt` | `pdftotext` of "Guion Ecoturístico UTON 2024" (57 pages, Manizales, 9 Sep 2024) |
| `guion_turistico_zona_norte.txt` | `pdftotext` of "Guión turístico (zona norte)" (7 pages, UTON summary for guides) |
| `proposals/` | `add-park-knowledge` proposal files and their natural replies |

Line ranges of the long extract: stations 79–450 (Aguacerales 79, Arenales 178, Lunares 275,
Valle de las Tumbas 352), glossary 451–525, geology 526–1196, glaciology 1197–1397,
anthropology 1398–1598, biology 1599–1796, climate 1797–1876, physiopathology 1877–2420.

## Entry rules

Follow `.agents/skills/add-park-knowledge/SKILL.md`, plus:

1. Operation `add` only, ids `<section>.uton_<topic>`. Never update an existing entry: its depth
   and paraphrase rows are not guion text and would show under the verified seal.
2. `verified_by_uton: true`. `sources` is exactly one item:
   `{"label": "Guion ecoturístico Zona Norte, UT Operación Nevados (2024)", "document": "research_notes/uton_guion_2024/guion_ecoturistico_uton_2024.txt", "retrieved_at": "2026-11-26"}`
   (or the short guide: label `Guión turístico zona norte, UT Operación Nevados (2024)`,
   document `research_notes/uton_guion_2024/guion_turistico_zona_norte.txt`). Both may be cited.
   `last_verified: "2026-11-26"`.
3. Evidence: one `{"document", "path", "quote", "checked_on"}` item per fact you state, with
   `document` equal to `path`. Copy quotes verbatim from the extract. Matching ignores line breaks
   and spacing, nothing else. Every number in the answer needs a quote that contains it.
4. Say only what the guion says. Paraphrase in friendly Spanish addressed with tú, no long dashes.
5. The guion contradicts itself in places. Do not pick silently: omit the number or attribute it
   ("según el guion"). Known cases: 1985 deaths (23.000 in the stations, 25.000 in the geology
   chapter), park area (62.142 ha vs the table's 62.271,7), Kumanday meanings, La Olleta
   "107,3 ± 6,2 Ma" (a typo for ka), the garbled 2015–2021 dome figures. List any others you hit.
6. Date time-bound claims: the yellow alert level ("en 2024, según el guion"), the 2022 glacier
   area.
7. Natural reply: one row per entry in `proposals/<shard>.natural.json`
   (`{"<id>": "<text>"}`): the chat's reply, the facts of `answer.short` rewritten naturally,
   no title, no added facts, same numbers.
