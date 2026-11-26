# Developer docs and agent skills

## Purpose

This page maps the human docs, the agent instructions, and the repo skills. It says which docs describe the code today and which are a record. Verified against the files on 2026-11-25.

## Start here

- [`docs/README.md`](../../README.md) is the docs index. Its "History" table marks every file in `docs/history/` as superseded.
- Current docs: [`retrieval-architecture.md`](../../retrieval-architecture.md), [`architecture.md`](../../architecture.md), and [`system-map.md`](../../system-map.md). The first and last state "Verified against the code on 2026-11-23".
- Contracts that code reads: [`knowledge-contract.md`](../../knowledge-contract.md) and [`schemas/knowledge-section.schema.json`](../../schemas/knowledge-section.schema.json). `experiments/laya/kb.py` and `.agents/skills/add-park-knowledge/scripts/knowledge.py` load the schema by path in `SCHEMA`. Keep both paths.
- Agent instructions: [`mobile/AGENTS.md`](../../../mobile/AGENTS.md) holds the Expo rules and checks. The repo root has no `AGENTS.md` or `CLAUDE.md`. The root [`README.md`](../../../README.md) is the nearest equivalent.
- Skills: `.agents/skills/add-park-knowledge/` is the knowledge editing skill. `.claude/skills/add-park-knowledge` is a symlink to it. `.claude/skills/` also holds `mobile-offline-stack`, `app-design`, and `hackathon-lean`.

## Runtime or data flow

`docs/history/phase3-architecture.md` is superseded but still cited by section number in code comments. Examples are `mobile/src/core/knowledge/types.ts`, `rerank.ts`, `safety.ts`, and `mobile/src/llm/laya.ts`. `mobile/src/core/knowledge/policy.ts` records that the top-1 policy replaced its menu of three. Read history docs to decode those comments, not as instructions.

`research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json` is a byte-identical copy of the docs schema (checked with `cmp`). Its `coordination/` folder holds `rebuild_all.py`, `coordinator_fixes.py`, and `validate_knowledge.py`.

## Tests

`tests/test_add_park_knowledge.py` runs `knowledge.py` against a temp root that copies `docs/schemas` and `data/knowledge/sections`. Run it with `uv run pytest` from the repo root.

## Common change paths

- Knowledge edits follow the `add-park-knowledge` skill and the "Changing the knowledge" steps in the root README.
- A schema change needs the `research_notes` copy updated too. No test checks that the copies match.
- A design or UI rule change belongs in `.claude/skills/app-design/SKILL.md`, which has uncommitted edits in the live checkout.

## Related docs

- [`docs/system-map.md`](../../system-map.md) lists the blast radius for each change.
- [`mobile/README.md`](../../../mobile/README.md) covers the build and the checks.
