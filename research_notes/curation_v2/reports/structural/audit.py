#!/usr/bin/env python3
"""Read-only structural audit of data/knowledge/sections (curation v2, agent 32).

Writes only to research_notes/curation_v2/reports/structural/. Never touches the corpus,
the registry, the proposals or git.
"""
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path

R = Path("/home/cruz1122/dev/hacka-airplane")
W = R / "research_notes/curation_v2"
COORD = R / "research_notes/Conocimiento turístico de Los Nevados/coordination"
SEC = R / "data/knowledge/sections"
BEFORE = W / "snapshots/sections_before"
SCHEMA_PATH = R / "docs/schemas/knowledge-section.schema.json"
OUT = W / "reports/structural"
TODAY = date(2026, 11, 22)

ORDER = [
    ("actions", 1), ("health_safety", 2), ("weather_volcano", 3), ("access", 4),
    ("booking_fees", 5), ("hours_status", 6), ("preparation", 7), ("activities", 8),
    ("rules", 9), ("services", 10), ("fauna", 11), ("flora_ecosystems", 12),
    ("geography", 13), ("history_culture", 14), ("conversation", 15),
]
SECTION_IDS = [s for s, _ in ORDER]
ALLOWED_ACTIONS = {"register_visit", "report_emergency"}
FACT_FIELDS = ["answer", "sources", "last_verified", "valid_until", "kind", "audience", "action"]

FAILS = []      # dicts: check, id, rule, detail
WARNS = []      # same shape, informational
COUNTS = defaultdict(lambda: defaultdict(int))


def fail(check, item, rule, detail=""):
    FAILS.append({"check": check, "id": item, "rule": rule, "detail": detail})


def warn(check, item, rule, detail=""):
    WARNS.append({"check": check, "id": item, "rule": rule, "detail": detail})


def canon(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=False)


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def fold(s):
    """Casefold and strip accents and punctuation: identity for label/example comparison."""
    s = unicodedata.normalize("NFKD", s.casefold())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(re.findall(r"\w+", s))


def strip_acc(s):
    s = unicodedata.normalize("NFKD", s.casefold())
    return "".join(c for c in s if not unicodedata.combining(c))


def parse_date(v):
    try:
        return date.fromisoformat(v)
    except (TypeError, ValueError):
        return None


def answer_texts(answer):
    for key, value in answer.items():
        if isinstance(value, str):
            yield key, value
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    yield key, item
                elif isinstance(item, list):
                    for text in item:
                        if isinstance(text, str):
                            yield key, text


# ---------------------------------------------------------------- load corpus
cur, ent, dup_ids = {}, {}, []
for s, order in ORDER:
    d = load(SEC / f"{s}.json")
    cur[s] = d
    for e in d["entries"]:
        if e["id"] in ent:
            dup_ids.append(e["id"])
        ent[e["id"]] = (s, e)
files_on_disk = sorted(p.name for p in SEC.glob("*.json"))
if files_on_disk != sorted(f"{s}.json" for s in SECTION_IDS):
    fail("2_schema", "sections/", "unexpected_section_files", str(files_on_disk))

before_entries = {}  # id -> (section, entry) from snapshot
before_sections = {}
for s in SECTION_IDS:
    d = load(BEFORE / f"{s}.json")
    before_sections[s] = d
    for e in d["entries"]:
        before_entries[e["id"]] = (s, e)

proposals = {}
for s in SECTION_IDS:
    p = load(W / "proposals" / f"{s}.final.json")
    ops = p["operations"] if isinstance(p, dict) and "operations" in p else p
    proposals[s] = ops
registry = load(COORD / "knowledge_additions.json")

COUNTS["entries"]["total"] = len(ent)
COUNTS["entries"]["sections"] = len(cur)
COUNTS["entries"]["examples"] = sum(len(e["examples"]) for _, e in ent.values())
if dup_ids:
    for i in dup_ids:
        fail("1_refs", i, "duplicate_entry_id")

# ================================================================ CHECK 1 refs
CHECK = "1_refs"
examples_owner = defaultdict(list)
for eid, (s, e) in ent.items():
    for x in e["examples"]:
        examples_owner[x].append(eid)

refs = []  # (source, field, target)
for eid, (s, e) in ent.items():
    for r in e.get("related", []):
        refs.append((eid, "related", r))
        COUNTS[CHECK]["related_refs"] += 1
        if r == eid:
            warn(CHECK, eid, "self_related")
