# Knowledge base contract

One JSON file per section (vector space): `data/knowledge/sections/<section_id>.json`.
Schema: [schemas/knowledge-section.schema.json](schemas/knowledge-section.schema.json).
Content (examples, answers) is Spanish unless `lang` says otherwise. Keys are English.

## Section order

The order follows a visitor's trip. It sets the section order in the gateway manifest, the order
of suggestions, and which section wins ties.

| order | id | Covers |
|---|---|---|
| 1 | `actions` | Register a visit, report an emergency, check a report (hand-off to the FSM) |
| 2 | `health_safety` | Altitude sickness, hypothermia, shelters, emergency contacts, getting lost |
| 3 | `weather_volcano` | Weather, volcanic activity and alerts, what they mean for the visit |
| 4 | `access` | How to get there, roads, sectors, entry points, transport, parking |
| 5 | `booking_fees` | Booking, fees, payment, entry requirements, age, insurance, guides |
| 6 | `hours_status` | Opening hours, open or closed, seasonal or conservation closures |
| 7 | `preparation` | Clothing, gear, food and water, fitness, children |
| 8 | `activities` | What to visit, trails, viewpoints, camping, photography, birding |
| 9 | `rules` | Park rules phrased for visitors: pets, drones, fire, trash, off-trail |
| 10 | `services` | Visitor center, toilets, food, phone signal, accessibility |
| 11 | `fauna` | Animals by group, where and when to see them, protected species |
| 12 | `flora_ecosystems` | Páramo, frailejones, wetlands, glaciers, water |
| 13 | `geography` | Peaks, lakes, heights, departments, park vs volcano |
| 14 | `history_culture` | Armero 1985, lahars, Indigenous names, park history, communities |
| 15 | `conversation` | Greetings, thanks, goodbyes, "what can you do" |

Safety comes first so it wins ties: a false alarm costs one extra question, while a missed
emergency is not acceptable.

## Section file

```json
{
  "contract_version": 1,
  "id": "access",
  "order": 4,
  "title": "Cómo llegar y accesos",
  "description": "Rutas, vías, sectores y puntos de entrada al parque, y cómo llegar desde cada ciudad.",
  "retrieval": {
    "profile": "procedure",
    "bm25_weight": 0.2,
    "top_k": 2,
    "min_score": null,
    "entity_filters": ["origin", "sector"]
  },
  "clarification": {
    "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
    "bank": [
      "¿Desde qué ciudad sales?",
      "¿A qué sector del parque quieres ir: norte (Brisas), Santa Isabel o Tolima?"
    ],
    "slot_questions": {
      "origin": "¿Desde qué ciudad vienes?",
      "sector": "¿A qué sector del parque vas?"
    },
    "fallback": "No tengo esa ruta exacta, pero puedo contarte cómo llegar desde Manizales o Murillo."
  },
  "featured": ["access.from_manizales", "access.sectors"],
  "entries": []
}
```

| Field | Required | Meaning |
|---|---|---|
| `contract_version` | yes | Always `1` for now |
| `id` | yes | Snake-case section id, unique |
| `order` | yes | Position in the list above |
| `title`, `description` | yes | The description is also embedded into the gateway |
| `retrieval.profile` | yes | `lookup`, `procedure`, `explain`, `rules`, `safety` or `chat` |
| `retrieval.bm25_weight` | no | 0-1; 0 means dense only |
| `retrieval.top_k` | no | Entries this section passes to System 1 (default 2) |
| `retrieval.min_score` | no | Section-specific acceptance threshold; `null` = calibrated global |
| `retrieval.entity_filters` | no | Entity names entries may declare in `entities` |
| `clarification.between_entries` | yes | Template with `{label_a}` and `{label_b}` |
| `clarification.bank` | yes | 2-10 questions to disambiguate within this section |
| `clarification.slot_questions` | no | One question per entity in `entity_filters` |
| `clarification.fallback` | yes | Reply when the section is the closest one but nothing matches |
| `featured` | no | Entry ids suggested in fallbacks |
| `entries` | yes | List of entries (below) |

