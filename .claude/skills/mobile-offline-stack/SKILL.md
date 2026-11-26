---
name: mobile-offline-stack
description: Fixed architecture and contracts of the Expo offline assistant in mobile/ - embedding knowledge chat (fine-tuned e5 GGUF on llama.rn + ONNX scorer on onnxruntime-react-native, top-1 curated answer, Laya reorderer off), Skia renderers on native, generated assets and side-loaded model files. Read before touching mobile/, experiments/nlu/export_nlu.py, experiments/laya/export_knowledge.py or src/nevados_bench/export_mobile.py.
---

# Mobile offline stack (decided; do not relitigate)

Human docs: `docs/retrieval-architecture.md` (gateway, gates, per-gate strategies, decision layer), `docs/architecture.md` (pipeline, assets, regeneration), `docs/system-map.md` (how every folder, script and model connects; what to redo after a change) and `mobile/README.md` (build, routes, layout). This skill holds the rules an agent must not break.

## User decisions

- Real PNN Los Nevados. **No generative model, no router, no LLM** in the chat (2026-11-22). Every reply is a curated catalog answer or a policy text.
- Top-1 policy: answer with the best entry when its score clears `policy.T`, else abstain. No menus.
- Laya reorderer: kept as an option, `policy.laya.enabled` false. `src/llm/laya.ts` is a stub that throws until its tokenizer port passes `src/core/knowledge/laya/__fixtures__/laya_io.json`.
- Native onboarding and Pet draw with `@shopify/react-native-skia` (2026-11-23, approved for perf). Web draws the onboarding and chat header scenes and the chat Pet on 2D canvases (2026-11-24, for perf); `NevadoScene` (react-native-svg) stays the reference look and the Lab's renderer.
- No network at runtime.

## Pipeline (do not reorder)

safety + live-status text rules (`src/core/knowledge/safety.ts`) -> follow-up check -> e5 embedding (`clean` only when `policy.strip_fillers`; off) with `"query: "` prefix (own llama.rn context in `src/llm/embedder.ts`, never through `ModelManager`) -> ONNX scorer over all index rows (`src/llm/scorer.ts`) -> vector gateway over the 15 gates (all open: `delta` 2.0, `max_sections` 15) -> entry score = mean of best `score_topk` rows, follow-up fusion (`engine.ts`, `policy.followup`) -> reranker seam (identity) -> top-1 policy (`policy.ts`) -> curated text by id, rendered by `app/index.tsx` through `src/state/useKnowledge.ts` and `knowledgeRows.ts`.

- `src/core/knowledge/` stays pure TS (no React/RN imports); embedder and scorer are injected.
- Missing or bad side-loaded files -> `degradedKnowledgeEngine`: safety rules still answer, other questions raise `KnowledgeEngineError`.
- Every reply carries the curated 123 line; urgent messages get a banner plus the emergency entry.

## Generated files (never hand-edit)

| Files | Generator |
|---|---|
| `mobile/assets/data/knowledge/{catalog,sections,policy,index}.json`, `src/core/knowledge/__fixtures__/{retrieval,clean}.json`, `models/knowledge/{index.f32.bin,index_scorer.onnx}` | `cd experiments/laya && uv run python ../nlu/export_nlu.py --gguf ../../models/knowledge/e5-nlu-ft4-f16.gguf --T 0.5 --w 5.0 --max-words 5 --below 0.7 --cue` |
| `src/core/knowledge/laya/__fixtures__/laya_io.json` | `experiments/laya/laya_fixtures.py` |
| `mobile/assets/data/world.json`, legacy `src/core/__fixtures__/*` | `uv run python -m nevados_bench.export_mobile` (legacy) |

Do not run `experiments/laya/export_knowledge.py` directly: it writes the older `e5-top1-v1` format over the current `e5-nlu-v1` assets. It is the shared library `export_nlu.py` imports.

## Model files (side-loaded, not in the APK)

- Named by `assets/data/knowledge/index.json`; pushed with `mobile/scripts/push-knowledge.sh [--with-laya]` (debug builds only, `run-as`). The app checks each file's byte size against the manifest.
- `models/knowledge/e5-nlu-ft4-f16.gguf` cannot be rebuilt from the repo (trained in Colab, payload not committed). Never delete or overwrite it.

## Stack and dependencies

- Expo SDK 58, RN 0.88 new arch, Hermes, TypeScript strict, `expo-router`, development build (`expo-dev-client`, CNG). Not Expo Go. Android arm64 first; npm only.
- `mobile/android` is generated: never edit; change `app.json` or plugins. Release: `cd mobile/android && ./gradlew assembleRelease -PreactNativeArchitectures=arm64-v8a`.
- Dependency whitelist: expo + its template deps, expo-router, expo-dev-client, expo-file-system, expo-sqlite (and kv-store), llama.rn, onnxruntime-react-native (patched by `scripts/patch-ort.js` on postinstall), @shopify/flash-list, @shopify/react-native-skia, react-native-svg, react-native-web, @wllama/wllama (web chat only, approved 2026-11-23). Dev: jest-expo, @types/*, prettier. Anything else needs the user's approval.
- Web: `metro.config.js` swaps `llama.rn` and `onnxruntime-react-native` for `src/web-stubs/`. The web chat runs the same e5 GGUF on wllama (`src/llm/knowledgeRuntime.web.ts`), fetched with the vectors from the dev server's `/knowledge-files/` (an allowlist in `metro.config.js`); no ONNX scorer (JS loop), Laya off. A static `expo export` has no models.

## Renderers

- One `SceneDoc` (`src/onboarding/scene/`), three renderers: `SceneCanvas.native.tsx` + `skia/drawScene.ts` (native, Skia), `SceneCanvas.tsx` + `canvas2d/drawScene2d.ts` (web app, one 2D canvas per layer, layer blur and opacity in CSS), `NevadoScene.tsx` (SVG, the reference: Lab, export). A new body kind goes into all three; `__tests__/canvas2dScene.test.ts` checks the web layout against the native one.
- Pet: `src/ui/pet/Pet.tsx` -> `PetVaporCanvas` (`.native.tsx` Skia via `drawPet.ts`, web 2D canvas via `drawPetCanvas2d.ts`); `PetVaporFigure` (SVG) is the reference and the Lab's figure.
- Skia pitfalls: always pass bounds to `PictureRecorder.beginRecording` (the default cull rect drops content at negative coordinates); Jest cannot load Skia, so data modules (e.g. `src/chat/headerScene.ts`) must not import renderers.
- Measure perf on a release build on the phone (`adb shell dumpsys gfxinfo`), never from web or debug numbers.

## Legacy (still compiled, not in the chat path)

`src/core/*.ts` outside `knowledge/` (FSM port), `src/llm/{llamaRn,modelManager,models,fake}.ts`, `app/settings.tsx` (model/backend/answer-mode controls the chat ignores) and `src/nevados_bench/` (`export_mobile` closure). They must stay unreachable from the knowledge path. Removing them starts with the settings screen; the old contracts are in git history and `docs/history/`.
