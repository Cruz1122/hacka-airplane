# Research and curation (`research_notes/`)

## Purpose

`research_notes/` holds the evidence, briefs, proposals, reviews, and coordinator scripts that produce the knowledge base. Some scripts in `experiments/laya/` and `experiments/nlu/` read these folders directly, for example `leak_check.py` and `build_payload.py`. The end-to-end picture is in [system-map.md](../../system-map.md#1-authoring-knowledge-research-to-sections).

## Start here

- `research_notes/Conocimiento turístico de Los Nevados/` (`NOTES` in `knowledge.py`). Each of the 15 sections has a `<section>.research.md` log and a folder with generator scripts, `check_quotes.py`, and `evidence/`. The binding agent rules are in [EVIDENCE_PROTOCOL.md](<../../../research_notes/Conocimiento turístico de Los Nevados/coordination/EVIDENCE_PROTOCOL.md>).
- `NOTES/coordination/` holds the coordinator scripts. `builders.py` (`BUILDERS`) maps each section to its builder scripts, whose names differ per section. `coordinator_fixes.py` applies the cross-section fixes. `rebuild_all.py` runs both under `coordinator_fixes.lock`. `validate_knowledge.py` and `check_sources.py` are read-only gates. `regen_test.py full|base|scratch` swaps the corpus and restores it afterwards.
- `research_notes/curation_v2/` holds the second curation round. Read [PLAN.md](../../../research_notes/curation_v2/PLAN.md) first. Section files follow `proposals/<S>.json`, `reviews/<S>.review.json`, `decisions/<S>.curator.md`, `findings/<S>.cross.json`, and `audit/<S>.csv`. Gate scripts are in `tools/`.
- `research_notes/depth_v1/` holds the follow-up and variant work. `spec/` contains `requirements.md`, `design.md`, and `tasks.md`. `briefs/` holds the role prompts. `tools/ledger.py` keeps `decisions/dispatch.jsonl`.
- `research_notes/dataset_final/` holds the Laya dataset. This page does not cover it.

## Runtime or data flow

1. A curator downloads a source with `curation_v2/tools/fetch_evidence.py`. The raw bytes land in the gitignored `evidence/*/raw/`, and the tracked `.txt` and `.meta.json` land beside them.
2. The curator writes a proposal and runs `knowledge.py stage --proposal`, `tools/verify_evidence.py`, and `tools/route_check.py`.
3. A reviewer from another model family runs `verify_evidence.py --refetch` and writes `reviews/<S>.review.json`. `tools/review_gate.py` checks the fix round.
4. One integrator runs `knowledge.py stage`, then `check`, then `apply`, then `rebuild_all.py`, `validate_knowledge.py`, and `regen_test.py full`. The logs land in `reports/integration/`.
5. depth_v1 runs `tools/integrate_depth.py` and `tools/integrate_replies.py`. They write `data/knowledge/app/depth_replies.json` and `reply_variants.json`.

Never edit `data/knowledge/sections/*.json` by hand. `rebuild_all.py` regenerates those files from the builders.

## Tests

- `tests/test_add_park_knowledge.py` copies `NOTES/rules/evidence` and covers `knowledge.py`.
- `mobile/src/core/knowledge/__tests__/e2e_sigue.test.ts` runs the fixture that `depth_v1/tools/e2e_sigue.ts` documents.
- No pytest covers the `coordination/`, `curation_v2/tools/`, or `depth_v1/tools/` scripts.

## Common change paths

- To add, update, or delete a topic, use [add-park-knowledge](../../../.agents/skills/add-park-knowledge/SKILL.md).
- To change a section's generated text, edit `NOTES/<S>/source/overlay.py` when the section has one (7 do). Otherwise edit the builder listed in `BUILDERS`. Then run `rebuild_all.py`.

## Related docs

- [knowledge-contract.md](../../knowledge-contract.md)
- [data/knowledge/app/README.md](../../../data/knowledge/app/README.md)
