# Section reviewer brief (agents 25–29, and the critical lead as second reviewer)

Read `BRIEF_COMMON.md` first. You review proposals written by **another** agent (a section
curator on another model). You approve nothing you wrote. You change no proposal and no corpus
file. Write boundary: `$W/reviews/S.review.json` and `$W/reviews/S.refetch.json` for your sections.
Do not ask questions or ask for confirmation.

## Inputs per section S

`$W/proposals/S.json` (+ `.verify.json`, `.route.json`), `$W/audit/S.csv`,
`$W/decisions/S.curator.md`, the before snapshot `$W/snapshots/sections_before/S.json`, the
evidence files the proposal and audit cite, and the findings that concern S:
`$W/findings/{labels,taxonomy,critical,contradictions,arbiter}.json` (when present) and
`$W/audit/inventory_before/S.csv` (`loo_top1`, `confused_with`).

## Checks

1. **Independent refetch.** Run
   `python3 $W/tools/verify_evidence.py --proposal $W/proposals/S.json --refetch > $W/reviews/S.refetch.json`.
   Any `fail` → reject the op. A `warn` (quote not found in a fresh download) blocks the op until
   you open the fresh page and confirm the passage is there in substance; record what you saw.
2. **Entailment, every factual op.** Read each quote and the new `answer` (short, variants, steps,
   detail). Every claim and every number must be supported by a quoted passage. `full`, `partial`
   (name the unsupported claim) or `none`. Partial or none → `revise` with the exact claim to drop
   or source.
3. **Audit rows, every row.** For each row with `primary_ok`/`secondary_only`, open
   `evidence_ref` and judge whether `evidence_excerpt` supports the entry's answer: `full`,
   `partial`, `none`. A passage that only mentions the topic ("El municipio de Armero" for a claim
   about 1595 lahars) is `none`. Count them; this is the honesty metric of the curator.
4. **Temporal policy** (PLAN.md and `$W/audit/temporal_policy.md` when present): changeable data
   dated, no claim of current state, official channel named. Emergency guidance never behind a
   clarification. Nothing promises transmission, tracking or rescue.
5. **Labels.** A label change is justified only if it fixes a documented confusion
   (`confused_with`, `findings/labels.json`, `findings/taxonomy.json`) or a label that misstates the
   answer. Stylistic rewording or added filler words → `revise` (keep the old label). Laya was
   trained on the current labels, so label churn has a cost.
6. **Examples.** Removed examples: `route.json` `removed_not_routing` must be empty or explained.
   Short real queries must not be removed. New examples: natural, varied, not near-copies, not
   asking another entry's question, no template filler.
7. **Deletes/merges.** Reason, references checked (`knowledge.py inspect`), `replace_with` for
   merges. Never accept a delete justified by textual similarity alone.

## Output `$W/reviews/S.review.json`

```json
{"section": "S", "reviewer": "agent NN / model",
 "ops": [{"id": "...", "op": "update", "verdict": "approve|revise|reject",
          "entailment": "full|partial|none|n/a", "label_change": "justified|stylistic|n/a",
          "examples": "ok|issues", "temporal": "ok|issue|n/a", "refetch": "ok|warn|fail|n/a",
          "reason": "...", "required_change": "..."}],
 "audit_rows": [{"id": "...", "claimed": "primary_ok", "support": "full|partial|none", "note": "..."}],
 "summary": {"approve": 0, "revise": 0, "reject": 0, "audit_support": {"full": 0, "partial": 0, "none": 0}}}
```

Every op and every audit row gets a record. Final reply: at most 10 lines in Spanish with the
summary counts per section and the worst problems.
