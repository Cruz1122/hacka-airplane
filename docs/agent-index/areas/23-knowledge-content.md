# Knowledge content

## Purpose

Find where a park topic is authored, validated, and turned into the JSON the phone bundles. [system-map.md](../../system-map.md) flows 1 to 3 give the full detail.

## Start here

- [knowledge-contract.md](../../knowledge-contract.md) and [knowledge-section.schema.json](../../schemas/knowledge-section.schema.json) define a section and an entry.
- `data/knowledge/sections/*.json` holds 15 sections with 806 entries, counted at this commit. Never hand-edit them, because `rebuild_all.py` regenerates them.
- `data/knowledge/app/` holds the app layer, keyed by entry id. See [its README](../../../data/knowledge/app/README.md).
- [add-park-knowledge SKILL.md](../../../.agents/skills/add-park-knowledge/SKILL.md) and its `scripts/knowledge.py` (`inspect`, `stage`, `check`, `apply`). `.claude/skills/add-park-knowledge` is a symlink to `.agents/skills/add-park-knowledge`.
- `research_notes/Conocimiento turístico de Los Nevados/coordination/` holds `builders.py` (`BUILDERS`), `coordinator_fixes.py`, `rebuild_all.py`, `regen_test.py`, and `validate_knowledge.py`.

## Runtime or data flow

1. `knowledge.py apply` writes `sections/` and appends the operation to `coordination/knowledge_additions.json`.
2. `rebuild_all.py` runs every builder under `coordinator_fixes.lock`, then `coordinator_fixes.main()`. That function replays `knowledge_additions.json` last through `knowledge.py`'s `replay()`.
3. `experiments/nlu/export_nlu.py` reads `sections/` and `app/`. It exits with `no natural reply for ...` when an entry lacks a `natural_replies.json` row.
4. The export writes `mobile/assets/data/knowledge/{catalog,sections,policy,index,depth}.json`, the Jest fixtures in `mobile/src/core/knowledge/__fixtures__/`, and `models/knowledge/{index.f32.bin,index_scorer.onnx}`.
5. `mobile/src/llm/knowledgeAssets.ts` imports the bundled JSON. `mobile/scripts/push-knowledge.sh` side-loads the files that `index.json` names.

`media.json` comes from `experiments/media/build_media.py` instead.

## Tests

- `tests/test_add_park_knowledge.py` covers stage, apply, update, delete, and replay against rebuilds.
- `validate_knowledge.py` must print `Errors: 0`. `experiments/laya/kb.py validate` runs the schema and contract rules.
- Jest suites in `mobile/src/core/knowledge/__tests__/` read the exported fixtures and assets.

## Common change paths

- Add or edit a topic. Follow the skill, then add `app/` rows, rerun the export ([architecture.md](../../architecture.md), "Regenerating the assets"), and run `npm test` in `mobile/`.
- Eval data. `data/knowledge/eval_v2/` is sealed. `MANIFEST.json` records its inputs with hashes. See [EVAL_SPEC.md](../../../data/knowledge/eval_v2/EVAL_SPEC.md).

## Related docs

The docs linked above include implementation notes and remaining gaps:

- The app README calls `answer_policy.json` legacy. `export_nlu.py` still reads it for `emergency_direct` ids.
- `validate_knowledge.py` reads the schema copy in `research_notes/.../inputs/`. The copy matches `docs/schemas/` today, but no code keeps the two in sync.
- `phase1/`, `phase2/`, `raw/`, and `laya_ft*/` are read by `experiments/laya`, the coordination tools, and `research_notes/dataset_final/tools/build_dataset.py`, not by the export. This page does not trace them.
