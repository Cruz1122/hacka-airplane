"""Local web chat over the guarded FSM driver. Standard library only, no network access.

One visitor session per process (a kiosk or a single phone): a lock serializes turns, and
`POST /api/reset` starts over. The model runs in a separate llama-server reached at
`backend_url` (on the phone itself, or through `adb forward` during development).

Endpoints:
    GET  /             the chat page (static/index.html, no external resources)
    GET  /api/info     device station, model and build of the backend
    POST /api/chat     {"message": str} -> {"reply", "state", "latency_ms", "steps"}
    POST /api/reset    forget the conversation
"""

from __future__ import annotations

import json
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import httpx

from nevados_bench.fsm.driver import DialogueRun, RouteScope
from nevados_bench.fsm.prompts import ExtractLayout
from nevados_bench.runner.client import LlamaClient
from nevados_bench.schemas import Dialogue, FcMode
from nevados_bench.scoring.grounding import detect_language
from nevados_bench.world import World, load_world

STATIC_DIR = Path(__file__).parent / "static"
MAX_BODY_BYTES = 4096
MAX_MESSAGE_CHARS = 600
REQUEST_TIMEOUT_S = 120.0


class LiveSession:
    """Interactive wrapper around the free-run driver with guards on."""

    def __init__(
        self,
        backend: Any,
        world: World,
        *,
        device_station: str | None,
        mode: FcMode = "uniform",
        extract_layout: ExtractLayout = "default",
        route_scope: RouteScope = "router",
    ) -> None:
        self.backend = backend
        self.world = world
        self.device_station = device_station
        self.mode = mode
        self.extract_layout: ExtractLayout = extract_layout
        self.route_scope: RouteScope = route_scope
        self.lock = threading.Lock()
        self.reset()

    def reset(self) -> None:
        dialogue = Dialogue(dialogue_id="live", depth=0, phenomena=[], turns=[])
        self.run = DialogueRun(
            dialogue,
            self.backend,
            self.world,
            self.mode,
            guards=True,
            device_station=self.device_station,
            extract_layout=self.extract_layout,
            route_scope=self.route_scope,
        )

    def chat(self, message: str) -> dict[str, Any]:
        with self.lock:
            first_step = len(self.run.steps)
            language = detect_language(message)
            self.run.language = language if language in ("es", "en") else "es"
            t0 = time.monotonic()
            reply = self.run.turn(message)
            latency_ms = (time.monotonic() - t0) * 1000.0
            self.run.turn_index += 1
            steps = [
                {
                    "kind": step.kind,
                    "call_type": step.call_type,
                    "path": step.path,
                    "note": step.note,
                    "executed_call": step.executed_call.model_dump()
                    if step.executed_call
                    else None,
                    "total_ms": step.completion.total_ms if step.completion else None,
                    "output_tokens": step.completion.predicted_n if step.completion else None,
                }
                for step in self.run.steps[first_step:]
            ]
            return {
                "reply": reply,
                "state": self.run.state,
                "latency_ms": round(latency_ms),
                "steps": steps,
            }


def make_handler(session: LiveSession, info: dict[str, Any]) -> type[BaseHTTPRequestHandler]:
    index_html = (STATIC_DIR / "index.html").read_bytes()

    class Handler(BaseHTTPRequestHandler):
        server_version = "nevados-app"

        def log_message(self, format: str, *args: Any) -> None:
            pass  # visitor messages are not written to logs

        def _send(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self._send(status, body, "application/json; charset=utf-8")

        def do_GET(self) -> None:
            if self.path in ("/", "/index.html"):
                self._send(HTTPStatus.OK, index_html, "text/html; charset=utf-8")
            elif self.path == "/api/info":
                self._json(HTTPStatus.OK, info)
            else:
                self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})

        def _read_json(self) -> dict[str, Any] | None:
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                length = -1
            if not 0 <= length <= MAX_BODY_BYTES:
                self._json(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, {"error": "body too large"})
                return None
            try:
                data = json.loads(self.rfile.read(length) or b"{}")
            except (json.JSONDecodeError, UnicodeDecodeError):
                self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid JSON"})
                return None
            if not isinstance(data, dict):
                self._json(HTTPStatus.BAD_REQUEST, {"error": "expected an object"})
                return None
            return data

        def do_POST(self) -> None:
            if self.path == "/api/reset":
                with session.lock:
                    session.reset()
                self._json(HTTPStatus.OK, {"ok": True})
                return
            if self.path != "/api/chat":
                self._json(HTTPStatus.NOT_FOUND, {"error": "not found"})
                return
            data = self._read_json()
            if data is None:
                return
            message = data.get("message")
            if not isinstance(message, str) or not message.strip():
                self._json(HTTPStatus.BAD_REQUEST, {"error": "message must be a non-empty string"})
                return
            if len(message) > MAX_MESSAGE_CHARS:
                self._json(
                    HTTPStatus.BAD_REQUEST,
                    {"error": f"message longer than {MAX_MESSAGE_CHARS} characters"},
                )
                return
            try:
                result = session.chat(message.strip())
            except httpx.HTTPError as exc:
                self._json(
                    HTTPStatus.BAD_GATEWAY,
                    {"error": f"model server unavailable: {type(exc).__name__}"},
                )
                return
            self._json(HTTPStatus.OK, result)

    return Handler


def backend_info(backend_url: str) -> dict[str, Any]:
    try:
        props = httpx.get(f"{backend_url}/props", timeout=5.0).json()
    except (httpx.HTTPError, ValueError) as exc:
        return {"backend_error": f"{type(exc).__name__}: {exc}"}
    return {
        "model": Path(str(props.get("model_path", ""))).name or None,
        "llama_build": props.get("build_info"),
    }


def serve(
    *,
    backend_url: str,
    device_station: str | None,
    host: str = "127.0.0.1",
    port: int = 8765,
    extract_layout: ExtractLayout = "default",
    route_scope: RouteScope = "router",
) -> None:
    world = load_world()
    if device_station is not None and device_station not in world.stations:
        raise SystemExit(f"unknown station {device_station!r}; one of {sorted(world.stations)}")
    info = {
        "device_station": device_station,
        "device_station_name": world.stations[device_station].name if device_station else None,
        "extract_layout": extract_layout,
        "route_scope": route_scope,
        **backend_info(backend_url),
    }
    # /completion for schema calls: same B2 accuracy on the phone, ~25 % fewer output tokens.
    # Start the model server with `--cache-ram 512` or every extract call evicts the route
    # prefix and the next route call re-reads ~2k tokens (~20 s on the phone).
    with LlamaClient(
        backend_url, timeout_s=REQUEST_TIMEOUT_S, schema_via_completion=True
    ) as client:
        session = LiveSession(
            client,
            world,
            device_station=device_station,
            extract_layout=extract_layout,
            route_scope=route_scope,
        )
        httpd = ThreadingHTTPServer((host, port), make_handler(session, info))
        print(f"assistant on http://{host}:{port}  (model server {backend_url})", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            httpd.server_close()
