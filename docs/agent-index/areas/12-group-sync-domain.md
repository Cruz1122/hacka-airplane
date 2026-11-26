# Group sync domain

## Purpose

`mobile/src/core/group/` is the pure TypeScript core of group sync, with no React and no radio code. The BLE and NFC wiring lives in `mobile/src/group/`.

## Start here

- [`types.ts`](../../../mobile/src/core/group/types.ts): `MemberId` (branded, made only by `memberId()`), `Member` (guide or visitor), `LinkEvent`, `Presence`, and `Alert`.
- [`groupState.ts`](../../../mobile/src/core/group/groupState.ts): `GroupState`, the reducer `step()`, and the selectors `presence()`, `alerts()`, and `alertMetersOf()`.
- [`signal.ts`](../../../mobile/src/core/group/signal.ts): `observe()` filters one edge with a median, an EMA, hysteresis, and a pocket dwell.
- [`policy.ts`](../../../mobile/src/core/group/policy.ts): `GROUP_POLICY` holds every threshold. Its comment marks the values as uncalibrated.
- [`wire.ts`](../../../mobile/src/core/group/wire.ts): the 22-byte beacon codec, the NFC pairing record, and the short id mapping.
- [`lane.ts`](../../../mobile/src/core/group/lane.ts): `lane()` places each visitor dot at `t` in [0, 1].

## Runtime or data flow

1. `src/group/bleTransport.ts` decodes beacons and emits `GroupInput` events through `GroupTransport` in `src/group/transport.ts`.
2. `src/group/useGroup.ts` folds each event with `step()` and calls `alerts()`.
3. `app/(tabs)/group.tsx` and `src/design/GroupLab.tsx` call `lane()`.

Only `tick` events advance `nowMs`. Edges are keyed `observer\nsubject`, and `left` drops every edge of that member. `alerts()` returns nothing on a visitor phone. "Unseen" is its own `Presence` kind, never `far`.

The live working tree has uncommitted changes that set beacon and pairing version 3 with a `look` byte. Committed HEAD `45a394d5` writes version 2. Both decode older versions. A changed byte offset needs a version bump and a decode branch. `MemberAccessory` and `MemberTint` mirror `PET_ACCESSORIES` and `PET_TINTS` in `src/ui/pet/petCore.ts`. Inference: reordering them changes what peers decode.

## Tests

- `__tests__/wire.test.ts`: round trips, UTF-8 truncation, malformed input, and old versions.
- `__tests__/groupState.test.ts`: pocket dips, zones, two-guide alerts, and alert distance.
- `__tests__/lane.test.ts`: dot placement with one or two guides.
- [`testing.ts`](../../../mobile/src/core/group/testing.ts): the `run()` scenario driver, imported only by tests.

Run `npm test` in `mobile/` (preset `jest-expo`).

## Common change paths

- Threshold: edit `GROUP_POLICY`, then rerun `groupState.test.ts` and `lane.test.ts`.
- Beacon field: edit `wire.ts`, bump the version, keep the old decode branch, and extend `wire.test.ts`.
- `Member` field: edit `types.ts`, `memberFromBeacon()`, and the self members in `src/group/session.ts`.

## Related docs

- The [mobile README](../../../mobile/README.md) maps `src/core/group/` and `src/group/`.
