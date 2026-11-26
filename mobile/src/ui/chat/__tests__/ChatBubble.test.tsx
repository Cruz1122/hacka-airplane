import { act, Profiler } from 'react';
import { Animated, StyleSheet } from 'react-native';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot, type TestInstance } from 'test-renderer';

import { fill, t } from '@/i18n';
import { fonts } from '@/ui/theme/tokens';

import { ChatBubble, type ChatBubbleProps, markEntered } from '../ChatBubble';
import type { ChatSource } from '../citations';
import { replyReveal, WORDS_PER_SECOND } from '../reveal';

let mockReduced = false;
jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => mockReduced }));

const PRESS = { nativeEvent: {}, stopPropagation: () => {}, preventDefault: () => {} };
const SOURCES: ChatSource[] = [
  { id: 'EST-D-01', title: 'Estación Refugio Quelital', excerpt: 'Abre a las 06:10.' },
  { id: 'PAR-07', title: 'Parque', excerpt: 'Protector FPS 85.' },
];

const flat = (n: TestInstance | string): string =>
  typeof n === 'string' ? n : n.children.map(flat).join('');

function mount(props: ChatBubbleProps) {
  const root = createRoot();
  const render = (p: ChatBubbleProps) => act(() => root.render(<ChatBubble {...p} />));
  render(props);
  const all = (pred: (n: TestInstance) => boolean) => root.container.queryAll(pred);
  return {
    root,
    render,
    /** Each outermost Text's whole content, nested bold runs included. */
    text: () =>
      all((n) => n.type === 'Text' && n.parent?.type !== 'Text')
        .map(flat)
        .join('|'),
    bold: () => all((n) => n.type === 'Text' && n.props.style?.fontFamily === fonts.bold).map(flat),
    label: () => all((n) => n.type === 'View' && n.props.accessible)[0]?.props.accessibilityLabel,
    /** The row's entry opacity. */
    opacity: () =>
      all((n) => n.type === 'View' && StyleSheet.flatten(n.props.style)?.opacity !== undefined)[0]
        ?.props.style,
    buttons: () => all((n) => n.type === 'View' && n.props.accessibilityRole === 'button'),
  };
}

const MS = 1000 / WORDS_PER_SECOND;
let clock = 0;
let frames: (() => void)[] = [];
/** Runs the reveal loop's pending frames as if `ms` had passed. */
const advance = (ms: number) =>
  act(() => {
    clock += ms;
    const due = frames;
    frames = [];
    due.forEach((f) => f());
  });
let ids = 0;
/** A reply the chat has just scheduled, under a fresh row id. */
/** Every row scheduled so far: the chat always hands the store its whole conversation. */
const rows: { id: string; role: 'assistant'; text: string }[] = [];
function scheduled(text: string) {
  const id = `r${++ids}`;
  rows.push({ id, role: 'assistant', text });
  act(() => replyReveal.schedule(rows, new Set(), clock));
  return id;
}