for s, d in cur.items():
    for f in d.get("featured", []):
        refs.append((s, "featured", f))
        COUNTS[CHECK]["featured_refs"] += 1
    if not 1 <= len(d.get("featured", [])) <= 5:
        warn(CHECK, s, "featured_count_outside_1_5", str(len(d.get("featured", []))))

# Ops in proposals and registry: delete/replace_with targets and every op id must exist.
all_ops = []
for s in SECTION_IDS:
    for op in proposals[s]:
        all_ops.append(("proposal:" + s, op))
for rec in registry:
    all_ops.append(("registry", rec))
for src, op in all_ops:
    oid = op.get("id") or (op.get("entry") or {}).get("id")
    if op.get("op") == "delete":
        COUNTS[CHECK]["delete_ops"] += 1
        if oid in ent:
            fail(CHECK, oid, "deleted_id_still_present", src)
        if op.get("replace_with"):
            refs.append((oid, "replace_with", op["replace_with"]))
for src, source_id, field, target in [(None, a, b, c) for a, b, c in refs]:
    if field in ("related", "replace_with"):
        pass
    if target not in ent and field == "featured":
        fail(CHECK, source_id, "featured_unresolved", target)
    elif target not in ent:
        fail(CHECK, source_id, f"{field}_unresolved", target)

for src, op in all_ops:
    oid = (op.get("entry") or {}).get("id") or op.get("id")
    if src != "registry" and src.startswith("proposal:") and op.get("op") in ("update", "add"):
        COUNTS[CHECK]["op_targets"] += 1
        if oid not in ent:
            fail(CHECK, oid, "op_target_missing_in_corpus", src)

# hard_negatives are example texts, not ids: each must match an example of another entry.
hn_total = hn_resolved = 0
for eid, (s, e) in ent.items():
    for hn in e.get("hard_negatives", []):
        hn_total += 1
        owners = [o for o in examples_owner.get(hn, []) if o != eid]
        if owners:
            hn_resolved += 1
        else:
            fail(CHECK, eid, "hard_negative_not_example_of_other_entry", hn)
COUNTS[CHECK]["hard_negatives_total"] = hn_total
COUNTS[CHECK]["hard_negatives_resolved"] = hn_resolved

# Code and docs that quote entry ids (conversation routing, mobile export, Laya, tests).
SECTION_RE = "|".join(re.escape(s) for s in SECTION_IDS)
QUOTED = re.compile(r"""["'`]((?:%s)\.[a-z][a-z0-9_]*)["'`]""" % SECTION_RE)
FILE_EXT = {"json", "py", "md", "ts", "tsx", "js", "txt", "csv", "jsonl", "yaml", "yml", "log",
            "png", "jpg", "jpeg", "svg", "webp", "wav", "mp3", "mp4", "sh", "toml", "lock"}
SKIP_DIRS = {"node_modules", ".git", "research_notes", "data", "android", "ios", ".expo",
             "__pycache__", ".venv", "dist", "build", "coverage", ".cxx", ".gradle", "eval"}
SCAN_EXT = {".py", ".ts", ".tsx", ".js", ".mjs", ".json", ".md", ".yaml", ".yml", ".toml"}
code_refs = []
scanned = 0
import os
for dirpath, dirnames, filenames in os.walk(R):
    rel_dir = Path(dirpath).relative_to(R)
    if rel_dir.parts and rel_dir.parts[0] in ("data", "research_notes", "node_modules", ".git"):
        dirnames[:] = []
        continue
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")
                   and not d.startswith(".") or d in (".claude", ".agents")]
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and (not d.startswith(".") or d in (".claude", ".agents"))]
    for fn in filenames:
        p = Path(dirpath) / fn
        rel = p.relative_to(R)
        if p.suffix not in SCAN_EXT or p.stat().st_size > 2_000_000:
            continue
        if re.search(r"eval|sealed|holdout", str(rel), re.I):
            continue
        scanned += 1
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for m in QUOTED.finditer(text):
            ident = m.group(1)
            if ident.rsplit(".", 1)[1] in FILE_EXT:
                continue
            code_refs.append((str(rel), ident))
COUNTS[CHECK]["code_files_scanned"] = scanned
COUNTS[CHECK]["code_id_refs"] = len(code_refs)
for path, ident in code_refs:
    if ident not in ent:
        fail(CHECK, ident, "code_reference_unresolved", path)

