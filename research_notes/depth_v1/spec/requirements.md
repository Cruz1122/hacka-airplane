# Requirements — Depth, variants and follow-ups (depth_v1)

Status: approved for execution. Spec-driven: `requirements.md` (what), `design.md` (how),
`tasks.md` (who, in what order, done when). Do not implement anything a requirement here does not
ask for.

## North star

**Fill the knowledge base with sourced variants and follow-ups.** Every one of the 806 entries ends
with:

- many more ways to be asked;
- many more conversations that lead to it;
- depth for "sigue": at least 2 extra sourced layers whenever any source supports them;
- **many ways to answer**: asking the same thing again gets a differently worded reply with the
  same facts, every time.

Volume is the goal. Fidelity to sources is the constraint that is never traded.

## Baseline (2026-11-23, re-measured in T0)

| Item | Today |
|---|---|
| Entries / sections | 806 / 15 |
| Corpus examples | 10,297 (median 12 per entry) |
| `aug_queries.json` | 10,517 (median 12 per entry) |
| `followup_convs.json` | 805 entries, ~4 two-turn convs each |
| Entries with non-null `answer.detail` | 163 (zero in flora, fauna, weather_volcano, health_safety, rules, conversation) |
| Depth served on "sigue" | none (cue regex misses "sigue/más/cuéntame más/por qué"; engine keeps no last entry) |
| ft4 follow-up accuracy (v3) | 49% |
| Reply texts per entry | 1 (`natural_replies.json`); the same question always gets the same text |

## Functional requirements (EARS)

### R1 — Query variants (volume)

- **R1.1** Every entry SHALL gain **≥20 new approved query variants**. That is ≥16,000 in total;
  `conversation` entries are exempt beyond 10.
- **R1.2** Each entry's variants SHALL follow this mix, ±1 per bucket:
  - 6 colloquial Colombian;
  - 4 misspelled or without accents;
  - 3 fragments of 1–4 words;
  - 3 indirect or situational ("voy con mi abuela de 70…");
  - 2 English;
  - 2 questions about a single specific fact of the answer.
- **R1.3** A variant SHALL be answerable by its entry's current answer. A variant that needs a fact
  not in the entry is `drop`.
- **R1.4** WHEN two variants of one entry have e5 cos ≥0.93, or match after normalisation, THE
  pipeline SHALL keep one.
- **R1.5** WHEN a variant has cos ≥0.88 to another entry's text, THE pipeline SHALL send the pair
  to pair judgment (`distinct | also_answers | query_dependent`). `query_dependent` rows SHALL NOT
  be used for training.

### R2 — Follow-up conversations (volume)

- **R2.1** Every entry SHALL gain **≥8 new approved multi-turn conversations** in which the last
  turn is answered by that entry. That is ≥6,400 in total.
- **R2.2** Per entry, the conversations SHALL include:
  - 3 two-turn conversations whose first turn is a specific question about a `related` entry;
  - 2 two-turn topic switches (the first turn is about an unrelated entry);
  - 2 three-turn chains;
  - 1 elliptic turn ("¿y para niños?", "¿y cuánto cuesta?").
- **R2.3** Every turn in a conversation SHALL carry the id of the entry that answers it, so that
  intermediate turns are labelled too.
- **R2.4** No conversation turn SHALL be a bare continuation cue (R4.1). Those cues are handled by
  rule, not by retrieval.

### R3 — Depth layers for "sigue" (volume with sources)

- **R3.1** Every entry with sources SHALL get **2 depth layers**:
  - L1 explains why or how;
  - L2 gives specifics (numbers, where, when).

  Each layer SHALL have 40–70 words. `conversation` and `kind: chat` entries are exempt.
- **R3.2** Every layer sentence SHALL list its support: a corpus field or a literal quote ref. A
  sentence without verified support SHALL be removed.
- **R3.3** IF an entry's current sources cannot support L1/L2, THEN a research task SHALL look for
  official or academic public sources and propose them through `knowledge.py` with quotes. Only if
  that also fails is the entry marked `no_headroom`, with the reason logged.
- **R3.4** Target: **≥90% of non-exempt entries** with L1, and **≥70%** with L2. The rest are
  `no_headroom`, each with a logged reason.
- **R3.5** New facts SHALL enter the corpus only through `add-park-knowledge`
  (`knowledge.py stage → apply → validate_knowledge.py`, Errors: 0). The app layer SHALL only
  re-layer facts that are already in the entry.
- **R3.6** Safety and rule caveats SHALL stay in L0, never only in a deeper layer.
  - For entries with `kind: safety` (77) or `kind: rule` (123), the canonical L0 text SHALL remain
    byte-identical.
  - Their paraphrases (R6) SHALL contain every caveat, number and step of the canonical text.

### R4 — Runtime continuation

- **R4.1** WHEN the whole message, accent-folded and ≤6 words, matches the continuation cue
  (`sigue, siga, continua, mas, que mas, y que mas, cuentame mas, dime mas, mas detalle(s),
  explicame mejor, amplia`, plus typos) AND there is a last answered entry, THE engine SHALL serve
  that entry's next unserved layer without embedding.
- **R4.2** WHEN the layers are exhausted, THE engine SHALL serve the next unserved entry of the
  `walk` (a related id), with a bridge of one fact-free clause.
- **R4.3** WHEN the walk is also exhausted, THE engine SHALL say "No tengo más detalle verificado
  sobre esto" and name 2 related topics in text. No menu.
- **R4.4** WHEN a continuation cue arrives with no last answered entry, THE engine SHALL reply
  "¿Sobre qué tema quieres que siga?".
