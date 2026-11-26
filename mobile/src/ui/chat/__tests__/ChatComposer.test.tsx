import { act } from 'react';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot, type TestInstance } from 'test-renderer';

import { ChatComposer, type ChatComposerProps, type ComposerVariant } from '../ChatComposer';

jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => true }));

const SEND = 'Enviar';
const PRESS = { nativeEvent: {}, stopPropagation: () => {}, preventDefault: () => {} };

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
  const button = () => one((n) => n.type === 'View' && n.props.accessibilityLabel === SEND);
  return {
    onSend,
    render,
    field,
    button,
    type: (text: string) => act(() => field().props.onChangeText(text)),
    submit: () => act(() => field().props.onSubmitEditing()),
    press: () => act(() => button().props.onClick(PRESS)),
  };
}

describe.each<ComposerVariant>(['floating', 'docked'])('ChatComposer (%s)', (variant) => {
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
    c.press();
    expect(c.onSend).toHaveBeenCalledWith('Hola');
  });

  it('ignores blank text', () => {
    const c = mount({ variant });
    c.type('   ');
    c.submit();
    c.press();
    expect(c.onSend).not.toHaveBeenCalled();
  });

  it('blocks sending while disabled and keeps the draft', () => {
    const c = mount({ variant, disabled: true });
    c.type('Pendiente');
    c.submit();
    c.press();
    expect(c.onSend).not.toHaveBeenCalled();
    expect(c.field().props.value).toBe('Pendiente');
    expect(c.button().props.accessibilityState).toEqual({ disabled: true });
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
});

describe('ChatComposer (docked)', () => {
  it('marks the send button disabled until there is text to send', () => {
    const c = mount({ variant: 'docked' });
    expect(c.button().props.accessibilityState).toEqual({ disabled: true });
    c.type('Hola');
    expect(c.button().props.accessibilityState).toEqual({ disabled: false });
    c.render({ variant: 'docked', disabled: true });
    expect(c.button().props.accessibilityState).toEqual({ disabled: true });
  });
});
