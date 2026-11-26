# T3 layer writer — what the park assistant says after "sigue"

An offline park assistant (Parque Nacional Natural Los Nevados, Colombia) answers a question with a
short first reply (`canonical_L0`, key facts). When the visitor says "sigue" / "cuéntame más", it
shows a deeper layer. You write those layers, ONLY from the entry's `complements`: facts that are
already verified against sources. Fidelity is absolute.

## Read only
- Your shard file (given in the task). Nothing else. No web.

## Output
Write ONLY the output path given in the task. JSONL, one row per layer text, entry by entry
(append each entry as soon as it is done):
{"lid": "<entry_id>#L1a", "entry_id": "...", "layer": 1, "kind": "why|how", "atoms": ["f6","f8"], "text": "..."}
{"lid": "<entry_id>#L1b", ...same layer and atoms, different wording...}
{"lid": "<entry_id>#L2a", "entry_id": "...", "layer": 2, "kind": "specifics", "atoms": [...], "text": "..."}
{"lid": "<entry_id>#L2b", ...}

## Rules
1. `layers_wanted` 1: write layer 1 only, using every complement. `layers_wanted` 2: split the
   complements in two disjoint groups: layer 1 (`why` or `how`: causes, processes, what it means)
   and layer 2 (`specifics`: numbers, places, dates, names). Every complement goes in exactly one layer.
2. Two texts per layer (`a`, `b`): same facts, clearly different wording and sentence order.
3. `atoms` = the fids that the text states. Both texts of a layer carry the same atoms.
4. State each tagged complement faithfully: numbers, units, dates and names exactly as written.
   You may restate a key fact briefly as context. Add NOTHING else: no reason, consequence,
   example, advice or comparison that the facts do not give. No connector that invents a relation
   between facts ("por lo que", "aunque", "como referencia", "gracias a"); join facts with neutral
   words ("y", "además", "también") or separate sentences. Keep who does what and every qualifier
   ("de diferentes edades", "según Parques Nacionales").
5. 40-70 words is the target, but facts beat length: with few facts write fewer words (minimum 20).
   Never pad with filler. Maximum 90 words.
6. Natural Colombian Spanish, a continuation of the first reply: do not repeat the label as a
   heading, do not start with "Además" in every text, no emojis, no lists, no bridge phrases
   like "Relacionado con esto" (the app adds those).
7. Self-check (required): `cd /home/cruz1122/dev/hacka-airplane/research_notes/depth_v1/tools && python3 check_layers.py <your output path>`.
   Rewrite rejected rows in place, up to 3 rounds.

Reply with one line: "<output path> <rows> <rejected after self-check>".
