"""Coordinator cross-section fixes, applied after every section generator.

Idempotent: rerun it whenever a section generator rewrites its JSON.
Fixes found in the 2026-11-21 global uniqueness review:
- fauna entries of kind "rule" duplicated topics owned by `rules` (lower order wins);
- intra-entry near-copies (accent-only variants) in `conversation`;
- artificial examples in `geography.laguna_encanto`.
"""

import fcntl
import importlib.util
from collections import Counter
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SECTIONS = ROOT / "data/knowledge/sections"

RES207 = {
    "label": "Parques Nacionales Naturales de Colombia - Resolución 207 de 2023 (Reglamentación)",
    "url": "https://www.parquesnacionales.gov.co/wp-content/uploads/2023/08/Resolucion_207_2023_ReglamentacionNevados.pdf",
    "retrieved_at": "2026-11-21",
}

# fauna id -> rules id that already covers (or now covers) the topic.
FAUNA_TO_RULES = {
    "fauna.feeding_wildlife_prohibition": "rules.feed_wildlife",
    "fauna.pets_prohibition_reason": "rules.pets",
    "fauna.noise_drone_disturbance": "rules.noise",
    "fauna.birding_playback_rules": "rules.playback",
    "fauna.poaching_hunting_prohibition": "rules.no_hunting",
}

NO_HUNTING = {
    "id": "rules.no_hunting",
    "label": "caza y captura de animales",
    "kind": "rule",
    "audience": "visitor",
    "lang": "es",
    "examples": [
        "se puede cazar en Los Nevados?",
        "puedo atrapar un animal para verlo de cerca",
        "dejan cazar conejos en el páramo",
        "me puedo llevar una pluma de cóndor que encontré",
        "está bien coger una mariposa del sendero",
        "puedo llevarme un escarabajo en un frasco",
        "toca dejar los nidos quietos?",
        "pongo una trampa para ver qué animales hay",
        "qué pasa si alguien caza en el parque",
        "se puede cojer una rana de la laguna",
        "is hunting allowed in the park?",
        "can I catch a lizard to take a photo?",
    ],
    "hard_negatives": [
        "se puede pescar en la Laguna del Otún",
        "me puedo llevar una piedra de recuerdo",
    ],
    "needs": [],
    "answer": {
        "short": "No puedes cazar, atrapar ni llevarte animales, plumas o nidos del parque; la Resolución 207 de 2023 prohíbe extraer fauna. Obsérvalos de lejos y, si ves a alguien cazando, avísale al personal del parque.",
        "variants": [
            "En Los Nevados está prohibido capturar o sacar cualquier animal, vivo o muerto. Míralos sin tocarlos y deja todo donde lo encontraste."
        ],
    },
    "sources": [RES207],
    "last_verified": "2026-11-21",
    "related": ["rules.fishing", "rules.leave_natural_objects", "fauna.injured_wildlife_protocol"],
    "tags": ["caza", "fauna", "prohibicion"],
}

CONVERSATION_REPLACE = {
    "conversation.capabilities_overview": ("que puedes hacer", "q cosas sabes hacer"),
    "conversation.ai_identity": ("quien eres tu", "kien me esta contestando"),
    "conversation.repeat_or_unclear": ("no entendi", "no te cogi la idea"),
    "conversation.compliment_reply": ("eres muy util", "q bacano este asistente"),
    "conversation.more_detail_followup": ("dame mas detalles", "explicame mas a fondo porfa"),
    "conversation.info_source_trust": ("de donde sacas la info", "de onde sale esa informacion"),
    "conversation.history_storage": ("que pasa con lo que escribo", "alguien lee lo q te escribo"),
    "conversation.time_or_date_request": ("que dia es hoy", "a como estamos hoy"),
}

ENCANTO_REPLACE = {
    "en hoyo frio nace el totare": "de qué laguna sale el río Totare",
    "Anzoátegui y la laguna del nevado": "qué laguna hay cerca de Anzoátegui",
    "4.000 metros según la Gobernación": "esa laguna queda muy alto?",
    "vereda Hoyo Frío y el Tolima": "en qué vereda queda el Encanto",
}


