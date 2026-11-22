"""Long-format ("tidy") metric rows shared by all metric CSVs.

Every metrics CSV row is one model x slice x metric with the same columns, so the
report can treat all axes uniformly.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from nevados_bench.scoring.stats import (
    BOOTSTRAP_RESAMPLES,
    bootstrap_ci,
    describe,
    is_low_n,
    percentile,
    stable_seed,
    wilson_interval,
)

KEY_COLUMNS = ("model_id", "quant", "profile", "fc_mode")
COLUMNS = (
    *KEY_COLUMNS,
    "suite",
    "slice_dim",
    "slice_value",
    "metric",
    "n",
    "value",
    "ci_low",
    "ci_high",
    "low_n",
)
ALL = "all"
ANY = "*"

ModelKey = tuple[str, str, str, str]


def model_key(source: Mapping[str, Any] | Any) -> ModelKey:
    """(model_id, quant, profile, fc_mode) of a record or scored row; fc_mode '' when unset."""
    get = source.get if isinstance(source, Mapping) else lambda k: getattr(source, k, None)
    return (
        str(get("model_id") or ""),
        str(get("quant") or ""),
        str(get("profile") or ""),
        str(get("fc_mode") or ""),
    )


def metric_row(
    key: ModelKey,
    suite: str,
    slice_dim: str,
    slice_value: Any,
    metric: str,
    n: int,
    value: float | None,
    ci_low: float | None = None,
    ci_high: float | None = None,
) -> dict[str, Any]:
    return {
        **dict(zip(KEY_COLUMNS, key, strict=True)),
        "suite": suite,
        "slice_dim": slice_dim,
        "slice_value": "" if slice_value is None else str(slice_value),
        "metric": metric,
        "n": n,
        "value": value,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "low_n": is_low_n(n),
    }


def rate_row(
    key: ModelKey, suite: str, slice_dim: str, slice_value: Any, metric: str, flags: Iterable[Any]
) -> dict[str, Any] | None:
    """Proportion of True among applicable (non-None) flags, with a Wilson 95 % CI."""
    applicable = [bool(f) for f in flags if f is not None]
    if not applicable:
        return None
    k, n = sum(applicable), len(applicable)
    lo, hi = wilson_interval(k, n)
    return metric_row(key, suite, slice_dim, slice_value, metric, n, k / n, lo, hi)


def mean_row(
    key: ModelKey, suite: str, slice_dim: str, slice_value: Any, metric: str, values: Iterable[Any]
) -> dict[str, Any] | None:
    """Mean of applicable numeric values, with a seeded bootstrap CI of the mean."""
    vals = [float(v) for v in values if v is not None]
    if not vals:
        return None
    seed = stable_seed(*key, suite, slice_dim, slice_value, metric)
    lo, hi = bootstrap_ci(vals, lambda s: sum(s) / len(s), seed=seed)
    return metric_row(
        key, suite, slice_dim, slice_value, metric, len(vals), sum(vals) / len(vals), lo, hi
    )


DESCRIBE_STATS = ("mean", "p50", "p90", "p95", "p99", "max", "std", "iqr", "cv")
BOOTSTRAPPED_STATS = {"p50": 50, "p95": 95}


def describe_rows(
    key: ModelKey,
    suite: str,
    slice_dim: str,
    slice_value: Any,
    metric: str,
    values: Sequence[float],
    *,
    n_resamples: int = BOOTSTRAP_RESAMPLES,
) -> list[dict[str, Any]]:
    """One row per distribution statistic; p50 and p95 carry a seeded bootstrap CI."""
    vals = [float(v) for v in values if v is not None]
    if not vals:
        return []
    stats = describe(vals)
    rows = []
    for stat in DESCRIBE_STATS:
        lo = hi = None
        if stat in BOOTSTRAPPED_STATS:
            q = BOOTSTRAPPED_STATS[stat]
            seed = stable_seed(*key, suite, slice_dim, slice_value, metric, stat)
            lo, hi = bootstrap_ci(
                vals, lambda s, q=q: percentile(s, q), n_resamples=n_resamples, seed=seed
            )
        rows.append(
            metric_row(
                key,
                suite,
                slice_dim,
                slice_value,
                f"{metric}_{stat}",
                len(vals),
                stats[stat],
                lo,
                hi,
            )
        )
    return rows


def compact(rows: Iterable[dict[str, Any] | None]) -> list[dict[str, Any]]:
    return [row for row in rows if row is not None]
