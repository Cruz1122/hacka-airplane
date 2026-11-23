import { parseCitations } from '../citations';

describe('parseCitations', () => {
  it('hides the markers the driver writes and keeps the punctuation after them', () => {
    expect(parseCitations('Abre a las 06:40 [fuente: EST-A-01].')).toEqual({
      prose: 'Abre a las 06:40.',
      ids: ['EST-A-01'],
    });
    expect(
      parseCitations('Abre a las 06:10 [fuente: EST-D-01]\nCuesta 30.000 pesos [fuente: EST-D-04]'),
    ).toEqual({ prose: 'Abre a las 06:10\nCuesta 30.000 pesos', ids: ['EST-D-01', 'EST-D-04'] });
  });

  it('accepts the case, plural and id lists a model writes, citing each id once', () => {
    expect(
      parseCitations(
        'Hay refugio [Fuentes: EST-B-03, PAR-02] y agua [fuente: PAR-02; INF-001 y EST-B-03].',
      ),
    ).toEqual({ prose: 'Hay refugio y agua.', ids: ['EST-B-03', 'PAR-02', 'INF-001'] });
  });

  it('keeps ordinary brackets and markers that cite no id', () => {
    const text =
      'Necesito la fecha [trámite: admite datos parciales] [fuente: el guardaparque] [nota]';
    expect(parseCitations(text)).toEqual({ prose: text, ids: [] });
  });

  it('hides a marker still being streamed, so it never flashes on screen', () => {
    for (const tail of [
      '[',
      '[fu',
      '[fuente',
      '[fuente:',
      '[fuente: EST-A',
      '[fuentes: EST-A-01, P',
    ]) {
      expect(parseCitations(`Abre a las 06:40 ${tail}`).prose).toBe('Abre a las 06:40');
    }
    expect(parseCitations('Ver [nota').prose).toBe('Ver [nota');
  });
});
