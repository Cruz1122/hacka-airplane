import catalog from '@/../assets/data/knowledge/catalog.json';

import { emphasize, findKeyword, parseMarkdown, replyDoc, sliceDoc, type Block } from '../markdown';

const plain = (blocks: Block[]) =>
  blocks.map((b) => (b.marker ? `${b.marker} ` : '') + b.spans.map((s) => s.text).join(''));
const bold = (blocks: Block[]) =>
  blocks.flatMap((b) => b.spans.filter((s) => s.bold).map((s) => s.text));

describe('parseMarkdown', () => {
  it('splits paragraphs on blank lines and keeps a single line break inside one', () => {
    const doc = parseMarkdown('Uno\ndos\n\n\nTres');
    expect(doc.blocks).toEqual([
      { marker: null, spans: [{ text: 'Uno\ndos', bold: false }] },
      { marker: null, spans: [{ text: 'Tres', bold: false }] },
    ]);
  });

  it('starts list items straight under a paragraph line, as catalog answers write them', () => {
    const doc = parseMarkdown(
      'Antes de salir:\n- Lleva abrigo.\n- Sal temprano.\n2. Registra la visita.',
    );
    expect(plain(doc.blocks)).toEqual([
      'Antes de salir:',
      '• Lleva abrigo.',
      '• Sal temprano.',
      '2. Registra la visita.',
    ]);
    expect(doc.text).toBe(
      'Antes de salir:\n• Lleva abrigo.\n• Sal temprano.\n2. Registra la visita.',
    );
  });

  it('keeps a dash without a space, or a lone dash, as text', () => {
    expect(plain(parseMarkdown('-5 °C de noche\n- ').blocks)).toEqual(['-5 °C de noche\n-']);
  });

  it('bolds ** pairs, honours escapes and leaves an unpaired ** as text', () => {
    const doc = parseMarkdown('Marca **el 123** ya; 2 \\*\\* 3 y \\\\ fin **sin cierre');
    expect(doc.blocks[0].spans).toEqual([
      { text: 'Marca ', bold: false },
      { text: 'el 123', bold: true },
      { text: ' ya; 2 ** 3 y \\ fin **sin cierre', bold: false },
    ]);
  });

  it('merges touching bold runs and drops empty ones', () => {
    expect(parseMarkdown('**a****b** c ****').blocks[0].spans).toEqual([
      { text: 'ab', bold: true },
      { text: ' c ', bold: false },
    ]);
  });

  it('stops after each word and its whitespace, across blocks, ending at the full length', () => {
    const doc = parseMarkdown('Hola **gran** día\n- sí');
    expect(doc.stops).toEqual([5, 10, 13, 15]);
  });
});

describe('sliceDoc', () => {
  const doc = parseMarkdown('Lleva **ropa impermeable** y agua.\n- Sal **antes** de las 7.');
  const total = doc.stops.at(-1)!;

  it('shows exactly the first n visible characters and never a marker', () => {
    const flat = doc.blocks.map((b) => b.spans.map((s) => s.text).join('')).join('');
    for (let n = 0; n <= total; n++) {
      const blocks = sliceDoc(doc, n);
      expect(blocks.map((b) => b.spans.map((s) => s.text).join('')).join('')).toBe(
        flat.slice(0, n),
      );
      expect(JSON.stringify(blocks)).not.toContain('*');
    }
  });

  it('keeps bold on a partly shown bold run', () => {
    expect(bold(sliceDoc(doc, 'Lleva ropa imp'.length))).toEqual(['ropa imp']);
  });

  it("shows a list marker with its item's first character only", () => {
    expect(sliceDoc(doc, 'Lleva ropa impermeable y agua.'.length)).toHaveLength(1);
    expect(plain(sliceDoc(doc, 'Lleva ropa impermeable y agua.'.length + 1))[1]).toBe('• S');
  });

  it('returns the original blocks when everything is shown', () => {
    expect(sliceDoc(doc, total)).toEqual(doc.blocks);
    expect(sliceDoc(doc, total)[1]).toBe(doc.blocks[1]);
  });
});

describe('findKeyword', () => {
  it('matches whole words only, accents being letters', () => {
    expect(findKeyword('El Cisne y Cisneros', 'Cisne')).toBe(3);
    expect(findKeyword('Cisneros', 'Cisne')).toBe(-1);
    expect(findKeyword('páramo', 'ramo')).toBe(-1);
    expect(findKeyword('la vía, no la víaa', 'vía')).toBe(3);
    expect(findKeyword('Brisas–Kumanday', 'Brisas')).toBe(0);
  });

  it('skips an occurrence inside a word and takes the next whole one', () => {
    expect(findKeyword('Otúnes y el Otún', 'Otún')).toBe(12);
  });

  it('needs no boundary at an edge that is not a letter', () => {
    expect(findKeyword('a unos 4100 m.', '4100 m.')).toBe(7);
  });

  it('counts only letters as word characters (the contract), so digits do not bound', () => {
    expect(findKeyword('unos 4100 m', '100 m')).toBe(6);
  });

  it('never matches a keyword with a line break or blank edges', () => {
    expect(findKeyword('uno\ndos', 'uno\ndos')).toBe(-1);
    expect(findKeyword('uno dos', ' dos')).toBe(-1);
    expect(findKeyword('uno', '')).toBe(-1);
  });
});

describe('emphasize', () => {
  it('bolds the first whole-word occurrence of each keyword', () => {
    expect(emphasize('Brisas abre; Brisas cierra', ['Brisas'])).toBe(
      '**Brisas** abre; Brisas cierra',
    );
  });

  it('prefers the longest keyword and leaves one inside it plain', () => {
    const md = emphasize('El centro de inducción Brisas está en Brisas.', [
      'Brisas',
      'centro de inducción Brisas',
    ]);
    expect(md).toBe('El **centro de inducción Brisas** está en Brisas.');
  });

  it('keeps partly overlapping keywords apart, longest first', () => {
    const md = emphasize('pico y placa ambiental del Tolima', [
      'placa ambiental del Tolima',
      'pico y placa',
    ]);
    expect(bold(parseMarkdown(md).blocks)).toEqual(['placa ambiental del Tolima']);
  });

  it("escapes the text's own asterisks and backslashes so they show as written", () => {
    const md = emphasize('2 ** 3 \\ y **Marca**', ['Marca']);
    const doc = parseMarkdown(md);
    expect(doc.text).toBe('2 ** 3 \\ y **Marca**');
    expect(bold(doc.blocks)).toEqual(['Marca']);
  });

  it('ignores keywords the text does not contain', () => {
    expect(emphasize('Hola', ['adiós', 'Hol'])).toBe('Hola');
  });

  it('bolds inside a list item without breaking the item', () => {
    const doc = parseMarkdown(emphasize('Lleva:\n- ropa impermeable', ['ropa impermeable']));
    expect(doc.blocks[1]).toEqual({
      marker: '•',
      spans: [{ text: 'ropa impermeable', bold: true }],
    });
  });
});

describe('replyDoc', () => {
  it('hides citation markers before parsing', () => {
    expect(replyDoc('Abre a las 06:10 [fuente: EST-D-01].', ['06:10']).text).toBe(
      'Abre a las 06:10.',
    );
  });

  it("shows every catalog answer's visible text unchanged apart from list markers", () => {
    for (const entry of catalog) {
      const expected = entry.short
        .split('\n')
        .map((l) => l.trim().replace(/^- /, '• '))
        .filter(Boolean)
        .join('\n');
      expect(replyDoc(entry.short, []).text).toBe(expected);
    }
  });
});
