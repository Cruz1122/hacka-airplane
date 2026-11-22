# Integration report

Curation v2 integration of the 15 approved `.final.json` proposals only. No sections were skipped.
Combined dry run staged 347 operations: 0 add, 347 update, 0 delete. All warnings were empty (`orphaned_hard_negatives=[]`, `similar_labels=[]`).

| Section | Operations | Apply | Transaction ID | Warnings |
|---|---:|---|---|---|
| actions | add 0, update 10, delete 0 | applied | b6713d5c195d44c8a291c956cd04ea7c | none |
| health_safety | add 0, update 59, delete 0 | applied | 8aa177bdc97a46b9b658ee06c962e221 | none |
| weather_volcano | add 0, update 27, delete 0 | applied | 66a2c15b38004a2f822f5306a1f1ee2a | none |
| access | add 0, update 11, delete 0 | applied | 6ae3a802b9ae4efd97b7939ce1a1a534 | none |
| booking_fees | add 0, update 43, delete 0 | applied | 3a60ad6191e54406bfd23ba5655ff398 | none |
| hours_status | add 0, update 37, delete 0 | applied | 7d83be31b14a4c9cbdec95b444c88762 | none |
| preparation | add 0, update 7, delete 0 | applied | 8815485c1a304757b09cbab3818e44ec | none |
| activities | add 0, update 5, delete 0 | applied | 650191e3a9dd41869be93e0c7d685c46 | none |
| rules | add 0, update 40, delete 0 | applied | c34ca94e621b4e2e8e56079073e6867a | none |
| services | add 0, update 22, delete 0 | applied | 7f7127e82694404ca44d4d9797ac50fc | none |
| fauna | add 0, update 31, delete 0 | applied | fa647aa30bba48dcbfc78a9163df4f4a | none |
| flora_ecosystems | add 0, update 18, delete 0 | applied | 32fbabbf98ae40269c2ff2a924440049 | none |
| geography | add 0, update 6, delete 0 | applied | 4bfa1b1280f841e3a310d029fadc3fa6 | none |
| history_culture | add 0, update 3, delete 0 | applied | 26a17dd499d44532828056fccbc97613 | none |
| conversation | add 0, update 28, delete 0 | applied | eb2689f724864a82a7da09c38ea7c4f8 | none |

## Verification (last output line)
- Preflight: hashes matched `sections_before.sha256.json`; git status recorded in `pre.txt`.
- Combined stage: {"status": "staged", "entries": 347, "ops": {"add": 0, "update": 347, "delete": 0}, "files": ["data/knowledge/sections/access.json", "data/knowledge/sections/actions.json", "data/knowledge/sections/activities.json", "data/knowledge/sections/booking_fees.json", "data/knowledge/sections/conversation.json", "data/knowledge/sections/fauna.json", "data/knowledge/sections/flora_ecosystems.json", "data/knowledge/sections/geography.json", "data/knowledge/sections/health_safety.json", "data/knowledge/sections/history_culture.json", "data/knowledge/sections/hours_status.json", "data/knowledge/sections/preparation.json", "data/knowledge/sections/rules.json", "data/knowledge/sections/services.json", "data/knowledge/sections/weather_volcano.json", "research_notes/Conocimiento turístico de Los Nevados/coordination/knowledge_additions.json", "research_notes/Conocimiento turístico de Los Nevados/access.research.md", "research_notes/Conocimiento turístico de Los Nevados/actions.research.md", "research_notes/Conocimiento turístico de Los Nevados/activities.research.md", "research_notes/Conocimiento turístico de Los Nevados/booking_fees.research.md", "research_notes/Conocimiento turístico de Los Nevados/conversation.research.md", "research_notes/Conocimiento turístico de Los Nevados/fauna.research.md", "research_notes/Conocimiento turístico de Los Nevados/flora_ecosystems.research.md", "research_notes/Conocimiento turístico de Los Nevados/geography.research.md", "research_notes/Conocimiento turístico de Los Nevados/health_safety.research.md", "research_notes/Conocimiento turístico de Los Nevados/history_culture.research.md", "research_notes/Conocimiento turístico de Los Nevados/hours_status.research.md", "research_notes/Conocimiento turístico de Los Nevados/preparation.research.md", "research_notes/Conocimiento turístico de Los Nevados/rules.research.md", "research_notes/Conocimiento turístico de Los Nevados/services.research.md", "research_notes/Conocimiento turístico de Los Nevados/weather_volcano.research.md"], "impact": {"related_updated": [], "featured_updated": []}, "warnings": {"orphaned_hard_negatives": [], "similar_labels": []}, "stage": "/tmp/pnn-curation-v2.mNicqh/combined.stage.json", "semantic_review": "required from author"}
- Canary check (`history_culture`): {"status": "valid", "entries": 3, "ops": {"add": 0, "update": 3, "delete": 0}, "files": ["data/knowledge/sections/history_culture.json", "research_notes/Conocimiento turístico de Los Nevados/coordination/knowledge_additions.json", "research_notes/Conocimiento turístico de Los Nevados/history_culture.research.md"], "impact": {"related_updated": [], "featured_updated": []}, "warnings": {"orphaned_hard_negatives": [], "similar_labels": []}}
- Canary post-rebuild presence: 3/3 applied ops found.
- Canary validation: Errors: 0; review flags: 0
- Final rebuild: rebuilt 15 sections
- Final validation: Errors: 0; review flags: 0
- `regen_test.py full`: last line `_polish_unchanged true`; all 15 section statuses were `OK`.
- Laya validate: OK: 0 errors
- Taxonomy audit (after corpus): `error_count=0`; raw last line `}`.
- Inventory after: {"entries": 806, "loo_top1": 0.4756, "confusable_pairs_ge2": 694}

Transaction IDs: actions:b6713d5c195d44c8a291c956cd04ea7c, health_safety:8aa177bdc97a46b9b658ee06c962e221, weather_volcano:66a2c15b38004a2f822f5306a1f1ee2a, access:6ae3a802b9ae4efd97b7939ce1a1a534, booking_fees:3a60ad6191e54406bfd23ba5655ff398, hours_status:7d83be31b14a4c9cbdec95b444c88762, preparation:8815485c1a304757b09cbab3818e44ec, activities:650191e3a9dd41869be93e0c7d685c46, rules:c34ca94e621b4e2e8e56079073e6867a, services:7f7127e82694404ca44d4d9797ac50fc, fauna:fa647aa30bba48dcbfc78a9163df4f4a, flora_ecosystems:32fbabbf98ae40269c2ff2a924440049, geography:4bfa1b1280f841e3a310d029fadc3fa6, history_culture:26a17dd499d44532828056fccbc97613, conversation:eb2689f724864a82a7da09c38ea7c4f8

After-corpus SHA-256 manifest: `snapshots/sections_after.sha256.json`.
