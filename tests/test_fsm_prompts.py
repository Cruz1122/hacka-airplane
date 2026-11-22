import json

import pytest
from jsonschema import Draft202012Validator

from nevados_bench.fsm.prompts import build_request, estimate_request_tokens
from nevados_bench.schemas import CONTEXT_LEVEL_TOKENS, Case, Gold
from nevados_bench.values import ABSTAIN_EN, ABSTAIN_ES
from nevados_bench.world import load_world

TOOLS = ["get_opening_hours", "get_entry_fee", "register_visit"]


@pytest.fixture(scope="module")
def world():
    return load_world()


def make_case(call_type="route", **kw):
    defaults = {
        "case_id": "c1",
        "suite": "test",
        "call_type": call_type,
        "fsm_state": "ROUTER",
        "user_message": "¿A qué hora abre Laguna Espejo?",
        "gold": Gold(),
    }
    if call_type == "route":
        defaults["tool_names"] = TOOLS
    defaults.update(kw)
    return Case(**defaults)


def _prefix(request):
    return json.dumps(
        {"messages": request.messages[:-1], "tools": request.tools, "schema": request.json_schema},
        ensure_ascii=False,
        sort_keys=True,
    )


def test_route_native_shape(world):
    req = build_request(make_case(), world, "native")
    assert req.tool_choice == "auto" and req.json_schema is None
    assert [t["function"]["name"] for t in req.tools] == TOOLS
    system = req.messages[0]["content"]
    assert "sin usar herramientas" in system and "pregunta" in system
    assert req.messages[-1] == {"role": "user", "content": "¿A qué hora abre Laguna Espejo?"}


def test_route_uniform_shape(world):
    req = build_request(make_case(), world, "uniform")
    assert req.tools is None and req.tool_choice == "none"
    Draft202012Validator.check_schema(req.json_schema)
    validator = Draft202012Validator(req.json_schema)
    assert validator.is_valid({"tool": "get_opening_hours", "args": {"station": "valle_bruma"}})
    assert validator.is_valid({"tool": "none"})
    assert validator.is_valid({"tool": "clarify", "question": "¿Qué estación?"})
    assert not validator.is_valid({"tool": "get_trail_details", "args": {}})
    assert not validator.is_valid({"tool": "get_opening_hours", "args": {"station": "x"}})
    assert len(req.json_schema["anyOf"]) == len(TOOLS) + 2
    for name in TOOLS:
        assert f"- {name}(" in req.messages[0]["content"]


def test_route_uniform_free_has_same_prompt_without_schema(world):
    uniform = build_request(make_case(), world, "uniform")
    free = build_request(make_case(), world, "uniform_free")
    assert free.json_schema is None and free.tools is None
    assert free.messages == uniform.messages


@pytest.mark.parametrize("mode", ["native", "uniform", "uniform_free"])
def test_extract_same_in_all_modes(world, mode):
    case = make_case("extract", fsm_state="SLOT_FILLING", slot_name="group_size")
    req = build_request(case, world, mode)
    assert req.tools is None
    assert req.json_schema["properties"]["value"]["anyOf"][1] == {"type": "null"}
    validator = Draft202012Validator(req.json_schema)
    assert validator.is_valid({"value": 4}) and validator.is_valid({"value": None})
    assert not validator.is_valid({"value": "cuatro"})
    assert req == build_request(case, world, "native")


def test_extract_enum_slot_lists_values(world):
    case = make_case("extract", slot_name="station", user_message="a la laguna")
    req = build_request(case, world, "uniform")
    assert "laguna_espejo" in req.messages[-1]["content"]


@pytest.mark.parametrize("mode", ["native", "uniform", "uniform_free"])
def test_answer_shape(world, mode):
    case = make_case("answer", passage_ids=["EST-B-01", "EST-C-03"])
    req = build_request(case, world, mode)
    assert req.tools is None and req.json_schema is None and req.tool_choice is None
    system = req.messages[0]["content"]
    for needle in (ABSTAIN_ES, ABSTAIN_EN, "[fuente: ID]", "[EST-B-01]", "[EST-C-03]"):
        assert needle in system
    assert system.index("[EST-B-01]") < system.index("[EST-C-03]")


