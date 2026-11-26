"""Run: uv run --with pytest --with pillow --with numpy python -m pytest experiments/trail_map -q"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_trail_map as bt


def test_bounds_cover_the_route():
    b = bt.map_bounds()
    # Brisas (north) and Valle de las Tumbas (south) from the route sketch.
    for lat, lon in (
        (4.934637957115937, -75.35013575948123),
        (4.908941693623378, -75.35354216596245),
    ):
        assert b.south < lat < b.north
        assert b.west < lon < b.east


def test_trace_is_y_down_and_shifted():
    mask = np.zeros((60, 60), bool)
    mask[36:56, 4:24] = (
        True  # a block near the bottom-left corner, larger than potrace's speck size
    )
    assert bt.TURD < 20 * 20
    d = bt.trace(mask, -4, -4)
    x, y = map(int, re.match(r"M(-?\d+) (-?\d+)", d).groups())
    assert 0 <= x <= 20 and 32 <= y <= 52


def test_trace_of_empty_mask_is_empty():
    assert bt.trace(np.zeros((8, 8), bool), 0, 0) == ""
