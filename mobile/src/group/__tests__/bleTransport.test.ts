import { EMPTY_GROUP, alerts, step, type GroupInput } from '@/core/group/groupState';
import { GROUP_POLICY } from '@/core/group/policy';
import { memberId, type GuideMember, type VisitorMember } from '@/core/group/types';
import {
  decodeBeacon,
  decodePairing,
  encodeBeacon,
  encodePairing,
  shortIdToMemberId,
  type BeaconFrame,
} from '@/core/group/wire';

import type {
  GroupRadioModule,
  RadioCapabilities,
  RadioNfcCard,
  RadioSighting,
  RadioTick,
} from '../../../modules/group-radio';
import { createBleTransport } from '../bleTransport';

interface FakeRadio {
  module: GroupRadioModule;
  started: { payloadHex: string; advertise: boolean; scan: boolean }[];
  updatedPayloads: string[];
  stops: number;
  alerts: number[];
  setNfc(nfc: RadioCapabilities['nfc']): void;
  /** Every setNfcCard call, in order. */
  cards: (string | null)[];
  readonly readerOn: boolean;
  logs: string[];
  /** `phy` defaults to '1m': the transport treats both PHYs alike. */
  emitSighting(s: Omit<RadioSighting, 'phy'> & { phy?: RadioSighting['phy'] }): void;
  emitTick(atMs: number): void;
  emitNfcCard(c: RadioNfcCard): void;
}

type Listener =
  ((s: RadioSighting) => void) | ((t: RadioTick) => void) | ((c: RadioNfcCard) => void);

/** `nfc` defaults to 'none' so the BLE-only tests cover the proximity fallback. */
function makeFakeRadio(nfc: RadioCapabilities['nfc'] = 'none'): FakeRadio {
  const listeners = {
    onSighting: new Set<(s: RadioSighting) => void>(),
    onTick: new Set<(t: RadioTick) => void>(),
    onNfcCard: new Set<(c: RadioNfcCard) => void>(),
  };
  const cards: (string | null)[] = [];
  const logs: string[] = [];
  let readerOn = false;
  const state = { nfc };
  const started: FakeRadio['started'] = [];
  const updatedPayloads: string[] = [];
  const alertsSent: number[] = [];
  let stops = 0;

  const module: GroupRadioModule = {
    capabilities: () => ({
      sdk: 35,
      bluetoothOn: true,
      canAdvertise: true,
      running: started.length > stops,
      lastError: null,
      nfc: state.nfc,
      codedPhy: true,
    }),
    start(payloadHex, advertise, scan) {
      started.push({ payloadHex, advertise, scan });
    },
    updatePayload(payloadHex) {
      updatedPayloads.push(payloadHex);
    },
    stop() {
      stops += 1;
    },
    alert(count) {
      alertsSent.push(count);
    },
    setNfcCard(payloadHex) {
      cards.push(payloadHex);
    },
    startNfcReader() {
      readerOn = true;
    },
    stopNfcReader() {
      readerOn = false;
    },
    log(message) {
      logs.push(message);
    },
    addListener(event: keyof typeof listeners, listener: Listener) {
      const set = listeners[event] as Set<Listener>;
      set.add(listener);
      return { remove: () => set.delete(listener) };
    },
  };

  return {
    module,
    started,
    updatedPayloads,
    get stops() {
      return stops;
    },
    alerts: alertsSent,
    setNfc(next) {
      state.nfc = next;
    },
    cards,
    get readerOn() {
      return readerOn;
    },
    logs,
    emitSighting(s) {
      for (const l of [...listeners.onSighting]) l({ phy: '1m', ...s });
    },
    emitTick(atMs) {
      for (const l of [...listeners.onTick]) l({ atMs });
    },
    emitNfcCard(c) {
      for (const l of [...listeners.onNfcCard]) l(c);
    },
  };
}

