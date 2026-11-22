"""Streaming OpenAI-compatible client for llama-server implementing schemas.LLMBackend.

Verified against llama.cpp b12375: the final SSE chunk (the one with `finish_reason`)
carries `timings` without any extra request flag, and the stream starts with a
role-only delta (`{"role": "assistant", "content": null}`).
"""

from __future__ import annotations

import json
import time
from typing import Any

import httpx

from nevados_bench.schemas import Completion, PromptRequest

_ERROR_BODY_LIMIT = 2000


def build_body(request: PromptRequest) -> dict[str, Any]:
    body: dict[str, Any] = {
        "messages": request.messages,
        "stream": True,
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "seed": request.seed,
        "cache_prompt": request.cache_prompt,
    }
    if request.top_p is not None:
        body["top_p"] = request.top_p
    if request.top_k is not None:
        body["top_k"] = request.top_k
    if request.tools is not None:
        body["tools"] = request.tools
    if request.tool_choice is not None:
        body["tool_choice"] = request.tool_choice
    if request.json_schema is not None:
        body["response_format"] = {
            "type": "json_schema",
            "json_schema": {"name": "output", "strict": True, "schema": request.json_schema},
        }
    body.update(request.extra_body)
    return body


def build_raw_body(request: PromptRequest, prompt: str) -> dict[str, Any]:
    """Body for /completion: the templated prompt plus the schema, no chat handler.

    Through /v1/chat/completions the Gemma 4 handler (b12375) wraps the schema grammar so
    the model may emit a ```json fence and pretty-printed JSON: ~10 extra decoded tokens
    per call. /completion applies the bare schema grammar.
    """
    body: dict[str, Any] = {
        "prompt": prompt,
        "stream": True,
        "n_predict": request.max_tokens,
        "temperature": request.temperature,
        "seed": request.seed,
        "cache_prompt": request.cache_prompt,
        "json_schema": request.json_schema,
    }
    if request.top_p is not None:
        body["top_p"] = request.top_p
    if request.top_k is not None:
        body["top_k"] = request.top_k
    body.update(request.extra_body)
    return body


class _StreamState:
    def __init__(self, t0: float) -> None:
        self.t0 = t0
        self.content: list[str] = []
        self.reasoning: list[str] = []
        self.tool_calls: dict[int, dict[str, Any]] = {}
        self.finish_reason: str | None = None
        self.ttft_ms: float | None = None
        self.ttfc_ms: float | None = None
        self.timings: dict[str, Any] = {}
        self.error: str | None = None

    def feed(self, chunk: dict[str, Any], now: float) -> None:
        if "error" in chunk:
            self.error = json.dumps(chunk["error"], ensure_ascii=False)
        if "timings" in chunk:
            self.timings = chunk["timings"]
        if "choices" not in chunk and "content" in chunk:  # /completion stream format
            choices = [{"delta": {"content": chunk["content"]}}]
            if chunk.get("stop"):
                limit = chunk.get("stop_type") == "limit"
                choices[0]["finish_reason"] = "length" if limit else "stop"
            chunk = {"choices": choices}
        for choice in chunk.get("choices") or []:
            delta = choice.get("delta") or {}
            content = delta.get("content")
            reasoning = delta.get("reasoning_content")
            calls = delta.get("tool_calls")
            if content or reasoning or calls:
                ms = (now - self.t0) * 1000.0
                if self.ttft_ms is None:
                    self.ttft_ms = ms
                if (content or calls) and self.ttfc_ms is None:
                    self.ttfc_ms = ms
            if content:
                self.content.append(content)
            if reasoning:
                self.reasoning.append(reasoning)
            for call in calls or []:
                slot = self.tool_calls.setdefault(call.get("index", 0), {"name": "", "args": []})
                fn = call.get("function") or {}
                if fn.get("name"):
                    slot["name"] += fn["name"]
                if fn.get("arguments"):
                    slot["args"].append(fn["arguments"])
            if choice.get("finish_reason"):
                self.finish_reason = choice["finish_reason"]

    def completion(self, total_ms: float, **extra: Any) -> Completion:
        t = self.timings
        return Completion(
            content="".join(self.content),
            reasoning_content="".join(self.reasoning),
            tool_calls=[
                {"name": c["name"], "arguments": "".join(c["args"])}
                for _, c in sorted(self.tool_calls.items())
            ],
            finish_reason=self.finish_reason,
            ttft_ms=self.ttft_ms,
            ttfc_ms=self.ttfc_ms,
            total_ms=total_ms,
            cache_n=t.get("cache_n"),
            prompt_n=t.get("prompt_n"),
            prompt_ms=t.get("prompt_ms"),
            prompt_tps=t.get("prompt_per_second"),
            predicted_n=t.get("predicted_n"),
            predicted_ms=t.get("predicted_ms"),
            predicted_tps=t.get("predicted_per_second"),
            http_error=extra.pop("http_error", None) or self.error,
            **extra,
        )


