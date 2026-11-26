#!/usr/bin/env bash
# Make a fresh git worktree runnable without reinstalling: link the main checkout's
# ignored heavy inputs (mobile/node_modules ~12 GB, models/knowledge, generated legacy fixtures).
# Idempotent. Never overwrites a real file or directory. Prints what it did.
set -euo pipefail

target="$(git rev-parse --show-toplevel)"
main="$(git worktree list --porcelain | awk 'NR==1{print $2}')"

if [[ "$target" == "$main" ]]; then
  echo "already in the main checkout ($main); nothing to link"
  exit 0
fi

link() {
  local rel="$1"
  local src="$main/$rel" dst="$target/$rel"
  if [[ ! -e "$src" ]]; then
    echo "skip   $rel (missing in main checkout)"
  elif [[ -L "$dst" ]]; then
    echo "ok     $rel (already linked)"
  elif [[ -e "$dst" ]]; then
    echo "keep   $rel (real path exists here; not touched)"
  else
    mkdir -p "$(dirname "$dst")"
    ln -s "$src" "$dst"
    echo "linked $rel -> $src"
  fi
}

# A symlink does not match the directory-only `node_modules/` ignore rule, so exclude it
# explicitly; otherwise `git add -A` in the worktree would commit the link.
exclude="$(git rev-parse --git-common-dir)/info/exclude"
grep -qxF '/mobile/node_modules' "$exclude" 2>/dev/null || echo '/mobile/node_modules' >>"$exclude"
link mobile/node_modules
link models/knowledge
for f in "$main"/mobile/src/core/__fixtures__/*.json; do
  [[ -e "$f" ]] && link "mobile/src/core/__fixtures__/$(basename "$f")"
done
