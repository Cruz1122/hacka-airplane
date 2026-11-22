"""Batch orchestration: one llama-server container at a time, incremental and resumable.

Layout written here (read back by report.aggregate):
    results/<run_id>/<batch>/<model_dir>/requests.jsonl   one RequestRecord per line
    results/<run_id>/<batch>/<model_dir>/meta.json        per-launch sidecar (load time, limits)

Timed and quality requests share the same serial lane on purpose: a second container would
compete for the same four physical cores and invalidate every latency number.
"""

from __future__ import annotations

import json
import time
from collections.abc import Callable, Iterable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from nevados_bench.config import (
    MODELS_DIR,
    PROJECT_ROOT,
    HardwareProfile,
    ModelConfig,
    load_image_lock,
    load_models_lock,
    load_profiles,
)
from nevados_bench.fsm.driver import AnswerMode, RouteScope, run_dialogue
from nevados_bench.fsm.parse import parse_output
from nevados_bench.fsm.prompts import ExtractLayout, build_request, native_tools
from nevados_bench.runner.client import LlamaClient
from nevados_bench.runner.measure import run_request
from nevados_bench.runner.phone import (
    Adb,
    PhoneHostProbe,
    PhoneProbe,
    PhoneServer,
    device_info,
    device_state,
)
from nevados_bench.runner.probe import CgroupProbe, HostProbe, parse_cpuset
from nevados_bench.runner.server import LlamaServer, ServerSpec, ServerStartError
from nevados_bench.runner.speed import run_speed_protocol
from nevados_bench.runner.writer import RecordWriter, done_keys
from nevados_bench.schemas import (
    Case,
    Completion,
    Dialogue,
    FcMode,
    PromptRequest,
    RequestRecord,
)
from nevados_bench.world import World, load_world

RESULTS_DIR = PROJECT_ROOT / "results"
SUITES_DIR = PROJECT_ROOT / "data" / "suites"
MAIN_PROFILE = "phone-tight"
ROUTE_MODES: tuple[FcMode, ...] = ("native", "uniform")
# "docker" (laptop container) or "phone" (adb device). Set by the CLI before a batch runs;
# on the phone every launch uses PHONE_PROFILE whatever profile the batch asks for.
TARGET = "docker"
PHONE_PROFILE = "phone-device"
# Host port of the server (container publish or adb forward). Distinct ports let a laptop
# batch and a phone batch run at the same time without one reaching the other's server.
HOST_PORT: int | None = None
# "chat" (r1: /v1/chat/completions) or "completion": schema-constrained calls go to
# /completion, which skips the chat handler's ```json fence (see client.build_raw_body).
SCHEMA_ENDPOINT = "chat"
# Host-RAM prompt cache (MiB) overriding profiles.yaml (0 there, so cold prefill is cold).
# Deployment-like dialogue runs set it: with one slot, an extract call otherwise evicts
# the ~2k-token route prefix and the next route call re-reads all of it.
CACHE_RAM_MIB: int | None = None
# Opt-in free-run speedups (see fsm.prompts.ExtractLayout and fsm.driver.RouteScope). The
# defaults reproduce the r2 prompts and FSM; both are recorded in meta.json and identity.
EXTRACT_LAYOUT: ExtractLayout = "default"
ROUTE_SCOPE: RouteScope = "router"
# Always-thinking models spend output tokens on reasoning before the answer.
THINKING_EXTRA_TOKENS = 1024
REQUEST_TIMEOUT_S = 900.0
PASS_K = 5
PASS_K_CASES = 60
# All logical CPUs, only as an SMT reference point in the thread sweep.
SMT_PROFILE = HardwareProfile(cpuset="0-7", threads=8, memory="5g")


class ServerDied(RuntimeError):
    """The container stopped answering mid-batch (typically an OOM kill)."""


# ----------------------------------------------------------------------------- suites


