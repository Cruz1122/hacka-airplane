---
name: add-park-knowledge
description: Research, add, modify, or delete sourced topics in the Los Nevados offline knowledge base, individually or in atomic batches. Use for adding new knowledge, updating answers/examples/labels/references, or retiring/merging obsolete topics while preserving canonical rebuilds.
---

# Manage park knowledge (add, update, delete)

Add, update, or delete visitor topics in the Los Nevados corpus, individually or as one atomic batch.
Use `scripts/knowledge.py` as the local tool. Do not hand-edit generated section JSON files.
Every approved operation is recorded in `coordination/knowledge_additions.json` and replayed last by
`coordinator_fixes.py`, so `rebuild_all.py` and `regen_test.py` preserve additions, updates, and
deletions identically.

## Read the local contract

Resolve the project root containing `docs/knowledge-contract.md` and `data/knowledge/sections`.
Read the contract, `docs/schemas/knowledge-section.schema.json`, and the relevant section before
authoring. Section ownership and lower-order tie-breaking come from the contract. Preserve the 15
sections. Entry IDs are globally unique and **never reused**: to modify an existing topic in place,
use `op: "update"`; to retire or merge one, use `op: "delete"` (optionally with `replace_with`).
To move a topic to a new section/ID, combine `op: "add"` (new ID) and `op: "delete"` (old ID with
`replace_with` pointing to the new ID) in one atomic batch.

## Inspect before modifying or deleting

Before updating or deleting an existing entry, inspect it to fetch its exact JSON, section
`slot_questions`, `featured` status, and every incoming `related` or `hard_negatives` reference:

```bash
uv run python "$TOOL" --root "$PWD" inspect --id rules.pets
```

Check `referenced_by_related` and `referenced_by_hard_negatives` before deleting or removing
examples. If deleting an entry or editing its examples orphans another entry's `hard_negatives`,
update those entries in the same batch (metadata-only updates need no new evidence) so
`validate_knowledge.py` stays at zero review flags.

## Research and author

- Prefer PNN, SGC, IDEAM, Humboldt/SiB and territorial environmental authorities. Read actual pages
  or documents, save UTF-8 source extracts inside the project, and keep URL/date provenance. A search
  snippet, homepage, or synthesized summary is not evidence for a factual claim. Never invent a
  quote or imply that the script independently fetched or authenticated a document.
- Every numerical claim, including written numbers in variants, steps and detail, must be supported
  by a dated official source. State the date/conditional nature of prices, schedules and alerts.
  If evidence is unavailable, log the gap instead of manufacturing a topic. Do not infer current
  openings from old permissions. Reconcile source conflicts explicitly.
- Use a distinct English snake_case ID, a specific 3–8-word Spanish label, at least 12 natural varied
  questions, 1–2 English questions, Colombian phrasing and realistic accentless/error forms. Avoid
  template filler and semantic duplicates. Do not split one intention to increase counts.
- Write `answer.short` in 1–3 friendly sentences addressing tú. Supply 1–2 faithful reformulations
  that differ from `short`; optional `detail` and nested `steps` add sourced depth, not speculation.
  Add 2–4 hard negatives copied from real examples of other entries, and 1–3 useful `related` IDs.
  References may point to another entry in the same batch. Provide questions for all new `needs`.
- The app is offline. Never promise network transmission, location tracking, saved registrations or
  rescue dispatch without implementation evidence. Do not gate immediate emergency guidance behind
  clarification slots. Editorial app behavior needs repository evidence and honest attribution.

## Operation rules and proposal format

The CLI accepts a single operation object, a list of operations, `{"entries": [...]}`, or
`{"operations": [...]}`. Operations may be mixed freely inside one atomic batch (one operation per
target ID per batch):

- **`add`** (default when `"op"` is omitted):
  - Target `entry.id` must not currently exist and must not have been previously deleted.
  - Requires complete schema-compatible `entry` and `evidence` with a local verbatim quote for every
    URL in `entry.sources`. Any digit in `answer` requires a quoted official source and `last_verified`.
- **`update`** (`"op": "update"`):
  - Target `entry.id` must currently exist; replaces the entry in place (preserving order).
  - Must actually change `entry` or `slot_questions`.
  - **Factual/behavioral changes** (`answer`, `sources`, `last_verified`, `valid_until`, `kind`,
    `audience`, `action`): require `evidence` covering every cited URL in `entry.sources` and
    `last_verified` (plus a quoted official source if `answer` contains digits).
  - **Retrieval/metadata-only changes** (`label`, `examples`, `hard_negatives`, `related`, `tags`,
    `entities`, `needs`, `lang`, `slot_questions`): `evidence` is optional (still validated if
    provided). Include a concise `reason` when helpful.
