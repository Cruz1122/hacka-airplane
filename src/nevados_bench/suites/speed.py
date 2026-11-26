"""Filler text source for the B1 speed protocol (``runner.speed.run_speed_protocol``).

The runner calls the source with a *variant index* (one per context level) and trims the
text to the exact token target itself, so each variant only needs to be long enough for
the largest level and different from the others (distinct variants defeat prefix reuse).
"""

from __future__ import annotations

from collections.abc import Callable

from nevados_bench.world import World
from nevados_bench.world.corpus import stable_hash

# 8k tokens at ~3.6 chars/token is ~29k chars; leave headroom for tokenizer variance.
DEFAULT_MIN_CHARS = 40_000


def text_source(world: World, *, min_chars: int = DEFAULT_MIN_CHARS) -> Callable[[int], str]:
    """Deterministic Spanish filler of at least ``min_chars`` characters per variant.

    Built only from the digit-free filler passages, so no trap value from the corpus can
    leak into speed prompts. Each variant uses its own passage order.
    """
    if min_chars <= 0:
        raise ValueError(f"min_chars must be positive, got {min_chars}")
    texts = {pid: p.text for pid, p in world.filler.items()}
    if not texts:
        raise ValueError("world has no filler passages")

    def source(variant: int) -> str:
        order = sorted(texts, key=lambda pid: stable_hash(f"speed|{variant}|{pid}"))
        parts: list[str] = []
        size = 0
        while size < min_chars:
            for pid in order:
                parts.append(texts[pid])
                size += len(texts[pid]) + 1
                if size >= min_chars:
                    break
            # Rotate on repeats so a long text never repeats the same passage sequence.
            order = order[1:] + order[:1]
        return " ".join(parts)

    return source
