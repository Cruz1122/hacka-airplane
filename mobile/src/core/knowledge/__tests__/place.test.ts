import { placeQuestion } from '../place';

describe('placeQuestion', () => {
  test.each([
    ['¿por qué le dicen así a este valle?', 'Lunares', '¿por qué le dicen así a Lunares?'],
    ['¿es verdad que aquí espantan?', 'Arenales', '¿es verdad que en Arenales espantan?'],
    ['¿qué animales se ven por aquí?', 'Brisas', '¿qué animales se ven por Brisas?'],
    [
      '¿qué cráter se ve desde acá?',
      'Valle de las Tumbas',
      '¿qué cráter se ve desde Valle de las Tumbas?',
    ],
    ['¿a qué altura estamos?', 'Brisas', '¿a qué altura estamos en Brisas?'],
    ['¿Qué hay en ESTA ZONA?', 'Arenales', '¿Qué hay en Arenales?'],
  ])('%s -> %s', (q, place, expected) => {
    expect(placeQuestion(q, place)).toBe(expected);
  });

  test('leaves a question without a deictic word alone', () => {
    expect(placeQuestion('¿cuánto cuesta la entrada al parque?', 'Aguacerales')).toBe(
      '¿cuánto cuesta la entrada al parque?',
    );
    expect(placeQuestion('¿qué es una morrena?', 'Arenales')).toBe('¿qué es una morrena?');
  });

  test('does not touch words that only contain "aqui"', () => {
    expect(placeQuestion('¿hay aquicultura?', 'Brisas')).toBe('¿hay aquicultura?');
  });
});
