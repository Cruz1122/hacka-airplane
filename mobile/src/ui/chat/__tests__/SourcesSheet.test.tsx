import { act } from 'react';
import { Animated, Linking } from 'react-native';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot, type TestInstance } from 'test-renderer';

import { fill, t } from '@/i18n';

import type { ChatSource } from '../citations';
import { SourcesSheet } from '../SourcesSheet';

let mockReduced = true;
jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => mockReduced }));

const copy = t.chatScreen.sources;
const PRESS = { nativeEvent: {}, stopPropagation: () => {}, preventDefault: () => {} };
const URL =
  'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/';

function mount(sources: ChatSource[] | null) {
  const onClose = jest.fn();
  const root = createRoot();
  act(() => root.render(<SourcesSheet sources={sources} onClose={onClose} />));
  const all = (pred: (n: TestInstance) => boolean) => root.container.queryAll(pred);
  const byLabel = (label: string) =>
    all((n) => n.type === 'View' && n.props.accessibilityLabel === label);
  return {
    onClose,
    byLabel,
    /** Whether the overlay still takes touches. */
    blocking: () => all((n) => n.type === 'View')[0].props.pointerEvents !== 'none',
    texts: () => all((n) => n.type === 'Text').map((n) => [n.props.children].flat().join('')),
    press: (node: TestInstance) => act(() => node.props.onClick(PRESS)),
  };
}

describe('SourcesSheet', () => {
  let open: jest.SpyInstance;
  beforeEach(() => {
    open = jest.spyOn(Linking, 'openURL').mockResolvedValue(undefined);
  });
  afterEach(() => {
    mockReduced = true;
    jest.restoreAllMocks();
  });

  it('stays closed without sources', () => {
    expect(mount(null).texts()).toEqual([]);
    expect(mount([]).texts()).toEqual([]);
  });

  it('lists each source and opens only web links', () => {
    const s = mount([
      { id: 'a', title: 'Parques Nacionales', url: URL, date: '2026-11-21' },
      { id: 'b', title: 'Estación Refugio Quelital', excerpt: 'Abre a las 06:10.' },
      { id: 'c', title: 'Otro', url: 'javascript:alert(1)' },
    ]);
    expect(s.texts()).toEqual(
      expect.arrayContaining([
        copy.title,
        'Parques Nacionales',
        fill(copy.retrieved, { date: '2026-11-21' }),
        'Estación Refugio Quelital',
        'Abre a las 06:10.',
        'Otro',
      ]),
    );
    expect(s.byLabel(fill(copy.openLabel, { title: 'Otro' }))).toEqual([]);
    const [link] = s.byLabel(fill(copy.openLabel, { title: 'Parques Nacionales' }));
    s.press(link);
    expect(open).toHaveBeenCalledWith(URL);
  });

  it('slides out before it tells the chat it closed, letting touches through meanwhile', () => {
    mockReduced = false;
    const done: (() => void)[] = [];
    jest.spyOn(Animated, 'timing').mockImplementation(() => ({
      start: (cb?: (r: { finished: boolean }) => void) => done.push(() => cb?.({ finished: true })),
      stop: () => {},
      reset: () => {},
    }));
    const s = mount([{ id: 'b', title: 'Estación Refugio Quelital' }]);
    expect(s.blocking()).toBe(true);
    s.press(s.byLabel(copy.close)[0]);
    expect(s.onClose).not.toHaveBeenCalled();
    expect(s.blocking()).toBe(false);
    act(() => done.forEach((f) => f()));
    expect(s.onClose).toHaveBeenCalledTimes(1);
  });

  it('closes from its close button', () => {
    const s = mount([{ id: 'b', title: 'Estación Refugio Quelital' }]);
    s.press(s.byLabel(copy.close)[0]);
    expect(s.onClose).toHaveBeenCalledTimes(1);
  });
});
