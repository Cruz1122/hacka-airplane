"""Shared data contracts between world, FSM, suites, runner, scoring and report.

This module is the single integration point of the package: every other module
depends on it and on nothing else across package boundaries (except where noted
in each package's docstring). Change it deliberately.
"""

from __future__ import annotations

from typing import Any, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field

CallType = Literal["route", "extract", "answer"]
FcMode = Literal["native", "uniform", "uniform_free"]
Decision = Literal["call", "none", "clarify"]
ContextLevel = Literal["0.5k", "1k", "2k", "4k", "8k"]

# Approximate prompt-token targets per context level (measured tokens are recorded per request).
CONTEXT_LEVEL_TOKENS: dict[str, int] = {"0.5k": 500, "1k": 1000, "2k": 2000, "4k": 4000, "8k": 8000}


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid")


# ----------------------------------------------------------------------------- world


class ToolSpec(_Model):
    name: str
    description: str
    parameters: dict[str, Any]  # JSON Schema object for the arguments
    has_side_effects: bool = False
    safety: bool = False
    near_duplicate_of: str | None = None
    fsm_states: list[str] = Field(default_factory=list)


class Passage(_Model):
    id: str
    station: str | None  # canonical station id, None for park-wide passages
    field: str  # e.g. "opening_hours", "altitude_m", "emergency_phone"
    text: str
    values: list[str]  # canonical trap values stated by this passage
    safety: bool = False
    # Plausible real-world/prior value this passage deliberately contradicts, if any.
    prior_values: list[str] = Field(default_factory=list)


class GazetteerEntry(_Model):
    value: str  # normalized value
    passage_id: str
    station: str | None
    field: str


# ----------------------------------------------------------------------------- cases


class ToolCall(_Model):
    name: str
    arguments: dict[str, Any]


class Gold(_Model):
    """Ground truth. Only the fields relevant to the case's call_type are set."""

    # route
    decision: Decision | None = None
    calls: list[ToolCall] = Field(default_factory=list)
    acceptable_tools: list[str] = Field(default_factory=list)  # extra tool names also correct
    missing_required: list[str] = Field(default_factory=list)  # args the user did not provide
    # extract
    slot_name: str | None = None
    slot_value: Any = None
    # answer
    answerable: bool | None = None
    gold_values: list[str] = Field(default_factory=list)
    gold_passage_id: str | None = None
    lure_values: list[str] = Field(default_factory=list)  # same field, other entity
    prior_values: list[str] = Field(default_factory=list)  # real-world prior to detect
    # fsm
    next_state: str | None = None


class Case(_Model):
    case_id: str
    suite: str
    call_type: CallType
    fsm_state: str
    user_message: str
    language: Literal["es", "en", "mixed"] = "es"
    strata: list[str] = Field(default_factory=list)
    history: list[dict[str, str]] = Field(default_factory=list)  # prior turns, oldest first
    state_summary: str | None = None  # code-generated summary of flow state
    tool_names: list[str] = Field(default_factory=list)  # visible tools, in prompt order
    passage_ids: list[str] = Field(default_factory=list)  # context passages, in prompt order
    context_level: ContextLevel | None = None
    bundle_id: str | None = None  # cases sharing a bundle share an identical prompt prefix
    slot_name: str | None = None  # for extract calls: the slot being requested
    gold: Gold
    # Free-form analysis dimensions: gold_position, distractors_n, tools_n, history_turns,
    # question_type, safety, injection, near_duplicate, dialogue_id, turn_index, ...
    tags: dict[str, Any] = Field(default_factory=dict)
    priority: int = 0  # lower runs first; used when a time budget truncates a suite


class DialogueTurn(_Model):
    user_message: str
    # One Case per generative step expected in this turn, evaluated from the gold state
    # (teacher forcing). case_id/suite are filled by the suite generator.
    steps: list[Case]


