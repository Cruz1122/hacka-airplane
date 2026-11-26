import data from '@/../assets/data/knowledge-keywords.json';
import catalog from '@/../assets/data/knowledge/catalog.json';

import { keywordsFor } from '../keywords';
import { findKeyword } from '../markdown';

describe('knowledge-keywords.json', () => {
  it('is version 1', () => {
    expect(data.version).toBe(1);
  });

  it('names catalog entries only, with phrases their short contains as whole words', () => {
    const shorts = new Map(catalog.map((e) => [e.id, e.short]));
    const entries: Record<string, readonly string[]> = data.entries;
    const problems = Object.entries(entries).flatMap(([id, keywords]) => {
      const short = shorts.get(id);
      if (short === undefined) return [`${id}: no such catalog entry`];
      return keywords
        .filter((k) => findKeyword(short, k) < 0)
        .map((k) => `${id}: "${k}" is not a whole-word phrase of its short`);
    });
    expect(problems).toEqual([]);
  });
});

describe('keywordsFor', () => {
  it("returns an entry's list, and one shared empty list otherwise", () => {
    expect(keywordsFor('access.brisas_entry_altitude')).toContain('4100 m');
    expect(keywordsFor('access.brisas_entry_altitude')).toBe(
      keywordsFor('access.brisas_entry_altitude'),
    );
    expect(keywordsFor(undefined)).toEqual([]);
    expect(keywordsFor('nope')).toBe(keywordsFor(undefined));
    expect(keywordsFor('constructor')).toBe(keywordsFor(undefined));
  });
});
