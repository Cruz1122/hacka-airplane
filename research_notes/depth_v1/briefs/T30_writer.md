# T3.0 writer — fact inventory (key vs complement)

Context: an offline park assistant answers each visitor question with one curated entry. New
behaviour: the first reply gives the KEY facts plus only some extras; the remaining COMPLEMENT facts
are held back for when the visitor says "sigue" / "cuéntame más". You build, per entry, the list of
atomic facts that this can draw on. Fidelity to sources is absolute: no fact without support.

## Read only
- Your shard file (given in the task). Do not read anything else. Do not browse the web.

## Output
- Write ONLY the output path given in the task: JSONL, one row per entry, in shard order.
- Write the file skeleton-first: append each entry's row as soon as it is done.
- Reply with exactly one line: "<output path> <rows>".

## Row schema
{"entry_id": "...", "facts": [{"fid": "f1", "text": "<one atomic fact, natural Spanish, one sentence>", "class": "key|complement", "support": [<support refs>]}], "note": "<optional, short>"}

Support refs (at least one per fact):
- {"field": "answer.short" | "answer.variants" | "answer.steps" | "answer.detail" | "answer.reflection" | "L0"} when the fact is stated there.
- {"qid": "<evidence window qid>", "quote": "<the exact substring copied from that window's text, 40-300 chars, copied character for character>"} when the fact comes from an evidence window.

## Rules
1. Atomic: one claim per fact. Keep numbers, units, dates, names and phone numbers exactly as in the source.
2. KEY = what answers the entry's label and its listed `questions`, plus everything in L0 that a
   visitor needs to act safely. Any fact that one of the listed questions asks for directly is KEY.
3. If `all_key_forced` is true: every fact is KEY (safety/rule/action/emergency entries) and you use
   only answer fields and L0 (no evidence windows are given).
4. Always KEY: procedure steps, every caveat or warning, "puede cambiar / confirma con PNN" style
   disclaimers.
5. COMPLEMENT = true, sourced extras that nobody in `questions` asks for directly: details from
   answer.detail/variants/reflection not in the key answer, and facts from evidence windows that are
   clearly about THIS entry's topic and this park. Volume matters: extract **at least 4 complements
   per entry** (up to 10) whenever its evidence windows hold on-topic facts. Read every window. If an
   entry gets fewer than 4, say why in `note` (e.g. "windows off-topic").
6. An evidence fact must be stated in the quote itself. No inference, no generalisation, no facts
   about other places presented as this park's.
7. Never state: a frailejón growth rate in cm per year, albedo percentages, ">90 %" water shares,
   "3-4 millones" beneficiaries, 5-10 °C microclimates, Polylepis at 3,500 m, camping cutoffs at
   16:30/17:30, comparendo amounts, N95 advice. These were purged as unsupported.
8. Spanish of Colombia, addressed neutrally (no "tú/usted" needed in facts). No emojis.