def build_suites(world: World | None = None, out_dir: Path = SUITES_DIR) -> dict[str, int]:
    """Materialize every suite as JSONL so that what is scored is exactly what was run."""
    from nevados_bench.suites import dialogues, fc, grounded

    world = world or load_world()
    out_dir.mkdir(parents=True, exist_ok=True)
    suites: dict[str, list[Any]] = {
        "smoke": fc.generate_smoke(world),
        "fc_core": fc.generate_fc_core(world),
        "fc_tools_sweep": fc.generate_fc_tools_sweep(world),
        "fc_ctx_sweep": fc.generate_fc_ctx_sweep(world),
        "grounded_qa": grounded.generate_grounded_qa(world),
        "dialogues": dialogues.generate_dialogues(world),
    }
    for name, items in suites.items():
        lines = [item.model_dump_json() for item in items]
        (out_dir / f"{name}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {name: len(items) for name, items in suites.items()}


def load_cases(suite: str, suites_dir: Path = SUITES_DIR) -> list[Case]:
    path = suites_dir / f"{suite}.jsonl"
    with path.open(encoding="utf-8") as handle:
        return [Case.model_validate_json(line) for line in handle if line.strip()]


def load_dialogues(suites_dir: Path = SUITES_DIR) -> list[Dialogue]:
    path = suites_dir / "dialogues.jsonl"
    with path.open(encoding="utf-8") as handle:
        return [Dialogue.model_validate_json(line) for line in handle if line.strip()]


def dialogue_step_cases(dialogues: Iterable[Dialogue]) -> list[Case]:
    """Flatten teacher-forced steps, adding the positional tags the scorers slice on."""
    cases = []
    for dialogue in dialogues:
        for turn_index, turn in enumerate(dialogue.turns):
            for step_index, step in enumerate(turn.steps):
                tags = {
                    "dialogue_id": dialogue.dialogue_id,
                    "turn_index": turn_index,
                    "step_index": step_index,
                    "depth": dialogue.depth,
                    **step.tags,
                }
                cases.append(step.model_copy(update={"tags": tags}))
    return cases


# ----------------------------------------------------------------------------- session


@dataclass
class Session:
    """One model loaded in one container, plus everything needed to record requests."""

    run_id: str
    batch: str
    model: ModelConfig
    profile_name: str
    world: World
    client: Any  # LlamaClient, or a fake LLMBackend in tests
    writer: RecordWriter
    done: set[tuple[Any, ...]]
    identity: dict[str, Any]
    probe: CgroupProbe | None = None
    host_probe: HostProbe | None = None
    server: LlamaServer | None = None
    deadline: float | None = None
    written: int = 0
    skipped_budget: int = 0
    _tool_tokens: dict[tuple[str, ...], int | None] = field(default_factory=dict)

    def out_of_budget(self) -> bool:
        return self.deadline is not None and time.monotonic() > self.deadline

    def template(self, **fields: Any) -> dict[str, Any]:
        return {**self.identity, **fields}

    def emit(self, record: RequestRecord) -> None:
        self.writer.append(record)
        self.done.add((record.case_id, record.rep, record.arm, record.fc_mode))
        self.written += 1

    def tools_tokens(self, tool_names: list[str]) -> int | None:
        """Token cost of the native tool list (cached per distinct list)."""
        key = tuple(tool_names)
        if key not in self._tool_tokens:
            tokenize = getattr(self.client, "tokenize", None)
            count = None
            if tool_names and callable(tokenize):
                rendered = json.dumps(native_tools(self.world, tool_names), ensure_ascii=False)
                try:
                    count = tokenize(rendered)
                except Exception:  # best-effort metadata; never fail a measured batch for it
                    count = None
            self._tool_tokens[key] = count
        return self._tool_tokens[key]

    def check_alive(self, completion: Completion) -> None:
        failed = completion.http_error is not None or completion.timeout
        if failed and self.server is not None and not self.server.is_running():
            raise ServerDied(completion.http_error or "timeout")


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _write_meta(path: Path, meta: dict[str, Any]) -> None:
    path.write_text(json.dumps(meta, indent=2, ensure_ascii=False, default=str), encoding="utf-8")


@contextmanager
def model_session(
    run_id: str,
    batch: str,
    model: ModelConfig,
    profile_name: str = MAIN_PROFILE,
    *,
    profile: HardwareProfile | None = None,
    threads: int | None = None,
    thinking: bool = False,
    log_verbosity: int | None = None,
    dir_suffix: str = "",
    budget_min: float | None = None,
    gguf_filename: str | None = None,
    quant: str | None = None,
    ctx_size: int | None = None,
) -> Iterator[Session | None]:
    """Start the server for `model`; yields None (after writing meta.json) if it cannot start."""
    profiles = load_profiles()
    on_phone = TARGET == "phone"
    if on_phone:
        profile_name, profile = PHONE_PROFILE, profiles.profiles[PHONE_PROFILE]
    profile = profile or profiles.profiles[profile_name]
    lock = load_models_lock().get(model.id)
    filename = gguf_filename or (lock.filename if lock else None)
    if filename is None:
        raise FileNotFoundError(f"{model.id} is not in models.lock.yaml; run `fetch` first")
    gguf_path = MODELS_DIR / filename
    quant = quant or model.quant
    out_dir = RESULTS_DIR / run_id / batch / f"{model.id}{dir_suffix}"
    out_dir.mkdir(parents=True, exist_ok=True)
    spec_kwargs: dict[str, Any] = {}
    if log_verbosity is not None:
        spec_kwargs["log_verbosity"] = log_verbosity
    spec = ServerSpec(
        model=model,
        gguf_filename=filename,
        profile_name=profile_name,
        profile=profile,
        server=profiles.server
        if CACHE_RAM_MIB is None
        else profiles.server.model_copy(update={"cache_ram_mib": CACHE_RAM_MIB}),
        models_dir=MODELS_DIR,
        image_lock=load_image_lock(),
        threads=threads,
        thinking=thinking,
        ctx_size=ctx_size,
        host_port=HOST_PORT,
        **spec_kwargs,
    )
    meta: dict[str, Any] = {
        "model_id": model.id,
        "quant": quant,
        "profile": profile_name,
        "threads": spec.effective_threads,
        "ctx_size": spec.effective_ctx,
        "gguf_file": filename,
        "gguf_size_bytes": gguf_path.stat().st_size if gguf_path.exists() else None,
        "license": model.license,
        "deployable": model.deployable,
        "thinking_mode": model.thinking,
        "target": TARGET,
        "schema_endpoint": SCHEMA_ENDPOINT,
        "extract_layout": EXTRACT_LAYOUT,
        "route_scope": ROUTE_SCOPE,
        "cache_ram_mib": spec.server.cache_ram_mib,
        "started": _now(),
    }
    meta_path = out_dir / "meta.json"
    cpus = parse_cpuset(profile.cpuset)
    adb = Adb() if on_phone else None
    if adb is not None:
        meta.update(device=device_info(adb), device_state_start=device_state(adb))
    try:
        with PhoneServer(spec, adb=adb, cpus=cpus) if adb else LlamaServer(spec) as server:
            probe: Any
            host_probe: Any
            if adb is not None:
                probe = PhoneProbe(adb, server.pid, cpus)
                host_probe = PhoneHostProbe(adb, cpus)
            else:
                probe = CgroupProbe.for_container(server.container_id or "", pid=server.pid)
                host_probe = HostProbe(cpus)
            limits = probe.effective_limits()
            meta.update(
                load_ms=server.load_ms,
                llama_build=server.llama_build,
                mem_limit=limits.memory_max,
                effective_cpus=limits.cpus,
                swap_max=limits.memory_swap_max,
                chat_template_caps=server.props.get("chat_template_caps"),
                chat_handlers=server.chat_handlers() if log_verbosity else None,
            )
            _write_meta(meta_path, meta)
            image = spec.image_lock
            requests_path = out_dir / "requests.jsonl"
            done = done_keys(requests_path)
            with (
                LlamaClient(
                    server.base_url,
                    timeout_s=REQUEST_TIMEOUT_S,
                    schema_via_completion=SCHEMA_ENDPOINT == "completion",
                ) as client,
                RecordWriter(requests_path) as writer,
            ):
                session = Session(
                    run_id=run_id,
                    batch=batch,
                    model=model,
                    profile_name=profile_name,
                    world=load_world(),
                    client=client,
                    writer=writer,
                    done=done,
                    probe=probe,
                    host_probe=host_probe,
                    server=server,
                    deadline=time.monotonic() + budget_min * 60 if budget_min else None,
                    identity={
                        "run_id": run_id,
                        "batch": batch,
                        "model_id": model.id,
                        "gguf_file": filename,
                        "gguf_sha256": lock.sha256 if lock and not gguf_filename else None,
                        "quant": quant,
                        "image_digest": image.digest if image else None,
                        "llama_build": server.llama_build,
                        "profile": profile_name,
                        "threads": spec.effective_threads,
                        "ctx_size": spec.effective_ctx,
                        "thinking": thinking or model.thinking == "always",
                        "load_ms": server.load_ms,
                        "schema_endpoint": SCHEMA_ENDPOINT,
                        "extract_layout": EXTRACT_LAYOUT,
                        "route_scope": ROUTE_SCOPE,
                    },
                )
                try:
                    yield session
                except ServerDied as exc:
                    meta.update(died=str(exc), oom_killed=server.oom_killed)
                finally:
                    meta.update(
                        finished=_now(),
                        records_written=session.written,
                        cases_skipped_budget=session.skipped_budget,
                        mem_peak_final=probe.snapshot().memory_peak,
                    )
                    if adb is not None:
                        meta.update(device_state_end=device_state(adb))
                    _write_meta(meta_path, meta)
    except ServerStartError as exc:
        meta.update(
            start_error=str(exc)[-2000:], oom_killed=exc.oom_killed, exit_code=exc.exit_code
        )
        _write_meta(meta_path, meta)
        yield None


# ----------------------------------------------------------------------------- running cases


def _prepare(session: Session, case: Case, mode: FcMode, sampling: dict[str, Any] | None):
    request = build_request(case, session.world, mode, sampling=sampling)
    if session.model.thinking == "always":
        request = request.model_copy(
            update={"max_tokens": request.max_tokens + THINKING_EXTRA_TOKENS}
        )
    return request


def run_case(
    session: Session,
    case: Case,
    mode: FcMode,
    *,
    arm: str = "default",
    rep: int = 0,
    sampling: dict[str, Any] | None = None,
    transform: Callable[[PromptRequest], PromptRequest] | None = None,
) -> RequestRecord | None:
    """Run one case unless already recorded. Returns None when skipped."""
    fc_mode = mode if case.call_type == "route" else None
    if (case.case_id, rep, arm, fc_mode) in session.done:
        return None
    request = _prepare(session, case, mode, sampling)
    if transform is not None:
        request = transform(request)
    record = run_request(
        session.client,
        session.probe,
        session.host_probe,
        request,
        session.template(
            suite=case.suite,
            case_id=case.case_id,
            rep=rep,
            arm=arm,
            fc_mode=fc_mode,
            call_type=case.call_type,
            fsm_state=case.fsm_state,
            strata=case.strata,
            context_level=case.context_level,
            tools_n=len(case.tool_names),
            tools_tokens=session.tools_tokens(case.tool_names),
            tags=case.tags,
        ),
    )
    record.parsed = parse_output(record.completion, case, mode)
    session.emit(record)
    session.check_alive(record.completion)
    return record


def run_cases(
    session: Session,
    cases: Iterable[Case],
    mode: FcMode,
    **kwargs: Any,
) -> None:
    """Run cases until done or the session's time budget is exhausted.

    Cases sharing an identical ordered tool list (and context level) run back to back so the
    server reuses the cached prompt prefix; groups are ordered by their most urgent case.
    """
    groups: dict[tuple[Any, ...], list[Case]] = {}
    for case in cases:
        groups.setdefault((tuple(case.tool_names), case.context_level), []).append(case)
    ordered = [
        case
        for group in sorted(groups.values(), key=lambda g: min((c.priority, c.case_id) for c in g))
        for case in sorted(group, key=lambda c: (c.priority, c.case_id))
    ]
    for index, case in enumerate(ordered):
        if session.out_of_budget():
            session.skipped_budget += len(ordered) - index
            return
        run_case(session, case, mode, **kwargs)


def run_bundled(session: Session, cases: list[Case], mode: FcMode = "uniform") -> None:
    """Run cases grouped by prompt-prefix bundle so the long prefill is paid once per bundle.

    The slot is erased before each bundle, so its first request is a true cold prefill and
    the rest are warm. The remaining time budget is split evenly across remaining bundles so
    a truncated run still covers every context level.
    """
    bundles: dict[str, list[Case]] = {}
    for case in cases:
        bundles.setdefault(case.bundle_id or case.case_id, []).append(case)
    names = sorted(bundles, key=lambda b: (min(c.priority for c in bundles[b]), b))
    for position, name in enumerate(names):
        slice_deadline = None
        if session.deadline is not None:
            remaining = session.deadline - time.monotonic()
            if remaining <= 0:
                session.skipped_budget += sum(len(bundles[n]) for n in names[position:])
                return
            slice_deadline = time.monotonic() + remaining / (len(names) - position)
        pending = [
            c for c in sorted(bundles[name], key=lambda c: (c.priority, c.case_id))
            if (c.case_id, 0, "default", None) not in session.done
        ]  # fmt: skip
        if not pending:
            continue
        erase = getattr(session.client, "erase_slot", None)
        if callable(erase):
            erase()
        for index, case in enumerate(pending):
            if slice_deadline is not None and time.monotonic() > slice_deadline:
                session.skipped_budget += len(pending) - index
                break
            run_case(session, case, mode)


# ----------------------------------------------------------------------------- arms


def _validation_error(session: Session, record: RequestRecord) -> str | None:
    """Why the first attempt is invalid, phrased for the model; None when it is valid."""
    parsed = record.parsed
    if parsed is None or not parsed.parse_ok:
        return f"no se pudo interpretar la salida ({parsed.parse_error if parsed else 'vacía'})"
    for call in parsed.calls:
        if call.name not in session.world.tools:
            return f"la herramienta '{call.name}' no existe"
        errors = session.world.validate_arguments(call.name, call.arguments)
        if errors:
            return f"argumentos inválidos para '{call.name}': {'; '.join(errors)}"
    return None


def run_retries(session: Session, cases: list[Case], mode: FcMode, first_records: Path) -> None:
    """One retry carrying the validation error, for first attempts that were invalid."""
    by_id = {case.case_id: case for case in cases}
    if not first_records.exists():
        return
    with first_records.open(encoding="utf-8") as handle:
        firsts = [RequestRecord.model_validate_json(line) for line in handle if line.strip()]
    for first in firsts:
        case = by_id.get(first.case_id)
        if case is None or first.arm != "default" or first.fc_mode != mode or first.rep != 0:
            continue
        if case.gold.missing_required:
            # A partial call is the correct answer here; "missing argument" feedback would
            # push the model to fabricate the value.
            continue
        if session.out_of_budget():
            session.skipped_budget += 1
            continue
        error = _validation_error(session, first)
        if error is None:
            continue
        previous = first.completion.content or json.dumps(
            first.completion.tool_calls, ensure_ascii=False
        )
        feedback = (
            f"Tu respuesta anterior no es válida: {error}. "
            "Corrígela y responde de nuevo siguiendo exactamente el formato indicado."
        )

        def with_feedback(
            request: PromptRequest, previous: str = previous, feedback: str = feedback
        ) -> PromptRequest:
            messages = [
                *request.messages,
                {"role": "assistant", "content": previous},
                {"role": "user", "content": feedback},
            ]
            return request.model_copy(update={"messages": messages})

        run_case(session, case, mode, arm="retry", transform=with_feedback)


def run_pass_k(session: Session, cases: list[Case], mode: FcMode) -> None:
    """Reliability under the model's recommended sampling: K seeded repetitions per case."""
    subset = sorted(cases, key=lambda c: (c.priority, c.case_id))[:PASS_K_CASES]
    for rep in range(PASS_K):
        sampling = {**session.model.sampling, "seed": 1234 + rep}
        run_cases(session, subset, mode, arm="passk", rep=rep, sampling=sampling)


def run_history_arms(session: Session, steps: list[Case], modes: Iterable[FcMode]) -> None:
    """Teacher-forced dialogue steps with state in code vs. the full transcript in the prompt."""
    arms = {
        "state_summary": lambda c: c.model_copy(update={"history": []}),
        "history_full": lambda c: c.model_copy(update={"state_summary": None}),
    }
    for arm, strip in arms.items():
        variants = [strip(step) for step in steps]
        for index, mode in enumerate(modes):
            # extract/answer prompts do not depend on the FC mode: run them once.
            selected = [c for c in variants if c.call_type == "route" or index == 0]
            run_cases(session, selected, mode, arm=arm)


class _Recorder:
    """LLMBackend wrapper measuring every call the free-run driver makes, in order."""

    def __init__(self, session: Session) -> None:
        self.session = session
        self.records: list[RequestRecord] = []

    def complete(self, request: PromptRequest) -> Completion:
        if self.session.model.thinking == "always":
            request = request.model_copy(
                update={"max_tokens": request.max_tokens + THINKING_EXTRA_TOKENS}
            )
        record = run_request(
            self.session.client,
            self.session.probe,
            self.session.host_probe,
            request,
            self.session.template(suite="dialogues", case_id="pending", arm="free_run"),
        )
        self.records.append(record)
        self.session.check_alive(record.completion)
        return record.completion


def run_free_dialogues(
    session: Session,
    dialogues: list[Dialogue],
    mode: FcMode,
    *,
    guards: bool = False,
    answer_mode: AnswerMode = "generate",
) -> None:
    """Free-run arm: the FSM is driven by the model's own outputs; errors compound.

    Arms: `free_run` (as in r1), `free_run_guarded` (code guards on), and
    `free_run_extractive` (guards on, answers are the tool passages verbatim).
    """
    if answer_mode == "extractive":
        arm = "free_run_extractive"
    else:
        arm = "free_run_guarded" if guards else "free_run"
    finished = {
        str(key[0]).split(":")[0] for key in session.done if key[2] == arm and key[3] == mode
    }
    for index, dialogue in enumerate(dialogues):
        if dialogue.dialogue_id in finished:
            continue
        if session.out_of_budget():
            session.skipped_budget += len(dialogues) - index
            return
        recorder = _Recorder(session)
        steps = run_dialogue(
            dialogue,
            recorder,
            session.world,
            mode,
            guards=guards or answer_mode == "extractive",
            answer_mode=answer_mode,
            extract_layout=EXTRACT_LAYOUT,
            route_scope=ROUTE_SCOPE,
        )
        measured = iter(recorder.records)
        for step in steps:
            base = next(measured) if step.kind == "llm" else None
            fields: dict[str, Any] = {
                # The recorder stamps a placeholder arm on model calls; the real arm wins here.
                "arm": arm,
                "case_id": f"{dialogue.dialogue_id}:t{step.turn_index}:s{step.step_index}",
                "fc_mode": mode,
                "call_type": step.call_type,
                "fsm_state": step.state_before,
                "parsed": step.parsed,
                "tags": {
                    "dialogue_id": dialogue.dialogue_id,
                    "turn_index": step.turn_index,
                    "step_index": step.step_index,
                    "depth": dialogue.depth,
                    "kind": step.kind,
                    "note": step.note,
                },
                "next_state": step.state_after,
                "path": step.path,
                "executed_call": step.executed_call.model_dump() if step.executed_call else None,
            }
            if base is None:  # code-only step (confirmation, execution): no model call
                record = RequestRecord.model_validate(
                    session.template(
                        suite="dialogues",
                        ts=_now(),
                        completion=Completion(),
                        **fields,
                    )
                )
            else:
                record = RequestRecord.model_validate({**base.model_dump(), **fields})
            session.emit(record)


def run_prefix_experiment(session: Session, cases: list[Case], n: int = 12) -> None:
    """Prompt-cache effect of prompt ordering on one context bundle.

    `prefix_stable` keeps the question last (the shared context is reused across questions);
    `prefix_dynamic` puts the question first, which invalidates the cached prefix every turn.
    """
    two_k = [c for c in cases if c.context_level == "2k" and c.bundle_id]
    if not two_k:
        return
    bundle = sorted({c.bundle_id for c in two_k})[0]
    subset = sorted((c for c in two_k if c.bundle_id == bundle), key=lambda c: c.case_id)[:n]

    def question_first(request: PromptRequest) -> PromptRequest:
        messages = [dict(m) for m in request.messages]
        question = messages[-1]["content"]
        messages[0]["content"] = f"Consulta actual: {question}\n\n{messages[0]['content']}"
        return request.model_copy(update={"messages": messages})

    for arm, transform in (("prefix_stable", None), ("prefix_dynamic", question_first)):
        erase = getattr(session.client, "erase_slot", None)
        if callable(erase):
            erase()
        for case in subset:
            if session.out_of_budget():
                return
            run_case(session, case, "uniform", arm=arm, transform=transform)


# ----------------------------------------------------------------------------- batches


def batch_b0(run_id: str, models: list[ModelConfig], budget_min: float | None) -> None:
    """Contract smoke: does each model load, parse tool calls and keep thinking off?"""
    cases = load_cases("smoke")
    for model in models:
        # Verbosity 5 logs which tool-call handler llama.cpp selected. It slows requests,
        # so it is used only here and B0 latencies are never reported.
        with model_session(run_id, "B0", model, log_verbosity=5, budget_min=budget_min) as session:
            if session is None:
                continue
            for mode in ROUTE_MODES:
                run_cases(session, cases, mode)


# Context window the phone app would actually run with. The server default (12288) only
# exists to fit the 8k stress sweeps; its KV cache alone pushes 4B models past the 4 GiB
# limit, so batches whose prompts stay under ~2k tokens use this instead.
DEPLOY_CTX = 4096

# (dir suffix, profile name, profile, threads, protocol calls)
SpeedLaunch = tuple[str, str, HardwareProfile, int | None, list[dict[str, Any]]]


def batch_b1(run_id: str, models: list[ModelConfig], budget_min: float | None) -> None:
    """Speed screening on the main profile: enough to rank and filter every model cheaply.

    Covers the realistic context range only (<= 2k). Long contexts, the second profile,
    the thread sweep and sustained load cost ~5x more and run in B1F on the survivors.
    """
    profile = load_profiles().profiles[MAIN_PROFILE]
    call = {"levels": ("0.5k", "1k", "2k"), "reps": 2, "sustained_n": 0}
    launch: SpeedLaunch = ("@c4k", MAIN_PROFILE, profile, None, [call])
    _run_speed_launches(run_id, "B1", models, [launch], budget_min, ctx_size=DEPLOY_CTX)


def batch_b1_full(run_id: str, models: list[ModelConfig], budget_min: float | None) -> None:
    """Full speed protocol: all context levels, both profiles, threads, sustained load."""
    profiles = load_profiles().profiles
    small, large = ("0.5k", "1k", "2k"), ("4k", "8k")
    launches: list[SpeedLaunch] = [
        (
            "",
            MAIN_PROFILE,
            profiles[MAIN_PROFILE],
            None,
            [
                {"levels": small, "reps": 3, "sustained_n": 30},
                {"levels": large, "reps": 2, "sustained_n": 0, "output_lengths": ()},
            ],
        ),
        (
            "@phone-nominal",
            "phone-nominal",
            profiles["phone-nominal"],
            None,
            [{"levels": (*small, *large), "reps": 2, "sustained_n": 0}],
        ),
    ]
    sweep = {"levels": ("1k",), "reps": 3, "sustained_n": 0, "output_lengths": (64,)}
    for threads in (1, 2):
        launches.append(
            (f"@t{threads}", MAIN_PROFILE, profiles[MAIN_PROFILE], threads, [sweep])
        )  # fmt: skip
    launches.append(("@smt-t8", "host-smt", SMT_PROFILE, None, [sweep]))
    _run_speed_launches(run_id, "B1F", models, launches, budget_min)


def _run_speed_launches(
    run_id: str,
    batch: str,
    models: list[ModelConfig],
    launches: list[SpeedLaunch],
    budget_min: float | None,
    ctx_size: int | None = None,
) -> None:
    from nevados_bench.suites.speed import text_source

    source = text_source(load_world())
    for model in models:
        for suffix, profile_name, profile, threads, calls in launches:
            with model_session(
                run_id,
                batch,
                model,
                profile_name,
                profile=profile,
                threads=threads,
                dir_suffix=suffix,
                budget_min=budget_min,
                ctx_size=ctx_size,
            ) as session:
                if session is None:
                    break  # does not load under the tight profile: skip its other launches
                if session.done:
                    continue  # the speed protocol is not resumable mid-way; keep what exists
                for call in calls:
                    run_speed_protocol(
                        session.client,
                        session.probe,
                        session.host_probe,
                        source,
                        session.template(),
                        threads=session.identity["threads"],
                        sink=session.emit,
                        **call,
                    )


def batch_b6(run_id: str, models: list[ModelConfig], budget_min: float | None) -> None:
    """Device anchor speed run: realistic contexts, more reps, and 30 sustained turns.

    Meant for `--target phone`; on the laptop it is just a longer B1 at DEPLOY_CTX.
    """
    profile = load_profiles().profiles[MAIN_PROFILE]
    call = {"levels": ("0.5k", "1k", "2k"), "reps": 3, "sustained_n": 30}
    launch: SpeedLaunch = ("@c4k", MAIN_PROFILE, profile, None, [call])
    _run_speed_launches(run_id, "B6", models, [launch], budget_min, ctx_size=DEPLOY_CTX)


def batch_b7(run_id: str, models: list[ModelConfig], budget_min: float | None) -> None:
    """Free-run dialogues without and with the code guards (uniform mode, deploy context).

    The two arms alternate per dialogue so a time budget cuts both at the same point and
    the comparison stays paired. r1 never measured free-run dialogues.
    """
    dialogues = load_dialogues()
    for model in models:
        with model_session(
            run_id, "B7", model, budget_min=budget_min, ctx_size=DEPLOY_CTX
        ) as session:
            if session is None:
                continue
            for dialogue in dialogues:
                for guards in (False, True):
                    run_free_dialogues(session, [dialogue], "uniform", guards=guards)
                if session.out_of_budget():
                    break


def batch_b8(run_id: str, models: list[ModelConfig], budget_min: float | None) -> None:
    """Free-run dialogues with guards and extractive answers (no answer-generation call)."""
    dialogues = load_dialogues()
    for model in models:
        with model_session(
            run_id, "B8", model, budget_min=budget_min, ctx_size=DEPLOY_CTX
        ) as session:
            if session is None:
                continue
            run_free_dialogues(session, dialogues, "uniform", answer_mode="extractive")


def batch_b2(run_id: str, models: list[ModelConfig], budget_min: float | None) -> None:
    """Single-turn function calling at the baseline context, native and uniform."""
    cases = load_cases("fc_core")
    for model in models:
        with model_session(
            run_id, "B2", model, budget_min=budget_min, ctx_size=DEPLOY_CTX
        ) as session:
            if session is None:
                continue
            for mode in ROUTE_MODES:
                run_cases(session, cases, mode)


def batch_b3(run_id: str, models: list[ModelConfig], budget_min: float | None) -> None:
    """Function-calling stress: tool count, context volume, grammar off, retry, pass^k."""
    core = load_cases("fc_core")
    tools_sweep = load_cases("fc_tools_sweep")
    ctx_sweep = load_cases("fc_ctx_sweep")
    for model in models:
        with model_session(run_id, "B3", model, budget_min=budget_min) as session:
            if session is None:
                continue
            for mode in ROUTE_MODES:
                run_cases(session, tools_sweep, mode)
                run_cases(session, ctx_sweep, mode)
            run_cases(session, core, "uniform_free")
            b2_records = RESULTS_DIR / run_id / "B2" / model.id / "requests.jsonl"
            run_retries(session, core, "native", b2_records)
            own_records = RESULTS_DIR / run_id / "B3" / model.id / "requests.jsonl"
            run_retries(session, core, "uniform_free", own_records)
            run_pass_k(session, core, "uniform")


def batch_b4(run_id: str, models: list[ModelConfig], budget_min: float | None) -> None:
    """Dialogues on the FSM: teacher-forced arms, free run, and the prompt-cache experiment."""
    dialogues = load_dialogues()
    steps = dialogue_step_cases(dialogues)
    grounded = load_cases("grounded_qa")
    for model in models:
        with model_session(run_id, "B4", model, budget_min=budget_min) as session:
            if session is None:
                continue
            run_history_arms(session, steps, ROUTE_MODES)
            for mode in ROUTE_MODES:
                run_free_dialogues(session, dialogues, mode)
            if model.grounded_qa:
                run_prefix_experiment(session, grounded)


def batch_b5(run_id: str, models: list[ModelConfig], budget_min: float | None) -> None:
    """Grounded answers under growing context: hallucination, abstention, lures."""
    cases = load_cases("grounded_qa")
    for model in models:
        if not model.grounded_qa:
            continue
        with model_session(run_id, "B5", model, budget_min=budget_min) as session:
            if session is None:
                continue
            run_bundled(session, cases)


BATCHES: dict[str, Callable[[str, list[ModelConfig], float | None], None]] = {
    "B0": batch_b0,
    "B1": batch_b1,
    "B1F": batch_b1_full,
    "B2": batch_b2,
    "B3": batch_b3,
    "B4": batch_b4,
    "B5": batch_b5,
    "B6": batch_b6,
    "B7": batch_b7,
    "B8": batch_b8,
}
