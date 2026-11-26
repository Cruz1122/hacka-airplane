// The radio-free, animation-free half of the slider: geometry and the screen-reader actions.
import { act } from 'react';
import { createRoot, type TestInstance } from 'test-renderer';

import { Slider, SLIDER_THUMB, sliderValueAt, sliderX } from '../Slider';

// No jest setup wires Reanimated or gesture-handler (their own mocks boot the native module), so
// plain stand-ins: the drag itself is checked in a browser, not here.
jest.mock('react-native-reanimated', () => {
  const { View } = jest.requireActual('react-native');
  return {
    __esModule: true,
    default: { View },
    useSharedValue: (value: number) => ({
      value,
      set(v: number) {
        this.value = v;
      },
    }),
    useAnimatedStyle: (style: () => object) => style(),
    withTiming: (value: number) => value,
  };
});
jest.mock('react-native-gesture-handler', () => {
  const { View } = jest.requireActual('react-native');
  return {
    GestureHandlerRootView: View,
    GestureDetector: ({ children }: { children: unknown }) => children,
    usePanGesture: () => ({}),
  };
});

const range = { min: 5, max: 150, step: 5 };
const W = 300;

describe('Slider geometry', () => {
  it('maps the ends of the thumb travel to min and max, and steps in between', () => {
    expect(sliderValueAt(SLIDER_THUMB / 2, W, range)).toBe(5);
    expect(sliderValueAt(W - SLIDER_THUMB / 2, W, range)).toBe(150);
    expect(sliderValueAt(-50, W, range)).toBe(5);
    expect(sliderValueAt(W + 50, W, range)).toBe(150);
    expect(sliderValueAt(sliderX(60, W, range) + 1, W, range)).toBe(60);
  });

  it('places every step where dragging there reads it back', () => {
    for (let v = range.min; v <= range.max; v += range.step) {
      expect(sliderValueAt(sliderX(v, W, range), W, range)).toBe(v);
    }
  });
});

describe('Slider for screen readers', () => {
  it('is adjustable, reads its value and steps with increment/decrement inside the range', () => {
    const changes: number[] = [];
    const root = createRoot();
    const render = (value: number) =>
      act(() =>
        root.render(
          <Slider
            {...range}
            value={value}
            onChange={(v) => changes.push(v)}
            label="Distancia de alerta"
            valueText={`${value} m`}
          />,
        ),
      );
    render(30);
    const node = root.container.queryAll(
      (n: TestInstance) => n.props.accessibilityRole === 'adjustable',
    )[0];
    expect(node.props).toMatchObject({
      'aria-valuemin': 5,
      'aria-valuemax': 150,
      'aria-valuenow': 30,
      'aria-valuetext': '30 m',
    });
    act(() => node.props.onAccessibilityAction({ nativeEvent: { actionName: 'increment' } }));
    act(() => node.props.onAccessibilityAction({ nativeEvent: { actionName: 'decrement' } }));
    render(150);
    const top = root.container.queryAll(
      (n: TestInstance) => n.props.accessibilityRole === 'adjustable',
    )[0];
    act(() => top.props.onAccessibilityAction({ nativeEvent: { actionName: 'increment' } }));
    expect(changes).toEqual([35, 25]);
    act(() => root.unmount());
  });
});
