# Shared UI: navigation, theme, and icons

## Purpose

This area covers the app shell, the top tab bar, design tokens, fonts, icons, and reduced motion. Chat, group, and Pet components are out of scope.

This page reflects the live checkout on 2026-11-25. The Recorrido tab and the `CloudNavBar` side buttons are uncommitted at `45a394d5`.

## Start here

- [`mobile/app/_layout.tsx`](../../../mobile/app/_layout.tsx): `RootLayout` waits for `FONT_FILES`, then renders the root `Stack`.
- [`mobile/app/(tabs)/_layout.tsx`](../../../mobile/app/%28tabs%29/_layout.tsx): `TabsLayout` redirects to `/onboarding` through `needsOnboarding` in [`src/state/launchGate.ts`](../../../mobile/src/state/launchGate.ts). The navigator's own tab bar is hidden.
- [`mobile/src/ui/AppNavBar.tsx`](../../../mobile/src/ui/AppNavBar.tsx): maps `NavTab` to route names in `ROUTE` and calls `navigation.navigate({ name, merge: true })`, so a switch keeps the tab's params.
- [`mobile/src/ui/CloudNavBar.tsx`](../../../mobile/src/ui/CloudNavBar.tsx): router-free bar exporting `NavTab` and `NAV_BAR_HEIGHT`. It reports taps through `onSelect`.
- [`mobile/src/ui/theme/tokens.ts`](../../../mobile/src/ui/theme/tokens.ts): `brand`, `fonts`, `type`, `colors`, `spacing`, and `radius`. [`theme/fonts.ts`](../../../mobile/src/ui/theme/fonts.ts) maps families to TTF files. [`theme.ts`](../../../mobile/src/ui/theme.ts) exports `useColors()`.
- [`mobile/src/ui/icons/Icon.tsx`](../../../mobile/src/ui/icons/Icon.tsx): Lucide paths in `GLYPHS`, typed by `IconName`, hidden from screen readers.
- [`mobile/src/ui/useReducedMotion.ts`](../../../mobile/src/ui/useReducedMotion.ts): `ReducedMotionOverride` lets `app/design.tsx` force it on.

## Runtime or data flow

1. `TabsLayout` mounts the `index`, `group`, and `recorrido` tabs.
2. Each tab screen draws its own `<AppNavBar active=... />`.
3. Content below the bar offsets by `insets.top + NAV_BAR_HEIGHT`, as in `src/chat/ChatView.tsx`.

Inferred from source: `AppNavBar` passes no `onSettings` or `onAccessibility`, so the settings and accessibility side buttons do nothing when pressed.

## Tests

- [`src/ui/__tests__/design-guard.test.ts`](../../../mobile/src/ui/__tests__/design-guard.test.ts) scans `app`, `src/ui`, `src/chat`, and `OnboardingOverlay.tsx`. It rejects raw colors, non-token fonts, `fontWeight`, and literal copy.
- [`src/state/__tests__/tabsNavigation.test.tsx`](../../../mobile/src/state/__tests__/tabsNavigation.test.tsx) drives the real `TabsLayout` and `AppNavBar`. It covers onboarding, Android back, kept params, and deep links.
- [`src/ui/__tests__/reduced-motion.test.tsx`](../../../mobile/src/ui/__tests__/reduced-motion.test.tsx) covers the override.

No test renders `CloudNavBar` or `Icon` alone. The bar renders on `/design` through `src/design/ControlsLabs.tsx`.

## Common change paths

- To add a tab, add a `Tabs.Screen` and extend `NavTab`, `TABS`, `ROUTE`, and `t.nav` in `src/i18n/en.ts` and `es.ts`.
- To add a color or text style, add it to `tokens.ts`. Inline hex values fail the design guard.
- To add an icon, paste its Lucide paths into `GLYPHS`.

## Related docs

- [`.claude/skills/app-design/SKILL.md`](../../../.claude/skills/app-design/SKILL.md) has the component catalog, token rules, and UI verification steps.
- [`docs/architecture.md`](../../architecture.md) lists the Skia and SVG renderers for each platform.
