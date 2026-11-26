---
name: app-design
description: Visual design system of the Nevados app in mobile/ (colors, Manrope body and Bricolage Grotesque heading scale, custom components, the Pet mascot, onboarding art direction). Use before creating, restyling or reviewing any screen, component, color, font, icon or illustration in mobile/. It lists the only tokens and components that exist; do not invent others.
---

# App design system

The values live in code. This skill tells you where. Read the files; never type a color, font
or size from memory.

## Sources of truth

| What | Where |
|---|---|
| Brand colors, fonts, type scale, spacing, radius | `mobile/src/ui/theme/tokens.ts` |
| Font files (Manrope and Bricolage Grotesque, static instances, OFL) | `mobile/assets/fonts/`, mapped in `mobile/src/ui/theme/fonts.ts`, loaded in `mobile/app/_layout.tsx` |
| Art direction (palette, light, composition, card) | `reference/onboarding.png` and `reference/chat.png` in this folder |
| Live catalog of everything below | route `/design` (web: `http://localhost:8081/design`) |
| Onboarding illustration palette | `mobile/src/onboarding/scene/preset.ts` (`DEFAULT_PALETTE`), edited in the Lab (`/lab`) |

## Components (use these before writing new ones)

| Component | File | Use | Props |
|---|---|---|---|
| `CloudCard` | `src/ui/CloudCard.tsx` | Bottom panel whose top edge (`CLOUD_EDGE` pt tall) is vapor drawn like the Pet: puffs with a solid centre and a soft rim billow over the card body, never hard lobes. It overlaps the art above it | `width`, `height`, `children` |
| `Icon` | `src/ui/icons/Icon.tsx` | Local Lucide outline glyphs, ISC licensed | `name`, `size`, `color`, `strokeWidth` |
| `PrimaryButton` | `src/ui/PrimaryButton.tsx` | The main action: ink surface with a defined edge, label and Lucide direction icon | `label`, `onPress`, `chevron?` |
| `PageDots` | `src/ui/PageDots.tsx` | Step indicator; `position` may be fractional while pages slide | `count`, `position`, `onSelect?` |
| `ParkEmblem` | `src/ui/ParkEmblem.tsx` | The park's emblem (raster badge, 1x/2x/3x PNGs in `assets/images`); tops the onboarding card, resting on its solid body | `size?` |
| `Pet` | `src/ui/pet/Pet.tsx` | The mascot, animated | see below |
| `ChatBubble`, `TypingBubble` | `src/ui/chat/` | A message surface with a small concave foot, no avatar or diffuse shadow. User ink, assistant soft teal. Entry (280 ms, 4 pt rise, ease-out) uses native opacity/translation once per mount and respects reduced motion. Hides an assistant's `[fuente: ID]` markers (`citations.ts`); with sources, a 28 pt book ring in a 44 pt target sits beside its bottom corner. Assistant text is a Markdown subset (`markdown.ts`: paragraphs, `- `/`1. ` items, `**bold**` in `fonts.bold`) with the entry's keywords (`keywords.ts`, `assets/data/knowledge-keywords.json`) in bold, typed out word by word from `reveal.ts` (keyed by row id, one frame loop; meta and the source ring appear when it ends; whole at once under reduced motion or a screen reader) | `role`, `text`, `meta?`, `sources?`, `onOpenSources?`, `keywords?`, `revealId?` |
| `SourcesSheet` | `src/ui/chat/SourcesSheet.tsx` | One per screen: lists an answer's sources (title, passage or retrieval date, web link). Scrim, close button and Android back close it | `sources`, `onClose`, `bottom?`, `reducedMotion?` |
| `UserAvatar` | `src/ui/chat/Avatars.tsx` | Teal circle with a person glyph | `size` |
| `PetCircle` | `src/chat/PetCircle.tsx` | The animated vapor Pet in its teal circle on the chat sheet's edge; thinking while busy, talking while a reply arrives; green dot when the model is ready; looks at the last typed character (`gaze`, fed by the composer's `onCaret`) | `x`, `y`, `r`, `voice`, `ready`, `gaze?` |
| `ChatComposer`, `ChatMenu` | `src/ui/chat/` | Input with floating and docked variants; docked joins the bottom base with concave shoulders. Owns its draft and reports empty/non-empty transitions and (docked, `onCaret`) the window point of the last typed character. With the keyboard open the chat lifts the composer above it and the vapor sheet, circle and list rise over the ranges (`chatLayout.keyboardLift`) and (docked) the caret's window point; the "more" button and its menu. With the keyboard open the chat lifts the composer above it and the vapor sheet rises over the ranges (`chatLayout.keyboardLift`) | see props |
| `Chip`, `DebugPanel` | `src/ui/` | Settings and debug view (still on the legacy `useColors()` light/dark palette) | — |
| `MediaRowList` | `src/ui/MediaRowList.tsx` | Scroll list of `{ image, title, description }`; even index image left, odd image right. One Card, `flexDirection` only | `items`, `ListHeaderComponent?`, `ListFooterComponent?`, `contentContainerStyle?` |

A new component goes in `src/ui/`, gets a row in this table and a sample on `/design`.

## Pet

The character is called `PET_NAME` (`src/ui/pet/petCore.ts`); the name is provisional, so never
hard-code it. Never redraw the Pet's geometry or face: they are ported from its own lab
(fleibo-face), and `petCore.ts` is the asset. It has one look, vapor (the user made it permanent
on 2026-11-22; the old glossy figure was deleted):

