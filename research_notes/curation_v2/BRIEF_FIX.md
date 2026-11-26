# Fix round brief (wave 4, section curators)

Read `BRIEF_COMMON.md` and `BRIEF_CURATOR.md` first; their rules still bind. You own section `S`.
Write boundary: `$W/proposals/S.v2.json` (+ `.v2.stage.json`, `.v2.route.json`, `.v2.verify.json`),
`$W/audit/S.csv`, `$W/evidence/S/`, `$W/decisions/S.fix.md`. Nothing else.

## Inputs

- Your round-1 proposal `$W/proposals/S.json` and its independent review `$W/reviews/S.review.json`
  (+ `S.refetch.json`). The reviewer's `required_change` is the instruction.
- Findings addressed to S (filter by ID prefix `S.` or `owner_section`):
  `$W/findings/labels.json`, `taxonomy.json`, `critical.json`, `contradictions.json`,
  `arbiter.json`, `<other>.cross.json` that name S, and `$W/reviews/_examples.json` (`drop` list).
- `$W/audit/temporal_policy.md` (dated phrasing for changeable data).

## Write `$W/proposals/S.v2.json`: the complete proposal for S

1. Ops the review **approved**: copy them byte for byte. `review_gate.py` fails if they change.
2. Ops marked **revise**: apply the `required_change`, or drop the op. Leaving it unchanged fails.
   When the change is "keep the old label", restore the label from
   `$W/snapshots/sections_before/S.json`.
3. Ops marked **reject**: drop them, unless new fetched evidence fixes the stated problem.
4. Findings: implement each one that is correct, or decline it with a reason in the log. Critical
   and contradiction findings for S are mandatory to resolve, either by a sourced fix or by removing
   the unsupported claim. Taxonomy merges are `delete` + `replace_with` on the entry of your section
   that does not survive (the survivor may be in another section); moves are an `add` in the target
   section's owner's file, so for a move you write only a finding note in your log.
5. Examples flagged in `_examples.json` `drop`: remove them (check `route_check` again).

## Audit CSV

Update `$W/audit/S.csv`. Where the reviewer judged `support` `partial` or `none`, either cite a
passage that really supports the answer (and fix the answer if no passage exists), or lower
`source_status` to `quote_missing` / `not_checked`. `primary_ok` with support `none` must not remain.

## Checks (all required)

1. `knowledge.py stage --proposal $W/proposals/S.v2.json --out $W/proposals/S.v2.stage.json` → staged.
2. `verify_evidence.py --proposal $W/proposals/S.v2.json --refetch` → `"fail": []`; explain warns.
3. `route_check.py --proposal $W/proposals/S.v2.json --out $W/proposals/S.v2.route.json`.
4. `audit_check.py --section S` → `"fail": []`.
5. `python3 $W/tools/review_gate.py --section S` → `"fail": []` (writes the re-review queue).

## Log `$W/decisions/S.fix.md`

One line per review item and per finding: `done` / `dropped` / `declined: <reason>`.
Final reply: at most 10 lines in Spanish with the last line of each check.
