import { act } from 'react';
import { createRoot } from 'test-renderer';

import type { VoiceState } from '@/ui/pet/petCore';

import { PetCircle } from '../PetCircle';

let mockEmotion: string | undefined;
let mockFocused = true;
let mockReduced = false;
jest.mock('@/ui/pet/Pet', () => ({
  Pet: ({ emotion }: { emotion: string }) => {
    mockEmotion = emotion;
    return null;
  },
}));
jest.mock('expo-router', () => ({ useIsFocused: () => mockFocused }));
jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => mockReduced }));
jest.mock('@/ui/useAccessibilityTheme', () => ({
  useAccessibilityTheme: () => ({ palette: jest.requireActual('@/ui/theme/tokens').brand }),
}));

function mount() {
  const root = createRoot();
  const render = (voice: VoiceState = 'idle', hidden = false, x = 60) =>
    act(() => root.render(<PetCircle x={x} y={60} r={60} voice={voice} hidden={hidden} ready />));
  render();
  return { root, render };
}
const wait = (ms: number) => act(() => jest.advanceTimersByTime(ms));

describe('occasional pet emotions', () => {
  beforeEach(() => {
    jest.useFakeTimers();
    jest.spyOn(Math, 'random').mockReturnValue(0);
    jest.spyOn(globalThis, 'setTimeout');
    mockFocused = true;
    mockReduced = false;
  });
  afterEach(() => {
    jest.restoreAllMocks();
    jest.useRealTimers();
  });

  it('shows brief, different gestures separated by quiet pauses', () => {
    const { root } = mount();
    expect(mockEmotion).toBe('happy');
    wait(11999);
    expect(mockEmotion).toBe('happy');
    wait(1);
    expect(mockEmotion).toBe('curious');
    wait(2200);
    expect(mockEmotion).toBe('happy');
    wait(12000);
    expect(mockEmotion).toBe('surprised');
    wait(2200 + 12000);
    expect(mockEmotion).toBe('excited');
    act(() => root.unmount());
    const scheduled = jest.mocked(setTimeout).mock.calls.length;
    wait(60000);
    expect(jest.mocked(setTimeout).mock.calls).toHaveLength(scheduled);
  });

  it('gives conversation states priority and restarts the quiet pause afterward', () => {
    const { root, render } = mount();
    wait(12000);
    render('thinking');
    expect(mockEmotion).toBe('thinking');
    wait(30000);
    expect(mockEmotion).toBe('thinking');
    render('speaking');
    expect(mockEmotion).toBe('speaking');
    render('idle');
    expect(mockEmotion).toBe('happy');
    wait(12000);
    expect(mockEmotion).toBe('curious');
    act(() => root.unmount());
  });

  it('cancels gestures when hidden or unfocused', () => {
    const { root, render } = mount();
    wait(12000);
    render('idle', true);
    expect(mockEmotion).toBe('happy');
    wait(30000);
    expect(mockEmotion).toBe('happy');
    mockFocused = false;
    render('idle', false);
    wait(30000);
    expect(mockEmotion).toBe('happy');
    mockFocused = true;
    render('idle', false, 61);
    wait(12000);
    expect(mockEmotion).toBe('curious');
    act(() => root.unmount());
  });

  it('keeps a steady expression with reduced motion, including mid-gesture changes', () => {
    const { root, render } = mount();
    wait(12000);
    mockReduced = true;
    render('idle', false, 61);
    expect(mockEmotion).toBe('happy');
    wait(60000);
    expect(mockEmotion).toBe('happy');
    act(() => root.unmount());
    const scheduled = jest.mocked(setTimeout).mock.calls.length;
    wait(60000);
    expect(jest.mocked(setTimeout).mock.calls).toHaveLength(scheduled);
  });
});
