"""Candidate search for contradictions and staleness in the FAQ snapshot.

Reads research_notes/curation_v2/snapshots/sections_before/*.json and prints a
JSON list of candidates. It does not decide which ones are real conflicts:
each candidate still has to be read against both answers and the cited evidence.

    python3 research_notes/curation_v2/tools/contradictions.py

A candidate is one of:
  numeric — same entity and measure, two normalized values;
  rule    — one entry allows a regulated activity another forbids;
  stale   — undated fee, undated closure, or a pre-2025 operational fact
            stated as what applies now;
  safety  — incompatible instructions for the same emergency.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SECTIONS = ROOT / "research_notes/curation_v2/snapshots/sections_before"

# Today for this audit. Years strictly older than 2025 are stale when a
# changeable fact is stated as current.
AS_OF_YEAR = 2025

PLACES = (
    "brisas", "potosi", "santa barbara", "asomadera", "laguna verde",
    "otun", "cocora", "juntas", "anzoategui", "palomar", "cedral",
    "arenales", "calvito", "termales", "cisne", "murillo", "manizales",
    "villamaria", "pereira", "salento", "armenia", "ibague",
)


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text.lower()


def sentences(text: str) -> list[str]:
    # "a. m." / "p. m." / "12:00 m." are not sentence ends.
    protected = re.sub(r"(?i)\b([ap])\.\s*m\.", r"\1<dot> m<dot>", text)
    protected = re.sub(r"(?i)(\d:\d{2})\s+m\.", r"\1 m<dot>", protected)
    parts = re.split(r"(?<=[.!?])\s+|\n+", protected.strip())
    return [part.replace("<dot>", ".").strip() for part in parts if part.strip()]


def num(raw: str) -> float:
    """Spanish grouped number: 61.388,24 -> 61388.24; 4.100 -> 4100; 7,5 -> 7.5."""
    raw = raw.strip().replace(" ", "")
    if "," in raw and "." in raw:
        raw = raw.replace(".", "").replace(",", ".")
    elif "," in raw:
        left, right = raw.split(",", 1)
        raw = f"{left}.{right}" if len(right) != 3 else left + right
    elif raw.count(".") == 1:
        left, right = raw.split(".", 1)
        if len(right) == 3 and len(left) <= 3:
            raw = left + right
    elif raw.count(".") > 1:
        raw = raw.replace(".", "")
    return float(raw)


def nearest(folded: str, start: int, names: tuple[str, ...], window: int = 90) -> str | None:
    chunk = folded[max(0, start - window):start]
    found = None
    at = -1
    for name in names:
        idx = chunk.rfind(name)
        if idx > at:
            at = idx
            found = name
    return found


def load_entries() -> list[dict]:
    entries = []
    for path in sorted(SECTIONS.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for entry in data["entries"]:
            answer = entry.get("answer") or {}
            fields = []
            if answer.get("short"):
                fields.append(("short", answer["short"]))
            for variant in answer.get("variants") or []:
                if isinstance(variant, str) and variant.strip():
                    fields.append(("variant", variant))
            detail = answer.get("detail")
            if isinstance(detail, str) and detail.strip():
                fields.append(("detail", detail))
            entries.append({
                "id": entry["id"],
                "section": path.stem,
                "fields": fields,
                "text": " ".join(text for _, text in fields),
            })
    return entries


def add_fact(facts: dict, topic: str, value: float, entry_id: str, quote: str) -> None:
    bucket = facts.setdefault(topic, {})
    key = f"{value:.4f}".rstrip("0").rstrip(".")
    bucket.setdefault(key, []).append((entry_id, quote))


ENTITIES = (
    "paramillo del cisne", "morro negro", "paramillo de santa rosa",
    "paramillo del quindio", "santa isabel", "nevado del tolima",
    "nevado del ruiz", "laguna del otun", "laguna del encanto",
    "laguna el corazon", "laguna bombona", "brisas", "potosi",
    "el cisne", "valle de las tumbas",
)


def entity_before(folded: str, start: int) -> str | None:
    return nearest(folded, start, ENTITIES, 160)


def _entry_entity(entry_id: str) -> str | None:
    folded = fold(entry_id.replace("_", " ").replace(".", " "))
    if "santa isabel" in folded or "poleka" in folded:
        return "santa isabel"
    if "morro negro" in folded or "paramillo cisne" in folded or "cisne" in folded and "height" in folded:
        return "paramillo del cisne"
    if "santa rosa" in folded and "paramillo" in folded:
        return "paramillo de santa rosa"
    if "paramillo quindio" in folded:
        return "paramillo del quindio"
    if "tolima" in folded and "height" in folded:
        return "nevado del tolima"
    if "ruiz" in folded and "height" in folded:
        return "nevado del ruiz"
    return None


def _altitude_clause(folded: str, start: int) -> bool:
    clause = folded[max(0, start - 35):start]
    if any(word in clause for word in ("bajo ", "cerca", "incendio", "afectad", "retroceso")):
        return False
    cue = folded[max(0, start - 50):start + 12]
    return any(word in cue for word in ("cima", "cumbre", "altura", "altitud", "esta a", "estan en", "metros", " m"))


def extract_numeric(entries: list[dict]) -> list[dict]:
    facts: dict[str, dict[str, list]] = {}
    altitude = re.compile(
        r"(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d{3,5}(?:[.,]\d+)?)\s*(?:m\b\.?|metros)",
        re.I,
    )
    # 4.923 / 4.965 written as a summit figure without repeating the unit.
    bare_summit = re.compile(r"(?<![\d])(\d\.\d{3})(?![\d])")
    hectares = re.compile(
        r"(\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?)\s*hect[aá]reas",
        re.I,
    )
    kilometers = re.compile(
        r"(\d{1,3}(?:[.,]\d+)?)\s*(?:km\b|kil[oó]metros)",
        re.I,
    )
    money = re.compile(r"\$\s*(\d{1,3}(?:\.\d{3})+|\d+)(?!\s*km)", re.I)
    age = re.compile(r"(\d{1,3})\s*años", re.I)
    deaths = re.compile(
        r"(?:m[aá]s de\s+)?(\d{1,3}(?:\.\d{3})+|\d+)(?:\s*mil)?",
        re.I,
    )
    clock = re.compile(
        r"(\d{1,2}:\d{2})\s*a\.?\s*m\.?\s*a\s*(?:las\s*)?(\d{1,2}:\d{2})\s*(a\.?\s*m\.?|p\.?\s*m\.?|m\.)",
        re.I,
    )

    for entry in entries:
        for _field, text in entry["fields"]:
            folded = fold(text)
            for sentence in sentences(text):
                folded_sentence = fold(sentence)
                for match in altitude.finditer(sentence):
                    ent = entity_before(folded_sentence, match.start()) or _entry_entity(entry["id"])
                    if not ent or not _altitude_clause(folded_sentence, match.start()):
                        continue
                    add_fact(facts, f"altitude:{ent}", num(match.group(1)), entry["id"], sentence)
                if _entry_entity(entry["id"]) in {"santa isabel", "paramillo de santa rosa", "paramillo del cisne", "morro negro"}:
                    for match in bare_summit.finditer(sentence):
                        before = folded_sentence[max(0, match.start() - 16):match.start()]
                        if "bajo" in before or "cerca" in before:
                            continue
                        ent = entity_before(folded_sentence, match.start()) or _entry_entity(entry["id"])
                        if ent:
                            add_fact(facts, f"altitude:{ent}", num(match.group(1)), entry["id"], sentence)

                for match in hectares.finditer(sentence):
                    if "paramo" in folded_sentence:
                        topic = "area:paramo"
                    elif "1973" in folded_sentence or "acuerdo" in folded_sentence or "aproximad" in folded_sentence:
                        topic = "area:founding_1973"
                    else:
                        topic = "area:park"
                    add_fact(facts, topic, num(match.group(1)), entry["id"], sentence)

                for match in kilometers.finditer(sentence):
                    places = tuple(place for place in PLACES if place in folded_sentence)
                    if len(places) < 1:
                        continue
                    topic = "km:" + "+".join(places[:4])
                    add_fact(facts, topic, num(match.group(1)), entry["id"], sentence)

                for match in money.finditer(sentence):
                    kind = _money_kind(folded_sentence, match.start())
                    add_fact(facts, f"cop:{kind}", num(match.group(1)), entry["id"], sentence)

                for match in age.finditer(sentence):
                    role = _age_role(folded_sentence)
                    if role:
                        add_fact(facts, f"age:{role}", float(match.group(1)), entry["id"], sentence)

                if any(word in folded_sentence for word in ("muerto", "victima", "fallec")) and "1985" in folded and "sin muertos" not in folded_sentence:
                    for match in deaths.finditer(sentence):
                        raw = match.group(0)
                        value = num(match.group(1))
                        if "mil" in fold(raw) and value < 1000:
                            value *= 1000
                        if value >= 1000:
                            add_fact(facts, "deaths:armero_1985", value, entry["id"], sentence)
                if "quindio" in folded_sentence and re.search(r"\$\s*0\b", sentence):
                    add_fact(facts, "cop:admission_under25", 0.0, entry["id"], sentence)

                for match in clock.finditer(sentence):
                    end = _clock_end(match.group(2), match.group(3))
                    window = folded_sentence[max(0, match.start() - 100):match.start()]
                    places = [place for place in PLACES if place in window]
                    for place in places or [None]:
                        if place:
                            add_fact(facts, f"close:{place}", end, entry["id"], sentence)

            if "conejeras" in folded and "exting" in folded:
                if "marzo de 2024" in folded:
                    add_fact(facts, "date:conejeras_extinction", 2024.03, entry["id"], _clip(text, "marzo de 2024"))
                if "comienzos de 2024" in folded:
                    add_fact(facts, "date:conejeras_extinction", 2024.01, entry["id"], _clip(text, "comienzos de 2024"))
            if "extinc" in folded and ("tres a cinco" in folded or "tres a cinco anos" in folded):
                add_fact(facts, "projection:santa_isabel_glacier", 3.0, entry["id"], _clip(text, "tres a cinco"))
            if re.search(r"\b2028\b", text) and "santa isabel" in folded:
                add_fact(facts, "projection:santa_isabel_glacier", 2028.0, entry["id"], _clip(text, "2028"))
            if "1,82" in text or "1.82" in text:
                add_fact(facts, "percent:glacier_share", 1.82, entry["id"], _clip(text, "1,82"))
            if re.search(r"\b10\b|\bdiez\b", folded) and "municipio" in folded:
                if re.search(r"\bdiez\b|\b10 municipios\b", folded):
                    add_fact(facts, "count:municipalities", 10, entry["id"], _clip(text, "municipio"))
            if re.search(r"\b11 municipios\b", folded):
                add_fact(facts, "count:municipalities", 11, entry["id"], _clip(text, "11"))
            if re.search(r"\bvei\b|explosividad", folded) and "1985" in folded:
                if "3 a 4" in folded or "3-4" in folded:
                    add_fact(facts, "vei:1985", 3.5, entry["id"], _clip(text, "3"))
                if re.search(r"\bvei 3\b", folded):
                    add_fact(facts, "vei:1985", 3.0, entry["id"], _clip(text, "VEI 3"))

    candidates = []
    for topic, values in sorted(facts.items()):
        values = _prune_values(topic, values)
        if len(values) < 2:
            continue
        # 7.5 km to the boundary and 18 km to the lagoon are two endpoints.
        if topic.startswith("km:") and _km_pair_is_two_endpoints(values):
            continue
        ids = []
        quotes = {}
        rendered = []
        for value, hits in sorted(values.items(), key=lambda item: float(item[0])):
            rendered.append(value)
            for entry_id, quote in hits:
                if entry_id not in quotes:
                    quotes[entry_id] = quote
                    ids.append(entry_id)
        if len(quotes) < 1:
            continue
        candidates.append({
            "type": "numeric",
            "topic": topic,
            "values": rendered,
            "ids": list(dict.fromkeys(ids)),
            "quotes": quotes,
        })
    return candidates


def _prune_values(topic: str, values: dict) -> dict:
    """Keep only figures that can be the same quantity. Different objects stay out."""
    def quote_blob(hits: list) -> str:
        return fold(" ".join(quote for _, quote in hits))

    kept = {}
    for raw, hits in values.items():
        value = float(raw)
        blob = quote_blob(hits)
        if topic == "area:park" and not 60000 <= value <= 70000:
            continue
        if topic == "area:paramo" and value < 100000:
            continue
        if topic.startswith("age:minimum"):
            continue
        if topic.startswith("altitude:santa isabel") and value < 4890:
            continue
        if topic.startswith("altitude:") and any(word in blob for word in ("bajo ", "incendio", "vivero", "retroceso")):
            # "bajo 4.900" is a band, not a summit height. The nursery is not the cabin.
            if "vivero" in blob or "propag" in blob:
                if topic != "altitude:potosi":
                    continue
            if "bajo " in blob or "incendio" in blob:
                continue
        if topic == "deaths:armero_1985" and value < 10000:
            continue
        if topic.startswith("km:"):
            if "tres caminos" in blob or "lahar" in blob:
                continue
        kept[raw] = hits
    if topic.startswith("altitude:"):
        nums = sorted((float(value), quote_blob(hits)) for value, hits in kept.items())
        if len(nums) >= 2:
            spread = nums[-1][0] - nums[0][0]
            approximate = all("unos" in blob or "aproxim" in blob for _, blob in nums)
            if spread < 1 or (approximate and spread < 15):
                return {}
    if topic == "area:paramo":
        nums = sorted(float(value) for value in kept)
        if len(nums) >= 2 and (nums[-1] - nums[0]) < 1:
            return {}
    if topic.startswith("close:"):
        nums = sorted(float(value) for value in kept)
        if len(nums) >= 2 and (nums[-1] - nums[0]) < 0.5:
            return {}
    return kept


def _km_pair_is_two_endpoints(values: dict) -> bool:
    if len(values) != 2:
        return False
    quotes = [quote for hits in values.values() for _, quote in hits]
    blob = fold(" ".join(quotes))
    conflict = any(word in blob for word in ("contradic", "no uses", "no coincid", "no son la misma", "tabla"))
    return not conflict


def _money_kind(folded: str, start: int) -> str:
    window = folded[max(0, start - 40):start + 40]
    if "buseta" in window or "microbus" in window:
        return "buseta"
    if "colectivo" in window:
        return "colectivo"
    if re.search(r"\bbus\b", window):
        return "bus"
    if "automovil" in window or "carro" in window:
        return "auto"
    if "guianza" in window or "interpretacion" in window:
        return "guide_brisas"
    if "quindio" in folded and num_is_zero(window):
        return "quindio_row"
    if "menor" in folded and "25" in folded:
        return "admission_under25"
    if "mayor" in folded and "25" in folded:
        return "admission_over25"
    if "no residente" in folded or "extranjero no" in folded:
        return "admission_foreign"
    return "other"


def num_is_zero(window: str) -> bool:
    return bool(re.search(r"\$\s*0\b", window))


def _age_role(folded: str) -> str | None:
    if "maxima" in folded or "limite maximo" in folded or "mayores de 70" in folded or "69" in folded and "70" in folded:
        if "69" in folded or "70" in folded:
            return "maximum"
    if "minima" in folded or "menores de" in folded:
        if "cumbre" in folded or "travesia" in folded or "resto de rutas" in folded:
            return "minimum_technical"
        if "brisas" in folded or "cisne" in folded or "otun" in folded:
            return "minimum_north"
    return None


def _clock_end(hhmm: str, meridiem: str) -> float:
    hour, minute = (int(part) for part in hhmm.split(":"))
    marker = fold(meridiem)
    if "p" in marker and hour < 12:
        hour += 12
    if marker.strip() in {"m.", "m"} and hour == 12:
        hour = 12
    return hour + minute / 60.0


def _clip(text: str, needle: str) -> str:
    folded = fold(text)
    idx = folded.find(fold(needle))
    if idx < 0:
        return text[:240]
    start = text.rfind(".", 0, idx)
    start = 0 if start < 0 else start + 1
    end = text.find(".", idx)
    end = len(text) if end < 0 else end + 1
    return " ".join(text[start:end].split())


RULES = (
    ("pets", ("mascota", "perro", "animal domestico"), ("prohib", "no puedes ingresar", "no esta permitido"), ("se permite", "puedes ingresar", "puedes llevar")),
    ("drones", ("dron",), ("prohib", "no puedes utilizar", "no uses el dron"), ("se permite", "puedes usar el dron", "puedes volar")),
    ("horses", ("cabalgata", "caballo", "semoviente"), ("no se permiten cabalgatas", "no entran mulas ni caballos", "prohib"), ("paseo a caballo", "puedes montar", "cabalgata turistica esta permitida")),
    ("camping", ("acamp", "pernoct", "camping"), ("no estaba habilitado", "no lo cuentes", "no armes", "prohib"), ("puedes pernoctar", "habilitados para pernoctar", "acampar solo en")),
    ("ruiz_summit", ("cima y el crater del ruiz", "cima del nevado del ruiz", "cumbre del ruiz", "crater del ruiz"), ("prohib",), ("puedes ascender", "puedes subir a la cima del ruiz", "esta habilitada la cima del ruiz")),
    ("night", ("nocturn", "de noche", "caminata nocturna"), ("prohibido ingresar", "esta prohibido", "no se autoriza"), ("permiso especial", "se lista caminata nocturna", "puedes entrar de noche")),
    ("bathing", ("bano terapeutico", "banos de salud", "entres al agua"), ("no se permiten", "prohib", "no entres"), ("esta permitido", "puedes banarte", "banos de salud")),
    ("cycling", ("ciclomontan", "bicicleta", "en bici"), ("restringid", "no salgas", "no te autoriza"), ("vias autorizadas", "brisas–olleta", "brisas-olleta")),
    ("guides", ("entrar solo", "acompanado de un guia", "guia o de personal"), ("no puedes entrar solo", "debes ir acompanado"), ("puedes entrar solo", "sin guia", "no necesitas guia")),
    ("fires", ("fogata",), ("prohib", "no hagas fogatas"), ("puedes hacer fogata", "fogata esta permitida")),
    ("porter", ("porteo",), ("prohibido",), ("se permite", "permitido", "lo lista")),
    ("lodging_brisas", ("alojamiento",), ("no lo menciona", "omite ese servicio"), ("gestiona alojamiento", "gestiona en brisas reservas")),
)


def extract_rules(entries: list[dict]) -> list[dict]:
    """Polarity is per sentence, so a ban on a different object in the same answer does not flip the sentence."""
    by_topic: dict[str, dict[str, list[tuple[dict, str]]]] = {}
    for entry in entries:
        for _field, text in entry["fields"]:
            for sentence in sentences(text):
                folded = fold(sentence)
                for topic, keys, forbid, allow in RULES:
                    if not any(key in folded for key in keys):
                        continue
                    polarity = None
                    if any(_positive(folded, key) for key in allow):
                        polarity = "allow"
                    if any(key in folded for key in forbid):
                        polarity = "mixed" if polarity == "allow" else "forbid"
                    if polarity is None:
                        continue
                    by_topic.setdefault(topic, {}).setdefault(polarity, []).append((entry, sentence))
    candidates = []
    for topic, poles in sorted(by_topic.items()):
        has_allow = "allow" in poles or "mixed" in poles
        has_forbid = "forbid" in poles or "mixed" in poles
        if not (has_allow and has_forbid):
            continue
        # Horses: every sentence both bans riding and allows cargo mules. Not two rules.
        if topic == "horses" and "allow" not in poles:
            continue
        quotes = {}
        ids = []
        for polarity, group in poles.items():
            for entry, sentence in group:
                if entry["id"] in quotes:
                    continue
                quotes[entry["id"]] = sentence
                ids.append(entry["id"])
        if len(ids) < 2 and topic not in {"porter", "lodging_brisas", "camping"}:
            continue
        if len(ids) < 1:
            continue
        candidates.append({"type": "rule", "topic": topic, "ids": ids, "quotes": quotes})
    return candidates


def _positive(folded: str, key: str) -> bool:
    idx = folded.find(key)
    if idx < 0:
        return False
    prefix = folded[max(0, idx - 8):idx]
    return not re.search(r"\bno\s*$", prefix)


def _rule_sentence(text: str, topic: str) -> str:
    keys = next(keys for name, keys, _, _ in RULES if name == topic)
    for sentence in sentences(text):
        if any(key in fold(sentence) for key in keys):
            return sentence
    return text[:240]


def extract_stale(entries: list[dict]) -> list[dict]:
    candidates = []
    fee = re.compile(r"\$\s*\d")
    closure = re.compile(r"\b(ha restringido|esta cerrado|están cerrados|permanece cerrado|sigue cerrado)\b", re.I)
    dated = re.compile(r"\b(20\d{2}|enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\b", re.I)
    for entry in entries:
        short = next((text for field, text in entry["fields"] if field == "short"), "")
        folded = fold(short)
        reasons = []
        if fee.search(short) and not re.search(r"20\d{2}", entry["text"]):
            reasons.append("fee_without_year")
        if closure.search(short) and not dated.search(short):
            reasons.append("closure_without_date")
        if re.search(r"cifra vigente de|la cifra vigente es|horario vigente (?!con)", folded):
            if not re.search(r"20(?:2[5-9])", short):
                reasons.append("vigente_without_2025_date")
        full = fold(entry["text"])
        if re.search(r"hoy el punto es|hoy esta (?:abiert|cerrad)|hoy se cobra|hoy la tarifa", full):
            reasons.append("hoy_as_current")
        if not reasons:
            continue
        candidates.append({
            "type": "stale",
            "topic": "+".join(reasons),
            "ids": [entry["id"]],
            "quotes": {entry["id"]: short},
        })
    return candidates


SAFETY = (
    ("ash_roof", ("ceniza", "techo"), ("sin agua", "sin utilizar agua"), ("humedec", "rociar", "con agua")),
    ("yellow_alert", ("alerta amarilla", "en amarilla"), ("siguen abiertos", "siguen bajo monitoreo"), ("restringir la parte alta", "no abras", "no subas")),
    ("hypothermia_drink", ("hipotermia", "frio"), ("bebida tibia",), ("no le des nada", "nada de comer ni beber")),
    ("lightning_posture", ("rayo", "tormenta electrica"), ("nunca te acuestes", "no te acuestes"), ("acuestate en el suelo", "tumbate")),
)


def extract_safety(entries: list[dict]) -> list[dict]:
    by_topic: dict[str, dict[str, list]] = {}
    for entry in entries:
        folded = fold(entry["text"])
        for topic, keys, left, right in SAFETY:
            if not any(key in folded for key in keys):
                continue
            side = None
            if any(key in folded for key in left):
                side = "a"
            if any(key in folded for key in right):
                side = "both" if side else "b"
            if side is None:
                continue
            by_topic.setdefault(topic, {}).setdefault(side, []).append(entry)
    candidates = []
    for topic, sides in sorted(by_topic.items()):
        if not (("a" in sides or "both" in sides) and ("b" in sides or "both" in sides)):
            continue
        if set(sides) == {"both"} and len(sides["both"]) < 1:
            continue
        quotes = {}
        ids = []
        for side, group in sides.items():
            for entry in group:
                if entry["id"] in quotes:
                    continue
                quotes[entry["id"]] = _safety_sentence(entry["text"], topic)
                ids.append(entry["id"])
        if len(ids) < 1:
            continue
        candidates.append({"type": "safety", "topic": topic, "ids": ids, "quotes": quotes})
    return candidates


def _safety_sentence(text: str, topic: str) -> str:
    keys = next(keys for name, keys, _, _ in SAFETY if name == topic)
    for sentence in sentences(text):
        folded = fold(sentence)
        if any(key in folded for key in keys):
            return sentence
    return text[:240]


def main() -> None:
    entries = load_entries()
    candidates = []
    candidates.extend(extract_numeric(entries))
    candidates.extend(extract_rules(entries))
    candidates.extend(extract_stale(entries))
    candidates.extend(extract_safety(entries))
    print(json.dumps({"entries": len(entries), "candidates": len(candidates), "items": candidates}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
