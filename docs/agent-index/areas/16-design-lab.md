# Design workshop and onboarding Lab

## Purpose

`/design` shows one design-system component at a time with live controls and sample data. `/lab` is a desktop web editor for the onboarding `SceneDoc`. `mobile/app/_layout.tsx` registers both as stack screens. No app screen links to either route, so you open them by URL.

All paths below are relative to `mobile/`.

## Start here

| Path | What it holds |
| --- | --- |
| `app/design.tsx` | `DesignScreen` and the `LABS` map from `WorkshopId` to a lab |
| `src/design/registry.ts` | `WorkshopId` and `WORKSHOP_ITEMS` in nav order |
| `src/design/chrome.tsx` | `LabProps`, `WorkshopNav`, and shared controls |
| `src/design/fixtures.ts` | Sample rows: `TALK`, `SOURCED`, `URGENT`, `PHOTO_THREADS`, `CATALOG_ANSWER`, `READY` |
| `app/lab.web.tsx` | Re-exports `@/lab/Lab`. `app/lab.tsx` is a native hint screen |
| `src/lab/` | `Lab.tsx`, `Stage.tsx`, `params.ts`, `useSceneHistory.ts` |

## Runtime or data flow

1. `registry.ts` builds `WORKSHOP_ITEMS` from `ORDER`.
2. `WorkshopNav` sets `selected`.
3. `DesignScreen` renders `LABS[selected]` with `key={selected}`, so lab state resets on switch.
4. Each lab renders real components from `src/ui/`, and `BubblesLab` also mounts `ChatView` from `src/chat/`.

`fixtures.ts` builds rows with the live chat's code: `messageSources`, `loadWorld`, `toChatRows`, and `pickMedia`. `GroupLab` builds `GroupState` with `step` from `@/core/group/groupState`.

`/lab` starts from `defaultScene()` in `src/onboarding/scene/preset.ts`. `useSceneHistory` autosaves to the `localStorage` key `nevados.onboardingLab.scene`. The Lab exports JSON and SVG downloads and writes no source file. I infer that a scene change reaches the app only through a manual edit of `preset.ts`.

## Tests

- `src/design/__tests__/BubblesLab.test.tsx` checks that `CATALOG_ANSWER` equals `catalog.json`.
- `src/design/__tests__/ComposerLab.test.tsx` covers presets, send, and reset.
- `src/onboarding/scene/__tests__/scene.test.ts` tests `PARAMS`, `handlesOf`, and `parseScene`.
- `src/chat/__tests__/ChatView.test.tsx` imports `READY` from the fixtures.
- `src/ui/__tests__/design-guard.test.ts` scans `app/` minus `app/lab*`, not `src/design` or `src/lab`.

No test covers `ButtonsLab`, `IndicatorsLab`, `GroupLab`, or `FoundationsLab`.

## Common change paths

To add a workshop entry:

1. Add the id to `WorkshopId` and `ORDER`.
2. Add `t.dev.workshop.items.<id>` in `src/i18n/es.ts` and `src/i18n/en.ts`.
3. Write the lab in `src/design/`.
4. Add it to `LABS`.

The `registry.ts` comment names a `./labs` folder that does not exist.

## Related docs

- [App design skill](../../../.claude/skills/app-design/SKILL.md) lists the tokens and components.
- [Architecture](../../architecture.md) names the web renderers.
