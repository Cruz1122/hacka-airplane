# T5b reviewer — reply paraphrases

You check reply texts another model wrote for an offline park assistant. Each is a rewording of an
entry's canonical answer (`canonical_L0`) that must keep every key fact and may carry a few tagged
complement facts. A wrong text tells a visitor something false in a national park with volcanoes and
altitude: be strict on facts, lenient on style.

## Read only
- The shard and the paraphrases file given in the task. Nothing else. No web.

## Output
Write ONLY the output path given in the task: JSONL, one row per paraphrase, in input order,
appended in batches of ~50.

{"pid": "...", "same_facts": true, "caveats_kept": true, "atoms_exact": true, "natural": true,
 "verdict": "ok|fix|drop", "fixed_text": "<only for fix>", "note": "<≤12 words, required unless ok>"}

(In a SECOND review pass the task also asks for `"emergency_ok": true|false`, see rule 6.)

## Rules
1. `same_facts`: every `key_facts` item is stated, with the same numbers, names, hours and phone
   numbers, and NOTHING is stated that is not in `key_facts`, the tagged complements or
   `canonical_L0` (no invented detail, no softened or strengthened claim).
2. `caveats_kept`: every warning, condition, "puede cambiar", "confirma con…" and every step (in
   order) of the canonical text survives.
3. `atoms_exact`: the text states exactly the complements listed in `atoms`, no more, no fewer.
4. `natural`: reads like a person from Colombia talking to "tú"; no emojis; for `kind: safety` or
   `emergency: true`, calm and without jokes.
5. Verdict: `ok` when all four are true. `fix` when one small edit repairs it: give the whole
   corrected text in `fixed_text` (same facts, same atoms). `drop` otherwise.
6. Second pass only (`emergency_ok`): true only if the text keeps 100% of the caveats and 100% of the
   steps of the canonical text, in order, with the emergency number exactly as given. Any doubt: false.
