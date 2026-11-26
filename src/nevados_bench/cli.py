"""Command line entry point: fetch models, build suites, run batches, score and report."""

from __future__ import annotations

import argparse
import sys
import time
from collections.abc import Sequence

import httpx

from nevados_bench.config import (
    MODELS_DIR,
    ModelConfig,
    load_models,
    load_models_lock,
    load_profiles,
)

FETCH_ATTEMPTS = 4


def select_models(spec: str, *, downloaded_only: bool = True) -> list[ModelConfig]:
    """`all`, `deployable`, or a comma-separated list of ids (registry order is kept)."""
    registry = load_models()
    if spec == "all":
        chosen = registry
    elif spec == "deployable":
        chosen = [m for m in registry if m.deployable]
    else:
        wanted = [part.strip() for part in spec.split(",") if part.strip()]
        known = {m.id for m in registry}
        unknown = [w for w in wanted if w not in known]
        if unknown:
            raise SystemExit(f"unknown model ids: {', '.join(unknown)}")
        chosen = [m for m in registry if m.id in wanted]
    if downloaded_only:
        lock = load_models_lock()
        missing = [m.id for m in chosen if m.id not in lock]
        if missing:
            print(f"skipping models not fetched yet: {', '.join(missing)}", file=sys.stderr)
        chosen = [m for m in chosen if m.id in lock]
    return chosen


def cmd_fetch(args: argparse.Namespace) -> int:
    from nevados_bench.runner.fetch import FetchError, lock_image, resolve_and_download

    image = lock_image(load_profiles().server.image)
    print(f"image {image.ref} ({image.version})")
    failures = 0
    for model in select_models(args.models, downloaded_only=False):
        # Downloads resume from the .part file, so transient network errors are retried.
        for attempt in range(1, FETCH_ATTEMPTS + 1):
            try:
                lock = resolve_and_download(model, MODELS_DIR)
            except (FetchError, httpx.HTTPError) as exc:
                print(f"attempt {attempt} failed for {model.id}: {exc!r}", file=sys.stderr)
                if isinstance(exc, FetchError) or attempt == FETCH_ATTEMPTS:
                    failures += 1
                    print(f"FAILED {model.id}", file=sys.stderr)
                    break
                time.sleep(5 * attempt)
            else:
                print(f"ok {model.id}: {lock.filename} {lock.size_bytes / 1e6:.0f} MB", flush=True)
                break
    return 1 if failures else 0


