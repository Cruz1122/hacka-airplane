import { act } from 'react';
import { Keyboard, Platform } from 'react-native';
import { createRoot } from 'test-renderer';

import { useChatKeyboard } from '../useChatKeyboard';

function mount(viewBottom = 0) {
  let current: ReturnType<typeof useChatKeyboard>;
  function Probe() {
    current = useChatKeyboard(viewBottom);
    return null;
  }
  const root = createRoot();
  act(() => root.render(<Probe />));
  return {
    now: () => current!,
    unmount: () => act(() => root.unmount()),
  };
}

const platform = Platform.OS;
const originalWindow = Object.getOwnPropertyDescriptor(globalThis, 'window');
const originalDocument = Object.getOwnPropertyDescriptor(globalThis, 'document');

class BrowserEvents {
  private listeners = new Map<string, Set<() => void>>();
  addEventListener = (name: string, listener: () => void) => {
    if (!this.listeners.has(name)) this.listeners.set(name, new Set());
    this.listeners.get(name)!.add(listener);
  };
  removeEventListener = (name: string, listener: () => void) => {
    this.listeners.get(name)?.delete(listener);
  };
  emit(name: string) {
    this.listeners.get(name)?.forEach((listener) => listener());
  }
}

function browser(height = 800, scale = 1) {
  const viewport = Object.assign(new BrowserEvents(), { height, offsetTop: 0, scale });
  const page = Object.assign(new BrowserEvents(), { innerHeight: 800, visualViewport: viewport });
  const doc = Object.assign(new BrowserEvents(), { activeElement: { tagName: 'INPUT' } });
  Object.defineProperty(globalThis, 'window', { configurable: true, value: page });
  Object.defineProperty(globalThis, 'document', { configurable: true, value: doc });
  return { viewport, page };
}
afterEach(() => {
  Platform.OS = platform;
  jest.restoreAllMocks();
  if (originalWindow) Object.defineProperty(globalThis, 'window', originalWindow);
  if (originalDocument) Object.defineProperty(globalThis, 'document', originalDocument);
  else Reflect.deleteProperty(globalThis, 'document');
});

it('lifts above the mobile browser keyboard and restores after it closes', () => {
  Platform.OS = 'web';
  const { viewport, page } = browser();
  const hook = mount();
  expect(hook.now()).toEqual({ open: false, bottom: 0 });
  act(() => {
    viewport.height = 480;
    viewport.emit('resize');
  });
  expect(hook.now()).toEqual({ open: true, bottom: 320 });
  act(() => {
    viewport.offsetTop = 40;
    viewport.emit('scroll');
  });
  expect(hook.now().bottom).toBe(280);
  // A browser that resizes the layout viewport must not get a second keyboard offset.
  act(() => {
    page.innerHeight = 480;
    viewport.offsetTop = 0;
    page.emit('resize');
  });
  expect(hook.now()).toEqual({ open: false, bottom: 0 });
  hook.unmount();
});

it('ignores pinch zoom and removes browser event subscriptions on unmount', () => {
  Platform.OS = 'web';
  const { viewport } = browser(400, 2);
  const remove = jest.spyOn(viewport, 'removeEventListener');
  const hook = mount();
  expect(hook.now()).toEqual({ open: false, bottom: 0 });
  hook.unmount();
  expect(remove.mock.calls.map(([event]) => event)).toEqual(['resize', 'scroll']);
});

it('native: lifts by what the keyboard covers of the chat view, 0 where the OS resized it', () => {
  Platform.OS = 'android';
  const callbacks = new Map<string, (e?: unknown) => void>();
  const remove = jest.fn();
  jest.spyOn(Keyboard, 'isVisible').mockReturnValue(false);
  jest.spyOn(Keyboard, 'addListener').mockImplementation((event, listener) => {
    callbacks.set(event, listener as (e?: unknown) => void);
    return { remove };
  });
  const show = (screenY: number) => ({ endCoordinates: { screenY, height: 0, screenX: 0, width: 0 } });
  // Edge to edge (Android 15+): the view still reaches the bottom of the window.
  const hook = mount(900);
  expect(hook.now()).toEqual({ open: false, bottom: 0 });
  act(() => callbacks.get('keyboardDidShow')!(show(560)));
  expect(hook.now()).toEqual({ open: true, bottom: 340 });
  act(() => callbacks.get('keyboardDidHide')!());
  expect(hook.now()).toEqual({ open: false, bottom: 0 });
  hook.unmount();
  expect(remove).toHaveBeenCalledTimes(2);
  // adjustResize did shrink the view to the keyboard's top: no second offset.
  const resized = mount(560);
  act(() => callbacks.get('keyboardDidShow')!(show(560)));
  expect(resized.now()).toEqual({ open: true, bottom: 0 });
  resized.unmount();
});
