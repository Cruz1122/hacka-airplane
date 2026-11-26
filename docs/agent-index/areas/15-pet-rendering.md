# Pet rendering

## Purpose

Map of the Pet mascot in `mobile/`: geometry, renderers, the stored look (accessory and tint), and how screens pass it to the Pet. `memberLookOf`, `wornFromMember`, `PET_FACE_VIEWBOX`, and the `hidden` prop of `PetCircle` come from uncommitted changes, not commit `45a394d5`.

## Start here

- `mobile/src/ui/pet/petCore.ts` holds geometry with no React: `PET_PRESET`, `petFrame()`, `transitionFace()`, `PET_ACCESSORIES`, `PET_TINTS`, `defaultTint()`, and the `PET_*_VIEWBOX` crops.
- `mobile/src/ui/pet/Pet.tsx` is the animated Pet. `frameLoop.ts` decides when its loop draws.
- `PetStill.tsx` draws one frame with no loop and morphs emotions through `useFaceTransition.ts`.
- `PetVaporCanvas.tsx` paints web through `drawPetCanvas2d.ts`. `PetVaporCanvas.native.tsx` uses Skia through `drawPet.ts`. Both copy the SVG reference `PetVaporFigure.tsx`.
- `mobile/src/state/petLook.ts` stores one `PetLook` per role (`guide`, `visitor`) under the kv-store key `petLook.v2`. It exposes `usePetLooks()` and `setPetLook()`.

## Runtime or data flow

1. `PetCustomizer.tsx`, opened from `RoleChoices.tsx`, edits a look. `app/(tabs)/group.tsx` wires `onLookChange={setPetLook}`.
2. `wornBy(look, role)` turns the `'role'` and `'none'` choices into a concrete `accessory` and `tint`.
3. `Pet` and `PetStill` take `accessory` and `tint` props. `Pet.tsx` copies them into the frame config as `accessory` and `accessoryTint`, then `petFrame()` draws the accessory.
4. For other phones, `memberLookOf()` encodes the look as a `MemberLook` (`mobile/src/core/group/types.ts`). `wornFromMember()` decodes a peer's look for `GroupLane.tsx`.

The knowledge chat does not use the stored look. This is verified in the source. `ChatView.tsx` renders `PetCircle` with `voice`, `ready`, `loading`, `hidden`, and `gaze`. `PetCircle` passes `Pet` no `accessory` or `tint`, only the scene mist colors and a crop. Its face comes from `usePetVoice()`, mapped through the `EMOTION` table in `PetCircle.tsx`.

## Tests

- `mobile/src/ui/pet/__tests__/` has `pet.test.ts` (geometry, accessory placement), `Pet.test.tsx` (loop), `frameLoop.test.ts`, `useFaceTransition.test.tsx`, `drawPetCanvas2d.test.ts`, and the `pet.bench.test.tsx` benchmark.
- `mobile/src/state/__tests__/petLook.test.ts` covers `parsePetLooks` and `wornBy`. No test calls `memberLookOf` or `wornFromMember`.
- `mobile/src/chat/__tests__/PetCircle.test.tsx` covers pausing out of focus and the loading badge.

## Common change paths

- To add an accessory or tint, edit `PET_ACCESSORIES`, `PET_TINTS`, and `ACCESSORY_SHAPES` in `petCore.ts`. `petLook.ts` validates stored values against those lists.
- To change a drawing, change all three drawers: `PetVaporFigure.tsx`, `drawPet.ts`, and `drawPetCanvas2d.ts`.
- To show the stored look in the chat, read `usePetLooks()` and pass `wornBy()` output through `PetCircle` to `Pet`. No code does this today.

## Related docs

- [App design skill, Pet section](../../../.claude/skills/app-design/SKILL.md)
- [Architecture, onboarding and rendering](../../architecture.md)