# 2026-11-21: the gemini expansion of flora_ecosystems cited homepages and evidence files
# written as prose (no fetched pages, unverifiable figures). Rejected until re-researched.
REJECTED_FLORA = {
    "flora_ecosystems." + suffix
    for suffix in (
        "subparamo_transition", "frailejon_growth_and_longevity",
        "frailejon_necromass_thermal_jacket", "adaptation_leaf_pubescence",
        "puya_paramo_bromeliads", "sphagnum_peat_moss", "paramo_lichens_rocks",
        "turberas_bogs_peatlands", "cushion_bogs_damage_trampling",
        "volcanic_ash_on_glaciers", "glaciers_vs_paramo_water_role",
        "paramo_sponge_mechanism", "fog_interception_water_cycle",
        "urban_water_supply_cities", "nevado_del_ruiz_ice_cap",
        "nevado_del_tolima_glacier", "glacier_monitoring_ideam",
        "wildfire_impact_and_recovery", "restoration_nurseries_high_mountain",
        "sujeto_de_derechos_ruling",
    )
}


POLISH = Path(__file__).resolve().parent / "polish"
STYLE_FINAL = Path(__file__).with_name("style_final")
STYLE = Path(__file__).resolve().parent / "style"
NUMBER = re.compile(r"\d+(?:[.,]\d+)*")


def fold(text):
    text = unicodedata.normalize("NFKD", text.casefold())
    return " ".join(re.findall(r"\w+", "".join(c for c in text if not unicodedata.combining(c))))


def numbers(text):
    return sorted(NUMBER.findall(text))


# (kept id, dropped id). Reservations belong to booking_fees (lower order than hours_status).
MERGES = [
    ("hours_status.conservation_closures", "hours_status.conservation_closures_dates_schedule"),
    ("booking_fees.reservation_requirements", "hours_status.booking_time_limits_before_visit"),
]
# Coordinator decisions from the near-duplicate review (near_duplicates.py):
# {"merges": [[keep_id, drop_id], ...], "drop_examples": {entry_id: [example, ...]}}.
DECISIONS = Path(__file__).with_name("dedup_decisions.json")
if DECISIONS.exists():
    MERGES += [tuple(pair) for pair in json.loads(DECISIONS.read_text(encoding="utf-8")).get("merges", [])]

MERGED = Path(__file__).with_name("merged_examples.json")
# Builder output short/variants per entry (regen_test.py base): the text polish patches replace.
BASES = Path(__file__).with_name("polish_base.json")
HN_MAP = Path(__file__).with_name("hard_negative_map.json")

PICO_ENTRY = "hours_status.pico_y_placa_hours_murillo"
PICO_NUMBERS = ["1815", "24", "2026", "5", "00", "4", "00"]  # as split by NUMBER


def dropped_pico_clause(old, new):
    """True when `new` keeps every number of `old` except one full pico y placa citation."""
    if "1815" not in old or "1815" in new:
        return False
    remaining = numbers(old)
    for token in PICO_NUMBERS:
        if token not in remaining:
            return False
        remaining.remove(token)
    return numbers(new) == sorted(remaining)


