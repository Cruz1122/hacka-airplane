// Real BLE beacon transport backed by the local `GroupRadio` Android foreground service.
// Every phone broadcasts a 22-byte beacon and scans simultaneously:
// - Guides broadcast their groupId + syncing flag and admit visitors in the same group while sync
//   mode is on; once admitted, visitors stay tracked across range drops even with sync mode off.
// - Visitors start unpaired (groupId = 0) and pair by tapping the guide's phone: the guide's NFC
//   card hands over the groupId and guide id. A visitor without NFC, or facing a guide whose beacon
//   says its card is down, pairs with the first syncing guide heard within touching range
//   (>= GROUP_POLICY.pairMinDbm) instead. Paired visitors broadcast that groupId + echoed guide
//   RSSIs so a two-guide lane can position them between both ends.
// - A guide's beacon and NFC card carry its alert distance; a phone that sees a known guide's
//   distance change re-emits `joined` for that guide with the new value.
import { PermissionsAndroid, Platform } from 'react-native';

import { GROUP_POLICY } from '@/core/group/policy';
import { memberId, type GuideMember, type Member, type MemberId } from '@/core/group/types';
import {
  clampAlertMeters,
  decodeBeacon,
  decodePairing,
  encodeBeacon,
  encodePairing,
  memberFromBeacon,
  memberIdToShortId,
  shortIdToMemberId,
  withAlertMeters,
  type BeaconFrame,
} from '@/core/group/wire';

import type { GroupRadioModule } from '../../modules/group-radio';
import type { GroupTransport } from './transport';

const DISCOVERY_MS = 1500;
const ECHO_MIN_INTERVAL_MS = 2000;
const ECHO_MIN_DELTA_DB = 3;

export type RadioPermissionState = 'granted' | 'denied';

export async function ensureRadioPermissions(): Promise<RadioPermissionState> {
  if (Platform.OS !== 'android') return 'denied';
  const P = PermissionsAndroid.PERMISSIONS;
  const required =
    Number(Platform.Version) >= 31
      ? [P.BLUETOOTH_SCAN, P.BLUETOOTH_ADVERTISE, P.BLUETOOTH_CONNECT]
      : [P.ACCESS_FINE_LOCATION];
  const optional =
    Number(Platform.Version) >= 33 && P.POST_NOTIFICATIONS ? [P.POST_NOTIFICATIONS] : [];
  const results = await PermissionsAndroid.requestMultiple([...required, ...optional]);
  return required.every((perm) => results[perm] === PermissionsAndroid.RESULTS.GRANTED)
    ? 'granted'
    : 'denied';
}

export interface BleTransportOptions {
  /** Fallback labels when a peer's beacon carries an empty name. */
  defaultGuideName?: string;
  defaultVisitorName?: string;
  /** Override discovery duration (ms), mainly for tests. */
  discoveryMs?: number;
  /** Override the front guide's group id, mainly for deterministic tests. */
  nextGroupId?: (self: GuideMember) => number;
}

interface GuideEcho {
  rssi: number;
  atMs: number;
}

interface HeardGuide extends GuideEcho {
  groupId: number;
}

/**
 * The group id a front guide broadcasts, derived from its session id rather than drawn at random:
 * a restart of the radio for the same session (fast refresh, NFC toggled, the effect re-running)
 * must keep the group its visitors already joined.
 */
function sessionGroupId(self: GuideMember): number {
  return memberIdToShortId(memberId(`group:${self.id}`));
}

