import { RevealStore, WORDS_PER_SECOND, type RevealRow } from '../reveal';

const MS = 1000 / WORDS_PER_SECOND;
const NONE = new Set<string>();

/** A store whose frames run only when the test says so. */
function store() {
  const frames: (() => void)[] = [];
  const s = new RevealStore((step) => frames.push(step));
  return { s, frames };
}

const reply = (id: string, text: string): RevealRow => ({ id, role: 'assistant', text });

describe('RevealStore', () => {
  it('shows the first word at once, then words by elapsed time, then all', () => {
    const { s } = store();
    s.schedule([reply('a', 'uno dos tres cuatro')], NONE, 1000);
    expect(s.shown('a')).toBe(1);
    s.step(1000 + MS * 2.5);
    expect(s.shown('a')).toBe(3);
    expect(s.revealing('a')).toBe(true);
    s.step(1000 + MS * 3);
    expect(s.shown('a')).toBe(Infinity);
    expect(s.revealing('a')).toBe(false);
    expect(s.busy()).toBe(false);
  });

  it('starts the next reply at once after a new chat drops one still typing out', () => {
    const { s } = store();
    s.schedule([reply('old', 'a b c d e f g h i j k l m n o p q r s t')], NONE, 0);
    s.schedule([], NONE, MS);
    s.schedule([reply('k9:banner', 'Marca el 123.')], NONE, MS * 2);
    expect(s.shown('k9:banner')).toBe(1);
    expect(s.revealing('old')).toBeUndefined();
  });

  it('moves the streams in chunks at most about 15 times a second, whatever the display rate', () => {
    const { s, frames } = store();
    let now = 0;
    const clock = jest.spyOn(performance, 'now').mockImplementation(() => now);
    let emits = 0;
    s.subscribe(() => emits++);
    s.schedule([reply('a', Array.from({ length: 80 }, (_, i) => `w${i}`).join(' '))], NONE, 0);
    emits = 0;
    // One second of 120 Hz frames.
    for (let i = 0; i < 120; i++) {
      now += 1000 / 120;
      frames.splice(0).forEach((f) => f());
    }
    expect(emits).toBeGreaterThanOrEqual(12);
    expect(emits).toBeLessThanOrEqual(16);
    // Time-based all the same: a second at WORDS_PER_SECOND has roughly that many words out.
    expect(s.shown('a')).toBeGreaterThanOrEqual(WORDS_PER_SECOND - 2);
    expect(s.shown('a')).toBeLessThanOrEqual(WORDS_PER_SECOND + 2);
    clock.mockRestore();
  });

  it('catches up after a dropped frame instead of slowing down', () => {
    const { s } = store();
    s.schedule([reply('a', 'a b c d e f g h')], NONE, 0);
    s.step(MS * 5);
    expect(s.shown('a')).toBe(6);
  });

  it('types a banner out before its reply, in data order', () => {
    const { s } = store();
    s.schedule(
      [reply('k1:banner', 'Marca el 123.'), reply('k1', 'Si hay peligro, llama.')],
      NONE,
      0,
    );
    expect([s.shown('k1:banner'), s.shown('k1')]).toEqual([1, 0]);
    s.step(MS * 2);
    expect([s.shown('k1:banner'), s.shown('k1')]).toEqual([Infinity, 0]);
    s.step(MS * 3);
    expect(s.shown('k1')).toBe(1);
    s.step(MS * 3 + MS * 3);
    expect(s.shown('k1')).toBe(Infinity);
  });

  it('shows rows seen at mount whole and never replays a scheduled one', () => {
    const { s } = store();
    s.schedule([reply('old', 'ya leída')], new Set(['old']), 0);
    expect(s.shown('old')).toBe(Infinity);
    s.schedule([reply('new', 'uno dos tres')], NONE, 0);
    s.step(MS * 10);
    s.schedule([reply('new', 'uno dos tres')], NONE, MS * 20);
    expect(s.shown('new')).toBe(Infinity);
  });

  it('skips user rows and knows nothing about unscheduled ones', () => {
    const { s } = store();
    s.schedule([{ id: 'u', role: 'user', text: 'hola' }], NONE, 0);
    expect(s.shown('u')).toBe(0);
    expect(s.revealing('u')).toBeUndefined();
  });

  it('runs one frame loop for every stream until the last one ends, with nobody listening', () => {
    const { s, frames } = store();
    const now = jest.spyOn(performance, 'now');
    s.schedule([reply('a', 'uno dos'), reply('b', 'tres cuatro')], NONE, 0);
    expect(frames).toHaveLength(1);
    let t = 0;
    while (frames.length) {
      t += 16;
      now.mockReturnValue(t);
      frames.shift()!();
    }
    expect([s.shown('a'), s.shown('b')]).toEqual([Infinity, Infinity]);
    expect(t).toBeGreaterThanOrEqual(MS * 3);
    expect(t).toBeLessThan(MS * 3 + 66 + 16 * 2);
    now.mockRestore();
  });

  it('notifies listeners only when a stream moves', () => {
    const { s } = store();
    const listener = jest.fn();
    s.subscribe(listener);
    s.schedule([reply('a', 'uno dos tres')], NONE, 0);
    expect(listener).toHaveBeenCalledTimes(1);
    s.step(MS * 0.5);
    expect(listener).toHaveBeenCalledTimes(1);
    s.step(MS * 1);
    expect(listener).toHaveBeenCalledTimes(2);
  });
});
