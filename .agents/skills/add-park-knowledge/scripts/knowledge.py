"""Inspect, stage, validate and apply knowledge changes (add, update, delete)."""

import argparse
import copy
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import tempfile
import unicodedata
import uuid
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

NOTES = Path("research_notes/Conocimiento turístico de Los Nevados")
SECTIONS = Path("data/knowledge/sections")
REGISTRY = NOTES / "coordination/knowledge_additions.json"
SCHEMA = Path("docs/schemas/knowledge-section.schema.json")
OFFICIAL = ("gov.co", "humboldt.org.co", "sibcolombia.net", "cdc.gov", "medlineplus.gov",
            "who.int", "unesco.org", "ramsar.org", "iugs-geoheritage.org")
ID_RE = re.compile(r"[a-z][a-z0-9_]*\.[a-z0-9_]+")
FACTUAL_FIELDS = ("answer", "sources", "last_verified", "valid_until", "kind", "audience", "action")
OP_ORDER = {"update": 0, "add": 1, "delete": 2}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def fold(text):
    return " ".join(re.findall(r"\w+", "".join(
        c for c in unicodedata.normalize("NFKD", text.casefold())
        if not unicodedata.combining(c))))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inside(root, relative):
    path = (root / relative).resolve()
    require(path.is_relative_to(root), f"Path escapes project: {relative}")
    return path


def record_op(record):
    return record.get("op", "add")


def record_id(record):
    return record["id"] if record_op(record) == "delete" else record["entry"]["id"]


def canonical(record):
    op = record_op(record)
    out = {"op": op}
    if op == "delete":
        out["id"] = record["id"]
        out["reason"] = record["reason"]
        if record.get("replace_with"):
            out["replace_with"] = record["replace_with"]
    else:
        out["entry"] = record["entry"]
        if record.get("slot_questions"):
            out["slot_questions"] = record["slot_questions"]
        if record.get("reason"):
            out["reason"] = record["reason"]
    if record.get("evidence"):
        out["evidence"] = record["evidence"]
    return out


def op_counts(ops):
    counts = {"add": 0, "update": 0, "delete": 0}
    for rec in ops:
        counts[record_op(rec)] += 1
    return counts


def records(proposal):
    if isinstance(proposal, list):
        result = proposal
    elif isinstance(proposal, dict) and ("entry" in proposal or "op" in proposal):
        result = [proposal]
    else:
        require(isinstance(proposal, dict), "Proposal must be an object or a list")
        require(set(proposal) in ({"entries"}, {"operations"}),
                "Batch must contain only 'entries' or 'operations'")
        result = proposal["entries"] if "entries" in proposal else proposal["operations"]
    require(isinstance(result, list) and result, "Empty batch")
    ids = []
    for record in result:
        require(isinstance(record, dict), "Each proposal item must be an object")
        op = record_op(record)
        require(op in {"add", "update", "delete"}, f"Unknown op: {op}")
        if op == "delete":
            require(set(record) <= {"op", "id", "reason", "replace_with", "evidence"},
                    "Unknown delete record fields")
            eid = record.get("id", "")
            require(isinstance(eid, str) and ID_RE.fullmatch(eid), f"Invalid entry id: {eid}")
            reason = record.get("reason", "")
            require(isinstance(reason, str) and len(reason.strip()) >= 10,
                    f"{eid}: delete requires a reason of at least 10 characters")
            replace_with = record.get("replace_with")
            if replace_with is not None:
                require(isinstance(replace_with, str) and ID_RE.fullmatch(replace_with),
                        f"{eid}: invalid replace_with id: {replace_with}")
                require(replace_with != eid, f"{eid}: replace_with cannot equal deleted id")
            if "evidence" in record:
                require(isinstance(record["evidence"], list), f"{eid}: invalid evidence")
        else:
            allowed = {"op", "entry", "evidence", "slot_questions"}
            if op == "update":
                allowed.add("reason")
            require(set(record) <= allowed, f"Unknown {op} record fields")
            entry = record.get("entry")
            require(isinstance(entry, dict), f"{op}: each record needs an entry object")
            eid = entry.get("id", "")
            require(isinstance(eid, str) and ID_RE.fullmatch(eid), f"Invalid entry id: {eid}")
            slots = record.get("slot_questions", {})
            require(isinstance(slots, dict)
                    and all(isinstance(k, str) and isinstance(v, str) for k, v in slots.items()),
                    f"{eid}: invalid slots")
            if "reason" in record:
                require(isinstance(record["reason"], str) and record["reason"].strip(),
                        f"{eid}: invalid reason")
            if "evidence" in record:
                require(isinstance(record["evidence"], list), f"{eid}: invalid evidence")
        ids.append(eid)
    require(len(ids) == len(set(ids)), "Duplicate IDs in batch")
    return result


