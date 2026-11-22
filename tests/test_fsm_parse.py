import pytest

from nevados_bench.fsm.parse import first_json_object, parse_output
from nevados_bench.schemas import Case, Completion, Gold, ToolCall


def case(call_type="route"):
    return Case(
        case_id="c",
        suite="t",
        call_type=call_type,
        fsm_state="ROUTER",
        user_message="x",
        slot_name="group_size" if call_type == "extract" else None,
        gold=Gold(),
    )


ROUTE = case("route")


def test_native_tool_call_with_string_arguments():
    comp = Completion(tool_calls=[{"name": "get_opening_hours", "arguments": '{"station": "a"}'}])
    out = parse_output(comp, ROUTE, "native")
    assert out.parse_ok and out.decision == "call"
    assert out.calls == [ToolCall(name="get_opening_hours", arguments={"station": "a"})]


def test_native_openai_shape_and_dict_arguments():
    raw = {"type": "function", "function": {"name": "list_trails", "arguments": {"station": "b"}}}
    out = parse_output(Completion(tool_calls=[raw]), ROUTE, "native")
    assert out.calls[0].arguments == {"station": "b"}


def test_native_without_call():
    assert parse_output(Completion(content="¿Qué estación?"), ROUTE, "native").decision == "clarify"
    out = parse_output(Completion(content="No puedo ayudar con eso."), ROUTE, "native")
    assert out.parse_ok and out.decision == "none" and out.answer_text


def test_native_malformed_arguments():
    comp = Completion(tool_calls=[{"name": "x", "arguments": "{station:"}])
    out = parse_output(comp, ROUTE, "native")
    assert not out.parse_ok and out.parse_error


@pytest.mark.parametrize(
    ("content", "decision"),
    [
        ('{"tool": "get_entry_fee", "args": {"station": "a", "visitor_type": "nacional"}}', "call"),
        ('{"tool": "none"}', "none"),
        ('{"tool": "clarify", "question": "¿Cuántos son?"}', "clarify"),
    ],
)
def test_uniform_well_formed(content, decision):
    out = parse_output(Completion(content=content), ROUTE, "uniform")
    assert out.parse_ok and out.decision == decision


@pytest.mark.parametrize(
    "content",
    [
        "",
        "hola",
        '{"tool": 3}',
        '{"args": {}}',
        '{"tool": "x", "args": [1]}',
        '{"tool": "clarify"}',
    ],
)
def test_uniform_malformed_never_raises(content):
    out = parse_output(Completion(content=content), ROUTE, "uniform")
    assert not out.parse_ok and out.parse_error


def test_uniform_is_strict_but_free_is_tolerant():
    text = 'Claro, aquí va: {"tool": "list_trails", "args": {"station": "c"}} ¡suerte!'
    assert not parse_output(Completion(content=text), ROUTE, "uniform").parse_ok
    out = parse_output(Completion(content=text), ROUTE, "uniform_free")
    assert out.parse_ok and out.calls[0].name == "list_trails"


def test_first_json_object_skips_invalid_and_handles_strings():
    assert first_json_object('{bad} y luego {"a": "}{", "b": {"c": 1}}') == {
        "a": "}{",
        "b": {"c": 1},
    }
    with pytest.raises(ValueError):
        first_json_object("sin json {")


def test_think_block_is_stripped():
    out = parse_output(Completion(content='<think>hmm</think>{"tool": "none"}'), ROUTE, "uniform")
    assert out.parse_ok and out.decision == "none"


def test_extract():
    ext = case("extract")
    assert parse_output(Completion(content='{"value": 4}'), ext, "native").slot_value == 4
    out = parse_output(Completion(content='{"value": null}'), ext, "uniform")
    assert out.parse_ok and out.slot_value is None
    assert not parse_output(Completion(content='{"valor": 4}'), ext, "uniform").parse_ok
    assert not parse_output(Completion(content="cuatro"), ext, "uniform").parse_ok


def test_answer():
    ans = case("answer")
    out = parse_output(Completion(content=" Abre a las 05:55 [fuente: EST-B-01]. "), ans, "native")
    assert out.parse_ok and out.answer_text == "Abre a las 05:55 [fuente: EST-B-01]."
    assert not parse_output(Completion(content="  "), ans, "native").parse_ok


def test_transport_failures():
    assert parse_output(Completion(timeout=True), ROUTE, "native").parse_error == "timeout"
    assert not parse_output(Completion(http_error="500"), ROUTE, "uniform").parse_ok


def test_native_leaked_tool_call_is_a_parse_failure():
    from nevados_bench.fsm.parse import _parse_route_native
    from nevados_bench.schemas import Completion

    leaked = [
        '<tool_call>{"name": "get_opening_hours", "arguments": {"station": "valle_bruma"}}',
        '{"type": "function", "function": {"name": "get_entry_fee", "arguments": {}}}',
        '[TOOL_CALLS]get_entry_fee[ARGS]{"station": "valle_bruma"}',
    ]
    for content in leaked:
        parsed = _parse_route_native(Completion(content=content))
        assert parsed.parse_ok is False
        assert parsed.decision is None
    plain = _parse_route_native(Completion(content="No puedo ayudarte con eso."))
    assert plain.parse_ok is True and plain.decision == "none"
    question = _parse_route_native(Completion(content="¿Para qué fecha sería la visita?"))
    assert question.parse_ok is True and question.decision == "clarify"