def apply_polish():
    """Apply wording-only patches from polish/<section>.json (written by polish agents).

    Patch format: {"<entry id>": {"short": str, "variants": [str], "examples": {"old": "new"},
    optional "short_from"/"variants_from": the exact current text the patch replaces}}.
    A short/variant is applied only while the current text still equals its recorded base
    (polish_base.json), and only if it keeps exactly the numbers of the text it replaces
    (variants: the numbers of the new short); an example swap is accepted only if the new
    example is unique across the corpus. Rejections are written to polish/rejections.json.
    """
    rejections = []
    files = sorted(POLISH.glob("*.json")) if POLISH.exists() else []
    files = [f for f in files if f.name not in ("rejections.json", "applied.json")]
    # Final style pass (style/<section>.json, every patch with short_from) runs after polish.
    files += sorted(STYLE.glob("*.json")) if STYLE.exists() else []
    # Final near-duplicate / eval-leakage example swaps (style_final/<section>.json) run last.
    files += sorted(STYLE_FINAL.glob("*.json")) if STYLE_FINAL.exists() else []
    if not files:
        return
    all_examples = {}
    for path in sorted(SECTIONS.glob("*.json")):
        for entry in json.loads(path.read_text(encoding="utf-8"))["entries"]:
            for example in entry["examples"]:
                all_examples[fold(example)] = entry["id"]
    bases = json.loads(BASES.read_text(encoding="utf-8")) if BASES.exists() else {}
    applied_path = POLISH / "applied.json"
    applied = json.loads(applied_path.read_text(encoding="utf-8")) if applied_path.exists() else {}
    swaps = {}
    for patch_file in files:
        name = patch_file.stem
        patches = json.loads(patch_file.read_text(encoding="utf-8"))
        section = load(name)
        by_id = {e["id"]: e for e in section["entries"]}
        for eid, patch in patches.items():
            entry = by_id.get(eid)
            if entry is None:
                if eid not in {drop for _, drop in MERGES}:
                    rejections.append({"id": eid, "reason": "unknown id"})
                continue
            answer = entry["answer"]
            base = bases.get(eid, {})
            if "short_from" in patch:
                # Style-pass patches name the exact text they replace; that wins over polish_base.
                base = {"short": patch["short_from"], "variants": patch.get("variants_from", answer.get("variants"))}
            new_short = patch.get("short")
            if new_short and new_short != answer["short"] and answer["short"] != base.get("short"):
                # The short changed after the patch was written (or has no recorded base): the
                # newer reviewed text wins; the patch must be rewritten against it.
                rejections.append({"id": eid, "field": "short", "reason": "short differs from patch base"})
            elif new_short and new_short != answer["short"]:
                if dropped_pico_clause(answer["short"], new_short):
                    # The Brisas pico y placa notice was pasted into many access shorts; it may be
                    # dropped whole as long as the entry links the dedicated entry.
                    related = entry.setdefault("related", [])
                    if PICO_ENTRY not in related:
                        related[:] = related[:2] + [PICO_ENTRY]
                    answer["short"] = new_short
                elif "short_from" in patch and not (Counter(numbers(new_short)) - Counter(numbers(answer["short"]))):
                    # Style pass may drop citation dates/numbers but never add or alter a figure;
                    # every drop is logged for the coordinator to check.
                    dropped = sorted((Counter(numbers(answer["short"])) - Counter(numbers(new_short))).elements())
                    if dropped:
                        rejections.append({"id": eid, "field": "short", "reason": "style pass dropped numbers (applied)", "dropped": dropped})
                    answer["short"] = new_short
                elif numbers(new_short) != numbers(answer["short"]):
                    rejections.append({"id": eid, "field": "short", "reason": "numbers changed"})
                else:
                    answer["short"] = new_short
            variants = patch.get("variants")
            if variants and variants != answer.get("variants") and answer.get("variants") != base.get("variants"):
                rejections.append({"id": eid, "field": "variants", "reason": "variants differ from patch base"})
            elif variants and variants != answer.get("variants"):
                if all(set(numbers(v)) <= set(numbers(answer["short"])) for v in variants):
                    answer["variants"] = variants
                else:
                    rejections.append({"id": eid, "field": "variants", "reason": "numbers not in short"})
            done = applied.setdefault(eid, {})
            for old, new in (patch.get("examples") or {}).items():
                key_old, key_new = fold(old), fold(new)
                idx = [i for i, x in enumerate(entry["examples"]) if fold(x) == key_old]
                owner = all_examples.get(key_new)
                if not idx:
                    if owner == eid:
                        done[key_old] = new  # already applied on a previous run
                        continue
                    previous = done.get(key_old)
                    idx = [i for i, x in enumerate(entry["examples"]) if previous and fold(x) == fold(previous)]
                    if not idx:
                        present = {fold(x) for x in entry["examples"]}
                        if swapped_forms(eid, old) & present:
                            continue  # a later patch already replaced this patch's result
                        rejections.append({"id": eid, "field": "examples", "old": old, "reason": "old not found"})
                        continue
                    swaps[fold(previous)] = new  # the patch now replaces an earlier replacement
                    key_old = fold(previous)
                if owner and owner != eid or key_new in {fold(x) for x in entry["examples"]}:
                    rejections.append({"id": eid, "field": "examples", "new": new, "reason": "duplicate"})
                    continue
                entry["examples"][idx[0]] = new
                all_examples.pop(key_old, None)
                all_examples[key_new] = eid
                done[fold(old)] = new
        save(name, section)
    applied_path.write_text(json.dumps(applied, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Hard negatives must stay copies of real examples (contract rule 3): follow every swap.
    for patch_file in files:
        for patch in json.loads(patch_file.read_text(encoding="utf-8")).values():
            for old, new in (patch.get("examples") or {}).items():
                swaps[fold(old)] = new
    for path in sorted(SECTIONS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for entry in data["entries"]:
            negatives = entry.get("hard_negatives", [])
            for i, text in enumerate(negatives):
                if fold(text) in swaps:
                    negatives[i] = swaps[fold(text)]
                    changed = True
        if changed:
            save(path.stem, data)
    # A stale polish short/variants is harmless once a later style patch for the same entry is in
    # place (style patches name the exact text they replace); drop those base-mismatch reports.
    final = {e["id"]: e["answer"] for path in sorted(SECTIONS.glob("*.json"))
             for e in json.loads(path.read_text(encoding="utf-8"))["entries"]}
    styled = {}
    for patch_file in files:
        if patch_file.parent != POLISH:
            for eid, patch in json.loads(patch_file.read_text(encoding="utf-8")).items():
                styled.setdefault(eid, []).append(patch)

    def superseded(r):
        answer, field = final.get(r["id"]), r.get("field")
        if answer is None or field not in ("short", "variants") or "differ" not in r["reason"]:
            return False
        return any(answer.get(field) == patch.get(field) for patch in styled.get(r["id"], []))

    rejections = [r for r in rejections if not superseded(r)]
    (POLISH / "rejections.json").write_text(json.dumps(rejections, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"polish applied from {len(files)} files, {len(rejections)} rejections")


def swapped_forms(eid, example):
    """Folded forms of a carried example: itself plus every replacement recorded in polish/applied.json.

    Keeps a merge carry from re-adding an example that a polish/style patch already replaced.
    """
    applied_path = POLISH / "applied.json"
    done = json.loads(applied_path.read_text(encoding="utf-8")).get(eid, {}) if applied_path.exists() else {}
    forms, key = set(), fold(example)
    while key and key not in forms:
        forms.add(key)
        key = fold(done[key]) if key in done else None
    return forms


def load(name):
    return json.loads((SECTIONS / f"{name}.json").read_text(encoding="utf-8"))


def save(name, data):
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    (SECTIONS / f"{name}.json").write_text(text, encoding="utf-8")


def replace_examples(entry, mapping):
    entry["examples"] = [mapping.get(x, x) for x in entry["examples"]]


def drop_examples():
    """Remove examples the near-duplicate review assigned to another entry (dedup_decisions.json)."""
    if not DECISIONS.exists():
        return
    drops = json.loads(DECISIONS.read_text(encoding="utf-8")).get("drop_examples", {})
    for f in sorted(SECTIONS.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        changed = False
        for entry in data["entries"]:
            gone = {fold(x) for x in drops.get(entry["id"], [])}
            if gone and any(fold(x) in gone for x in entry["examples"]):
                entry["examples"] = [x for x in entry["examples"] if fold(x) not in gone]
                changed = True
        if changed:
            save(f.stem, data)


def apply_hard_negative_map():
    """Replace invented hard negatives with the real examples chosen by map_hard_negatives.py.

    A mapping is used only while its target is still an example of another entry; otherwise the
    invented text stays (the validator keeps flagging it) and the map must be regenerated.
    """
    if not HN_MAP.exists():
        return
    mapping = json.loads(HN_MAP.read_text(encoding="utf-8"))
    files = sorted(SECTIONS.glob("*.json"))
    owner = {}
    for f in files:
        for entry in json.loads(f.read_text(encoding="utf-8"))["entries"]:
            for example in entry["examples"]:
                owner.setdefault(example, entry["id"])
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        changed = False
        for entry in data["entries"]:
            pairs = mapping.get(entry["id"], {})
            negatives = entry.get("hard_negatives", [])
            for i, text in enumerate(negatives):
                real = pairs.get(text)
                if real and owner.get(real, entry["id"]) != entry["id"] and real not in negatives:
                    negatives[i] = real
                    changed = True
        if changed:
            save(f.stem, data)


def main():
    fauna = load("fauna")
    fauna["entries"] = [e for e in fauna["entries"] if e["id"] not in FAUNA_TO_RULES]
    for entry in fauna["entries"]:
        entry["related"] = list(dict.fromkeys(FAUNA_TO_RULES.get(r, r) for r in entry.get("related", [])))
    fauna["featured"] = [f for f in fauna.get("featured", []) if f not in FAUNA_TO_RULES]
    save("fauna", fauna)

    rules = load("rules")
    rules["entries"] = [e for e in rules["entries"] if e["id"] != NO_HUNTING["id"]] + [NO_HUNTING]
    save("rules", rules)

    conversation = load("conversation")
    for entry in conversation["entries"]:
        if entry["id"] in CONVERSATION_REPLACE:
            old, new = CONVERSATION_REPLACE[entry["id"]]
            replace_examples(entry, {old: new})
    save("conversation", conversation)

    geography = load("geography")
    for entry in geography["entries"]:
        if entry["id"] == "geography.laguna_encanto":
            replace_examples(entry, ENCANTO_REPLACE)
    save("geography", geography)

    # access and activities both used "caminata desde El Cedral"; lower order (access) keeps
    # the walk distances, activities keeps the walk itself.
    for name, eid, label in (
        ("access", "access.cedral_walk_distances", "distancia y tiempo desde El Cedral"),
        ("activities", "activities.otun_cedral_walk", "caminata El Cedral a Laguna del Otún"),
    ):
        section = load(name)
        for entry in section["entries"]:
            if entry["id"] == eid:
                entry["label"] = label
        save(name, section)
    flora = load("flora_ecosystems")
    flora["entries"] = [e for e in flora["entries"] if e["id"] not in REJECTED_FLORA]
    flora["featured"] = [f for f in flora.get("featured", []) if f not in REJECTED_FLORA]
    save("flora_ecosystems", flora)

    apply_polish()

    # Duplicate topics: keep one entry, carry the dropped entry's examples into it.
    for keep_id, drop_id in MERGES:
        keep_sec, drop_sec = keep_id.split(".")[0], drop_id.split(".")[0]
        keep_data = load(keep_sec)
        drop_data = keep_data if drop_sec == keep_sec else load(drop_sec)
        keep = next((e for e in keep_data["entries"] if e["id"] == keep_id), None)
        drop = next((e for e in drop_data["entries"] if e["id"] == drop_id), None)
        if keep is None:
            continue
        # Record the carried examples so a rebuild of the kept section alone (donor already
        # merged away) still gets them.
        carried = json.loads(MERGED.read_text(encoding="utf-8")) if MERGED.exists() else {}
        if drop is not None:
            carried[keep_id] = drop["examples"]
            MERGED.write_text(json.dumps(carried, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        seen = {fold(x) for x in keep["examples"]}
        keep["examples"] += [x for x in carried.get(keep_id, []) if not swapped_forms(keep_id, x) & seen]
        if drop is None:
            save(keep_sec, keep_data)
            continue
        drop_data["entries"] = [e for e in drop_data["entries"] if e["id"] != drop_id]
        for data in {id(keep_data): keep_data, id(drop_data): drop_data}.values():
            for entry in data["entries"]:
                entry["related"] = [keep_id if r == drop_id else r for r in entry.get("related", [])]
                entry["related"] = [r for r in dict.fromkeys(entry["related"]) if r != entry["id"]]
            data["featured"] = list(dict.fromkeys(keep_id if f == drop_id else f for f in data.get("featured", [])))
        save(keep_sec, keep_data)
        if drop_sec != keep_sec:
            save(drop_sec, drop_data)

    # Second pass: example swaps written against examples carried in by MERGES only find them now,
    # and shorts already set by the first pass no longer log base mismatches. Idempotent.
    apply_polish()
    drop_examples()
    apply_hard_negative_map()

    # User-approved changes (add, update, delete) replay last so builders cannot erase them.
    registry = Path(__file__).with_name("knowledge_additions.json")
    if registry.exists():
        helper = ROOT / ".agents/skills/add-park-knowledge/scripts/knowledge.py"
        spec = importlib.util.spec_from_file_location("knowledge_additions", helper)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sections = {f.stem: json.loads(f.read_text(encoding="utf-8"))
                    for f in SECTIONS.glob("*.json")}
        additions = json.loads(registry.read_text(encoding="utf-8"))
        for sid, data in module.replay(sections, additions).items():
            if data != sections[sid]:
                save(sid, data)

    # Drop references to any id removed above, in every section.
    files = sorted(SECTIONS.glob("*.json"))
    ids = {e["id"] for f in files for e in json.loads(f.read_text(encoding="utf-8"))["entries"]}
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        before = json.dumps(data, ensure_ascii=False)
        for entry in data["entries"]:
            entry["related"] = [r for r in entry.get("related", []) if r in ids]
        data["featured"] = [x for x in data.get("featured", []) if x in ids]
        if json.dumps(data, ensure_ascii=False) != before:
            save(f.stem, data)
    print("coordinator fixes applied")


if __name__ == "__main__":
    # Several agents run this script concurrently; serialize the read-modify-write passes.
    with open(Path(__file__).with_suffix(".lock"), "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        main()
