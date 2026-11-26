from __future__ import annotations

import json
import threading
import time
from collections.abc import Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import pytest

from nevados_bench.runner.client import LlamaClient, build_body
from nevados_bench.schemas import PromptRequest

TIMINGS = {
    "cache_n": 3,
    "prompt_n": 40,
    "prompt_ms": 50.0,
    "prompt_per_second": 800.0,
    "predicted_n": 4,
    "predicted_ms": 20.0,
    "predicted_per_second": 200.0,
}


def chunk(delta: dict[str, Any], finish: str | None = None, **extra: Any) -> dict[str, Any]:
    return {"choices": [{"index": 0, "delta": delta, "finish_reason": finish}], **extra}


class FakeLlama:
    """Scripted SSE server. Each script item is (delay_s, chunk-dict) or a raw string."""

    def __init__(self) -> None:
        self.status = 200
        self.error_body = ""
        self.script: list[tuple[float, Any]] = []
        self.bodies: list[dict[str, Any]] = []
        self.paths: list[str] = []
        self.template_status = 200
        fake = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args: Any) -> None:
                pass

            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length", 0))
                body = json.loads(self.rfile.read(length) or b"{}")
                fake.bodies.append(body)
                fake.paths.append(self.path)
                if self.path == "/apply-template":
                    if fake.template_status != 200:
                        self.send_response(fake.template_status)
                        self.send_header("Content-Length", "4")
                        self.end_headers()
                        self.wfile.write(b"boom")
                        return
                    self._json({"prompt": "<templated>"})
                    return
                if self.path == "/tokenize":
                    self._json({"tokens": list(range(len(body["content"].split())))})
                    return
                if self.path.startswith("/slots/0"):
                    self._json({"id_slot": 0, "n_erased": 1})
                    return
                if fake.status != 200:
                    data = fake.error_body.encode()
                    self.send_response(fake.status)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                    return
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.end_headers()
                try:
                    for delay, item in fake.script:
                        time.sleep(delay)
                        text = item if isinstance(item, str) else json.dumps(item)
                        self.wfile.write(f"data: {text}\n\n".encode())
                        self.wfile.flush()
                    self.wfile.write(b"data: [DONE]\n\n")
                    self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass

            def _json(self, obj: Any) -> None:
                data = json.dumps(obj).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.httpd.daemon_threads = True
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()


@pytest.fixture
def fake() -> Iterator[FakeLlama]:
    server = FakeLlama()
    yield server
    server.close()


def req(**kw: Any) -> PromptRequest:
    return PromptRequest(messages=[{"role": "user", "content": "hola"}], **kw)


def test_content_stream_and_timings(fake: FakeLlama) -> None:
    fake.script = [
        (0.0, chunk({"role": "assistant", "content": None})),
        (0.05, chunk({"content": "Hola"})),
        (0.0, chunk({"content": " mundo"})),
        (0.0, chunk({}, "stop", timings=TIMINGS)),
    ]
    with LlamaClient(fake.url) as client:
        c = client.complete(req())
    assert c.content == "Hola mundo"
    assert c.finish_reason == "stop"
    assert c.ttft_ms is not None and c.ttft_ms >= 45  # role-only delta ignored
    assert c.ttfc_ms == c.ttft_ms
    assert c.total_ms is not None and c.total_ms >= c.ttft_ms
    assert (c.cache_n, c.prompt_n, c.predicted_n) == (3, 40, 4)
    assert (c.prompt_tps, c.predicted_tps) == (800.0, 200.0)
    assert c.http_error is None and not c.timeout


def test_tool_call_fragments_accumulate_by_index(fake: FakeLlama) -> None:
    fake.script = [
        (0.0, chunk({"tool_calls": [{"index": 0, "id": "a", "function": {"name": "get_w"}}]})),
        (0.0, chunk({"tool_calls": [{"index": 0, "function": {"arguments": '{"ci'}}]})),
        (0.0, chunk({"tool_calls": [{"index": 1, "function": {"name": "x", "arguments": "{}"}}]})),
        (0.0, chunk({"tool_calls": [{"index": 0, "function": {"arguments": 'ty": "P"}'}}]})),
        (0.0, chunk({}, "tool_calls", timings=TIMINGS)),
    ]
    with LlamaClient(fake.url) as client:
        c = client.complete(req())
    assert c.tool_calls == [
        {"name": "get_w", "arguments": '{"city": "P"}'},
        {"name": "x", "arguments": "{}"},
    ]
    assert c.ttfc_ms is not None
    assert c.finish_reason == "tool_calls"