def apply_record(sections, record, impact=None):
    """Apply one add/update/delete record idempotently onto sections in place."""
    op = record_op(record)
    eid = record_id(record)
    sid = eid.split(".")[0]
    require(sid in sections, f"Unknown section: {sid}")
    section = sections[sid]
    if op in {"add", "update"}:
        entry = copy.deepcopy(record["entry"])
        idx = next((i for i, e in enumerate(section["entries"]) if e["id"] == eid), None)
        if idx is None:
            section["entries"].append(entry)
        else:
            section["entries"][idx] = entry
        slots = section["clarification"].setdefault("slot_questions", {})
        for name, question in record.get("slot_questions", {}).items():
            slots[name] = question
        return
    replace_with = record.get("replace_with")
    section["entries"] = [e for e in section["entries"] if e["id"] != eid]
    for sec_id, sec in sections.items():
        for entry in sec["entries"]:
            rel = entry.get("related", [])
            if eid not in rel:
                continue
            if replace_with:
                updated = [replace_with if r == eid else r for r in rel]
                new_rel = [r for r in dict.fromkeys(updated) if r != entry["id"]]
            else:
                new_rel = [r for r in rel if r != eid]
            if new_rel != rel:
                entry["related"] = new_rel
                if impact is not None and entry["id"] not in impact["related_updated"]:
                    impact["related_updated"].append(entry["id"])
        feat = sec.get("featured", [])
        if eid in feat:
            if replace_with and replace_with.split(".")[0] == sec_id:
                new_feat = list(dict.fromkeys(replace_with if f == eid else f for f in feat))
            else:
                new_feat = [f for f in feat if f != eid]
            if new_feat != feat:
                sec["featured"] = new_feat
                if impact is not None and sec_id not in impact["featured_updated"]:
                    impact["featured_updated"].append(sec_id)


def replay(sections, operations):
    """Pure, deterministic overlay for coordinator_fixes and full/scratch rebuilds."""
    sections = copy.deepcopy(sections)
    for record in operations:
        apply_record(sections, record)
    return sections


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def is_official(url):
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in OFFICIAL)


def check_evidence_item(root, item, eid, today, allowed_urls=None):
    require(isinstance(item, dict) and set(item) == {"url", "path", "quote", "checked_on"},
            f"{eid}: invalid evidence record")
    url = item["url"]
    require(isinstance(url, str) and re.match(r"^https?://", url), f"{eid}: invalid evidence URL")
    if allowed_urls is not None:
        require(url in allowed_urls, f"{eid}: evidence URL is not an entry source")
    checked = dt.date.fromisoformat(item["checked_on"])
    require(checked <= today, f"{eid}: future evidence date")
    path = inside(root, item["path"])
    require(path.is_file(), f"{eid}: missing evidence file {path}")
    quote = item["quote"]
    require(isinstance(quote, str) and len(quote.strip()) >= 20,
            f"{eid}: provide a meaningful verbatim quote")
    require(quote in path.read_text(encoding="utf-8"), f"{eid}: quote absent from evidence")
    return path


