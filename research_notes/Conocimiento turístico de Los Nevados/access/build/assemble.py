"""Build the corrected access section. Does not load the round-1 part files."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import jsonschema

from corrected_n1 import N1
from corrected_n2 import N2
from corrected_n3 import N3
from corrected_n4 import N4
from corrected_n5 import N5

ROOT = Path("/home/cruz1122/dev/hacka-airplane")
NOTES = ROOT / "research_notes/Conocimiento turístico de Los Nevados"
SCHEMA_PATH = NOTES / "inputs/knowledge-section.schema.json"
OUT = ROOT / "data/knowledge/sections/access.json"
HEADER_KEYS = (
    "contract_version",
    "id",
    "order",
    "title",
    "description",
    "retrieval",
    "clarification",
    "featured",
)


def sentences(text: str) -> list[str]:
    protected = text.replace("a. m.", "⟦am⟧").replace("p. m.", "⟦pm⟧")
    protected = protected.replace("12:00 m.", "⟦med⟧")
    protected = re.sub(r"(\d)\.(\d)", r"\1⟦dot⟧\2", protected)
    parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", protected) if part.strip()]

    def restore(part: str) -> str:
        return (
            part.replace("⟦am⟧", "a. m.")
            .replace("⟦pm⟧", "p. m.")
            .replace("⟦med⟧", "12:00 m.")
            .replace("⟦dot⟧", ".")
        )

    return [restore(part) for part in parts]


def fold_to_three(text: str) -> str:
    parts = sentences(text)
    while len(parts) > 3:
        head = parts[-2].rstrip()
        if head.endswith("."):
            head = head[:-1]
        tail = parts[-1]
        if tail and tail[0].isupper():
            tail = tail[0].lower() + tail[1:]
        parts[-2] = head + "; " + tail
        del parts[-1]
    return " ".join(parts)


def normalized(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(re.findall(r"\w+", text))


def answer_texts(answer: dict) -> list[str]:
    found: list[str] = []
    for value in answer.values():
        if isinstance(value, str):
            found.append(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    found.append(item)
                elif isinstance(item, list):
                    found.extend(text for text in item if isinstance(text, str))
    return found


def build() -> dict:
    previous = json.loads(OUT.read_text())
    section = {key: previous[key] for key in HEADER_KEYS}
    entries = N1 + N2 + N3 + N4 + N5
    for entry in entries:
        answer = entry["answer"]
        answer["short"] = fold_to_three(answer["short"])
        answer["variants"] = [fold_to_three(variant) for variant in answer.get("variants", [])]
    section["entries"] = entries
    return section


def local_errors(section: dict) -> list[str]:
    errors: list[str] = []
    entries = section["entries"]
    ids = [entry["id"] for entry in entries]
    if len(ids) != len(set(ids)):
        errors.append("duplicate entry id")
    example_owner: dict[str, str] = {}
    normalized_owner: dict[str, str] = {}
    for entry in entries:
        entry_id = entry["id"]
        label_words = len(entry["label"].split())
        if not 3 <= label_words <= 8:
            errors.append(f"{entry_id} label words {label_words}")
        if len(entry["examples"]) < 12:
            errors.append(f"{entry_id} examples {len(entry['examples'])}")
        if len(set(entry["examples"])) != len(entry["examples"]):
            errors.append(f"{entry_id} repeated example")
        if not 2 <= len(entry["hard_negatives"]) <= 4:
            errors.append(f"{entry_id} hard negatives")
        if not 1 <= len(entry["answer"].get("variants", [])) <= 2:
            errors.append(f"{entry_id} variants")
        if not 1 <= len(entry.get("related", [])) <= 3:
            errors.append(f"{entry_id} related")
        for need in entry.get("needs", []):
            if need not in section["clarification"]["slot_questions"]:
                errors.append(f"{entry_id} need {need}")
        short_count = len(sentences(entry["answer"]["short"]))
        if short_count > 3:
            errors.append(f"{entry_id} short sentences {short_count}")
        for index, variant in enumerate(entry["answer"].get("variants", [])):
            count = len(sentences(variant))
            if count > 3:
                errors.append(f"{entry_id} variant {index} sentences {count}")
        blob = "\n".join(answer_texts(entry["answer"]))
        if re.search(r"desde este entorno|no pude consultar|norma que revis[eé]|HTTP [45]\d\d|no los copio|esta guía", blob, re.I):
            errors.append(f"{entry_id} environment leak")
        if re.search(r"\d", blob) and not entry.get("last_verified"):
            errors.append(f"{entry_id} number without last_verified")
        if "noviembre" in entry["answer"]["short"].casefold() or "1815" in entry["answer"]["short"]:
            for variant in entry["answer"]["variants"]:
                folded = variant.casefold()
                for token in ("noviembre", "1815", "5:00", "4:00"):
                    if token not in folded:
                        errors.append(f"{entry_id} variant missing {token}")
        if entry_id == "access.control_coordinates":
            for text in [entry["answer"]["short"], *entry["answer"]["variants"]]:
                if "2023" not in text:
                    errors.append(f"{entry_id} missing 2023 caveat")
        for example in entry["examples"]:
            if example in example_owner:
                errors.append(f"duplicate example {example!r} in {example_owner[example]} and {entry_id}")
            example_owner[example] = entry_id
            key = normalized(example)
            if key in normalized_owner and normalized_owner[key] != entry_id:
                errors.append(f"normalized collision {example!r} with {normalized_owner[key]}")
            normalized_owner[key] = entry_id
            if re.search(r"\bficha\b|no invent|esta guía|este entorno", example, re.I):
                errors.append(f"{entry_id} commentary example {example!r}")
        for related in entry["related"]:
            if related not in ids:
                errors.append(f"{entry_id} related missing {related}")
    for featured in section["featured"]:
        if featured not in ids:
            errors.append(f"featured missing {featured}")
    bank = section["clarification"]["bank"]
    if not 4 <= len(bank) <= 8:
        errors.append("clarification bank size")
    return errors


def external_collisions(section: dict) -> list[str]:
    own = {example for entry in section["entries"] for example in entry["examples"]}
    hits: list[str] = []
    for path in (ROOT / "data/knowledge/sections").glob("*.json"):
        if path.name == "access.json":
            continue
        if not path.exists():
            continue
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        for entry in data.get("entries", []):
            for example in entry.get("examples", []):
                if example in own:
                    hits.append(f"{example!r} also in {path.name}:{entry.get('id')}")
    return hits


def main() -> int:
    section = build()
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = jsonschema.Draft202012Validator(schema)
    schema_errors = [
        f"schema {list(error.path)}: {error.message}" for error in validator.iter_errors(section)
    ]
    problems = schema_errors + local_errors(section)
    collisions = external_collisions(section)
    print(f"entries {len(section['entries'])}")
    print(f"examples {sum(len(entry['examples']) for entry in section['entries'])}")
    if problems:
        print(f"PROBLEMS {len(problems)}")
        for problem in problems:
            print(problem)
        return 1
    OUT.write_text(json.dumps(section, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {OUT}")
    if collisions:
        print(f"EXTERNAL COLLISIONS {len(collisions)}")
        for collision in collisions:
            print(collision)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit("Superseded 2026-11-21: access now builds from access/source/access.v1.json via coordination/build_from_snapshot.py access; rerunning this script would revert reviewed corrections.")
    sys.exit(main())
