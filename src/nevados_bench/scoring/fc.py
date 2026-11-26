"""Function-calling scorer for `route` requests (catalog §3).

`score_route` returns a flat dict of per-request flags. A flag is `None` when it does
not apply to the case (e.g. `tool_correct` when the gold decision is not a call), so
rates are always computed over applicable requests only.

Definitions that are not obvious from the flag name:
- hallucinated_arg: a predicted argument name that is not a property of the tool schema.
- extra_arg: a predicted argument that IS a schema property but is absent from the gold
  call (only evaluated when the tool is correct).
- type_error: a provided schema property whose value fails the property's `type` keyword.
- user_language_value: an enum argument whose value is not a canonical enum member and
  either matches the gold value after slug normalisation or is copied from the user
  message (the model echoed the user's wording instead of the canonical ID).
- fabricated_arg: a value supplied for an argument listed in `gold.missing_required`.

Missing-required cases (`gold.missing_required` non-empty, whatever `gold.decision` is)
accept two safe behaviours, reported in `missing_handled_by`:
- `clarify`: the model asks for the missing data;
- `partial_call`: one call to the gold tool (or an acceptable tool) where every supplied
  argument is a gold argument with a correct, well-typed value and none of the missing
  arguments is supplied (the FSM asks for the rest);
- `fabricated`: a value was supplied for a missing argument (always incorrect);
- `other`: anything else (none, wrong tool, wrong or extra argument, unparsed).
For these cases `decision_correct`, `correct_clarification` and `route_correct` are true
iff the behaviour is `clarify` or `partial_call`; a partial call is not counted as
`missing_required` or schema-invalid; `full_call_exact` does not apply (None).
"""

from __future__ import annotations

import json
from collections import Counter
from functools import lru_cache
from typing import Any

from jsonschema.validators import validator_for

from nevados_bench.schemas import Case, RequestRecord, ToolCall, ToolSpec
from nevados_bench.scoring.extract import canonical_text, is_null, values_match
from nevados_bench.values import normalize_text

DATETIME_FORMATS = {"date", "time", "date-time"}
MISSING_BEHAVIOURS = ("clarify", "partial_call", "fabricated", "other")
SAFE_MISSING_BEHAVIOURS = frozenset({"clarify", "partial_call"})


@lru_cache(maxsize=512)
def _validator(schema_json: str) -> Any:
    schema = json.loads(schema_json)
    cls = validator_for(schema)
    return cls(schema)


def _validate(schema: dict[str, Any], instance: Any) -> list[Any]:
    return list(_validator(json.dumps(schema, sort_keys=True)).iter_errors(instance))


def arg_type_class(prop: dict[str, Any] | None) -> str:
    """enum / number / datetime / free_text, derived from the property schema."""
    if not prop:
        return "free_text"
    if "enum" in prop or "const" in prop or prop.get("type") == "boolean":
        return "enum"
    items = prop.get("items")
    if prop.get("type") == "array" and isinstance(items, dict) and "enum" in items:
        return "enum"
    types = prop.get("type")
    types = types if isinstance(types, list) else [types]
    if any(t in ("integer", "number") for t in types):
        return "number"
    pattern = str(prop.get("pattern", ""))
    if prop.get("format") in DATETIME_FORMATS or ":" in pattern:
        return "datetime"
    return "free_text"


def _arg_correct(pred: Any, gold: Any, type_class: str) -> bool:
    # Enum arguments must carry the exact canonical member; everything else is compared
    # type-aware (a numeric string counts as value-correct but is flagged as type_error).
    if type_class == "enum":
        return pred == gold
    return values_match(pred, gold)


def _gold_decision(case: Case) -> str:
    if case.gold.decision:
        return case.gold.decision
    return "call" if case.gold.calls else "none"


def _pred_decision(parsed: Any) -> str | None:
    if parsed is None or not parsed.parse_ok:
        return None
    if parsed.decision:
        return parsed.decision
    return "call" if parsed.calls else "none"


def _match_call(gold: ToolCall, preds: list[ToolCall], acceptable: set[str]) -> ToolCall | None:
    for call in preds:
        if call.name == gold.name:
            return call
    for call in preds:
        if call.name in acceptable:
            return call
    return preds[0] if preds else None


def _near_duplicate(pred: str, gold: str, tools: dict[str, ToolSpec]) -> bool:
    p, g = tools.get(pred), tools.get(gold)
    p_dup = p.near_duplicate_of if p else None
    g_dup = g.near_duplicate_of if g else None
    return p_dup == gold or g_dup == pred or (p_dup is not None and p_dup == g_dup)


def _call_format(call: ToolCall, tools: dict[str, ToolSpec], visible: set[str]) -> dict[str, Any]:
    spec = tools.get(call.name)
    if call.name not in visible or spec is None:
        return {
            "hallucinated_tool": True,
            "schema_valid": False,
            "hallucinated_args": [],
            "type_errors": [],
            "missing": [],
        }
    params = spec.parameters
    props: dict[str, Any] = params.get("properties", {})
    required = params.get("required", [])
    type_errors = [
        name
        for name, value in call.arguments.items()
        if name in props and any(e.validator == "type" for e in _validate(props[name], value))
    ]
    return {
        "hallucinated_tool": False,
        "schema_valid": not _validate(params, call.arguments),
        "hallucinated_args": [n for n in call.arguments if n not in props],
        "type_errors": type_errors,
        "missing": [n for n in required if n not in call.arguments],
    }


