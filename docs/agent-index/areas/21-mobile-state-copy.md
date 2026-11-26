# Mobile state, copy, and launch handoff

## Purpose

Map of client state ownership in `mobile/`, UI copy lookup, and the onboarding-to-chat launch handoff. Written against a checkout with uncommitted edits in `mobile/src/state/`, `mobile/src/i18n/`, and `mobile/app/`.

## Start here

| Need | File | Symbols |
| --- | --- | --- |
| Chat state | `mobile/src/state/knowledgeChat.ts` | `KnowledgeChat`, `KnowledgeRow`, `KnowledgeChatState` |
| React binding of chat state | `mobile/src/state/useKnowledge.ts` | `preloadKnowledge`, `useKnowledge` |
| Rows to bubbles | `mobile/src/state/knowledgeRows.ts` | `toChatRows` |
| Persisted settings | `mobile/src/state/settings.ts` | `useSettings`, `loadSettings`, `saveSettings` |
| Grupo stores | `mobile/src/state/petLook.ts`, `alertDistance.ts` | `usePetLooks`, `setPetLook`, `useAlertDistance`, `setAlertDistance` |
| Verified-only chat switch | `mobile/src/state/verifiedOnly.ts` | `useVerifiedOnly`, `setVerifiedOnly`, `getVerifiedOnly`, `loadVerifiedOnly` |
| Tool-effect log | `mobile/src/state/history.ts` | `recordEffect`, `useHistory` |
| Copy | `mobile/src/i18n/index.ts`, `es.ts`, `en.ts` | `t`, `fill`, `LOCALES`, `Labels` |
| Launch gate | `mobile/src/state/launchGate.ts`, `mobile/src/onboarding/launch.ts` | `needsOnboarding`, `onboardingDone`, `markOnboardingDone` |

## Runtime or data flow

State ownership:

- `useKnowledge.ts` holds one `KnowledgeChat` per process. `app/_layout.tsx` calls `preloadKnowledge` in an effect, so the runtime loads while the onboarding plays. A failed load uses `degradedKnowledgeEngine`.
- `petLook.ts` and `alertDistance.ts` are module stores read through `useSyncExternalStore`. They load on first subscribe and write through to kv-store keys `petLook.v2` and `group.alertMeters.v1`.
- `verifiedOnly.ts` follows the same pattern (kv-store key `knowledge.verifiedOnly.v1`, default off). `useKnowledge.ts` starts its load with the chat store and passes `getVerifiedOnly` to `KnowledgeChat`, which reads it at each question and resets the engine context when it flips.
- `settings.ts` is per-screen `useState` over kv-store key `settings.v1`. `history.ts` uses the `history` table in `nevados.db`.

Localization lookup:

- `es.ts` is the source shape. `Labels = typeof es`, so the type checker rejects missing or extra keys in `en.ts`.
- `LOCALE` is fixed to `'es'`. Screens import `t` and read nested keys such as `t.onboarding.next`. `fill` replaces `{name}` placeholders and throws when a value is missing.
- Gap: `knowledgeChat.ts` keeps Spanish photo and capability replies as string literals outside `i18n`.

Launch handoff:

1. `app/(tabs)/_layout.tsx` redirects to `/onboarding` when `needsOnboarding(onboardingDone(), pathname)` is true. That happens only on the chat path `/` before handover.
2. `openChat` in `app/onboarding.tsx` calls `markOnboardingDone` and replaces the route with `/`, passing `sceneTime` when the idle clock has a time. Under reduced motion it skips the handoff animation.
3. `app/(tabs)/index.tsx` reads `sceneTime` and passes it to `ChatView`.

`handedOver` is module state, so every app start or JS reload shows the onboarding again.

## Tests

- `mobile/src/state/__tests__/` covers each store except `settings` and `history`. `tabsNavigation.test.tsx` covers the launch gate and tab back behavior.
- `mobile/src/i18n/__tests__/labels.test.ts` checks that every locale matches the keys and placeholders of `es` and covers `fill`.
- `mobile/src/onboarding/__tests__/onboarding.test.tsx` covers the `sceneTime` handoff.
- `npm test` in `mobile/` runs `jest` with the `jest-expo` preset.

## Common change paths

- To add a label, add the key to `es.ts`, then add the same key to `en.ts`. `labels.test.ts` fails when the keys or placeholders differ.
- To add persisted cross-screen state, copy the `alertDistance.ts` pattern: a parse function, a lazy load, and `useSyncExternalStore`.
- To change launch routing, edit `needsOnboarding`, then update `tabsNavigation.test.tsx`.

## Related docs

- [Mobile README](../../../mobile/README.md)
- [Mobile agent rules](../../../mobile/AGENTS.md)
- [Architecture](../../architecture.md)
- [System map](../../system-map.md)
