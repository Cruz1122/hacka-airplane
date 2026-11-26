// How much of the chat the keyboard covers. Native: Android 15+ draws edge to edge, where
// adjustResize no longer shrinks the window, so the occlusion comes from the keyboard's top edge
// against the chat view's bottom (0 when the platform did resize the view). Mobile browsers
// shrink visualViewport while leaving the layout viewport (and absolute footer) intact.
import { useEffect, useState } from 'react';
import { Keyboard, type KeyboardEvent, Platform } from 'react-native';

interface ChatKeyboard {
  open: boolean;
  /** Points of the chat view hidden under the keyboard. */
  bottom: number;
}

/**
 * @param viewBottom the chat view's bottom edge in window coordinates (measureInWindow y + height);
 *   native only, ignored on web.
 */
export function useChatKeyboard(viewBottom = 0): ChatKeyboard {
  const [web, setWeb] = useState<ChatKeyboard>({ open: false, bottom: 0 });
  // Native: the keyboard's top edge in window coordinates while it is shown, else null.
  const [keyboardTop, setKeyboardTop] = useState<number | null>(() =>
    Platform.OS !== 'web' && Keyboard.isVisible() ? (Keyboard.metrics()?.screenY ?? null) : null,
  );
  useEffect(() => {
    if (Platform.OS !== 'web') {
      const show = Keyboard.addListener(
        Platform.OS === 'ios' ? 'keyboardWillShow' : 'keyboardDidShow',
        (e: KeyboardEvent) => setKeyboardTop(e.endCoordinates.screenY),
      );
      const hide = Keyboard.addListener(
        Platform.OS === 'ios' ? 'keyboardWillHide' : 'keyboardDidHide',
        () => setKeyboardTop(null),
      );
      return () => {
        show.remove();
        hide.remove();
      };
    }
    if (typeof window === 'undefined' || !window.visualViewport) return;
    const viewport = window.visualViewport;
    const update = (open: boolean, bottom: number) =>
      setWeb((previous) =>
        previous.open === open && previous.bottom === bottom ? previous : { open, bottom },
      );
    const sync = () => {
      const active = document.activeElement;
      const editing = active?.tagName === 'INPUT' || active?.tagName === 'TEXTAREA' ||
        (active instanceof HTMLElement && active.isContentEditable);
      // Pinch zoom also shrinks visualViewport. It is not keyboard occlusion.
      const bottom = editing && viewport.scale === 1
        ? Math.max(0, window.innerHeight - viewport.height - viewport.offsetTop)
        : 0;
      update(bottom > 0, bottom);
    };
    sync();
    viewport.addEventListener('resize', sync);
    viewport.addEventListener('scroll', sync);
    window.addEventListener('resize', sync);
    document.addEventListener('focusin', sync);
    document.addEventListener('focusout', sync);
    return () => {
      viewport.removeEventListener('resize', sync);
      viewport.removeEventListener('scroll', sync);
      window.removeEventListener('resize', sync);
      document.removeEventListener('focusin', sync);
      document.removeEventListener('focusout', sync);
    };
  }, []);
  if (Platform.OS === 'web') return web;
  if (keyboardTop === null) return CLOSED;
  return { open: true, bottom: Math.max(0, Math.round(viewBottom - keyboardTop)) };
}

const CLOSED: ChatKeyboard = { open: false, bottom: 0 };
