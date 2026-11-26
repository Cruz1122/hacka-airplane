# Nevados mobile (offline assistant)

Offline visitor assistant for four stations of a fictional park. The app runs a GGUF model on the phone through `llama.rn` (llama.cpp) and ports the Python FSM in `src/nevados_bench` to TypeScript. Expo SDK 58, React Native 0.88, TypeScript strict, Expo Router. Target: Android arm64.

Status: typecheck, lint and Jest are green. No APK has been built yet, so no device run has happened.

## Prerequisites

| Tool | Found on this machine | Notes |
|---|---|---|
| Node | v22.22.3 (fnm) | npm is the only package manager |
| JDK | OpenJDK 21.0.12 (`/usr/bin/java`) | required by Gradle |
| Android SDK | `/opt/android-sdk` (`ANDROID_HOME`) | has build-tools 37.0.0 only |
| Android NDK | missing | needs `ndk;27.1.12297006` |
| Platform | missing (`platforms/` empty) | needs `platforms;android-37` |
| adb | `/usr/bin/adb` | for install, model push, port forward |

Unblock the SDK (user decision: needs licence acceptance and ~1.5 GB download):

```bash
# System-wide (needs sudo)
sudo /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager --licenses
sudo /opt/android-sdk/cmdline-tools/latest/bin/sdkmanager "ndk;27.1.12297006" "platforms;android-37"

# User-level alternative
cp -r /opt/android-sdk ~/Android/Sdk
~/Android/Sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root=$HOME/Android/Sdk --licenses
~/Android/Sdk/cmdline-tools/latest/bin/sdkmanager --sdk_root=$HOME/Android/Sdk "ndk;27.1.12297006" "platforms;android-37"
export ANDROID_HOME=$HOME/Android/Sdk
```

## Install

```bash
cd mobile
npm install
```

## Build and run

Dev build (a development build is required; Expo Go cannot load `llama.rn`):

```bash
cd mobile/android
./gradlew assembleDebug -PreactNativeArchitectures=arm64-v8a --console=plain > /tmp/apk.log 2>&1
tail -40 /tmp/apk.log
```

The first build takes about 3 minutes or more; run it in the background and tail the log. Expected output: `mobile/android/app/build/outputs/apk/debug/app-debug.apk`.

Install and start:

```bash
adb install -r mobile/android/app/build/outputs/apk/debug/app-debug.apk
cd mobile && npx expo start   # Metro for the dev client
```

Side-load the model (debug builds only, uses `run-as`):

```bash
mobile/scripts/push-model.sh /home/cruz1122/dev/hacka-airplane/models/Qwen3-0.6B-Q4_K_M.gguf
```

The script copies the file to `/data/data/co.nevados.assistant/files/`. Set `ANDROID_SERIAL` to pick a device.

Dev HTTP backend (optional, not the default): run a llama-server on the laptop and forward it to the phone:

```bash
adb forward tcp:8083 tcp:8083
```

The app default is `http://127.0.0.1:8083` (`httpUrl` in `src/state/settings.ts`). Ports 8080 to 8082 are used by other work on this machine; do not reuse them.

## Models

Single registry: `src/llm/models.ts` (`MODELS`, `ModelSpec = { id, file, label, quirks }`). `file` is a glob matched against files in the app files dir.

To switch model:
1. Pick an `id` from `MODELS` in the Settings screen (`app/settings.tsx`), or change `modelId` in `DEFAULT_SETTINGS` (`src/state/settings.ts`).
2. Push the matching GGUF with `push-model.sh`. The file name must match the `file` glob in `models.ts`.

Current default is `gemma4-e2b`. The r2 decision (Qwen3-0.6B router) is not applied yet; `DEFAULT_MODEL_ID` in `models.ts` is unused and duplicates `DEFAULT_SETTINGS`.

## Regenerate world data and fixtures

Never edit these files by hand:
- `assets/data/world.json`
- `src/core/__fixtures__/prompts.json`
- `src/core/__fixtures__/replays.json`

```bash
uv run python -m nevados_bench.export_mobile   # writes into mobile/ (--out-dir default)
```

## Tests and checks

```bash
cd mobile
npm run typecheck              # tsc --noEmit
npx expo lint --no-cache       # use --no-cache if import/no-unresolved shows a stale resolver error
npm test                       # jest-expo, Node only
uv run pytest                  # Python side, export_mobile (2 passed in last run)
```

Jest covers the core parity fixtures (`src/core/__tests__`), `src/llm/http.test.ts` and `src/llm/models.test.ts`.

Prettier is not a required check (no `.prettierrc`; `prettier --check` fails on the whole tree).
## Known limitations

- No APK and no device run yet. Install, model load, first-turn latency and second-turn cache reuse are unmeasured.
- Hermes runtime is unverified for `String.normalize`, `BigInt` and regex lookbehind. Jest runs on Node.
- `llama.rn` calls (`initLlama`, `completion`, `stopCompletion`) are unverified on a device.
- `HttpBackend` is non-streaming, so `ttft_ms` is null.
- `ModelManager.warmup()` is not called. The first turn pays the full ~2k-token route prefill.
- Switching backend from device to HTTP leaves the llama context loaded (RAM held). Call `modelManager.release()` in `getBackend` when `kind=http`.
- Model switching (`s.modelId` in `runKey` and `getBackend`) is not exercised in a running app.
- Parity risks not covered by fixtures: `llamaRn.ts` (finish_reason mapping, think-block check, schema stringify), `http.ts` body, `ModelManager`.
- Unused template dependencies may remain in `package.json` (`react-native-reanimated`, `react-native-worklets`, `react-native-gesture-handler`, `expo-font`, `expo-linking`, `expo-constants`). Remove only after a successful build.
- `notebooks/finetune_router.ipynb` has 30 Ruff errors. Outside this scope.
