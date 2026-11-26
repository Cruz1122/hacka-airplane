import { GROUP_POLICY } from '../policy';
import { memberId } from '../types';
import {
  BEACON_BYTES,
  PAIRING_NAME_MAX_BYTES,
  decodeBeacon,
  decodePairing,
  encodeBeacon,
  encodePairing,
  memberFromBeacon,
  memberIdToShortId,
  shortIdToMemberId,
  type BeaconFrame,
  type PairingRecord,
} from '../wire';

describe('group BLE wire codec', () => {
  it('round-trips a syncing front guide frame', () => {
    const frame: BeaconFrame = {
      groupId: 0x1a2b,
      senderId: 0x3c4d,
      role: 'guide',
      slot: 'front',
      syncing: true,
      nfcCard: false,
      echoFrontRssi: null,
      echoRearRssi: -74,
      name: 'Marta',
      tag: 0,
    };
    const hex = encodeBeacon(frame);
    expect(hex).toHaveLength(BEACON_BYTES * 2);
    expect(decodeBeacon(hex)).toEqual(frame);
  });

  it('round-trips a rear guide and visitor echoing both guides', () => {
    const rear: BeaconFrame = {
      groupId: 0xffff,
      senderId: 0x0001,
      role: 'guide',
      slot: 'rear',
      syncing: false,
      nfcCard: false,
      echoFrontRssi: -88,
      echoRearRssi: null,
      name: 'Carlos',
      tag: 0xdeadbeef,
    };
    expect(decodeBeacon(encodeBeacon(rear))).toEqual(rear);

    const visitor: BeaconFrame = {
      groupId: 0x1234,
      senderId: 0x5678,
      role: 'visitor',
      slot: 'front',
      syncing: false,
      nfcCard: false,
      echoFrontRssi: -55,
      echoRearRssi: -91,
      name: 'Sofía',
      tag: 0,
    };
    expect(decodeBeacon(encodeBeacon(visitor))).toEqual(visitor);
  });

  it('truncates Spanish accented names cleanly on UTF-8 boundaries without corruption', () => {
    const frame: BeaconFrame = {
      groupId: 0x0010,
      senderId: 0x0020,
      role: 'visitor',
      slot: 'front',
      syncing: false,
      nfcCard: false,
      echoFrontRssi: null,
      echoRearRssi: null,
      name: 'José María Peña',
      tag: 0,
    };
    const decoded = decodeBeacon(encodeBeacon(frame));
    expect(decoded).not.toBeNull();
    // "José Marí" is 11 UTF-8 bytes (J o s C3 A9 ' ' M a r C3 AD): the 2-byte í does not fit in
    // the 10-byte field, so the cut lands before it, never inside it.
    expect(decoded!.name).toBe('José Mar');
  });

  it('clamps extreme RSSI values and treats 0 as unheard', () => {
    const hex = encodeBeacon({
      groupId: 1,
      senderId: 2,
      role: 'visitor',
      slot: 'front',
      syncing: false,
      nfcCard: false,
      echoFrontRssi: -150,
      echoRearRssi: 5,
      name: 'Ana',
      tag: 0,
    });
    const decoded = decodeBeacon(hex);
    expect(decoded?.echoFrontRssi).toBe(-127);
    expect(decoded?.echoRearRssi).toBe(-1);
  });

  it('rejects malformed, wrong-length, wrong-version, and zero-sender payloads', () => {
    expect(decodeBeacon('')).toBeNull();
    expect(decodeBeacon('a2')).toBeNull();
    expect(decodeBeacon('zz'.repeat(BEACON_BYTES))).toBeNull();
    // Version 4
    const valid = encodeBeacon({
      groupId: 1,
      senderId: 2,
      role: 'visitor',
      slot: 'front',
      syncing: false,
      nfcCard: false,
      echoFrontRssi: null,
      echoRearRssi: null,
      name: 'Ana',
      tag: 0,
    });
    expect(decodeBeacon('40' + valid.slice(2))).toBeNull();
    // senderId == 0
    expect(decodeBeacon(valid.slice(0, 6) + '0000' + valid.slice(10))).toBeNull();
  });

  it('round-trips short ids and hashes arbitrary member ids into non-zero 16-bit values', () => {
    const id = shortIdToMemberId(0x00a2);
    expect(id).toBe('g-00a2');
    expect(memberIdToShortId(id)).toBe(0x00a2);

    const hashed = memberIdToShortId(memberId('m-arbitrary-session-id'));
    expect(hashed).toBeGreaterThanOrEqual(1);
    expect(hashed).toBeLessThanOrEqual(0xffff);
    expect(memberIdToShortId(memberId('m-arbitrary-session-id'))).toBe(hashed);
  });

  it('constructs domain Member with fallback name when beacon name is empty', () => {
    const frame: BeaconFrame = {
      groupId: 5,
      senderId: 0x0102,
      role: 'visitor',
      slot: 'front',
      syncing: false,
      nfcCard: false,
      echoFrontRssi: null,
      echoRearRssi: null,
      name: '',
      tag: 0,
    };
    expect(memberFromBeacon(frame, 'Visitante')).toEqual({
      id: 'g-0102',
      role: 'visitor',
      name: 'Visitante',
    });
  });

  it('carries the nfcCard flag for guides only', () => {
    const guide: BeaconFrame = {
      groupId: 0x0042,
      senderId: 0x00e6,
      role: 'guide',
      slot: 'front',
      syncing: true,
      nfcCard: true,
      echoFrontRssi: null,
      echoRearRssi: null,
      name: 'Marta',
      tag: 0,
    };
    expect(decodeBeacon(encodeBeacon(guide))).toEqual(guide);
    const visitor = decodeBeacon(encodeBeacon({ ...guide, role: 'visitor', syncing: false }));
    expect(visitor?.nfcCard).toBe(false);
  });

  const guideFrame: BeaconFrame = {
    groupId: 0x0042,
    senderId: 0x00e6,
    role: 'guide',
    slot: 'front',
    syncing: false,
    nfcCard: false,
    echoFrontRssi: null,
    echoRearRssi: null,
    name: 'Marta',
    alertMeters: 45,
    tag: 0,
  };

  it('carries a guide alert distance into its Member, and none for visitors', () => {
    const hex = encodeBeacon(guideFrame);
    expect(hex.slice(BEACON_BYTES * 2 - 10, BEACON_BYTES * 2 - 8)).toBe('2d'); // byte 17 = 45
    const decoded = decodeBeacon(hex);
    expect(decoded).toEqual(guideFrame);
    expect(memberFromBeacon(decoded!, 'Guía')).toEqual({
      id: 'g-00e6',
      role: 'guide',
      name: 'Marta',
      slot: 'front',
      alertMeters: 45,
    });

    const noDistance = decodeBeacon(encodeBeacon({ ...guideFrame, alertMeters: undefined }));
    expect(noDistance).not.toHaveProperty('alertMeters');
    expect(memberFromBeacon(noDistance!, 'Guía')).not.toHaveProperty('alertMeters');

    const visitor = decodeBeacon(encodeBeacon({ ...guideFrame, role: 'visitor' }));
    expect(visitor).not.toHaveProperty('alertMeters');
  });

  it('carries Pet skins (accessory + tint, and explicit bare head) for guides and visitors', () => {
    const withFlower: BeaconFrame = {
      ...guideFrame,
      role: 'visitor',
      alertMeters: undefined,
      look: { accessory: 'flower', tint: 'lupine' },
    };
    const decodedVisitor = decodeBeacon(encodeBeacon(withFlower));
    expect(decodedVisitor?.look).toEqual({ accessory: 'flower', tint: 'lupine' });
    expect(memberFromBeacon(decodedVisitor!, 'Visitante')).toEqual({
      id: 'g-00e6',
      role: 'visitor',
      name: 'Marta',
      look: { accessory: 'flower', tint: 'lupine' },
    });

    const bareGuide: BeaconFrame = {
      ...guideFrame,
      look: { accessory: 'none' },
    };
    const decodedGuide = decodeBeacon(encodeBeacon(bareGuide));
    expect(decodedGuide?.look).toEqual({ accessory: 'none' });
    expect(memberFromBeacon(decodedGuide!, 'Guía')).toEqual({
      id: 'g-00e6',
      role: 'guide',
      name: 'Marta',
      slot: 'front',
      alertMeters: 45,
      look: { accessory: 'none' },
    });
  });

  it('snaps an off-policy alert byte into the policy range', () => {
    const hex = encodeBeacon(guideFrame);
    const withByte = (b: string) => hex.slice(0, 34) + b + hex.slice(36);
    expect(decodeBeacon(withByte('ff'))?.alertMeters).toBe(GROUP_POLICY.alertMeters.max);
    expect(decodeBeacon(withByte('01'))?.alertMeters).toBe(GROUP_POLICY.alertMeters.min);
    expect(decodeBeacon(withByte('21'))?.alertMeters).toBe(35); // 33 m snaps to the 5 m step
    expect(decodeBeacon(encodeBeacon({ ...guideFrame, alertMeters: 999 }))?.alertMeters).toBe(150);
  });

  it('bounds the v3 name to 9 bytes', () => {
    const decoded = decodeBeacon(encodeBeacon({ ...guideFrame, name: 'Maximiliano Ruiz' }));
    expect(decoded?.name).toBe('Maximilia');
    expect(decoded?.alertMeters).toBe(45);
  });

  it('still decodes v2 and v1 frames from older builds', () => {
    // version 2 | guide, group 0x0042, sender 0x00e6, no echoes, "Maximilian", alertMeters 45, tag 0.
    const v2 = '21' + '0042' + '00e6' + '0000' + '4d6178696d696c69616e' + '2d' + '00000000';
    expect(v2).toHaveLength(BEACON_BYTES * 2);
    expect(decodeBeacon(v2)).toEqual({
      groupId: 0x0042,
      senderId: 0x00e6,
      role: 'guide',
      slot: 'front',
      syncing: false,
      nfcCard: false,
      echoFrontRssi: null,
      echoRearRssi: null,
      name: 'Maximilian',
      alertMeters: 45,
      tag: 0,
    });

    // version 1 | guide+syncing, group 0x0042, sender 0x00e6, no echoes, "Maximiliano", tag 0.
    const v1 = '15' + '0042' + '00e6' + '0000' + '4d6178696d696c69616e6f' + '00000000';
    expect(v1).toHaveLength(BEACON_BYTES * 2);
    const decoded = decodeBeacon(v1);
    expect(decoded).toEqual({
      groupId: 0x0042,
      senderId: 0x00e6,
      role: 'guide',
      slot: 'front',
      syncing: true,
      nfcCard: false,
      echoFrontRssi: null,
      echoRearRssi: null,
      name: 'Maximiliano',
      tag: 0,
    });
    expect(memberFromBeacon(decoded!, 'Guía')).not.toHaveProperty('alertMeters');
  });
});