def test_reasoning_then_content_separates_ttft_and_ttfc(fake: FakeLlama) -> None:
    fake.script = [
        (0.0, chunk({"reasoning_content": "pienso"})),
        (0.1, chunk({"content": "ok"})),
        (0.0, chunk({}, "stop", timings=TIMINGS)),
    ]
    with LlamaClient(fake.url) as client:
        c = client.complete(req())
        assert client.count_reasoning_tokens(c) == 1
    assert c.reasoning_content == "pienso"
    assert c.content == "ok"
    assert c.ttft_ms is not None and c.ttfc_ms is not None
    assert c.ttfc_ms - c.ttft_ms >= 90


def test_http_400_returns_body(fake: FakeLlama) -> None:
    fake.status = 400
    fake.error_body = '{"error":{"message":"unsupported template"}}'
    with LlamaClient(fake.url) as client:
        c = client.complete(req())
    assert c.http_error is not None
    assert c.http_error.startswith("400:") and "unsupported template" in c.http_error
    assert not c.timeout


def test_timeout_returns_partial(fake: FakeLlama) -> None:
    fake.script = [(0.0, chunk({"content": "a"})), (1.5, chunk({"content": "b"}))]
    with LlamaClient(fake.url, timeout_s=0.3) as client:
        c = client.complete(req())
    assert c.timeout
    assert c.content == "a"


def test_stream_error_chunk(fake: FakeLlama) -> None:
    fake.script = [(0.0, {"error": {"code": 500, "message": "boom"}})]
    with LlamaClient(fake.url) as client:
        c = client.complete(req())
    assert c.http_error is not None and "boom" in c.http_error


def test_transport_error_does_not_raise() -> None:
    with LlamaClient("http://127.0.0.1:9", timeout_s=1.0) as client:
        c = client.complete(req())
    assert c.http_error is not None and c.http_error.startswith("transport:")


def test_request_body_mapping(fake: FakeLlama) -> None:
    fake.script = [(0.0, chunk({}, "stop"))]
    schema = {"type": "object", "properties": {"tool": {"type": "string"}}}
    r = req(
        json_schema=schema,
        tool_choice="none",
        top_p=0.9,
        top_k=20,
        seed=7,
        max_tokens=33,
        cache_prompt=False,
        extra_body={"ignore_eos": True},
    )
    with LlamaClient(fake.url) as client:
        client.complete(r)
        client.erase_slot()
        assert client.tokenize("a b c") == 3
    body = fake.bodies[0]
    assert body["response_format"]["json_schema"]["schema"] == schema
    assert body["stream"] is True
    assert (body["seed"], body["max_tokens"], body["top_p"], body["top_k"]) == (7, 33, 0.9, 20)
    assert body["cache_prompt"] is False and body["ignore_eos"] is True
    assert body["tool_choice"] == "none" and "tools" not in body
    assert "top_p" not in build_body(req())


SCHEMA = {"type": "object", "properties": {"tool": {"const": "none"}}, "required": ["tool"]}


def test_schema_via_completion_uses_raw_endpoint(fake: FakeLlama) -> None:
    fake.script = [
        (0.0, {"content": '{"tool": ', "stop": False}),
        (0.0, {"content": '"none"}', "stop": False}),
        (0.0, {"content": "", "stop": True, "stop_type": "eos", "timings": TIMINGS}),
    ]
    with LlamaClient(fake.url, schema_via_completion=True) as client:
        c = client.complete(req(json_schema=SCHEMA, max_tokens=32))
    assert fake.paths == ["/apply-template", "/completion"]
    body = fake.bodies[1]
    assert body["prompt"] == "<templated>"
    assert body["json_schema"] == SCHEMA and body["n_predict"] == 32
    assert "messages" not in body and "response_format" not in body
    assert c.content == '{"tool": "none"}'
    assert c.finish_reason == "stop" and c.predicted_n == 4
    assert c.ttfc_ms is not None


def test_schema_via_completion_length_stop(fake: FakeLlama) -> None:
    fake.script = [(0.0, {"content": "{", "stop": True, "stop_type": "limit", "timings": TIMINGS})]
    with LlamaClient(fake.url, schema_via_completion=True) as client:
        c = client.complete(req(json_schema=SCHEMA))
    assert c.finish_reason == "length"


def test_schema_via_completion_keeps_chat_for_free_text_and_tools(fake: FakeLlama) -> None:
    fake.script = [(0.0, chunk({"content": "ok"}, "stop", timings=TIMINGS))]
    tools = [{"type": "function", "function": {"name": "f", "parameters": {}}}]
    with LlamaClient(fake.url, schema_via_completion=True) as client:
        client.complete(req())
        client.complete(req(json_schema=SCHEMA, tools=tools))
    assert fake.paths == ["/v1/chat/completions", "/v1/chat/completions"]


def test_schema_via_completion_template_error_does_not_raise(fake: FakeLlama) -> None:
    fake.template_status = 500
    with LlamaClient(fake.url, schema_via_completion=True) as client:
        c = client.complete(req(json_schema=SCHEMA))
    assert c.http_error == "500: boom"
    assert fake.paths == ["/apply-template"]
