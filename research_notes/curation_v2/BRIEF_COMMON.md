# Binding rules for every curation v2 agent

Project root `R=/home/cruz1122/dev/hacka-airplane`. Workspace `W=$R/research_notes/curation_v2`.
Today is 2026-11-22. Read `$W/PLAN.md` first.

The product: an offline tourist assistant for PNN Los Nevados. It does **not** generate text. e5
embeds the question, a soft gateway picks up to 5 of 15 sections, Laya picks one of 3–5 candidate
labels or "ninguna", and the stored `answer.short` is shown verbatim with its source. A wrong fact
reaches a tourist unchanged, so a gap is better than padding.

## Never

1. Edit `$R/data/knowledge/sections/`, the registry `coordination/knowledge_additions.json`, or run
   `knowledge.py apply`, `rebuild_all.py`, `regen_test.py`, `coordinator_fixes.py`. Only the
   integrator (agent 6) writes the corpus.
2. Read `$R/data/knowledge/phase2/eval/`, `$R/data/knowledge/laya_ft/eval.jsonl`, or any sealed
   evaluation directory you were not explicitly given. (Eval authors are the exception for their
   own directory.)
3. Invent a source, quote, number, route, permit, schedule, phone number or date. Write evidence
   files by hand. Save evidence only with `tools/fetch_evidence.py`.
4. Claim that the park, a trail, a road or the volcano is open, closed or at a given alert level
   *now*. The app is offline; it only knows dated information.
5. Touch files outside your write boundary, commit, stash, or change git state.
6. Approve your own work. Ask the user questions: decide, log the decision, continue.

## Tools (run from `$R`)

| Command | Use |
|---|---|
| `python3 $W/tools/fetch_evidence.py --section S --name slug URL` | Download a source; cite the printed `.txt` path in `evidence[].path`. Fails on HTTP ≥ 400: log the gap, do not work around it |
| `python3 $W/tools/verify_evidence.py --proposal P [--refetch]` | Must print `"fail": []`. Explain every `flags` item |
| `uv run python .claude/skills/add-park-knowledge/scripts/knowledge.py --root $R inspect --id X` | Exact JSON of an entry and every incoming reference |
| `uv run python .claude/skills/add-park-knowledge/scripts/knowledge.py --root $R stage --proposal P --out P.stage.json` | Validates the proposal against the current corpus; writes only `--out` |
| `uv run --project experiments/laya python $W/tools/route_check.py --proposal P --out P.route.json` | e5 routing of touched and removed examples (serialized; may wait for a lock) |

Pre-existing Phase 2 evidence under `research_notes/Conocimiento turístico de Los Nevados/<S>/evidence/`
may be cited as is (it is hash-pinned in `$W/snapshots/legacy_evidence_manifest.json`).

## Inputs

- Contract `docs/knowledge-contract.md`, schema `docs/schemas/knowledge-section.schema.json`, skill
  `.claude/skills/add-park-knowledge/SKILL.md` (proposal format, op rules).
- Inventory `$W/audit/inventory_before/<S>.csv` (per entry: sources, dates, temporal terms,
  `loo_top1` and `confused_with`) and `confusable_pairs.csv`. `loo_top1` locates confusion; it is
  not a target. Do not add near-duplicate examples to raise it.
- Phase 2 notes `research_notes/Conocimiento turístico de Los Nevados/<S>.research.md`, `<S>/`,
  `coordination/<S>.review.json`, `EVIDENCE_PROTOCOL.md`.

## Report

Your final reply is at most 15 lines: what you wrote (paths), counts, blockers, and the last line of
each required check. Everything else goes in files. Write in Spanish for prose; JSON keys, IDs and
code in English.