def cmd_build_suites(_: argparse.Namespace) -> int:
    from nevados_bench.batches import build_suites

    for name, count in build_suites().items():
        print(f"{name}: {count}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    from nevados_bench import batches
    from nevados_bench.batches import BATCHES

    models = select_models(args.models)
    if not models:
        raise SystemExit("no models selected")
    if args.modes:
        # Batches read this module global at call time; restricting it halves the cost of
        # the route suites when only one contract is being screened.
        batches.ROUTE_MODES = tuple(args.modes.split(","))
    batches.TARGET = args.target
    batches.HOST_PORT = args.port
    batches.SCHEMA_ENDPOINT = args.schema_endpoint
    batches.CACHE_RAM_MIB = args.cache_ram_mib
    batches.EXTRACT_LAYOUT = args.extract_layout
    batches.ROUTE_SCOPE = args.route_scope
    BATCHES[args.batch](args.run_id, models, args.budget_min)
    return 0


def cmd_score(args: argparse.Namespace) -> int:
    from nevados_bench.batches import RESULTS_DIR, SUITES_DIR
    from nevados_bench.report.aggregate import aggregate_run
    from nevados_bench.report.markdown import write_report
    from nevados_bench.world import load_world

    run_dir = RESULTS_DIR / args.run_id
    aggregate_run(run_dir, SUITES_DIR, load_world())
    print(write_report(run_dir))
    return 0


def cmd_guard_eval(args: argparse.Namespace) -> int:
    from nevados_bench.batches import RESULTS_DIR, SUITES_DIR
    from nevados_bench.report.guard_eval import run_guard_eval
    from nevados_bench.world import load_world

    answers, routes = run_guard_eval(RESULTS_DIR / args.run_id, SUITES_DIR, load_world())
    for row in answers:
        print(
            f"{row['model_id']}: n={row['n']} rejected={row['rejected']} "
            f"(was correct {row['rejected_was_correct']}) "
            f"correct {row['grounded_correct_before_rate']}"
            f" -> {row['grounded_correct_after_rate']} "
            f"hallucinated {row['hallucinated_before']} -> {row['hallucinated_after']} "
            f"safety_fab {row['safety_fabrication_before']} -> {row['safety_fabrication_after']} "
            f"reasons {row['reasons']}"
        )
    for row in routes:
        print(
            f"route {row['model_id']}/{row['fc_mode']} {row['set']}: n={row['n']} "
            f"correct {row['correct_before']} -> {row['correct_after']} "
            f"fabricated_arg {row['fabricated_arg_before']} -> {row['fabricated_arg_after']} "
            f"changed {row['changed']} (broke {row['changed_was_correct']}) "
            f"injection obeyed {row['injection_obeyed']} "
            f"-> executes {row['injection_executes_after']}"
        )
    return 0


def cmd_app(args: argparse.Namespace) -> int:
    from nevados_bench.app.server import serve

    serve(
        backend_url=args.backend_url,
        device_station=args.device_station,
        host=args.host,
        port=args.port,
        extract_layout=args.extract_layout,
        route_scope=args.route_scope,
    )
    return 0


def add_speedup_flags(parser: argparse.ArgumentParser) -> None:
    """Opt-in FSM speedups; the defaults reproduce the r2 prompts and behaviour."""
    parser.add_argument(
        "--extract-layout",
        choices=["default", "shared_prefix"],
        default="default",
        help="shared_prefix: all extract prompts share one long cacheable system prefix",
    )
    parser.add_argument(
        "--route-scope",
        choices=["router", "state"],
        default="router",
        help="state: mid-flow routing sees only the flow tools (shorter prompt, no "
        "information questions answered mid-flow)",
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nevados-bench", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="download and pin GGUF files and the server image")
    fetch.add_argument("--models", default="all")
    fetch.set_defaults(func=cmd_fetch)

    build = sub.add_parser("build-suites", help="write data/suites/*.jsonl")
    build.set_defaults(func=cmd_build_suites)

    run = sub.add_parser("run", help="run one batch (resumable)")
    run.add_argument("batch", choices=["B0", "B1", "B1F", "B2", "B3", "B4", "B5", "B6", "B7", "B8"])
    run.add_argument(
        "--target",
        choices=["docker", "phone"],
        default="docker",
        help="phone: llama-server on the adb device (binary and GGUF pushed beforehand)",
    )
    run.add_argument("--run-id", required=True)
    run.add_argument("--models", default="all")
    run.add_argument(
        "--port", type=int, default=None, help="host port (default from profiles.yaml)"
    )
    run.add_argument("--budget-min", type=float, default=None, help="time budget per model")
    run.add_argument(
        "--schema-endpoint",
        choices=["chat", "completion"],
        default="chat",
        help="completion: schema-constrained calls skip the chat handler (no ```json fence)",
    )
    run.add_argument(
        "--cache-ram-mib",
        type=int,
        default=None,
        help="host-RAM prompt cache for the server (default: profiles.yaml, 0)",
    )
    run.add_argument("--modes", default=None, help="route modes to run, e.g. uniform")
    add_speedup_flags(run)
    run.set_defaults(func=cmd_run)

    score = sub.add_parser("score", help="aggregate metrics and write REPORT.md")
    score.add_argument("--run-id", required=True)
    score.set_defaults(func=cmd_score)

    guard = sub.add_parser("guard-eval", help="re-score recorded answers through the guards")
    guard.add_argument("--run-id", required=True)
    guard.set_defaults(func=cmd_guard_eval)

    app = sub.add_parser("app", help="local web chat prototype over the guarded FSM")
    app.add_argument("--backend-url", default="http://127.0.0.1:8080")
    app.add_argument("--device-station", default=None, help="station id the device is at")
    app.add_argument("--host", default="127.0.0.1")
    app.add_argument("--port", type=int, default=8765)
    add_speedup_flags(app)
    app.set_defaults(func=cmd_app)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
