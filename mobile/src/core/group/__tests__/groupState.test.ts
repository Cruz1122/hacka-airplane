import { presence, step, type GroupState } from '../groupState';
import { GROUP_POLICY } from '../policy';
import { dbmAtMeters, zoneCuts } from '../signal';
import {
  alertKeys,
  front,
  FRONT,
  join,
  last,
  rear,
  REAR,
  run,
  V1,
  V2,
  visitor,
  zoneOf,
  type Feed,
  type Frame,
} from '../testing';

const { hysteresisDb, unseenAfterMs, degradeDwellMs } = GROUP_POLICY;
const CUT = zoneCuts(GROUP_POLICY.alertMeters.default);
const steady = (rssi: number) => () => rssi;
const NEAR = CUT.nearMinDbm + 10;
/** Mid, close enough to the far cut-off that a 15 dB dip carries the smoothed value past it. */
const MID = CUT.midMinDbm + 3;

/** Distinct values in order, e.g. ['near', 'mid', 'far']. */
const changes = <T>(xs: T[]) => xs.filter((x, i) => i === 0 || x !== xs[i - 1]);
/** Zone after every input, from the first reading on. */
const zones = (frames: Frame[]) => {
  const zs = frames.map((f) => zoneOf(f.state, V1));
  return zs.slice(zs.findIndex((z) => z !== 'unseen'));
};

describe('signal filter through the reducer', () => {
  const s0 = join(front, visitor(V1));
  const scan = (rssi: (t: number) => number): Feed => ({
    observer: FRONT,
    subject: V1,
    rssi,
  });

  it('a 15 dB dip for 5 s changes neither zone nor alerts', () => {
    const dip = (t: number) => (t >= 20_000 && t < 25_000 ? MID - 15 : MID);
    const frames = run(s0, [scan(dip)], 0, 60_000);
    expect(changes(zones(frames))).toEqual(['mid']);
    expect(frames.flatMap((f) => alertKeys(f.state, FRONT))).toEqual([]);
  });

  it('the same drop, sustained, does reach far (so the dwell is what saved the dip)', () => {
    const drop = (t: number) => (t >= 20_000 ? MID - 15 : MID);
    const s = last(run(s0, [scan(drop)], 0, 20_000 + degradeDwellMs + 10_000));
    expect(zoneOf(s, V1)).toBe('far');
    expect(alertKeys(s, FRONT)).toEqual(['visitorFar:v1']);
  });

  it('a steady walk-away goes near, mid, far and raises visitorFar; coming back clears it at once', () => {
    const from = NEAR;
    const to = CUT.midMinDbm - hysteresisDb - 6;
    // Slow enough (about 0.7 m/s) that the mid band outlasts the pocket guard's dwell.
    const walk = (t: number) => from + ((to - from) * Math.min(t, 120_000)) / 120_000;
    const out = run(s0, [scan(walk)], 0, 120_000 + degradeDwellMs + 5_000);
    expect(changes(zones(out))).toEqual(['near', 'mid', 'far']);
    const away = last(out);
    expect(alertKeys(away, FRONT)).toEqual(['visitorFar:v1']);

    const startBack = away.nowMs + 1;
    const back = run(away, [scan(steady(NEAR))], startBack, startBack + 20_000);
    const cleared = back.find((f) => alertKeys(f.state, FRONT).length === 0)!;
    expect(cleared).toBeDefined();
    expect(cleared.atMs - startBack).toBeLessThan(degradeDwellMs / 2);
    expect(zoneOf(last(back), V1)).toBe('near');
  });

  it('a reading that lands between ticks counts at once', () => {
    // Radios report whenever they hear; the clock only ticks once a second.
    const s = step(step(s0, { kind: 'tick', nowMs: 10_000 }), {
      kind: 'sighting',
      sighting: { observer: FRONT, subject: V1, rssi: NEAR, atMs: 10_400 },
    });
    expect(presence(s, V1)).toEqual({ kind: 'tracked', zone: 'near' });
    expect(alertKeys(s, FRONT)).toEqual([]);
  });

  it('silence past the unseen window gives unseen and visitorLost', () => {
    const heard = run(s0, [scan(steady(NEAR))], 0, 10_000);
    const lastReading = 9_000;
    const quiet = run(last(heard), [], 10_000, lastReading + unseenAfterMs + 3_000);
    const before = quiet.filter((f) => f.atMs <= lastReading + unseenAfterMs);
    expect(before.every((f) => zoneOf(f.state, V1) === 'near')).toBe(true);
    expect(before.flatMap((f) => alertKeys(f.state, FRONT))).toEqual([]);
    const end = last(quiet);
    expect(presence(end, V1)).toEqual({ kind: 'unseen', sinceMs: lastReading });
    expect(alertKeys(end, FRONT)).toEqual(['visitorLost:v1']);
  });
});

