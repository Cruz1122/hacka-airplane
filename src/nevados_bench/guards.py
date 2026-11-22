"""Deterministic guards applied in code to model output before a visitor sees it.

The benchmark showed the chosen model's grounded answers fail in one dominant way: when the
asked station's passage is missing, it answers with another station's value and cites that
station's passage. These guards catch that without a second model call:

1. Values in the answer (times, quantities) must be stated by a passage it cites, or by
   the user message. An answer with values but no citation is rejected.
2. Cited passages must be among the passages shown to the model.
3. Cited passages must belong to the target station (the one asked about, or the one the
   device is installed at), unless they are park-wide (station None).
4. Named values (places, meeting points) from another station's passages are rejected.

A rejected answer is replaced by the fixed abstention sentence; for safety questions a
fixed referral to the station rangers is appended. The fallback never states a value.

Guards only remove answers; they can turn a correct answer into an abstention (measured as
false abstention) but cannot add a wrong value.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import TYPE_CHECKING, Any

from nevados_bench.schemas import GazetteerEntry, Passage, ToolCall
from nevados_bench.scoring.grounding import evidence_values

if TYPE_CHECKING:
    from nevados_bench.world import World
from nevados_bench.values import (
    ABSTAIN_ES,
    contains_named_value,
    extract_citations,
    extract_values,
    is_abstention,
    normalize_text,
)

SAFETY_REFERRAL_ES = (
    "Si se trata de una emergencia o tiene síntomas, busque de inmediato a un guardaparque "
    "de la estación."
)


@dataclass(frozen=True)
class GuardResult:
    text: str
    passed: bool
    reasons: tuple[str, ...] = field(default_factory=tuple)


# Visitors type fast on a phone keyboard: "alto senizo", "laguna espjo", "valle brma".
FUZZY_RATIO = 0.8
FUZZY_MIN_CHARS = 5  # shorter words must match exactly
# Words that do not identify a place on their own ("alto" also means "high").
_GENERIC_WORDS = {"alto", "laguna", "valle", "refugio", "sendero", "estacion", "del", "de", "la"}


def _tokens(norm: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", norm)


def _similar(a: str, b: str) -> bool:
    if a == b:
        return True
    return len(b) >= FUZZY_MIN_CHARS and SequenceMatcher(None, a, b).ratio() >= FUZZY_RATIO


def fuzzy_last_index(tokens: list[str], phrase: str) -> int | None:
    """Start index of the last window of len(phrase words) tokens similar to `phrase`."""
    n = len(phrase.split())
    hits = [i for i in range(len(tokens) - n + 1) if _similar(" ".join(tokens[i : i + n]), phrase)]
    return hits[-1] if hits else None


def fuzzy_contains(tokens: list[str], phrase: str) -> bool:
    return fuzzy_last_index(tokens, phrase) is not None


def _short_name(name: str) -> str:
    norm = normalize_text(name)
    for prefix in ("estacion ", "sendero del ", "sendero de la ", "sendero de ", "sendero "):
        norm = norm.removeprefix(prefix)
    return norm


def station_mentions(text: str, station_names: Mapping[str, str]) -> dict[str, int]:
    """station id -> token index of its last mention (typo-tolerant, 'Estación' optional,
    the distinctive word alone is enough: "Quelital")."""
    tokens = _tokens(normalize_text(text))
    found: dict[str, int] = {}
    for station_id, name in station_names.items():
        short = _short_name(name)
        phrases = [short, *(w for w in short.split() if w not in _GENERIC_WORDS)]
        hits = [i for p in phrases if (i := fuzzy_last_index(tokens, p)) is not None]
        # "estamos en Valle Bruma, no en Alto Cenizo": a negated mention is not the target.
        hits = [i for i in hits if not _negated(tokens, i)]
        if hits:
            found[station_id] = max(hits)
    return found


def _negated(tokens: list[str], index: int) -> bool:
    before = tokens[max(0, index - 3) : index]
    return any(t in ("no", "not", "ni") for t in before) and "sino" not in before


def detect_station(
    text: str, station_names: Mapping[str, str], *, prefer_last: bool = False
) -> str | None:
    """The station `text` is about, or None.

    With several stations named, returns None unless `prefer_last`: then the last one
    mentioned wins ("entre Alto Cenizo y Quelital, ¿a qué altura está Alto Cenizo?",
    "no es en Laguna Espejo, es en Quelital").
    """
    found = station_mentions(text, station_names)
    if len(found) == 1:
        return next(iter(found))
    if found and prefer_last:
        return max(found, key=found.__getitem__)
    return None


def fallback_text(*, safety: bool) -> str:
    return f"{ABSTAIN_ES} {SAFETY_REFERRAL_ES}" if safety else ABSTAIN_ES


def guard_answer(
    text: str,
    *,
    user_message: str,
    shown: Mapping[str, Passage],
    target_station: str | None,
    gazetteer: Iterable[GazetteerEntry] = (),
    safety: bool = False,
) -> GuardResult:
    """Check a grounded answer against the passages that were shown; see module docstring."""
    if is_abstention(text) or not text.strip():
        return GuardResult(text, True)
    reasons: list[str] = []
    shown_upper = {pid.upper(): p for pid, p in shown.items()}
    cited_ids = extract_citations(text)
    cited = [shown_upper[c] for c in cited_ids if c in shown_upper]
    if any(c not in shown_upper for c in cited_ids):
        reasons.append("cited_not_shown")
    if target_station is not None and any(
        p.station is not None and p.station != target_station for p in cited
    ):
        reasons.append("other_station_cited")

    values = evidence_values(text)  # list numbering ("1.", "2.") is not a stated value
    supported = set(extract_values(user_message))
    for p in cited:
        supported |= extract_values(p.text) | set(p.values)
    if values and not cited_ids:
        reasons.append("uncited_values")
    elif values - supported:
        reasons.append("unsupported_values")

    if target_station is not None:
        norm_text = normalize_text(text)
        norm_user = normalize_text(user_message)
        for entry in gazetteer:
            if (
                entry.station is not None
                and entry.station != target_station
                and not any(ch.isdigit() for ch in entry.value)
                and contains_named_value(norm_text, entry.value)
                and not contains_named_value(norm_user, entry.value)
            ):
                reasons.append("other_station_named_value")
                break

    if reasons:
        return GuardResult(fallback_text(safety=safety), False, tuple(reasons))
    return GuardResult(text, True)


# ----------------------------------------------------------------------------- tool calls

_MONTHS = "enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre"  # noqa: E501
_DAYS = "lunes|martes|miercoles|jueves|viernes|sabado|domingo"
_DAYS_EN = "monday|tuesday|wednesday|thursday|friday|saturday|sunday"
_DATE_RE = re.compile(
    rf"\b(hoy|manana|pasado manana|{_DAYS}|fin de semana|today|tomorrow|tonight|{_DAYS_EN}"
    rf"|weekend)\b|\b\d{{1,2}} de ({_MONTHS})\b|\b({_MONTHS}) \d{{1,2}}\b|\d{{4}}-\d{{2}}-\d{{2}}"
    r"|\b\d{1,2}/\d{1,2}\b"
)
_MONTH_WORDS = [*_MONTHS.split("|"), "january", "february", "march", "april", "may", "june",
                "july", "august", "september", "october", "november", "december"]  # fmt: skip
_CITIES = "bogota|medellin|cali|manizales|pereira|armenia|barranquilla|cartagena|bucaramanga|ibague"
# Stating where the visitors come from grounds visitor_type; the model maps it to the enum.
_VISITOR_RE = re.compile(
    r"colombian|nacional|national|extranjer|foreign|internacional|international"
    r"|reducid|discapacidad|disability|adultos? mayor|senior"
    rf"|\b(soy|somos|vengo|venimos|vamos \w+) de \w+|\bfrom \w+|\bde ({_CITIES})\b"
)
_COUNT_WORDS = (
    "uno|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|once|doce|quince|veinte"
    "|one|two|three|four|five|six|seven|eight|nine|ten|twelve|twenty"
)
_NUM = rf"(\d+|{_COUNT_WORDS})"
_PEOPLE = (
    "personas|persona|adultos|adulto|ninos|nino|visitantes|turistas|amigos|estudiantes"
    "|heridos|herido|afectados|lesionados|people|persons|person|adults|kids|students|friends"
    "|visitors|visitor|tourists|hikers|travelers"
)
# A number counts as a group size only next to people words or a group verb: the "29" in
# "domingo 29 de noviembre" must not ground group_size.
_COUNT_RE = re.compile(
    rf"\b{_NUM} (\w+ )?({_PEOPLE})\b"
    rf"|\b(somos|seremos|vamos|iremos|grupo de|group of|we are|para) {_NUM}\b"
    r"|\b(yo solo|yo sola|solo yo|mi novia y yo|mi novio y yo|mi esposa y yo|mi esposo y yo"
    r"|alone|just me|pareja|couple|es solo|solo (el|ella|mi \w+|uno|una))\b"
    r"|(people|person|personas|people_count|group_size)\W+\d+"
)


@dataclass(frozen=True)
class RouteGuardResult:
    decision: str | None  # unchanged model decision, or "clarify" when a slot is not grounded
    calls: tuple[ToolCall, ...]
    missing: tuple[str, ...] = ()  # required args the user never stated: ask for these
    needs_confirmation: bool = False  # a side-effect tool: execute only after an explicit "sí"
    # With `missing`: the calls minus the unstated arguments, so a slot-filling flow can
    # start with what the user did say and ask for the rest.
    partial_calls: tuple[ToolCall, ...] = ()


def _states_date(norm: str, tokens: list[str]) -> bool:
    if _DATE_RE.search(norm):
        return True
    # "10 de dicembre", "December 3": a (possibly misspelt) month next to a day number.
    has_month = any(_similar(t, m) for t in tokens for m in _MONTH_WORDS)
    return has_month and any(t.isdigit() and len(t) <= 2 for t in tokens)


def grounded_args(text: str, world: World) -> dict[str, Any]:
    """Arguments the user's own words support. Station/trail map to ids; others to True."""
    norm = normalize_text(text)
    tokens = _tokens(norm)
    found: dict[str, Any] = {}
    trails = [t for t in world.trails.values() if fuzzy_contains(tokens, _short_name(t.name))]
    if len(trails) == 1:
        found["trail_id"] = trails[0].id
    names = {sid: s.name for sid, s in world.stations.items()}
    station = detect_station(text, names, prefer_last=True)
    if station is None and len(trails) == 1:
        station = trails[0].station
    if station is not None:
        found["station"] = station
    if _states_date(norm, tokens):
        found["date"] = True
    if _VISITOR_RE.search(norm):
        found["visitor_type"] = True
    if _COUNT_RE.search(norm):
        found["group_size"] = found["people_count"] = True
    return found


