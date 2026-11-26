# Chat UI components

## Purpose

`mobile/src/ui/chat/` holds reusable chat components and their pure helpers. Screen wiring lives in `mobile/src/chat/ChatView.tsx`. The design catalog (`mobile/src/design/BubblesLab.tsx`, `ComposerLab.tsx`, `ControlsLabs.tsx`) renders them in isolation.

## Start here

- `ChatBubble.tsx`: `ChatBubble` (one message), `BubbleRow` (row, foot shape, entry animation, footer), `markEntered`.
- `ChatComposer.tsx`: `ChatComposer` with `variant` `'docked'` (chat) or `'floating'` (default, used only by `ComposerLab`). `DOCK` holds the docked geometry. The composer owns the draft text.
- `MediaGallery.tsx`: `MediaGallery` lays out a `MediaPick` as `single`, `rows`, or cards. It falls back to rows below `MIN_CARD_WIDTH`. `revealRows` and `mediaRevealId` add a caption stream after each reply.
- `reveal.ts`: `RevealStore` and the shared `replyReveal` type replies out by row id. `useRevealedWords` reads progress.
- `markdown.ts` (`replyDoc`, `parseMarkdown`, `sliceDoc`, `emphasize`), `citations.ts` (`parseCitations`, `ChatSource`), `keywords.ts` (`keywordsFor`, reads `mobile/assets/data/knowledge-keywords.json`).
- Smaller pieces: `SourcesSheet.tsx`, `TypingBubble.tsx` (built on `BubbleRow`), `Avatars.tsx` (`UserAvatar`), `useScreenReader.ts` with a `.web.ts` variant.

## Runtime or data flow

Verified in `ChatView.tsx`:

1. `ChatView` calls `markEntered` for the rows on screen at mount. It then calls `replyReveal.schedule(revealRows(messages), seen, now)`.
2. `renderItem` passes each row's `text`, `keywordsFor(entryId)`, `sources`, `media`, `revealId`, `entryId`, and latency `meta` to `ChatBubble`.
3. `ChatBubble` builds `replyDoc(text, keywords)`. That call strips citation markers, bolds keywords, and parses Markdown. The bubble then shows `sliceDoc` up to the revealed word count. The gallery, `meta`, and sources badge appear only after the text has fully typed out.
4. The sources badge calls `onOpenSources`. `ChatView` holds one `SourcesSheet` per screen.

`mobile/src/state/messageSources.ts` builds `ChatSource[]` from citation ids. Reduced motion or a screen reader shows the whole reply at once.

## Tests

`mobile/src/ui/chat/__tests__/` has one file per module except `TypingBubble`, `Avatars`, and `useScreenReader`. `mobile/src/chat/__tests__/ChatView.test.tsx` covers reveal order across rows. The runner is `jest` with the `jest-expo` preset.

## Common change paths

- Bubble look or footer: edit `BubbleRow` styles. Keep `ROW_PADDING`, `COLUMN_SHARE`, and `BUBBLE_PADDING` in sync with `predictedGalleryWidth`.
- Typing speed: edit `WORDS_PER_SECOND` or `CHUNK_MS` in `reveal.ts`.
- New citation syntax: edit `MARKER` and `PARTIAL` in `citations.ts`.
- New composer prop: add it to `ChatComposerProps`, then pass it from `ChatView` and `ComposerLab`.

Gap: this page describes uncommitted working-tree versions of `ChatBubble.tsx`, `ChatComposer.tsx`, and `MediaGallery.tsx`.

## Related docs

- [System map](../../system-map.md)
- [Architecture](../../architecture.md)
- [App design skill](../../../.claude/skills/app-design/SKILL.md)
