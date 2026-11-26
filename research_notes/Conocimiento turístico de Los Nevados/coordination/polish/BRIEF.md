Respond to me in Spanish. You are a WORDING POLISHER for knowledge section(s) named in your task message of a 100% offline tourist assistant for Parque Nacional Natural Los Nevados (Colombia). Today is 2026-11-21. Runtime: an embedder matches the tourist's question against each entry's `examples`; the curated `answer.short` is shown verbatim on a phone. You do NOT research and you do NOT add facts.

Working dir: /home/cruz1122/dev/hacka-airplane. N = `research_notes/Conocimiento turístico de Los Nevados`.

## Read
- `docs/knowledge-contract.md` (format), the section file(s) `data/knowledge/sections/<section>.json`.
- `N/coordination/coordinator_fixes.py`, function `apply_polish` (how your patch is applied and what gets rejected).

## What to improve (only these)
1. `answer.short` that is long (more than 3 sentences or ~320 characters) → rewrite to 1-3 short sentences, "tú", kind, concrete, ending with the action the tourist should take. Move removed detail nowhere (it already lives in `detail`/`steps`).
2. Answers that talk about the source instead of answering ("esa página no dice…", "según la ficha…", "la Gobernación ubica…", "no publica…") → answer the tourist directly. Keep at most one short attribution when the fact is changeable or disputed (e.g. "según Parques Nacionales"), and keep any "confirma con…" instruction.
3. `variants`: 1-2 real rephrasings of the NEW short.
4. `examples`: replace artificial or near-copy examples (only accent/order changes, keyword salads like "4.000 metros según la Gobernación", encyclopedic phrasing no tourist would type). Each entry should end with a mix: short query, full question, Colombian colloquial ("toca", "qué vía cojo", "cuánto vale", "pa' llegar", "harto frío"), no accents/typos ("cuanto bale", "q hora abren"), 1-2 in English. Replace at most 4 examples per entry.
   Colloquial means Colombian vocabulary and syntax ("qué vía cojo", "cuánto vale", "toca madrugar?", "eso queda lejos?"), NOT appending a tag. Use "parce", "porfa", "o qué", "cierto" in at most 1 example per entry and in at most 1 of every 5 new examples overall.

## Hard constraints
- Never add, remove or change a fact. Every number in the old short must appear identically in the new short (same digits and separators, e.g. "4.100", "8:00"); do not add numbers. Variants may only use numbers present in the new short. Patches that break this are auto-rejected.
- Never change meaning, safety warnings, prohibitions or "confirm with the official source" instructions.
- New examples must be unique across ALL files in `data/knowledge/sections/` (case/accent-insensitive). Check with a script before writing.
- Do NOT edit `data/knowledge/sections/*.json` or any generator. Write ONLY your patch file(s): `N/coordination/polish/<section>.json` with format
  {"<entry id>": {"short": "...", "variants": ["..."], "examples": {"<exact old example>": "<new example>"}}}
  Include only entries you change; omit fields you do not change.

## Apply and verify
1. Run `python3 "N/coordination/coordinator_fixes.py"` (applies all patches; idempotent).
2. Read `N/coordination/polish/rejections.json`; fix your rejected items and rerun until none of your ids appear there.
3. Run `python3 "N/coordination/validate_knowledge.py"`; last line must say `Errors: 0`.

## Final reply (short)
Per section: entries patched, shorts shortened, meta-talk removed, examples replaced, rejections left (should be 0), validator last line, and 3 before→after examples of shorts.
