"""Export everything the TypeScript port in ``mobile/`` needs, so it never reads Python.

Writes (run: ``uv run python -m nevados_bench.export_mobile``):

- ``mobile/assets/data/world.json``: world data plus every constant the FSM, prompts,
  guards and values modules hardcode.
- ``mobile/src/core/__fixtures__/prompts.json``: ``{case, request}`` pairs, the spec for
  ``buildRequest``.
- ``mobile/src/core/__fixtures__/replays.json``: free-run driver replays driven by an
  oracle backend, the spec for ``DialogueRun``.

Both fixtures are generated from the Python implementation: never edit them by hand.
"""

from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path
from typing import Any

from nevados_bench.finetune import generate as G
from nevados_bench.fsm import driver as D
from nevados_bench.fsm import parse as PARSE
from nevados_bench.fsm import prompts as PR
from nevados_bench.fsm import states as S
from nevados_bench.guards import (
    _CITIES,
    _COUNT_RE,
    _COUNT_WORDS,
    _DATE_RE,
    _DAYS,
    _DAYS_EN,
    _GENERIC_WORDS,
    _MONTH_WORDS,
    _MONTHS,
    _PEOPLE,
    _VISITOR_RE,
    CHECKED_ARGS,
    FUZZY_MIN_CHARS,
    FUZZY_RATIO,
    SAFETY_REFERRAL_ES,
)
from nevados_bench.schemas import CONTEXT_LEVEL_TOKENS, Case, Dialogue
from nevados_bench.scoring.grounding import _ENUM_LINE, _ENUM_PAREN, SMALL_NUMBER_LIMIT
from nevados_bench.values import (
    _ABSTAIN_PATTERNS,
    _CITATION_RE,
    _NUMBER_RE,
    _TIME_RE,
    ABSTAIN_EN,
    ABSTAIN_ES,
)
from nevados_bench.world import PARK_NAME, World, load_world
from nevados_bench.world import model as WM
from nevados_bench.world.corpus import INJECTION_FIELD, stable_hash

# ----------------------------------------------------------------------------- world.json

# Declarative form of ``World.execute_tool`` for the 24 base tools (clones return empty
# results). ``st``: station passage fields, then ``park``: park keys (-> exec.park_passages).
# tests/test_export_mobile.py interprets this table and compares it with the Python result.
_EXEC_RULES: dict[str, dict[str, Any]] = {
    "get_opening_hours": {"st": ["opening_hours", "last_entry"]},
    "get_station_altitude": {"st": ["altitude_m"]},
    "get_station_services": {"st": ["services"]},
    "get_transport_options": {"st": ["transport"]},
    "get_entry_fee": {"fee_by_visitor_type": True},
    "get_entry_requirements": {
        "st": ["minimum_age"],
        "park": ["insurance", "guide_requirement"],
    },
    "check_daily_capacity": {
        "st": ["daily_capacity"],
        "data": {"key": "cupos_disponibles", "kind": "hash_mod4_nonzero"},
    },
    "list_trails": {
        "st": ["trail"],
        "data": {"key": "senderos", "kind": "station_trail_ids"},
    },
    "get_trail_details": {"trail_passage": True},
    "get_trail_conditions": {
        "trail_passage": True,
        "data": {"key": "estado", "kind": "hash_choice", "choices": "trail_status"},
    },
    "get_required_gear": {"st": ["required_gear"], "park": ["sunscreen"]},
    "get_weather_forecast": {
        "st": ["weather_window"],
        "data": {"key": "pronostico", "kind": "hash_choice", "choices": "forecast"},
    },
    "get_weather_window": {"st": ["weather_window"]},
    "get_park_rules": {
        "st": ["max_group_size", "prohibition"],
        "park": ["drones", "pets", "camping"],
    },
    "check_item_allowed": {
        "item_rule": True,
        "data": {"key": "permitido", "kind": "item_allowed"},
    },
    "get_flora_fauna_info": {"st": ["flora_fauna"]},
    "list_protected_species": {"st": ["wildlife_distance"]},
    "get_altitude_sickness_protocol": {"st": ["altitude_sickness_protocol", "oxygen_point"]},
    "get_acclimatization_advice": {
        "park": ["acclimatization", "max_visitor_altitude"],
        "data": {"key": "altitud_permitida", "kind": "altitude_limit", "passage_id": "PAR-08"},
    },
    "find_nearest_shelter": {"st": ["storm_shelter"], "park": ["lightning_protocol"]},
    "get_emergency_contacts": {
        "st": ["emergency_phone", "radio_channel"],
        "park": ["rescue_line", "police_contact", "fire_brigade"],
    },
    "get_emergency_procedure": {"procedure_by_emergency_type": True},
    "report_emergency": {
        "st": ["emergency_phone", "emergency_procedure"],
        "data": {"key": "codigo_reporte", "kind": "letter_code", "prefix": "EMG"},
    },
    "register_visit": {
        "st": ["daily_capacity"],
        "data": {"key": "codigo_registro", "kind": "letter_code", "prefix": "REG"},
    },
}

