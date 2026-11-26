import { step } from '../groupState';
import { lane } from '../lane';
import { GROUP_POLICY } from '../policy';
import { dbmAtMeters, zoneCuts } from '../signal';
import { front, FRONT, join, last, rear, REAR, run, V1, V2, visitor, type Feed } from '../testing';
import { memberId } from '../types';

const { unseenAfterMs } = GROUP_POLICY;
const CUT = zoneCuts(GROUP_POLICY.alertMeters.default);
const V3 = memberId('v3');
const feed = (observer: typeof FRONT, subject: typeof V1, rssi: number): Feed => ({
  observer,
  subject,
  rssi: () => rssi,
});
const dot = (s: Parameters<typeof lane>[0], id: typeof V1) =>
  lane(s, FRONT).dots.find((d) => d.id === id)!;

describe('lane', () => {
  it('one guide: the guide tops the line and dots follow their signal', () => {
    const s = last(
      run(
        join(front, visitor(V1), visitor(V2), visitor(V3)),
        [
          feed(FRONT, V1, CUT.midMinDbm - 5),
          feed(FRONT, V2, CUT.nearMinDbm + 8),
          feed(FRONT, V3, CUT.midMinDbm + 4),
        ],
        0,
        20_000,
      ),
    );
    const l = lane(s, FRONT);
    expect(l.top?.id).toBe(FRONT);
    expect(l.bottom).toBeNull();
    expect(l.dots.map((d) => d.id)).toEqual([V1, V2, V3]);
    const [far, near, mid] = l.dots;
    expect([near.status, mid.status, far.status]).toEqual(['near', 'mid', 'far']);
    expect(0 <= near.t && near.t < mid.t && mid.t < far.t && far.t <= 1).toBe(true);
  });

  it('two guides: a dot heard by both sits between the ends, nearer the louder guide', () => {
    const s = last(
      run(
        join(front, rear, visitor(V1), visitor(V2)),
        [feed(FRONT, V1, -70), feed(REAR, V1, -85), feed(FRONT, V2, -80), feed(REAR, V2, -80)],
        0,
        20_000,
      ),
    );
    const l = lane(s, FRONT);
    expect([l.top?.id, l.bottom?.id]).toEqual([FRONT, REAR]);
    expect(dot(s, V1).t).toBeGreaterThan(0);
    expect(dot(s, V1).t).toBeLessThan(0.5);
    expect(dot(s, V2).t).toBeCloseTo(0.5, 1);
  });

  it('one guide: an unseen dot keeps its last t', () => {
    const heard = run(join(front, visitor(V1)), [feed(FRONT, V1, -85)], 0, 10_000);
    const tracked = dot(last(heard), V1);
    const quiet = last(run(last(heard), [], 10_000, 10_000 + 2 * unseenAfterMs));
    expect(dot(quiet, V1)).toMatchObject({ status: 'unseen', t: tracked.t });
  });

  it('two guides losing the dot at different times: it keeps the t it had last', () => {
    const s0 = join(front, rear, visitor(V1));
    const both = run(s0, [feed(FRONT, V1, -72), feed(REAR, V1, -88)], 0, 10_000);
    const rearOnly = run(last(both), [feed(REAR, V1, -88)], 10_000, 15_000);
    // Watch the dot until it goes unseen; the last tracked frame is what the guide saw.
    const quiet = run(last(rearOnly), [], 15_000, 15_000 + 2 * unseenAfterMs);
    const frames = [...rearOnly, ...quiet].map((f) => dot(f.state, V1));
    const firstUnseen = frames.findIndex((d) => d.status === 'unseen');
    expect(firstUnseen).toBeGreaterThan(0);
    const lastTracked = frames[firstUnseen - 1];
    // Front went stale first, so by then the dot was placed from the rear end alone, not where
    // both guides put it.
    expect(lastTracked.t).not.toBeCloseTo(dot(last(both), V1).t, 2);
    expect(frames[frames.length - 1]).toMatchObject({
      status: 'unseen',
      t: lastTracked.t,
    });
  });

  it('one guide: the line is meters, with the alert distance at t = 2/3', () => {
    const guide = { ...front, alertMeters: 30 };
    const at30 = last(run(join(guide, visitor(V1)), [feed(FRONT, V1, dbmAtMeters(30))], 0, 10_000));
    const l = lane(at30, FRONT);
    expect(l.scale?.meters).toBe(45);
    expect(l.scale?.marks).toEqual([
      { kind: 'near', meters: 15, t: 1 / 3 },
      { kind: 'alert', meters: 30, t: 2 / 3 },
    ]);
    expect(dot(at30, V1).t).toBeCloseTo(2 / 3, 6);

    // At 60 m the same visitor sits halfway to the alert mark.
    const wider = step(at30, {
      kind: 'joined',
      member: { ...guide, alertMeters: 60 },
    });
    expect(lane(wider, FRONT).scale?.meters).toBe(90);
    expect(dot(wider, V1).t).toBeCloseTo(1 / 3, 6);
  });

  it('one guide: beyond 1.5 alert distances a dot pins to the end; two guides have no scale', () => {
    const s = last(run(join(front, visitor(V1)), [feed(FRONT, V1, dbmAtMeters(200))], 0, 20_000));
    expect(dot(s, V1).t).toBe(1);
    expect(lane(join(front, rear), FRONT).scale).toBeNull();
  });
});
