import json

import pytest

from nevados_bench.fsm import states as S
from nevados_bench.fsm.driver import is_affirmative, is_cancel, run_dialogue
from nevados_bench.schemas import Completion, Dialogue, DialogueTurn, PromptRequest
from nevados_bench.world import load_world


class ScriptedBackend:
    """Returns pre-scripted completions in order and records every request."""

    def __init__(self, completions):
        self.completions = list(completions)
        self.requests: list[PromptRequest] = []

    def complete(self, request: PromptRequest) -> Completion:
        self.requests.append(request)
        return self.completions.pop(0)


def call(mode, name, args):
    if mode == "native":
        return Completion(tool_calls=[{"name": name, "arguments": json.dumps(args)}])
    return Completion(content=json.dumps({"tool": name, "args": args}))


def value(v):
    return Completion(content=json.dumps({"value": v}))


def dialogue(*messages):
    turns = [DialogueTurn(user_message=m, steps=[]) for m in messages]
    return Dialogue(dialogue_id="d1", depth=len(turns), phenomena=[], turns=turns)


@pytest.mark.parametrize("mode", ["native", "uniform"])
def test_slot_filling_confirm_execute(mode):
    world = load_world()
    backend = ScriptedBackend(
        [
            call(mode, "register_visit", {"station": "alto_cenizo"}),
            value("2026-12-03"),
            value(None),  # user did not give the group size
            Completion(content='{"tool": "none"}' if mode != "native" else "Entiendo."),
            value(4),
            value("nacional"),
        ]
    )
    steps = run_dialogue(
        dialogue(
            "Quiero registrar una visita a Alto Cenizo",
            "el 3 de diciembre, o sea 2026-12-03",
            "mmm no sé",
            "somos 4",
            "nacionales",
            "sí, confirmo",
        ),
        backend,
        world,
        mode,
    )
    assert backend.completions == []
    for step in steps:
        S.check_path(step.path)
    assert steps[0].path == ["ROUTER", "VISIT_REGISTRATION", "SLOT_FILLING"]
    assert steps[0].assistant_message == S.SLOT_QUESTIONS["date"]
    # Group size was asked again after the unanswered turn.
    reasks = [s for s in steps if s.note == "reask"]
    assert reasks and reasks[0].assistant_message == S.SLOT_QUESTIONS["group_size"]
    confirm = [s for s in steps if s.state_after == "CONFIRM"]
    assert confirm and "¿Confirmas?" in confirm[0].assistant_message
    last = steps[-1]
    assert last.kind == "code" and last.path == ["CONFIRM", "EXECUTE", "ANSWER"]
    assert last.executed_call.arguments == {
        "station": "alto_cenizo",
        "date": "2026-12-03",
        "group_size": 4,
        "visitor_type": "nacional",
    }
    assert last.tool_result["ok"] and "REG-" in last.assistant_message
    # No side-effect tool ran before confirmation.
    executed = [s for s in steps if s.executed_call is not None]
    assert executed == [last]
    # Extract requests carry the pending slot in the suffix and the flow summary.
    extract_reqs = [s.request for s in steps if s.call_type == "extract"]
    assert all(r.json_schema is not None for r in extract_reqs)
    assert "Trámite en curso: register_visit" in extract_reqs[0].messages[-1]["content"]
    # History grows turn by turn.
    assert len(backend.requests[-1].messages) == 1 + 2 * 4 + 1


def test_intent_switch_from_slot_filling():
    world = load_world()
    backend = ScriptedBackend(
        [
            call("native", "register_visit", {"station": "valle_bruma", "group_size": 3}),
            value(None),
            call("native", "get_opening_hours", {"station": "laguna_espejo"}),
            Completion(content="Abre a las 05:55 [fuente: EST-B-01]."),
        ]
    )
    steps = run_dialogue(
        dialogue("Registra una visita a Valle Bruma para 3", "mejor dime el horario de Laguna"),
        backend,
        world,
        "native",
    )
    switch = steps[-2]
    assert switch.path == ["SLOT_FILLING", "ROUTER", "STATION_INFO"]
    assert switch.executed_call.name == "get_opening_hours"
    answer = steps[-1]
    assert answer.call_type == "answer" and answer.path == ["STATION_INFO", "ANSWER"]
    system = answer.request.messages[0]["content"]
    assert "[EST-B-01]" in system and "[EST-A-01]" not in system
    assert answer.assistant_message.startswith("Abre")


