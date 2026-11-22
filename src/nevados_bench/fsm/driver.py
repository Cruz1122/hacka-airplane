"""Free-run dialogue executor.

The FSM state is driven by the model's own outputs (no teacher forcing): code validates
tool calls against their schemas, asks for missing required slots, confirms before any
side-effect tool and handles cancel / intent switch back to ROUTER. One generative call
per step; confirmation and execution are code-only steps.

With `guards=True` the deterministic guards of `nevados_bench.guards` sit between the model
and the FSM: tool arguments the user never stated are dropped (and asked for), stated
stations override the model's, and grounded answers citing another station's passages, or
stating values their cited passages do not, are replaced by the fixed abstention.
Guards also catch explicit corrections of filled slots during SLOT_FILLING ("cambia la fecha:
mejor el 5 de diciembre"): the extracted pending value is discarded and the flow router
restates the call, so the correction is merged instead of lost.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from nevados_bench.fsm import states as S
from nevados_bench.fsm.parse import parse_output
from nevados_bench.fsm.prompts import ExtractLayout, build_request
from nevados_bench.guards import (
    CHECKED_ARGS,
    detect_station,
    grounded_args,
    guard_answer,
    guard_route,
)
from nevados_bench.schemas import (
    CallType,
    Case,
    Completion,
    Dialogue,
    FcMode,
    Gold,
    LLMBackend,
    ParsedOutput,
    PromptRequest,
    ToolCall,
)
from nevados_bench.values import ABSTAIN_ES, normalize_text
from nevados_bench.world import World

_AFFIRM = {
    "si",
    "dale",
    "confirmo",
    "confirmado",
    "correcto",
    "listo",
    "ok",
    "okay",
    "yes",
    "claro",
    "hagale",
    "perfecto",
    "exacto",
}
_CANCEL = ("cancel", "olvidalo", "olvida eso", "ya no quiero", "dejalo", "anula", "no quiero")
_FALLBACK = "No entendí bien tu solicitud. ¿Puedes reformularla?"
# Explicit correction cues (on normalized text). A message naming a station or a date is
# only a correction of a filled slot if it says so: "¿hay dónde cargar el celular en Laguna
# Espejo?" mid-flow is an information question, not a new station for the flow.
_CORRECTION_RE = re.compile(
    r"\b(perdon|disculpa|corrijo|me corrijo|correccion|cambia|cambiar|cambiemos|cambio"
    r"|mejor|me equivoque|equivocado|equivocada|en realidad|realmente|sino|no|error"
    r"|sorry|actually|instead|change|i meant|wrong|correction)\b"
)
# "generate": the model writes the answer from the tool's passages (one more LLM call).
# "extractive": the passages are returned verbatim with citations (no LLM call, and no
# value can be fabricated). See the r2 report for the latency/quality trade-off.
AnswerMode = Literal["generate", "extractive"]
# Tools the flow router sees in SLOT_FILLING. "router" (r2): every ROUTER tool, so the
# visitor can switch to an information query mid-flow. "state": only the tools valid in
# SLOT_FILLING (the side-effect flows): a much shorter prompt, but an information question
# asked mid-flow is re-asked instead of answered. CONFIRM always sees only the flow tool.
RouteScope = Literal["router", "state"]


class StepResult(BaseModel):
    """One step of a free-run dialogue (an LLM call, or a code-only step)."""

    model_config = ConfigDict(extra="forbid")

    dialogue_id: str
    turn_index: int
    step_index: int
    kind: Literal["llm", "code"]
    call_type: CallType | None = None
    path: list[str]  # FSM states traversed by this step, first = state before
    request: PromptRequest | None = None
    completion: Completion | None = None
    parsed: ParsedOutput | None = None
    executed_call: ToolCall | None = None
    tool_result: dict[str, Any] | None = None
    assistant_message: str | None = None
    note: str | None = None
    slots: dict[str, Any] = Field(default_factory=dict)  # flow slots after the step

    @property
    def state_before(self) -> str:
        return self.path[0]

    @property
    def state_after(self) -> str:
        return self.path[-1]


@dataclass
class _Flow:
    tool: str
    slots: dict[str, Any] = field(default_factory=dict)
    pending: str | None = None


def _tokens(text: str) -> list[str]:
    cleaned = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in normalize_text(text))
    return cleaned.split()


def is_cancel(text: str) -> bool:
    norm = " ".join(_tokens(text))
    return any(word in norm for word in _CANCEL)


def is_affirmative(text: str) -> bool:
    tokens = _tokens(text)
    return bool(tokens) and tokens[0] in _AFFIRM and len(tokens) <= 4 and "no" not in tokens


def is_plain_negative(text: str) -> bool:
    tokens = _tokens(text)
    return bool(tokens) and tokens[0] == "no" and len(tokens) <= 2


class _Run:
    def __init__(
        self,
        dialogue: Dialogue,
        backend: LLMBackend,
        world: World,
        mode: FcMode,
        *,
        guards: bool = False,
        device_station: str | None = None,
        answer_mode: AnswerMode = "generate",
        extract_layout: ExtractLayout = "default",
        route_scope: RouteScope = "router",
    ):
        self.guards = guards
        self.answer_mode = answer_mode
        self.extract_layout = extract_layout
        self.route_scope = route_scope
        self.device_station = device_station
        self.dialogue = dialogue
        self.backend = backend
        self.world = world
        self.mode = mode
        self.state = S.ROUTER
        self.flow: _Flow | None = None
        self.history: list[dict[str, str]] = []
        self.steps: list[StepResult] = []
        self.turn_index = 0
        self.language: str = "es"
        self._current_message = ""

    # ------------------------------------------------------------------ helpers

    def _case(self, call_type: CallType, message: str, **kw: Any) -> Case:
        return Case(
            case_id=f"{self.dialogue.dialogue_id}-t{self.turn_index}-s{len(self.steps)}",
            suite="free_run",
            call_type=call_type,
            fsm_state=self.state,
            user_message=message,
            language=self.language,  # type: ignore[arg-type]
            history=list(self.history),
            gold=Gold(),
            tags={"dialogue_id": self.dialogue.dialogue_id, "turn_index": self.turn_index},
            **kw,
        )

    def _call(self, case: Case) -> tuple[PromptRequest, Completion, ParsedOutput]:
        request = build_request(case, self.world, self.mode, extract_layout=self.extract_layout)
        completion = self.backend.complete(request)
        return request, completion, parse_output(completion, case, self.mode)

    def _record(self, path: list[str], **kw: Any) -> StepResult:
        S.check_path(path)
        step = StepResult(
            dialogue_id=self.dialogue.dialogue_id,
            turn_index=self.turn_index,
            step_index=len(self.steps),
            kind="llm" if kw.get("request") is not None else "code",
            path=path,
            slots=dict(self.flow.slots) if self.flow else {},
            **kw,
        )
        self.steps.append(step)
        self.state = path[-1]
        return step

    def _summary(self) -> str | None:
        if self.flow is None:
            return None
        given = ", ".join(f"{k}={v}" for k, v in self.flow.slots.items()) or "ninguno"
        lines = [f"Trámite en curso: {self.flow.tool}.", f"Datos ya recibidos: {given}."]
        if self.flow.pending:
            lines.append(f"Dato pendiente: {self.flow.pending}.")
        return "\n".join(lines)

    def _guard_call(self, call: ToolCall) -> tuple[ToolCall | None, tuple[str, ...]]:
        """(call to act on, unstated required args). The call is None if it must not run."""
        if not self.guards:
            return call, ()
        # Only the visitor's words ground arguments: an assistant reply (an extractive one
        # quotes whole official passages) would let any value it mentions pass as stated.
        context = [m["content"] for m in self.history if m.get("role") == "user"]
        summary = self._summary()
        if summary:
            context.append(summary)
        result = guard_route(
            "call",
            [call],
            user_text=self._current_message,
            context_texts=context,
            world=self.world,
            device_station=self.device_station,
        )
        if result.missing:
            partial = result.partial_calls[0] if result.partial_calls else None
            return partial, result.missing
        return (result.calls[0] if result.calls else None), ()

    def _route_tools(self) -> list[str]:
        return S.visible_tools(self.world, S.ROUTER)

    def _slot_filling_tools(self) -> list[str]:
        """Tools the flow router sees when a SLOT_FILLING message is not the pending slot."""
        if self.route_scope == "state":
            return S.visible_tools(self.world, S.SLOT_FILLING)
        return self._route_tools()

    def _merge_valid(self, arguments: dict[str, Any]) -> list[str]:
        """Merge individually valid flow arguments; return the names rejected."""
        assert self.flow is not None
        props = self.world.tools[self.flow.tool].parameters["properties"]
        rejected = []
        for name, value in arguments.items():
            if name in props and not self.world.validate_value(name, value):
                self.flow.slots[name] = value
            else:
                rejected.append(name)
        return rejected

    def _is_correction(self) -> bool:
        """Whether the message explicitly corrects an already filled flow slot instead of
        answering the pending one (guards only; the visitor's words alone decide).

        Needs a correction cue (`_CORRECTION_RE`), a filled slot the message restates (a
        station named by name, never inferred from a trail, and different from the one
        held; or a date, count or visitor type), and no statement of the pending slot.
        Unchecked pending slots (enums such as emergency_type) cannot be told apart in
        code, so a message may always answer them.
        """
        assert self.flow is not None
        message = self._current_message
        pending = self.flow.pending
        if not _CORRECTION_RE.search(normalize_text(message)):
            return False
        if pending is None or pending not in CHECKED_ARGS:
            return False
        stated = grounded_args(message, self.world)
        if pending in stated:
            return False
        filled = self.flow.slots
        names = {sid: st.name for sid, st in self.world.stations.items()}
        station = detect_station(message, names, prefer_last=True)
        if station is not None and "station" in filled and station != filled["station"]:
            return True
        props = self.world.tools[self.flow.tool].parameters["properties"]
        return any(
            name in props and name in filled and name not in ("station", "trail_id")
            for name in stated
        )

    def _next_missing(self) -> str | None:
        assert self.flow is not None
        return next((s for s in S.REQUIRED_SLOTS[self.flow.tool] if s not in self.flow.slots), None)

    def _confirm_text(self) -> str:
        assert self.flow is not None
        details = ", ".join(f"{S.SLOT_LABELS.get(k, k)}: {v}" for k, v in self.flow.slots.items())
        label = S.TOOL_LABELS.get(self.flow.tool, self.flow.tool)
        return f"Voy a enviar {label} con estos datos: {details}. ¿Confirmas? Responde sí o no."

    def _advance_flow(self) -> tuple[str, str]:
        """(next state, assistant message) after slots changed: ask next slot or confirm."""
        assert self.flow is not None
        missing = self._next_missing()
        self.flow.pending = missing
        if missing:
            return S.SLOT_FILLING, S.SLOT_QUESTIONS[missing]
        return S.CONFIRM, self._confirm_text()

    # ----------------------------------------------------------------- dispatch

    def _dispatch(self, call: ToolCall, path: list[str], llm: dict[str, Any]) -> str:
        """Act on a routed tool call from ROUTER. Records the routing step; may run an
        answer step. Returns the assistant message of the turn."""
        world = self.world
        guarded, unstated = self._guard_call(call)
        if guarded is None:
            self._record(
                [*path, S.CLARIFY], assistant_message=_FALLBACK, note="guard_blocked", **llm
            )
            return _FALLBACK
        if unstated and guarded.name not in S.FLOW_STATE:
            # A query with an unstated argument: ask for it instead of guessing.
            message = S.SLOT_QUESTIONS.get(unstated[0], _FALLBACK)
            note = f"guard_missing={list(unstated)}"
            self._record([*path, S.CLARIFY], assistant_message=message, note=note, **llm)
            return message
        call = guarded  # flows ask for the unstated slots themselves
        if call.name not in self._route_tools():
            self._record(
                [*path, S.CLARIFY], assistant_message=_FALLBACK, note="unknown_tool", **llm
            )
            return _FALLBACK
        if call.name in S.FLOW_STATE:
            self.flow = _Flow(tool=call.name)
            rejected = self._merge_valid(call.arguments)
            nxt, message = self._advance_flow()
            route = [*path, S.FLOW_STATE[call.name], S.SLOT_FILLING]
            if nxt == S.CONFIRM:
                route.append(S.CONFIRM)
            note = f"rejected_args={rejected}" if rejected else None
            self._record(route, assistant_message=message, note=note, **llm)
            return message
        errors = world.validate_arguments(call.name, call.arguments)
        if errors:
            missing = world.missing_required(call.name, call.arguments)
            message = S.SLOT_QUESTIONS.get(missing[0], _FALLBACK) if missing else _FALLBACK
            self._record(
                [*path, S.CLARIFY], assistant_message=message, note="; ".join(errors), **llm
            )
            return message
        topic = S.tool_topic(world, call.name)
        result = world.execute_tool(call)
        self._record([*path, topic], executed_call=call, tool_result=result, **llm)
        return self._answer(result, call)

    def _extractive_answer(self, result: dict[str, Any]) -> str:
        """The official passages verbatim, each with its citation; no model call."""
        data = result.get("data") or {}
        lines = [f"{str(k).replace('_', ' ').capitalize()}: {v}." for k, v in data.items()]
        for pid in result.get("passage_ids", []):
            lines.append(f"{self.world.get_passage(pid).text} [fuente: {pid}]")
        return "\n".join(lines) if lines else ABSTAIN_ES

    def _answer(self, result: dict[str, Any], call: ToolCall | None = None) -> str:
        if self.answer_mode == "extractive":
            message = self._extractive_answer(result)
            self._record([self.state, S.ANSWER], assistant_message=message, note="extractive")
            return message
        data = result.get("data") or {}
        summary = (
            "Resultado de la herramienta: " + ", ".join(f"{k}={v}" for k, v in data.items())
            if data
            else None
        )
        case = self._case(
            "answer",
            self._current_message,
            passage_ids=list(result.get("passage_ids", [])),
            state_summary=summary,
        )
        request, completion, parsed = self._call(case)
        message = parsed.answer_text or ABSTAIN_ES
        note = None
        if self.guards:
            spec = self.world.tools.get(call.name) if call else None
            station = call.arguments.get("station") if call else None
            if station is None and call is not None and "trail_id" in call.arguments:
                trail = self.world.trails.get(call.arguments["trail_id"])
                station = trail.station if trail else None
            checked = guard_answer(
                message,
                user_message=self._current_message,
                shown={pid: self.world.get_passage(pid) for pid in case.passage_ids},
                target_station=station or self.device_station,
                gazetteer=self.world.gazetteer,
                safety=bool(spec and spec.safety),
            )
            if not checked.passed:
                message, note = checked.text, f"guard_answer={list(checked.reasons)}"
        self._record(
            [self.state, S.ANSWER],
            call_type="answer",
            request=request,
            completion=completion,
            parsed=parsed,
            assistant_message=message,
            note=note,
        )
        return message

    def _route(self, path: list[str], tool_names: list[str] | None = None) -> str:
        case = self._case(
            "route",
            self._current_message,
            tool_names=tool_names or self._route_tools(),
            state_summary=self._summary(),
        )
        request, completion, parsed = self._call(case)
        llm = {"call_type": "route", "request": request, "completion": completion, "parsed": parsed}
        if not parsed.parse_ok:
            self._record([*path, S.CLARIFY], assistant_message=_FALLBACK, note="parse_error", **llm)
            return _FALLBACK
        if parsed.decision == "none":
            message = parsed.answer_text or ABSTAIN_ES
            self._record([*path, S.OUT_OF_SCOPE], assistant_message=message, **llm)
            return message
        if parsed.decision == "clarify":
            message = parsed.answer_text or _FALLBACK
            self._record([*path, S.CLARIFY], assistant_message=message, **llm)
            return message
        return self._dispatch(parsed.calls[0], path, llm)

    # ------------------------------------------------------------------ states

    def _turn_router(self) -> str:
        path = [self.state] if self.state == S.ROUTER else [self.state, S.ROUTER]
        return self._route(path)

    def _turn_slot_filling(self) -> str:
        assert self.flow is not None and self.flow.pending is not None
        message = self._current_message
        if is_cancel(message):
            self.flow = None
            reply = "Listo, cancelé el trámite. ¿En qué más te puedo ayudar?"
            self._record([S.SLOT_FILLING, S.ROUTER], assistant_message=reply, note="cancel")
            return reply
        slot = self.flow.pending
        case = self._case("extract", message, slot_name=slot, state_summary=self._summary())
        request, completion, parsed = self._call(case)
        llm = {
            "call_type": "extract",
            "request": request,
            "completion": completion,
            "parsed": parsed,
        }
        value = parsed.slot_value
        # "cambia la fecha: mejor el 5 de diciembre" while asked for the visitor type: the
        # model tends to fabricate a pending value (r2 dlg-13, dlg-18), which used to fill
        # the slot and drop the correction. Discard it so the flow router sees the turn.
        correction = self.guards and self._is_correction()
        valid = parsed.parse_ok and value is not None and not self.world.validate_value(slot, value)
        if valid and not correction:
            self.flow.slots[slot] = value
            nxt, reply = self._advance_flow()
            self._record([S.SLOT_FILLING, nxt], assistant_message=reply, **llm)
            return reply
        # Slot not given: record the extract, then let the router decide whether the user
        # switched intent, corrected another slot, or just did not answer.
        note = "correction_detected" if correction else "slot_not_extracted"
        self._record([S.SLOT_FILLING, S.SLOT_FILLING], note=note, **llm)
        return self._flow_reroute(S.SLOT_FILLING, self._slot_filling_tools())

    def _flow_reroute(self, origin: str, tool_names: list[str]) -> str:
        assert self.flow is not None
        case = self._case(
            "route", self._current_message, tool_names=tool_names, state_summary=self._summary()
        )
        request, completion, parsed = self._call(case)
        llm = {"call_type": "route", "request": request, "completion": completion, "parsed": parsed}
        call = parsed.calls[0] if parsed.parse_ok and parsed.decision == "call" else None
        if call is not None and call.name == self.flow.tool and self.guards:
            call, _ = self._guard_call(call)  # merge only the arguments the user stated
        if call is not None and call.name != self.flow.tool and call.name in tool_names:
            # Intent switch: abandon the flow and handle the new call from ROUTER.
            self.flow = None
            return self._dispatch(call, [origin, S.ROUTER], llm)
        if call is not None and call.name == self.flow.tool:
            rejected = self._merge_valid(call.arguments)
            nxt, reply = self._advance_flow()
            route = [origin, S.SLOT_FILLING] if origin == S.CONFIRM else [origin]
            route.append(nxt)
            note = f"correction; rejected_args={rejected}" if rejected else "correction"
            self._record(route, assistant_message=reply, note=note, **llm)
            return reply
        # Nothing usable: ask again for the pending slot (or the confirmation).
        nxt, reply = self._advance_flow()
        route = [origin, S.SLOT_FILLING] if origin == S.CONFIRM else [origin]
        route.append(nxt)
        self._record(route, assistant_message=reply, note="reask", **llm)
        return reply

    def _turn_confirm(self) -> str:
        assert self.flow is not None
        message = self._current_message
        if is_affirmative(message):
            call = ToolCall(name=self.flow.tool, arguments=dict(self.flow.slots))
            result = self.world.execute_tool(call)
            if result["ok"]:
                code = result["data"].get("codigo_registro") or result["data"].get("codigo_reporte")
                reply = f"Listo, quedó enviado {S.TOOL_LABELS[self.flow.tool]}. Código: {code}."
            else:
                reply = f"No se pudo completar el trámite: {result['error']}"
            self._record(
                [S.CONFIRM, S.EXECUTE, S.ANSWER],
                executed_call=call,
                tool_result=result,
                assistant_message=reply,
            )
            self.flow = None
            return reply
        if is_cancel(message) or is_plain_negative(message):
            self.flow = None
            reply = "Entendido, no envié nada. ¿En qué más te puedo ayudar?"
            self._record([S.CONFIRM, S.ROUTER], assistant_message=reply, note="cancel")
            return reply
        # Correction: let the model restate the flow call with the corrected arguments.
        return self._flow_reroute(S.CONFIRM, [self.flow.tool])

    # -------------------------------------------------------------------- loop

    def turn(self, message: str) -> str:
        """Handle one user message from the current state; returns the assistant reply."""
        self._current_message = message
        if self.state in (S.ANSWER, S.OUT_OF_SCOPE, S.CLARIFY, S.ROUTER):
            reply = self._turn_router()
        elif self.state == S.SLOT_FILLING:
            reply = self._turn_slot_filling()
        elif self.state == S.CONFIRM:
            reply = self._turn_confirm()
        else:  # pragma: no cover - every step ends in a turn-boundary state
            raise AssertionError(f"turn started in non-boundary state {self.state}")
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def run(self) -> list[StepResult]:
        for index, turn in enumerate(self.dialogue.turns):
            self.turn_index = index
            if turn.steps:
                self.language = turn.steps[0].language
            self.turn(turn.user_message)
        return self.steps


# Public name for interactive use (one `turn(message)` per visitor message).
DialogueRun = _Run


def run_dialogue(
    dialogue: Dialogue,
    backend: LLMBackend,
    world: World,
    mode: FcMode,
    *,
    guards: bool = False,
    device_station: str | None = None,
    answer_mode: AnswerMode = "generate",
    extract_layout: ExtractLayout = "default",
    route_scope: RouteScope = "router",
) -> list[StepResult]:
    """Run ``dialogue`` free-running: FSM state follows the model's own outputs."""
    run = _Run(
        dialogue,
        backend,
        world,
        mode,
        guards=guards,
        device_station=device_station,
        answer_mode=answer_mode,
        extract_layout=extract_layout,
        route_scope=route_scope,
    )
    return run.run()