# ================================================================ CHECK 2 schema
CHECK = "2_schema"
schema = load(SCHEMA_PATH)
validator = __import__("jsonschema").Draft202012Validator(
    schema, format_checker=__import__("jsonschema").FormatChecker())
for s, order in ORDER:
    d = cur[s]
    COUNTS[CHECK]["sections_checked"] += 1
    if d.get("id") != s:
        fail(CHECK, s, "section_id_mismatch", str(d.get("id")))
    if d.get("order") != order:
        fail(CHECK, s, "section_order_mismatch", f"{d.get('order')} != {order}")
    for err in validator.iter_errors(d):
        where = s
        if err.path and err.path[0] == "entries" and len(err.path) > 1:
            where = d["entries"][err.path[1]]["id"]
        fail(CHECK, where, "schema", f"{'/'.join(map(str, err.path))}: {err.message[:160]}")
    if len(d["entries"]) < 1:
        fail(CHECK, s, "no_entries")

for eid, (s, e) in ent.items():
    COUNTS[CHECK]["entries_checked"] += 1
    if not eid.startswith(s + "."):
        fail(CHECK, eid, "id_prefix_not_section")
    if len(e["examples"]) < 10:
        fail(CHECK, eid, "examples_below_contract_minimum_10", str(len(e["examples"])))
    if e["kind"] == "action":
        if e.get("action") not in ALLOWED_ACTIONS:
            fail(CHECK, eid, "action_not_in_allowed_set", str(e.get("action")))
    elif "action" in e:
        fail(CHECK, eid, "action_field_on_non_action_kind")
    lv = e.get("last_verified")
    lv_d = parse_date(lv) if lv is not None else None
    if lv is not None and lv_d is None:
        fail(CHECK, eid, "last_verified_not_real_date", str(lv))
    if lv_d and lv_d > TODAY:
        fail(CHECK, eid, "last_verified_in_future", lv)
    vu = e.get("valid_until")
    vu_d = parse_date(vu) if vu else None
    if vu and vu_d is None:
        fail(CHECK, eid, "valid_until_not_real_date", str(vu))
    if vu_d and lv_d and vu_d < lv_d:
        fail(CHECK, eid, "valid_until_before_last_verified", f"{vu} < {lv}")
    if vu_d and vu_d < TODAY:
        fail(CHECK, eid, "valid_until_expired_before_today", vu)
    for src in e.get("sources", []):
        rd = parse_date(src.get("retrieved_at"))
        if rd is None:
            fail(CHECK, eid, "retrieved_at_not_real_date", str(src.get("retrieved_at")))
        elif rd > TODAY:
            fail(CHECK, eid, "retrieved_at_in_future", src.get("retrieved_at"))
        if not src.get("url", "").startswith("https://"):
            warn(CHECK, eid, "source_url_not_https", src.get("url", ""))
    has_digit = any(re.search(r"\d", t) for _, t in answer_texts(e["answer"]))
    if has_digit and not lv:
        fail(CHECK, eid, "digits_without_last_verified")
    if has_digit and not any(src for src in e["sources"]):
        fail(CHECK, eid, "digits_without_source")
    if e.get("lang", "es") != "es":
        warn(CHECK, eid, "non_spanish_lang", e.get("lang"))

# ================================================================ CHECK 3 manual edits
CHECK = "3_no_manual_edits"
for s in SECTION_IDS:
    raw_before = (BEFORE / f"{s}.json").read_bytes()
    COUNTS[CHECK]["sections"] += 1
    b = before_sections[s]
    a = cur[s]
    for k in set(b) | set(a):
        if k == "entries":
            continue
        if canon(b.get(k)) != canon(a.get(k)):
            fail(CHECK, s, "top_level_field_changed", k)

# Hash manifests.
before_manifest = load(W / "snapshots/sections_before.sha256.json")["files"]
after_manifest = load(W / "snapshots/sections_after.sha256.json")["files"]
for s in SECTION_IDS:
    fn = f"{s}.json"
    h_before = hashlib.sha256((BEFORE / fn).read_bytes()).hexdigest()
    h_now = hashlib.sha256((SEC / fn).read_bytes()).hexdigest()
    if before_manifest.get(fn) != h_before:
        fail(CHECK, s, "sections_before_snapshot_hash_mismatch")
    if after_manifest.get(fn) != h_now:
        fail(CHECK, s, "sections_after_manifest_hash_mismatch_or_manual_edit")
    COUNTS[CHECK]["hash_files"] += 1