describe('ChatBubble', () => {
  let timing: jest.SpyInstance;
  beforeEach(() => {
    mockReduced = false;
    timing = jest
      .spyOn(Animated, 'timing')
      .mockImplementation(() => ({ start: jest.fn(), stop: jest.fn(), reset: jest.fn() }));
    jest.spyOn(performance, 'now').mockImplementation(() => clock);
    jest.spyOn(global, 'requestAnimationFrame').mockImplementation((f) => {
      frames.push(() => f(clock));
      return frames.length;
    });
  });
  afterEach(() => {
    // Let every stream of this test end, and its queue run out, before the next test.
    while (frames.length) advance(1000);
    clock += 1000;
    jest.restoreAllMocks();
  });

  it('enters once and not again while the streamed answer grows', () => {
    const b = mount({ role: 'assistant', text: 'Abre' });
    b.render({ role: 'assistant', text: 'Abre a las 06:10 [fue' });
    expect(b.text()).toBe('Abre a las 06:10');
    b.render({ role: 'assistant', text: 'Abre a las 06:10 [fuente: EST-D-01].' });
    expect(b.text()).toBe('Abre a las 06:10.');
    expect(timing).toHaveBeenCalledTimes(1);
  });

  it('enters once per row, also when a recycled cell shows that row again', () => {
    const opacity = (b: ReturnType<typeof mount>) => StyleSheet.flatten(b.opacity()).opacity;
    const b = mount({ role: 'user', text: 'Hola', entryId: 'e1' });
    expect(timing).toHaveBeenCalledTimes(1);
    // FlashList hands the cell to a new row: hidden from its first frame, then it enters.
    b.render({ role: 'user', text: 'Otra', entryId: 'e2' });
    expect(opacity(b)).toBe(0);
    expect(timing).toHaveBeenCalledTimes(2);
    // Scrolled back to the first row: it shows at once.
    b.render({ role: 'user', text: 'Hola', entryId: 'e1' });
    expect(opacity(b)).toBe(1);
    expect(timing).toHaveBeenCalledTimes(2);
  });

  it('shows rows the reader has already seen without an entry', () => {
    markEntered(['seen']);
    mount({ role: 'user', text: 'Hola', entryId: 'seen' });
    expect(timing).not.toHaveBeenCalled();
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

  it('types a reply out word by word, then shows its meta and source button', () => {
    const text = 'Abre a las 06:10 en Quelital.';
    const id = scheduled(text);
    const b = mount({
      role: 'assistant',
      text,
      meta: '0.6 s',
      sources: SOURCES,
      onOpenSources: jest.fn(),
      revealId: id,
    });
    expect(b.text()).toBe('Abre ');
    expect(b.label()).toBe(text);
    expect(b.buttons()).toEqual([]);
    advance(MS * 2);
    expect(b.text()).toBe('Abre a las ');
    advance(MS * 3);
    expect(b.text()).toBe(`${text}|0.6 s`);
    expect(b.buttons()).toHaveLength(1);
  });

  it('shows nothing until the chat schedules it or its turn comes', () => {
    const b = mount({ role: 'assistant', text: 'Hola', revealId: 'never-scheduled' });
    expect(b.text()).toBe('');
    const banner = scheduled('Marca el 123.');
    const reply = scheduled('Llama ya.');
    b.render({ role: 'assistant', text: 'Llama ya.', revealId: reply });
    expect(b.text()).toBe('');
    advance(MS * 3);
    expect(b.text()).toBe('Llama ');
    expect(banner).not.toBe(reply);
  });

  it('shows the whole reply at once under reduced motion', () => {
    mockReduced = true;
    const id = scheduled('Abre a las 06:10.');
    const b = mount({ role: 'assistant', text: 'Abre a las 06:10.', meta: '1.0 s', revealId: id });
    expect(b.text()).toBe('Abre a las 06:10.|1.0 s');
  });

  it('does not replay a reply when the chat mounts again, even one left mid-way', () => {
    const text = 'uno dos tres cuatro cinco seis';
    const id = scheduled(text);
    const first = mount({ role: 'assistant', text, revealId: id });
    advance(MS);
    expect(first.text()).toBe('uno dos ');
    act(() => first.root.unmount());
    advance(MS * 10);
    expect(mount({ role: 'assistant', text, revealId: id }).text()).toBe(text);
  });

  it('sets keywords in bold and lists as items', () => {
    const b = mount({
      role: 'assistant',
      text: 'Si hay peligro, marca el 123.\n- Avisa a tu guía.',
      keywords: ['marca el 123', 'tu guía'],
    });
    expect(b.bold()).toEqual(['marca el 123', 'tu guía']);
    expect(b.text()).toBe('Si hay peligro, marca el 123.|•|Avisa a tu guía.');
  });

  it('re-renders only the bubble that is typing out', () => {
    const renders = { done: 0, live: 0 };
    const root = createRoot();
    const text = 'uno dos tres cuatro cinco seis siete ocho nueve diez once doce';
    const live = scheduled(text);
    act(() =>
      root.render(
        <>
          <Profiler id="done" onRender={() => renders.done++}>
            <ChatBubble role="assistant" text="Ya leída." revealId="never" />
            <ChatBubble role="assistant" text="Fija." />
          </Profiler>
          <Profiler id="live" onRender={() => renders.live++}>
            <ChatBubble role="assistant" text={text} revealId={live} />
          </Profiler>
        </>,
      ),
    );
    const before = { ...renders };
    // One chunk per step: the loop moves the streams at most ~15 times a second.
    advance(MS * 3);
    advance(MS * 3);
    advance(MS * 3);
    expect(renders.done - before.done).toBe(0);
    expect(renders.live - before.live).toBe(3);
  });
});
