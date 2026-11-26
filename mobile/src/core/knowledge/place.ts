// A stage chat's question with its deictic words ("aquí", "este valle", "estamos") replaced by the
// stage's place. Appending a sentence about the stage instead outweighs a short question in the
// e5 embedding: every question then answered the stage itself ("cuánto cuesta la entrada" from
// Aguacerales got the Aguacerales station). A question with no deictic word is left alone.

// JS `\b` is ASCII-only, so "aquí" would never end a word: boundaries are spelled out.
const L = '(^|[^a-z0-9áéíóúüñ])';
const R = '(?=$|[^a-z0-9áéíóúüñ])';
const NOUN = new RegExp(
  `${L}(?:este|esta|ese|esa)\\s+(?:lugar|sitio|punto|zona|parte|parada|etapa|estaci[oó]n|valle|sector|paraje|tramo)${R}`,
  'gi',
);
const FROM_HERE = new RegExp(`${L}(desde|por|de|hasta)\\s+(?:aqu[ií]|ac[aá])${R}`, 'gi');
const HERE = new RegExp(`${L}(?:aqu[ií]|ac[aá])${R}`, 'gi');
const WE_ARE = new RegExp(`${L}estamos${R}`, 'i');

export function placeQuestion(question: string, place: string): string {
  const out = question
    .replace(NOUN, (_, b: string) => `${b}${place}`)
    .replace(FROM_HERE, (_, b: string, prep: string) => `${b}${prep} ${place}`)
    .replace(HERE, (_, b: string) => `${b}en ${place}`);
  if (out !== question || question.toLowerCase().includes(place.toLowerCase())) return out;
  return question.replace(WE_ARE, (_, b: string) => `${b}estamos en ${place}`);
}
