import { act } from 'react';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot, type TestInstance } from 'test-renderer';

import { t } from '@/i18n';

import { ComposerLab } from '../ComposerLab';
import { COMPOSER_TEXT, DEMO_REPLY, DEMO_SEND_MS } from '../fixtures';

jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => true }));

const w = t.dev.workshop;
const PRESS = { nativeEvent: {}, stopPropagation: () => {}, preventDefault: () => {} };

function mount() {
  const root = createRoot();
  act(() => root.render(<ComposerLab wide={false} reducedMotion />));
  const all = (pred: (n: TestInstance) => boolean) => root.container.queryAll(pred);
  const byLabel = (label: string) => {
    const found = all((n) => n.type === 'View' && n.props.accessibilityLabel === label);
    expect(found).toHaveLength(1);
    return found[0];
  };
  const texts = () => all((n) => n.type === 'Text').map((n) => [n.props.children].flat().join(''));
  const field = () => all((n) => n.type === 'TextInput')[0];
  return {
    texts,
    field,
    send: () => byLabel(t.send),
    press: (label: string) => act(() => byLabel(label).props.onClick(PRESS)),
    type: (text: string) => act(() => field().props.onChangeText(text)),
    submit: () => act(() => field().props.onSubmitEditing()),
    typing: () => all((n) => n.props.accessibilityRole === 'progressbar').length > 0,
  };
}

describe('ComposerLab', () => {
  beforeEach(() => jest.useFakeTimers());
  afterEach(() => jest.useRealTimers());

  it('applies content presets to the real composer', () => {
    const lab = mount();
    expect(lab.field().props.value).toBe('');
    lab.press(w.presetLong);
    expect(lab.field().props.value).toBe(COMPOSER_TEXT.long);
    lab.press(w.presetPending);
    expect(lab.field().props.value).toBe(COMPOSER_TEXT.pending);
    expect(lab.send().props.accessibilityState).toEqual({ disabled: true });
    expect(lab.texts()).toContain(w.stateDisabled);
  });

  it('sends, shows the sending state, then lands the sample reply', () => {
    const lab = mount();
    lab.type('¿Hay refugio?');
    lab.submit();
    expect(lab.texts()).toEqual(expect.arrayContaining(['¿Hay refugio?', w.stateSending]));
    expect(lab.typing()).toBe(true);
    lab.type('otra');
    expect(lab.send().props.accessibilityState).toEqual({ disabled: true });

    act(() => jest.advanceTimersByTime(DEMO_SEND_MS));
    expect(lab.typing()).toBe(false);
    expect(lab.texts()).toEqual(expect.arrayContaining([DEMO_REPLY, w.stateTyping]));
    expect(lab.send().props.accessibilityState).toEqual({ disabled: false });
  });

  it('reflects manual typing and clearing in its visible state', () => {
    const lab = mount();
    expect(lab.texts()).toContain(w.stateIdle);
    lab.type('¿Hay refugio?');
    expect(lab.texts()).toContain(w.stateTyping);
    lab.type('');
    expect(lab.texts()).toContain(w.stateIdle);
  });

  it('reset clears the sent messages and a pending reply', () => {
    const lab = mount();
    lab.type('Hola');
    lab.submit();
    lab.press(w.reset);
    act(() => jest.advanceTimersByTime(DEMO_SEND_MS));
    expect(lab.texts()).not.toContain('Hola');
    expect(lab.texts()).not.toContain(DEMO_REPLY);
    expect(lab.texts()).toContain(w.nothingSent);
  });
});
