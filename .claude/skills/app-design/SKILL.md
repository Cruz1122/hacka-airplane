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
| `SecondaryButton` | `src/ui/SecondaryButton.tsx` | The quieter action beside the main content ("Cancelar" on the guide's empty Grupo): `card` surface, 1.5 pt ink edge, ink label, 44 pt tall, `cardShade` while pressed | `label`, `onPress`, `hint?` |
| `Slider` | `src/ui/Slider.tsx` | A horizontal value on steps (no slider package; `react-native-gesture-handler` v3 `usePanGesture` + a Reanimated shared value, inside its own `GestureHandlerRootView`). 8 pt track; with `split` it reads near (`primary`, up to `split` of the value), mid (`primarySoft`, up to the thumb) and beyond (`wineSoft`); without it `primarySoft` fill on `cardShade`. 28 pt `card` knob with a 3 pt ink edge and `glow`, in a 44 pt target. Follows the finger, settles on the nearest step, `onChange` once per step; horizontal drags only, vertical ones stay with the scroll. `accessibilityRole="adjustable"` with increment/decrement. No haptics | `value`, `min`, `max`, `step`, `onChange`, `label`, `valueText`, `hint?`, `split?` |
| `PageDots` | `src/ui/PageDots.tsx` | Step indicator; `position` may be fractional while pages slide | `count`, `position`, `onSelect?` |
| `ParkEmblem` | `src/ui/ParkEmblem.tsx` | The park's emblem (raster badge, 1x/2x/3x PNGs in `assets/images`); tops the onboarding card, resting on its solid body | `size?` |
| `Pet` | `src/ui/pet/Pet.tsx` | The mascot, animated | see below |
| `ChatBubble`, `TypingBubble` | `src/ui/chat/` | A message surface with a small concave foot, no avatar or diffuse shadow. User ink, assistant soft teal. Entry (280 ms, 4 pt rise, ease-out) uses native opacity/translation once per mount and respects reduced motion. Hides an assistant's `[fuente: ID]` markers (`citations.ts`); with sources, a 28 pt book ring in a 44 pt target sits beside its bottom corner. Assistant text is a Markdown subset (`markdown.ts`: paragraphs, `- `/`1. ` items, `**bold**` in `fonts.bold`) with the entry's keywords (`keywords.ts`, `assets/data/knowledge-keywords.json`) in bold, typed out word by word from `reveal.ts` (keyed by row id, one frame loop; meta and the source ring appear when it ends; whole at once under reduced motion or a screen reader). A `verified` answer (from the UTON guion) shows a "Verificado por UTON" seal in its footer before the latency: `primary` `circleCheck` + `ink` semibold 12 pt caption, one accessible label (`t.chatScreen.verified.label`) | `role`, `text`, `meta?`, `sources?`, `onOpenSources?`, `keywords?`, `revealId?`, `verified?` |
| `SourcesSheet` | `src/ui/chat/SourcesSheet.tsx` | One per screen: lists an answer's sources (title, passage or retrieval date, web link). Scrim, close button and Android back close it | `sources`, `onClose`, `bottom?`, `reducedMotion?` |
| `MediaGallery` | `src/ui/chat/MediaGallery.tsx` | Photos under an answer about a species or place, inside its `ChatBubble` (`media` prop; picked once per reply by `src/core/media`): a bubble with photos takes its full max width and the gallery spans it: `single` (full-width photo, 1.1× height, ≤360 pt), `rows` (104 pt square thumbnails, `primarySoft` hairlines) or `columns` (cards share the width, never scroll or clip; under 100 pt per card they fall back to `rows`). Caption "Común (*Científico*)" (italic via `fontStyle`; no italic family). Credit is a pill on the photo's bottom-left corner: `brand.photoScrim` background, white SVG licence glyph (cc / public domain) + short author in bold, one line; the full licence is only in its a11y label `t.chatScreen.media.credit`. Laid out from the bubble's first frame; after the text, cards rise in (90 ms stagger, native driver) and captions type out as the `<id>:media` reveal stream (`revealRows`); whole at once when read before, under reduced motion or a screen reader. No fullscreen | `media`, `revealId?` |
| `UserAvatar` | `src/ui/chat/Avatars.tsx` | Teal circle with a person glyph | `size` |
| `PetCircle` | `src/chat/PetCircle.tsx` | The animated vapor Pet in its teal circle on the chat sheet's edge; thinking while busy, talking while a reply arrives; green dot when the model is ready; looks at the last typed character (`gaze`, fed by the composer's `onCaret`) | `x`, `y`, `r`, `voice`, `ready`, `gaze?` |
| `ChatComposer` | `src/ui/chat/ChatComposer.tsx` | Input with floating and docked variants; docked joins the bottom base with concave shoulders and (with `onNewChat`) has a 44 pt pen button left of the field that starts a new conversation. Owns its draft and reports empty/non-empty transitions and (docked, `onCaret`) the window point of the last typed character. With the keyboard open the chat lifts the composer above it and the vapor sheet, circle and list rise over the ranges (`chatLayout.keyboardLift`) | see props |
| `CloudNavBar`, `AppNavBar` | `src/ui/CloudNavBar.tsx`, `src/ui/AppNavBar.tsx` | The top navigation over the chat and Grupo: a solid `card` pill with a crisp 1 pt `cardShade` edge and a soft `glow` shadow, with three small solid puffs rising from its top edge (puffs and pill are one outlined shape; no blur, halo or soft rim). Three `tab`s, Chat, Grupo and Recorrido; the active one is a plain `primary` pill, pressed a `cardShade` pill. `CloudNavBar` is router-free; `AppNavBar` places it under the safe area and switches tabs in the `app/(tabs)` navigator (`navigate` with `merge`, so tab params survive). Each tab screen draws its own bar; the chat fades it out while the keyboard lifts the sheet | `active`, `onSelect`, `top`, `screenWidth` / `active` |
| `GroupLane`, `PetDot`, `ZoneLegend` | `src/ui/group/GroupLane.tsx` | The guide's group line: with one guide the line is meters from the guide (0 to 1.5× the alert distance, `lane.scale`), with a dashed `brand.alert` line at 2/3 and a dotted `cardShade` line at the near boundary ("15 m"); when `alertMeters` + `onAlertMetersChange` are passed, the dashed alert line carries an inline draggable `- 30 m +` pill (or a compact inline footer pill on a two-guide lane) instead of a separate card. Guides at the ends and one 56 pt marker per visitor ON the line, ordered by `t` and spread along it (`laneLayout.ts`). Each `PetDot` floats that member's still Pet (wearing the skin sent over BLE/NFC v3) on a soft teal disc separated by a white gap from an outer zone ring (near solid `primary`, mid double, far dashed `alert`, unseen dotted `inkMuted` with a scaled crossed-eye badge; guides get an `ink` outer ring). `ZoneLegend` is a balanced 2×2 grid of crisp 18 pt vector ring swatches (no Pet circles). `laneHeightFor(n, twoGuides)` fits n markers at full spacing | `lane`, `selfId`, `selfWears?`, `alertMeters?`, `onAlertMetersChange?`, `width`, `height` |
| `PetCustomizer` | `src/ui/PetCustomizer.tsx` | One role's Pet options, opened under its `RoleCard` by the pencil: "Tu Pet de guía/visitante", the accessory tiles (Pet heads wearing each) and color swatches (radios), "Listo" closes. No avatar of its own: the card above shows the result live | `role`, `look`, `onChange`, `onDone` |
| `RoleCard` | `src/ui/group/RoleCard.tsx` | One of the two role choices on `/group`, stacked; each takes its share of the height left under the name field (`flex: 1`, at least `ROLE_CARD_MIN`), sits on `brand.card` with `brand.glow` and a calm pulsing `brand.primary` halo around the edge so it reads as pressable, and centres the role's own Pet (as dressed) above its `brand.ink` title and a subtle `brand.primary` chevron. Spring press/selection feedback (still/instant under reduced motion). The card picks the role; the 36 pt ink pencil badge on the circle (a sibling of the card's button, not nested) opens that Pet's options and turns into a check while open | `label`, `hint?`, `wears`, `onPress`, `width`, `onEdit?`, `editLabel?`, `editing?`, `selected?`, `dimmed?`, `pulseDelay?`, `disabled?` |
| `RoleChoices` | `src/ui/group/RoleChoices.tsx` | Both `RoleCard`s, filling the height they are given, with one `PetCustomizer` open at a time under its card. Looks are per role (`src/state/petLook.ts`: `usePetLooks()`, `setPetLook(role, patch)`, `wornBy(look, role)`, `memberLookOf(look, role)`, `wornFromMember(look, role)`; kv-store `petLook.v2`; by default each role wears its own hat) and broadcast over the v3 BLE beacon and NFC pairing record so other phones render each member's skin | `looks`, `onLookChange`, `onChoose`, `width`, `disabled?`, `selected?`, `editing?`, `onEditingChange?` |
| `SignalPulse` | `src/ui/group/SignalPulse.tsx` | The visitor's "bring your phone close" glyph: a broadcast dot and three arcs (SVG) lighting up outward in sequence (opacity only, continuous loop on native and web); still and fully lit under reduced motion | `size?` (160) |
| `EmptyLane` | `src/ui/group/EmptyLane.tsx` | The guide's screen before anyone joins, centred under the bar (not in a card): the guide's own Pet (as dressed) in a teal circle with three staggered rings (`cardShade` disc, `primary` edge) expanding out of it on the native driver, two still halos under reduced motion; "Aún no hay visitantes", how visitors join (phone to phone) and, with `onCancel`, a `SecondaryButton` "Cancelar" back to the role chooser | `wears`, `onCancel?` |
| `GroupAlertBanner` | `src/ui/group/GroupAlertBanner.tsx` | The guide's alert: first alert named on a `brand.alert` surface with `onPrimary` text, warning glyph pulsing unless reduced motion, "y N avisos más" | `alerts`, `nameOf` |
| `Chip`, `DebugPanel` | `src/ui/` | Settings and debug view (still on the legacy `useColors()` light/dark palette) | — |
| `BottomSheet` | `src/ui/BottomSheet.tsx` | Shared overlay bottom sheet (scrim, 28 pt top corners, 560 pt max width, grab handle, native slide/fade or instant under reduced motion, Android back handler) used by the top-bar panels | `open`, `onClose`, `onHardwareBack?`, `bottom?`, `reducedMotion?`, `children` |
| `AccessibilitySheet` | `src/ui/AccessibilitySheet.tsx` | Accessibility overlay opened from `CloudNavBar`'s left side button: text size (`Slider` + `-`/`+` + level pills + live park preview), outdoor high contrast toggle, reduce motion toggle (with device-setting notice), and color-vision radio cards (`none`, `protanopia`, `deuteranopia`, `tritanopia`) with live swatches and icon+text status strip; persisted in `src/state/accessibility.ts` | `open`, `onClose`, `bottom?`, `reducedMotion?` |
| `SettingsSheet` | `src/ui/SettingsSheet.tsx` | Settings overlay opened from `CloudNavBar`'s right side button: root menu with **Fuentes guardadas** (reads `src/state/favoriteSources.ts`, inline Undo on remove, web link launch), the **Solo información verificada por UTON** switch (`SwitchRow` from `AccessibilitySheet` in a menu card; `src/state/verifiedOnly.ts`) and **Acerca de** (`ParkEmblem`, version, offline/sources/credits info cards) | `open`, `onClose`, `bottom?`, `reducedMotion?`, `initialView?` |
| `PhotoCredit` | `src/ui/PhotoCredit.tsx` | A photo's credit on its corner, the chat's style: camera glyph + author in bold on a `brand.photoScrim` pill, one line; licence only in the a11y label; links to the photo's source when given `url`. Used by `MediaGallery`, `MediaRowList` and the trail's station sheet; place it absolutely at `PHOTO_CREDIT_INSET` | `author`, `license`, `url?`, `maxWidth?` |
| `InfoCard` | `src/ui/InfoCard.tsx` | A titled card with a 40 pt glyph tile (`cardShade`, or `primary` with `tone="done"`), the settings info-card look: scan results, Bluetooth receive states, the locked-station notice. Actions go in `children` under the text | `icon`, `title`, `body?`, `tone?`, `children?` |
| `ScanFrame` | `src/ui/ScanFrame.tsx` | `onPrimary` corner brackets over a camera preview (`QrCamera`, native and web) | — |
| `Greeting` | `src/ui/chat/Greeting.tsx` | The chat's first message (chat and station sheet). While the chat is locked it adds the station-QR request and a `PrimaryButton` inside the bubble (`ChatBubble` `action`) | `locked?`, `onScan?` |
| `MediaRowList` | `src/ui/MediaRowList.tsx` | Trail station pages: list of `{ image, subtitle, description }` with a `PhotoCredit` on the photo; even index image left, odd right (web floats the photo). `**bold**` in the body | `items`, `ListHeaderComponent?`, `ListFooterComponent?`, `contentContainerStyle?` |

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
- `accessory` (`PET_ACCESSORIES`: `guideHat` ranger hat, `visitorCap`, `beanie` wool hat,
  `bandana`, `flower` frailejón flower) and `tint` (`PET_TINTS`: ink, sky, sun, lupine; each
  accessory has its own default, `defaultTint`): worn on the head, from one geometry in
  `petCore.ts` (`ACCESSORY_SHAPES`, Pet units, shapes toned main/accent/light and resolved to
  `brand.*`), drawn by all three drawers (`drawPet` Skia, `drawPetCanvas2d` web canvas,
  `PetVaporFigure` SVG). Hats sit low and wide enough to wrap the head (measured on its
  outline), with no outlines: shaded like the Pet, brims casting a soft `cardShade` on the head.
  They ride the body's rotation and float, tip with the float's speed and lean with the gaze,
  and mirror without collapsing. No teal tint: the Pet always sits on a teal circle. With an
  accessory the default crop is `PET_ACCESSORY_VIEWBOX` (room for the crown).
- `PetStill` (`src/ui/pet/PetStill.tsx`): one still frame (no idle loop, blink or gaze) for places
  that show many Pets, like the lane dots; an emotion change still morphs (`useFaceTransition`).
  Props `size`, `emotion`, `accessory?`, `crop?`.
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
   `alert` (red) is only for the group module's alert states (a visitor far or lost, the other
   guide lost): alerting lane dots, the alert banner, the visitor's "drifting / no signal" state.
   Text on it is `onPrimary`. Zones never rely on it alone: shape, icon and pulse carry them too.
   `wine` (vinotinto) and `wineSoft` are only for the visitor's error states ("te estás alejando",
   "sin señal"): `wineSoft` washes the whole screen (fading in 300 ms unless reduced motion),
   `wine` is the title and warning glyph (9.0:1 on `wineSoft`). Body text there is `ink` (7.8:1);
   `inkMuted` is only 4.3:1 on `wineSoft`. `sun` and `lupine` are Pet accessory tints only.
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