def test_cancel_and_info_tool_missing_argument():
    world = load_world()
    backend = ScriptedBackend(
        [
            call("uniform", "report_emergency", {"station": "refugio_quelital"}),
            call("uniform", "get_entry_fee", {"station": "refugio_quelital"}),
        ]
    )
    steps = run_dialogue(
        dialogue("Hay una emergencia en Quelital", "cancela", "¿cuánto cuesta entrar a Quelital?"),
        backend,
        world,
        "uniform",
    )
    assert steps[1].path == ["SLOT_FILLING", "ROUTER"] and steps[1].kind == "code"
    assert steps[2].path == ["ROUTER", "CLARIFY"]
    assert steps[2].assistant_message == S.SLOT_QUESTIONS["visitor_type"]
    assert all(s.executed_call is None for s in steps)


def test_confirm_correction_then_execute():
    world = load_world()
    args = {
        "station": "laguna_espejo",
        "emergency_type": "hipotermia",
        "people_count": 2,
    }
    backend = ScriptedBackend(
        [
            call("native", "report_emergency", args),
            call("native", "report_emergency", {**args, "people_count": 3}),
        ]
    )
    steps = run_dialogue(
        dialogue("Emergencia: hipotermia, 2 personas, Laguna Espejo", "no, son 3 personas", "sí"),
        backend,
        world,
        "native",
    )
    assert steps[0].path[-1] == "CONFIRM"
    assert steps[1].path == ["CONFIRM", "SLOT_FILLING", "CONFIRM"]
    # The correction route only sees the flow tool.
    assert [t["function"]["name"] for t in steps[1].request.tools] == ["report_emergency"]
    assert steps[-1].executed_call.arguments["people_count"] == 3


def test_parse_failure_and_out_of_scope():
    world = load_world()
    backend = ScriptedBackend([Completion(content="{roto"), Completion(content='{"tool": "none"}')])
    steps = run_dialogue(dialogue("hola", "¿quién ganó el mundial?"), backend, world, "uniform")
    assert steps[0].path == ["ROUTER", "CLARIFY"] and steps[0].note == "parse_error"
    assert steps[1].path == ["CLARIFY", "ROUTER", "OUT_OF_SCOPE"]


def test_keyword_helpers():
    assert is_affirmative("Sí, dale") and is_affirmative("ok")
    assert not is_affirmative("no") and not is_affirmative("sí pero cambia la fecha a otro día")
    assert is_cancel("Cancela eso") and is_cancel("olvídalo")
    assert not is_cancel("somos 4")


# ----------------------------------------------------------------------------- guards


def test_guard_unstated_station_asks_instead_of_executing():
    world = load_world()
    backend = ScriptedBackend([call("uniform", "get_opening_hours", {"station": "alto_cenizo"})])
    steps = run_dialogue(dialogue("¿A qué hora abre la estación?"), backend, world, "uniform",
                         guards=True)  # fmt: skip
    assert len(steps) == 1
    assert steps[0].executed_call is None
    assert steps[0].state_after == S.CLARIFY
    assert steps[0].assistant_message == S.SLOT_QUESTIONS["station"]


def test_guard_device_station_fills_unstated_station():
    world = load_world()
    backend = ScriptedBackend(
        [
            call("uniform", "get_opening_hours", {"station": "alto_cenizo"}),
            Completion(content='{"answer": "No tengo información oficial sobre eso."}'),
        ]
    )
    steps = run_dialogue(dialogue("¿A qué hora abre?"), backend, world, "uniform",
                         guards=True, device_station="valle_bruma")  # fmt: skip
    assert steps[0].executed_call is not None
    assert steps[0].executed_call.arguments["station"] == "valle_bruma"


