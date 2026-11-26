import pytest

from nevados_bench.fsm import states as S
from nevados_bench.world import load_world


def test_every_state_has_outgoing_transitions():
    assert set(S.TRANSITIONS) == set(S.STATES)
    for targets in S.TRANSITIONS.values():
        assert targets <= set(S.STATES)


def test_diagram_edges_present():
    edges = [
        ("ROUTER", "VISIT_REGISTRATION"),
        ("VISIT_REGISTRATION", "SLOT_FILLING"),
        ("EMERGENCY", "SLOT_FILLING"),
        ("SLOT_FILLING", "SLOT_FILLING"),
        ("SLOT_FILLING", "CONFIRM"),
        ("SLOT_FILLING", "ROUTER"),
        ("CONFIRM", "EXECUTE"),
        ("CONFIRM", "SLOT_FILLING"),
        ("EXECUTE", "ANSWER"),
        ("ANSWER", "ROUTER"),
    ]
    for src, dst in edges:
        assert S.can_transition(src, dst)
    assert not S.can_transition("ROUTER", "EXECUTE")
    assert not S.can_transition("SLOT_FILLING", "EXECUTE")


def test_check_path():
    S.check_path(["ROUTER", "VISIT_REGISTRATION", "SLOT_FILLING", "CONFIRM"])
    with pytest.raises(ValueError):
        S.check_path(["ROUTER", "EXECUTE"])


def test_visible_tools():
    world = load_world()
    assert S.visible_tools(world, "ROUTER") == world.base_tools
    assert len(S.visible_tools(world, "ROUTER", include_clones=True)) == 48
    assert S.visible_tools(world, "SLOT_FILLING") == ["report_emergency", "register_visit"]
    for state in S.TOPIC_STATES:
        assert S.visible_tools(world, state)


def test_required_slots_match_tool_schemas():
    world = load_world()
    for tool, slots in S.REQUIRED_SLOTS.items():
        assert world.tools[tool].parameters["required"] == slots
        for slot in slots:
            assert slot in S.SLOT_QUESTIONS
