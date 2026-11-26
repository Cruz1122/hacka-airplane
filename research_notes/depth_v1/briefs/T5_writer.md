# T5 writer — follow-up conversations

An offline park assistant (Parque Nacional Natural Los Nevados, Colombia) answers each visitor
message with ONE curated entry. Visitors ask follow-ups that only make sense with the previous turn.
You write training conversations so the retriever learns to pick the right entry for every turn.

## Read only
- The shard given in the task. Nothing else. No web.

## Output
- Write ONLY the output path given in the task: JSONL, one row per conversation, appended entry by
  entry as you go (so partial work survives). Reply with one line: "<output path> <rows>".

{"entry_id": "<target id>", "conv_id": "<target id>#c1", "type": "related|switch|chain3|elliptic",
 "turns": [{"text": "...", "entry_id": "<id that answers this turn>"}, ...]}

## Per entry: 12 conversations whose LAST turn is answered by the target entry
- 3 × `related` (2 turns): turn 1 is a specific question answered by one of the entry's `related`
  entries; turn 2 moves to the target, naturally linked ("¿y eso aplica también para…?").
- 2 × `switch` (2 turns): turn 1 is about one of the `unrelated` entries; turn 2 abruptly asks
  about the target, as a complete question (a real topic change).
- 2 × `chain3` (3 turns): turns 1–2 about related entries or the target itself, turn 3 on the target.
- 1 × `elliptic` (2 turns): turn 1 about a related entry; turn 2 is short and elliptic and only
  makes sense in context ("¿y para niños?", "¿y cuánto vale?", "¿y en Brisas?"), answered by the target.
- 4 more of any type (surplus; reviews and the leak check drop ~25 %).

## Rules
1. Every turn's `entry_id` is the target, one of its `related` ids, or one of its `unrelated` ids.
   Pick the entry whose answer (L0) would really answer that turn.
2. The last turn MUST be answered by the target's L0. Do not ask for facts the L0 does not give.
3. Never reuse an `examples` text or the label in ANY turn, not even lightly edited. Avoid ultra-generic
   turns that any visitor would type ("¿y para niños?" alone is fine once per entry, not more).
4. Real visitor Spanish from Colombia: colloquial, short, some typos, no accents sometimes, the odd
   English turn (≤1 in 10). Vary wording.
5. No turn may be a bare continuation cue: "sigue", "continúa", "cuéntame más", "y qué más", "más",
   "¿por qué?", "explícame mejor", "dale". The app handles those by rule.
6. Do not mention the app, the entries or ids in the text.
7. `conversation` section entries (greetings, thanks, off-topic, chit-chat): the last turn is that
   chit-chat after a normal park question (e.g. turn 1 about a related/unrelated entry, turn 2
   "listo, gracias"). Use types `related`/`switch`/`chain3` as fits; skip `elliptic` for them.
8. Safety entries: keep the visitor's question realistic and calm; never invent medical advice.