def test_guard_flow_drops_fabricated_slots_and_asks_for_them():
    world = load_world()
    fabricated = {"station": "laguna_espejo", "date": "2026-11-26", "group_size": 1,
                  "visitor_type": "nacional"}  # fmt: skip
    backend = ScriptedBackend([call("uniform", "register_visit", fabricated)])
    steps = run_dialogue(dialogue("Anóteme pa' visitar Laguna Espejo"), backend, world,
                         "uniform", guards=True)  # fmt: skip
    assert steps[0].slots == {"station": "laguna_espejo"}
    assert steps[0].state_after == S.SLOT_FILLING
    assert steps[0].assistant_message == S.SLOT_QUESTIONS["date"]


def test_without_guards_fabricated_slots_are_kept():
    world = load_world()
    fabricated = {"station": "laguna_espejo", "date": "2026-11-26", "group_size": 1,
                  "visitor_type": "nacional"}  # fmt: skip
    backend = ScriptedBackend([call("uniform", "register_visit", fabricated)])
    steps = run_dialogue(dialogue("Anóteme pa' visitar Laguna Espejo"), backend, world,
                         "uniform")  # fmt: skip
    assert steps[0].state_after == S.CONFIRM  # unchanged r1 behaviour


def test_guard_answer_citing_other_station_is_replaced():
    world = load_world()
    other = next(p for p in world.passages.values() if p.station == "alto_cenizo" and p.values)
    wrong = f"Es {other.values[0]} [fuente: {other.id}]."
    backend = ScriptedBackend(
        [
            call("uniform", "get_station_altitude", {"station": "laguna_espejo"}),
            Completion(content=json.dumps({"answer": wrong})),
        ]
    )
    steps = run_dialogue(dialogue("¿A qué altura está Laguna Espejo?"), backend, world,
                         "uniform", guards=True)  # fmt: skip
    answer = steps[-1]
    assert answer.call_type == "answer"
    assert answer.assistant_message.startswith("No tengo información oficial")
    assert answer.note and "guard_answer" in answer.note


def test_extractive_answer_quotes_passages_without_model_call():
    world = load_world()
    backend = ScriptedBackend([call("uniform", "get_opening_hours", {"station": "valle_bruma"})])
    steps = run_dialogue(dialogue("¿A qué hora abre Valle Bruma?"), backend, world, "uniform",
                         guards=True, answer_mode="extractive")  # fmt: skip
    assert len(backend.requests) == 1  # routing only
    answer = steps[-1]
    assert answer.kind == "code" and answer.note == "extractive"
    first = world.get_passage("EST-C-01")
    assert first.text in answer.assistant_message
    assert "[fuente: EST-C-01]" in answer.assistant_message


def test_guard_ignores_values_only_quoted_by_the_assistant():
    """Regression: an extractive reply quoting a trail let the model's trail_id pass as stated."""
    from nevados_bench.fsm.driver import DialogueRun

    world = load_world()
    args = {"station": "alto_cenizo", "emergency_type": "persona_perdida", "people_count": 1,
            "trail_id": "sendero_ceniza_roja"}  # fmt: skip
    backend = ScriptedBackend([call("uniform", "report_emergency", args)])
    run = DialogueRun(dialogue(), backend, world, "uniform", guards=True)
    run.history += [
        {"role": "user", "content": "¿Qué senderos salen de Alto Cenizo?"},
        {"role": "assistant", "content": "El Sendero Ceniza Roja mide 3740 m. [fuente: X]"},
    ]
    run.turn("Hay una persona perdida en Alto Cenizo, es solo una persona")
    assert run.flow is not None
    assert "trail_id" not in run.flow.slots
    assert run.flow.slots["people_count"] == 1


# ----------------------------------------------------------------------------- corrections


class SlotAwareBackend:
    """Answers extract calls by (user message, requested slot) and route calls in order.

    The extract replies reproduce the r2 Gemma behaviour: asked for the pending slot while
    the visitor corrects another one, it returns a fabricated value for the pending slot.
    """

    def __init__(self, extracts, routes=()):
        self.extracts = dict(extracts)
        self.routes = list(routes)
        self.requests: list[PromptRequest] = []

    def complete(self, request: PromptRequest) -> Completion:
        self.requests.append(request)
        content = request.messages[-1]["content"]
        if "[Dato solicitado]" in content:
            slot = content.split("[Dato solicitado]\n", 1)[1].split(":", 1)[0]
            message = content.rsplit("[Mensaje del usuario]\n", 1)[1]
            return value(self.extracts.get((message, slot)))
        return self.routes.pop(0)