- **R4.5** WHEN the message is "por qué" alone, THE engine SHALL serve the unserved `why` layer if
  one exists. Otherwise the message follows the normal follow-up path.
- **R4.6** WHEN retrieval returns the last answered entry again (the same question re-asked),
  THE engine SHALL serve the next unserved paraphrase of that entry's L0 (R6). It SHALL never
  repeat the text just shown.
- **R4.7** WHEN a turn is urgent, abstains or is off-topic, or the context is reset, THE engine
  SHALL clear the continuation state.
- **R4.8** WHEN `policy.continuation` is null or missing, THE engine SHALL behave exactly as today.

### R6 — Reply variants: same question, different answer every time

- **R6.1** Every non-exempt entry SHALL have **≥8 approved paraphrases of L0** (the canonical L0
  plus 7 or more). Each depth layer SHALL have **≥4 approved paraphrases**. In total that is
  ≥6,000 L0 paraphrases plus the layer paraphrases.
- **R6.2** Each paraphrase SHALL carry exactly the facts of its source text: no added fact, no
  dropped caveat, and identical numbers, units, dates, names and phone numbers, all checked by
  script.
- **R6.3** Paraphrases SHALL actually differ.
  - Within an entry, every pair SHALL have character-trigram Jaccard < 0.55.
  - No two paraphrases SHALL share their first 4 words.
  - The set SHALL use at least 3 different structures: direct answer first, context first,
    advice first, or a question back that is answered at once.
- **R6.4** Register SHALL vary within limits: warm, neutral, brief and more explained. It SHALL
  stay natural Colombian Spanish addressed to "tú", with no slang that changes meaning, no emojis
  and no jokes in `kind: safety` entries.
- **R6.5** WHEN an entry is answered again in the same app session, THE engine SHALL serve the
  next unserved paraphrase.
  - The order is shuffled per session from a seed.
  - After all paraphrases are used, the engine reshuffles and never starts with the text just
    shown.
  - This applies to L0, to every depth layer, and to walk entries.
- **R6.6** Exceptions:
  - `emergency_direct` entries (40, `knowledge/answer_policy.json`) SHALL rotate only among
    paraphrases that a second verifier approved for 100% caveat and step coverage. If an entry
    has fewer than 3 such paraphrases, it keeps its canonical text. Consistency beats variety in
    an emergency.
  - `kind: chat` entries SHALL rotate freely.

### R5 — Evaluation and ft5 readiness

- **R5.1** Before any new variant or conversation is written, blind_v4 SHALL be written by
  agents that have never seen the corpus, then labelled, split and sealed. Contents:
  - single-turn: ≥600 rows;
  - multi-turn: ≥300 follow-up turns;
  - continuation: 150 positives and 150 negatives.
- **R5.2** New variants and conversations SHALL have 0 leaks against v4: exact match or e5 cos ≥0.93.
- **R5.3** A reproducible ft5 dataset ZIP SHALL be produced, with no training run. It contains:
  - training rows;
  - hard-negative clusters;
  - v4-dev, and the v4-sealed hash;
  - validators and `MANIFEST.json`;
  - `QUALITY_REPORT.md` and `COLAB_HANDOFF.md`.

## Non-functional requirements

- **N1 Fidelity:** 0 unsupported sentences in depth layers and 0 fact changes in paraphrases.
  Checks:
  - a script verifies 100% of quotes and numbers;
  - a different model family verifies entailment on 100% of `health_safety` and `rules`, and on
    ≥10% of every other section.
- **N2 Label quality:** a reviewer from another model family judges every variant and every
  conversation turn (`ok | fix | drop`), and Luna arbitrates every `fix`.
- **N3 Index size:** the phone index does not grow by default. New rows go to the training pool. A
  row enters the index only if an index-only A/B on v2 with ft4 shows a gain.
- **N4 No regression:** ft4 single-turn accuracy on v4-dev with the final index ≥ with today's
  index (Wilson CI reported).
- **N5 Reproducibility:** every artifact is generated by a script from reviewed JSONL, and its
  inputs are hashed in a manifest.
- **N6 Context budget:** each subagent's read set stays under 40% of its window. Work is sharded
  and written skeleton-first.

## Acceptance (the mission is done only when all hold)

| Id | Check | Pass |
|---|---|---|
| A1 | approved new variants per entry (script) | ≥20 for 100% of non-conversation entries |
| A2 | approved new conversations per entry | ≥8 for 100% of entries |
| A3 | L1 / L2 coverage of non-exempt entries | ≥90% / ≥70%, every gap logged `no_headroom` with a reason |
| A4 | unsupported depth sentences | 0 |
| A5 | E2E "ask → sigue ×4" over all 806 entries | 0 repeated replies; ≥3 distinct turns where headroom exists |
| A6 | continuation detector on v4-dev | precision ≥98%, recall ≥90% |
| A7 | urgent clears state; null policy = today | unit tests green |
| A8 | leaks vs v4 | 0 |
| A9 | `validate_knowledge.py`; `export_nlu.py` + lint; mobile tests, typecheck, lint | all green |
| A10 | ft5 ZIP validated on a clean extraction | exit 0, no local paths or user data |
| A11 | same question ×8 on every non-exempt entry (E2E, real engine) | 8 different texts for 100% of entries (emergency entries: ≥3 or canonical, per R6.6) |
| A12 | paraphrase fidelity and distinctness (script + reviewer) | 0 fact changes; 100% pass R6.3 |

## Non-goals

- Training ft5. Phone benchmarks, unless the user asks.
- Menus or separate screens. Generative answers.
- Replacing the canonical L0 replies. They stay as one of the paraphrases.