# emergency_type -> passages, each {"st": field} or {"park": key}, in World._procedure_passages
# order.
_PROCEDURES: dict[str, list[dict[str, str]]] = {
    "mal_de_altura": [{"st": "altitude_sickness_protocol"}],
    "hipotermia": [{"park": "hypothermia_protocol"}],
    "lesion": [{"st": "emergency_procedure"}],
    "persona_perdida": [{"park": "lost_person_protocol"}],
    "tormenta_electrica": [{"park": "lightning_protocol"}, {"st": "storm_shelter"}],
    "incendio": [{"park": "fire_brigade"}],
}

# Texts whose sha256-based stable_hash a TS implementation must reproduce (decimal strings:
# the values exceed 2**53).
_HASH_SAMPLES = [
    "",
    "a",
    "ñandú",
    "check_daily_capacity|[('station', 'alto_cenizo')]",
    "get_trail_conditions|[('trail_id', 'sendero_mirlo')]",
    "register_visit|[('date', '2026-12-03'), ('group_size', 4), ('station', 'valle_bruma')]",
]


def _rx(pattern: re.Pattern[str]) -> dict[str, str]:
    flags = ("i" if pattern.flags & re.IGNORECASE else "") + (
        "s" if pattern.flags & re.DOTALL else ""
    )
    return {"source": pattern.pattern, "flags": flags}


def _passage_index(world: World) -> dict[str, list[str]]:
    # Key "<station or ''>|<field>"; injection passages are never indexed (see load_world).
    return {
        f"{station or ''}|{field_name}": list(ids)
        for (station, field_name), ids in world._by_field.items()
    }