# Registry vs proposals (same ops, same content).
reg_by_id = defaultdict(list)
for rec in registry:
    reg_by_id[rec["entry"]["id"]].append(rec)
prop_by_id = defaultdict(list)
for s in SECTION_IDS:
    for op in proposals[s]:
        oid = op.get("id") or op["entry"]["id"]
        prop_by_id[oid].append((s, op))
COUNTS[CHECK]["registry_records"] = len(registry)
COUNTS[CHECK]["proposal_ops"] = sum(len(v) for v in proposals.values())
for oid in set(reg_by_id) | set(prop_by_id):
    rr = reg_by_id.get(oid, [])
    pp = prop_by_id.get(oid, [])
    if len(rr) != 1:
        fail(CHECK, oid, "registry_record_count", str(len(rr)))
    if len(pp) != 1:
        fail(CHECK, oid, "proposal_op_count", str(len(pp)))
    if rr and pp:
        if canon(rr[0]["entry"]) != canon(pp[0][1]["entry"]):
            fail(CHECK, oid, "registry_entry_differs_from_proposal")
        if rr[0].get("op") != pp[0][1].get("op"):
            fail(CHECK, oid, "registry_op_differs_from_proposal")

# Every entry: changed vs snapshot must be explained by an op and registry, and current
# content must equal the registry entry.
changed_ids = set()
for eid, (s, e) in ent.items():
    if eid not in before_entries:
        changed_ids.add(eid)
        fail(CHECK, eid, "entry_added_without_registry_record" if eid not in reg_by_id
             else "entry_added_outside_snapshot")
        continue
    if canon(before_entries[eid][1]) != canon(e):
        changed_ids.add(eid)
for eid in before_entries:
    if eid not in ent:
        fail(CHECK, eid, "entry_removed_from_corpus")
COUNTS[CHECK]["entries_changed_vs_snapshot"] = len(changed_ids)
for eid in changed_ids:
    s, e = ent[eid]
    if eid not in reg_by_id:
        fail(CHECK, eid, "changed_without_registry_record")
    if eid not in prop_by_id:
        fail(CHECK, eid, "changed_without_proposal_op")
    for rec in reg_by_id.get(eid, []):
        if canon(rec["entry"]) != canon(e):
            fail(CHECK, eid, "current_content_differs_from_registry_entry")
    for ps, op in prop_by_id.get(eid, []):
        if ps != s:
            fail(CHECK, eid, "op_in_wrong_section_proposal", f"proposal {ps}, entry {s}")
        if canon(op["entry"]) != canon(e):
            fail(CHECK, eid, "current_content_differs_from_proposal_entry")
for eid, pp in prop_by_id.items():
    if eid in ent and eid not in changed_ids:
        for ps, op in pp:
            fail(CHECK, eid, "op_is_noop_entry_unchanged_vs_snapshot", ps)
# Unchanged entries in one section must still match the registry (no silent drift).
for eid, (s, e) in ent.items():
    if eid not in changed_ids and eid in reg_by_id:
        for rec in reg_by_id[eid]:
            if canon(rec["entry"]) != canon(e):
                fail(CHECK, eid, "unchanged_entry_drifted_from_registry")

# Run the project validator (writes coordination/validation.json; restored afterwards).
val_json = COORD / "validation.json"
backup = val_json.read_bytes()
run = subprocess.run([sys.executable, "validate_knowledge.py"], cwd=COORD,
                     capture_output=True, text=True, timeout=600)
val_after = val_json.read_bytes()
val_json.write_bytes(backup)
restored_same = val_after == backup
VALIDATOR = {"returncode": run.returncode, "stdout_tail": run.stdout.strip().splitlines()[-2:],
             "stderr_tail": run.stderr.strip().splitlines()[-3:],
             "report_identical_to_stored": restored_same}
if run.returncode != 0 or run.stderr.strip():
    fail(CHECK, "validate_knowledge.py", "validator_nonzero_or_stderr", run.stderr[-300:])
if not restored_same:
    warn(CHECK, "validation.json", "rerun_report_differs_from_stored", "stored file was restored")
try:
    rep = json.loads(val_after)
    VALIDATOR["errors"] = len(rep["errors"])
    VALIDATOR["review_flags"] = len(rep["warnings"])
    VALIDATOR["total_entries"] = rep["total_entries"]
    for er in rep["errors"]:
        fail(CHECK, er.get("id") or er.get("section") or er.get("example", "?")[:60],
             "validator_error_" + er["rule"], json.dumps(er, ensure_ascii=False)[:200])
    for wr in rep["warnings"]:
        warn(CHECK, wr.get("id") or (wr.get("ids") or ["?"])[0], "validator_warning_" + wr["rule"],
             json.dumps(wr, ensure_ascii=False)[:200])
