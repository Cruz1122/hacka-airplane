import { draftFromEntry, emptyDraft, entryFromDraft, prepareDraft } from '../adminDraft';
import { encodeKnowledgePatch, parseKnowledgePatch, qrBytes, utf8Bytes } from '../qrPatch';

test('builds an editable QR draft for a Spanish entry and keeps authored fields', () => {
  const draft = {
    ...emptyDraft('geography'),
    title: 'Mirador del cóndor',
    answer: 'La vista principal está al sur.',
    questions: '¿Dónde está el mirador?',
    more: 'Otra vista está hacia el norte.',
    related: ['geography.laguna_otun'],
    sources: 'Guía | https://example.org/from',
  };
  const edited = prepareDraft(draft);
  expect(edited.id).toBe('geography.mirador_del_condor');
  expect(edited.questions).toBe(draft.questions);
  const payload = encodeKnowledgePatch({
    op: 'put',
    id: edited.id,
    revision: 1,
    entry: entryFromDraft(edited, 'Bad source'),
  });
  const decoded = parseKnowledgePatch(payload);
  if (decoded.op !== 'put') throw new Error('Expected put');
  expect(draftFromEntry(decoded.id, decoded.entry)).toEqual(edited);
  expect(utf8Bytes(payload)).toEqual(Uint8Array.from(Buffer.from(payload)));
  expect(qrBytes(payload)).toBe(utf8Bytes(payload).length);
});
