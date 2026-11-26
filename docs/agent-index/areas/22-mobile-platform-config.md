# Mobile platform config

## Purpose

This page maps the build, bundler, lint, and type settings of the Expo app in `mobile/`. Knowledge side-loading (`scripts/push-knowledge.sh`) and the `group-radio` native module internals are out of scope.

## Start here

- `mobile/package.json`: Expo SDK `~58`, React Native `0.88.1`, React `19.3.0`. Scripts are `start`, `android` (`expo run:android`), `lint` (`expo lint`), `test` (`jest`), `typecheck` (`tsc --noEmit`), and `postinstall` (`node scripts/patch-ort.js`). The Jest config lives here too, with preset `jest-expo` and `android/` and `ios/` ignored.
- `mobile/app.json`: Android package `co.nevados.assistant`, scheme `nevados`, and the config plugins `expo-router`, `expo-splash-screen`, `expo-sqlite`, `expo-image-picker`, `llama.rn`, `expo-build-properties` (`buildArchs: ["arm64-v8a"]`), and `expo-asset`. `experiments` turns on `typedRoutes` and `reactCompiler`.
- `mobile/metro.config.js`: web-only stubs, COOP and COEP headers, and the `/knowledge-files/` dev route.
- `mobile/tsconfig.json`: extends `expo/tsconfig.base`, `strict`, path aliases `@/*` to `./src/*` and `@/assets/*` to `./assets/*`.
- `mobile/eslint.config.js`: `eslint-config-expo/flat` with `dist/*` ignored.

The scripts in `mobile/scripts/` are run by hand, except `patch-ort.js`.

- `mobile/scripts/patch-ort.js` patches `node_modules/onnxruntime-react-native` on install. It deletes `unimodule.json`, removes a Gradle 9 `VersionNumber` check, and pins the ORT aar to the JS package version.
- `mobile/scripts/push-model.sh <gguf>` copies a GGUF into the app's `files/` with `adb` and `run-as`. It needs a debug build.
- `mobile/scripts/build-vision.py <model> <photos>` writes `assets/vision/encoder.onnx` and `assets/vision/index.json`. Photo sources are listed in `mobile/scripts/vision-sources.json`.

## Runtime or data flow

`mobile/metro.config.js` does four things:

1. `resolveRequest` swaps `llama.rn` and `onnxruntime-react-native` for `src/web-stubs/*.ts` when `platform === 'web'`. The stubs throw on use.
2. `assetExts` gains `wasm` and `onnx`.
3. `enhanceMiddleware` sets `Cross-Origin-Embedder-Policy: credentialless` and `Cross-Origin-Opener-Policy: same-origin` on every response.
4. `/knowledge-files/<name>` serves only the names in `KNOWLEDGE_FILES`. Consumers are `src/llm/knowledgeRuntime.web.ts` and `src/vision/classifyPhoto.web.ts`.

Native modules load lazily where import side effects matter. `src/llm/ort.ts` `ort()` calls `require('onnxruntime-react-native')` because expo-router evaluates every route at startup.

`android/` is generated and git-ignored (`mobile/.gitignore` has `/android`). Change native behavior in `app.json`, not in `android/`.

## Tests

No test covers `metro.config.js`, `app.json`, or `patch-ort.js`. Tests mock native packages instead, for example `jest.mock('@shopify/react-native-skia', ...)` in `src/onboarding/__tests__/skiaScene.test.tsx` and `jest.mock('expo-sqlite/kv-store', ...)` in `src/state/__tests__/petLook.test.ts`.

## Common change paths

- Add a native library: run `npx expo install <pkg>`, add its config plugin to `app.json`, rebuild the dev client. If it touches JSI at import, add a web stub in `metro.config.js` or load it lazily like `ort()`.
- Serve a new file to the web preview: add its name to `KNOWLEDGE_FILES`.

## Related docs

- [Mobile README](../../../mobile/README.md) has the build commands, APK paths, prerequisites, and checks.
- [Mobile AGENTS.md](../../../mobile/AGENTS.md) has the Expo rules and the Gradle build note.
- [Mobile offline stack skill](../../../.claude/skills/mobile-offline-stack/SKILL.md) has the runtime contracts.
