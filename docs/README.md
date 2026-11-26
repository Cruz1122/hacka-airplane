# Docs

| Doc | What |
|---|---|
| [`retrieval-architecture.md`](retrieval-architecture.md) | **The architecture**: vector gateway, the 15 gates and their strategies (declared vs running), shared embedder, follow-ups, decision layer, parameters |
| [`architecture.md`](architecture.md) | Current design: runtime pipeline, assets, regeneration, renderers, what is legacy |
| [`system-map.md`](system-map.md) | The web of the whole repo: every data flow with its script, blast radius per change, nodes not rebuildable from git |
| [`agent-index/`](agent-index/README.md) | Task-first index to 30 code maps for the repository's source, data, tools, and tests |
| [`knowledge-contract.md`](knowledge-contract.md) | Schema and rules of a knowledge entry (read by `kb.py`, the `add-park-knowledge` skill and its tests; do not move) |
| [`schemas/`](schemas/) | JSON Schema of a section file (read by code; do not move) |
| [`../mobile/README.md`](../mobile/README.md) | Mobile developer guide |
| [`../data/knowledge/app/README.md`](../data/knowledge/app/README.md) | App layer files on top of the sections |

## History

Superseded, kept as the record of how the design got here. Do not follow them as instructions.

| Doc | Period |
|---|---|
| `history/project-context.md`, `history/metrics.md`, `history/reports/r1`, `history/reports/r2` | LLM era: Gemma/Qwen benchmarks, router fine-tune, metric definitions |
| `history/plan-knowledge-system.md`, `history/phase1-laya-report.md` | Phase 1: embedding retrieval vs Laya |
| `history/prompts/phase2-deep-research.md` | Phase 2: research prompt for the knowledge base |
| `history/phase3-architecture.md`, `history/phase3-implementation-plan.md` | Phase 3: on-device knowledge system design (menu-of-3 later replaced by top-1) |
| `history/demo/guion.md` | Demo script of the LLM app; needs a rewrite for the knowledge app |
