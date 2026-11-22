from __future__ import annotations

import json
import threading
from http.server import ThreadingHTTPServer

import httpx
import pytest

from nevados_bench.app.server import MAX_MESSAGE_CHARS, LiveSession, make_handler
from nevados_bench.fsm import states as S
from nevados_bench.schemas import Completion, PromptRequest
from nevados_bench.world import load_world


class ScriptedBackend:
    def __init__(self, completions: list[Completion]) -> None:
        self.completions = list(completions)
        self.requests: list[PromptRequest] = []

    def complete(self, request: PromptRequest) -> Completion:
        self.requests.append(request)
        return self.completions.pop(0)


def route(name: str, args: dict) -> Completion:
    return Completion(content=json.dumps({"tool": name, "args": args}))


def test_live_session_keeps_state_across_turns_and_resets() -> None:
    backend = ScriptedBackend([route("register_visit", {"station": "valle_bruma"})])
    session = LiveSession(backend, load_world(), device_station="valle_bruma")
    first = session.chat("Quiero registrar una visita")
    assert first["state"] == S.SLOT_FILLING
    assert first["reply"] == S.SLOT_QUESTIONS["date"]
    assert len(session.run.history) == 2
    session.reset()
    assert session.run.history == [] and session.run.state == S.ROUTER


def test_live_session_uses_device_station_for_unstated_station() -> None:
    backend = ScriptedBackend(
        [
            route("get_opening_hours", {"station": "alto_cenizo"}),
            Completion(content=json.dumps({"answer": "No tengo información oficial sobre eso."})),
        ]
    )
    session = LiveSession(backend, load_world(), device_station="valle_bruma")
    result = session.chat("¿A qué hora abren?")
    executed = [s["executed_call"] for s in result["steps"] if s["executed_call"]]
    assert executed[0]["arguments"]["station"] == "valle_bruma"


@pytest.fixture
def server():
    backend = ScriptedBackend([])
    session = LiveSession(backend, load_world(), device_station=None)
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(session, {"model": "fake"}))
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}", backend
    httpd.shutdown()
    httpd.server_close()


def test_http_serves_page_and_info(server) -> None:
    url, _ = server
    page = httpx.get(f"{url}/")
    assert page.status_code == 200 and "Asistente del parque" in page.text
    assert "http://" not in page.text.replace("http://127.0.0.1", "")  # no external resources
    assert httpx.get(f"{url}/api/info").json() == {"model": "fake"}
    assert httpx.get(f"{url}/nope").status_code == 404


def test_http_rejects_bad_input(server) -> None:
    url, _ = server
    assert httpx.post(f"{url}/api/chat", content=b"{not json").status_code == 400
    assert httpx.post(f"{url}/api/chat", json={"message": "  "}).status_code == 400
    assert httpx.post(f"{url}/api/chat", json=["x"]).status_code == 400
    long = "a" * (MAX_MESSAGE_CHARS + 1)
    assert httpx.post(f"{url}/api/chat", json={"message": long}).status_code == 400
    huge = json.dumps({"message": "a" * 5000})
    assert httpx.post(f"{url}/api/chat", content=huge).status_code == 413


def test_http_chat_round_trip(server) -> None:
    url, backend = server
    backend.completions.append(route("register_visit", {"station": "valle_bruma"}))
    response = httpx.post(f"{url}/api/chat", json={"message": "Registrar visita a Valle Bruma"})
    assert response.status_code == 200
    body = response.json()
    assert body["state"] == S.SLOT_FILLING and body["reply"] == S.SLOT_QUESTIONS["date"]
    assert httpx.post(f"{url}/api/reset").json() == {"ok": True}


def test_live_session_passes_speedup_flags_to_the_driver() -> None:
    session = LiveSession(ScriptedBackend([]), load_world(), device_station=None,
                          extract_layout="shared_prefix", route_scope="state")  # fmt: skip
    assert session.run.extract_layout == "shared_prefix"
    assert session.run.route_scope == "state"
    session.reset()
    assert session.run.route_scope == "state"
    default = LiveSession(ScriptedBackend([]), load_world(), device_station=None)
    assert (default.run.extract_layout, default.run.route_scope) == ("default", "router")


def test_cli_speedup_flags_default_to_r2_behaviour() -> None:
    import argparse

    from nevados_bench.cli import add_speedup_flags

    parser = argparse.ArgumentParser()
    add_speedup_flags(parser)
    args = parser.parse_args([])
    assert (args.extract_layout, args.route_scope) == ("default", "router")
    args = parser.parse_args(["--extract-layout", "shared_prefix", "--route-scope", "state"])
    assert (args.extract_layout, args.route_scope) == ("shared_prefix", "state")
