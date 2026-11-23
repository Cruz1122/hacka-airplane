#!/usr/bin/env bash
# Side-load the knowledge runtime files into the app's files dir (debug builds only: needs run-as).
# Usage: scripts/push-knowledge.sh [--with-laya]   (set ANDROID_SERIAL to pick a device)
# Pushes the e5 GGUF, the index vectors and the ONNX scorer named in assets/data/knowledge/index.json; with --with-laya
# also the Laya ONNX and its tokenizer (only needed when policy.laya.enabled is turned on).
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
PKG="co.nevados.assistant"
MANIFEST="$HERE/assets/data/knowledge/index.json"
[[ -f "$MANIFEST" ]] || { echo "missing $MANIFEST: run experiments/laya/export_knowledge.py" >&2; exit 1; }

read -r GGUF BIN SCORER < <(python3 -c 'import json,sys; m=json.load(open(sys.argv[1])); print(m["embedder"].get("file","-"), m["vectors"]["file"], m["scorer"]["file"])' "$MANIFEST")
[[ "$GGUF" != "-" ]] || { echo "manifest was built with sentence-transformers; re-export with --embedder gguf" >&2; exit 1; }

FILES=("$ROOT/models/knowledge/$GGUF" "$ROOT/models/knowledge/$BIN" "$ROOT/models/knowledge/$SCORER")
if [[ "${1:-}" == "--with-laya" ]]; then
  LAYA="$ROOT/models/laya_final_rlcd6_raw/LOS_NEVADOS_LAYA_FINAL/run_rlcd6/model"
  FILES+=("$LAYA/onnx/laya_final.gather_int8.onnx" "$LAYA/tokenizer/tokenizer.json")
fi

adb get-state >/dev/null
adb shell run-as "$PKG" true || { echo "run-as $PKG failed: install a debug build first" >&2; exit 1; }
adb shell run-as "$PKG" mkdir -p files
for SRC in "${FILES[@]}"; do
  [[ -f "$SRC" ]] || { echo "not a file: $SRC" >&2; exit 1; }
  NAME="$(basename "$SRC")"
  [[ "$NAME" == tokenizer.json ]] && NAME="laya_tokenizer.json"
  TMP="/data/local/tmp/$NAME"
  adb push "$SRC" "$TMP"
  adb shell run-as "$PKG" cp "$TMP" "files/$NAME"
  adb shell rm -f "$TMP"
  adb shell run-as "$PKG" ls -l "files/$NAME"
done