# Only these arguments are checked: their values cannot be inferred from the question topic.
# Enums such as emergency_type or item are classifications of what the user said.
CHECKED_ARGS = ("station", "trail_id", "date", "visitor_type", "group_size", "people_count")


def guard_route(
    decision: str | None,
    calls: Iterable[ToolCall],
    *,
    user_text: str,
    world: World,
    context_texts: Sequence[str] = (),
    device_station: str | None = None,
) -> RouteGuardResult:
    """Validate the model's tool call against what the user actually said.

    - A required checked argument the user never stated is not trusted: if it is the
      station and the device knows where it is installed, the device station is used;
      otherwise the turn becomes a clarification asking for the missing slots.
    - A station or trail the user did name overrides whatever the model put there.
    - Side-effect tools are flagged for the FSM's explicit confirmation step, so an
      injected instruction can at most produce a confirmation question, never an action.

    `context_texts` (oldest first) are earlier turns or the FSM state summary. They only
    ground, never override: a station the model picked that was mentioned earlier is kept
    (resolves "¿y en la otra?"); one never mentioned is replaced by the most recent one.
    """
    calls = tuple(calls)
    if decision != "call" and not (decision is None and calls):
        return RouteGuardResult(decision, calls)
    stated = grounded_args(user_text, world)  # current message: may override the model
    from_context: dict[str, Any] = {}
    names = {sid: st.name for sid, st in world.stations.items()}
    mentioned: set[str] = set(station_mentions(user_text, names))
    for text in reversed(context_texts):
        mentioned |= set(station_mentions(text, names))
        for name, value in grounded_args(text, world).items():
            from_context.setdefault(name, value)
    fixed: list[ToolCall] = []
    missing: list[str] = []
    for call in calls:
        spec = world.tools.get(call.name)
        if spec is None:
            return RouteGuardResult("clarify", (), ())  # hallucinated tool: never execute
        args = dict(call.arguments)
        unstated: list[str] = []
        for name in spec.parameters.get("required", []):
            if name not in CHECKED_ARGS:
                continue
            if name in ("station", "trail_id") and name in stated:
                args[name] = stated[name]
            elif name == "station" and args.get(name) in mentioned:
                pass  # refers back to a station already in the conversation
            elif name in ("station", "trail_id") and name in from_context:
                args[name] = from_context[name]
            elif name == "station" and device_station is not None:
                args[name] = device_station
            elif name not in stated and name not in from_context:
                unstated.append(name)
        required = set(spec.parameters.get("required", []))
        for name in CHECKED_ARGS:
            if name in required or name not in args:
                continue
            # Optional and unstated: drop it (nothing to ask), never execute it as said.
            if name in ("station", "trail_id") and name in stated:
                args[name] = stated[name]
            elif name in ("station", "trail_id") and name in from_context:
                args[name] = from_context[name]
            elif name not in stated and name not in from_context:
                del args[name]
        missing.extend(unstated)
        kept = {k: v for k, v in args.items() if k not in unstated}
        fixed.append(call.model_copy(update={"arguments": kept}))
    if missing:
        return RouteGuardResult(
            "clarify", (), tuple(dict.fromkeys(missing)), partial_calls=tuple(fixed)
        )
    side_effects = any(world.tools[c.name].has_side_effects for c in fixed if c.name in world.tools)
    return RouteGuardResult(decision or "call", tuple(fixed), (), side_effects)
