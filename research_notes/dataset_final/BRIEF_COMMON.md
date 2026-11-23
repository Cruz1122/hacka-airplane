# Final dataset phase — common brief (read fully, it is short)

Project root `R=/home/cruz1122/dev/hacka-airplane`. Work dir `W=$R/research_notes/dataset_final`.

Product: an offline tourist assistant for PNN Los Nevados (Colombia). A visitor question is embedded
with `multilingual-e5-base`; a gateway picks up to 5 of 15 sections; 3–5 candidate FAQs reach a
small classifier (Laya) that picks one FAQ **by its topic label** or "ninguna de estas opciones".
The app then shows that FAQ's prewritten, sourced answer, or asks a clarification (up to 3 options),
or abstains. **Nothing is generated at inference.** Answer quality = the curated FAQ text.

## Hard rules

1. Write only inside your write boundary (given in your task). Never edit
   `$R/data/knowledge/sections/` or any file under `$R/research_notes/curation_v2/`, never run
   `knowledge.py apply`, never commit, never touch `$R/mobile/`.
2. Read only the files your task names. Use `jq` / `python3 -c` to pull fields from big files
   instead of reading them whole. Do not open `$R/data/knowledge/eval_v2/`, `laya_ft*/` or
   `phase2/eval/` (sealed evaluation material) unless your task names them.
3. Never invent facts, quotes, URLs or FAQ IDs. Every FAQ ID you write must exist in
   `$W/inputs/kb_catalog.jsonl` (check by script before you finish).
4. The app is offline: it cannot call rescue, send data, track location or register a visit with
   the park. Never write or approve text implying it does.
5. Spanish as Colombian tourists write it; code, file names and JSON keys in English.
6. Write your output file early (skeleton first) and fill it section by section, so partial work
   survives. Final reply: at most 10 lines, Spanish, counts + worst problems + output paths.

## Files

- `$W/inputs/kb_catalog.jsonl` — 806 FAQs: `id`, `section`, `label`, `short` (no examples).
- `$W/inputs/kb_catalog_trim.jsonl` — same, `short` cut to 150 chars (smaller).
- `$W/inputs/kb_view.jsonl` — full view: + `detail`, `steps`, dates, sources, reviewer `support`
  (`full|partial|none|n/a`) and `support_note`. 695 KB: read it with `jq` filters, not whole.
- Section scopes: `$R/docs/knowledge-contract.md`.