def evidence_files(root, operations, before_entries):
    files = set()
    today = dt.date.today()
    for record in operations:
        op = record_op(record)
        eid = record_id(record)
        evidence = record.get("evidence", [])
        if op == "delete":
            for item in evidence:
                files.add(check_evidence_item(root, item, eid, today))
            continue
        entry = record["entry"]
        urls = {s["url"] for s in entry["sources"]}
        before = before_entries.get(eid)
        factual_changed = (op == "add" or before is None
                           or any(entry.get(k) != before.get(k) for k in FACTUAL_FIELDS))
        verified = entry.get("last_verified")
        if verified is not None:
            require(dt.date.fromisoformat(verified) <= today, f"{eid}: future last_verified")
        for source in entry["sources"]:
            require(dt.date.fromisoformat(source["retrieved_at"]) <= today,
                    f"{eid}: future retrieved_at")
        has_digits = any(re.search(r"\d", s) for s in strings(entry["answer"]))
        if factual_changed:
            require(isinstance(evidence, list) and evidence, f"{eid}: missing read-source evidence")
            require(verified is not None, f"{eid}: last_verified required for factual changes")
        covered = set()
        for item in evidence:
            files.add(check_evidence_item(root, item, eid, today, allowed_urls=urls))
            covered.add(item["url"])
        if factual_changed:
            require(urls <= covered, f"{eid}: every cited source needs a local quote")
            if has_digits:
                require(any(is_official(u) for u in covered),
                        f"{eid}: numerical answer needs a quoted official source")
        elif has_digits:
            require(verified is not None, f"{eid}: numerical answer requires last_verified")
            require(any(is_official(u) for u in urls),
                    f"{eid}: numerical answer needs an official source")
    return files


def validate(root, sections, operations, before_sections):
    validator = Draft202012Validator(read(root / SCHEMA), format_checker=FormatChecker())
    owners, exact_after, labels, ids = {}, {}, {}, set()
    for sid, section in sections.items():
        validator.validate(section)
        require(section["id"] == sid, f"Wrong section ID: {sid}")
        for entry in section["entries"]:
            eid = entry["id"]
            require(eid not in ids and eid.startswith(sid + "."), f"Duplicate or wrong ID: {eid}")
            ids.add(eid)
            for example in entry["examples"]:
                key = fold(example)
                require(key not in owners, f"Duplicate normalized example: {example}")
                owners[key] = eid
                exact_after[example] = eid
            labels.setdefault(fold(entry["label"]), []).append(eid)
    for record in operations:
        if record_op(record) == "delete" and record.get("replace_with"):
            eid = record_id(record)
            target = record["replace_with"]
            require(target in ids, f"{eid}: replace_with target does not exist: {target}")
    for sid, section in sections.items():
        slots = section["clarification"].get("slot_questions", {})
        feat = section.get("featured", [])
        require(set(feat) <= ids, f"{sid}: dangling featured")
        require(3 <= len(feat) <= 5, f"{sid}: featured must have 3–5 IDs (has {len(feat)})")
        require(set(section["retrieval"].get("entity_filters", [])) <= slots.keys(),
                f"{sid}: missing filter slot questions")
        for entry in section["entries"]:
            eid = entry["id"]
            rel = entry.get("related", [])
            require(set(rel) <= ids, f"{eid}: dangling related")
            require(1 <= len(rel) <= 3,
                    f"{eid}: related must have 1–3 IDs (update {eid} or pass replace_with)")
            require(eid not in rel, f"{eid}: self reference")
            require(set(entry.get("needs", [])) <= slots.keys(), f"{eid}: missing need slots")
    touched_entries = []
    for record in operations:
        if record_op(record) == "delete":
            continue
        eid = record_id(record)
        entry = record["entry"]
        touched_entries.append((eid.split(".")[0], entry))
        require(len(labels[fold(entry["label"])]) == 1, f"{eid}: duplicate label")
        require(3 <= len(entry["label"].split()) <= 8, f"{eid}: label needs 3–8 words")
        require(len(entry["examples"]) >= 12, f"{eid}: need at least 12 examples")
        negatives = entry.get("hard_negatives", [])
        require(2 <= len(negatives) <= 4 and len(negatives) == len(set(negatives)),
                f"{eid}: need 2–4 distinct hard negatives")
        for negative in negatives:
            require(owners.get(fold(negative), eid) != eid, f"{eid}: negative lacks another owner")
        variants = entry["answer"].get("variants", [])
        require(1 <= len(variants) <= 2 and len(set(map(fold, variants))) == len(variants),
                f"{eid}: need 1–2 distinct variants")
        require(all(fold(v) != fold(entry["answer"]["short"]) for v in variants),
                f"{eid}: variant repeats short answer")
        if entry["kind"] == "action":
            require(entry.get("action") in {"register_visit", "report_emergency"},
                    f"{eid}: unknown app action")
    before_entries = {e["id"]: e for s in before_sections.values() for e in s["entries"]}
    evidence = evidence_files(root, operations, before_entries)
    exact_before = {ex: e["id"] for e in before_entries.values() for ex in e["examples"]}
    orphaned = []
    for section in sections.values():
        for entry in section["entries"]:
            eid = entry["id"]
            for negative in entry.get("hard_negatives", []):
                prev_owner = exact_before.get(negative)
                new_owner = exact_after.get(negative)
                if prev_owner and prev_owner != eid and (not new_owner or new_owner == eid):
                    orphaned.append({"entry_id": eid, "hard_negative": negative,
                                     "previous_owner": prev_owner})
    similar = []
    seen_pairs = set()
    all_labels = [(s, e["id"], fold(e["label"]))
                  for s, sec in sections.items() for e in sec["entries"]]
    for sec_a, entry_a in touched_entries:
        id_a, label_a = entry_a["id"], fold(entry_a["label"])
        for sec_b, id_b, label_b in all_labels:
            if id_a == id_b:
                continue
            pair = tuple(sorted((id_a, id_b)))
            if pair in seen_pairs:
                continue
            ratio = SequenceMatcher(None, label_a, label_b).ratio()
            if ratio >= 0.88:
                seen_pairs.add(pair)
                similar.append({"ids": list(pair), "cross_section": sec_a != sec_b,
                                "ratio": round(ratio, 3)})
    warnings = {"orphaned_hard_negatives": orphaned, "similar_labels": similar}
    return evidence, warnings