class LlamaClient:
    """`complete()` never raises for timeouts, HTTP errors or transport errors.

    `timeout_s` is a wall-clock budget per request, checked between SSE lines; a single
    stalled read is bounded by the same value, so the worst case is ~2x `timeout_s`.
    """

    def __init__(
        self, base_url: str, *, timeout_s: float = 300.0, schema_via_completion: bool = False
    ) -> None:
        """`schema_via_completion`: send schema-constrained requests without tools to
        /completion (see build_raw_body). The template round trip counts in total_ms."""
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.schema_via_completion = schema_via_completion
        self._http = httpx.Client(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout_s, connect=10.0),
        )

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> LlamaClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def complete(self, request: PromptRequest) -> Completion:
        t0 = time.perf_counter()
        state = _StreamState(t0)

        def elapsed_ms() -> float:
            return (time.perf_counter() - t0) * 1000.0

        raw = self.schema_via_completion and request.json_schema is not None and not request.tools
        try:
            if raw:
                path, body = (
                    "/completion",
                    build_raw_body(request, self.apply_template(request.messages)),
                )
            else:
                path, body = "/v1/chat/completions", build_body(request)
            with self._http.stream("POST", path, json=body) as resp:
                if resp.status_code >= 400:
                    text = resp.read().decode("utf-8", "replace")[:_ERROR_BODY_LIMIT]
                    return state.completion(elapsed_ms(), http_error=f"{resp.status_code}: {text}")
                for line in resp.iter_lines():
                    now = time.perf_counter()
                    if now - t0 > self.timeout_s:
                        return state.completion(elapsed_ms(), timeout=True)
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                    except json.JSONDecodeError:
                        state.error = f"unparseable SSE data: {data[:200]}"
                        continue
                    state.feed(chunk, now)
        except httpx.TimeoutException:
            return state.completion(elapsed_ms(), timeout=True)
        except httpx.HTTPStatusError as exc:  # /apply-template failed
            text = exc.response.text[:_ERROR_BODY_LIMIT]
            return state.completion(elapsed_ms(), http_error=f"{exc.response.status_code}: {text}")
        except httpx.TransportError as exc:
            return state.completion(elapsed_ms(), http_error=f"transport: {exc!r}")
        return state.completion(elapsed_ms())

    def tokenize(self, text: str) -> int:
        resp = self._http.post("/tokenize", json={"content": text})
        resp.raise_for_status()
        return len(resp.json()["tokens"])

    def apply_template(self, messages: list[dict[str, Any]]) -> str:
        """Prompt string the server builds from `messages` (chat template applied)."""
        resp = self._http.post("/apply-template", json={"messages": messages})
        resp.raise_for_status()
        return resp.json()["prompt"]

    def count_prompt_tokens(self, messages: list[dict[str, Any]]) -> int:
        return self.tokenize(self.apply_template(messages))

    def erase_slot(self, slot_id: int = 0) -> None:
        """Drop the slot's KV cache. Needs the server started with --slot-save-path."""
        resp = self._http.post(f"/slots/{slot_id}", params={"action": "erase"})
        if resp.status_code != 200:
            raise RuntimeError(f"slot erase failed: HTTP {resp.status_code}: {resp.text[:300]}")

    def count_reasoning_tokens(self, completion: Completion) -> int:
        return self.tokenize(completion.reasoning_content) if completion.reasoning_content else 0

    def props(self) -> dict[str, Any]:
        resp = self._http.get("/props")
        resp.raise_for_status()
        return resp.json()
