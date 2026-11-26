import { existsSync } from 'node:fs';
import { join } from 'node:path';

import { clean } from '../clean';
import { fixture } from '../__fixtures__/load';

describe('clean (port of experiments/nlu/kb.py clean)', () => {
  it('strips leading and trailing chat fillers', () => {
    expect(clean('ey parce, ¿puedo acampar allá o cómo es el tema?')).toBe(
      '¿puedo acampar allá o cómo es el tema?',
    );
    expect(clean('bro, ¿puedo meter el dron pa grabar?')).toBe('¿puedo meter el dron pa grabar?');
    expect(clean('qué más pues, ¿y las tarifas de este año cuánto son?')).toBe(
      'las tarifas de este año cuánto son?',
    );
    expect(clean('vea, y eso es peligroso pues')).toBe('eso es peligroso');
  });

  it('keeps a message that is only fillers', () => {
    expect(clean('ey parce qué más')).toBe('ey parce qué más');
    expect(clean('hola')).toBe('hola');
  });

  const spec = join(__dirname, '..', '__fixtures__', 'clean.json');
  (existsSync(spec) ? it : it.skip)('matches Python on every blind-set turn', () => {
    const rows = fixture<{ in: string; out: string }[]>('clean.json');
    const bad = rows.filter((r) => clean(r.in) !== r.out);
    expect(bad.slice(0, 5)).toEqual([]);
  });
});
