import json

import pytest

from nevados_bench.batches import Session, run_free_dialogues
from nevados_bench.config import load_models
from nevados_bench.runner.writer import RecordWriter
from nevados_bench.schemas import Completion, Dialogue, DialogueTurn
from nevados_bench.world import load_world


class RouteBackend:
    """Always routes to a read-only tool, so every turn makes one model call."""

    def complete(self, request):
        return Completion(
            content=json.dumps({"tool": "get_station_hours", "args": {"station": "alto_cenizo"}}),
            predicted_n=12,
        )


def make_session(tmp_path):
    model = next(m for m in load_models() if m.id == "gemma4-e2b")
    writer = RecordWriter(tmp_path / "requests.jsonl")
    writer.open()
    return Session(
        run_id="t",
        batch="B7",
        model=model,
        profile_name="phone-tight",
        world=load_world(),
        client=RouteBackend(),
        writer=writer,
        done=set(),
        identity={
            "run_id": "t",
            "batch": "B7",
            "model_id": model.id,
            "gguf_file": "x.gguf",
            "quant": "Q4_K_M",
            "profile": "phone-tight",
            "threads": 3,
            "ctx_size": 4096,
        },
    )


@pytest.mark.parametrize(
    ("kwargs", "arm"),
    [
        ({}, "free_run"),
        ({"guards": True}, "free_run_guarded"),
        ({"answer_mode": "extractive"}, "free_run_extractive"),
    ],
)
def test_every_record_carries_the_arm(tmp_path, kwargs, arm):
    """Regression: model-call records were stamped `free_run` whatever the arm."""
    session = make_session(tmp_path)
    turns = [DialogueTurn(user_message="¿A qué hora abre Alto Cenizo?", steps=[])]
    dialogue = Dialogue(dialogue_id="d1", depth=1, phenomena=[], turns=turns)

    run_free_dialogues(session, [dialogue], "uniform", **kwargs)
    session.writer.close()

    records = [json.loads(line) for line in (tmp_path / "requests.jsonl").read_text().splitlines()]
    assert any(r["tags"]["kind"] == "llm" for r in records)
    assert {r["arm"] for r in records} == {arm}


class ConfirmBackend:
    """Routes to a side-effect tool so the dialogue also produces code-only steps."""

    def complete(self, request):
        return Completion(
            content=json.dumps(
                {
                    "tool": "register_visit",
                    "args": {
                        "station": "alto_cenizo",
                        "date": "2026-12-03",
                        "group_size": 4,
                        "visitor_type": "nacional",
                    },
                }
            ),
            predicted_n=20,
        )


@pytest.mark.parametrize("kwargs", [{}, {"guards": True}, {"answer_mode": "extractive"}])
def test_code_steps_are_recorded_with_the_arm(tmp_path, kwargs):
    """Regression: code-only steps crashed with a duplicate `arm` keyword."""
    session = make_session(tmp_path)
    session.client = ConfirmBackend()
    messages = ["Quiero registrar una visita a Alto Cenizo el 2026-12-03, somos 4 nacionales"]
    messages += ["sí, confirmo", "no, cancela"]
    turns = [DialogueTurn(user_message=m, steps=[]) for m in messages]
    dialogue = Dialogue(dialogue_id="d2", depth=len(turns), phenomena=[], turns=turns)

    run_free_dialogues(session, [dialogue], "uniform", **kwargs)
    session.writer.close()

    records = [json.loads(line) for line in (tmp_path / "requests.jsonl").read_text().splitlines()]
    assert any(r["tags"]["kind"] == "code" for r in records)
    assert len({r["arm"] for r in records}) == 1
