import { act } from 'react';
import { Animated, Linking, StyleSheet } from 'react-native';
// Ships with jest-expo (its replacement for the deprecated react-test-renderer).
import { createRoot, type TestInstance } from 'test-renderer';

import type { MediaPick, MediaPickItem } from '@/core/media/media';

import { ChatBubble, type ChatBubbleProps } from '../ChatBubble';
import type { ChatSource } from '../citations';
import { licenseFamily, mediaRevealId, photoSourceUrl, revealRows } from '../MediaGallery';
import { replyReveal, WORDS_PER_SECOND } from '../reveal';

let mockReduced = false;
jest.mock('@/ui/useReducedMotion', () => ({ useReducedMotion: () => mockReduced }));
let mockScreen = 390;
jest.mock('react-native/Libraries/Utilities/useWindowDimensions', () => ({
  __esModule: true,
  default: () => ({ width: mockScreen, height: 844, scale: 2, fontScale: 1 }),
}));

const item = (
  id: string,
  common: string,
  scientific: string | null,
  author = 'Ana',
  license = 'CC BY 2.0',
  url?: string,
): MediaPickItem => ({
  id,
  common,
  scientific,
  photo: { file: `${id}.1.webp`, author, license, ...(url ? { url } : undefined) },
});
const CONDOR = item('condor', 'Cóndor de los Andes', 'Vultur gryphus');
const OSO = item('oso', 'Oso de anteojos', 'Tremarctos ornatus', 'Luis');
const OTUN = item('otun', 'Laguna del Otún', null, 'Eva', 'Public domain');
const SINGLE: MediaPick = { layout: 'single', items: [CONDOR] };
const ROWS: MediaPick = { layout: 'rows', items: [CONDOR, OSO, OTUN] };
const COLUMNS: MediaPick = { layout: 'columns', items: [CONDOR, OTUN] };
const TEXT = 'El cóndor anida en los riscos del parque.'; // 8 words
const SOURCES: ChatSource[] = [{ id: 'EST-D-01', title: 'Estación', excerpt: 'Abre a las 06:10.' }];
const SOURCED = { sources: SOURCES, onOpenSources: () => {} };
const PRESS = { nativeEvent: {}, stopPropagation: () => {}, preventDefault: () => {} };

const transparent = (n: TestInstance) => StyleSheet.flatten(n.props.style)?.color === 'transparent';
/** Text as a reader sees it: words not typed yet are transparent. */
const visible = (n: TestInstance | string): string =>
  typeof n === 'string' ? n : transparent(n) ? '' : n.children.map(visible).join('');
/** The credit's author: the only single-line text in a bubble. */
const isAuthor = (n: TestInstance) => n.props.numberOfLines === 1;

function mount(props: ChatBubbleProps) {
  const root = createRoot();
  act(() => root.render(<ChatBubble {...props} />));
  const all = (pred: (n: TestInstance) => boolean) => root.container.queryAll(pred);
  const outer = () => all((n) => n.type === 'Text' && n.parent?.type !== 'Text');
  const authors = () => outer().filter(isAuthor);
  const images = () => all((n) => n.type === 'Image');
  const size = (n: TestInstance) => {
    const { width, height } = StyleSheet.flatten(n.props.style);
    return { width, height };
  };
  return {
    /** Each outermost Text as it reads on screen, the photo credits aside. */
    lines: () => outer().filter((n) => !isAuthor(n)).map(visible),
    /** Styles of non-author outermost Text nodes, parallel to `lines()`. */
    lineStyles: () => outer().filter((n) => !isAuthor(n)).map((n) => StyleSheet.flatten(n.props.style)),
    authors: () => authors().map(visible),
    /** What a screen reader hears for each credit. */
    creditLabels: () => authors().map((n) => n.parent!.props.accessibilityLabel),
    /** Pressable credit nodes. */
    credits: () => authors().map((n) => n.parent!),
    images,
    sizes: () => images().map(size),
    italic: () =>
      all(
        (n) => n.type === 'Text' && StyleSheet.flatten(n.props.style)?.fontStyle === 'italic',
      ).map(visible),
    scrolls: () => all((n) => n.props.horizontal === true),
    dividers: () => all((n) => StyleSheet.flatten(n.props.style)?.borderTopWidth > 0),
    /** The gallery reports its laid-out width, as the bubble sizes it. */
    layout: (width: number) => {
      const [gallery] = all((n) => typeof n.props.onLayout === 'function');
      act(() =>
        gallery.props.onLayout({ nativeEvent: { layout: { x: 0, y: 0, width, height: 300 } } }),
      );
    },
    press: (node: TestInstance) => act(() => node.props.onClick(PRESS)),
  };
}

/** Cards side by side: their total width, and how much of `width` they leave. */
const spread = (sizes: { width: number }[], width: number) => {
  const total = sizes.reduce((sum, s) => sum + s.width, 0);
  return { total, left: width - total };
};

