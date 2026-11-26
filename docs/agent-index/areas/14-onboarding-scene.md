# Onboarding scene

## Purpose

One `SceneDoc` describes the onboarding illustration, the chat header backdrop, and the Lab canvas. Three renderers draw it. Paths are relative to `mobile/`.

## Start here

- `src/onboarding/scene/types.ts`: `SceneDoc`, `Layer`, `SceneObject`, the `Body` union, `Track`, and `SCENE_VERSION`. The header comment defines the 390 x 844 coordinate system.
- `src/onboarding/scene/preset.ts`: `defaultScene()` and `DEFAULT_PALETTE`, the shipped scene.
- `src/onboarding/scene/timeline.ts`: `evaluateTracks` (keyframes over progress) and `applyMotions` (idle loops over seconds).
- `src/onboarding/scene/geometry.ts`: pure shape builders and `sceneViewBox`. `scene/doc.ts` holds lookups such as `volcanoOf` and immutable edits.
- `app/onboarding.tsx`: the screen that wires playback to the renderer.

## Runtime or data flow

1. `usePlaybackClock` in `src/onboarding/usePlayback.ts` runs one `requestAnimationFrame` loop. It produces `progress` (0 to `ONBOARDING_SCREENS - 1`) and an idle `time` that holds still during transitions.
2. `OnboardingScene` in `app/onboarding.tsx` computes `applyMotions(evaluateTracks(scene, progress), time)` and passes the doc to `SceneCanvas`.
3. The platform file extension picks the renderer (inferred from the React Native convention).
   - Native: `SceneCanvas.native.tsx` calls `skia/drawScene.ts` `layoutFrame`, which caches one `SkPicture` per body in a `WeakMap`. `drawFrame` then replays the pictures under per-object matrices onto one Skia `Canvas`. The Pet is recorded separately with `@/ui/pet/drawPet`.
   - Web: `SceneCanvas.tsx` renders one `<canvas>` per layer through `canvas2d/drawScene2d.ts` `drawLayer`. CSS applies layer opacity and blur. `samePaint` skips layers whose items did not change.
   - Reference: `NevadoScene.tsx` (react-native-svg), used by `src/lab/Stage.tsx`. Only this renderer reads the `moving` prop.

`src/chat/headerScene.ts` reuses the doc at progress 2 with the volcano and Pet layers hidden. `src/lab/useSceneHistory.ts` `parseScene` rejects imports whose `version` differs from `SCENE_VERSION`.

## Tests

Run `npx jest <path>` from `mobile/` (preset `jest-expo`).

- `src/onboarding/scene/__tests__/scene.test.ts`: the preset, editor parameters, handles, and document edits.
- `src/onboarding/__tests__/canvas2dScene.test.ts`: checks that the web layout matches the native layout and that every body paints.
- `src/onboarding/__tests__/skiaScene.test.tsx`: the Skia renderer on CanvasKit wasm, including the Pet picture cache.
- `usePlayback.test.tsx`, `onboarding.test.tsx`, `overlayMotion.test.ts`, `idleCost.test.ts` in the same folder: playback, re-render counts, and the chat handoff.
- `frameCost.bench.test.tsx` is skipped unless `BENCH=1` is set.

## Common change paths

- New body kind: add it to `types.ts`, bump `SCENE_VERSION`, then draw it in `skia/drawScene.ts`, `canvas2d/drawScene2d.ts`, and `NevadoScene.tsx`. Expose its fields in `src/lab/params.ts`.
- New animated property: add a `Track` in `preset.ts` that uses the target grammar documented on `Track` in `types.ts`.

## Related docs

- [Onboarding and rendering in the architecture doc](../../architecture.md). Its web row names only the SVG renderer and omits `canvas2d`.
- [Onboarding scene in the system map](../../system-map.md)
- [Renderer contracts and Skia pitfalls](../../../.claude/skills/mobile-offline-stack/SKILL.md)
- [Palette and art direction](../../../.claude/skills/app-design/SKILL.md)
