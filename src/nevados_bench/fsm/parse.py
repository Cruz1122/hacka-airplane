"""Normalise raw completions of any FcMode into a ParsedOutput. Never raises."""

from __future__ import annotations

import json
import re
from typing import Any

from nevados_bench.schemas import Case, Completion, FcMode, ParsedOutput, ToolCall

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL | re.IGNORECASE)


def strip_reasoning(text: str) -> str:
    """Drop ``<think>`` blocks some templates leak into content, plus an unclosed tail."""
    text = _THINK_RE.sub("", text)
    if "<think>" in text.lower():
        text = text[: text.lower().index("<think>")]
    return text.strip()


def first_json_object(text: str) -> Any:
    """First balanced ``{...}`` in ``text`` that decodes as JSON; raises ValueError if none."""
    start = text.find("{")
    while start != -1:
        depth, in_string, escaped = 0, False, False
        for index in range(start, len(text)):
            ch = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    in_string = False
            elif ch == '"':
                in_string = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start : index + 1])
                    except json.JSONDecodeError:
                        break
        start = text.find("{", start + 1)
    raise ValueError("no JSON object found in output")


def _fail(error: str, **fields: Any) -> ParsedOutput:
    return ParsedOutput(parse_ok=False, parse_error=error, **fields)


def _native_call(raw: dict[str, Any]) -> ToolCall:
    # Accept both the raw {name, arguments} shape and the OpenAI {function: {...}} shape.
    fn = raw.get("function", raw)
    name = fn.get("name")
    if not isinstance(name, str) or not name:
        raise ValueError("tool call without name")
    arguments = fn.get("arguments", {})
    if isinstance(arguments, str):
        arguments = json.loads(arguments) if arguments.strip() else {}
    if not isinstance(arguments, dict):
        raise ValueError("tool call arguments are not an object")
    return ToolCall(name=name, arguments=arguments)


_TOOL_MARKUP_RE = re.compile(
    r"<\|?tool_call|\[TOOL_CALLS\]|<start_function_call>|<function=|<\|python_tag\|>"
    r"|<\|tool_call_start\|>",
    re.IGNORECASE,
)


def _leaked_tool_call(text: str) -> bool:
    """Tool-call markup, or a bare {name, arguments} JSON object, left in the content."""
    if _TOOL_MARKUP_RE.search(text):
        return True
    try:
        obj = first_json_object(text)
    except ValueError:
        return False
    if isinstance(obj, dict) and isinstance(obj.get("function"), dict):
        obj = obj["function"]
    return (
        isinstance(obj, dict)
        and isinstance(obj.get("name"), str)
        and ("arguments" in obj or "parameters" in obj)
    )


def _looks_like_question(text: str) -> bool:
    return "?" in text or "¿" in text


def _parse_route_native(completion: Completion) -> ParsedOutput:
    text = strip_reasoning(completion.content)
    if completion.tool_calls:
        try:
            calls = [_native_call(raw) for raw in completion.tool_calls]
        except (ValueError, TypeError, AttributeError) as exc:
            return _fail(f"malformed native tool call: {exc}", answer_text=text or None)
        return ParsedOutput(parse_ok=True, decision="call", calls=calls, answer_text=text or None)
    if _leaked_tool_call(text):
        # The model tried to call a tool but the runtime did not turn it into a structured
        # call: the app would show raw markup to the user. That is a contract failure, not
        # an abstention.
        return _fail("tool call leaked into content (not parsed by the runtime)", answer_text=text)
    decision = "clarify" if _looks_like_question(text) else "none"
    return ParsedOutput(parse_ok=True, decision=decision, answer_text=text or None)


def _parse_route_json(obj: Any) -> ParsedOutput:
    if not isinstance(obj, dict) or not isinstance(obj.get("tool"), str):
        return _fail('route output lacks a string "tool" field')
    tool = obj["tool"]
    if tool == "none":
        return ParsedOutput(parse_ok=True, decision="none")
    if tool == "clarify":
        question = obj.get("question")
        if not isinstance(question, str):
            return _fail('clarify output lacks a string "question"', decision="clarify")
        return ParsedOutput(parse_ok=True, decision="clarify", answer_text=question)
    args = obj.get("args", {})
    if not isinstance(args, dict):
        return _fail('"args" is not an object')
    return ParsedOutput(parse_ok=True, decision="call", calls=[ToolCall(name=tool, arguments=args)])


def _decode(text: str, *, tolerant: bool) -> Any:
    if not tolerant:
        return json.loads(text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return first_json_object(text)


def parse_output(completion: Completion, case: Case, mode: FcMode) -> ParsedOutput:
    if completion.timeout:
        return _fail("timeout")
    if completion.http_error:
        return _fail(f"http error: {completion.http_error}")
    try:
        if case.call_type == "route":
            if mode == "native":
                return _parse_route_native(completion)
            text = strip_reasoning(completion.content)
            obj = _decode(text, tolerant=mode == "uniform_free")
            return _parse_route_json(obj)
        if case.call_type == "extract":
            obj = _decode(strip_reasoning(completion.content), tolerant=True)
            if not isinstance(obj, dict) or "value" not in obj:
                return _fail('extract output lacks a "value" field')
            return ParsedOutput(parse_ok=True, slot_value=obj["value"])
        text = strip_reasoning(completion.content)
        if not text:
            return _fail("empty answer", answer_text="")
        return ParsedOutput(parse_ok=True, answer_text=text)
    except (ValueError, TypeError) as exc:  # JSONDecodeError is a ValueError
        return _fail(f"{type(exc).__name__}: {exc}")