describe('createBleTransport', () => {
  beforeEach(() => jest.useFakeTimers());
  afterEach(() => jest.useRealTimers());

  it('pairs a visitor only when a syncing guide is within touching range and echoes RSSI', () => {
    const radio = makeFakeRadio();
    const transport = createBleTransport(radio.module);
    const visitor: VisitorMember = { id: shortIdToMemberId(0x00a2), role: 'visitor', name: 'Ana' };
    const events: GroupInput[] = [];
    const stop = transport.start(visitor, (e) => events.push(e));

    // Starts advertising unpaired (groupId = 0)
    expect(decodeBeacon(radio.started[0].payloadHex)?.groupId).toBe(0);

    const guideHex = encodeBeacon({
      groupId: 0x4242,
      senderId: 0x00e6,
      role: 'guide',
      slot: 'front',
      syncing: true,
      nfcCard: false,
      echoFrontRssi: null,
      echoRearRssi: null,
      name: 'Marta',
      tag: 0,
    });

    // Too far: must NOT pair
    radio.emitSighting({ payload: guideHex, rssi: GROUP_POLICY.pairMinDbm - 10, atMs: 1000 });
    expect(events).toHaveLength(0);

    // Within touching range: pairs immediately and updates beacon with groupId + echo
    radio.emitSighting({ payload: guideHex, rssi: GROUP_POLICY.pairMinDbm + 15, atMs: 2000 });
    expect(events).toEqual([
      {
        kind: 'joined',
        member: { id: shortIdToMemberId(0x00e6), role: 'guide', name: 'Marta', slot: 'front' },
      },
      {
        kind: 'sighting',
        sighting: {
          observer: visitor.id,
          subject: shortIdToMemberId(0x00e6),
          rssi: GROUP_POLICY.pairMinDbm + 15,
          atMs: 2000,
        },
      },
    ]);
    const updated = decodeBeacon(radio.updatedPayloads[0]);
    expect(updated?.groupId).toBe(0x4242);
    expect(updated?.echoFrontRssi).toBe(GROUP_POLICY.pairMinDbm + 15);

    stop();
    expect(radio.stops).toBe(1);
  });

  it('admits new visitors only while sync mode is on, keeps known visitors when off, and relays echoes', () => {
    const radio = makeFakeRadio();
    const transport = createBleTransport(radio.module, { nextGroupId: () => 0x7777 });
    const guide: GuideMember = {
      id: shortIdToMemberId(0x00e6),
      role: 'guide',
      name: 'Marta',
      slot: 'front',
    };
    const events: GroupInput[] = [];
    const stop = transport.start(guide, (e) => events.push(e));
    transport.setSyncMode(true);

    const anaHex = encodeBeacon({
      groupId: 0x7777,
      senderId: 0x00a2,
      role: 'visitor',
      slot: 'front',
      syncing: false,
      nfcCard: false,
      echoFrontRssi: -52,
      echoRearRssi: null,
      name: 'Ana',
      tag: 0,
    });
    radio.emitSighting({ payload: anaHex, rssi: -50, atMs: 1000 });
    expect(events.map((e) => e.kind)).toEqual(['joined', 'sighting', 'sighting']);
    // Relayed echo sighting has Ana as observer and Marta as subject
    expect(events[2]).toEqual({
      kind: 'sighting',
      sighting: { observer: shortIdToMemberId(0x00a2), subject: guide.id, rssi: -52, atMs: 1000 },
    });

    // Turn off sync mode: unknown visitor Pedro is ignored, known visitor Ana still tracked
    transport.setSyncMode(false);
    expect(decodeBeacon(radio.updatedPayloads.at(-1)!)?.syncing).toBe(false);

    const pedroHex = encodeBeacon({
      groupId: 0x7777,
      senderId: 0x00b3,
      role: 'visitor',
      slot: 'front',
      syncing: false,
      nfcCard: false,
      echoFrontRssi: -50,
      echoRearRssi: null,
      name: 'Pedro',
      tag: 0,
    });
    const before = events.length;
    radio.emitSighting({ payload: pedroHex, rssi: -48, atMs: 2000 });
    expect(events).toHaveLength(before);

    radio.emitSighting({ payload: anaHex, rssi: -70, atMs: 3000 });
    expect(events).toHaveLength(before + 2);

    stop();
  });

  it('discovers a nearby syncing front guide and joins the same group as rear guide', async () => {
    const radio = makeFakeRadio();
    const transport = createBleTransport(radio.module, { discoveryMs: 500 });

    const pending = transport.findSyncingGuides();
    const frontHex = encodeBeacon({
      groupId: 0x9999,
      senderId: 0x0001,
      role: 'guide',
      slot: 'front',
      syncing: true,
      nfcCard: false,
      echoFrontRssi: null,
      echoRearRssi: null,
      name: 'Marta',
      tag: 0,
    });
    radio.emitSighting({ payload: frontHex, rssi: -50, atMs: 100 });
    jest.advanceTimersByTime(500);
    const found = await pending;
    expect(found).toEqual([
      { id: shortIdToMemberId(0x0001), role: 'guide', name: 'Marta', slot: 'front' },
    ]);

    const rear: GuideMember = {
      id: shortIdToMemberId(0x0002),
      role: 'guide',
      name: 'Carlos',
      slot: 'rear',
    };
    const events: GroupInput[] = [];
    const stop = transport.start(rear, (e) => events.push(e));
    // Rear guide immediately joins front guide's group and announces front guide
    expect(decodeBeacon(radio.started.at(-1)!.payloadHex)?.groupId).toBe(0x9999);
    expect(events[0]).toEqual({ kind: 'joined', member: found[0] });
    stop();
  });

  it('a restarted front-guide session keeps its group id, so joined visitors still match', () => {
    const radio = makeFakeRadio();
    const transport = createBleTransport(radio.module);
    const marta: GuideMember = { id: memberId('m-marta'), role: 'guide', name: 'Marta', slot: 'front' };
    transport.start(marta, () => {})();
    transport.start(marta, () => {})();
    const [first, second] = radio.started.map((s) => decodeBeacon(s.payloadHex)?.groupId);
    expect(first).toBeGreaterThan(0);
    expect(second).toBe(first);
    const other: GuideMember = { ...marta, id: memberId('m-other') };
    transport.start(other, () => {})();
    expect(decodeBeacon(radio.started[2].payloadHex)?.groupId).not.toBe(first);
  });

  it('forwards native ticks so a silent visitor ages into visitorLost without JS timers', () => {
    const radio = makeFakeRadio();
    const transport = createBleTransport(radio.module, { nextGroupId: () => 0x1111 });
    const guide: GuideMember = {
      id: shortIdToMemberId(0x0001),
      role: 'guide',
      name: 'Marta',
      slot: 'front',
    };
    let state = step(step(EMPTY_GROUP, { kind: 'tick', nowMs: 1000 }), {
      kind: 'joined',
      member: guide,
    });
    const stop = transport.start(guide, (e) => {
      state = step(state, e);
    });

    const anaHex = encodeBeacon({
      groupId: 0x1111,
      senderId: 0x0002,
      role: 'visitor',
      slot: 'front',
      syncing: false,
      nfcCard: false,
      echoFrontRssi: null,
      echoRearRssi: null,
      name: 'Ana',
      tag: 0,
    });
    radio.emitSighting({ payload: anaHex, rssi: -55, atMs: 1000 });
    expect(alerts(state, guide.id)).toEqual([]);

    radio.emitTick(1000 + GROUP_POLICY.unseenAfterMs + 1000);
    expect(alerts(state, guide.id)).toEqual([
      { kind: 'visitorLost', id: shortIdToMemberId(0x0002) },
    ]);

    stop();
  });

  describe('NFC tap pairing', () => {
    const marta: GuideMember = {
      id: shortIdToMemberId(0x00e6),
      role: 'guide',
      name: 'Marta',
      slot: 'front',
    };
    const martaBeacon = (nfcCard: boolean) =>
      encodeBeacon({
        groupId: 0x4242,
        senderId: 0x00e6,
        role: 'guide',
        slot: 'front',
        syncing: true,
        nfcCard,
        echoFrontRssi: null,
        echoRearRssi: null,
        name: 'Marta',
        tag: 0,
      });
    const martaCard = encodePairing({
      groupId: 0x4242,
      guideShortId: 0x00e6,
      slot: 'front',
      name: 'Marta',
    });
    const ana: VisitorMember = { id: shortIdToMemberId(0x00a2), role: 'visitor', name: 'Ana' };

    it('a guide raises its card while syncing and drops it when sync stops or the session ends', () => {
      const radio = makeFakeRadio('on');
      const transport = createBleTransport(radio.module, { nextGroupId: () => 0x4242 });
      const stop = transport.start(marta, () => {});

      expect(radio.cards).toEqual([martaCard]);
      expect(decodeBeacon(radio.started[0].payloadHex)?.nfcCard).toBe(true);

      transport.setSyncMode(false);
      expect(radio.cards.at(-1)).toBeNull();
      expect(decodeBeacon(radio.updatedPayloads.at(-1)!)?.nfcCard).toBe(false);

      transport.setSyncMode(true);
      expect(radio.cards.at(-1)).toBe(martaCard);

      stop();
      expect(radio.cards.at(-1)).toBeNull();
      expect(radio.readerOn).toBe(false);
    });

    it('a guide drops and restores the card flag when NFC is switched off and on', () => {
      const radio = makeFakeRadio('on');
      const transport = createBleTransport(radio.module, { nextGroupId: () => 0x4242 });
      const stop = transport.start(marta, () => {});
      radio.setNfc('off');
      radio.emitTick(1000);
      expect(decodeBeacon(radio.updatedPayloads.at(-1)!)?.nfcCard).toBe(false);
      const updates = radio.updatedPayloads.length;
      radio.emitTick(2000);
      expect(radio.updatedPayloads).toHaveLength(updates);
      radio.setNfc('on');
      radio.emitTick(3000);
      expect(decodeBeacon(radio.updatedPayloads.at(-1)!)?.nfcCard).toBe(true);
      stop();
    });

    it('a guide without NFC keeps the card flag down so visitors pair over BLE', () => {
      const radio = makeFakeRadio('off');
      const transport = createBleTransport(radio.module, { nextGroupId: () => 0x4242 });
      const stop = transport.start(marta, () => {});
      expect(decodeBeacon(radio.started[0].payloadHex)?.nfcCard).toBe(false);
      stop();
    });

    it('a visitor with NFC waits for the tap, then joins with the beacon it already heard', () => {
      const radio = makeFakeRadio('on');
      const transport = createBleTransport(radio.module);
      const events: GroupInput[] = [];
      const stop = transport.start(ana, (e) => events.push(e));
      expect(radio.readerOn).toBe(true);

      // Touching range over BLE, but the guide's card is up: no proximity join.
      radio.emitSighting({ payload: martaBeacon(true), rssi: -45, atMs: 1000 });
      expect(events).toEqual([]);

      // A record that does not parse is ignored and the reader keeps polling.
      radio.emitNfcCard({ payload: 'deadbeef', atMs: 1500 });
      expect(events).toEqual([]);
      expect(radio.readerOn).toBe(true);

      radio.emitNfcCard({ payload: martaCard, atMs: 2000 });
      expect(events).toEqual([
        { kind: 'joined', member: marta },
        {
          kind: 'sighting',
          sighting: { observer: ana.id, subject: marta.id, rssi: -45, atMs: 1000 },
        },
      ]);
      expect(radio.readerOn).toBe(false);
      expect(radio.logs).toContain('joined via nfc group=16962 guide=230');
      const beacon = decodeBeacon(radio.updatedPayloads.at(-1)!);
      expect(beacon?.groupId).toBe(0x4242);
      expect(beacon?.echoFrontRssi).toBe(-45);

      // A second tap does nothing; the guide's beacons now track as a paired member.
      radio.emitNfcCard({ payload: martaCard, atMs: 2500 });
      radio.emitSighting({ payload: martaBeacon(true), rssi: -60, atMs: 3000 });
      expect(events.slice(2)).toEqual([
        {
          kind: 'sighting',
          sighting: { observer: ana.id, subject: marta.id, rssi: -60, atMs: 3000 },
        },
      ]);
      stop();
    });

    it('a tap with no beacon heard yet joins without a sighting', () => {
      const radio = makeFakeRadio('on');
      const transport = createBleTransport(radio.module);
      const events: GroupInput[] = [];
      const stop = transport.start(ana, (e) => events.push(e));
      radio.emitNfcCard({ payload: martaCard, atMs: 2000 });
      expect(events).toEqual([{ kind: 'joined', member: marta }]);
      expect(decodeBeacon(radio.updatedPayloads.at(-1)!)?.echoFrontRssi).toBeNull();
      stop();
    });

    it('a visitor with NFC falls back to BLE when no tap arrives within the grace window', () => {
      const radio = makeFakeRadio('on');
      const transport = createBleTransport(radio.module);
      const events: GroupInput[] = [];
      const stop = transport.start(ana, (e) => events.push(e));
      // Far beacons do not start the wait; the first in-range one does.
      radio.emitSighting({ payload: martaBeacon(true), rssi: -80, atMs: 500 });
      radio.emitSighting({ payload: martaBeacon(true), rssi: -45, atMs: 1000 });
      radio.emitSighting({
        payload: martaBeacon(true),
        rssi: -45,
        atMs: 1000 + GROUP_POLICY.nfcGraceMs - 1,
      });
      expect(events).toEqual([]);
      radio.emitSighting({
        payload: martaBeacon(true),
        rssi: -45,
        atMs: 1000 + GROUP_POLICY.nfcGraceMs,
      });
      expect(events.map((e) => e.kind)).toEqual(['joined', 'sighting']);
      expect(radio.logs).toContain('joined via ble group=16962 guide=230');
      expect(radio.readerOn).toBe(false);
      stop();
    });

    it('a visitor with NFC still pairs over BLE with a guide whose card is down', () => {
      const radio = makeFakeRadio('on');
      const transport = createBleTransport(radio.module);
      const events: GroupInput[] = [];
      const stop = transport.start(ana, (e) => events.push(e));
      radio.emitSighting({ payload: martaBeacon(false), rssi: -45, atMs: 1000 });
      expect(events.map((e) => e.kind)).toEqual(['joined', 'sighting']);
      expect(radio.readerOn).toBe(false);
      expect(radio.logs).toContain('joined via ble group=16962 guide=230');
      stop();
    });
  });

  describe('alert distance', () => {
    const marta: GuideMember = {
      id: shortIdToMemberId(0x00e6),
      role: 'guide',
      name: 'Marta Valentina',
      slot: 'front',
    };
    const ana: VisitorMember = { id: shortIdToMemberId(0x00a2), role: 'visitor', name: 'Ana' };
    const guideFrame = (alertMeters: number | undefined, over: Partial<BeaconFrame> = {}) =>
      encodeBeacon({
        groupId: 0x4242,
        senderId: 0x00e6,
        role: 'guide',
        slot: 'front',
        syncing: true,
        nfcCard: false,
        echoFrontRssi: null,
        echoRearRssi: null,
        name: 'Marta Valentina',
        alertMeters,
        tag: 0,
        ...over,
      });
    const joins = (events: GroupInput[]) =>
      events.flatMap((e) => (e.kind === 'joined' ? [e.member] : []));

    it('a guide broadcasts its distance in beacon and card, clamped, refreshed at once', () => {
      const radio = makeFakeRadio('on');
      const transport = createBleTransport(radio.module, { nextGroupId: () => 0x4242 });
      transport.setAlertMeters!(40); // before start, like setSyncMode
      const stop = transport.start(marta, () => {});
      expect(decodeBeacon(radio.started[0].payloadHex)?.alertMeters).toBe(40);
      expect(decodePairing(radio.cards.at(-1)!)?.alertMeters).toBe(40);

      transport.setAlertMeters!(152);
      expect(decodeBeacon(radio.updatedPayloads.at(-1)!)?.alertMeters).toBe(
        GROUP_POLICY.alertMeters.max,
      );
      expect(decodePairing(radio.cards.at(-1)!)?.alertMeters).toBe(GROUP_POLICY.alertMeters.max);
      transport.setAlertMeters!(33);
      expect(decodeBeacon(radio.updatedPayloads.at(-1)!)?.alertMeters).toBe(35);

      const updates = radio.updatedPayloads.length;
      transport.setAlertMeters!(35);
      transport.setAlertMeters!(Number.NaN);
      expect(radio.updatedPayloads).toHaveLength(updates);
      stop();
    });

    it("a guide that never set a distance starts with self's, or none", () => {
      const radio = makeFakeRadio();
      const withOwn = createBleTransport(radio.module).start(
        { ...marta, alertMeters: 70 },
        () => {},
      );
      expect(decodeBeacon(radio.started[0].payloadHex)?.alertMeters).toBe(70);
      withOwn();
      createBleTransport(radio.module).start(marta, () => {})();
      expect(decodeBeacon(radio.started[1].payloadHex)).not.toHaveProperty('alertMeters');
    });

    it('a visitor never broadcasts a distance', () => {
      const radio = makeFakeRadio();
      const transport = createBleTransport(radio.module);
      transport.setAlertMeters!(60);
      const stop = transport.start(ana, () => {});
      expect(decodeBeacon(radio.started[0].payloadHex)).not.toHaveProperty('alertMeters');
      stop();
    });

    it('a visitor joined by tap takes the card distance and re-joins the guide when it changes', () => {
      const radio = makeFakeRadio('on');
      const transport = createBleTransport(radio.module);
      const events: GroupInput[] = [];
      const stop = transport.start(ana, (e) => events.push(e));
      radio.emitNfcCard({
        payload: encodePairing({
          groupId: 0x4242,
          guideShortId: 0x00e6,
          slot: 'front',
          name: 'Marta Valentina',
          alertMeters: 60,
        }),
        atMs: 1000,
      });
      expect(joins(events)).toEqual([{ ...marta, alertMeters: 60 }]);

      // Same distance on the air: just a sighting, no re-join.
      radio.emitSighting({ payload: guideFrame(60), rssi: -60, atMs: 2000 });
      expect(joins(events)).toHaveLength(1);

      // The guide moves the slider: re-join with the new distance, keeping the card's full name
      // (the beacon only carries "Marta Vale").
      radio.emitSighting({ payload: guideFrame(90), rssi: -60, atMs: 3000, phy: 'coded' });
      expect(joins(events)).toEqual([
        { ...marta, alertMeters: 60 },
        { ...marta, alertMeters: 90 },
      ]);
      expect(events.at(-1)).toEqual({
        kind: 'sighting',
        sighting: { observer: ana.id, subject: marta.id, rssi: -60, atMs: 3000 },
      });

      // A guide back on an older build (no distance byte): re-join without one.
      radio.emitSighting({ payload: guideFrame(undefined), rssi: -60, atMs: 4000 });
      expect(joins(events).at(-1)).toEqual(marta);
      expect(joins(events).at(-1)).not.toHaveProperty('alertMeters');
      stop();
    });

    it('a visitor paired over BLE takes the beacon distance', () => {
      const radio = makeFakeRadio();
      const events: GroupInput[] = [];
      const stop = createBleTransport(radio.module).start(ana, (e) => events.push(e));
      radio.emitSighting({ payload: guideFrame(25), rssi: -45, atMs: 1000 });
      expect(joins(events)).toEqual([{ ...marta, name: 'Marta Vale', alertMeters: 25 }]);
      stop();
    });

    it('the rear guide re-joins the front guide when its distance changes', () => {
      const radio = makeFakeRadio();
      const transport = createBleTransport(radio.module, { nextGroupId: () => 0x4242 });
      const rear: GuideMember = {
        id: shortIdToMemberId(0x00b7),
        role: 'guide',
        name: 'Luis',
        slot: 'rear',
      };
      const events: GroupInput[] = [];
      const stop = transport.start(rear, (e) => events.push(e));
      radio.emitSighting({ payload: guideFrame(30, { syncing: false }), rssi: -70, atMs: 1000 });
      radio.emitSighting({ payload: guideFrame(30, { syncing: false }), rssi: -70, atMs: 2000 });
      radio.emitSighting({ payload: guideFrame(50, { syncing: false }), rssi: -70, atMs: 3000 });
      expect(joins(events).map((m) => m.role === 'guide' && m.alertMeters)).toEqual([30, 50]);
      stop();
    });
  });

  it('stops the discovery burst immediately when findSyncingGuides is aborted', async () => {
    const radio = makeFakeRadio();
    const transport = createBleTransport(radio.module, { discoveryMs: 1500 });
    const ctrl = new AbortController();
    const pending = transport.findSyncingGuides(ctrl.signal);
    expect(radio.started).toHaveLength(1);
    expect(radio.stops).toBe(0);

    ctrl.abort();
    await expect(pending).resolves.toEqual([]);
    expect(radio.stops).toBe(1);

    // Timer was cleared, so advancing past discoveryMs does not stop a second time.
    jest.advanceTimersByTime(2000);
    expect(radio.stops).toBe(1);
  });
});
