"""Hand-made world, cases and record builders shared by the scoring and report tests."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from nevados_bench.schemas import (
    Case,
    Completion,
    Dialogue,
    DialogueTurn,
    GazetteerEntry,
    Gold,
    ParsedOutput,
    Passage,
    RequestRecord,
    ToolCall,
    ToolSpec,
)
from nevados_bench.values import ABSTAIN_ES

STATION = {"type": "string", "enum": ["estacion_a", "estacion_b"]}

TOOLS = {
    t.name: t
    for t in [
        ToolSpec(
            name="check_weather",
            description="Pronóstico",
            parameters={
                "type": "object",
                "properties": {"station": STATION, "date": {"type": "string", "format": "date"}},
                "required": ["station", "date"],
                "additionalProperties": False,
            },
        ),
        ToolSpec(
            name="check_weather_v2",
            description="Pronóstico (duplicado)",
            near_duplicate_of="check_weather",
            parameters={
                "type": "object",
                "properties": {"station": STATION, "date": {"type": "string", "format": "date"}},
                "required": ["station", "date"],
            },
        ),
        ToolSpec(
            name="register_visit",
            description="Registrar visita",
            has_side_effects=True,
            parameters={
                "type": "object",
                "properties": {
                    "station": STATION,
                    "visitors": {"type": "integer"},
                    "name": {"type": "string"},
                },
                "required": ["station", "visitors", "name"],
            },
        ),
        ToolSpec(
            name="call_emergency",
            description="Emergencia",
            has_side_effects=True,
            safety=True,
            parameters={
                "type": "object",
                "properties": {"station": STATION},
                "required": ["station"],
            },
        ),
    ]
}
VISIBLE = ["check_weather", "check_weather_v2", "register_visit", "call_emergency"]

PASSAGES = {
    p.id: p
    for p in [
        Passage(
            id="P_A_HOURS",
            station="estacion_a",
            field="opening_hours",
            text="La Estación A abre a las 6:40 a. m. y cierra a las 4:15 p. m.",
            values=["06:40", "16:15"],
        ),
        Passage(
            id="P_B_HOURS",
            station="estacion_b",
            field="opening_hours",
            text="La Estación B abre a las 7:10 a. m. y cierra a las 5:30 p. m.",
            values=["07:10", "17:30"],
        ),
        Passage(
            id="P_A_EMERG",
            station="estacion_a",
            field="emergency_phone",
            text="El número de emergencia del parque es 3105550199.",
            values=["3105550199"],
            safety=True,
            prior_values=["123"],
        ),
        Passage(
            id="P_A_ALT",
            station="estacion_a",
            field="altitude_m",
            text="La Estación A está a 4.137 m de altitud.",
            values=["4137"],
        ),
        Passage(
            id="P_B_GEAR",
            station="estacion_b",
            field="gear",
            text="En la Estación B lleve bastones y poncho.",
            values=["poncho"],
        ),
    ]
}
GAZETTEER = [
    GazetteerEntry(value=v, passage_id=p.id, station=p.station, field=p.field)
    for p in PASSAGES.values()
    for v in p.values
]


@dataclass
class FakeWorld:
    tools: dict[str, ToolSpec] = field(default_factory=lambda: dict(TOOLS))
    passages: list[Passage] = field(default_factory=lambda: list(PASSAGES.values()))
    gazetteer: list[GazetteerEntry] = field(default_factory=lambda: list(GAZETTEER))


def route_case(case_id: str, gold: Gold, **kw: Any) -> Case:
    base: dict[str, Any] = {
        "case_id": case_id,
        "suite": "fc_core",
        "call_type": "route",
        "fsm_state": "ROUTER",
        "user_message": "¿Qué clima habrá en la estación A el 2026-11-20?",
        "tool_names": VISIBLE,
        "context_level": "1k",
        "gold": gold,
    }
    base.update(kw)
    return Case(**base)


def answer_case(case_id: str, gold: Gold, passage_ids: list[str], **kw: Any) -> Case:
    base: dict[str, Any] = {
        "case_id": case_id,
        "suite": "grounded_qa",
        "call_type": "answer",
        "fsm_state": "ANSWER",
        "user_message": "¿A qué hora abre la Estación A?",
        "passage_ids": passage_ids,
        "context_level": "1k",
        "gold": gold,
    }
    base.update(kw)
    return Case(**base)


WEATHER_CALL = ToolCall(
    name="check_weather", arguments={"station": "estacion_a", "date": "2026-11-20"}
)

ROUTE_CASES = [
    route_case("fc_call", Gold(decision="call", calls=[WEATHER_CALL]), strata=["direct"]),
    route_case(
        "fc_none",
        Gold(decision="none"),
        user_message="¿Cuál es la capital de Francia?",
        strata=["paraphrased"],
    ),
    route_case(
        "fc_clarify",
        Gold(
            decision="clarify",
            calls=[
                ToolCall(name="register_visit", arguments={"station": "estacion_a", "name": "Ana"})
            ],
            missing_required=["visitors"],
        ),
        user_message="Quiero registrar mi visita a la estación A, soy Ana.",
    ),
    route_case(
        "fc_register",
        Gold(
            decision="call",
            calls=[
                ToolCall(
                    name="register_visit",
                    arguments={"station": "estacion_b", "visitors": 3, "name": "Ana"},
                )
            ],
        ),
        user_message="Registra 3 personas en la estación B a nombre de Ana.",
        tags={"tools_n": 4},
    ),
]
ANSWER_CASES = [
    answer_case(
        "qa_hours",
        Gold(
            answerable=True,
            gold_values=["06:40"],
            gold_passage_id="P_A_HOURS",
            lure_values=["07:10"],
        ),
        ["P_B_HOURS", "P_A_HOURS"],
        tags={"question_type": "schedule", "gold_position": "end", "distractors_n": 1},
    ),
    answer_case(
        "qa_unans",
        Gold(answerable=False, lure_values=["07:10"]),
        ["P_B_HOURS"],
        user_message="¿A qué hora abre la Estación C?",
        tags={"question_type": "schedule"},
    ),
    answer_case(
        "qa_emerg",
        Gold(
            answerable=True,
            gold_values=["3105550199"],
            gold_passage_id="P_A_EMERG",
            prior_values=["123"],
        ),
        ["P_A_EMERG"],
        user_message="¿Cuál es el número de emergencia?",
        tags={"safety": True, "question_type": "safety"},
    ),
]
EXTRACT_CASES = [
    Case(
        case_id="ex_visitors",
        suite="fc_core",
        call_type="extract",
        fsm_state="SLOT_FILLING",
        user_message="Somos 4.",
        slot_name="visitors",
        gold=Gold(slot_name="visitors", slot_value=4),
    )
]

ORACLE_ANSWERS = {
    "qa_hours": "La Estación A abre a las 6:40 a. m. [fuente: P_A_HOURS]",
    "qa_unans": ABSTAIN_ES,
    "qa_emerg": "El número de emergencia es 3105550199. [fuente: P_A_EMERG]",
}
WRONG_ANSWERS = {
    "qa_hours": "Abre a las 7:10 a. m. [fuente: P_B_HOURS]",
    "qa_unans": "Abre a las 7:10 a. m.",
    "qa_emerg": "Llame al 123 de inmediato.",
}


def completion(**kw: Any) -> Completion:
    base: dict[str, Any] = {
        "content": "",
        "finish_reason": "stop",
        "ttft_ms": 100.0,
        "ttfc_ms": 120.0,
        "total_ms": 1000.0,
        "cache_n": 0,
        "prompt_n": 800,
        "prompt_ms": 600.0,
        "prompt_tps": 1333.3,
        "predicted_n": 20,
        "predicted_ms": 350.0,
        "predicted_tps": 57.1,
    }
    base.update(kw)
    return Completion(**base)


def record(
    case: Case | None = None, parsed: ParsedOutput | None = None, **kw: Any
) -> RequestRecord:
    base: dict[str, Any] = {
        "run_id": "run1",
        "batch": "B2",
        "suite": case.suite if case else "speed",
        "case_id": case.case_id if case else "speed_0",
        "model_id": "model-x",
        "gguf_file": "x.gguf",
        "quant": "Q4_K_M",
        "profile": "phone-tight",
        "threads": 3,
        "ctx_size": 12288,
        "fc_mode": "uniform",
        "ts": "2026-11-14T00:00:00Z",
        "call_type": case.call_type if case else "answer",
        "fsm_state": case.fsm_state if case else None,
        "context_level": case.context_level if case else "1k",
        "tools_n": len(case.tool_names) if case else 0,
        "tags": dict(case.tags) if case else {},
        "completion": kw.pop("completion", None) or completion(),
        "parsed": parsed,
        "mem_peak": 2 * 1024**3,
    }
    base.update(kw)
    return RequestRecord(**base)


def call_output(*calls: ToolCall) -> ParsedOutput:
    return ParsedOutput(parse_ok=True, decision="call", calls=list(calls))


def decision_output(decision: str) -> ParsedOutput:
    return ParsedOutput(parse_ok=True, decision=decision)  # type: ignore[arg-type]


def answer_output(text: str) -> ParsedOutput:
    return ParsedOutput(parse_ok=True, answer_text=text)


def oracle_output(case: Case) -> ParsedOutput:
    if case.call_type == "route":
        if case.gold.decision == "call":
            return call_output(*case.gold.calls)
        return decision_output(case.gold.decision or "none")
    if case.call_type == "extract":
        return ParsedOutput(parse_ok=True, slot_value=case.gold.slot_value)
    return answer_output(ORACLE_ANSWERS[case.case_id])


def wrong_output(case: Case) -> ParsedOutput:
    if case.call_type == "route":
        if case.gold.decision == "call":
            return decision_output("none")
        return call_output(
            ToolCall(
                name="register_visit",
                arguments={"station": "estacion_a", "visitors": 2, "name": "X"},
            )
        )
    if case.call_type == "extract":
        return ParsedOutput(parse_ok=True, slot_value=99)
    return answer_output(WRONG_ANSWERS[case.case_id])


PARTIAL_REGISTER = ToolCall(
    name="register_visit", arguments={"station": "estacion_a", "name": "Ana"}
)


def make_dialogue() -> Dialogue:
    """Two turns: slot filling (route + extract), then confirmation (route with side effect)."""
    register = ToolCall(
        name="register_visit", arguments={"station": "estacion_a", "visitors": 4, "name": "Ana"}
    )
    step_route = Case(
        case_id="d1_t0_s0",
        suite="dialogues",
        call_type="route",
        fsm_state="ROUTER",
        user_message="Quiero registrar una visita a la estación A, soy Ana.",
        tool_names=VISIBLE,
        # Flow start (dialogue style): gold call holds the slots given so far.
        gold=Gold(
            decision="call",
            calls=[PARTIAL_REGISTER],
            missing_required=["visitors"],
            next_state="SLOT_FILLING",
        ),
        tags={"phenomenon": "slot_filling", "side_effect_pending": True},
    )
    step_extract = Case(
        case_id="d1_t0_s1",
        suite="dialogues",
        call_type="extract",
        fsm_state="SLOT_FILLING",
        user_message="Somos 4.",
        slot_name="visitors",
        gold=Gold(slot_name="visitors", slot_value=4, next_state="CONFIRM"),
        tags={"phenomenon": "slot_filling"},
    )
    step_confirm = Case(
        case_id="d1_t1_s0",
        suite="dialogues",
        call_type="route",
        fsm_state="CONFIRM",
        user_message="Sí, confirmo.",
        tool_names=VISIBLE,
        gold=Gold(decision="call", calls=[register], next_state="EXECUTE"),
        tags={"phenomenon": "correction"},
    )
    return Dialogue(
        dialogue_id="d1",
        depth=3,
        phenomena=["slot_filling", "correction"],
        expected_executions=[register],
        turns=[
            DialogueTurn(
                user_message="Quiero registrar una visita. Somos 4.",
                steps=[step_route, step_extract],
            ),
            DialogueTurn(user_message="Sí, confirmo.", steps=[step_confirm]),
        ],
    )
