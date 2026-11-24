import { act } from 'react';
import { Animated, Keyboard, Platform, StyleSheet } from 'react-native';
import { initialWindowMetrics } from 'react-native-safe-area-context';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot, type TestInstance } from 'test-renderer';

import { READY } from '@/design/fixtures';

import { chatLayout } from '../chatLayout';
import { ChatView, type ChatRow, type ChatViewProps } from '../ChatView';
import { headerScene } from '../headerScene';

// The list is a stub that records its props and scroll calls; the backdrop and the Pet are memo
// counters, so a test sees what a keyboard change re-renders. Skia never loads under Jest.
const mockList = {
  props: {} as Record<string, any>,
  renders: 0,
  scrollToEnd: jest.fn(),
  scrollToOffset: jest.fn(),
};
const mockRenders = { backdrop: 0, circle: 0 };
let mockReduced = false;

jest.mock('react-native-safe-area-context', () =>
  jest.requireActual('react-native-safe-area-context/jest/mock').default,
);
jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => mockReduced }));
jest.mock('@shopify/flash-list', () => {
  const { forwardRef: fwd, memo: m, useImperativeHandle: handle } = jest.requireActual('react');
  return {
    FlashList: m(
      fwd((props: Record<string, unknown>, ref: unknown) => {
        mockList.renders++;
        mockList.props = props;
        handle(ref, () => ({
          scrollToEnd: mockList.scrollToEnd,
          scrollToOffset: mockList.scrollToOffset,
        }));
        return null;
      }),
    ),
  };
});
jest.mock('../ChatBackdrop', () => ({
  ChatBackdrop: jest.requireActual('react').memo(() => {
    mockRenders.backdrop++;
    return null;
  }),
}));
jest.mock('../PetCircle', () => ({
  PetCircle: jest.requireActual('react').memo(() => {
    mockRenders.circle++;
    return null;
  }),
}));

const ROWS: ChatRow[] = [
  { id: '1', role: 'user', text: '¿Qué sendero corto hay?' },
  { id: '2', role: 'assistant', text: 'El Sendero del Pajonal.' },
];
const noop = () => {};
const PROPS: ChatViewProps = {
  messages: ROWS,
  busy: false,
  draft: '',
  model: READY,
  steps: [],
  state: '',
  sceneTime: null,
  onSend: noop,
  onReset: noop,
  onSettings: noop,
  onHistory: noop,
};

/** Each Animated.timing runs only when a test finishes it, so motion is stepped by hand. */
let pending: (() => void)[] = [];
const finishMotion = () =>
  act(() => {
    const due = pending;
    pending = [];
    due.forEach((f) => f());
  });
let frames: (() => void)[] = [];
const nextFrame = () =>
  act(() => {
    const due = frames;
    frames = [];
    due.forEach((f) => f());
  });

const keyboard = new Map<string, (e?: unknown) => void>();
const platform = Platform.OS;

function mount(props: Partial<ChatViewProps> = {}) {
  const root = createRoot();
  act(() => root.render(<ChatView {...PROPS} {...props} />));
  const input = () => root.container.queryAll((n) => n.type === 'TextInput')[0];
  /** How far the transforms of a node and its ancestors move it down (negative = up). */
  const shift = (node: TestInstance) => {
    let y = 0;
    for (let n: TestInstance | null = node; n; n = n.parent) {
      const transform = StyleSheet.flatten(n.props.style)?.transform as
        | { translateY?: number }[]
        | undefined;
      y += transform?.reduce((sum, t) => sum + (t.translateY ?? 0), 0) ?? 0;
    }
    return y;
  };
  /** The layout boxes (no transforms) of the composer's ancestors. */
  const boxes = () => {
    const out: unknown[] = [];
    for (let n: TestInstance | null = input(); n; n = n.parent) {
      const { top, bottom, height, flex } = StyleSheet.flatten(n.props.style) ?? {};
      out.push({ top, bottom, height, flex });
    }
    return out;
  };
  return {
    root,
    composerShift: () => shift(input()),
    boxes,
    listPad: () => StyleSheet.flatten(mockList.props.contentContainerStyle).paddingBottom,
    type: (text: string) => act(() => input().props.onChangeText(text)),
    submit: () => act(() => input().props.onSubmitEditing()),
    unmount: () => act(() => root.unmount()),
  };
}