def test_bundle_prefix_is_byte_identical(world):
    passages = ["EST-A-03", "EST-B-17", "PAR-02"]
    questions = ["¿Altitud de Alto Cenizo?", "What is the rescue line?", "¿Teléfono de Laguna?"]
    for call_type in ("answer", "route"):
        for level in (None, "2k"):
            reqs = [
                build_request(
                    make_case(
                        call_type,
                        case_id=f"q{i}",
                        user_message=q,
                        passage_ids=passages,
                        bundle_id="b1",
                        context_level=level,
                        language="en" if q.startswith("What") else "es",
                    ),
                    world,
                    "native",
                )
                for i, q in enumerate(questions)
            ]
            assert len({_prefix(r) for r in reqs}) == 1
            assert len({r.messages[-1]["content"] for r in reqs}) == 3


@pytest.mark.parametrize("level", list(CONTEXT_LEVEL_TOKENS))
def test_context_level_padding(world, level):
    case = make_case("answer", passage_ids=["EST-A-03", "EST-D-02"], context_level=level)
    req = build_request(case, world, "native")
    estimate = estimate_request_tokens(req)
    target = CONTEXT_LEVEL_TOKENS[level]
    assert target * 0.85 <= estimate <= target * 1.1, (level, estimate)
    system = req.messages[0]["content"]
    # Real passages keep their relative order and stay inside the context.
    assert system.index("[EST-A-03]") < system.index("[EST-D-02]")
    assert build_request(case, world, "native") == req


def test_history_and_state_summary_in_suffix(world):
    history = [
        {"role": "user", "content": "Quiero registrar una visita"},
        {"role": "assistant", "content": "¿A qué estación?"},
    ]
    case = make_case(history=history, state_summary="Trámite en curso: register_visit.")
    req = build_request(case, world, "native")
    assert req.messages[1:3] == history
    last = req.messages[-1]["content"]
    assert "Trámite en curso" in last and last.endswith("¿A qué hora abre Laguna Espejo?")
    assert "Trámite en curso" not in req.messages[0]["content"]


def test_sampling_overrides(world):
    req = build_request(make_case(), world, "native", sampling={"temperature": 0.7, "min_p": 0.1})
    assert req.temperature == 0.7 and req.extra_body == {"min_p": 0.1}


def test_unknown_tool_rejected(world):
    with pytest.raises(ValueError):
        build_request(make_case(tool_names=["nope"]), world, "native")


def test_flow_tools_accept_partial_calls(world):
    req = build_request(make_case(), world, "uniform")
    validator = Draft202012Validator(req.json_schema)
    assert validator.is_valid({"tool": "register_visit", "args": {"station": "alto_cenizo"}})
    assert validator.is_valid({"tool": "register_visit", "args": {}})
    # Informational tools still require their arguments.
    assert not validator.is_valid({"tool": "get_entry_fee", "args": {"station": "alto_cenizo"}})
    # The world spec keeps required for code-side slot filling.
    assert world.tools["register_visit"].parameters["required"]
    assert world.missing_required("register_visit", {"station": "alto_cenizo"}) == [
        "date",
        "group_size",
        "visitor_type",
    ]
    native = {
        t["function"]["name"]: t["function"]["parameters"]
        for t in build_request(make_case(), world, "native").tools
    }
    assert "required" not in native["register_visit"]
    assert native["get_entry_fee"]["required"] == ["station", "visitor_type"]


