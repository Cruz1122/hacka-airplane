import { fill, LOCALES } from '..';
import { es } from '../es';

/** Every string in a label tree as [path, text]. */
function entries(node: unknown, path = ''): [string, string][] {
  if (typeof node === 'string') return [[path, node]];
  return Object.entries(node as object).flatMap(([k, v]) => entries(v, path ? `${path}.${k}` : k));
}

const placeholders = (text: string) => [...text.matchAll(/\{(\w+)\}/g)].map((m) => m[1]).sort();

describe('labels', () => {
  const source = Object.fromEntries(entries(es));

  it.each(Object.keys(LOCALES))('%s has every label of es, non-empty', (locale) => {
    const labels = entries(LOCALES[locale as keyof typeof LOCALES]);
    expect(labels.map(([path]) => path)).toEqual(Object.keys(source));
    expect(labels.filter(([, text]) => text.trim() === '')).toEqual([]);
  });

  it.each(Object.keys(LOCALES))('%s keeps the placeholders of es', (locale) => {
    const wrong = entries(LOCALES[locale as keyof typeof LOCALES]).filter(
      ([path, text]) => placeholders(text).join() !== placeholders(source[path]).join(),
    );
    expect(wrong).toEqual([]);
  });

  it('fills placeholders and rejects a missing value', () => {
    expect(fill('Paso {n} de {total}', { n: 2, total: 3 })).toBe('Paso 2 de 3');
    expect(() => fill('Hola {pet}', {})).toThrow('{pet}');
  });
});