const show = (screenY: number) => ({
  endCoordinates: { screenY, height: 0, screenX: 0, width: 0 },
});
const scrolled = (offset: number, content: number, viewport: number) => ({
  nativeEvent: {
    contentOffset: { x: 0, y: offset },
    contentSize: { width: 0, height: content },
    layoutMeasurement: { width: 0, height: viewport },
  },
});

beforeEach(() => {
  mockReduced = false;
  mockRenders.backdrop = 0;
  mockRenders.circle = 0;
  mockList.renders = 0;
  mockList.scrollToEnd.mockClear();
  mockList.scrollToOffset.mockClear();
  pending = [];
  frames = [];
  Platform.OS = 'android';
  jest.spyOn(Keyboard, 'isVisible').mockReturnValue(false);
  jest.spyOn(Keyboard, 'addListener').mockImplementation((event, listener) => {
    keyboard.set(event, listener as (e?: unknown) => void);
    return { remove: noop } as ReturnType<typeof Keyboard.addListener>;
  });
  jest.spyOn(global, 'requestAnimationFrame').mockImplementation((f) => {
    frames.push(() => f(0));
    return frames.length;
  });
  jest.spyOn(Animated, 'timing').mockImplementation((value, config) => {
    const v = value as Animated.Value;
    return {
      start: (done?: (result: { finished: boolean }) => void) =>
        pending.push(() => {
          v.setValue(config.toValue as number);
          done?.({ finished: true });
        }),
      stop: noop,
      reset: noop,
    };
  });
});
afterEach(() => {
  Platform.OS = platform;
  jest.restoreAllMocks();
});

describe('ChatView keyboard', () => {
  // useChatSize starts from the window (no layout event under Jest): its bottom is the window's.
  const { width, height } = jest.requireActual('react-native').Dimensions.get('window');
  const { insets } = initialWindowMetrics!;
  const lift = chatLayout(headerScene, width, height, insets).keyboardLift;
  const K = 340;

  it('moves the composer and the sheet by transforms only, re-rendering neither backdrop nor Pet', () => {
    const chat = mount();
    finishMotion();
    const before = chat.boxes();
    const renders = { ...mockRenders, list: mockList.renders };
    act(() => keyboard.get('keyboardDidShow')!(show(height - K)));
    finishMotion();
    expect(chat.composerShift()).toBe(-K);
    expect(chat.boxes()).toEqual(before);
    // The list re-renders once for its end padding: the part of it the composer covers.
    expect(chat.listPad()).toBe(K - lift);
    expect(mockList.renders - renders.list).toBe(1);
    expect(mockRenders).toEqual({ backdrop: renders.backdrop, circle: renders.circle });
    chat.unmount();
  });

  it('keeps the padding until the composer is down, scrolling back at the end first', () => {
    const chat = mount();
    act(() => keyboard.get('keyboardDidShow')!(show(height - K)));
    finishMotion();
    act(() => mockList.props.onScroll(scrolled(900, 1400, 500)));
    act(() => keyboard.get('keyboardDidHide')!());
    // Dropped now, the offset would clamp: the rows would fall a keyboard's height in one frame.
    expect(chat.listPad()).toBe(K - lift);
    expect(mockList.scrollToOffset).toHaveBeenCalledWith({ offset: 900 - (K - lift), animated: true });
    finishMotion();
    expect(chat.composerShift()).toBe(0);
    expect(chat.listPad()).toBe(0);
    chat.unmount();
  });

  it('lands at once under reduced motion', () => {
    mockReduced = true;
    const chat = mount();
    act(() => keyboard.get('keyboardDidShow')!(show(height - K)));
    expect(chat.composerShift()).toBe(-K);
    act(() => keyboard.get('keyboardDidHide')!());
    expect(chat.composerShift()).toBe(0);
    expect(chat.listPad()).toBe(0);
    chat.unmount();
  });
});

