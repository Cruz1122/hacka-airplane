# Eval replacement questions — binding brief

An offline tourist assistant for PNN Los Nevados matches a tourist question to one entry. The eval set must
contain questions written WITHOUT seeing the training examples. 122 existing eval questions turned out to be
almost identical to a training example, so each needs ONE new replacement question.

Working dir `/home/cruz1122/dev/hacka-airplane`, `N` = `research_notes/Conocimiento turístico de Los Nevados`.
READ ONLY `N/coordination/eval_replacement_tasks.json`: per row `row`, `file`, `expected`, `label`, `answer`,
`too_close_question`. Do NOT open `data/knowledge/sections/*.json`, any `examples` list, or any other file of the
corpus: you must not see the training examples. WRITE ONLY `N/coordination/eval_replacements.json`.

For each row write `q`: a question a real tourist would type on a phone, whose correct answer is that entry's
`answer`. Rules:
- Different wording AND structure from `too_close_question` (not only accents, one synonym or word order).
  Change the angle: a concrete situation ("voy con mi mamá de 70…"), a different verb, a shorter keyword query,
  or a longer context-rich question. One topic per question.
- Same language as `too_close_question` (Spanish rows: Colombian colloquial or plain, some without accents;
  English rows stay English).
- No facts or numbers that are not in `answer`; do not copy phrases from `answer`.
- Do not mention another entry's topic so the expected id stays the only right answer.
- All 122 `q` distinct from each other.

Output: a JSON list `[{"row": <int>, "file": "<file>", "expected": [...], "q": "<question>"}]`, every row 0..121
exactly once (copy `file` and `expected` unchanged). Self-check with a short Python script: valid JSON, every row
once, no `q` equal (casefold, accents stripped) to its `too_close_question` or to another `q`.
Do not edit any other file. Do not commit. Final reply in Spanish: count and 5 sample rows.