describe('group NFC pairing record', () => {
  it('round-trips front and rear guides', () => {
    const front: PairingRecord = {
      groupId: 0x4242,
      guideShortId: 0x00e6,
      slot: 'front',
      name: 'Marta',
    };
    const rear: PairingRecord = {
      groupId: 0xffff,
      guideShortId: 0x0001,
      slot: 'rear',
      name: '',
    };
    expect(decodePairing(encodePairing(front))).toEqual(front);
    expect(decodePairing(encodePairing(rear))).toEqual(rear);
    expect(encodePairing(front)).toBe('304242' + '00e6' + '00' + '00' + '05' + '4d61727461');
  });

  it('round-trips the alert distance and Pet skin, and still decodes v2 and v1 records', () => {
    const record: PairingRecord = {
      groupId: 0x4242,
      guideShortId: 0x00e6,
      slot: 'front',
      name: 'Marta',
      alertMeters: 60,
      look: { accessory: 'beanie', tint: 'sun' },
    };
    expect(decodePairing(encodePairing(record))).toEqual(record);
    // v2 record (alertMeters, no look)
    expect(decodePairing('204242' + '00e6' + '3c' + '05' + '4d61727461')).toEqual({
      groupId: 0x4242,
      guideShortId: 0x00e6,
      slot: 'front',
      name: 'Marta',
      alertMeters: 60,
    });
    // v1 record (no alertMeters, no look)
    expect(decodePairing('124242' + '00e6' + '05' + '4d61727461')).toEqual({
      groupId: 0x4242,
      guideShortId: 0x00e6,
      slot: 'rear',
      name: 'Marta',
    });
  });

  it('bounds the name on a UTF-8 boundary', () => {
    const long = 'Ñ'.repeat(40);
    const decoded = decodePairing(
      encodePairing({ groupId: 1, guideShortId: 2, slot: 'front', name: long }),
    );
    expect(decoded?.name).toBe('Ñ'.repeat(PAIRING_NAME_MAX_BYTES / 2));
  });

  it('rejects malformed records', () => {
    const valid = encodePairing({
      groupId: 1,
      guideShortId: 2,
      slot: 'front',
      name: 'Ana',
    });
    expect(decodePairing('')).toBeNull();
    expect(decodePairing(valid.slice(0, -1))).toBeNull(); // odd hex
    expect(decodePairing(valid.slice(0, -2))).toBeNull(); // name shorter than its length byte
    expect(decodePairing(valid + '00')).toBeNull(); // trailing byte
    expect(decodePairing('40' + valid.slice(2))).toBeNull(); // version 4
    expect(decodePairing('300000' + valid.slice(6))).toBeNull(); // groupId 0
    expect(decodePairing(valid.slice(0, 6) + '0000' + valid.slice(10))).toBeNull(); // guide 0
    expect(decodePairing('zz' + valid.slice(2))).toBeNull();
  });
});
