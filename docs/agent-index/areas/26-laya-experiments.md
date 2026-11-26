# Laya experiments

## Purpose

`experiments/laya/` is an isolated uv project (`pyproject.toml`, `laya==0.5.1`, CPU torch) for the e5-base retrieval and Laya reorderer experiments. Most scripts are historical. One file, `export_knowledge.py`, is still a live library for the shipping export.

## Start here

- `export_knowledge.py` is a shared library. `experiments/nlu/export_nlu.py` imports `ASSETS`, `FIXTURES`, `PREFIX`, `SECTIONS`, `EMERGENCY_LINE_ID`, `corpus_hash`, `embed_gguf`, and `write_scorer` from it. Do not run its `main()`. It writes the old `e5-top1-v1` policy over the current `e5-nlu-v1` assets.
- `kb.py` loads and validates sections (`load_sections`, `Entry`). `export_nlu.py` puts its own directory first on `sys.path`, so its `from kb import APP, app_texts, clean` resolves to `experiments/nlu/kb.py`, not this file.
- `retrieval.py` has `Retriever.retrieve`, the gateway or flat pool used by the curation-v2 scripts.

## Runtime or data flow

These are historical runs, grouped by phase in their docstrings.

1. Phase 1 (`exp.py`, `onnx_exp.py`, `prompts_exp.py`) reads `data/knowledge/phase1/` and writes `results/p1-laya/`.
2. Phase 3 fine-tune (`ft_data.py`, `ft_smoke.py`, `eval_ft.py`, `quant_sweep.py`, `final_onnx.py`) builds rows in `data/knowledge/laya_ft/`, then gates an ONNX int8 checkpoint.
3. Curation v2 runs `leak_check.py`, then `splits_v2.py` for the family-disjoint `dev_gate`/`test_blind` split and `MANIFEST.json`. Next, `ft_data_v2.py` writes `data/knowledge/laya_ft_v2`, and `bench_v2.py` compares results with Wilson intervals.
4. `gguf_parity.py` compares GGUF and sentence-transformers vectors. `laya_fixtures.py` writes `mobile/src/core/knowledge/laya/__fixtures__/laya_io.json`.

Laya status on the phone is verified in code. It is off. `policy.laya.enabled` is `false` in `mobile/assets/data/knowledge/policy.json`. `encodeLaya` in `mobile/src/llm/laya.ts` throws because the tokenizer is not ported yet. `loadLaya` in `mobile/src/llm/knowledgeRuntime.ts` returns `undefined` when Laya is off. No test reads `laya_io.json`.

## Tests

- `experiments/laya/test_retrieval_v2.py` covers the gateway delta and the five-section cap, `is_correct`, `filter_verified`/`split`, and `wilson(0, 0)`. pytest is not a dependency in `pyproject.toml`, so the run command is unverified.
- `mobile/src/core/knowledge/__tests__/engine.test.ts` tests the reranker seam with Laya off.

## Common change paths

- To change the shipped assets, edit `experiments/nlu/export_nlu.py`. The regeneration command is in `.claude/skills/mobile-offline-stack/SKILL.md`.
- To turn Laya on, port `encodeLaya` against `laya_io.json` first, then follow the gate in `phase3-architecture.md` §1.4.

## Related docs

- [Phase 1 Laya report](../../history/phase1-laya-report.md)
- [Phase 3 architecture](../../history/phase3-architecture.md)
- [Knowledge system plan](../../history/plan-knowledge-system.md)
- [Knowledge contract](../../knowledge-contract.md)
- [Retrieval architecture](../../retrieval-architecture.md)