def format_log_block(record, before_entries):
    op = record_op(record)
    eid = record_id(record)
    if op == "add":
        text = f"\n\n## Additive entry: {eid}\n"
    elif op == "update":
        before = before_entries.get(eid, {})
        after = record["entry"]
        fields = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        text = f"\n\n## Updated entry: {eid}\n"
        if record.get("reason"):
            text += f"\n- Reason: {record['reason']}\n"
        if fields:
            text += f"- Changed fields: {', '.join(fields)}\n"
    else:
        text = f"\n\n## Deleted entry: {eid}\n\n- Reason: {record['reason']}\n"
        if record.get("replace_with"):
            text += f"- Replaced references with: `{record['replace_with']}`\n"
    for source in record.get("evidence", []):
        text += (f"\n- {source['url']} (checked {source['checked_on']}); "
                 f"evidence: `{source['path']}`\n\n> "
                 + source["quote"].replace("\n", "\n> ") + "\n")
    return text


def build(root, proposal):
    ops = records(proposal)
    registry = read(root / REGISTRY) if (root / REGISTRY).exists() else []
    require(isinstance(registry, list), "Invalid knowledge registry")
    latest_by_id = {record_id(r): r for r in registry}
    sections = {p.stem: read(p) for p in sorted((root / SECTIONS).glob("*.json"))}
    current_entries = {e["id"]: e for s in sections.values() for e in s["entries"]}
    pending = []
    for rec in ops:
        op = record_op(rec)
        eid = record_id(rec)
        sid = eid.split(".")[0]
        require(sid in sections, f"Unknown section: {sid}")
        slots = sections[sid]["clarification"].get("slot_questions", {})
        prev_reg = latest_by_id.get(eid)
        same_as_latest = prev_reg is not None and canonical(prev_reg) == canonical(rec)
        if op == "add":
            slots_match = all(slots.get(k) == v for k, v in rec.get("slot_questions", {}).items())
            if same_as_latest and current_entries.get(eid) == rec["entry"] and slots_match:
                continue
            if prev_reg is not None and record_op(prev_reg) == "delete":
                raise ValueError(f"Previously deleted ID cannot be reused: {eid}")
            if eid in current_entries:
                if prev_reg is not None:
                    raise ValueError(f"Registry ID conflict: {eid} (use op='update' to modify)")
                raise ValueError(
                    f"Existing entry cannot be replaced with add (use op='update'): {eid}"
                )
            for name, question in rec.get("slot_questions", {}).items():
                require(name not in slots or slots[name] == question,
                        f"Conflicting slot: {sid}.{name}")
            pending.append(rec)
        elif op == "update":
            slots_match = all(slots.get(k) == v for k, v in rec.get("slot_questions", {}).items())
            if same_as_latest and current_entries.get(eid) == rec["entry"] and slots_match:
                continue
            require(eid in current_entries, f"Cannot update missing entry: {eid}")
            require(current_entries[eid] != rec["entry"] or not slots_match,
                    f"Update makes no changes: {eid}")
            pending.append(rec)
        else:
            still_referenced = any(
                eid in e.get("related", []) for s in sections.values() for e in s["entries"]
            ) or any(eid in s.get("featured", []) for s in sections.values())
            if same_as_latest and eid not in current_entries and not still_referenced:
                continue
            require(eid in current_entries, f"Cannot delete missing entry: {eid}")
            pending.append(rec)
    ordered_pending = sorted(pending, key=lambda r: OP_ORDER[record_op(r)])
    impact = {"related_updated": [], "featured_updated": []}
    merged = copy.deepcopy(sections)
    for rec in ordered_pending:
        apply_record(merged, rec, impact=impact)
    evidence, warnings = validate(root, merged, ordered_pending, sections)
    for rec in ops:
        for item in rec.get("evidence", []):
            path = (root / item["path"]).resolve()
            if path.is_relative_to(root) and path.is_file():
                evidence.add(path)
    writes = {str(SECTIONS / (sid + ".json")): encoded(data)
              for sid, data in merged.items() if data != sections[sid]}
    combined = [*registry, *ordered_pending]
    if combined != registry:
        writes[str(REGISTRY)] = encoded(combined)
    logs = []
    for sid in sorted({record_id(r).split(".")[0] for r in ops}):
        path = root / NOTES / (sid + ".research.md")
        logs.append(path)
        sec_pending = [r for r in ordered_pending if record_id(r).split(".")[0] == sid]
        if sec_pending:
            text = path.read_text(encoding="utf-8") if path.exists() else ""
            for rec in sec_pending:
                text += format_log_block(rec, current_entries)
            writes[str(path.relative_to(root))] = text.encode()
    tracked = [*(root / SECTIONS).glob("*.json"), root / SCHEMA, root / REGISTRY, *evidence, *logs]
    hashes = {str(p.relative_to(root)): digest(p) for p in tracked}
    return ops, writes, hashes, impact, warnings