def build_world_json(world: World) -> dict[str, Any]:
    slot_names = list(
        dict.fromkeys(n for t in world.tools.values() for n in t.parameters.get("properties", {}))
    )
    base_tools = world.base_tools
    missing_rules = set(base_tools) - set(_EXEC_RULES)
    if missing_rules:
        raise RuntimeError(f"export rules missing for tools: {sorted(missing_rules)}")
    return {
        "meta": {
            "park_name": PARK_NAME,
            "reference_date": PR.REFERENCE_DATE,
            "chars_per_token": PR.CHARS_PER_TOKEN,
            "suffix_allowance_tokens": PR.SUFFIX_ALLOWANCE_TOKENS,
            "max_tokens": PR.MAX_TOKENS,
            "context_level_tokens": CONTEXT_LEVEL_TOKENS,
            "partial_tag": PR.PARTIAL_TAG,
            "injection_field": INJECTION_FIELD,
        },
        "stations": [
            {"id": s.id, "name": s.name, "code": s.code, "trails": [t.id for t in s.trails]}
            for s in world.stations.values()
        ],
        "trails": [
            {
                "id": t.id,
                "name": t.name,
                "station": t.station,
                "length_m": t.length_m,
                "duration_min": t.duration_min,
                "difficulty": t.difficulty,
            }
            for t in world.trails.values()
        ],
        "tools": [t.model_dump(mode="json") for t in world.tools.values()],
        "base_tools": base_tools,
        "passages": [p.model_dump(mode="json") for p in world.passages.values()],
        "filler": [p.model_dump(mode="json") for p in world.filler.values()],
        "gazetteer": [g.model_dump(mode="json") for g in world.gazetteer],
        "passage_index": _passage_index(world),
        "slot_schemas": {name: world.slot_schema(name) for name in slot_names},
        "exec": {
            "park_passages": WM._PARK,
            "item_rules": {
                item: {"passage_id": pid, "allowed": allowed}
                for item, (pid, allowed) in WM._ITEM_RULES.items()
            },
            "fee_field": WM._FEE_FIELD,
            "trail_status": WM._TRAIL_STATUS,
            "forecast": WM._FORECAST,
            "procedures": _PROCEDURES,
            "rules": _EXEC_RULES,
            "hash_vectors": [{"text": t, "value": str(stable_hash(t))} for t in _HASH_SAMPLES],
        },
        "states": {
            "all": list(S.STATES),
            "topic": list(S.TOPIC_STATES),
            "transitions": {k: sorted(v) for k, v in S.TRANSITIONS.items()},
            "flow_state": S.FLOW_STATE,
            "required_slots": S.REQUIRED_SLOTS,
            "slot_labels": S.SLOT_LABELS,
            "slot_questions": S.SLOT_QUESTIONS,
            "tool_labels": S.TOOL_LABELS,
            "visible_tools": {s: S.visible_tools(world, s) for s in S.STATES},
            "tool_topic": {name: S.tool_topic(world, name) for name in world.tools},
        },
        "prompts": {
            "intro": PR._intro(world),
            "route_rules": PR._ROUTE_RULES,
            "uniform_format": PR._UNIFORM_FORMAT,
            "extract_rules": PR._EXTRACT_RULES,
            "answer_rules": PR._ANSWER_RULES,
        },
        "values": {
            "abstain_es": ABSTAIN_ES,
            "abstain_en": ABSTAIN_EN,
            "abstain_patterns": list(_ABSTAIN_PATTERNS),
            "time_re": _rx(_TIME_RE),
            "number_re": _rx(_NUMBER_RE),
            "citation_re": _rx(_CITATION_RE),
        },
        "parse": {
            "think_re": _rx(PARSE._THINK_RE),
            "tool_markup_re": _rx(PARSE._TOOL_MARKUP_RE),
        },
        "grounding": {
            "small_number_limit": SMALL_NUMBER_LIMIT,
            "enum_line_re": _rx(_ENUM_LINE),
            "enum_paren_re": _rx(_ENUM_PAREN),
        },
        "guards": {
            "safety_referral_es": SAFETY_REFERRAL_ES,
            "fuzzy_ratio": FUZZY_RATIO,
            "fuzzy_min_chars": FUZZY_MIN_CHARS,
            "generic_words": sorted(_GENERIC_WORDS),
            # Inline literals of guards._short_name / guards._negated.
            "short_name_prefixes": [
                "estacion ",
                "sendero del ",
                "sendero de la ",
                "sendero de ",
                "sendero ",
            ],
            "negation_tokens": ["no", "not", "ni"],
            "negation_exception": "sino",
            "negation_window": 3,
            "checked_args": list(CHECKED_ARGS),
            "months": _MONTHS.split("|"),
            "days": _DAYS.split("|"),
            "days_en": _DAYS_EN.split("|"),
            "month_words": _MONTH_WORDS,
            "cities": _CITIES.split("|"),
            "count_words": _COUNT_WORDS.split("|"),
            "people_words": _PEOPLE.split("|"),
            "date_re": _rx(_DATE_RE),
            "visitor_re": _rx(_VISITOR_RE),
            "count_re": _rx(_COUNT_RE),
        },
        "driver": {
            "affirm": sorted(D._AFFIRM),
            "affirm_max_tokens": 4,
            "cancel": list(D._CANCEL),
            "fallback": D._FALLBACK,
            "correction_re": _rx(D._CORRECTION_RE),
            "templates": {
                "slot_cancel_reply": "Listo, cancelé el trámite. ¿En qué más te puedo ayudar?",
                "confirm_cancel_reply": "Entendido, no envié nada. ¿En qué más te puedo ayudar?",
                "confirm": (
                    "Voy a enviar {label} con estos datos: {details}. ¿Confirmas? Responde sí o no."
                ),
                "done": "Listo, quedó enviado {label}. Código: {code}.",
                "failed": "No se pudo completar el trámite: {error}",
                "summary_flow": "Trámite en curso: {tool}.",
                "summary_given": "Datos ya recibidos: {given}.",
                "summary_given_none": "ninguno",
                "summary_pending": "Dato pendiente: {pending}.",
                "summary_tool_result": "Resultado de la herramienta: ",
                "state_summary_header": "[Estado del trámite]\n",
                "user_message_header": "[Mensaje del usuario]\n",
                "slot_requested_header": "[Dato solicitado]\n",
            },
        },
    }


