# Mobile app routes

## Purpose

This page maps the Expo Router files in `mobile/app/`. Each file is one route. `package.json` sets `"main": "expo-router/entry"`, and `app.json` sets the `nevados` URL scheme and `experiments.typedRoutes`. The recorrido tab and the `estacion/` routes belong to area 19.

## Start here

- `mobile/app/_layout.tsx`: `RootLayout`. It waits for `FONT_FILES`, calls `preloadKnowledge`, and declares a `Stack` with `(tabs)`, `settings`, `history`, `onboarding`, `lab`, `design`, and `estacion`.
- `mobile/app/(tabs)/_layout.tsx`: `TabsLayout`. It declares a `Tabs` navigator with `index` (chat), `group`, and `recorrido`. `tabBar={hiddenTabBar}` hides the built-in bar, and `backBehavior="firstRoute"` sends Android back to the chat.
- `mobile/src/ui/AppNavBar.tsx`: the tab switcher. `ROUTE` maps `NavTab` ids to tab route names, and it calls `navigation.navigate({ name, merge: true })`.
- `mobile/src/state/launchGate.ts` and `mobile/src/onboarding/launch.ts`: `needsOnboarding` and the per-launch `handedOver` flag.
- Other routes: `settings.tsx`, `history.tsx`, `onboarding.tsx`, `design.tsx`, `lab.tsx` (native fallback), and `lab.web.tsx` (web editor). `spike.tsx` and `radio-spike.tsx` are dev-only and get no `Stack.Screen` entry.

## Runtime or data flow

1. The launch opens `/`. `TabsLayout` returns `<Redirect href="/onboarding" />` while `needsOnboarding(onboardingDone(), pathname)` is true.
2. `openChat` in `onboarding.tsx` calls `markOnboardingDone()` and `router.replace('/')`, with an optional `sceneTime` param.
3. A link into `/group` skips the onboarding. `TabsLayout` then calls `markOnboardingDone()`.
4. Tab switches keep each tab mounted and keep its params because of `merge: true`.

Gap, verified by grep: no code in `mobile/app/` or `mobile/src/` navigates to `/settings` or `/history`. `AppNavBar` passes no `onSettings` to `CloudNavBar`, so the settings button has no handler. Inferred from Expo Router file routing and the `nevados` scheme, these screens open only by URL, such as `nevados://settings`.

The repository has uncommitted route edits at the time of writing. The `recorrido` tab, the `estacion` stack entry, and the reduced-motion tab animation are not committed yet.

## Tests

- `mobile/src/state/__tests__/tabsNavigation.test.tsx` mounts the real `TabsLayout` with `ExpoRoot` and `getMockContext`. It covers the onboarding handoff, back behavior, kept params, and links into `/group`.
- `mobile/src/ui/group/__tests__/groupScreen.test.tsx` mounts `TabsLayout` at `/group`.
- `mobile/src/onboarding/__tests__/onboarding.test.tsx` mocks `router.replace`.

## Common change paths

- To add a stack screen, add `mobile/app/<name>.tsx`. Add a `Stack.Screen` in `_layout.tsx` only when it needs a title or options.
- To add a tab, add `mobile/app/(tabs)/<name>.tsx` and a `Tabs.Screen`. Extend `NavTab`, `TABS` in `CloudNavBar.tsx`, and `ROUTE` in `AppNavBar.tsx`. Then add a case to `tabsNavigation.test.tsx`.
- To wire the settings button, pass `onSettings` from `AppNavBar`.

## Related docs

- [System map](../../system-map.md) names `app/settings.tsx` as the reader of `world.json`.
- [Architecture](../../architecture.md) lists the legacy modules that the settings screen still uses.
