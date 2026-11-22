"""B1 speed protocol: cold/warm prefill per context level, decode by output length, sustained.

The thread sweep is driven by the caller (one server restart per thread count); the
`threads` argument is only recorded.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from nevados_bench.runner.client import LlamaClient
from nevados_bench.runner.measure import run_request
from nevados_bench.runner.probe import CgroupProbe, HostProbe
from nevados_bench.schemas import CONTEXT_LEVEL_TOKENS, PromptRequest, RequestRecord

TextSource = Callable[[int], str]  # variant index -> long filler text
Sink = Callable[[RequestRecord], None]

DEFAULT_LEVELS = ("0.5k", "1k", "2k", "4k", "8k")
DEFAULT_OUTPUT_LENGTHS = (16, 64, 256)
SYSTEM = "Eres un asistente. Lee el texto y responde."
QUESTION = "\n\nResume el texto anterior en una frase."
DECODE_PROMPT = (
    "Escribe una historia muy larga sobre una caminata por un páramo de alta montaña. "
    "No te detengas: sigue escribiendo sin concluir."
)


class ColdCacheError(RuntimeError):
    """A request meant to be cold reused KV cache: the cold measurement is invalid."""


def _messages(filler: str) -> list[dict[str, Any]]:
    return [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": filler + QUESTION},
    ]


def fit_prompt(
    client: LlamaClient, text: str, target_tokens: int
) -> tuple[list[dict[str, Any]], int]:
    """Largest word prefix of `text` whose templated prompt is <= target tokens.

    Tokens are counted with the server's own template + tokenizer, so they equal what
    prefill processes (up to BOS handling).
    """
    words = text.split()
    while len(words) < target_tokens * 2:  # ensure enough material; words >= ~1 token
        words = words + words
    lo, hi = 0, len(words)
    best = (_messages(""), client.count_prompt_tokens(_messages("")))
    while lo <= hi:
        mid = (lo + hi) // 2
        msgs = _messages(" ".join(words[:mid]))
        n = client.count_prompt_tokens(msgs)
        if n <= target_tokens:
            best = (msgs, n)
            lo = mid + 1
        else:
            hi = mid - 1
    return best


def run_speed_protocol(
    client: LlamaClient,
    probe: CgroupProbe | None,
    host_probe: HostProbe | None,
    text_source: TextSource,
    record_template: dict[str, Any],
    *,
    threads: int,
    sink: Sink | None = None,
    levels: Iterable[str] = DEFAULT_LEVELS,
    output_lengths: Iterable[int] = DEFAULT_OUTPUT_LENGTHS,
    reps: int = 5,
    sustained_n: int = 30,
    prefill_max_tokens: int = 32,
    sustained_level: str = "1k",
    seed: int = 1234,
) -> list[RequestRecord]:
    """Run the protocol; every kept record goes to `sink` as soon as it exists.

    Each cell runs one warm-up that is discarded (not recorded) and then `reps` kept
    repetitions. Cold = slot erased + cache_prompt=false (server runs with --cache-ram 0);
    warm = identical request right after, cache_prompt=true. `ignore_eos` forces exact
    output lengths so decode numbers are comparable across models.
    """
    out: list[RequestRecord] = []
    base = {**record_template, "suite": "speed", "threads": threads}

    def measure(req: PromptRequest, keep: bool, **fields: Any) -> RequestRecord:
        record = run_request(client, probe, host_probe, req, {**base, **fields})
        if keep:
            out.append(record)
            if sink is not None:
                sink(record)
        return record

    def req(msgs: list[dict[str, Any]], max_tokens: int, cache: bool) -> PromptRequest:
        return PromptRequest(
            messages=msgs,
            max_tokens=max_tokens,
            temperature=0.0,
            seed=seed,
            cache_prompt=cache,
            extra_body={"ignore_eos": True},
        )

    prompts: dict[str, tuple[list[dict[str, Any]], int]] = {}
    for variant, level in enumerate(levels):
        target = CONTEXT_LEVEL_TOKENS[level]
        msgs, n = fit_prompt(client, text_source(variant), target)
        prompts[level] = (msgs, n)
        tags = {"target_tokens": target, "measured_prompt_tokens": n}
        for rep in range(-1, reps):  # rep -1 is the discarded warm-up
            keep = rep >= 0
            client.erase_slot()
            cold = measure(
                req(msgs, prefill_max_tokens, cache=False),
                keep,
                case_id=f"speed:prefill:{level}",
                rep=max(rep, 0),
                arm="cold",
                context_level=level,
                tags=tags,
            )
            c = cold.completion
            if c.cache_n:
                raise ColdCacheError(f"{level} rep {rep}: cold request had cache_n={c.cache_n}")
            measure(
                req(msgs, prefill_max_tokens, cache=True),
                keep,
                case_id=f"speed:prefill:{level}",
                rep=max(rep, 0),
                arm="warm",
                context_level=level,
                tags=tags,
            )

    decode_msgs = [{"role": "user", "content": DECODE_PROMPT}]
    for length in output_lengths:
        for rep in range(-1, reps):
            measure(
                req(decode_msgs, length, cache=True),
                rep >= 0,
                case_id=f"speed:decode:{length}",
                rep=max(rep, 0),
                arm="decode",
                tags={"output_len": length},
            )

    if sustained_n > 0:
        if sustained_level in prompts:
            msgs, n = prompts[sustained_level]
        else:
            target = CONTEXT_LEVEL_TOKENS[sustained_level]
            msgs, n = fit_prompt(client, text_source(len(prompts)), target)
        tags = {"target_tokens": CONTEXT_LEVEL_TOKENS[sustained_level], "measured_prompt_tokens": n}
        for i in range(sustained_n):
            measure(
                req(msgs, 64, cache=True),
                True,
                case_id="speed:sustained",
                rep=i,
                arm="sustained",
                context_level=sustained_level,
                tags=tags,
            )
    return out