# ----------------------------------------------------------------------------- prompts.json


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _prompt_entry(case: Case, world: World) -> dict[str, Any]:
    request = PR.build_request(case, world, "uniform")
    return {
        "case": case.model_dump(mode="json"),
        "request": request.model_dump(mode="json", exclude_none=True),
    }


def build_prompts(
    world: World, suites_dir: Path, grounded_sample: int | None
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    cases: list[Case] = []
    counts: dict[str, int] = {}
    for name in ("fc_core", "smoke"):
        got = [Case.model_validate(r) for r in _read_jsonl(suites_dir / f"{name}.jsonl")]
        counts[name] = len(got)
        cases += got
    steps = [
        step
        for r in _read_jsonl(suites_dir / "dialogues.jsonl")
        for turn in Dialogue.model_validate(r).turns
        for step in turn.steps
    ]
    counts["dialogue_steps"] = len(steps)
    cases += steps
    grounded = [Case.model_validate(r) for r in _read_jsonl(suites_dir / "grounded_qa.jsonl")]
    if grounded_sample is not None and grounded_sample < len(grounded):
        # Deterministic even stride keeps every question type represented.
        stride = len(grounded) / grounded_sample
        grounded = [grounded[int(i * stride)] for i in range(grounded_sample)]
    counts["grounded_qa"] = len(grounded)
    cases += grounded
    return [_prompt_entry(c, world) for c in cases], counts


# ----------------------------------------------------------------------------- replays.json


def _dump(obj: Any) -> Any:
    return None if obj is None else obj.model_dump(mode="json", exclude_none=True)


def _step_json(step: Any) -> dict[str, Any]:
    return {
        "turn_index": step.turn_index,
        "step_index": step.step_index,
        "kind": step.kind,
        "call_type": step.call_type,
        "path": step.path,
        "note": step.note,
        "assistant_message": step.assistant_message,
        "executed_call": _dump(step.executed_call),
        "tool_result": step.tool_result,
        "slots": step.slots,
        "request": _dump(step.request),
        "completion_content": step.completion.content if step.completion else None,
    }


def _replay(
    world: World,
    dialogue: Dialogue,
    outputs: list[tuple[str, str]],
    config: dict[str, Any],
    source: str,
) -> dict[str, Any] | None:
    """One oracle-driven run; None when the oracle and the driver disagree."""
    rec = G.Recorder(outputs)
    run = D.DialogueRun(
        dialogue,
        rec,
        world,
        "uniform",
        guards=config["guards"],
        device_station=config["device_station"],
        answer_mode=config["answer_mode"],
    )
    replies = []
    try:
        for index, turn in enumerate(dialogue.turns):
            run.turn_index = index
            if turn.steps:
                run.language = turn.steps[0].language
            replies.append(run.turn(turn.user_message))
    except (ValueError, AssertionError, KeyError):
        return None
    if rec.desync or rec.outputs:
        return None
    return {
        "id": dialogue.dialogue_id,
        "source": source,
        "config": config,
        "user_messages": [t.user_message for t in dialogue.turns],
        "assistant_messages": replies,
        "oracle_outputs": [{"call_type": k, "content": c} for k, c in outputs],
        "steps": [_step_json(s) for s in run.steps],
        "final_state": run.state,
        "final_flow": (
            {"tool": run.flow.tool, "slots": run.flow.slots, "pending": run.flow.pending}
            if run.flow
            else None
        ),
    }


def _gold_outputs(dialogue: Dialogue) -> list[tuple[str, str]]:
    return [
        G._target_for(s)
        for t in dialogue.turns
        for s in t.steps
        if s.call_type in ("route", "extract")
    ]


_BASE_CONFIG = {"guards": True, "answer_mode": "extractive", "device_station": None}
_SUITE_VARIANTS = [
    _BASE_CONFIG,
    {"guards": False, "answer_mode": "extractive", "device_station": None},
    {"guards": True, "answer_mode": "extractive", "device_station": "laguna_espejo"},
]


def build_replays(
    world: World, suites_dir: Path, n_random: int, n_single: int, n_suite: int | None = None
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    replays: list[dict[str, Any]] = []
    stats: dict[str, int] = {}

    def keep(source: str, rep: dict[str, Any] | None, tag: str) -> None:
        key = f"{source}:{tag}"
        stats[f"{key}:{'kept' if rep else 'dropped'}"] = (
            stats.get(f"{key}:{'kept' if rep else 'dropped'}", 0) + 1
        )
        if rep:
            replays.append(rep)

    for line in _read_jsonl(suites_dir / "dialogues.jsonl")[:n_suite]:
        dialogue = Dialogue.model_validate(line)
        outputs = _gold_outputs(dialogue)
        for config in _SUITE_VARIANTS:
            tag = f"g{int(config['guards'])}_{config['device_station'] or 'nodev'}"
            keep("suite", _replay(world, dialogue, outputs, config, "suite"), tag)

    # Same loop and RNG consumption as finetune.generate.main (seed 123).
    rng = random.Random(123)
    sb = G.ScriptBuilder(rng, world)
    kept = attempts = 0
    while kept < n_random and attempts < n_random * 20:
        i, attempts = attempts, attempts + 1
        en = rng.random() < 0.1
        script = sb.flow_script(en) if rng.random() < 0.6 else sb.info_script(en)
        if not script:
            continue
        try:
            trace = G._TrainSim(world, f"t{i:05d}", tuple(script)).run()
        except (ValueError, AssertionError, KeyError):
            stats["random:sim_error"] = stats.get("random:sim_error", 0) + 1
            continue
        rep = _replay(world, trace.dialogue, _gold_outputs(trace.dialogue), _BASE_CONFIG, "random")
        keep("random", rep, "base")
        kept += bool(rep)

    # One-message dialogues cover clarify / none routes, which suite dialogues never use.
    rng = random.Random(123)
    sb = G.ScriptBuilder(rng, world)
    kept = attempts = 0
    while kept < n_single and attempts < n_single * 20:
        i, attempts = attempts, attempts + 1
        got = G.single_turn(world, rng, sb)
        if not got:
            continue
        ex = got[0]
        dialogue = Dialogue(
            dialogue_id=f"single{i:04d}",
            depth=1,
            phenomena=[],
            turns=[{"user_message": ex["messages"][-1]["content"], "steps": []}],  # type: ignore[list-item]
        )
        rep = _replay(world, dialogue, [(ex["call_type"], ex["target"])], _BASE_CONFIG, "single")
        keep("single", rep, "base")
        kept += bool(rep)
    return replays, stats


# ----------------------------------------------------------------------------- entry point


def _write(path: Path, data: Any, indent: int | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    separators = None if indent else (",", ":")
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=indent, separators=separators) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {path} ({path.stat().st_size / 1e6:.2f} MB)")


def export(
    out_dir: Path = Path("mobile"),
    suites_dir: Path = Path("data/suites"),
    *,
    n_random: int = 80,
    n_single: int = 20,
    n_suite: int | None = None,
    grounded_sample: int | None = None,
) -> dict[str, Any]:
    world = load_world()
    _write(out_dir / "assets/data/world.json", build_world_json(world), indent=1)
    fixtures = out_dir / "src/core/__fixtures__"
    prompts, prompt_counts = build_prompts(world, suites_dir, grounded_sample)
    _write(fixtures / "prompts.json", prompts)
    replays, replay_stats = build_replays(world, suites_dir, n_random, n_single, n_suite)
    _write(fixtures / "replays.json", replays)
    summary = {"prompts": len(prompts), "replays": len(replays)}
    print(json.dumps({**summary, **prompt_counts, **replay_stats}, indent=1, sort_keys=True))
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out-dir", type=Path, default=Path("mobile"))
    ap.add_argument("--suites-dir", type=Path, default=Path("data/suites"))
    ap.add_argument("--n-random", type=int, default=80)
    ap.add_argument("--n-single", type=int, default=20)
    ap.add_argument("--grounded-sample", type=int, default=None)
    args = ap.parse_args()
    export(
        args.out_dir,
        args.suites_dir,
        n_random=args.n_random,
        n_single=args.n_single,
        grounded_sample=args.grounded_sample,
    )


if __name__ == "__main__":
    main()
