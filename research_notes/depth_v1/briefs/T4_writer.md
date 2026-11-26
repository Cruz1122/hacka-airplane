# T4 writer — query variants

An offline park assistant (Parque Nacional Natural Los Nevados, Colombia) answers each visitor
message with ONE curated entry. You write new ways a visitor would ask for each entry, so the
retriever learns to find it. The first reply gives only the entry's KEY facts.

## Read only
- The shard given in the task. Nothing else. No web.

## Output
- Write ONLY the output path given in the task: JSONL, one row per variant, appended entry by entry
  as you go. Reply with one line: "<output path> <rows>".

{"vid": "<entry_id>#v01", "entry_id": "...", "bucket": "colloquial|misspelled|fragment|situational|english|specific_fact", "text": "..."}

## Per entry: `per_entry` variants following the shard's `mix` (the surplus absorbs drops)
- colloquial: Colombian visitor Spanish ("parce", "qué más", "toca", "¿será que…?"), natural.
- misspelled: typos, no accents, phone-keyboard style ("q", "xq", "aki"), still understandable.
- fragment: 1–4 words, like a search box ("tarifa estudiante", "frailejones").
- situational: indirect, from the visitor's situation ("voy con mi abuela de 70 años, …").
- english: a natural English question from a foreign visitor.
- specific_fact: asks for ONE of the entry's `key_facts` only.

## Rules
1. Every variant must be fully answered by the entry's `key_facts`. Never ask for anything else (no
   prices, hours, heights, names that are not in `key_facts`).
2. Never ask what the `do_not_ask` labels cover: those are other entries.
3. Do not copy or lightly reword the `examples` or the label. Each variant of an entry must differ
   from the others in wording, not only in one word.
4. No bare continuation cues ("sigue", "cuéntame más", "y qué más", "¿por qué?").
5. Single line, no ids, no mention of the app.