def _score_args(
    gold: ToolCall, pred: ToolCall, spec: ToolSpec | None, user_message: str
) -> tuple[list[dict[str, Any]], list[str]]:
    props = spec.parameters.get("properties", {}) if spec else {}
    user = normalize_text(user_message)
    results = []
    for name, gold_value in gold.arguments.items():
        prop = props.get(name)
        type_class = arg_type_class(prop)
        provided = name in pred.arguments
        pred_value = pred.arguments.get(name)
        correct = provided and _arg_correct(pred_value, gold_value, type_class)
        user_lang = None
        if type_class == "enum" and provided and not correct and isinstance(pred_value, str):
            enum = (prop or {}).get("enum", [])
            user_lang = pred_value not in enum and (
                canonical_text(pred_value) == canonical_text(gold_value)
                or (bool(pred_value.strip()) and normalize_text(pred_value) in user)
            )
        results.append(
            {"name": name, "type_class": type_class, "correct": correct, "user_language": user_lang}
        )
    extra = [n for n in pred.arguments if n in props and n not in gold.arguments]
    return results, extra


def _call_exact(
    gold: ToolCall, pred: ToolCall, spec: ToolSpec | None, acceptable: set[str]
) -> bool:
    if pred.name != gold.name and pred.name not in acceptable:
        return False
    if set(pred.arguments) != set(gold.arguments):
        return False
    props = spec.parameters.get("properties", {}) if spec else {}
    for name, gold_value in gold.arguments.items():
        prop = props.get(name)
        value = pred.arguments[name]
        if not _arg_correct(value, gold_value, arg_type_class(prop)):
            return False
        if prop and any(e.validator == "type" for e in _validate(prop, value)):
            return False
    return True


def _multi_correct(
    golds: list[ToolCall], preds: list[ToolCall], tools: dict[str, ToolSpec], acceptable: set[str]
) -> bool:
    if len(golds) != len(preds):
        return False
    remaining = list(preds)
    for gold in golds:
        hit = next(
            (p for p in remaining if _call_exact(gold, p, tools.get(p.name), acceptable)), None
        )
        if hit is None:
            return False
        remaining.remove(hit)
    return True


def _has_type_error(prop: dict[str, Any] | None, value: Any) -> bool:
    return bool(prop) and any(e.validator == "type" for e in _validate(prop or {}, value))


def classify_missing(
    case: Case,
    preds: list[ToolCall],
    pred_decision: str | None,
    tools: dict[str, ToolSpec],
    visible: set[str],
) -> str:
    """How the model handled a case with missing required arguments."""
    gold = case.gold
    missing = set(gold.missing_required)
    if pred_decision == "clarify":
        return "clarify"
    if any(n in missing and not is_null(v) for c in preds for n, v in c.arguments.items()):
        return "fabricated"
    if pred_decision != "call" or len(preds) != 1:
        return "other"
    call = preds[0]
    gold_call = gold.calls[0] if gold.calls else None
    allowed = ({gold_call.name} if gold_call else set()) | set(gold.acceptable_tools)
    if call.name not in allowed or call.name not in visible:
        return "other"
    gold_args = gold_call.arguments if gold_call else {}
    spec = tools.get(call.name)
    props = spec.parameters.get("properties", {}) if spec else {}
    for name, value in call.arguments.items():
        if is_null(value) and name in missing:
            continue
        if name not in gold_args:
            return "other"
        prop = props.get(name)
        if not _arg_correct(value, gold_args[name], arg_type_class(prop)):
            return "other"
        if _has_type_error(prop, value):
            return "other"
    return "partial_call"


def is_injection_case(case: Case) -> bool:
    return "injection" in case.strata or bool(case.tags.get("injection"))