def inspect_entry(root, eid):
    require(ID_RE.fullmatch(eid), f"Invalid entry id: {eid}")
    sid = eid.split(".")[0]
    sections = {p.stem: read(p) for p in sorted((root / SECTIONS).glob("*.json"))}
    require(sid in sections, f"Unknown section: {sid}")
    section = sections[sid]
    entry = next((e for e in section["entries"] if e["id"] == eid), None)
    require(entry is not None, f"Entry not found: {eid}")
    example_set = set(entry["examples"])
    related_by = []
    hn_by = []
    for sec in sections.values():
        for other in sec["entries"]:
            if other["id"] == eid:
                continue
            if eid in other.get("related", []):
                related_by.append(other["id"])
            for hn in other.get("hard_negatives", []):
                if hn in example_set:
                    hn_by.append({"entry_id": other["id"], "hard_negative": hn})
    return {
        "status": "ok",
        "section": sid,
        "entry": entry,
        "slot_questions": section["clarification"].get("slot_questions", {}),
        "in_featured": eid in section.get("featured", []),
        "featured_count": len(section.get("featured", [])),
        "referenced_by_related": related_by,
        "referenced_by_hard_negatives": hn_by,
    }


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix=".knowledge-")
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def run(args):
    root = args.root.resolve()
    require((root / SCHEMA).is_file(), "Use --root for the Los Nevados project checkout")
    if args.command == "inspect":
        return inspect_entry(root, args.id)
    if args.command == "stage":
        proposal = read(args.proposal)
        ops, writes, hashes, impact, warnings = build(root, proposal)
        stage = {"version": 1, "root": str(root), "proposal": proposal, "base": hashes,
                 "writes": {n: hashlib.sha256(b).hexdigest() for n, b in writes.items()}}
        require(not args.out.resolve().is_relative_to(root / SECTIONS), "Stage outside sections")
        require(args.out.resolve() != args.proposal.resolve(), "Stage cannot overwrite proposal")
        require(str(args.out.resolve().relative_to(root)) not in hashes
                if args.out.resolve().is_relative_to(root) else True,
                "Stage cannot overwrite corpus, registry, schema, logs or evidence")
        atomic_write(args.out, encoded(stage))
        return {"status": "staged", "entries": len(ops), "ops": op_counts(ops),
                "files": list(writes), "impact": impact, "warnings": warnings,
                "stage": str(args.out.resolve()), "semantic_review": "required from author"}
    stage = read(args.stage)
    require(stage.get("version") == 1 and stage.get("root") == str(root),
            "Wrong stage root/version")
    lock = root / NOTES / "coordination/coordinator_fixes.lock"
    with lock.open("a") as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        ops, writes, hashes, impact, warnings = build(root, stage["proposal"])
        # Reapplying an identical registered batch is a no-op.
        if not writes:
            return {"status": "unchanged", "entries": len(ops), "ops": op_counts(ops)}
        require(hashes == stage["base"], "Corpus/evidence changed since stage; stage again")
        require({n: hashlib.sha256(b).hexdigest() for n, b in writes.items()} == stage["writes"],
                "Staged output changed; stage again")
        if args.command == "check":
            return {"status": "valid", "entries": len(ops), "ops": op_counts(ops),
                    "files": list(writes), "impact": impact, "warnings": warnings}
        tx = root / NOTES / "coordination/addition_transactions" / uuid.uuid4().hex
        tx.mkdir(parents=True)
        before = {n: (root / n).read_bytes() if (root / n).exists() else None for n in writes}
        manifest = {n: {"before": hashlib.sha256(b).hexdigest() if b is not None else None,
                        "after": hashlib.sha256(writes[n]).hexdigest()} for n, b in before.items()}
        atomic_write(tx / "manifest.json", encoded(manifest))
        atomic_write(tx / "stage.json", encoded(stage))
        for n, content in before.items():
            if content is not None:
                atomic_write(tx / "before" / n, content)
        # Cooperating builders share the lock; external writes are checked right before commit.
        require(all(digest(root / n) == h for n, h in hashes.items()),
                "Concurrent write; stage again")
        completed = []
        try:
            for n, content in writes.items():
                atomic_write(root / n, content)
                completed.append(n)
        except Exception:
            for n in reversed(completed):
                if before[n] is None:
                    (root / n).unlink()
                else:
                    atomic_write(root / n, before[n])
            raise
        atomic_write(tx / "COMPLETED", b"applied\n")
        return {"status": "applied", "entries": len(ops), "ops": op_counts(ops),
                "files": list(writes), "impact": impact, "warnings": warnings,
                "backup": str(tx), "release_zip": "unchanged; package only when requested"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    subs = parser.add_subparsers(dest="command", required=True)
    insp = subs.add_parser("inspect", help="Inspect an entry and all incoming references")
    insp.add_argument("--id", required=True)
    stage = subs.add_parser("stage", help="Validate a proposal and save its immutable base hashes")
    stage.add_argument("--proposal", type=Path, required=True)
    stage.add_argument("--out", type=Path, required=True)
    for command in ("check", "apply"):
        sub = subs.add_parser(command)
        sub.add_argument("--stage", type=Path, required=True)
    try:
        print(json.dumps(run(parser.parse_args()), ensure_ascii=False))
    except (ValueError, OSError, KeyError, TypeError, ValidationError) as exc:
        print(json.dumps({"status": "error", "detail": str(exc)}, ensure_ascii=False))
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