def test_partial_call_rule_text(world):
    for mode in ("native", "uniform"):
        system = build_request(make_case(), world, mode).messages[0]["content"]
        assert "solo con los datos que el usuario dio" in system
        assert "Nunca inventes un valor" in system
        assert "Consultas de información" in system
    system = build_request(make_case(), world, "uniform").messages[0]["content"]
    line = next(x for x in system.splitlines() if x.startswith("- register_visit("))
    assert "admite datos parciales" in line
    line = next(x for x in system.splitlines() if x.startswith("- get_entry_fee("))
    assert "admite datos parciales" not in line


# ----------------------------------------------------------------------------- extract layout

# sha256 of the default requests below, pinned before the opt-in layouts were added. The
# fine-tuning data is generated from the default prompts: they must stay byte-identical.
DEFAULT_PROMPTS_SHA256 = "4f156bced04c78a887f0bc1f6a9f8c2ff0b1fb741a6bb7ccce8956ef17e4f6f5"


def _golden_cases():
    hist = [
        {"role": "user", "content": "Quiero registrar una visita a Alto Cenizo"},
        {"role": "assistant", "content": "¿Para qué fecha? Indícala como AAAA-MM-DD."},
    ]
    summary = (
        "Trámite en curso: register_visit.\nDatos ya recibidos: station=alto_cenizo.\n"
        "Dato pendiente: date."
    )
    specs = [
        ("route", {"tool_names": ["get_opening_hours", "register_visit", "report_emergency"]}),
        ("route", {"tool_names": ["register_visit"], "history": hist, "state_summary": summary}),
        ("extract", {"slot_name": "date", "history": hist, "state_summary": summary}),
        ("extract", {"slot_name": "station"}),
        ("extract", {"slot_name": "visitor_type", "history": hist}),
        ("extract", {"slot_name": "emergency_type", "state_summary": summary}),
        ("answer", {"passage_ids": ["EST-B-01", "EST-C-01"], "state_summary": "Resultado: x=1"}),
    ]
    return [
        Case(
            case_id=f"g{i}",
            suite="t",
            call_type=ct,
            fsm_state="ROUTER",
            user_message="el 5 de diciembre",
            gold=Gold(),
            **kw,
        )
        for i, (ct, kw) in enumerate(specs)
    ]


def _digest(world, **kw):
    import hashlib

    blob = [
        build_request(case, world, mode, **kw).model_dump(mode="json")
        for case in _golden_cases()
        for mode in ("native", "uniform", "free")
    ]
    text = json.dumps(blob, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(text.encode()).hexdigest()


def test_default_prompts_are_unchanged(world):
    assert _digest(world) == DEFAULT_PROMPTS_SHA256
    assert _digest(world, extract_layout="default") == DEFAULT_PROMPTS_SHA256


def test_shared_prefix_extracts_share_the_system_message(world):
    slots = ["station", "date", "group_size", "visitor_type", "emergency_type", "people_count"]
    reqs = {
        s: build_request(
            make_case("extract", slot_name=s, state_summary="x"),
            world,
            "uniform",
            extract_layout="shared_prefix",
        )
        for s in slots
    }
    systems = {r.messages[0]["content"] for r in reqs.values()}
    assert len(systems) == 1
    system = systems.pop()
    default = build_request(make_case("extract", slot_name="date"), world, "uniform")
    assert system.startswith(default.messages[0]["content"])  # same rules, catalog appended
    for slot in slots:
        assert f"- {slot}: " in system
        suffix = reqs[slot].messages[-1]["content"]
        assert f"[Dato solicitado]\n{slot}\n\n[Mensaje del usuario]" in suffix
        assert "Valores permitidos" not in suffix
        # The output contract is unchanged.
        assert (
            reqs[slot].json_schema
            == build_request(make_case("extract", slot_name=slot), world, "uniform").json_schema
        )


def test_extract_layout_does_not_touch_route_or_answer(world):
    for case in _golden_cases():
        if case.call_type == "extract":
            continue
        assert build_request(case, world, "uniform", extract_layout="shared_prefix") == (
            build_request(case, world, "uniform")
        )
