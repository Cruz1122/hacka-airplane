# Eval leakage fix — binding brief (no new facts)

The eval set `data/knowledge/phase2/eval/paraphrase.*.jsonl` must test UNSEEN phrasings. `N/coordination/eval_leakage.json`
lists 123 eval questions (`q`, `file`, `expected`) that are almost identical (cosine >= 0.95) to a training
example (`example`, `example_owner`). Working dir `/home/cruz1122/dev/hacka-airplane`,
`N` = `research_notes/Conocimiento turístico de Los Nevados`.

READ ONLY: `data/knowledge/sections/*.json`, the eval files, `N/coordination/eval_leakage.json`.
WRITE ONLY: `N/coordination/leakage_proposal.json`. Never edit the eval files (they were written by other
models on purpose) or the sections.

Fix the TRAINING side: for each row, replace the training `example` in entry `example_owner` with a new example
that asks the same thing as that entry but is clearly different wording from the eval question (different
words/structure, not only accents or one synonym). Real phone phrasing, Spanish (Colombian colloquial or plain,
some without accents), ~1 in 10 English if the old one was English keep English. Must not already exist anywhere
in the corpus (case/accent-insensitive), must not be another entry's topic, no facts or numbers that are not
in that entry's answer, "parce"/"porfa" only if the entry has none yet.

Special case: when `example_owner` is NOT in `expected` (6 rows) the eval question may be legitimately answered
by both entries. Decide: `add_expected` (both answers are correct for that question; I will add the owner to
`expected`) or `swap` as above (the training example is the ambiguous one). Explain in `why`.

Output (valid JSON):
```json
{"swaps": [{"entry": "<example_owner>", "old": "<exact example>", "new": "<new example>", "row": <index in eval_leakage.json>}],
 "add_expected": [{"row": <index>, "file": "<eval file>", "q": "<eval question>", "add": "<entry id>", "why": "<short>"}]}
```
Every row index 0..122 must appear exactly once. Self-check with Python before finishing: every `old` is literally
in that entry's examples, every `new` is unique corpus-wide and among your swaps, and no `new` matches any
eval question (casefolded, accents stripped). Do not commit. Final reply in Spanish: counts and 3 examples.
