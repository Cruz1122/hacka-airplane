# Mobile chat flow

## Purpose

This page maps the chat tab in `mobile/` from route to store. The retrieval engine is in [the runtime pipeline](../../architecture.md#runtime-pipeline).

## Start here

| Role | File and symbol |
|---|---|
| Route and wiring | `mobile/app/(tabs)/index.tsx`, `ChatScreen` |
| React hook, one store per process | `mobile/src/state/useKnowledge.ts`, `useKnowledge`, `preloadKnowledge` |
| Chat state | `mobile/src/state/knowledgeChat.ts`, `KnowledgeChat.ask`, `askPhoto`, `reset` |
| Rows to bubbles | `mobile/src/state/knowledgeRows.ts`, `toChatRows` |
| Screen | `mobile/src/chat/ChatView.tsx`, `ChatView`, `ChatRow`, `ChatViewProps` |
| Input | `mobile/src/ui/chat/ChatComposer.tsx`, `useDraft` |
| Onboarding exit animation | `mobile/src/chat/handoff.ts`, used by `mobile/app/onboarding.tsx` |

## Runtime or data flow

Verified from the code:

1. `mobile/app/_layout.tsx` calls `preloadKnowledge()` at launch.
2. `useDraft` in `ChatComposer` sends only when enabled and with text or a photo, then clears the field.
3. `ChatView.send` calls `follow.rearm()`, then `onSend`.
4. `ChatScreen.onSend` calls `askPhoto` when a photo is attached, otherwise `ask`.
5. `KnowledgeChat.ask` drops blank text and calls made while `busy`. It appends the user row with `busy: true`. Help and photo-edit requests get a fixed `abstain` reply. Other text goes to `engine.ask`. An exception becomes an `error` row.
6. `toChatRows` splits a banner into its own bubble and shows `t.knowledge.error` for an error row.
7. `ChatView` shows `TypingBubble` while `busy`. The composer is disabled while `busy` or until `model.status` is `ready`. `ChatScreen` maps a degraded runtime to `ready`.

The onboarding calls `router.replace('/', { sceneTime })`. `ChatScreen` passes `sceneTime` and `fadeIn` to `ChatView`.

`reset()` increments `generation`. Only `askPhoto` checks `generation`, so a text reply that is still pending at reset still appends its row.

## Tests

Jest files under `mobile/`:

- `src/state/__tests__/knowledgeChat.test.ts` covers `ask`, `reset`, and media picks.
- `src/vision/__tests__/photo.test.ts` covers `askPhoto`.
- `src/state/__tests__/knowledgeRows.test.ts` covers `toChatRows`.
- `src/state/__tests__/useKnowledge.test.tsx` covers the preload and the degraded load.
- `src/chat/__tests__/ChatView.test.tsx` covers keyboard, fade-in, scroll follow, and latency format. The other files in `src/chat/__tests__/` and `src/ui/chat/__tests__/` cover single components.

## Common change paths

- To change reply logic, edit `knowledgeChat.ts`, then the `KnowledgeChat` tests.
- To change bubble content, edit `toChatRows` and `ChatRow` together.
- To change send rules, edit `useDraft`, then `ChatComposer.test.tsx`.

## Related docs

- [Runtime pipeline](../../architecture.md#runtime-pipeline)
- [System map](../../system-map.md)
- [Mobile agent rules](../../../mobile/AGENTS.md)
