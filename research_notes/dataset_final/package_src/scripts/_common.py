"""Shared helpers for the package validators (standard library only)."""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]
NONE = "ninguna de estas opciones"
SPLITS = {
    "train": "train/train.jsonl",
    "checkpoint_selection": "validation/checkpoint_selection.jsonl",
    "calibration": "validation/calibration.jsonl",
    "unseen_topics": "validation/unseen_topics.jsonl",
    "adversarial": "evaluation/adversarial.jsonl",
    "final_test": "evaluation/final_test_SEALED.jsonl",
    "retrospective_READ_ONLY": "evaluation/retrospective_test_blind_READ_ONLY.jsonl",
}
TRAINABLE = {"train", "checkpoint_selection"}


def jl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]


def norm(text: str) -> str:
    t = unicodedata.normalize("NFD", text.casefold()).encode("ascii", "ignore").decode()
    return " ".join(re.sub(r"[^\w\s]", " ", t).split())


class Report:
    def __init__(self, name: str):
        self.name, self.fails, self.notes = name, [], []

    def check(self, ok: bool, msg: str) -> None:
        if not ok:
            self.fails.append(msg)

    def done(self) -> None:
        for n in self.notes:
            print(f"  {n}")
        if self.fails:
            for f in self.fails[:40]:
                print(f"  FAIL {f}")
            if len(self.fails) > 40:
                print(f"  ... {len(self.fails) - 40} more")
            print(f"{self.name}: FAIL ({len(self.fails)})")
            sys.exit(1)
        print(f"{self.name}: PASS")
