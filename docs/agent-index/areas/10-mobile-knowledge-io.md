# Mobile knowledge I/O

## Purpose

This page maps how knowledge inputs reach `KnowledgeEngine`. Retrieval logic in `mobile/src/core/knowledge` is out of scope. So are `llamaRn.ts`, `modelManager.ts`, and `models.ts`, which serve the generative model.

## Start here

- `mobile/src/llm/knowledgeAssets.ts` imports the bundled JSON and defines `degradedKnowledgeEngine`.
- `mobile/src/llm/knowledgeRuntime.ts` and `knowledgeRuntime.web.ts` define `loadKnowledgeRuntime` for native and web.
- `mobile/src/llm/embedder.ts` has `loadEmbedder`, `loadVectors`, and `findSideLoaded`.
- `mobile/src/llm/scorer.ts`, `ort.ts`, and `laya.ts` hold the onnxruntime adapters.

## Runtime or data flow

Bundled inputs ship in the JS bundle: `catalog.json`, `sections.json`, `policy.json`, `index.json`, and `depth.json`. `experiments/nlu/export_nlu.py` writes them. Never edit them by hand.

Side-loaded inputs live outside the bundle. `index.json` names each one with its byte size: the e5 GGUF, `index.f32.bin`, and `index_scorer.onnx`. `mobile/scripts/push-knowledge.sh` copies them from `models/knowledge/` into the app files dir with `adb` and `run-as`, so it needs a debug build. `--with-laya` also pushes the Laya ONNX and tokenizer.

On native, `mobile/src/state/useKnowledge.ts` calls `loadKnowledgeRuntime`, which finds each file with `findSideLoaded` and rejects a size mismatch. It does not check hashes. The GGUF runs on llama.rn. The scorer runs on onnxruntime, which `ort()` requires lazily. Laya loads only when `policy.laya.enabled` is true, and it is false. If loading fails, `useKnowledge.ts` falls back to `degradedKnowledgeEngine`, which answers only the safety rules.

On web, the GGUF runs on wllama. The GGUF and vectors come from `/knowledge-files/`, which `mobile/metro.config.js` serves from `models/knowledge/`. There is no scorer, so the JS loop scores the rows. Metro also swaps `llama.rn` and `onnxruntime-react-native` for files in `mobile/src/web-stubs/`.

## Tests

- `mobile/src/state/__tests__/useKnowledge.test.tsx` mocks `@/llm/knowledgeRuntime`.
- `mobile/src/core/knowledge/__tests__/retrieve_sims.test.ts` checks that scorer-style similarities match the JS path.
- Core tests read `models/knowledge/index.f32.bin`, or `KNOWLEDGE_VECTORS`, through `__fixtures__/load.ts`, and throw when it is missing or stale.

Gap: no test covers the `mobile/src/llm` loaders directly.

## Common change paths

1. To add a bundled JSON file, update `export_nlu.py`, `knowledgeAssets`, and `KnowledgeAssets` in `mobile/src/core/knowledge/assets.ts`.
2. To add a side-loaded file, have `export_nlu.py` write it into `index.json`, then add it to `FILES` in `push-knowledge.sh`, and to `KNOWLEDGE_FILES` in `metro.config.js` if the web build needs it.
3. To change embedding settings, edit `CONTEXT_PARAMS` in `embedder.ts` and the matching `loadModel` call in `knowledgeRuntime.web.ts`.

## Related docs

- [Architecture: assets and regeneration](../../architecture.md)
- [System map](../../system-map.md)
- [Knowledge contract](../../knowledge-contract.md)
- [Phase 3 architecture, including the Laya gate](../../history/phase3-architecture.md)
- [Mobile README](../../../mobile/README.md)
- [Models README](../../../models/README.md)
