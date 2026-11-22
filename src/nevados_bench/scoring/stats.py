"""Statistics helpers used by every scorer and by the report.

Pure stdlib, deterministic: every resampling procedure takes an explicit seed.
"""

from __future__ import annotations

import math
import random
import zlib
from collections.abc import Callable, Sequence

LOW_N_THRESHOLD = 30
Z95 = 1.959963984540054
BOOTSTRAP_RESAMPLES = 1000


def is_low_n(n: int, threshold: int = LOW_N_THRESHOLD) -> bool:
    """Cells with fewer than `threshold` observations are flagged in every CSV."""
    return n < threshold


def stable_seed(*parts: object) -> int:
    """Seed derived from a cell key, so bootstrap results do not depend on iteration order."""
    return zlib.crc32("|".join(str(part) for part in parts).encode("utf-8"))


def wilson_interval(successes: int, n: int, z: float = Z95) -> tuple[float | None, float | None]:
    """Wilson score interval for a binomial proportion (95 % by default)."""
    if n <= 0:
        return (None, None)
    if not 0 <= successes <= n:
        raise ValueError(f"successes={successes} outside [0, {n}]")
    p = successes / n
    z2 = z * z
    denom = 1 + z2 / n
    centre = (p + z2 / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def percentile(values: Sequence[float], q: float) -> float | None:
    """Linear-interpolation percentile (same definition as numpy's default), q in [0, 100]."""
    if not values:
        return None
    if not 0 <= q <= 100:
        raise ValueError(f"q={q} outside [0, 100]")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q / 100
    lower = math.floor(pos)
    upper = math.ceil(pos)
    if lower == upper:
        return float(ordered[lower])
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (pos - lower)


def mean(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def stdev(values: Sequence[float]) -> float | None:
    """Sample standard deviation (ddof=1); None below two observations."""
    if len(values) < 2:
        return None
    mu = sum(values) / len(values)
    return math.sqrt(sum((v - mu) ** 2 for v in values) / (len(values) - 1))


def describe(values: Sequence[float]) -> dict[str, float | None]:
    """Mean, p50/p90/p95/p99, min, max, sample std, IQR and CV of a sample."""
    vals = [float(v) for v in values]
    mu = mean(vals)
    sd = stdev(vals)
    p25, p75 = percentile(vals, 25), percentile(vals, 75)
    return {
        "n": float(len(vals)),
        "mean": mu,
        "p50": percentile(vals, 50),
        "p90": percentile(vals, 90),
        "p95": percentile(vals, 95),
        "p99": percentile(vals, 99),
        "min": min(vals) if vals else None,
        "max": max(vals) if vals else None,
        "std": sd,
        "iqr": (p75 - p25) if p25 is not None and p75 is not None else None,
        "cv": (sd / mu) if sd is not None and mu else None,
    }


def bootstrap_ci(
    values: Sequence[float],
    statistic: Callable[[Sequence[float]], float | None],
    *,
    n_resamples: int = BOOTSTRAP_RESAMPLES,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float | None, float | None]:
    """Percentile bootstrap confidence interval of `statistic`, seeded."""
    if len(values) < 2:
        return (None, None)
    rng = random.Random(seed)
    data = list(values)
    estimates = []
    for _ in range(n_resamples):
        est = statistic(rng.choices(data, k=len(data)))
        if est is not None:
            estimates.append(est)
    if not estimates:
        return (None, None)
    return (percentile(estimates, 100 * alpha / 2), percentile(estimates, 100 * (1 - alpha / 2)))


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p-value from the discordant counts b and c."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2**n
    return min(1.0, 2 * tail)


def mcnemar_paired(a: Sequence[bool], b: Sequence[bool]) -> dict[str, float]:
    """Exact McNemar test on paired binary outcomes (same cases, two systems)."""
    if len(a) != len(b):
        raise ValueError("paired samples must have equal length")
    both = sum(1 for x, y in zip(a, b, strict=True) if x and y)
    a_only = sum(1 for x, y in zip(a, b, strict=True) if x and not y)
    b_only = sum(1 for x, y in zip(a, b, strict=True) if y and not x)
    return {
        "n": len(a),
        "both": both,
        "a_only": a_only,
        "b_only": b_only,
        "neither": len(a) - both - a_only - b_only,
        "p_value": mcnemar_exact(a_only, b_only),
    }


def paired_delta(
    a: Sequence[float], b: Sequence[float], *, seed: int = 0
) -> tuple[float | None, float | None, float | None]:
    """Mean of paired differences a-b with a seeded bootstrap CI."""
    if len(a) != len(b):
        raise ValueError("paired samples must have equal length")
    diffs = [x - y for x, y in zip(a, b, strict=True)]
    if not diffs:
        return (None, None, None)
    lo, hi = bootstrap_ci(diffs, mean, seed=seed)
    return (mean(diffs), lo, hi)


def ols(xs: Sequence[float], ys: Sequence[float]) -> dict[str, float] | None:
    """Least-squares fit y = intercept + slope * x; None without two distinct x values."""
    if len(xs) != len(ys):
        raise ValueError("xs and ys must have equal length")
    n = len(xs)
    if n < 2:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return None
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    slope = sxy / sxx
    intercept = my - slope * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - intercept - slope * x) ** 2 for x, y in zip(xs, ys, strict=True))
    r2 = 1 - ss_res / ss_tot if ss_tot else 1.0
    return {"slope": slope, "intercept": intercept, "r2": r2, "n": float(n)}