- **`delete`** (`"op": "delete"`):
  - Target `id` must currently exist. Requires `reason` (≥ 10 chars). `evidence` is optional
    (recommended when removing a topic due to an official change; validated if provided).
  - Optional `replace_with` (a surviving entry ID, which may be added in the same batch) redirects
    incoming `related` across all sections and same-section `featured` to that ID.
  - Without `replace_with`, incoming `related` and `featured` drop the deleted ID automatically, and
    the tool fails closed if any surviving entry would drop below 1 `related` or any section below
    3 `featured` (or 1 entry).

Do not place `evidence` or `reason` inside the served `entry`; the section schema forbids it.

```json
{
  "operations": [
    {
      "op": "add",
      "entry": {"id": "geography.example_topic", "...": "complete entry per schema"},
      "slot_questions": {},
      "evidence": [
        {
          "url": "https://www.parquesnacionales.gov.co/actual-source-page",
          "path": "research_notes/new-topic/evidence/source.txt",
          "quote": "An exact passage copied from the source extract, never invented.",
          "checked_on": "YYYY-MM-DD"
        }
      ]
    },
    {
      "op": "update",
      "reason": "Refresh visitor fee after 2026 PNN resolution.",
      "entry": {"id": "booking_fees.example_existing", "...": "complete updated entry"},
      "evidence": [
        {
          "url": "https://www.parquesnacionales.gov.co/actual-source-page",
          "path": "research_notes/update-topic/evidence/source.txt",
          "quote": "An exact passage copied from the source extract, never invented.",
          "checked_on": "YYYY-MM-DD"
        }
      ]
    },
    {
      "op": "delete",
      "id": "rules.obsolete_topic",
      "reason": "Merged into rules.surviving_topic because both covered the same prohibition.",
      "replace_with": "rules.surviving_topic"
    }
  ]
}
```

The example shows shape, not a valid proposal. Use real entries, URLs, quotes and actual dates.
Review whether passages support **all** claims yourself. The script checks literal quote presence,
not truth or entailment.

## Run the tool

From the project root, resolve `TOOL` to this skill's `scripts/knowledge.py`:

```bash
uv run python "$TOOL" --root "$PWD" inspect --id rules.pets
uv run python "$TOOL" --root "$PWD" stage --proposal /tmp/changes.json --out /tmp/changes.stage.json
uv run python "$TOOL" --root "$PWD" check --stage /tmp/changes.stage.json
uv run python "$TOOL" --root "$PWD" apply --stage /tmp/changes.stage.json
(cd "research_notes/Conocimiento turístico de Los Nevados/coordination" && uv run python validate_knowledge.py)
```

The tool prints one JSON result and exits nonzero on failure. Read its actual result—including
`impact` (`related_updated`, `featured_updated`) and `warnings` (`orphaned_hard_negatives`,
`similar_labels`)—before applying or reporting success. After `apply`, run `validate_knowledge.py`:
it must report `Errors: 0` and no review flag introduced by the change; fix and restage otherwise.

`stage` validates the entire candidate corpus without changing it. Check affected IDs, source
support, warnings, and semantic separation once. `check` is optional immediately before `apply`;
`apply` repeats the check itself under the coordinator lock.

`apply` rechecks hashes under `coordinator_fixes.lock`. It refuses changes made since staging,
preserves unrelated entries, appends an audit block to affected `<section>.research.md` logs, and
records the operations in `coordination/knowledge_additions.json`. Identical reapplication of an
already-applied stage is a no-op (`"status": "unchanged"`).

For a conflict, restage against current content after reviewing the difference. Do not bypass the
hash guard or overwrite concurrent work. For batches, validate all records together and apply none
if one fails. Parallel authors produce separate proposal files; only one coordinator applies.

Backups, original bytes and a write manifest live in `coordination/addition_transactions/<id>`.
Each file is replaced atomically, and ordinary write exceptions roll back completed writes. A power
loss can interrupt a multi-file commit. If the receipt lacks `COMPLETED`, compare current hashes with
its before/after manifest before restoring backups; stop if a file has since changed. Do not restore
blindly over concurrent work. No release ZIP, eval label, embeddings or model is modified by this tool.

## Finish at a bounded result

Report added, updated, and deleted IDs, any cleaned/redirected references, sources, actual checks,
and remaining factual gaps. Explicitly separate structural validity from retrieval quality and
factual entailment. For a safety-critical new or modified protocol, use a focused independent source
review before applying; ordinary edits need no panel. Package a ZIP or run semantic/evaluation
suites only when requested or when a concrete new ambiguity requires it.
