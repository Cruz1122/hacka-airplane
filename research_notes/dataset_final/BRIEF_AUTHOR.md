# Query author brief (G4, G5, G6, X1, X2, X3, X4)

Read `$W/BRIEF_COMMON.md` first. You write **new visitor questions** with their correct FAQ, used
for training and for sealed evaluation (you will not know which; write every row as if it were test).

## Output `$W/authored/<AGENT>.jsonl`, one JSON object per line

```json
{"qid": "G4-0001", "q": "toca pagar parqueadero en brisas o eso va incluido",
 "family": "G4-f001", "scenario": "colloquial", "case": "answerable",
 "gold": "booking_fees.vehicle_entry_fee", "acceptable": ["booking_fees.vehicle_entry_fee"],
 "near_ids": ["booking_fees.entry_fee_adults"], "why": "parking fee, not the person entry fee",
 "author": "G4"}
```

- `family`: one visitor intent. 1–2 surface forms per family (same family id), never more. Families
  never repeat an intent you already wrote.
- `case`:
  - `answerable`: `gold` = the FAQ whose answer text (`short`, plus `detail`/`steps` from
    `kb_view.jsonl` when needed) actually answers the question. `acceptable` = **every** FAQ whose
    answer also fully answers it (gold included). Judge by the answer text, not the label.
  - `none`: no FAQ in the catalog answers it. Search the catalog (`grep -i`, `jq`) before deciding;
    `gold: null`, `acceptable: []`, `near_ids` = the closest FAQs you checked and rejected.
  - `ambiguous`: under-specified; 2–3 FAQs are plausible and a clarification is the right reply.
    `gold: null`, `acceptable` = the plausible FAQs.
- `near_ids`: 1–3 close FAQs that do **not** answer the question (they become hard negatives). Only
  list one when you can say in `why` exactly what it does not answer. Never list an FAQ that also
  answers it — that one goes in `acceptable`.
- `scenario` (one of): `natural`, `colloquial`, `typo`, `short`, `long`, `indirect`, `compound`,
  `confusable`, `cross_section`, `near_miss`, `out_of_scope`, `ambiguous`, `emergency`, `english`.
- Write how real Colombian tourists type: no accents, slang (parce, toca, qué tal, bacano), typos,
  WhatsApp style, incomplete sentences, long stories with the question at the end. Do **not** copy
  the FAQ label or answer wording into the question; a tourist does not know the label.
- Do not paraphrase your own earlier rows to fill the quota. Fewer, sharper rows beat more rows.
- No real personal data.

Before finishing, run a check script: every ID exists in `kb_catalog.jsonl`; `gold ∈ acceptable`
for answerable rows; `near_ids ∩ acceptable = ∅`; qids unique; ≤ 2 rows per family.
