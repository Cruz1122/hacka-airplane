import re

import pytest

from nevados_bench.suites.speed import text_source
from nevados_bench.world import load_world


@pytest.fixture(scope="module")
def world():
    return load_world()


def test_text_is_long_enough_and_deterministic(world):
    source = text_source(world, min_chars=5000)
    text = source(0)
    assert len(text) >= 5000
    assert text == text_source(world, min_chars=5000)(0)


def test_default_length_covers_largest_level(world):
    # 8k tokens at 3.6 chars per token.
    assert len(text_source(world)(4)) >= 8000 * 3.6


def test_variants_differ(world):
    source = text_source(world, min_chars=3000)
    assert len({source(i)[:500] for i in range(5)}) == 5


def test_text_is_digit_free_spanish(world):
    text = text_source(world, min_chars=3000)(1)
    assert not re.search(r"\d", text)
    assert " el " in text or " la " in text


def test_rejects_non_positive_length(world):
    with pytest.raises(ValueError):
        text_source(world, min_chars=0)
