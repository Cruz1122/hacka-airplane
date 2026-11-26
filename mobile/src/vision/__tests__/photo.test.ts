import classes from '@/../assets/vision/classes.json';
import references from '@/../assets/vision/index.json';
import { degradedKnowledgeEngine } from '@/llm/knowledgeAssets';
import { KnowledgeChat } from '@/state/knowledgeChat';
import { matchPhoto } from '@/vision/matchPhoto';
import { photoFrames } from '@/vision/pixels';

const parkClasses = Object.entries(classes).flatMap(([id, expected]) =>
  'entryId' in expected ? [{ id, expected }] : [],
);

test.each(parkClasses)('a $id reference retrieves the corresponding curated answer', async ({ id, expected }) => {
  const image = references.find((row) => row.classId === id)!;
  const match = matchPhoto(Float32Array.from(image.vector));
  expect(match).toEqual(expected);
  const engine = degradedKnowledgeEngine('text embedder not loaded');
  const ask = jest.spyOn(engine, 'ask');
  const chat = new KnowledgeChat(async () => ({ engine }));
  await chat.askPhoto("file:///foto.jpg", "", async () => match);
  expect(ask).toHaveBeenCalledWith(`dime que es esto ${expected.label}`, expected.entryId);
  expect(chat.snapshot().rows.at(-1)).toMatchObject({
    role: 'assistant',
    reply: { type: 'answer', id: expected.entryId, text: expect.stringContaining(expected.label) },
  });
});

test('an unrecognizable photo leaves the chat ready without an invented label', async () => {
  const engine = { ask: jest.fn() };
  const chat = new KnowledgeChat(async () => ({ engine }));
  await chat.askPhoto("file:///foto.jpg", "", async () => matchPhoto(new Float32Array(1024)));
  expect(engine.ask).not.toHaveBeenCalled();
  expect(chat.snapshot()).toMatchObject({
    busy: false,
    rows: [expect.anything(), { role: 'assistant', reply: { type: 'abstain', text: expect.stringContaining('guía turístico') } }],
  });
});

test('keeps the real caption and photo visible while passing the inferred class internally', async () => {
  const match = classes.frailejon;
  const engine = degradedKnowledgeEngine('text embedder not loaded');
  const ask = jest.spyOn(engine, 'ask');
  const chat = new KnowledgeChat(async () => ({ engine }));
  await chat.askPhoto('file:///foto.jpg', '¿Qué altura alcanza?', async () => match);
  expect(ask).toHaveBeenCalledWith('¿Qué altura alcanza? frailejón', match.entryId, true);
  expect(chat.snapshot().rows[0]).toMatchObject({
    role: 'user', photoUri: 'file:///foto.jpg', text: '¿Qué altura alcanza?',
  });
});


test.each(['', '¿Qué ves aquí?', 'Mira', 'Mírame', 'Míranos en esta foto'])('unlocks the selfie reply only after the visual match for %s', async (caption) => {
  const engine = { ask: jest.fn() };
  const chat = new KnowledgeChat(async () => ({ engine }));
  const reference = references.find((row) => row.classId === 'persona')!;
  await chat.askPhoto('file:///selfie.jpg', caption, async () => matchPhoto(Float32Array.from(reference.vector)));
  expect(chat.snapshot().rows.at(-1)).toMatchObject({
    reply: { text: '¡Te identifico a ti pasándola muy bien en nuestro parque!' },
  });
  expect(engine.ask).not.toHaveBeenCalled();
});

test('a selfie caption alone never triggers the easter egg for a non-person photo', async () => {
  const engine = degradedKnowledgeEngine('text embedder not loaded');
  const chat = new KnowledgeChat(async () => ({ engine }));
  await chat.askPhoto('file:///planta.jpg', 'Mírame', async () => classes.frailejon);
  expect(chat.snapshot().rows.at(-1)).toMatchObject({
    reply: { type: 'answer', id: classes.frailejon.entryId },
  });
});

test.each(['Cambia el fondo', '¿Puedes recortar la foto?', 'Ponme un sombrero', 'Quiero editar la imagen', 'Quiero que le quites el fondo'])('declines %s before attempting photo classification', async (caption) => {
  const engine = { ask: jest.fn() };
  const chat = new KnowledgeChat(async () => ({ engine }));
  const classify = jest.fn(async () => classes.persona);
  await chat.askPhoto('file:///foto.jpg', caption, classify);
  expect(classify).not.toHaveBeenCalled();
  expect(chat.snapshot().rows.at(-1)).toMatchObject({
    reply: { text: expect.stringContaining('No puedo editar imágenes') },
  });
  expect(engine.ask).not.toHaveBeenCalled();
});

test('declines a follow-up edit after a photo was sent', async () => {
  const engine = { ask: jest.fn() };
  const chat = new KnowledgeChat(async () => ({ engine }));
  await chat.askPhoto('file:///foto.jpg', 'Mírame', async () => classes.persona);
  await chat.ask('Ponme un sombrero');
  expect(chat.snapshot().rows.at(-1)).toMatchObject({
    reply: { text: expect.stringContaining('No puedo editar imágenes') },
  });
  expect(engine.ask).not.toHaveBeenCalled();
});

test('reference index contains at least ten photos per enabled class and rejection', () => {
  const classesInIndex = [...new Set(references.map((row) => row.classId))].sort();
  expect(classesInIndex).toEqual([...Object.keys(classes), 'other'].sort());
  for (const id of classesInIndex) {
    expect(references.filter((row) => row.classId === id).length).toBeGreaterThanOrEqual(10);
  }
});

test('keeps both shores of a panorama in the fallback frame', () => {
  expect([...photoFrames(224, 84)]).toEqual([
    { source: [70, 0, 84, 84], destination: [0, 0, 224, 224], padded: false },
    { source: [0, 0, 224, 84], destination: [0, 70, 224, 84], padded: true },
  ]);
  expect([...photoFrames(224, 224)]).toHaveLength(1);
});

test.each(['mariposa_cydno', 'abejorro_funebris'] as const)('answers with a local source when a %s is detected', async (id) => {
  const engine = { ask: jest.fn() };
  const chat = new KnowledgeChat(async () => ({ engine }));
  const reference = references.find((row) => row.classId === id)!;
  await chat.askPhoto('file:///insecto.jpg', '', async () => matchPhoto(Float32Array.from(reference.vector)));
  expect(chat.snapshot().rows.at(-1)).toMatchObject({
    reply: { type: 'answer', id: classes[id].id, sources: [classes[id].source] },
  });
  expect(engine.ask).not.toHaveBeenCalled();
});
