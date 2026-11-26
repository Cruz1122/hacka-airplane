"""T3 layers: script check + verifier verdicts -> resolved/T3L_S.final.jsonl (DECISION_LOG 26).

A layer text is kept when check_layers.py passes it and the verifier says ok. A layer is kept when
at least one of its texts is. Output row: {entry_id, layers: [{kind, texts: [{text, atoms}]}]},
layers in order (1, then 2); integrate_depth.py reads these files.

usage: python3 t3l_final.py T3L_000 [T3L_001 ...]
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter

from common import DEPTH, read_jsonl


def main() -> None:
    for s in sys.argv[1:]:
        clean = DEPTH / f"resolved/{s}.clean.jsonl"
        subprocess.run([sys.executable, "check_layers.py", str(DEPTH / f"proposals/{s}.jsonl"),
                        "--write", str(clean)], check=True, cwd=DEPTH / "tools", stdout=subprocess.DEVNULL)
        ver = {r["lid"]: r.get("verdict") for r in read_jsonl(DEPTH / f"reviews/{s}.jsonl")}
        why = Counter()
        by: dict[str, dict[int, dict]] = {}
        for r in read_jsonl(clean):
            v = ver.get(r["lid"])
            why[str(v)] += 1
            if v != "ok":
                continue
            layer = by.setdefault(r["entry_id"], {}).setdefault(r["layer"], {"kind": r["kind"], "texts": []})
            layer["texts"].append({"text": r["text"], "atoms": r["atoms"]})
        rows = [{"entry_id": e, "layers": [ls[k] for k in sorted(ls)]} for e, ls in by.items()]
        (DEPTH / f"resolved/{s}.final.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        print(s, dict(why), "entries", len(rows), "layers", sum(len(r["layers"]) for r in rows))


if __name__ == "__main__":
    main()