describe('two guides', () => {
  const s0 = join(front, rear, visitor(V1), visitor(V2));
  const guidesHearEachOther: Feed[] = [
    { observer: FRONT, subject: REAR, rssi: steady(MID) },
    { observer: REAR, subject: FRONT, rssi: steady(MID) },
  ];
  const rearHears = (id: typeof V1, offsetMs = 0): Feed => ({
    observer: REAR,
    subject: id,
    rssi: steady(NEAR),
    offsetMs,
  });

  it("a visitor heard only by the reachable rear guide raises nothing on the front guide's phone", () => {
    const frames = run(s0, [...guidesHearEachOther, rearHears(V1), rearHears(V2)], 0, 40_000);
    expect(frames.flatMap((f) => alertKeys(f.state, FRONT))).toEqual([]);
    expect(presence(last(frames), V1)).toEqual({
      kind: 'tracked',
      zone: 'near',
    });
  });

  it('rear guide goes silent: exactly one guideLost and no visitorLost for its visitors', () => {
    const live = run(s0, [...guidesHearEachOther, rearHears(V1), rearHears(V2, 400)], 0, 20_000);
    // The rear's last reports trickle in: V2's outlives V1's by two seconds, so V1 runs out of
    // its window while the rear guide still counts as reachable.
    const trickle = run(last(live), [rearHears(V2, 400)], 20_000, 22_000);
    const silent = [...trickle, ...run(last(trickle), [], 22_000, 22_000 + 3 * unseenAfterMs)];
    for (const f of silent) {
      expect(alertKeys(f.state, FRONT).filter((k) => k !== 'guideLost:rear')).toEqual([]);
    }
    const end = last(silent);
    expect(alertKeys(end, FRONT)).toEqual(['guideLost:rear']);
    expect(zoneOf(end, V1)).toBe('unseen');
    expect(zoneOf(end, V2)).toBe('unseen');
  });

  it('a visitor the rear guide stops hearing while it keeps reporting is lost', () => {
    const live = run(s0, [...guidesHearEachOther, rearHears(V1), rearHears(V2)], 0, 20_000);
    const gone = run(
      last(live),
      [...guidesHearEachOther, rearHears(V2)],
      20_000,
      20_000 + 2 * unseenAfterMs,
    );
    expect(alertKeys(last(gone), FRONT)).toEqual(['visitorLost:v1']);
  });
});

describe('alert distance in meters', () => {
  const at = (meters: number) => steady(dbmAtMeters(meters));
  const guideAt = (alertMeters: number) => ({ ...front, alertMeters });
  const scan = (meters: number): Feed => ({
    observer: FRONT,
    subject: V1,
    rssi: at(meters),
  });
  /** The guide's phone re-joining itself with a new slider value, as useGroup does. */
  const slide = (s: GroupState, alertMeters: number) =>
    step(s, { kind: 'joined', member: guideAt(alertMeters) });

  it('at 30 m, a visitor 20 m away is mid and one 40 m away is far', () => {
    const s = last(
      run(
        join(guideAt(30), visitor(V1), visitor(V2)),
        [scan(20), { observer: FRONT, subject: V2, rssi: at(40) }],
        0,
        5_000,
      ),
    );
    expect(zoneOf(s, V1)).toBe('mid');
    expect(zoneOf(s, V2)).toBe('far');
    expect(alertKeys(s, FRONT)).toEqual(['visitorFar:v2']);
  });

  it.each([40, 50])(
    'moving the slider from 30 to 60 m turns a far visitor %i m away mid at the next reading',
    (meters) => {
      const far = last(run(join(guideAt(30), visitor(V1)), [scan(meters)], 0, 20_000));
      expect(alertKeys(far, FRONT)).toEqual(['visitorFar:v1']);
      const moved = slide(far, 60);
      // Zones are decided per reading: nothing changes until the radio reports again.
      expect(zoneOf(moved, V1)).toBe('far');
      const next = step(moved, {
        kind: 'sighting',
        sighting: {
          observer: FRONT,
          subject: V1,
          rssi: dbmAtMeters(meters),
          atMs: 20_000,
        },
      });
      expect(zoneOf(next, V1)).toBe('mid');
      expect(alertKeys(next, FRONT)).toEqual([]);
    },
  );

  it("a visitor phone zones with its guide's distance, a guide phone with its own", () => {
    const visitorPhone = (alertMeters: number) =>
      last(
        run(
          join(visitor(V1), guideAt(alertMeters)),
          [{ observer: V1, subject: FRONT, rssi: at(40) }],
          0,
          5_000,
        ),
      );
    expect(zoneOf(visitorPhone(30), V1)).toBe('far');
    expect(zoneOf(visitorPhone(60), V1)).toBe('mid');

    const rearPhone = last(
      run(
        join({ ...rear, alertMeters: 60 }, guideAt(30), visitor(V1)),
        [{ observer: REAR, subject: V1, rssi: at(40) }],
        0,
        5_000,
      ),
    );
    expect(zoneOf(rearPhone, V1)).toBe('mid');
  });
});
