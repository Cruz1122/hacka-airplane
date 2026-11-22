#!/usr/bin/env bash
# Side-load a GGUF into the app's files dir without root (debug builds only: needs run-as).
# Usage: scripts/push-model.sh <path-to-gguf>   (set ANDROID_SERIAL to pick a device)
set -euo pipefail

PKG="co.nevados.assistant"
SRC="${1:?usage: push-model.sh <path-to-gguf>}"
[[ -f "$SRC" ]] || { echo "not a file: $SRC" >&2; exit 1; }
NAME="$(basename "$SRC")"
TMP="/data/local/tmp/$NAME"

adb get-state >/dev/null
adb shell run-as "$PKG" true || { echo "run-as $PKG failed: install a debug build first" >&2; exit 1; }

adb shell run-as "$PKG" mkdir -p files
adb push "$SRC" "$TMP"
adb shell run-as "$PKG" cp "$TMP" "files/$NAME"
adb shell rm -f "$TMP"
adb shell run-as "$PKG" ls -l "files/$NAME"
echo "/data/data/$PKG/files/$NAME"