class Dialogue(_Model):
    dialogue_id: str
    depth: int
    phenomena: list[str]  # slot_filling, correction, intent_switch, cancel_resume, ellipsis
    turns: list[DialogueTurn]
    # Side-effect tool calls a correct run executes (after confirmation), in order, with
    # their final arguments. Ground truth for free-run dialogue success.
    expected_executions: list[ToolCall] = Field(default_factory=list)


# ----------------------------------------------------------------------------- runtime


class PromptRequest(_Model):
    """Runtime-agnostic request built by the FSM prompt assembler."""

    messages: list[dict[str, Any]]
    tools: list[dict[str, Any]] | None = None  # OpenAI tools array (native mode)
    tool_choice: Literal["auto", "none", "required"] | None = None
    json_schema: dict[str, Any] | None = None  # constrained output (uniform mode)
    max_tokens: int = 256
    temperature: float = 0.0
    top_p: float | None = None
    top_k: int | None = None
    seed: int = 1234
    cache_prompt: bool = True
    extra_body: dict[str, Any] = Field(default_factory=dict)


class Completion(_Model):
    content: str = ""
    reasoning_content: str = ""
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)  # raw: {name, arguments}
    finish_reason: str | None = None
    # client-side wall clock
    ttft_ms: float | None = None  # first SSE delta of any kind
    ttfc_ms: float | None = None  # first content or tool-call delta (excludes reasoning)
    total_ms: float | None = None
    # server-side timings
    cache_n: int | None = None
    prompt_n: int | None = None
    prompt_ms: float | None = None
    prompt_tps: float | None = None
    predicted_n: int | None = None
    predicted_ms: float | None = None
    predicted_tps: float | None = None
    timeout: bool = False
    http_error: str | None = None


class LLMBackend(Protocol):
    def complete(self, request: PromptRequest) -> Completion: ...


class ParsedOutput(_Model):
    """Normalized model decision, produced by the FSM output parser for any FcMode."""

    parse_ok: bool
    decision: Decision | None = None
    calls: list[ToolCall] = Field(default_factory=list)
    slot_value: Any = None
    answer_text: str | None = None
    parse_error: str | None = None


class RequestRecord(_Model):
    """One line of requests.jsonl. Append-only; scoring is recomputed from these."""

    model_config = ConfigDict(extra="allow")

    # identity
    run_id: str
    batch: str
    suite: str
    case_id: str
    rep: int = 0
    arm: str = "default"  # experiment arm, e.g. "cold", "warm", "history_full", "retry"
    model_id: str
    gguf_file: str
    gguf_sha256: str | None = None
    quant: str
    image_digest: str | None = None
    llama_build: str | None = None
    profile: str
    threads: int
    ctx_size: int
    fc_mode: FcMode | None = None
    thinking: bool = False
    sampling: dict[str, Any] = Field(default_factory=dict)
    seed: int = 1234
    ts: str
    # input description
    call_type: CallType | None = None
    fsm_state: str | None = None
    strata: list[str] = Field(default_factory=list)
    context_level: str | None = None
    tools_n: int = 0
    tools_tokens: int | None = None
    tags: dict[str, Any] = Field(default_factory=dict)
    # measurements
    completion: Completion
    prompt_tokens_total: int | None = None  # cache_n + prompt_n
    reasoning_tokens: int | None = None
    overhead_ms: float | None = None  # total_ms - prompt_ms - predicted_ms
    truncated: bool = False
    # system probe
    mem_current: int | None = None
    mem_peak: int | None = None
    mem_anon: int | None = None
    mem_file: int | None = None
    pgmajfault_delta: int | None = None
    oom_events: int | None = None
    cpu_usage_usec_delta: int | None = None
    nr_throttled: int | None = None
    host_freq_mhz: float | None = None
    host_temp_c: float | None = None
    # normalized output (stored so scoring does not need the model's template knowledge)
    parsed: ParsedOutput | None = None
