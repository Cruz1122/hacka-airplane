import json
from itertools import product
from pathlib import Path

import pytest

from nevados_bench.export_mobile import export
from nevados_bench.schemas import ToolCall
from nevados_bench.world import load_world
from nevados_bench.world.corpus import stable_hash
from nevados_bench.world.model import _letter_code


@pytest.fixture(scope="module")
def out(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("mobile")
    export(root, n_random=3, n_single=3, n_suite=4, grounded_sample=10)
    return root


def _load(root: Path, rel: str):
    return json.loads((root / rel).read_text(encoding="utf-8"))


def test_files_parse_and_have_content(out: Path) -> None:
    world = _load(out, "assets/data/world.json")
    prompts = _load(out, "src/core/__fixtures__/prompts.json")
    replays = _load(out, "src/core/__fixtures__/replays.json")
    assert len(world["tools"]) > 24 and len(world["stations"]) == 4
    assert world["passages"] and world["filler"] and world["slot_schemas"]
    assert prompts and {"case", "request"} == set(prompts[0])
    assert {r["source"] for r in replays} == {"suite", "random", "single"}
    assert all(r["steps"] and r["oracle_outputs"] for r in replays)
    llm = [s for r in replays for s in r["steps"] if s["kind"] == "llm"]
    assert llm and all(s["request"] and s["completion_content"] for s in llm)


def _interpret(w: dict, call: ToolCall) -> dict:
    """Reference reading of world.json's exec table; the TS port implements the same."""
    ex = w["exec"]
    rule = ex["rules"][call.name]
    a = call.arguments
    st = a.get("station")
    index = w["passage_index"]
    passages = {p["id"]: p for p in w["passages"]}

    def st_ids(field: str) -> list[str]:
        return index.get(f"{st or ''}|{field}", [])

    key = f"{call.name}|{sorted(a.items())}"
    pids: list[str] = []
    if "procedure_by_emergency_type" in rule:
        for ref in ex["procedures"][a["emergency_type"]]:
            pids += st_ids(ref["st"]) if "st" in ref else [ex["park_passages"][ref["park"]]]
    elif "item_rule" in rule:
        pids = [ex["item_rules"][a["item"]]["passage_id"]]
    elif "trail_passage" in rule:
        trail = next(t for t in w["trails"] if t["id"] == a["trail_id"])
        pids = [
            pid
            for pid in index[f"{trail['station']}|trail"]
            if trail["name"] in passages[pid]["text"]
        ][:1]
    elif "fee_by_visitor_type" in rule:
        pids = st_ids(ex["fee_field"][a["visitor_type"]])
    else:
        pids = [p for f in rule.get("st", []) for p in st_ids(f)]
        pids += [ex["park_passages"][k] for k in rule.get("park", [])]
    data: dict = {}
    spec = rule.get("data")
    if spec:
        kind = spec["kind"]
        if kind == "hash_mod4_nonzero":
            value = stable_hash(key) % 4 != 0
        elif kind == "hash_choice":
            choices = ex[spec["choices"]]
            value = choices[stable_hash(key) % len(choices)]
        elif kind == "station_trail_ids":
            value = next(s for s in w["stations"] if s["id"] == st)["trails"]
        elif kind == "item_allowed":
            value = ex["item_rules"][a["item"]]["allowed"]
        elif kind == "altitude_limit":
            value = a["target_altitude_m"] <= int(passages[spec["passage_id"]]["values"][0])
        else:
            assert kind == "letter_code"
            value = _letter_code(spec["prefix"], key)
        data[spec["key"]] = value
    return {"ok": True, "tool": call.name, "passage_ids": pids, "data": data}


def test_exec_rules_match_python_execute_tool(out: Path) -> None:
    w = _load(out, "assets/data/world.json")
    world = load_world()
    sample = {"date": "2026-12-03", "group_size": 4, "people_count": 2, "target_altitude_m": 4500,
              "report_code": "X"}  # fmt: skip
    checked = 0
    for name in world.base_tools:
        props = world.tools[name].parameters["properties"]
        axes = [
            [(p, v) for v in schema["enum"]] if "enum" in schema else [(p, sample[p])]
            for p, schema in props.items()
        ]
        for combo in product(*axes):
            call = ToolCall(name=name, arguments=dict(combo))
            assert _interpret(w, call) == world.execute_tool(call), call
            checked += 1
    assert checked > 100
    for vec in w["exec"]["hash_vectors"]:
        assert str(stable_hash(vec["text"])) == vec["value"]
