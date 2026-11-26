# Group sync transport

## Purpose

The **Grupo** tab keeps a guided group together over Bluetooth LE beacons, with NFC tap pairing. This page maps the transport layer. The reducer and wire format in `mobile/src/core/group/` are out of scope.

## Start here

- `mobile/src/group/transport.ts`: the `GroupTransport` interface, the seam between the reducer and the radio.
- `mobile/src/group/bleTransport.ts`: `createBleTransport(radio)` and `ensureRadioPermissions()`.
- `mobile/src/group/useGroup.ts`: `useGroup(transport, self, syncing, alertMeters)` feeds transport events into `step()` from `@/core/group/groupState`.
- `mobile/src/group/session.ts`: the `Session` union (`choosing`, `guide`, `visitor`), `guideSession()`, and `visitorSession()`.
- `mobile/app/(tabs)/group.tsx`: `GroupRoute` picks the transport. UI parts live in `mobile/src/ui/group/`.

## Runtime or data flow

1. `GroupRoute` uses `createBleTransport(GroupRadio)` when the native module loads. On web it falls back to `createWebPreviewSim()`, and otherwise to `IDLE_TRANSPORT`.
2. `mobile/modules/group-radio/index.ts` loads `GroupRadio` with `requireOptionalNativeModule`. The value is null on web and on builds without the module. `expo-module.config.json` lists Android only.
3. `start()` calls `radio.start(payloadHex, true, true)`. `GroupRadioModule.kt` then starts `GroupRadioService.kt` as a foreground service.
4. The service advertises manufacturer data under company id `0xFFFF` with the magic prefix `NV`. It scans for the same prefix and emits `onSighting`. It also emits `onTick` every 1000 ms (`TICK_EVERY_MS`).
5. `bleTransport.ts` decodes each frame with `decodeBeacon` and emits `joined`, `sighting`, and `tick` inputs. It sets `nativeTicks: true`, so `useGroup` starts no JS interval.
6. For NFC pairing, the guide calls `setNfcCard`. `GroupNfcCardService.kt` answers a SELECT of AID `F04E45564752`. The visitor runs `startNfcReader`, and `GroupNfcReader.kt` emits `onNfcCard`, which `decodePairing` parses.

Code comments claim that native ticks and `radio.alert` work with the screen off. No test listed below proves it.

## Tests

- `mobile/src/group/__tests__/bleTransport.test.ts` drives a `FakeRadio`. It covers pairing range, sync mode, NFC pairing, alert distance, and discovery abort.
- `mobile/src/group/__tests__/useGroup.test.tsx` covers how the alert distance reaches the radio.
- `mobile/src/ui/group/__tests__/groupScreen.test.tsx` mocks `group-radio` and `bleTransport`.

The Kotlin code has no tests. `mobile/app/radio-spike.tsx` is a manual probe that logs to logcat tag `GroupRadio`.

## Common change paths

- To change beacon bytes, edit `mobile/src/core/group/wire.ts`. The native payload limit is 22 bytes after the magic prefix.
- To add a native call, update `GroupRadioModule` in `index.ts`, the `Function(...)` in `GroupRadioModule.kt`, and `FakeRadio` in `bleTransport.test.ts`.
- `webPreviewSim.ts` is marked temporary, to remove before shipping.

## Related docs

- [Docs index](../../README.md)
- [System map](../../system-map.md)
