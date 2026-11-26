"""Behavior of the add-park-knowledge tool (add, update, delete, inspect, replay)."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / ".agents/skills/add-park-knowledge/scripts/knowledge.py"
NOTES = "research_notes/Conocimiento turístico de Los Nevados"
EVIDENCE = f"{NOTES}/rules/evidence/pnn.txt"
QUOTE = "Parque Nacional Natural Los Nevados • Parques Nacionales Naturales de Colombia"
URL = "https://www.parquesnacionales.gov.co/nuestros-parques/parque-nacional-natural-los-nevados/"


def record(eid: str, word: str, related: list[str]) -> dict:
    questions = ["uno", "dos", "tres", "cuatro", "cinco", "seis"]
    questions += ["siete", "ocho", "nueve", "diez", "once", "doce"]
    return {
        "entry": {
            "id": eid, "label": f"fixture {word} de prueba", "kind": "rule",
            "audience": "visitor", "lang": "es",
            "examples": [f"zzq {word} pregunta {q}" for q in questions] + [f"zzq {word} question"],
            "hard_negatives": ["puedo llevar a mi perro", "dónde boto la basura"],
            "entities": {}, "needs": [],
            "answer": {
                "short": f"Respuesta {word} de prueba.",
                "variants": [f"Variante {word} de prueba."],
            },
            "sources": [{"label": "PNN Los Nevados", "url": URL, "retrieved_at": "2026-11-21"}],
            "related": related, "tags": ["prueba"], "last_verified": "2026-11-21",
        },
        "evidence": [{"url": URL, "path": EVIDENCE, "quote": QUOTE, "checked_on": "2026-11-21"}],
    }


@pytest.fixture
def root(tmp_path: Path) -> Path:
    for rel in ("docs/schemas", "data/knowledge/sections", f"{NOTES}/rules/evidence"):
        shutil.copytree(REPO / rel, tmp_path / rel)
    (tmp_path / f"{NOTES}/coordination").mkdir(parents=True)
    return tmp_path


def tool(root: Path, *args: str) -> tuple[int, dict]:
    done = subprocess.run([sys.executable, str(TOOL), "--root", str(root), *args],
                          capture_output=True, text=True, check=False)
    return done.returncode, json.loads(done.stdout)


def snapshot(root: Path) -> dict[str, bytes]:
    # The coordinator lock file is created on open and carries no content.
    files = (p for p in sorted(root.rglob("*")) if p.is_file() and p.suffix != ".lock")
    return {str(p.relative_to(root)): p.read_bytes() for p in files}


def stage(root: Path, proposal: object, name: str) -> tuple[int, dict, Path]:
    path = root.parent / f"{name}.json"
    path.write_text(json.dumps(proposal, ensure_ascii=False), encoding="utf-8")
    out = root.parent / f"{name}.stage.json"
    code, result = tool(root, "stage", "--proposal", str(path), "--out", str(out))
    return code, result, out


def load_sections(root: Path) -> dict[str, dict]:
    return {
        p.stem: json.loads(p.read_text(encoding="utf-8"))
        for p in sorted((root / "data/knowledge/sections").glob("*.json"))
    }


def rules_ids(root: Path) -> set[str]:
    return {e["id"] for e in load_sections(root)["rules"]["entries"]}


def load_knowledge_module():
    spec = importlib.util.spec_from_file_location("knowledge_under_test", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_invalid_batch_writes_nothing(root: Path) -> None:
    bad = record("rules.zz_beta", "beta", ["rules.pets"])
    bad["entry"]["examples"] = bad["entry"]["examples"][:5]
    before = snapshot(root)
    batch = {"entries": [record("rules.zz_alpha", "alfa", ["rules.pets"]), bad]}
    code, result, out = stage(root, batch, "bad")
    assert code == 1 and "12 examples" in result["detail"]
    assert not out.exists() and snapshot(root) == before


def test_batch_and_single_apply_then_reapply_is_noop(root: Path) -> None:
    batch = {"entries": [record("rules.zz_alpha", "alfa", ["rules.zz_beta"]),
                         record("rules.zz_beta", "beta", ["rules.pets"])]}
    code, _, out = stage(root, batch, "batch")
    assert code == 0
    assert tool(root, "apply", "--stage", str(out))[1]["status"] == "applied"
    assert tool(root, "apply", "--stage", str(out))[1]["status"] == "unchanged"
    code, _, single = stage(root, record("rules.zz_gamma", "gamma", ["rules.pets"]), "single")
    assert code == 0 and tool(root, "apply", "--stage", str(single))[0] == 0
    assert {"rules.zz_alpha", "rules.zz_beta", "rules.zz_gamma"} <= rules_ids(root)
    registry = json.loads((root / f"{NOTES}/coordination/knowledge_additions.json").read_text())
    expected = ["rules.zz_alpha", "rules.zz_beta", "rules.zz_gamma"]
    assert [r["entry"]["id"] for r in registry] == expected


def test_apply_refuses_corpus_changed_after_stage(root: Path) -> None:
    code, _, out = stage(root, record("rules.zz_alpha", "alfa", ["rules.pets"]), "one")
    assert code == 0
    fauna = root / "data/knowledge/sections/fauna.json"
    fauna.write_bytes(fauna.read_bytes() + b" ")
    before = snapshot(root)
    code, result = tool(root, "apply", "--stage", str(out))
    assert code == 1 and "changed since stage" in result["detail"]
    assert snapshot(root) == before


def test_existing_entry_cannot_be_replaced(root: Path) -> None:
    code, result, _ = stage(root, record("rules.pets", "perro", ["rules.leave_no_waste"]), "pets")
    assert code == 1 and "cannot be replaced" in result["detail"]


def test_inspect_returns_entry_and_incoming_references(root: Path) -> None:
    code, info = tool(root, "inspect", "--id", "rules.pets")
    assert code == 0 and info["status"] == "ok"
    assert info["section"] == "rules"
    assert info["entry"]["id"] == "rules.pets"
    assert info["in_featured"] is True
    assert info["referenced_by_hard_negatives"]
    code, err = tool(root, "inspect", "--id", "rules.no_existe")
    assert code == 1 and "Entry not found" in err["detail"]


def test_update_factual_requires_evidence_and_preserves_order(root: Path) -> None:
    _, info = tool(root, "inspect", "--id", "rules.pets")
    updated = copy.deepcopy(info["entry"])
    updated["answer"]["short"] = "No está permitido ingresar mascotas al parque por norma oficial."
    updated["sources"] = [{"label": "PNN Los Nevados", "url": URL, "retrieved_at": "2026-11-21"}]
    updated["last_verified"] = "2026-11-21"

    code, err, _ = stage(root, {"op": "update", "entry": updated}, "no_ev")
    assert code == 1 and "missing read-source evidence" in err["detail"]

    before_index = [e["id"] for e in load_sections(root)["rules"]["entries"]].index("rules.pets")
    proposal = {
        "op": "update",
        "reason": "Actualizar redacción con fuente PNN verificada.",
        "entry": updated,
        "evidence": [{"url": URL, "path": EVIDENCE, "quote": QUOTE, "checked_on": "2026-11-21"}],
    }
    code, staged, out = stage(root, proposal, "upd_factual")
    assert code == 0 and staged["ops"] == {"add": 0, "update": 1, "delete": 0}
    code, applied = tool(root, "apply", "--stage", str(out))
    assert code == 0 and applied["status"] == "applied"
    assert tool(root, "apply", "--stage", str(out))[1]["status"] == "unchanged"

    entries = load_sections(root)["rules"]["entries"]
    assert entries[before_index]["id"] == "rules.pets"
    assert entries[before_index]["answer"]["short"] == updated["answer"]["short"]
    log = (root / f"{NOTES}/rules.research.md").read_text(encoding="utf-8")
    assert "## Updated entry: rules.pets" in log


def test_update_metadata_only_needs_no_evidence_and_rejects_noop(root: Path) -> None:
    _, info = tool(root, "inspect", "--id", "rules.pets")
    same = copy.deepcopy(info["entry"])
    code, err, _ = stage(root, {"op": "update", "entry": same}, "noop_upd")
    assert code == 1 and "makes no changes" in err["detail"]

    missing = copy.deepcopy(info["entry"])
    missing["id"] = "rules.zz_missing"
    code, err, _ = stage(root, {"op": "update", "entry": missing}, "missing_upd")
    assert code == 1 and "missing entry" in err["detail"]

    edited = copy.deepcopy(info["entry"])
    edited["examples"].append("zzq se puede subir con perrito al nevado")
    code, _, out = stage(root, {"op": "update", "entry": edited, "reason": "Add example"}, "meta")
    assert code == 0
    assert tool(root, "apply", "--stage", str(out))[1]["status"] == "applied"
    assert tool(root, "apply", "--stage", str(out))[1]["status"] == "unchanged"
    _, after = tool(root, "inspect", "--id", "rules.pets")
    assert "zzq se puede subir con perrito al nevado" in after["entry"]["examples"]


def test_delete_cleans_references_forbids_reuse_and_reports_orphans(root: Path) -> None:
    code, err, _ = stage(root, {"op": "delete", "id": "rules.pets", "reason": "short"}, "bad_r")
    assert code == 1 and "at least 10 characters" in err["detail"]

    code, err, _ = stage(
        root,
        {"op": "delete", "id": "rules.pets", "reason": "Redirect to unknown ID test.",
         "replace_with": "rules.zz_ghost"},
        "bad_rep",
    )
    assert code == 1 and "replace_with target does not exist" in err["detail"]

    proposal = {
        "op": "delete",
        "id": "rules.pets",
        "reason": "Retirar entrada duplicada en prueba de limpieza de referencias.",
        "replace_with": "rules.leave_no_waste",
    }
    code, staged, out = stage(root, proposal, "del_pets")
    assert code == 0 and staged["ops"] == {"add": 0, "update": 0, "delete": 1}
    assert staged["warnings"]["orphaned_hard_negatives"]
    assert "rules" in staged["impact"]["featured_updated"]

    code, applied = tool(root, "apply", "--stage", str(out))
    assert code == 0 and applied["status"] == "applied"
    assert tool(root, "apply", "--stage", str(out))[1]["status"] == "unchanged"

    sections = load_sections(root)
    assert "rules.pets" not in rules_ids(root)
    assert "rules.pets" not in sections["rules"]["featured"]
    assert len(sections["rules"]["featured"]) == len(set(sections["rules"]["featured"]))
    for sec in sections.values():
        for entry in sec["entries"]:
            assert "rules.pets" not in entry.get("related", [])
            assert entry["id"] not in entry.get("related", [])
    log = (root / f"{NOTES}/rules.research.md").read_text(encoding="utf-8")
    assert "## Deleted entry: rules.pets" in log

    # Deleted IDs can never be reused per knowledge-contract.md.
    code, err, _ = stage(root, record("rules.pets", "reuso", ["rules.leave_no_waste"]), "reuse")
    assert code == 1 and "cannot be reused" in err["detail"]


def test_delete_refuses_breaking_related_count_unless_fixed(root: Path) -> None:
    setup = {"entries": [record("rules.zz_alpha", "alfa", ["rules.zz_beta"]),
                         record("rules.zz_beta", "beta", ["rules.pets"])]}
    code, _, out = stage(root, setup, "setup_rel")
    assert code == 0 and tool(root, "apply", "--stage", str(out))[0] == 0

    bad_del = {"op": "delete", "id": "rules.zz_beta", "reason": "Eliminar sin actualizar alpha."}
    code, err, _ = stage(root, bad_del, "bad_del")
    assert code == 1 and "related must have 1–3 IDs" in err["detail"]

    _, alpha_info = tool(root, "inspect", "--id", "rules.zz_alpha")
    fixed_alpha = copy.deepcopy(alpha_info["entry"])
    fixed_alpha["related"] = ["rules.pets"]
    good_batch = {
        "operations": [
            {"op": "update", "entry": fixed_alpha, "reason": "Reemplazar related eliminado."},
            {"op": "delete", "id": "rules.zz_beta", "reason": "Eliminar tema temporal de prueba."},
        ]
    }
    code, _, out = stage(root, good_batch, "good_del")
    assert code == 0 and tool(root, "apply", "--stage", str(out))[1]["status"] == "applied"
    assert "rules.zz_beta" not in rules_ids(root)


def test_mixed_atomic_batch_move_keeps_zero_orphans(root: Path) -> None:
    old = record("rules.zz_old", "viejo", ["rules.pets"])
    ref = record("rules.zz_ref", "referencia", ["rules.zz_old"])
    ref["entry"]["hard_negatives"] = [old["entry"]["examples"][0], "dónde boto la basura"]
    code, _, setup_out = stage(root, {"entries": [old, ref]}, "setup_move")
    assert code == 0 and tool(root, "apply", "--stage", str(setup_out))[0] == 0

    moved = copy.deepcopy(old)
    moved["op"] = "add"
    moved["entry"]["id"] = "rules.zz_new"
    moved["entry"]["label"] = "fixture nuevo tema movido"
    batch = {
        "operations": [
            moved,
            {"op": "delete", "id": "rules.zz_old", "replace_with": "rules.zz_new",
             "reason": "Mover entrada al nuevo identificador canónico."},
        ]
    }
    code, staged, out = stage(root, batch, "move_batch")
    assert code == 0
    assert staged["warnings"]["orphaned_hard_negatives"] == []
    assert "rules.zz_ref" in staged["impact"]["related_updated"]
    assert tool(root, "apply", "--stage", str(out))[1]["status"] == "applied"

    _, ref_after = tool(root, "inspect", "--id", "rules.zz_ref")
    assert ref_after["entry"]["related"] == ["rules.zz_new"]
    assert "rules.zz_old" not in rules_ids(root)
    assert "rules.zz_new" in rules_ids(root)


def test_replay_matches_live_on_full_and_scratch_rebuilds(root: Path) -> None:
    original = load_sections(root)

    # 1. Add a new entry, then update it.
    alpha_v1 = record("rules.zz_alpha", "alfa", ["rules.pets"])
    code, _, out = stage(root, alpha_v1, "r1")
    assert code == 0 and tool(root, "apply", "--stage", str(out))[0] == 0

    alpha_v2 = copy.deepcopy(alpha_v1)
    alpha_v2["op"] = "update"
    alpha_v2["entry"]["examples"].append("zzq alfa pregunta extra trece")
    code, _, out = stage(root, alpha_v2, "r2")
    assert code == 0 and tool(root, "apply", "--stage", str(out))[0] == 0

    # 2. Update a legacy entry and delete another legacy entry in one batch.
    _, stay_info = tool(root, "inspect", "--id", "rules.stay_on_routes")
    stay_upd = copy.deepcopy(stay_info["entry"])
    stay_upd["examples"].append("zzq puedo salirme un poquito del camino")
    mixed = {
        "operations": [
            {"op": "update", "entry": stay_upd, "reason": "Agregar ejemplo coloquial."},
            {"op": "delete", "id": "rules.research_permissions",
             "replace_with": "rules.leave_no_waste",
             "reason": "Simular eliminación de entrada con referencia cruzada en activities."},
        ]
    }
    code, staged, out = stage(root, mixed, "r3")
    assert code == 0 and "activities.environmental_education" in staged["impact"]["related_updated"]
    assert tool(root, "apply", "--stage", str(out))[0] == 0

    live = load_sections(root)
    registry = json.loads((root / f"{NOTES}/coordination/knowledge_additions.json").read_text())
    mod = load_knowledge_module()

    # Full rebuild simulation (all 15 sections reset to builder output).
    assert mod.replay(original, registry) == live

    # Single-section scratch rebuild simulation (only rules reset, others already live).
    scratch_rules = copy.deepcopy(live)
    scratch_rules["rules"] = copy.deepcopy(original["rules"])
    assert mod.replay(scratch_rules, registry) == live

    # Cross-section scratch rebuild simulation (only activities reset, rules already live).
    scratch_activities = copy.deepcopy(live)
    scratch_activities["activities"] = copy.deepcopy(original["activities"])
    assert mod.replay(scratch_activities, registry) == live


GUION = "research_notes/uton_guion_2024/guion_fixture.txt"
GUION_QUOTE = "Aguacerales está a 4.160 msnm aproximadamente, en el páramo propiamente dicho."


def guion_record(eid: str, word: str, related: list[str]) -> dict:
    rec = record(eid, word, related)
    rec["entry"]["answer"]["short"] = "Aguacerales está a unos 4.160 metros, en pleno páramo."
    rec["entry"]["sources"] = [{"label": "Guion ecoturístico UTON 2024", "document": GUION,
                                "retrieved_at": "2026-11-26"}]
    rec["entry"]["verified_by_uton"] = True
    rec["evidence"] = [{"document": GUION, "path": GUION, "quote": GUION_QUOTE,
                        "checked_on": "2026-11-26"}]
    return rec


@pytest.fixture
def guion_root(root: Path) -> Path:
    path = root / GUION
    path.parent.mkdir(parents=True)
    # pdftotext wraps lines: the quote is split across a line break in the extract.
    path.write_text("Intro.\nAguacerales está a 4.160 msnm aproximadamente,\nen el páramo "
                    "propiamente dicho.\n", encoding="utf-8")
    return root


def test_guion_document_source_backs_a_verified_numeric_answer(guion_root: Path) -> None:
    code, result, out = stage(guion_root, guion_record("rules.zz_guion", "guion", ["rules.pets"]),
                              "guion")
    assert code == 0, result
    assert tool(guion_root, "apply", "--stage", str(out))[0] == 0
    entry = next(e for e in load_sections(guion_root)["rules"]["entries"]
                 if e["id"] == "rules.zz_guion")
    assert entry["verified_by_uton"] is True
    log = (guion_root / f"{NOTES}/rules.research.md").read_text(encoding="utf-8")
    assert GUION in log


def test_verified_entry_must_cite_only_the_guion(guion_root: Path) -> None:
    rec = guion_record("rules.zz_guion", "guion", ["rules.pets"])
    rec["entry"]["sources"].append({"label": "PNN", "url": URL, "retrieved_at": "2026-11-21"})
    rec["evidence"].append({"url": URL, "path": EVIDENCE, "quote": QUOTE, "checked_on": "2026-11-21"})
    code, result, _ = stage(guion_root, rec, "mixed")
    assert code == 1 and "document" in result["detail"]


def test_document_source_outside_the_guion_folder_is_rejected(guion_root: Path) -> None:
    rec = guion_record("rules.zz_guion", "guion", ["rules.pets"])
    rec["entry"]["sources"][0]["document"] = "research_notes/otro/doc.txt"
    code, _, _ = stage(guion_root, rec, "elsewhere")
    assert code == 1


def test_flipping_verified_flag_is_a_factual_change(guion_root: Path) -> None:
    rec = guion_record("rules.zz_guion", "guion", ["rules.pets"])
    _, _, out = stage(guion_root, rec, "guion")
    assert tool(guion_root, "apply", "--stage", str(out))[0] == 0
    flipped = copy.deepcopy(rec["entry"])
    flipped["verified_by_uton"] = False
    code, err, _ = stage(guion_root, {"op": "update", "entry": flipped, "reason": "Quitar el sello."},
                         "flip")
    assert code == 1 and "missing read-source evidence" in err["detail"]