except (ValueError, KeyError):
    fail(CHECK, "validation.json", "validator_report_unparseable")

# ================================================================ CHECK 4 evidence
CHECK = "4_evidence"
VERIFY = W / "tools/verify_evidence.py"
ev_summary = {}
for s in SECTION_IDS:
    pf = W / "proposals" / f"{s}.final.json"
    r = subprocess.run([sys.executable, str(VERIFY), "--proposal", str(pf)], cwd=R,
                       capture_output=True, text=True, timeout=600)
    try:
        out = json.loads(r.stdout)
    except ValueError:
        fail(CHECK, s, "verify_evidence_unparseable", (r.stdout + r.stderr)[-300:])
        continue
    ev_summary[s] = {"rc": r.returncode, "ops": out["ops"], "evidence_items": out["evidence_items"],
                     "fail": len(out["fail"]), "flags": len(out["flags"]), "warn": len(out["warn"])}
    for msg in out["fail"]:
        eid = msg.split(":", 1)[0]
        fail(CHECK, eid, "verify_evidence_fail", msg[:300])
    for msg in out["flags"]:
        eid = msg.split(":", 1)[0]
        warn(CHECK, eid, "verify_evidence_flag_number_not_in_evidence", msg[:300])
    for msg in out["warn"]:
        warn(CHECK, msg.split(":", 1)[0], "verify_evidence_warn", msg[:200])
    if r.returncode != 0:
        fail(CHECK, s, "verify_evidence_nonzero_rc", str(r.returncode))

factual_ops = 0
for s in SECTION_IDS:
    for op in proposals[s]:
        eid = op.get("id") or op["entry"]["id"]
        if op.get("op", "add") == "delete":
            if not op.get("reason") or len(op["reason"]) < 10:
                fail(CHECK, eid, "delete_without_reason")
            continue
        COUNTS[CHECK]["ops"] += 1
        ent_new = op["entry"]
        ev = op.get("evidence", []) or []
        for item in ev:
            for k in ("url", "path", "quote", "checked_on"):
                if not item.get(k):
                    fail(CHECK, eid, "evidence_item_missing_" + k)
            cd = parse_date(item.get("checked_on"))
            if item.get("checked_on") and (cd is None or cd > TODAY):
                fail(CHECK, eid, "evidence_checked_on_invalid_or_future", str(item.get("checked_on")))
        if eid in before_entries:
            old = before_entries[eid][1]
            changed_fact = [f for f in FACT_FIELDS if canon(old.get(f)) != canon(ent_new.get(f))]
        else:
            changed_fact = ["new_entry"]
        if not changed_fact:
            continue
        factual_ops += 1
        COUNTS[CHECK]["factual_ops"] += 1
        if not ev:
            fail(CHECK, eid, "factual_op_without_evidence", ",".join(changed_fact))
            continue
        ev_urls = {x.get("url") for x in ev}
        for src in ent_new.get("sources", []):
            if src["url"] not in ev_urls:
                fail(CHECK, eid, "source_url_without_evidence", src["url"])
        if any(re.search(r"\d", t) for _, t in answer_texts(ent_new["answer"])):
            if not ent_new.get("last_verified"):
                fail(CHECK, eid, "digits_without_last_verified_in_op")
# Count factual ops that are not factual only because of metadata.
for s in SECTION_IDS:
    pass

# ================================================================ CHECK 5 temporal
CHECK = "5_temporal"
TERM = re.compile(r"\b(abiert[oa]s?|cerrad[oa]s?|hoy|actualmente|vigentes?|tarifas?|horarios?|alertas?)\b")
MONTHS = "enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre"
STRONG = re.compile(
    rf"\b\d{{1,2}} de (?:{MONTHS}) de (?:19|20)\d{{2}}\b"
    rf"|\b(?:{MONTHS}) de (?:19|20)\d{{2}}\b"
    r"|\b(?:19|20)\d{2}-\d{2}-\d{2}\b"
    r"|\b\d{1,2}/\d{1,2}/(?:19|20)?\d{2}\b")
YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
CURRENT = re.compile(
    r"\b(hoy|actualmente|en este momento|ahora mismo|ahora)\b"
    r"|\b(esta|estan|estan|es|son)\s+(abiert[oa]s?|cerrad[oa]s?)\b")
temporal_terms = {}
for eid, (s, e) in ent.items():
    text_all = " \n ".join(t for _, t in answer_texts(e["answer"]))
    norm_text = strip_acc(text_all)
    terms = sorted(set(TERM.findall(norm_text)))
    if not terms:
        continue
    COUNTS[CHECK]["entries_with_terms"] += 1
    temporal_terms[eid] = terms
    has_strong = bool(STRONG.search(norm_text))
    has_year = bool(YEAR.search(norm_text))
    cur_hits = sorted({m.group(0) for m in CURRENT.finditer(norm_text)})
    if not has_strong:
        fail(CHECK, eid, "terms_without_stated_date", ",".join(terms))
    if cur_hits:
        fail(CHECK, eid, "current_state_claim_phrase", ",".join(cur_hits))
    if has_strong:
        COUNTS[CHECK]["with_full_date"] += 1
    elif has_year:
        warn(CHECK, eid, "year_only_no_full_date", ",".join(terms))

# ================================================================ CHECK 6 duplicates
CHECK = "6_duplicates"


def groups(pairs):
    g = defaultdict(list)
    for key, eid in pairs:
        if key:
            g[key].append(eid)
    return {k: v for k, v in g.items() if len(set(v)) > 1}


exact_labels = groups((e["label"], eid) for eid, (s, e) in ent.items())
norm_labels = groups((fold(e["label"]), eid) for eid, (s, e) in ent.items())
exact_short = groups((e["answer"]["short"], eid) for eid, (s, e) in ent.items())
norm_short = groups((fold(e["answer"]["short"]), eid) for eid, (s, e) in ent.items())
exact_examples = groups((x, eid) for eid, (s, e) in ent.items() for x in e["examples"])
norm_examples = groups((fold(x), eid) for eid, (s, e) in ent.items() for x in e["examples"])
for kind, g, rule in [
    ("label", exact_labels, "identical_label"),
    ("label", norm_labels, "label_identical_after_normalization"),
    ("answer.short", exact_short, "identical_answer_short"),
    ("answer.short", norm_short, "answer_short_identical_after_normalization"),
    ("example", exact_examples, "identical_example_shared"),
]:
    for key, ids in g.items():
        for eid in sorted(set(ids)):
            fail(CHECK, eid, rule, f"{kind}={key[:90]!r} shared_with={sorted(set(ids) - {eid})}")
for key, ids in norm_examples.items():
    if len(set(ids)) > 1 and key not in exact_examples:
        for eid in sorted(set(ids)):
            warn(CHECK, eid, "example_identical_after_normalization",
                 f"{key[:90]!r} shared_with={sorted(set(ids) - {eid})}")
COUNTS[CHECK]["exact_label_groups"] = len(exact_labels)
COUNTS[CHECK]["normalized_label_groups"] = len(norm_labels)
COUNTS[CHECK]["exact_short_groups"] = len(exact_short)
COUNTS[CHECK]["normalized_short_groups"] = len(norm_short)
COUNTS[CHECK]["exact_example_groups"] = len(exact_examples)
COUNTS[CHECK]["normalized_example_groups"] = len(norm_examples)

# ================================================================ output
CHECKS = ["1_refs", "2_schema", "3_no_manual_edits", "4_evidence", "5_temporal", "6_duplicates"]
summary = {}
for c in CHECKS:
    f_ids = sorted({x["id"] for x in FAILS if x["check"] == c})
    summary[c] = {"failing_rows": sum(1 for x in FAILS if x["check"] == c),
                  "failing_ids": f_ids, "failing_ids_count": len(f_ids),
                  "warnings_rows": sum(1 for x in WARNS if x["check"] == c)}
result = {"generated_for": "2026-11-22", "counts": {k: dict(v) for k, v in COUNTS.items()},
          "summary": summary, "validator": VALIDATOR, "verify_evidence": ev_summary,
          "temporal_terms": temporal_terms, "fails": FAILS, "warnings": WARNS}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "structural_audit.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8")
print(json.dumps({"summary": {c: {k: v for k, v in summary[c].items() if k != "failing_ids"}
                              for c in CHECKS},
                  "counts": {k: dict(v) for k, v in COUNTS.items()},
                  "validator": VALIDATOR, "verify_evidence": ev_summary},
                 ensure_ascii=False, indent=1))