| Component | Where | Colors |
|---|---|---|
| `Pet` (animated, draws `PetVaporCanvas`: Skia on native, a 2D canvas (`drawPetCanvas2d`) on web) | the chat's circle (`PetCircle`), `/design` | `fill`/`shade` props; default `brand.card`/`brand.cardShade`, the chat circle passes the scene's mist colors |
| one frame from `petFrame()` (`drawPet` on Skia, `drawPetCanvas2d` on the web canvas, `PetVaporFigure` in the SVG reference) | inside the onboarding scene, rising out of the crater | the scene's mist colors (`PetBody.fill`/`shade`, default `$mist`/`$cloudShade`) |

The vapor look draws the same body and face, solid and defined, with a soft halo of puffs
(`petVaporPuffs`) behind the outline so the vapor reads as part of the body (never puffs on top
of it), and a tail that thins out where it leaves the crater. No filters, masks or clips.
The scene has no separate steam plume: the Pet is the crater's vapor.

```tsx
import { Pet } from '@/ui/pet/Pet';

<Pet size={180} emotion="idle" voice="idle" audioLevel={0} />
<Pet size={180} emotion="speaking" voice="speaking" audioLevel={0.65} />
```

- `emotion`: one of `PET_EMOTIONS` (idle, happy, curious, surprised, thinking, listening,
  speaking, sleepy, sad, excited, default-happy, intimidated, angry).
- `voice`: one of `VOICE_STATES` (idle, listening, thinking, speaking). `audioLevel` 0..1 moves
  the speaking mouth.
- `lookAt` (a window point it holds its gaze on, e.g. the last typed character; turning left
  mirrors in place about the body's center), `paused`, `reducedMotion` (the system setting also applies), `trackPointer` (web only),
  `lookAround` (default on: glances around on its own when the pointer rests or on touch
  screens), `crop` (part of the Pet to show, in Pet units).
- Inside a scene, draw one frame from `petFrame()`: `drawPet` in the Skia renderer
  (`SceneCanvas.native.tsx`), `drawPetCanvas2d` in the web one (`SceneCanvas.tsx`),
  `PetVaporFigure` in the SVG reference (`NevadoScene`: Lab, export). All read the same frame, so
  change the look in `petCore.ts` and keep the three drawers in step.
- Emotion changes always morph with the Pet's own (fleibo-face) transition: `motion.transition`
  ms with `motion.easing`, from the face on screen. `Pet` does it in its engine; a host drawing
  single frames uses `useFaceTransition` (every scene renderer does). Never switch poses
  directly, and show a chat moment as an emotion (`PetCircle`: happy, thinking, speaking), not
  only a voice state, since the voice alone just swaps the mouth.

## Rules

1. Colors come from `brand.*` in `tokens.ts` (chat screens: `useColors()`). No hex or `rgb()` in
   UI files: `src/ui/__tests__/design-guard.test.ts` fails on them.
2. Text uses Manrope and Bricolage Grotesque through `type.*` (spread the style, then set `color`) or `fonts.*`. Never set
   `fontWeight`: Android ignores it for bundled fonts, so the weight is the family name. The guard
   test enforces both.
3. Text on the card: titles `brand.ink`, body `brand.inkMuted`. On `primary`: `brand.onPrimary`.
   `primarySoft` and `cardShade` are decoration, never text. The components are teal (#5E9999,
   the park emblem's ring, and shades of it), not the reference's violet: the user's call. White
   on that teal is 3.2:1, below AA for the 16 px label; the user accepted it for the exact color.
   The scene keeps its lavender sky. `online` (green) is only the ready dot on the Pet's circle.
4. UI gradients, icons and shapes are drawn with `react-native-svg`. The onboarding scene, the
   chat header scene and the Pet draw with `@shopify/react-native-skia` on native and on 2D
   canvases on web (the scene one canvas per layer, layer blur and opacity in CSS). The SVG
   renderer (`NevadoScene`, `PetVaporFigure`) is the reference look and what the Lab and export
   use (`mobile/README.md`, "Onboarding scene"). There is no icon or gradient package; do not add
   one.
5. Illustration colors (sky, volcano, páramo, frailejones, lupines) belong to the scene palette,
   not to the tokens. The look is the reference: lavender dusk sky with a golden horizon,
   blue-violet ranges, white snow with lavender shadows, green-gold páramo, frailejones, purple
   lupines and yellow flowers. The chat header alone repaints its ranges in natural earth browns
   derived from the scene palette (`src/chat/headerPeaks.ts`); the user's call on 2026-11-22.
6. Touch targets are at least 44 pt (use `hitSlop` on small controls). Buttons set
   `accessibilityRole` and a label; step dots are `tab`s named by `t.pageDot` ("Paso N de M").
7. Copy comes from `src/i18n` (`t.<key>`, `fill()` for `{placeholders}`), never from literals in
   UI files; the guard test enforces it. New text = a key in `es.ts` and in every other locale.
   Onboarding copy leads with the park; the Pet is the guide, not the product.
8. Respect reduced motion (`useReducedMotion` in `src/ui/useReducedMotion.ts`): no idle loops and
   instant page changes.

## Not decided yet (do not invent)

- A dark variant of the brand palette.
- The remaining legacy settings/history screens' migration from `useColors()` to `brand` and the bundled font families.
- Additional icon glyphs: extend the local Lucide family in `src/ui/icons/Icon.tsx`; keep its ISC license.

## Verify a UI change

1. `cd mobile && npx jest src/ui` (design guard) and `npx tsc --noEmit`.
2. Run `npx expo start --web --port 8081`, then open `/design` and the screen you changed at
   390x844 and 820x1180 (Playwright screenshots). Compare against `reference/onboarding.png`.