describe('ChatView fade in', () => {
  const opacity = (chat: ReturnType<typeof mount>) =>
    chat.root.container
      .queryAll((n) => n.type === 'View')
      .map((n) => StyleSheet.flatten(n.props.style)?.opacity)
      .find((o) => o !== undefined);

  it('fades the conversation in after the onboarding hands over', () => {
    const chat = mount({ fadeIn: true });
    expect(opacity(chat)).toBe(0);
    finishMotion();
    expect(opacity(chat)).toBe(1);
    chat.unmount();
  });

  it('shows it at once under reduced motion', () => {
    mockReduced = true;
    const chat = mount({ fadeIn: true });
    expect(opacity(chat)).toBe(1);
    chat.unmount();
  });
});

describe('ChatView follow', () => {
  it('scrolls to the end once per frame however often the content grows', () => {
    const chat = mount();
    nextFrame();
    mockList.scrollToEnd.mockClear();
    act(() => {
      mockList.props.onContentSizeChange(0, 1000);
      mockList.props.onContentSizeChange(0, 1020);
    });
    nextFrame();
    expect(mockList.scrollToEnd).toHaveBeenCalledTimes(1);
    chat.unmount();
  });

  it('drops a scroll already requested when the reader scrolls up before its frame', () => {
    const chat = mount();
    nextFrame();
    act(() => mockList.props.onScroll(scrolled(900, 1400, 500)));
    mockList.scrollToEnd.mockClear();
    act(() => mockList.props.onContentSizeChange(0, 1420));
    act(() => mockList.props.onScroll(scrolled(400, 1420, 500)));
    nextFrame();
    expect(mockList.scrollToEnd).not.toHaveBeenCalled();
    chat.unmount();
  });

  it('leaves a reader who scrolled up where they are until they send', () => {
    const onSend = jest.fn();
    const chat = mount({ onSend });
    nextFrame();
    act(() => mockList.props.onScroll(scrolled(900, 1400, 500)));
    act(() => mockList.props.onScroll(scrolled(400, 1400, 500)));
    mockList.scrollToEnd.mockClear();
    act(() => mockList.props.onContentSizeChange(0, 1420));
    nextFrame();
    expect(mockList.scrollToEnd).not.toHaveBeenCalled();
    // Back near the end, the list follows again.
    act(() => mockList.props.onScroll(scrolled(910, 1420, 500)));
    act(() => mockList.props.onContentSizeChange(0, 1440));
    nextFrame();
    expect(mockList.scrollToEnd).toHaveBeenCalledTimes(1);
    // A drag that moves nothing keeps following; one up and away from the end stops it.
    act(() => mockList.props.onScrollBeginDrag());
    act(() => mockList.props.onScrollEndDrag());
    act(() => mockList.props.onContentSizeChange(0, 1460));
    nextFrame();
    expect(mockList.scrollToEnd).toHaveBeenCalledTimes(2);
    act(() => mockList.props.onScroll(scrolled(960, 1460, 500)));
    act(() => mockList.props.onScrollBeginDrag());
    act(() => mockList.props.onScroll(scrolled(700, 1460, 500)));
    act(() => mockList.props.onScrollEndDrag());
    mockList.scrollToEnd.mockClear();
    act(() => mockList.props.onContentSizeChange(0, 1480));
    nextFrame();
    expect(mockList.scrollToEnd).not.toHaveBeenCalled();
    chat.type('¿Necesito guía?');
    chat.submit();
    expect(onSend).toHaveBeenCalledWith('¿Necesito guía?');
    act(() => mockList.props.onContentSizeChange(0, 1540));
    nextFrame();
    expect(mockList.scrollToEnd).toHaveBeenCalledTimes(1);
    chat.unmount();
  });
});
