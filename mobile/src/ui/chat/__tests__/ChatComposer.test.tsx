import { act } from 'react';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot, type TestInstance } from 'test-renderer';

import { t } from '@/i18n';
import type { DictateCallbacks } from '@/speech/dictate';
import { ChatComposer, type ChatComposerProps, type ComposerVariant } from '../ChatComposer';

jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => true }));

const mockStartDictate = jest.fn((cb: DictateCallbacks) => Promise.resolve());
const mockStopDictate = jest.fn();
const mockCancelDictate = jest.fn();

jest.mock('@/speech/dictate', () => ({
  startDictate: (cb: DictateCallbacks) => mockStartDictate(cb),
  stopDictate: () => mockStopDictate(),
  cancelDictate: () => mockCancelDictate(),
}));

const SEND = t.send;
const MIC = t.chatScreen.voice.mic;
const PRESS = {
  nativeEvent: { pageX: 1, pageY: 1, timestamp: 1 },
  persist: () => {},
  stopPropagation: () => {},
  preventDefault: () => {},
};

function mount(props: Partial<ChatComposerProps>) {
  const onSend = jest.fn();
  const root = createRoot();
  const render = (p: Partial<ChatComposerProps>) =>
    act(() =>
      root.render(
        <ChatComposer
          disabled={false}
          placeholder="Pregunta"
          sendLabel={SEND}
          onSend={onSend}
          {...p}
        />,
      ),
    );
  render(props);
  const one = (pred: (n: TestInstance) => boolean) => {
    const found = root.container.queryAll(pred);
    expect(found).toHaveLength(1);
    return found[0];
  };
  const field = () => one((n) => n.type === 'TextInput');
  const byLabel = (label: string) =>
    one((n) => n.type === 'View' && n.props.accessibilityLabel === label);
  return {
    onSend,
    render,
    field,
    send: () => byLabel(SEND),
    mic: () => byLabel(MIC),
    all: (pred: (n: TestInstance) => boolean) => root.container.queryAll(pred),
    type: (text: string) => act(() => field().props.onChangeText(text)),
    submit: () => act(() => field().props.onSubmitEditing()),
    pressSend: () => act(() => byLabel(SEND).props.onClick(PRESS)),
    holdMic: async () => {
      await act(async () => {
        byLabel(MIC).props.onResponderGrant(PRESS);
      });
    },
  };
}

describe.each<ComposerVariant>(['floating', 'docked'])('ChatComposer (%s)', (variant) => {
  beforeEach(() => {
    mockStartDictate.mockReset();
    mockStopDictate.mockReset();
    mockCancelDictate.mockReset();
    mockStartDictate.mockResolvedValue(undefined);
  });

  it('sends the typed text from the keyboard and clears the field', () => {
    const c = mount({ variant });
    c.type('¿Hay refugio?');
    c.submit();
    expect(c.onSend).toHaveBeenCalledWith('¿Hay refugio?');
    expect(c.field().props.value).toBe('');
  });

  it('sends from the button', () => {
    const c = mount({ variant });
    c.type('Hola');
    c.pressSend();
    expect(c.onSend).toHaveBeenCalledWith('Hola');
  });

  it('ignores blank text from the keyboard', () => {
    const c = mount({ variant });
    c.type('   ');
    c.submit();
    expect(c.onSend).not.toHaveBeenCalled();
  });

  it('blocks sending while disabled and keeps the draft', () => {
    const c = mount({ variant, disabled: true });
    c.type('Pendiente');
    c.submit();
    c.pressSend();
    expect(c.onSend).not.toHaveBeenCalled();
    expect(c.field().props.value).toBe('Pendiente');
    expect(c.send().props.accessibilityState).toEqual({ disabled: true });
  });

  it('reports empty/non-empty transitions without reporting every keystroke', () => {
    const onHasTextChange = jest.fn();
    const c = mount({ variant, onHasTextChange });
    expect(onHasTextChange.mock.calls).toEqual([[false]]);
    c.type('H');
    c.type('Hola');
    expect(onHasTextChange.mock.calls).toEqual([[false], [true]]);
    c.type('');
    expect(onHasTextChange.mock.calls).toEqual([[false], [true], [false]]);
  });

  it('starts from initialText', () => {
    const c = mount({ variant, initialText: 'Texto de muestra' });
    expect(c.field().props.value).toBe('Texto de muestra');
    c.submit();
    expect(c.onSend).toHaveBeenCalledWith('Texto de muestra');
  });

  it('shows a microphone until there is text to send', () => {
    const c = mount({ variant });
    expect(c.mic().props.accessibilityState).toEqual({ disabled: false, busy: false });
    c.type('Hola');
    expect(c.send().props.accessibilityLabel).toBe(SEND);
  });

  it('starts dictation when the microphone is held', async () => {
    const c = mount({ variant });
    await c.holdMic();
    expect(mockStartDictate).toHaveBeenCalledTimes(1);
    expect(c.onSend).not.toHaveBeenCalled();
  });
});

describe('ChatComposer (docked)', () => {
  beforeEach(() => {
    mockStartDictate.mockReset();
    mockStopDictate.mockReset();
    mockStartDictate.mockResolvedValue(undefined);
  });

  it('keeps the microphone disabled while the composer is disabled', () => {
    const c = mount({ variant: 'docked', disabled: true });
    expect(c.mic().props.accessibilityState).toEqual({ disabled: true, busy: false });
  });

  it('shows the framed photo attachment preview, enables sending, and removes it on press', () => {
    const onRemovePhoto = jest.fn();
    const c = mount({ variant: 'docked', photoUri: 'file:///frailejon.jpg', onRemovePhoto });
    expect(c.send().props.accessibilityState).toEqual({ disabled: false });
    expect(c.all((n) => n.type === 'Image')).toHaveLength(1);
    const removeBtn = c.all(
      (n) => n.type === 'View' && n.props.accessibilityLabel === 'Quitar foto',
    );
    expect(removeBtn).toHaveLength(1);
    act(() => removeBtn[0].props.onClick(PRESS));
    expect(onRemovePhoto).toHaveBeenCalledTimes(1);
  });
});
