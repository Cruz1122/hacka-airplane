"""Verify the history_culture evidence: quotes, entry coverage, numbers and names.

Three checks, all must pass:
1. Every «...» quote in evidence/quotes.md occurs verbatim (whitespace and NBSP normalized)
   in the raw text file named by the nearest preceding `Archivo:` line.
2. Every quote is tagged with existing entry ids through an `Entradas:` line, and every
   entry of data/knowledge/sections/history_culture.json has at least one tagged quote.
3. For every entry, each number, and each capitalized name or acronym in its answer
   (short, variants, detail, steps, reflection), occurs in the quotes tagged to that entry.
   A figure the source does not print verbatim is a failure: rewrite the answer or drop it.

Run from anywhere: python3 "<notes>/history_culture/check_quotes.py". Exit 1 on any failure.
The last line is always: quotes checked: N; failures: M
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
NOTES = HERE.parent
ROOT = NOTES.parent.parent
QUOTES = HERE / "evidence" / "quotes.md"
SECTION = ROOT / "data" / "knowledge" / "sections" / "history_culture.json"

ARCHIVO = re.compile(r"Archivo:\s*`([^`]+)`")
ENTRADAS = re.compile(r"Entradas:\s*(.+)$")
ENTRY_ID = re.compile(r"`([^`]+)`")
QUOTE = re.compile(r"«([^»]+)»")
NUMBER = re.compile(r"(?<![\w.,])\d+(?:[.,]\d+)*(?![\w])")
CAPITAL = re.compile(r"[A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñ]{2,}")
SENTENCE_START = re.compile(r"(?:^|[.!?:;]\s+|[¿¡]\s*|\(|«\s*|“\s*|\"\s*)$")

# Institution names used only to attribute a statement (the source line of the entry carries the
# deep URL and the raw file). Every other capitalized word, including place and legal names, is checked.
ATTRIBUTION = {
    "Parques", "Nacionales", "Servicio", "Geológico", "Colombiano", "SGC", "Unesco", "IUGS",
    "Congreso", "Corte", "Suprema", "Portal", "Ficha", "Hoja", "Nota", "Memoria", "Sala",
}
# Capitalized words that are generic prose (verbs, pronouns, the bare words "Parque
# Nacional Natural"). Every other capitalized word in an answer must appear in its quotes,
# including place names such as Armero and Tolima and the park name "Los Nevados".
STOP_NAMES = {
    "Parque", "Nacional", "Natural", "Según", "Para", "Pero", "Esta", "Este", "Ese", "Esa",
    "Con", "Sin", "Como", "Que", "Qué", "Cómo", "Cuál", "Puedes", "Pregunta", "Confirma",
    "Consulta", "Revisa", "Mira", "Usa",
}


def normalize(text: str) -> str:
    """NFC, NBSP and zero-width characters removed, whitespace collapsed (the SGC table has them)."""
    text = unicodedata.normalize("NFC", text).replace("\xa0", " ")
    text = text.replace("\u200b", "").replace("\u00ad", "")
    return re.sub(r"\s+", " ", text)


def fold(text: str) -> str:
    """Case- and accent-insensitive form, used only to compare names (IUGS writes 'Joaquin')."""
    decomposed = unicodedata.normalize("NFKD", text.casefold())
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def load_raw(path: Path, cache: dict) -> str | None:
    key = str(path)
    if key not in cache:
        if not path.is_file():
            cache[key] = None
        else:
            raw = path.read_bytes()
            try:
                cache[key] = normalize(raw.decode("utf-8"))
            except UnicodeDecodeError:
                cache[key] = normalize(raw.decode("cp1252", errors="replace"))
    return cache[key]


def parse_quotes():
    """Return (quotes, failures): quotes is a list of (line, file, entries, quote)."""
    quotes, failures = [], []
    current_file, current_entries = None, []
    for number, line in enumerate(QUOTES.read_text(encoding="utf-8").splitlines(), 1):
        match = ARCHIVO.search(line)
        if match:
            current_file = match.group(1)
        entradas = ENTRADAS.search(line)
        if entradas:
            current_entries = ENTRY_ID.findall(entradas.group(1))
            if not current_entries:
                failures.append((number, "entradas", "Entradas: line has no backticked ids"))
        for quote in QUOTE.findall(line):
            quotes.append((number, current_file, list(current_entries), quote))
    return quotes, failures


def answer_texts(answer: dict):
    for key in ("short", "reflection", "detail"):
        if answer.get(key):
            yield answer[key]
    for variant in answer.get("variants", []) or []:
        yield variant
    for step in answer.get("steps", []) or []:
        for part in (step if isinstance(step, list) else [step]):
            if isinstance(part, str):
                yield part


def facts_of(text: str):
    numbers = set(NUMBER.findall(text))
    names = set()
    for match in CAPITAL.finditer(text):
        word = match.group(0)
        before = text[: match.start()]
        if SENTENCE_START.search(before) or word in STOP_NAMES or word in ATTRIBUTION:
            continue
        names.add(word)
    return numbers, names


def main() -> int:
    failures = []
    cache = {}
    quotes, parse_failures = parse_quotes()
    failures.extend(parse_failures)

    section = json.loads(SECTION.read_text(encoding="utf-8"))
    entry_ids = {e["id"]: e for e in section["entries"]}

    # Check 1 and 2: verbatim quotes and entry tags.
    tagged = {eid: [] for eid in entry_ids}
    for number, file_name, entries, quote in quotes:
        if file_name is None:
            failures.append((number, "archivo", f"quote before any Archivo line: «{quote}»"))
            continue
        if not entries:
            failures.append((number, file_name, f"quote without Entradas tag: «{quote}»"))
        raw = load_raw(NOTES / file_name, cache)
        if raw is None:
            failures.append((number, file_name, "raw file does not exist"))
        elif normalize(quote) not in raw:
            failures.append((number, file_name, f"not found verbatim: «{quote}»"))
        for eid in entries:
            if eid not in entry_ids:
                failures.append((number, file_name, f"unknown entry id `{eid}` (removed or misspelled)"))
            else:
                tagged[eid].append(quote)

    # Check 3: every entry has a tagged quote; its numbers and names appear in those quotes.
    checked_facts = 0
    for eid, entry in entry_ids.items():
        own = [normalize(q) for q in tagged[eid]]
        if not own:
            failures.append((0, eid, "entry has no tagged quote"))
            continue
        blob = fold(" \n ".join(own))
        numbers, names = set(), set()
        for text in answer_texts(entry["answer"]):
            n, m = facts_of(text)
            numbers |= n
            names |= m
        for token in sorted(numbers):
            checked_facts += 1
            # "No.15" and "1.000" both count: a dot or comma only glues digits to the left.
            if not re.search(rf"(?<!\d)(?<!\d[.,]){re.escape(token)}(?![\d]|[.,]\d)", blob):
                failures.append((0, eid, f"number {token!r} in answer not in its quotes"))
        for word in sorted(names):
            checked_facts += 1
            if not re.search(rf"\b{re.escape(fold(word))}\b", blob):
                failures.append((0, eid, f"name {word!r} in answer not in its quotes"))

    for number, where, reason in failures:
        print(f"FAIL line {number} [{where}] {reason}")
    print(f"entries checked: {len(entry_ids)}; quotes: {len(quotes)}; facts: {checked_facts}")
    print(f"quotes checked: {len(quotes)}; failures: {len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