const MS = 1000 / WORDS_PER_SECOND;
let clock = 0;
let frames: (() => void)[] = [];
const advance = (ms: number) =>
  act(() => {
    clock += ms;
    const due = frames;
    frames = [];
    due.forEach((f) => f());
  });
let ids = 0;
/** A reply with photos the chat has just scheduled; every row so far is handed over, as the chat does. */
const rows: { id: string; role: 'assistant'; text: string; media?: MediaPick }[] = [];
function scheduled(media: MediaPick, seen = false) {
  const id = `m${++ids}`;
  rows.push({ id, role: 'assistant', text: TEXT, media });
  const seenIds = new Set(seen ? revealRows(rows).map((r) => r.id) : []);
  act(() => replyReveal.schedule(revealRows(rows), seenIds, clock));
  return id;
}

describe('MediaGallery', () => {
  let timing: jest.SpyInstance;
  let openURL: jest.SpyInstance;
  /** Delays of the card entrances started so far (the bubble's own entry has none). */
  const cascade = () => timing.mock.calls.map(([, c]) => c.delay).filter((d) => d !== undefined);
  beforeEach(() => {
    mockReduced = false;
    mockScreen = 390;
    openURL = jest.spyOn(Linking, 'openURL').mockResolvedValue(undefined);
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
    while (frames.length) advance(1000);
    clock += 1000;
    jest.restoreAllMocks();
  });

  it('captions one photo with scientific name below, smaller and without parentheses, and credits it with a camera link', () => {
    const b = mount({ role: 'assistant', text: TEXT, media: SINGLE });
    expect(b.lines()).toEqual([TEXT, 'Cóndor de los Andes', 'Vultur gryphus']);
    const [, commonStyle, scientificStyle] = b.lineStyles();
    expect(scientificStyle.fontSize).toBeLessThan(commonStyle.fontSize);
    expect(b.italic()).toEqual(['Vultur gryphus']);
    expect(b.authors()).toEqual(['Ana']);
    expect([...b.lines(), ...b.authors()].join(' ')).not.toMatch(/CC|Foto|\(|\)/);
    expect(b.creditLabels()).toEqual(['Foto de Ana, licencia CC BY 2.0']);
    expect(b.images().map((i) => i.props.accessibilityLabel)).toEqual([
      'Cóndor de los Andes, Vultur gryphus',
    ]);
    b.press(b.credits()[0]);
    expect(openURL).toHaveBeenCalledWith(photoSourceUrl(CONDOR));
  });

  it('opens an explicit photo url when present, or falls back to Wikimedia Commons search', () => {
    const customUrl = 'https://commons.wikimedia.org/wiki/File:Condor.jpg';
    const withUrl = item('condor', 'Cóndor de los Andes', 'Vultur gryphus', 'Ana', 'CC BY 2.0', customUrl);
    expect(photoSourceUrl(withUrl)).toBe(customUrl);
    expect(photoSourceUrl(CONDOR)).toContain('commons.wikimedia.org');
    expect(['CC0', 'CC0 1.0', 'CC BY-SA 4.0', 'Public domain'].map(licenseFamily)).toEqual([
      'cc',
      'cc',
      'cc',
      'publicDomain',
    ]);
  });

  it('spans the bubble at its full share of the row from the first frame, whatever the reply says', () => {
    // 88 % of the row inside its 22 pt margins, less the bubble's 17 pt sides (the sources badge
    // sits at the bottom corner without eating into photo width).
    const width = (props: Partial<ChatBubbleProps>, text = TEXT) =>
      mount({ role: 'assistant', text, media: SINGLE, ...props }).sizes()[0].width;
    expect(width({})).toBe(270);
    expect(width({}, `${TEXT} `.repeat(12))).toBe(270);
    expect(width({}, 'Sí.')).toBe(270);
    expect(width(SOURCED)).toBe(270);
    mockScreen = 360;
    expect(width({})).toBe(244);
    expect(width(SOURCED)).toBe(244);
  });

  it('follows the width it is laid out at, inside a narrower frame', () => {
    mockScreen = 1280;
    const b = mount({ role: 'assistant', text: TEXT, media: SINGLE });
    b.layout(301.6);
    const [{ width, height }] = b.sizes();
    expect(width).toBe(301);
    expect(height).toBeGreaterThan(width);
    expect(height).toBeLessThan(width * 1.25);
  });

  it('lists rows as large square thumbnails with dividers between them; a place has no scientific name', () => {
    const b = mount({ role: 'assistant', text: TEXT, media: ROWS });
    expect(b.lines().slice(1)).toEqual([
      'Cóndor de los Andes',
      'Vultur gryphus',
      'Oso de anteojos',
      'Tremarctos ornatus',
      'Laguna del Otún',
    ]);
    const sizes = b.sizes();
    expect(sizes).toHaveLength(3);
    sizes.forEach(({ width, height }) => {
      expect(width).toBe(height);
      expect(width).toBeGreaterThanOrEqual(96);
    });
    expect(b.dividers()).toHaveLength(2);
    expect(b.scrolls()).toEqual([]);
  });

  it('shares the width between two portrait cards on a 360 pt phone, never overflowing it', () => {
    mockScreen = 360;
    const b = mount({ role: 'assistant', text: TEXT, media: COLUMNS, ...SOURCED });
    expect(b.scrolls()).toEqual([]);
    const sizes = b.sizes();
    expect(sizes).toHaveLength(2);
    sizes.forEach(({ width, height }) => expect(height / width).toBeCloseTo(5 / 4, 1));
    expect(sizes[0].width).toBe(sizes[1].width);
    const { left } = spread(sizes, 244);
    expect(left).toBeGreaterThan(0); // the gap between them
    expect(left).toBeLessThanOrEqual(12);
  });

  it('falls back to rows when the cards would be too narrow: three on a phone, two in a narrow frame', () => {
    const three = mount({ role: 'assistant', text: TEXT, media: { ...ROWS, layout: 'columns' } });
    expect(three.scrolls()).toEqual([]);
    three.sizes().forEach(({ width, height }) => expect(width).toBe(height));
    expect(three.dividers()).toHaveLength(2);

    const two = mount({ role: 'assistant', text: TEXT, media: COLUMNS });
    two.sizes().forEach(({ width, height }) => expect(height).toBeGreaterThan(width));
    two.layout(180);
    two.sizes().forEach(({ width, height }) => expect(width).toBe(height));
  });

  it('keeps three cards side by side where they fit, on a tablet', () => {
    mockScreen = 820;
    const b = mount({ role: 'assistant', text: TEXT, media: { ...ROWS, layout: 'columns' } });
    const sizes = b.sizes();
    sizes.forEach(({ width, height }) => expect(height / width).toBeCloseTo(5 / 4, 1));
    const { left } = spread(sizes, Math.floor(0.88 * (820 - 44)) - 34);
    expect(left).toBeGreaterThan(0);
    expect(left).toBeLessThanOrEqual(2 * 8 + 3);
    expect(b.dividers()).toEqual([]);
  });

  it('waits until the reply text finishes before mounting the gallery, then cascades it in and types its captions', () => {
    const id = scheduled(ROWS);
    const b = mount({ role: 'assistant', text: TEXT, media: ROWS, revealId: id, entryId: id });
    // Avoids reserving tall invisible image space while the reply text is still typing out.
    expect(b.images()).toHaveLength(0);
    advance(MS * 4);
    expect(cascade()).toEqual([]);
    advance(MS * 4); // the text is out
    expect(b.images()).toHaveLength(3);
    expect(b.authors()).toEqual(['Ana', 'Luis', 'Eva']);
    expect(b.lines()[0]).toBe(TEXT);
    expect(cascade()).toEqual([0, 90, 180]);
    expect(b.lines()[1]).toMatch(/^Cóndor/);
    expect(b.lines()[2]).toBe('');
    advance(MS * 20);
    expect(b.lines().slice(1)).toEqual([
      'Cóndor de los Andes',
      'Vultur gryphus',
      'Oso de anteojos',
      'Tremarctos ornatus',
      'Laguna del Otún',
    ]);
    expect(cascade()).toEqual([0, 90, 180]); // once
  });

  it('shows the photos of a reply already read whole, without a cascade', () => {
    const id = scheduled(COLUMNS, true);
    const b = mount({ role: 'assistant', text: TEXT, media: COLUMNS, revealId: id, entryId: id });
    expect(b.lines()).toContain('Cóndor de los Andes');
    expect(b.lines()).toContain('Vultur gryphus');
    expect(b.lines()).toContain('Laguna del Otún');
    expect(cascade()).toEqual([]);
  });

  it('shows everything at once under reduced motion', () => {
    mockReduced = true;
    const id = scheduled(SINGLE);
    const b = mount({ role: 'assistant', text: TEXT, media: SINGLE, revealId: id, entryId: id });
    expect(b.lines()).toEqual([TEXT, 'Cóndor de los Andes', 'Vultur gryphus']);
    expect(b.authors()).toEqual(['Ana']);
    expect(cascade()).toEqual([]);
  });
});

describe('revealRows', () => {
  it('queues each reply’s captions right after it', () => {
    expect(
      revealRows([
        { id: 'a', role: 'assistant', text: 'Hola' },
        { id: 'b', role: 'assistant', text: 'El cóndor.', media: ROWS },
      ]),
    ).toEqual([
      { id: 'a', role: 'assistant', text: 'Hola' },
      { id: 'b', role: 'assistant', text: 'El cóndor.', media: ROWS },
      { id: mediaRevealId('b'), role: 'assistant', text: expect.any(String) },
    ]);
  });
});
