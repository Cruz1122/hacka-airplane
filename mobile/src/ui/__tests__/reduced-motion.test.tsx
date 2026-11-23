import { act } from 'react';
import { AccessibilityInfo } from 'react-native';
import { createRoot } from 'test-renderer';

import { ReducedMotionOverride, useReducedMotion } from '../useReducedMotion';

afterEach(() => jest.restoreAllMocks());

it.each([false, true])(
  'keeps system reduced motion (%s) when the workshop override changes',
  async (system) => {
    jest.spyOn(AccessibilityInfo, 'isReduceMotionEnabled').mockResolvedValue(system);
    const seen: boolean[] = [];
    function Probe() {
      seen.push(useReducedMotion());
      return null;
    }
    const root = createRoot();
    const render = async (value: boolean) => {
      await act(async () => {
        root.render(
          <ReducedMotionOverride.Provider value={value}>
            <Probe />
          </ReducedMotionOverride.Provider>,
        );
      });
    };
    await render(false);
    expect(seen.at(-1)).toBe(system);
    await render(true);
    expect(seen.at(-1)).toBe(true);
    await render(false);
    expect(seen.at(-1)).toBe(system);
    act(() => root.unmount());
  },
);
