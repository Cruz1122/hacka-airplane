---
name: hackathon-lean
description: Hackathon delivery discipline for this repo. Use for any implementation task in mobile/ or src/ under time pressure - smallest correct change, no speculative abstractions, no token waste, terse reports.
---

# Hackathon lean

Deadline: 2026-11-26. Working beats elegant. Every line must earn its place.

## Build rules

1. Smallest change that fully solves the task. No "future-proof" layers, plugin systems, DI containers, generic repositories, or config for things with one value.
2. One way to do each thing. No second state library, test runner, styling system, or HTTP client.
3. Dependencies: only the whitelist in `mobile-offline-stack`. Need another one? Stop and report it; do not install.
4. Port, do not redesign. When porting Python to TypeScript keep names, order and behavior; parity fixtures are the spec.
5. Tests prove behavior that matters (parity fixtures, guards, flows). No snapshot tests of UI, no tests of trivial getters.
6. No placeholder code that pretends to work. If something is not done, leave a precise `TODO(<what>, <why>)` and report it.
7. Errors: surface them with context; never swallow. No retries/backoff unless a measured failure needs it.
8. Comments say why, never what.

## Token rules

1. Read only the files your task names, plus what a failing check points to. Use `grep -n`/`sed -n` ranges, not whole large files.
2. Do not re-read files you just wrote. Do not print big files or long logs; `tail` them.
3. Run the narrowest check first (one test file, `tsc --noEmit` on the package), the full suite once at the end.
4. Long commands (gradle, prebuild, npm install): run once, `tail -40` the log; do not poll in loops.
5. Final report: caveman-terse. What changed (paths), checks run with exact results, what is NOT done or NOT verified. No prose recap.

## Stop conditions

- Same failure after 3 fix attempts: stop, report the failing command, the error and the assumption you doubt.
- A task needs a file another agent owns: do not edit it; report the needed change.