def test_guarded_date_correction_during_slot_filling_is_applied():
    """Regression (dlg-13): the corrected date was lost and the old one executed."""
    world = load_world()
    messages = [
        "Buenas tardes, quisiera registrar una visita a la Estación Laguna Espejo.",
        "Para el viernes 4 de diciembre.",
        "Vamos a ir cuatro personas.",
        "Ay, perdón, cambia la fecha: mejor para el sábado 5 de diciembre.",
        "Todos somos extranjeros.",
        "Sí, perfecto.",
    ]
    backend = SlotAwareBackend(
        {
            (messages[1], "date"): "2026-12-04",
            (messages[2], "group_size"): 4,
            (messages[3], "visitor_type"): "nacional",  # r2: fabricated for the pending slot
            (messages[4], "visitor_type"): "extranjero",
        },
        routes=[
            call("uniform", "register_visit", {"station": "laguna_espejo"}),
            call("uniform", "register_visit", {"station": "laguna_espejo", "date": "2026-12-05",
                                               "group_size": 4}),
        ],
    )  # fmt: skip
    steps = run_dialogue(dialogue(*messages), backend, world, "uniform", guards=True,
                         answer_mode="extractive")  # fmt: skip
    executed = [s.executed_call for s in steps if s.executed_call is not None]
    assert [c.arguments for c in executed] == [
        {"station": "laguna_espejo", "date": "2026-12-05", "group_size": 4,
         "visitor_type": "extranjero"}
    ]  # fmt: skip
    turn = [s for s in steps if s.turn_index == 3]
    # Same call sequence as the gold scripts: extract (value discarded), then flow route.
    assert [(s.call_type, s.note) for s in turn] == [
        ("extract", "correction_detected"),
        ("route", "correction"),
    ]
    assert "visitor_type" not in turn[0].slots
    assert turn[-1].assistant_message == S.SLOT_QUESTIONS["visitor_type"]


def test_guarded_station_correction_during_slot_filling_is_applied():
    """Regression (dlg-18): the corrected station was lost and the old one executed."""
    world = load_world()
    messages = [
        "Quiero reportar una emergencia en la Estación Laguna Espejo.",
        "Mi amigo se cayó y se lastimó la pierna.",
        "Perdón, me corrijo: no estamos en Laguna Espejo, estamos en Alto Cenizo.",
        "Solo él, una persona.",
        "Sí, envíalo.",
    ]
    backend = SlotAwareBackend(
        {
            (messages[1], "emergency_type"): "lesion",
            (messages[2], "people_count"): 1,  # r2: fabricated for the pending slot
            (messages[3], "people_count"): 1,
        },
        routes=[
            call("uniform", "report_emergency", {"station": "laguna_espejo"}),
            # Even if the model restates the old station, the stated one wins (route guard).
            call("uniform", "report_emergency", {"station": "laguna_espejo",
                                                 "emergency_type": "lesion"}),
        ],
    )  # fmt: skip
    steps = run_dialogue(dialogue(*messages), backend, world, "uniform", guards=True,
                         answer_mode="extractive")  # fmt: skip
    executed = [s.executed_call for s in steps if s.executed_call is not None]
    assert [c.arguments for c in executed] == [
        {"station": "alto_cenizo", "emergency_type": "lesion", "people_count": 1}
    ]
    assert [s.note for s in steps if s.turn_index == 2] == ["correction_detected", "correction"]


def _visit_until_visitor_type(extra_turn, extracts, routes):
    world = load_world()
    messages = ["Quiero registrar una visita a Valle Bruma para el 3 de diciembre, somos 4",
                extra_turn]  # fmt: skip
    backend = SlotAwareBackend(
        extracts,
        routes=[call("uniform", "register_visit", {"station": "valle_bruma",
                                                   "date": "2026-12-03", "group_size": 4}),
                *routes],
    )  # fmt: skip
    steps = run_dialogue(dialogue(*messages), backend, world, "uniform", guards=True,
                         answer_mode="extractive")  # fmt: skip
    return [s for s in steps if s.turn_index == 1]


