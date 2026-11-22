# Section curator brief (agents 7–21)

Read `BRIEF_COMMON.md` first. You own one section `S`. Write boundary:
`$W/audit/S.csv`, `$W/proposals/S.json` (+ `.stage.json`, `.route.json`, `.verify.json`),
`$W/evidence/S/`, `$W/findings/S.cross.json`, `$W/decisions/S.curator.md`. Nothing else.

## 1. Audit every entry → `$W/audit/S.csv`

Columns: `id, verdict, reasons, source_status, evidence_ref, evidence_excerpt, temporal, confusable_with, notes`.

- `verdict`: `keep`, `modify_meta` (label/examples/hard_negatives/related only), `modify_fact`
  (answer/sources/dates), `merge_into:<id>`, `delete`, `move_to:<section>`, `flag_review`.
- `reasons` (codes, `|`-separated): `ok`, `wrong_fact`, `unsupported`, `stale`, `needs_date`,
  `duplicate`, `overlap`, `wrong_section`, `confusable`, `weak_label`, `low_demand`, `unsafe`.
- `source_status`: `primary_ok`, `secondary_only`, `quote_missing`, `url_dead`, `not_checked`.
  `primary_ok`/`secondary_only` mean you **read** a passage that supports the answer's claims:
  `evidence_ref` = repo-relative path of that evidence file (Phase 2 evidence under
  `research_notes/Conocimiento turístico de Los Nevados/<S>/evidence/` or your fetched `.txt`),
  `evidence_excerpt` = a verbatim passage (≥ 20 chars) from it. `tools/audit_check.py` verifies
  both. If you did not read it, the status is `not_checked`. Honest `not_checked` beats a false
  `primary_ok`; a false one is the worst outcome of this audit.
- `temporal`: `none`, `dated_ok`, `needs_date`, `claims_current_state`.
- An entry you could not check is `flag_review` with `not_checked`, never `keep`.

Order of work: safety and numbers first, then entries with `temporal_terms`, then entries with low
`loo_top1`, then the rest. Every entry gets a row.

## 2. Proposal → `$W/proposals/S.json`

Format: the skill's `{"operations": [...]}`. Only entries whose ID starts with `S.`.

- Prefer metadata ops. For a confusable pair, fix the cause: a label that does not say what is
  different, examples that really ask the other entry's question (remove them, after checking with
  `route_check.py` that the removed phrasing still reaches an entry that answers it), missing
  contrastive examples, missing `hard_negatives` (copied verbatim from the other entry's examples).
- Keep short queries. One- or two-word examples ("baños", "señal", "cuánto vale") are what
  tourists really type; do not remove them for being short. Remove an example only if it asks
  another entry's question or duplicates one.
- New examples: natural Colombian tourist phrasing, typos/no accents, short and long, indirect,
  1–2 English. No template filler, no near-copies of existing examples in any section.
- Factual ops only for a real error, an unsupported claim, or a missing date on changeable data.
  Every URL in `sources` needs an evidence record with a fetched quote that supports the claim.
- New entries (`add`) only for a real, frequent tourist question with primary evidence; at most 6.
  Full schema entry, ≥ 12 examples, `answer.short` 1–3 sentences in tú.
- Deletes and merges: run `inspect` first, give a reason, use `replace_with` for merges, update
  orphaned `hard_negatives` in your own section in the same batch.
- Cross-section problems (an entry belongs elsewhere, a duplicate in another section): write them to
  `$W/findings/S.cross.json` as `[{"ids": [...], "problem": "...", "suggestion": "..."}]`.
- Labels: specific, 3–8 words, distinct from every label in the corpus. Laya compares the question
  against labels only.

## 3. Checks (all required before you report)

1. `knowledge.py stage` → `"status": "staged"`.
2. `verify_evidence.py --proposal $W/proposals/S.json > $W/proposals/S.verify.json` → `"fail": []`.
3. `route_check.py` → `n_removed_not_routing` = 0, or each case explained in the decision log.
4. `python3 $W/tools/audit_check.py --section S` → `"fail": []`.

## 4. Decision log → `$W/decisions/S.curator.md`

One line per op: id, op, why, evidence path. Then: entries not checked, factual gaps, sources that
failed to download, cross-section findings.