export function createBleTransport(
  radio: GroupRadioModule,
  options: BleTransportOptions = {},
): GroupTransport {
  const defaultGuideName = options.defaultGuideName ?? 'Guía';
  const defaultVisitorName = options.defaultVisitorName ?? 'Visitante';
  const discoveryMs = options.discoveryMs ?? DISCOVERY_MS;
  const nextGroupId = options.nextGroupId ?? sessionGroupId;

  // Remembered across findSyncingGuides() -> start() so a rear guide joins the front guide's group.
  let lastDiscovered: { guide: GuideMember; groupId: number }[] = [];

  let activeSyncing = true;
  // Set by `setAlertMeters`, which may run before `start` (like `setSyncMode`); it outlives sessions.
  let activeAlertMeters: number | undefined;
  let refreshBeacon: (() => void) | null = null;

  return {
    nativeTicks: true,

    alert(freshCount: number) {
      radio.alert(freshCount);
    },

    setSyncMode(on: boolean) {
      activeSyncing = on;
      refreshBeacon?.();
    },

    setAlertMeters(meters: number) {
      if (!Number.isFinite(meters)) return;
      const next = clampAlertMeters(meters);
      if (next === activeAlertMeters) return;
      activeAlertMeters = next;
      radio.log(`alert meters set ${next}`);
      refreshBeacon?.();
    },

    findSyncingGuides(signal?: AbortSignal): Promise<GuideMember[]> {
      if (signal?.aborted) return Promise.resolve([]);
      return new Promise((resolve) => {
        const found = new Map<MemberId, { guide: GuideMember; groupId: number; rssi: number }>();
        const sub = radio.addListener('onSighting', (s) => {
          if (s.rssi < GROUP_POLICY.pairMinDbm) return;
          const frame = decodeBeacon(s.payload);
          if (!frame || frame.role !== 'guide' || !frame.syncing || frame.groupId === 0) return;
          const member = memberFromBeacon(frame, defaultGuideName);
          if (member.role !== 'guide') return;
          const prev = found.get(member.id);
          if (!prev || s.rssi > prev.rssi) {
            found.set(member.id, { guide: member, groupId: frame.groupId, rssi: s.rssi });
          }
        });

        let done = false;
        const finish = (aborted: boolean) => {
          if (done) return;
          done = true;
          clearTimeout(timer);
          signal?.removeEventListener('abort', onAbort);
          sub.remove();
          radio.stop();
          if (aborted) {
            resolve([]);
            return;
          }
          const ordered = [...found.values()].sort((a, b) => {
            if (a.guide.slot !== b.guide.slot) return a.guide.slot === 'front' ? -1 : 1;
            return b.rssi - a.rssi;
          });
          lastDiscovered = ordered.map(({ guide, groupId }) => ({ guide, groupId }));
          resolve(ordered.map((x) => x.guide));
        };
        const onAbort = () => finish(true);

        // Scan-only burst: payload is unused when advertise=false.
        radio.start('00', false, true);
        const timer = setTimeout(() => finish(false), discoveryMs);
        signal?.addEventListener('abort', onAbort, { once: true });
      });
    },

    start(self, onEvent) {
      const selfShortId = memberIdToShortId(self.id);
      const known = new Map<number, Member>([[selfShortId, self]]);
      let frontGuideId: MemberId | null =
        self.role === 'guide' && self.slot === 'front' ? self.id : null;
      let rearGuideId: MemberId | null =
        self.role === 'guide' && self.slot === 'rear' ? self.id : null;

      let groupId = 0;
      const preJoined: GuideMember[] = [];
      if (self.role === 'guide') {
        const front = lastDiscovered.find((d) => d.guide.slot === 'front') ?? lastDiscovered[0];
        if (self.slot === 'rear' && front) {
          groupId = front.groupId;
          const frontShort = memberIdToShortId(front.guide.id);
          known.set(frontShort, front.guide);
          frontGuideId = front.guide.id;
          preJoined.push(front.guide);
        } else {
          groupId = nextGroupId(self);
        }
        lastDiscovered = [];
      }

      const echoes: { front: GuideEcho | null; rear: GuideEcho | null } = {
        front: null,
        rear: null,
      };
      const nfcOn = () => radio.capabilities().nfc === 'on';
      // Guide: `setAlertMeters` wins over the distance `self` started with.
      const ownAlertMeters = (): number | undefined =>
        self.role !== 'guide'
          ? undefined
          : (activeAlertMeters ??
            (self.alertMeters === undefined ? undefined : clampAlertMeters(self.alertMeters)));
      // Guide: what a tapping visitor reads, and whether the beacon tells visitors to tap.
      let cardAdvertised = false;
      const syncCard = () => {
        if (self.role !== 'guide') return;
        radio.setNfcCard(
          activeSyncing
            ? encodePairing({
                groupId,
                guideShortId: selfShortId,
                slot: self.slot,
                name: self.name,
                ...withAlertMeters(ownAlertMeters()),
              })
            : null,
        );
        cardAdvertised = activeSyncing && nfcOn();
      };
      // Unpaired visitor: last beacon of each syncing guide, so an NFC join starts with a reading.
      const heardGuides = new Map<number, HeardGuide>();
      let visitorNfc = self.role === 'visitor' && nfcOn();
      // When the visitor first heard a card-up guide within pairing range; starts the NFC grace.
      let tapWaitSinceMs: number | null = null;

      let lastAdvertisedHex = '';
      let lastEchoSentAtMs = 0;
      let lastEchoFront: number | null = null;
      let lastEchoRear: number | null = null;

      const buildPayload = (): string => {
        const frame: BeaconFrame = {
          groupId,
          senderId: selfShortId,
          role: self.role,
          slot: self.role === 'guide' ? self.slot : 'front',
          syncing: self.role === 'guide' && activeSyncing,
          nfcCard: self.role === 'guide' && cardAdvertised,
          echoFrontRssi: self.role === 'visitor' ? (echoes.front?.rssi ?? null) : null,
          echoRearRssi: self.role === 'visitor' ? (echoes.rear?.rssi ?? null) : null,
          name: self.name,
          ...withAlertMeters(ownAlertMeters()),
          tag: 0,
        };
        return encodeBeacon(frame);
      };

      const pushPayload = (force: boolean, nowMs: number) => {
        if (!force) {
          const curFront = echoes.front?.rssi ?? null;
          const curRear = echoes.rear?.rssi ?? null;
          const changed =
            (curFront === null) !== (lastEchoFront === null) ||
            (curRear === null) !== (lastEchoRear === null) ||
            (curFront !== null &&
              lastEchoFront !== null &&
              Math.abs(curFront - lastEchoFront) >= ECHO_MIN_DELTA_DB) ||
            (curRear !== null &&
              lastEchoRear !== null &&
              Math.abs(curRear - lastEchoRear) >= ECHO_MIN_DELTA_DB);
          if (!changed || nowMs - lastEchoSentAtMs < ECHO_MIN_INTERVAL_MS) return;
        }
        const hex = buildPayload();
        if (hex === lastAdvertisedHex) return;
        lastAdvertisedHex = hex;
        lastEchoSentAtMs = nowMs;
        lastEchoFront = echoes.front?.rssi ?? null;
        lastEchoRear = echoes.rear?.rssi ?? null;
        radio.updatePayload(hex);
      };

      refreshBeacon = () => {
        syncCard();
        pushPayload(true, Date.now());
      };

      const registerGuide = (guide: GuideMember) => {
        if (guide.slot === 'front') frontGuideId = guide.id;
        else rearGuideId = guide.id;
      };

      const joinGroup = (
        joinedGroupId: number,
        guideShortId: number,
        guide: GuideMember,
        heard: GuideEcho | null,
        atMs: number,
        via: 'nfc' | 'ble',
      ) => {
        groupId = joinedGroupId;
        heardGuides.clear();
        if (self.role === 'visitor') radio.stopNfcReader();
        known.set(guideShortId, guide);
        registerGuide(guide);
        onEvent({ kind: 'joined', member: guide });
        if (heard) {
          echoes[guide.slot] = heard;
          onEvent({
            kind: 'sighting',
            sighting: { observer: self.id, subject: guide.id, rssi: heard.rssi, atMs: heard.atMs },
          });
        }
        radio.log(`joined via ${via} group=${joinedGroupId} guide=${guideShortId}`);
        pushPayload(true, atMs);
      };

      const nfcSub =
        self.role === 'visitor'
          ? radio.addListener('onNfcCard', ({ payload, atMs }) => {
              if (groupId !== 0) return;
              const record = decodePairing(payload);
              if (!record || record.guideShortId === selfShortId) {
                radio.log(`nfc card ignored: ${payload}`);
                return;
              }
              const guide: GuideMember = {
                id: shortIdToMemberId(record.guideShortId),
                role: 'guide',
                name: record.name || defaultGuideName,
                slot: record.slot,
                ...withAlertMeters(record.alertMeters),
              };
              const heard = heardGuides.get(record.guideShortId);
              const fresh =
                heard &&
                heard.groupId === record.groupId &&
                atMs - heard.atMs <= GROUP_POLICY.unseenAfterMs;
              joinGroup(
                record.groupId,
                record.guideShortId,
                guide,
                fresh ? { rssi: heard.rssi, atMs: heard.atMs } : null,
                atMs,
                'nfc',
              );
            })
          : null;

      const sightingSub = radio.addListener('onSighting', ({ payload, rssi, atMs }) => {
        const frame = decodeBeacon(payload);
        if (!frame || frame.senderId === selfShortId) return;

        // Unpaired visitor: wait for the tap when both phones can do NFC, otherwise lock onto the
        // first syncing guide within touching range.
        if (self.role === 'visitor' && groupId === 0) {
          if (frame.role !== 'guide' || !frame.syncing || frame.groupId === 0) return;
          heardGuides.set(frame.senderId, { groupId: frame.groupId, rssi, atMs });
          if (rssi < GROUP_POLICY.pairMinDbm) return;
          if (frame.nfcCard && visitorNfc) {
            tapWaitSinceMs ??= atMs;
            if (atMs - tapWaitSinceMs < GROUP_POLICY.nfcGraceMs) return;
          }
          const guide = memberFromBeacon(frame, defaultGuideName);
          if (guide.role !== 'guide') return;
          joinGroup(frame.groupId, frame.senderId, guide, { rssi, atMs }, atMs, 'ble');
          return;
        }

        if (groupId === 0 || frame.groupId !== groupId) return;

        let peer = known.get(frame.senderId);
        if (!peer) {
          // Guides only admit new visitors while sync mode is enabled; other guides in the same
          // group are always admitted.
          if (self.role === 'guide' && frame.role === 'visitor' && !activeSyncing) return;
          peer = memberFromBeacon(
            frame,
            frame.role === 'guide' ? defaultGuideName : defaultVisitorName,
          );
          known.set(frame.senderId, peer);
          if (peer.role === 'guide') registerGuide(peer);
          onEvent({ kind: 'joined', member: peer });
        } else if (
          peer.role === 'guide' &&
          frame.role === 'guide' &&
          peer.alertMeters !== frame.alertMeters
        ) {
          // Keep the stored name: an NFC join carries up to 32 bytes of it, a beacon only 10.
          peer = {
            id: peer.id,
            role: 'guide',
            name: peer.name,
            slot: peer.slot,
            ...withAlertMeters(frame.alertMeters),
          };
          known.set(frame.senderId, peer);
          radio.log(`guide ${frame.senderId} alert meters ${frame.alertMeters ?? 'none'}`);
          onEvent({ kind: 'joined', member: peer });
        }

        onEvent({
          kind: 'sighting',
          sighting: { observer: self.id, subject: peer.id, rssi, atMs },
        });

        if (self.role === 'visitor' && peer.role === 'guide') {
          echoes[peer.slot] = { rssi, atMs };
          pushPayload(false, atMs);
        } else if (self.role === 'guide' && peer.role === 'visitor') {
          // Relay visitor's own readings of each guide so the two-guide lane has both ends.
          if (frame.echoFrontRssi !== null && frontGuideId) {
            onEvent({
              kind: 'sighting',
              sighting: {
                observer: peer.id,
                subject: frontGuideId,
                rssi: frame.echoFrontRssi,
                atMs,
              },
            });
          }
          if (frame.echoRearRssi !== null && rearGuideId) {
            onEvent({
              kind: 'sighting',
              sighting: { observer: peer.id, subject: rearGuideId, rssi: frame.echoRearRssi, atMs },
            });
          }
        }
      });

      const tickSub = radio.addListener('onTick', ({ atMs }) => {
        // NFC can be switched on or off in settings while the visitor waits to pair; re-arm the
        // reader when it comes on, since reader mode may not have taken while NFC was off.
        if (self.role === 'visitor' && groupId === 0) {
          const on = nfcOn();
          if (on && !visitorNfc) radio.startNfcReader();
          visitorNfc = on;
        }
        // A guide who switches NFC off must stop telling visitors to tap.
        if (self.role === 'guide' && activeSyncing && cardAdvertised !== nfcOn()) {
          cardAdvertised = !cardAdvertised;
          pushPayload(true, atMs);
        }
        if (self.role === 'visitor' && groupId !== 0) {
          let expired = false;
          if (echoes.front && atMs - echoes.front.atMs > GROUP_POLICY.unseenAfterMs) {
            echoes.front = null;
            expired = true;
          }
          if (echoes.rear && atMs - echoes.rear.atMs > GROUP_POLICY.unseenAfterMs) {
            echoes.rear = null;
            expired = true;
          }
          if (expired) pushPayload(false, atMs);
        }
        onEvent({ kind: 'tick', nowMs: atMs });
      });

      for (const g of preJoined) onEvent({ kind: 'joined', member: g });

      syncCard();
      lastAdvertisedHex = buildPayload();
      radio.start(lastAdvertisedHex, true, true);
      if (self.role === 'visitor') radio.startNfcReader();

      return () => {
        refreshBeacon = null;
        sightingSub.remove();
        tickSub.remove();
        nfcSub?.remove();
        if (self.role === 'visitor') radio.stopNfcReader();
        else radio.setNfcCard(null);
        radio.stop();
      };
    },
  };
}
