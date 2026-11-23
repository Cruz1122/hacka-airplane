# App layer of the knowledge base

Read by `experiments/nlu/export_nlu.py` on top of `data/knowledge/sections/` (never edited here).
Every file is keyed by entry id; an id missing from `sections/` is an export error.

| File | What | Made by |
|---|---|---|
| `natural_replies.json` | the chat reply per entry: the curated facts rewritten as a natural answer, no title | section writers, then a fidelity review against `answer.short/variants/steps/detail` (no added facts; numbers checked by script) |
| `aug_queries.json` | 12 extra visitor messages per entry (colloquial, misspelled, fragments) for the index and the e5 fine-tune | section writers (blind to the eval set) |
| `followup_convs.json` | 2-turn conversations whose second turn is answered by the entry, for follow-up retrieval | section writers |
| `hubs.json` | composite answers for broad questions, built only from facts of their member entries | hub designer + fidelity review |
| `redirects.json` | entry id -> target id: the key's index rows retrieve the target (a meta reply such as `conversation.first_time_help` gives way to the content hub); the key stays in the catalog for featured chips | hand-kept, measured on the blind sets |

`aug_queries.json` for `conversation.off_topic_question` holds ~300 out-of-park messages (other destinations, cities' weather and transport, cooking, homework...) so the off-topic entry wins on its top-3 neighbours.

Calibration/Laya files in this folder (`clarification_labels.json`, `answer_policy.json`, `calibration.jsonl`) belong to the earlier menu design.
