"""Shared loaders for the depth_v1 orchestrator scripts. Read-only over the corpus."""

from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DEPTH = ROOT / "research_notes/depth_v1"
SECTIONS = ROOT / "data/knowledge/sections"
APP = ROOT / "data/knowledge/app"
RESEARCH = ROOT / "research_notes/Conocimiento turístico de Los Nevados"

SECTION_ORDER = [
    "flora_ecosystems", "fauna", "weather_volcano", "health_safety", "rules", "geography",
    "history_culture", "activities", "access", "booking_fees", "preparation", "hours_status",
    "services", "actions", "conversation",
]

STOP = set(
    "a al algo ante como con cual cuales de del desde donde el ella ellas en entre era es esa ese eso "
    "esta este esto estos estas fue ha hay la las le les lo los mas me mi muy no nos o para pero por "
    "que se si sin sobre su sus te tu un una uno unos y ya the and of to in is for on with que puedes "
    "puede tiene tienen ser son estan esta parque nevados los".split()
)


def fold(text: str) -> str:
    t = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", fold(text))


def content_words(text: str) -> set[str]:
    return {w for w in words(text) if len(w) > 2 and w not in STOP}


@lru_cache(maxsize=1)
def entries() -> dict[str, dict]:
    out = {}
    for s in SECTION_ORDER:
        d = json.loads((SECTIONS / f"{s}.json").read_text())
        for e in d["entries"]:
            out[e["id"]] = {**e, "section": s}
    return out


@lru_cache(maxsize=None)
def app(name: str):
    return json.loads((APP / name).read_text())


def emergency_ids() -> set[str]:
    return {k for k, v in app("answer_policy.json").items() if isinstance(v, dict) and v.get("policy") == "emergency_direct"}


def exempt(e: dict) -> bool:
    """Depth/paraphrase-exempt per R3.1: conversation section and kind chat."""
    return e["section"] == "conversation" or e.get("kind") == "chat"


def entry_facts_text(e: dict) -> str:
    a = e.get("answer") or {}
    parts = [a.get("short") or ""] + list(a.get("variants") or [])
    parts += [s if isinstance(s, str) else json.dumps(s, ensure_ascii=False) for s in (a.get("steps") or [])]
    if a.get("detail"):
        parts.append(a["detail"] if isinstance(a["detail"], str) else json.dumps(a["detail"], ensure_ascii=False))
    return "\n".join(p for p in parts if p)


def write_jsonl(path: Path, rows) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with path.open("w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            n += 1
    return n


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
