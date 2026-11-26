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

Jest covers the core parity fixtures (`src/core/__tests__`), `src/llm/http.test.ts`, `src/llm/models.test.ts` and the onboarding scene (`src/onboarding/scene/__tests__`).

Prettier is not a required check (no `.prettierrc`; `prettier --check` fails on the whole tree).

## Onboarding and Onboarding Lab

The onboarding scene is layered SVG (`react-native-svg`) generated from one JSON document (`SceneDoc`). The app and the Lab both render it with the same component.

```bash
cd mobile
npx expo start --web --port 8081 < /dev/null   # then open:
#   http://localhost:8081/lab          editor (desktop, web only)
#   http://localhost:8081/onboarding   production onboarding screen
#   http://localhost:8081/design       design system catalog (tokens, components, Pet)
```

| Path | Role |
|---|---|
| `src/onboarding/scene/` | Pure TS: `types.ts` (coordinate system, 14 layer ids), `preset.ts` (default scene, palette and timeline), `geometry.ts` (path builders, `sceneViewBox`), `doc.ts` (lookups and immutable edits), `timeline.ts` (keyframe tracks, idle motions, keyframe editing) |
| `src/onboarding/NevadoScene.tsx` | Production renderer: one view + `<Svg>` per layer (`<G id="layer-*">`), `<G id="obj-*">` per object. Layer opacity and blur are view styles, so they cost no SVG redraw |
| `src/onboarding/OnboardingOverlay.tsx` | UIOverlay layer: the cloud card (React Native title, subtitle, step dots, CTA), driven by the same progress as the scene |
| `src/onboarding/layout.ts` | Screen split: the scene fills the area above the card; app, Lab stage and SVG export share it. Also the emblem's place in the card |
| `src/chat/` | Chat screen: `ChatView` (plain props; `app/index.tsx` wires `useAssistant`, `/design` shows fixtures), `ChatBackdrop` (the screen-3 scene without its volcano and Pet, zoomed and moved so the crater's spot sits over the Pet's circle, plus the vapor sheet), `chatLayout.ts` (that placement; the header is laid out from the tallest height seen, so the keyboard never moves it), `PetCircle.tsx` (the animated Pet in its circle), `handoff.ts` (the onboarding's exit into the chat: card copy fades, volcano and scene Pet fade, scene and card-turned-sheet move together, the circle opens; transforms and opacity only, native driver, ends on the chat's first frame) |
| `src/i18n/` | UI copy: `es.ts` (source of the keys), `en.ts`, `index.ts` (`t`, `fill`, `LOCALE`). A new language is one file plus a line in `LOCALES`; the active locale is fixed to `es` because the assistant answers only in Spanish |
| `src/ui/pet/` | The Pet mascot: `petCore.ts` (geometry and preset ported from its own lab), `PetVaporFigure.tsx` (one frame drawn as vapor, the Pet's only look), `Pet.tsx` (animated: breathing, tail, blinking, glancing around, thinking/talking), `useFaceTransition.ts` (the Pet's own emotion morph for frame-by-frame hosts such as the scene), `PetFigure.tsx` (old glossy frame, no longer drawn) |
| `src/onboarding/usePlayback.ts` | Progress between screens (transitions, swipe), idle-motion clock, reduced-motion setting |
| `src/lab/` | Web-only editor: layer tree, phone/tablet stage with drag and handles, inspector with ◇ keyframe buttons, timeline (play, scrub, tracks), undo/redo, JSON/SVG export |
| `app/onboarding.tsx`, `app/lab.web.tsx` | Routes (`app/lab.tsx` is the native fallback Expo Router requires) |

How the animation works:
- Progress runs from 0 (screen 1) to 2 (screen 3). Tracks in `doc.timeline` key camera, layer opacity and blur, object transform/body fields or palette colors per progress; "Siguiente", the dots and a horizontal swipe animate progress with `transitionMs` (900) and `easing` (easeOut).
- Focus: each layer has `blur` (scene units, 0 = sharp), keyed per screen as `layer.<id>.blur`, so the sharp depth moves between screens (1: Nevado and Pet sharp, sky and ranges soft; 2: sky and far ranges sharp, hills and vegetation soft; 3: everything sharp, since a soft background on screen 3 cost a tablet 3 -> 1 transition about 24 fps). Blur tracks exist only for distantClouds, farMountains, midMountains, hills, vegetation and ruizMascot: each blurred layer is a GPU pass every frame, so the volcano layers and the foreground mist stay unblurred. In the Lab: select an object, then "Desenfoque (foco)" in the layer section; ◇ keys it at the current progress. On web, during a transition or swipe each layer follows the camera as a view transform and the SVG is redrawn once when it stops; native keeps the camera inside the SVG (see TODO in NevadoScene.tsx).
- The cloud card's top edge is vapor like the Pet (wide solid-centre billows over the card body, `src/ui/CloudCard.tsx`); its surface is memoized, so transitions do not redraw it. The park emblem (`ParkEmblem`) sits below that edge (`EMBLEM_TOP` in `layout.ts`).
- Idle motions (`object.motion`: drift, bob, sway, breathe, rise, live) run on wall-clock time and stop under the OS reduce-motion setting, which also makes screen changes instant.
- In the Lab, editing a property that has a track sets a keyframe at the current progress; other edits change the base scene.
- The visible window adapts to the screen (`sceneViewBox`): phones keep the 390 width, tablets keep the 844 height and show more landscape. The scene only fills the area above the cloud card (`onboardingLayout`); on landscape tablets the card covers more of the foreground so the sky and the Pet are never cropped.
- The `ruizMascot` layer holds the Pet, hosted on the volcano like the steam: its transform is an offset from the crater vent, and the `live` motion drives its blinking, mist and tail. Its emotion, voice and audio are keyed per screen (text values switch at the midpoint of a transition). In the scene it is drawn as vapor (`PetVaporFigure`: a defined body with a soft halo, in the mist colors `fill`/`shade`, without filters or masks) and its tail rises out of the crater's opening; the default scene has no separate steam plume.

The Lab autosaves to the browser's `localStorage`, which hides later changes to `preset.ts`. Use "Preset" to reload the code preset, and "Copiar JSON" or "Exportar JSON" to hand edits back. A saved scene from an older `SCENE_VERSION` (now 5: layers gained `blur`) is ignored and the preset loads instead.

Design system: colors, Inter fonts and components are documented in `.claude/skills/app-design/SKILL.md` and defined in `src/ui/theme/tokens.ts`; `src/ui/__tests__/design-guard.test.ts` fails on raw colors, font names, `fontWeight` or literal copy in UI files. Inter ships in `assets/fonts/` (static weights cut from the variable font, Latin subset, `Inter-OFL.txt`); swapping the font means replacing those files and `fonts` in the tokens.

Web build notes:
- `metro.config.js` swaps `llama.rn` for `src/web-stubs/llama-rn.ts` on web only. Expo Router bundles every route, and `llama.rn` reads a TurboModule at import time.
- `metro.config.js` also adds `.wasm` assets and the COEP/COOP headers that `expo-sqlite` needs on web (Expo SDK 58 "Web setup"). Without them the settings read never resolved and the chat stayed on "Cargando modelo...". On web the chat then reports that the model only runs on the phone (`expo-file-system` cannot check the model file there).
- `react-native-svg` and `react-native-web` were added for this feature (approved 2026-11-22). `react-native-svg` is native code: the dev APK must be rebuilt before the app opens on a phone.

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
