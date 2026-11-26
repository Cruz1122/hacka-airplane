import { act } from 'react';
import { Animated, Linking } from 'react-native';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot, type TestInstance } from 'test-renderer';

import { fill, t } from '@/i18n';
import { resetFavoriteSourcesForTest } from '@/state/favoriteSources';

import type { ChatSource } from '../citations';
import { SourcesSheet } from '../SourcesSheet';

const mockGetItem = jest.fn<Promise<string | null>, [string]>(async () => null);
const mockSetItem = jest.fn<Promise<void>, [string, string]>(async () => {});
jest.mock('expo-sqlite/kv-store', () => ({
  __esModule: true,
  default: {
    getItemAsync: (key: string) => mockGetItem(key),
    setItemAsync: (key: string, value: string) => mockSetItem(key, value),
  },
}));

let mockReduced = true;
jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => mockReduced }));

const copy = t.chatScreen.sources;
const PRESS = { nativeEvent: {}, stopPropagation: () => {}, preventDefault: () => {} };
const URL =
  'https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/?ref=1';

function mount(sources: ChatSource[] | null) {
  const onClose = jest.fn();
  const root = createRoot();
  act(() => root.render(<SourcesSheet sources={sources} onClose={onClose} />));
  const show = (next: ChatSource[]) =>
    act(() => root.render(<SourcesSheet sources={next} onClose={onClose} />));
  const all = (pred: (n: TestInstance) => boolean) => root.container.queryAll(pred);
  const byLabel = (label: string) =>
    all((n) => n.type === 'View' && n.props.accessibilityLabel === label);
  return {
    onClose,
    show,
    byLabel,
    /** Whether the overlay still takes touches. */
    blocking: () => all((n) => n.type === 'View')[0].props.pointerEvents !== 'none',
    texts: () => all((n) => n.type === 'Text').map((n) => [n.props.children].flat().join('')),
    images: () => all((n) => n.type === 'Image'),
    press: (node: TestInstance) => act(() => node.props.onClick(PRESS)),
  };
}

describe('SourcesSheet', () => {
  let open: jest.SpyInstance;
  beforeEach(() => {
    resetFavoriteSourcesForTest();
    mockGetItem.mockClear();
    mockSetItem.mockClear();
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

  it('shows favicon, main link fragment, bare date without Consultada, and icon-only open link', () => {
    const s = mount([
      { id: 'a', title: 'Parques Nacionales', url: URL, date: '2026-11-21' },
      { id: 'b', title: 'Estación Refugio Quelital', excerpt: 'Abre a las 06:10.' },
      { id: 'c', title: 'Otro', url: 'javascript:alert(1)' },
    ]);
    const texts = s.texts();
    expect(texts).toEqual(
      expect.arrayContaining([
        copy.title,
        'Parques Nacionales',
        'parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados',
        '2026-11-21',
        'Estación Refugio Quelital',
        'Abre a las 06:10.',
        'Otro',
      ]),
    );
    // No "Consultada..." wording and no visible "Abrir enlace" text label on the icon button.
    expect(texts.join(' ')).not.toContain('Consultada');
    expect(texts).not.toContain(copy.open);
    expect(s.images().some((img) => String(img.props.source?.uri).includes('parquesnacionales.gov.co'))).toBe(true);
    expect(s.byLabel(fill(copy.openLabel, { title: 'Otro' }))).toEqual([]);
    const [link] = s.byLabel(fill(copy.openLabel, { title: 'Parques Nacionales' }));
    s.press(link);
    expect(open).toHaveBeenCalledWith(URL);
  });

  it('toggles and persists favorite sources', () => {
    const s = mount([{ id: 'a', title: 'Parques Nacionales', url: URL, date: '2026-11-21' }]);
    const [saveBtn] = s.byLabel(fill(copy.favoriteLabel, { title: 'Parques Nacionales' }));
    expect(saveBtn.props.accessibilityState).toEqual({ selected: false });
    s.press(saveBtn);
    const [removeBtn] = s.byLabel(fill(copy.unfavoriteLabel, { title: 'Parques Nacionales' }));
    expect(removeBtn.props.accessibilityState).toEqual({ selected: true });
    expect(mockSetItem).toHaveBeenCalledTimes(1);
    s.press(removeBtn);
    expect(s.byLabel(fill(copy.favoriteLabel, { title: 'Parques Nacionales' }))).toHaveLength(1);
    expect(mockSetItem).toHaveBeenCalledTimes(2);
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

  it('keeps sources asked for while it slides out', () => {
    mockReduced = false;
    const anims: { done?: (r: { finished: boolean }) => void; stopped: boolean }[] = [];
    jest.spyOn(Animated, 'timing').mockImplementation(() => {
      const a: (typeof anims)[number] = { stopped: false };
      anims.push(a);
      return {
        start: (cb?: (r: { finished: boolean }) => void) => {
          a.done = cb;
        },
        stop: () => {
          if (!a.stopped) a.done?.({ finished: false });
          a.stopped = true;
        },
        reset: () => {},
      };
    });
    const s = mount([{ id: 'a', title: 'Estación Refugio Quelital' }]);
    s.press(s.byLabel(copy.close)[0]);
    const exit = anims.at(-1)!;
    s.show([{ id: 'b', title: 'Parque' }]);
    act(() => exit.done?.({ finished: true }));
    expect(s.onClose).not.toHaveBeenCalled();
    expect(s.blocking()).toBe(true);
    expect(s.texts()).toContain('Parque');
  });

  it('closes from its close button', () => {
    const s = mount([{ id: 'b', title: 'Estación Refugio Quelital' }]);
    s.press(s.byLabel(copy.close)[0]);
    expect(s.onClose).toHaveBeenCalledTimes(1);
  });
});
