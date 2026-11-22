"""Phase 2 evaluation-set helpers (independent paraphrases written by non-Claude models).

  python3 eval_tools.py dump <section>     print id, label and answer.short per entry (no examples:
                                          writers must not see them)
  python3 eval_tools.py remap             rewrite expected ids of merged entries (dedup_decisions.json)
  python3 eval_tools.py check             validate data/knowledge/phase2/eval/*.jsonl: JSON per line,
                                          known ids, no query equal (case/accent-insensitive) to any
                                          example, no duplicate queries across files
"""

import json
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SECTIONS = ROOT / "data/knowledge/sections"
EVAL = ROOT / "data/knowledge/phase2/eval"


def fold(text):
    text = unicodedata.normalize("NFKD", text.strip().lower())
    return " ".join("".join(c for c in text if not unicodedata.combining(c) and (c.isalnum() or c.isspace())).split())


def entries():
    return [e for f in sorted(SECTIONS.glob("*.json")) for e in json.loads(f.read_text(encoding="utf-8"))["entries"]]


def dump(section):
    for e in entries():
        if e["id"].startswith(section + "."):
            print(json.dumps({"id": e["id"], "label": e["label"], "answer": e["answer"]["short"]}, ensure_ascii=False))


def check():
    all_entries = entries()
    ids = {e["id"] for e in all_entries}
    examples = {fold(x): e["id"] for e in all_entries for x in e["examples"]}
    seen, problems, counts = {}, [], {}
    for path in sorted(EVAL.glob("*.jsonl")):
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                problems.append(f"{path.name}:{n} bad JSON ({exc})")
                continue
            q, expected = row.get("q", ""), row.get("expected")
            if not q or not isinstance(expected, list):
                problems.append(f"{path.name}:{n} needs q and expected list")
                continue
            for i in expected:
                if i not in ids:
                    problems.append(f"{path.name}:{n} unknown id {i}")
            key = fold(q)
            if key in examples:
                problems.append(f"{path.name}:{n} equals an example of {examples[key]}: {q}")
            if key in seen:
                problems.append(f"{path.name}:{n} duplicates {seen[key]}")
            seen[key] = f"{path.name}:{n}"
            counts[path.name] = counts.get(path.name, 0) + 1
    for p in problems[:50]:
        print(p)
    print(f"rows {counts}; problems: {len(problems)}")
    return not problems


def remap():
    decisions = Path(__file__).with_name("dedup_decisions.json")
    merges = {drop: keep for keep, drop in json.loads(decisions.read_text(encoding="utf-8")).get("merges", [])}
    for path in sorted(EVAL.glob("*.jsonl")):
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        changed = 0
        for row in rows:
            new = list(dict.fromkeys(merges.get(i, i) for i in row["expected"]))
            changed += new != row["expected"]
            row["expected"] = new
        if changed:
            path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
            print(f"{path.name}: {changed} rows remapped")


if __name__ == "__main__":
    if sys.argv[1] == "dump":
        dump(sys.argv[2])
    elif sys.argv[1] == "remap":
        remap()
    else:
        sys.exit(0 if check() else 1)