## Entry

```json
{
  "id": "access.from_manizales",
  "label": "cómo llegar desde Manizales",
  "kind": "procedure",
  "audience": "visitor",
  "lang": "es",
  "examples": [
    "cómo llego desde Manizales",
    "qué vía cojo para ir desde Manizales",
    "ruta desde Manizales al nevado",
    "how do I get there from Manizales"
  ],
  "hard_negatives": ["dónde queda Valle de las Tumbas"],
  "entities": {"origin": ["manizales"], "sector": ["norte"]},
  "needs": [],
  "answer": {
    "short": "Desde Manizales, la referencia para el sector norte es la vía a Bogotá por Letras...",
    "variants": ["Si sales de Manizales hacia Brisas, toma como referencia la vía a Bogotá por Letras..."],
    "steps": [["Desde Manizales, toma la vía hacia Bogotá por Letras..."]],
    "detail": null,
    "reflection": "Puedes preparar la ruta con tiempo y adaptar el plan a las condiciones que encuentres."
  },
  "sources": [
    {
      "label": "Parques Nacionales Naturales",
      "url": "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/",
      "retrieved_at": "2026-11-21"
    }
  ],
  "last_verified": "2026-11-21",
  "valid_until": null,
  "related": ["access.sectors", "access.valle_tumbas"],
  "tags": ["ruta", "vía"]
}
```

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | `<section_id>.<snake_case>`, globally unique, never reused |
| `label` | yes | Short topic name. System 1 compares it to the question, so labels inside a section must be clearly different |
| `kind` | yes | `fact`, `procedure`, `explanation`, `rule`, `safety`, `action` or `chat` |
| `audience` | yes | `visitor` or `staff`. Only `visitor` entries are answered |
| `lang` | no | Default `es` |
| `examples` | yes | ≥ 4 in Phase 1, ≥ 10 from Phase 2 on; how a visitor would ask |
| `hard_negatives` | no | Similar questions that belong to another entry (used in evaluation and thresholds) |
| `entities` | no | Values for the section's `entity_filters` |
| `needs` | no | Entities that must be known before answering; missing ones trigger a slot question |
| `answer.short` | yes | 1-3 sentences, the default reply |
| `answer.variants` | no | Rephrasings of `short`, rotated to avoid repetition |
| `answer.steps` | no | Follow-up depth: a list of levels, each level a list of alternative texts |
| `answer.detail` | no | Optional extra paragraph |
| `answer.reflection` | no | Optional closing line for the visitor |
| `action` | only when `kind` is `action` | FSM tool name to hand off to, e.g. `register_visit` |
| `sources` | yes | At least one, with `url` and `retrieved_at` |
| `last_verified` | yes for numbers, hours, prices, phones | ISO date |
| `valid_until` | no | ISO date after which the entry must not be served |
| `related` | no | Entry ids for "¿quieres saber también…?" |
| `tags` | no | Free keywords, also fed to BM25 |

## Mapping from `conocimiento.json` (v0)

| v0 field | Contract field |
|---|---|
| `label` | `label` |
| `examples` | `examples` |
| `reply` | `answer.short` |
| `variants` | `answer.variants` |
| `steps` | `answer.steps` |
| `detail` | `answer.detail` |
| `reflection` | `answer.reflection` |
| `source` (`label`, `url`) | `sources[0]` plus `retrieved_at` = conversion date |
| — | `id`, `kind`, `audience`, section: assigned during conversion (see the Phase 1 mapping in [plan-knowledge-system.md](plan-knowledge-system.md)) |

## Validation rules (enforced by the validator, beyond the schema)

1. Entry ids are unique across all sections and start with their section id.
2. No example appears in two entries; near-duplicates (cosine ≥ 0.95) across entries are reported.
3. Every `related` and `featured` id resolves; every `hard_negatives` text is an example of some other entry or is flagged for review.
4. Every entity in `needs` has a `slot_questions` entry in its section.
5. Answers containing digits (hours, prices, phones) have `last_verified`.
