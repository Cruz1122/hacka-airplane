import { act } from 'react';
import { Animated } from 'react-native';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot, type TestInstance } from 'test-renderer';

import { fill, t } from '@/i18n';

import { ChatBubble, type ChatBubbleProps } from '../ChatBubble';
import type { ChatSource } from '../citations';

let mockReduced = false;
jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => mockReduced }));

const PRESS = { nativeEvent: {}, stopPropagation: () => {}, preventDefault: () => {} };
const SOURCES: ChatSource[] = [
  { id: 'EST-D-01', title: 'Estación Refugio Quelital', excerpt: 'Abre a las 06:10.' },
  { id: 'PAR-07', title: 'Parque', excerpt: 'Protector FPS 85.' },
];

function mount(props: ChatBubbleProps) {
  const root = createRoot();
  const render = (p: ChatBubbleProps) => act(() => root.render(<ChatBubble {...p} />));
  render(props);
  const all = (pred: (n: TestInstance) => boolean) => root.container.queryAll(pred);
  return {
    render,
    text: () =>
      all((n) => n.type === 'Text')
        .map((n) => [n.props.children].flat().join(''))
        .join('|'),
    buttons: () => all((n) => n.type === 'View' && n.props.accessibilityRole === 'button'),
  };
}

describe('ChatBubble', () => {
  let timing: jest.SpyInstance;
  beforeEach(() => {
    mockReduced = false;
    timing = jest
      .spyOn(Animated, 'timing')
      .mockImplementation(() => ({ start: jest.fn(), stop: jest.fn(), reset: jest.fn() }));
  });
  afterEach(() => timing.mockRestore());

  it('enters once and not again while the streamed answer grows', () => {
    const b = mount({ role: 'assistant', text: 'Abre' });
    b.render({ role: 'assistant', text: 'Abre a las 06:10 [fue' });
    expect(b.text()).toBe('Abre a las 06:10');
    b.render({ role: 'assistant', text: 'Abre a las 06:10 [fuente: EST-D-01].' });
    expect(b.text()).toBe('Abre a las 06:10.');
    expect(timing).toHaveBeenCalledTimes(1);
  });

  it('appears at once under reduced motion', () => {
    mockReduced = true;
    mount({ role: 'assistant', text: 'Hola' });
    expect(timing).not.toHaveBeenCalled();
  });

  it('opens the sources of an assistant answer from its corner button', () => {
    const onOpenSources = jest.fn();
    const b = mount({
      role: 'assistant',
      text: 'Dato [fuente: EST-D-01]',
      sources: SOURCES,
      onOpenSources,
    });
    const [button] = b.buttons();
    expect(b.buttons()).toHaveLength(1);
    expect(button.props.accessibilityLabel).toBe(fill(t.chatScreen.sources.showMany, { n: 2 }));
    act(() => button.props.onClick(PRESS));
    expect(onOpenSources).toHaveBeenCalledWith(SOURCES);
  });

  it('has no source button without sources, and shows the user words as typed', () => {
    const onOpenSources = jest.fn();
    expect(
      mount({ role: 'assistant', text: 'Hola', sources: [], onOpenSources }).buttons(),
    ).toEqual([]);
    const mine = mount({
      role: 'user',
      text: 'Cita [fuente: EST-D-01]',
      sources: SOURCES,
      onOpenSources,
    });
    expect(mine.buttons()).toEqual([]);
    expect(mine.text()).toBe('Cita [fuente: EST-D-01]');
  });
});
