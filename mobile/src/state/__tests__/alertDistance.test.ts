// jest.mock is hoisted above the import: the store never touches the real kv-store.
import Storage from 'expo-sqlite/kv-store';

import { parseAlertMeters, setAlertDistance, snapAlertMeters } from '../alertDistance';

jest.mock('expo-sqlite/kv-store', () => ({
  __esModule: true,
  default: { getItemAsync: jest.fn(async () => null), setItemAsync: jest.fn(async () => {}) },
}));

describe('alert distance', () => {
  it('snaps to the 5 m step inside 5..150 m', () => {
    expect([snapAlertMeters(32), snapAlertMeters(33), snapAlertMeters(0)]).toEqual([30, 35, 5]);
    expect(snapAlertMeters(400)).toBe(150);
  });

  it('reads a saved value and falls back to 30 m when missing or damaged', () => {
    expect(parseAlertMeters('60')).toBe(60);
    expect(parseAlertMeters(null)).toBe(30);
    expect(parseAlertMeters('far')).toBe(30);
  });

  it('saves a new value once, snapped', () => {
    setAlertDistance(61);
    setAlertDistance(60);
    expect(Storage.setItemAsync).toHaveBeenCalledTimes(1);
    expect(Storage.setItemAsync).toHaveBeenCalledWith('group.alertMeters.v1', '60');
  });
});
