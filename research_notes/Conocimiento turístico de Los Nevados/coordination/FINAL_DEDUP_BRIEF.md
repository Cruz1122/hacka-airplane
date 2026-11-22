# Final near-duplicate review — binding brief (no new facts)

Retrieval-only assistant: a tourist question is embedded (e5) and matched against every entry's `examples`;
the winning entry's `answer.short` is shown verbatim. Two examples of DIFFERENT entries that are almost the
same text make the router guess. Working dir `/home/cruz1122/dev/hacka-airplane`,
`N` = `research_notes/Conocimiento turístico de Los Nevados`.

READ ONLY: `data/knowledge/sections/*.json`, `N/coordination/near_duplicates.json` (196 pairs, cosine >= 0.95,
fields `a`/`b` = [entry id, example]), `N/coordination/dedup_proposal.batch1.json` (keys `answer_needs` and
`template_risk` are doubts left from batch 1 — resolve them too), `N/coordination/dedup_decisions.json`
(decisions already applied: do not repeat them).
WRITE ONLY: `N/coordination/dedup_proposal.final.json`.

For each pair read BOTH entries (label, answer.short, all examples) and decide:

- `distinct`: the two questions really ask different things and each fits its own entry. Use sparingly:
  cosine >= 0.95 almost always means one of them must change.
- `swap`: one example is ambiguous or belongs better to the other entry. Replace it (in the entry where it
  fits worse) with a NEW example that clearly asks that entry's own topic (its label/answer), real phone
  phrasing, Spanish (Colombian colloquial or plain, some without accents) or ~1 in 10 English. Must not
  exist anywhere in the corpus (case/accent-insensitive) and must not be a near-copy of another entry's
  example. This keeps the entry's example count.
- `merge`: the two ENTRIES answer the same question. Give keep/drop ids and say which facts of the dropped
  answer are missing from the kept answer (I will patch the kept short). Only when the answers overlap.

Never write a fact, number, place or species. Examples are questions, not answers.

Output format (valid JSON):
```json
{"swaps": [{"entry": "<id>", "old": "<exact current example>", "new": "<new example>", "pair": <index in near_duplicates.json>}],
 "merges": [{"keep": "<id>", "drop": "<id>", "missing_facts": "<text or empty>", "pair": <index>}],
 "distinct": [{"pair": <index>, "why": "<short>"}],
 "batch1_doubts": [{"item": "<what>", "decision": "<swap/merge/distinct + ref>"}]}
```
Every pair index 0..195 must appear exactly once across swaps/merges/distinct (a pair may need 2 swaps:
list both with the same index). Self-check with a short Python script before finishing: all indexes covered,
every `old` is literally in that entry's examples, every `new` is unique corpus-wide and among your swaps.
Do not edit any other file. Do not commit. Final reply in Spanish: counts per decision, and the 5 hardest calls.