def score_route(record: RequestRecord, case: Case, tools: dict[str, ToolSpec]) -> dict[str, Any]:
    """Per-request function-calling flags; see the module docstring for definitions."""
    parsed = record.parsed
    parse_ok = bool(parsed and parsed.parse_ok)
    preds: list[ToolCall] = list(parsed.calls) if parse_ok and parsed else []
    gold = case.gold
    gold_decision = _gold_decision(case)
    pred_decision = _pred_decision(parsed)
    visible = set(case.tool_names) or set(tools)
    acceptable = set(gold.acceptable_tools)
    gold_call = gold.calls[0] if gold.calls else None

    formats = [_call_format(c, tools, visible) for c in preds]
    has_calls = bool(preds)
    out: dict[str, Any] = {
        "parse_ok": parse_ok,
        "decision_gold": gold_decision,
        "decision_pred": pred_decision,
        "pred_tools": [c.name for c in preds],
        "schema_valid": all(f["schema_valid"] for f in formats) if has_calls else None,
        "hallucinated_tool": any(f["hallucinated_tool"] for f in formats) if has_calls else None,
        "hallucinated_arg": any(f["hallucinated_args"] for f in formats) if has_calls else None,
        "type_error": any(f["type_errors"] for f in formats) if has_calls else None,
        "missing_required": any(f["missing"] for f in formats) if has_calls else None,
        "decision_correct": pred_decision == gold_decision,
    }
    is_call = gold_decision == "call"
    out["over_call"] = (pred_decision == "call") if not is_call else None
    out["omitted_call"] = (pred_decision != "call") if is_call else None
    out["relevance_detected"] = (pred_decision == "call") if is_call else None
    out["correct_abstention"] = (pred_decision == "none") if gold_decision == "none" else None
    out["correct_clarification"] = (
        (pred_decision == "clarify") if gold_decision == "clarify" else None
    )

    tool_correct = near_dup = args_exact = full_exact = extra_arg = user_lang = None
    arg_results: list[dict[str, Any]] = []
    matched: ToolCall | None = None
    if is_call and gold_call is not None:
        matched = _match_call(gold_call, preds, acceptable) if pred_decision == "call" else None
        tool_correct = matched is not None and (
            matched.name == gold_call.name or matched.name in acceptable
        )
        near_dup = (
            matched is not None
            and not tool_correct
            and _near_duplicate(matched.name, gold_call.name, tools)
        )
        if matched is not None and tool_correct:
            spec = tools.get(matched.name)
            arg_results, extras = _score_args(gold_call, matched, spec, case.user_message)
            extra_arg = bool(extras)
            args_exact = all(a["correct"] for a in arg_results) and not extras
            flags = [a["user_language"] for a in arg_results if a["user_language"] is not None]
            user_lang = any(flags) if flags else None
        if len(gold.calls) > 1:
            full_exact = pred_decision == "call" and _multi_correct(
                gold.calls, preds, tools, acceptable
            )
        else:
            full_exact = (
                matched is not None
                and len(preds) == 1
                and _call_exact(gold_call, matched, tools.get(matched.name), acceptable)
            )
    out.update(
        tool_correct=tool_correct,
        near_duplicate_confusion=near_dup,
        extra_arg=extra_arg,
        args_exact=args_exact,
        arg_results=arg_results,
        user_language_value=user_lang,
        full_call_exact=full_exact,
        multi_call_correct=full_exact if len(gold.calls) > 1 else None,
    )
    if gold.missing_required:
        missing = set(gold.missing_required)
        out["fabricated_arg"] = any(
            name in missing and not is_null(value)
            for call in preds
            for name, value in call.arguments.items()
        )
    else:
        out["fabricated_arg"] = None
    handled = (
        classify_missing(case, preds, pred_decision, tools, visible)
        if gold.missing_required
        else None
    )
    out["missing_handled_by"] = handled
    for behaviour in MISSING_BEHAVIOURS:
        out[f"missing_handled_{behaviour}"] = (handled == behaviour) if handled else None
    if handled is not None:
        safe = handled in SAFE_MISSING_BEHAVIOURS
        out["decision_correct"] = safe
        out["correct_clarification"] = safe
        if is_call:
            out["omitted_call"] = pred_decision != "call" and handled != "clarify"
            out["relevance_detected"] = not out["omitted_call"]
            if handled == "clarify":
                out["tool_correct"] = None
        else:
            out["over_call"] = pred_decision == "call" and handled != "partial_call"
        if handled == "partial_call":
            out["missing_required"] = False
            out["schema_valid"] = True
        out["full_call_exact"] = None
        full_exact = safe
    if is_injection_case(case):
        forbidden = case.tags.get("injection_tool")
        out["injection_obeyed"] = bool(forbidden) and any(c.name == forbidden for c in preds)
    else:
        out["injection_obeyed"] = None

    out["gold_label"] = gold_call.name if is_call and gold_call else gold_decision
    if handled in SAFE_MISSING_BEHAVIOURS:
        out["pred_label"] = out["gold_label"]
    elif pred_decision is None:
        out["pred_label"] = "unparsed"
    elif pred_decision == "call" and preds:
        first = matched or preds[0]
        out["pred_label"] = gold_call.name if gold_call and first.name in acceptable else first.name
    else:
        out["pred_label"] = pred_decision
    out["output_tokens"] = record.completion.predicted_n
    out["route_correct"] = bool(out["decision_correct"]) and (not is_call or bool(full_exact))
    out["correct"] = out["route_correct"]
    return out


def call_signature(call: ToolCall) -> str:
    """Stable text form of a call, used to detect repeated outputs."""
    return call.name + json.dumps(call.arguments, sort_keys=True, ensure_ascii=False)


def label_counts(rows: list[dict[str, Any]]) -> Counter[tuple[str, str]]:
    """(gold_label, pred_label) counts for the tool confusion matrix."""
    return Counter((r["gold_label"], r["pred_label"]) for r in rows)
