"""Assemble and validate fauna section."""
import json
import re
from pathlib import Path
import jsonschema

from entries_part1 import ENTRIES_PART1
from entries_part2 import ENTRIES_PART2
from entries_part3 import ENTRIES_PART3

ROOT = Path("/home/cruz1122/dev/hacka-airplane")
SCHEMA_PATH = ROOT / "research_notes/Conocimiento turístico de Los Nevados/inputs/knowledge-section.schema.json"
TARGET_FILE = ROOT / "data/knowledge/sections/fauna.json"

all_entries = ENTRIES_PART1 + ENTRIES_PART2 + ENTRIES_PART3

section_data = {
    "contract_version": 1,
    "id": "fauna",
    "order": 11,
    "title": "Fauna y vida silvestre",
    "description": "Animales por grupo, especies emblemáticas, hábitats, recomendaciones de avistamiento y pautas de convivencia.",
    "retrieval": {
        "profile": "explain",
        "bm25_weight": 0.3,
        "top_k": 2,
        "min_score": None,
        "entity_filters": ["animal_group", "sector"]
    },
    "clarification": {
        "between_entries": "¿Te refieres a {label_a} o a {label_b}?",
        "bank": [
            "¿Sobre qué grupo de animales quisieras saber: aves, mamíferos, anfibios, reptiles o insectos?",
            "¿Te interesa una especie en particular, como el cóndor andino, el oso de anteojos o la danta de montaña?",
            "¿Buscas recomendaciones para avistar fauna o saber qué hacer en caso de un encuentro?",
            "¿Deseas saber en qué sector o altitud del parque es más probable observar animales silvestres?",
            "¿Te interesa conocer las normas de protección de la fauna y por qué está prohibido alimentarla?"
        ],
        "slot_questions": {
            "animal_group": "¿Qué grupo de fauna buscas: aves, mamíferos, anfibios, reptiles o insectos?",
            "sector": "¿En qué sector del parque planeas tu recorrido: Brisas, Laguna del Otún, La Pastora o Santa Isabel?"
        },
        "fallback": "No tengo información sobre esa especie puntual, pero puedo orientarte sobre aves de páramo como el cóndor o el chivito, mamíferos como la danta y el oso, o pautas de avistamiento responsable."
    },
    "featured": [
        "fauna.andean_condor",
        "fauna.spectacled_bear",
        "fauna.mountain_tapir",
        "fauna.buffy_helmetcrest",
        "fauna.birds_overview"
    ],
    "entries": all_entries
}

# 1. Schema validation
schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
validator = jsonschema.Draft202012Validator(schema)
errors = list(validator.iter_errors(section_data))
if errors:
    print(f"SCHEMA VALIDATION FAILED with {len(errors)} errors:")
    for err in errors[:10]:
        print(f"  Path: {list(err.path)} - Message: {err.message}")
    raise SystemExit(1)
print("Schema validation: PASSED (Draft 2020-12)")

# 2. Detailed Contract Verification
problems = []
entry_ids = {e["id"] for e in all_entries}
labels = set()
all_examples = {}

if len(all_entries) != 90:
    problems.append(f"Expected 90 entries, got {len(all_entries)}")

for idx, e in enumerate(all_entries):
    eid = e["id"]
    if not eid.startswith("fauna."):
        problems.append(f"{eid}: ID must start with 'fauna.'")
    
    # Label word count (3-8 words)
    words = e["label"].strip().split()
    if not (3 <= len(words) <= 8):
        problems.append(f"{eid}: label '{e['label']}' has {len(words)} words (must be 3-8)")
    
    # Label uniqueness
    if e["label"] in labels:
        problems.append(f"{eid}: duplicate label '{e['label']}'")
    labels.add(e["label"])
    
    # Examples count (>= 12)
    if len(e["examples"]) < 12:
        problems.append(f"{eid}: has {len(e['examples'])} examples (< 12)")
    
    # Hard negatives count (2-4)
    negs = e.get("hard_negatives", [])
    if not (2 <= len(negs) <= 4):
        problems.append(f"{eid}: has {len(negs)} hard negatives (must be 2-4)")
    
    # Example uniqueness across the entire file
    for ex in e["examples"]:
        clean_ex = ex.strip().lower()
        if clean_ex in all_examples:
            problems.append(f"Duplicate example between {all_examples[clean_ex]} and {eid}: '{ex}'")
        all_examples[clean_ex] = eid
        
    # Related resolution
    for rel in e.get("related", []):
        if rel not in entry_ids:
            problems.append(f"{eid}: unresolved related id '{rel}'")
            
    # Needs slots resolution
    for need in e.get("needs", []):
        if need not in section_data["clarification"].get("slot_questions", {}):
            problems.append(f"{eid}: missing slot question for need '{need}'")
            
    # Check digits in answers have last_verified
    full_text = e["answer"]["short"] + " " + " ".join(e["answer"].get("variants", []))
    if re.search(r"\d", full_text):
        if not e.get("last_verified"):
            problems.append(f"{eid}: answer contains digits but lacks last_verified")

# Check featured IDs resolve
for feat in section_data.get("featured", []):
    if feat not in entry_ids:
        problems.append(f"Featured id unresolved: '{feat}'")

# Check entity filters have slot questions
for filt in section_data["retrieval"].get("entity_filters", []):
    if filt not in section_data["clarification"].get("slot_questions", {}):
        problems.append(f"Missing slot question for entity filter '{filt}'")

if problems:
    print(f"CONTRACT VERIFICATION FAILED with {len(problems)} issues:")
    for p in problems[:20]:
        print(f"  - {p}")
    raise SystemExit(1)

print(f"Contract verification: PASSED")
print(f"  Total entries: {len(all_entries)}")
print(f"  Total examples: {sum(len(e['examples']) for e in all_entries)}")
print(f"  Total hard negatives: {sum(len(e.get('hard_negatives', [])) for e in all_entries)}")

# Write output file
TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)
TARGET_FILE.write_text(json.dumps(section_data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Successfully generated and wrote {TARGET_FILE} ({TARGET_FILE.stat().st_size} bytes)")
