# Integrator brief (agent 6, wave 4–5)

Read `BRIEF_COMMON.md` and `PLAN.md` first. You are the **only writer** of the corpus. Nobody else
applies. No curator or reviewer runs while you work (the orchestrator guarantees it; `regen_test.py`
must never run beside other agents).

Root `R=/home/cruz1122/dev/hacka-airplane`, `W=$R/research_notes/curation_v2`,
`C="$R/research_notes/Conocimiento turístico de Los Nevados/coordination"`,
`K=$R/.claude/skills/add-park-knowledge/scripts/knowledge.py`.

## Inputs

`$W/proposals/<S>.final.json` for each section (built by `tools/review_gate.py --final`: ops approved
in round 1 plus ops approved in re-review). Apply nothing else. A section without a final file is
skipped and reported.

## Steps

1. Record `git status --porcelain` and `sha256sum data/knowledge/sections/*.json` to
   `$W/reports/integration/pre.txt`. They must match `$W/snapshots/sections_before.sha256.json`;
   stop if not.
2. Combined dry run: concatenate every final file into one proposal and `stage` it to a scratch file.
   Any error → stop and report the op. Record warnings.
3. Canary apply: apply the smallest section first (`stage` → `check` → `apply`), then run
   `(cd "$C" && python3 rebuild_all.py)` and `validate_knowledge.py`, and confirm with a script that
   every applied op is present in `data/knowledge/sections` after the rebuild (registry replay
   works). Stop on any loss.
4. Apply the remaining sections one at a time in contract order (actions … conversation): `stage`
   against the current corpus right before each `apply` (hashes change after every apply), then
   `apply`. Read the JSON result each time; a refusal means restage, never bypass.
5. Final: `rebuild_all.py`; `validate_knowledge.py` must print `Errors: 0; review flags: 0`;
   `regen_test.py full` must report OK for all 15 sections; `cd $R/experiments/laya && uv run python kb.py validate $R/data/knowledge/sections` (if it takes a directory); `python3 $W/tools/taxonomy_audit.py` on the after corpus;
   `uv run --project experiments/laya python $W/tools/inventory.py --sections data/knowledge/sections --out $W/audit/inventory_after`.
6. Write `$W/snapshots/sections_after.sha256.json` and `$W/reports/integration.md`: ops applied per
   section and type, skipped sections, every check's last line, warnings, and the transaction IDs.

Write boundary: the corpus via `knowledge.py apply` only, `$W/reports/integration*`,
`$W/snapshots/sections_after*`, `$W/audit/inventory_after/`, and scratch files in your temp dir.
Final reply: at most 12 lines in Spanish with the last line of each check.
