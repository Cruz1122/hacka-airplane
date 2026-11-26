---
name: shared-checkout
description: Use at the start of any task in this repo, and before delegating to a worktree. Several agent chats edit the main checkout at once, and fresh worktrees lack mobile/node_modules, models/, and ignored fixtures. Gives the link script that makes a worktree testable in seconds and the rules that keep agents from overwriting each other.
---

# Shared checkout and worktrees

## Fresh worktree: link, do not install

A new git worktree has no `mobile/node_modules` (12 GB), no `models/knowledge/` (vectors and GGUF files), and no `mobile/src/core/__fixtures__/*.json`. Without them, Jest cannot start and knowledge tests fail. Do not run `npm install` there. Run:

```bash
bash "$(git worktree list --porcelain | awk 'NR==1{print $2}')/.agents/skills/shared-checkout/scripts/link-worktree-deps.sh"
```

Run it from anywhere inside the worktree. It symlinks those paths from the main checkout and adds `/mobile/node_modules` to the shared `info/exclude`, so `git status` stays clean. It is idempotent and never replaces a real file. Measured 2026-11-26 on a T3 worktree: after linking, 249 of 249 tests in `engine` and `driver` passed and `npx tsc --noEmit` passed. Metro and Gradle through the link are untested.

The link shares packages with the main checkout. Do not run `npm install` or `npx expo install` through the link. That changes the main checkout's dependencies for every other agent.

## Main checkout: other chats are writing

The main checkout (the first line of `git worktree list`, branch `dev`) usually has uncommitted work from other chats. Those chats may be editing the same `mobile/` files while you work.

1. Run `git status --short` before your first edit. Treat every modified path you did not change as someone else's work.
2. Do not revert, reformat, stash, or `git checkout` those paths.
3. Before you edit a file that already shows as modified, read `git diff <file>`. Keep the other edits.
4. Stage only your own paths with `git add <path>`. Never use `git add -A` or `git add .`.
5. When parallel writers need the same file, give each one its own worktree, or give one writer the file.

## Ports and long jobs

- Metro on 8081 may belong to another chat. Use your own port (see the `mobile-verify-fast` skill).
- GPU training powers off this laptop. Train in Colab. The flow is in `docs/agent-index/areas/25-nlu-experiments.md`.

## Delegating

Size each child's read set to its context window. Point it at `docs/agent-index/README.md` and the `repo-search-budget` skill, and give it file paths, not pasted content.
