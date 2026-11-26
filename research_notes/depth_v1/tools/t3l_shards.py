"""T3 layer shards (DECISION_LOG 26): "sigue" layers written only from an entry's own complement
facts (fact_inventory, already verified with support), so no new fact enters the app.

Eligible: non-exempt entries with >= 2 complements. Entries with 2-3 complements get one layer,
>= 4 get two (L1 why|how, L2 specifics). Shards of PER entries, section order of Part C T3a.

usage: python3 t3l_shards.py [--pilot]   -> shards/T3L_NNN.json (prints names)
"""

from __future__ import annotations

import json
import sys

from common import DEPTH, app, entries, exempt

PER = 20
ORDER = ["flora_ecosystems", "fauna", "weather_volcano", "health_safety", "rules", "geography",
         "history_culture", "activities", "access", "booking_fees", "preparation", "hours_status",
         "services", "actions"]


def main() -> None:
    E, inv, nat = entries(), app("fact_inventory.json"), app("natural_replies.json")
    rows = []
    for eid in sorted(E, key=lambda i: (ORDER.index(E[i]["section"]) if E[i]["section"] in ORDER else 99, i)):
        e = E[eid]
        comp = [f for f in inv.get(eid, []) if f["class"] == "complement"]
        if exempt(e) or len(comp) < 2:
            continue
        rows.append({
            "entry_id": eid, "label": e["label"], "kind": e.get("kind"), "section": e["section"],
            "canonical_L0": nat.get(eid, ""),
            "key_facts": [f["text"] for f in inv[eid] if f["class"] == "key"],
            "complements": [{"fid": f["fid"], "text": f["text"]} for f in comp],
            "layers_wanted": 1 if len(comp) < 4 else 2,
        })
    if "--pilot" in sys.argv:
        rows = rows[:10]
    names = []
    for k in range(0, len(rows), PER):
        name = "T3L_P00" if "--pilot" in sys.argv else f"T3L_{k // PER:03d}"
        (DEPTH / f"shards/{name}.json").write_text(json.dumps(
            {"shard": name, "entries": rows[k:k + PER]}, ensure_ascii=False, indent=1))
        names.append(name)
    print(len(rows), "entries", names)


if __name__ == "__main__":
    main()
