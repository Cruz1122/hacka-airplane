# T5b writer — reply paraphrases (same question, different answer)

An offline park assistant (Parque Nacional Natural Los Nevados, Colombia) answers each visitor
question with ONE curated entry. Today it always prints the same canonical text. You write
alternative versions of that first answer, so a visitor who asks again gets different wording, and
so the first answer holds back some extras for when the visitor says "sigue".

## Read only
- The shard given in the task. Nothing else. No web.

## Output
Write ONLY the output path given in the task: JSONL, one row per paraphrase, appended entry by entry
(partial work must survive).

{"pid": "<entry_id>#p01", "entry_id": "...", "structure": "direct|context|advice|question_back",
 "register": "warm|neutral|brief|explained", "atoms": ["f7", "f9"], "text": "..."}

## Per entry: `per_entry` (10) paraphrases of `canonical_L0`
1. **Key facts, all of them, every time.** Each text states every `key_facts` item, with identical
   numbers, units, dates, hours, names and phone numbers. Every caveat, warning and "confirma con…"
   stays. Steps stay in order. Never add anything that is not in `key_facts`, the complements you
   tag, or `canonical_L0`.
2. **Complements: hold some back.** `atoms` lists the `complements` fids the text states; state them
   fully, tag exactly those (none untagged, none tagged but missing). At most `max_atoms` per text.
   Vary the subsets across the 10 texts (at least 3 different subsets when there are ≥2
   complements; some texts with none). Never invent a fid.
3. **Numbers:** every value in `numbers_required` appears in every text, written the same way
   (keep "8:00 a. m.", "$ 25.000", "123" as given). A text may contain no other number except those
   of the complements it tags.
4. **Really different texts.** No two texts of an entry (nor a text and `canonical_L0`) start with the
   same 4 words, and none reuse long stretches of each other: rewrite sentences, reorder, change
   connectors. Use ≥3 structures across the 10:
   - `direct`: the answer first;
   - `context`: one short clause of context, then the answer;
   - `advice`: practical advice first, then the facts;
   - `question_back`: opens with a short rhetorical question that is answered at once
     ("¿Vas a subir al Ruiz? Entonces…").
   And spread registers: `warm`, `neutral`, `brief` (shortest that still has every key fact),
   `explained` (a bit more connective tissue, no new facts).
5. **Voice:** natural Colombian Spanish addressed to "tú". No slang that changes meaning, no emojis,
   no exclamation spam. `kind: safety` and `emergency: true` entries: calm and clear, no jokes, no
   "parce", keep every step and the emergency number exactly; prefer `direct`/`advice`.
   In these entries vary only the wording AROUND the facts: keep the actions in the canonical
   order, never add a detail (no "por el viento", no "el guía coordina"), never move who does
   what, never soften or harden a requirement ("debes" stays "debes").
6. Length: about the same as `canonical_L0` (brief may be shorter, explained ≤1.5×). The check rejects any text longer than 2× (the longer of the canonical and the key facts together, + the complements it tags). Keep every key fact even when that makes the text longer than the canonical.
7. Do not mention the app, entries, ids or "según la fuente".
8. `kind: rule` entries: state the rule and only what the canonical says around it. Do not add a
   reason ("para proteger la fauna"), a consequence, an example or advice that the canonical does
   not give; reviewers drop those as unsupported (seen in 26-36 % of rule texts).

## Self-check before replying (required)
Run: `cd /home/cruz1122/dev/hacka-airplane/research_notes/depth_v1/tools && python3 check_replies.py <your output path>`
It prints rejected rows (missing number, too many atoms, same first 4 words, character-trigram
similarity ≥0.55 to another text "vs <pid>" or to the canonical) and entries below goal (8 surviving
texts, 3 structures, 2 subsets). Rewrite the rejected rows in place (same pid) and re-run, up to 4
rounds, until every entry passes.

The similarity is measured after removing the words of the key facts (names, places, numbers you
must repeat anyway), so it judges only the wording around them. Aim for ~0.40.
The facts themselves (names, numbers) are shared; everything AROUND them must differ. Change the
verbs, connectors and sentence order; split or merge sentences; turn a list into prose or prose
into a short list; open with a different element each time; use synonyms for common words
("ingresar/entrar/acceder", "debes/toca/conviene"). A text that just swaps two words is still too
close. Never pad a text with filler sentences that add nothing; change the wording instead. Then reply with one line: "<output path> <rows> <entries below goal>".