@pytest.mark.parametrize(
    "message",
    [
        "¿Cuánto se demora uno haciendo el Sendero Glaciar Viejo?",
        "¿Hay dónde cargar el celular en la Estación Laguna Espejo?",
    ],
)
def test_info_question_naming_a_place_mid_flow_is_not_a_correction(message):
    """Coordinator regression: an information question is an intent switch, not a new
    station for the flow (no cue; and a trail never implies a station)."""
    tool = "get_trail_details" if "Sendero" in message else "get_station_services"
    args = {"trail_id": "sendero_glaciar_viejo"} if "Sendero" in message else {
        "station": "laguna_espejo"}  # fmt: skip
    turn = _visit_until_visitor_type(message, {(message, "visitor_type"): None},
                                     [call("uniform", tool, args)])  # fmt: skip
    assert turn[0].note == "slot_not_extracted"
    assert turn[1].executed_call.name == tool
    assert all("correction" not in (s.note or "") for s in turn)


@pytest.mark.parametrize(
    ("message", "station"),
    [("Valle bruma.", "valle_bruma"), ("Estamos en la estacón refugio quelital.",
                                       "refugio_quelital")],
)  # fmt: skip
def test_plain_answer_to_pending_station_is_a_fill(message, station):
    world = load_world()
    backend = SlotAwareBackend(
        {(message, "station"): station},
        routes=[call("uniform", "report_emergency", {"emergency_type": "lesion"})],
    )
    steps = run_dialogue(dialogue("Hay un herido, se fracturó el brazo", message), backend,
                         world, "uniform", guards=True)  # fmt: skip
    assert steps[-1].call_type == "extract" and steps[-1].note is None
    assert steps[-1].slots["station"] == station


def test_answering_the_pending_slot_with_a_cue_is_not_a_correction():
    message = "Perdón, somos extranjeros"
    turn = _visit_until_visitor_type(message, {(message, "visitor_type"): "extranjero"}, [])
    assert [(s.call_type, s.note) for s in turn] == [("extract", None)]
    assert turn[0].slots["visitor_type"] == "extranjero"


# ----------------------------------------------------------------------------- speedup flags


def _mid_flow_run(**kw):
    world = load_world()
    backend = ScriptedBackend(
        [
            call("uniform", "register_visit", {"station": "alto_cenizo"}),
            value(None),
            Completion(content='{"tool": "none"}'),
        ]
    )
    run_dialogue(
        dialogue("Quiero registrar una visita a Alto Cenizo", "mmm no sé"),
        backend, world, "uniform", **kw,
    )  # fmt: skip
    return world, backend.requests


def test_route_scope_default_keeps_every_router_tool_mid_flow():
    world, requests = _mid_flow_run()
    reroute = requests[-1].json_schema["anyOf"]
    names = [o["properties"]["tool"]["const"] for o in reroute][:-2]
    assert names == S.visible_tools(world, S.ROUTER)


def test_route_scope_state_exposes_only_slot_filling_tools():
    world, requests = _mid_flow_run(route_scope="state")
    reroute = requests[-1].json_schema["anyOf"]
    names = [o["properties"]["tool"]["const"] for o in reroute][:-2]
    assert names == S.visible_tools(world, S.SLOT_FILLING) == ["report_emergency", "register_visit"]
    # The first routing call (state ROUTER) is unaffected.
    first = [o["properties"]["tool"]["const"] for o in requests[0].json_schema["anyOf"]][:-2]
    assert first == S.visible_tools(world, S.ROUTER)


def test_extract_layout_reaches_extract_requests():
    from nevados_bench.fsm.prompts import render_slot_catalog

    world, requests = _mid_flow_run(extract_layout="shared_prefix")
    extract = requests[1]
    assert render_slot_catalog(world) in extract.messages[0]["content"]
    _, default_requests = _mid_flow_run()
    assert render_slot_catalog(world) not in default_requests[1].messages[0]["content"]
    assert requests[0] == default_requests[0] and requests[2] == default_requests[2]
