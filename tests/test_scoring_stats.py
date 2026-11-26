from __future__ import annotations

import pytest

from nevados_bench.scoring.stats import (
    bootstrap_ci,
    describe,
    is_low_n,
    mcnemar_exact,
    mcnemar_paired,
    mean,
    ols,
    paired_delta,
    percentile,
    wilson_interval,
)


def test_wilson_known_values():
    lo, hi = wilson_interval(8, 10)
    assert lo == pytest.approx(0.4902, abs=1e-4) and hi == pytest.approx(0.9433, abs=1e-4)
    lo, hi = wilson_interval(0, 10)
    assert lo == 0.0 and hi == pytest.approx(0.2775, abs=1e-4)
    assert wilson_interval(0, 0) == (None, None)
    with pytest.raises(ValueError):
        wilson_interval(11, 10)


def test_percentile_matches_linear_interpolation():
    assert percentile([1, 2, 3, 4], 50) == 2.5
    assert percentile([1, 2, 3, 4], 90) == pytest.approx(3.7)
    assert percentile([5], 99) == 5
    assert percentile([], 50) is None


def test_describe():
    d = describe([1, 2, 3, 4])
    assert d["mean"] == 2.5 and d["p50"] == 2.5 and d["max"] == 4
    assert d["std"] == pytest.approx(1.290994, abs=1e-6)
    assert d["iqr"] == pytest.approx(1.5) and d["cv"] == pytest.approx(0.516398, abs=1e-6)


def test_bootstrap_is_seeded_and_brackets_estimate():
    values = list(range(100))
    a = bootstrap_ci(values, mean, seed=7)
    assert a == bootstrap_ci(values, mean, seed=7)
    assert a[0] < 49.5 < a[1]
    assert bootstrap_ci([1.0], mean) == (None, None)


def test_mcnemar_exact():
    assert mcnemar_exact(1, 9) == pytest.approx(0.021484375)
    assert mcnemar_exact(0, 0) == 1.0
    assert mcnemar_exact(5, 5) == 1.0
    res = mcnemar_paired([True, True, False, True], [True, False, False, False])
    assert (res["both"], res["a_only"], res["b_only"], res["neither"]) == (1, 2, 0, 1)
    assert res["p_value"] == pytest.approx(0.5)


def test_ols_and_paired_delta():
    fit = ols([0, 1, 2, 3], [1, 3, 5, 7])
    assert fit["slope"] == pytest.approx(2) and fit["intercept"] == pytest.approx(1)
    assert fit["r2"] == pytest.approx(1)
    assert ols([1, 1], [2, 3]) is None
    delta, lo, hi = paired_delta([1, 1, 1, 0], [0, 0, 1, 0], seed=1)
    assert delta == 0.5 and lo <= delta <= hi


def test_low_n_flag():
    assert is_low_n(29) and not is_low_n(30)
