#!/usr/bin/env bash
# Builds the production APK with the knowledge models inside, then checks the artifact.
# Usage: scripts/release-android.sh            (from anywhere; needs the TUMAK_UPLOAD_* signing
#        properties in ~/.gradle/gradle.properties, see plugins/withReleaseAndroid.js)
# Output: android/app/build/outputs/apk/release/app-release.apk
set -euo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
MANIFEST="$HERE/assets/data/knowledge/index.json"
STAGE="$HERE/.release-models/models"
# The user SDK: /opt/android-sdk is root-owned and incomplete on this machine.
SDK="${TUMAK_ANDROID_SDK:-$HOME/Android/Sdk}"
BT="$(ls -d "$SDK"/build-tools/* | sort -V | tail -1)"
APK="$HERE/android/app/build/outputs/apk/release/app-release.apk"

grep -q '^TUMAK_UPLOAD_STORE_FILE=' "$HOME/.gradle/gradle.properties" 2>/dev/null \
  || { echo "missing TUMAK_UPLOAD_* in ~/.gradle/gradle.properties: no release key" >&2; exit 1; }

# 1. Stage exactly the files the manifest names, checked against its bytes and sha256.
rm -rf "$HERE/.release-models" && mkdir -p "$STAGE"
python3 - "$MANIFEST" "$ROOT/models/knowledge" "$STAGE" <<'PY'
import hashlib, json, os, sys
manifest, src, out = sys.argv[1:]
m = json.load(open(manifest))
lines = []
for key in ("embedder", "vectors", "scorer"):
    e = m.get(key)
    if not e:
        continue
    path = os.path.join(src, e["file"])
    size = os.path.getsize(path)
    if size != e["bytes"]:
        sys.exit(f"{e['file']}: {size} bytes, manifest says {e['bytes']}")
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    if e.get("sha256") and h.hexdigest() != e["sha256"]:
        sys.exit(f"{e['file']}: sha256 differs from the manifest")
    os.link(path, os.path.join(out, e["file"]))
    lines.append(f"{h.hexdigest()}  {e['file']}")
open(os.path.join(out, "models.sha256"), "w").write("\n".join(lines) + "\n")
print("staged:", ", ".join(l.split()[1] for l in lines))
PY

# 2. Regenerate android/ from app.json (icons, name, splash, plugins). SDK 58 prebuild recreates it.
cd "$HERE"
npx expo prebuild -p android --no-install
# Prebuild recreates android/, which drops local.properties.
echo "sdk.dir=$SDK" > "$HERE/android/local.properties"

# 3. Build.
cd "$HERE/android"
export ANDROID_HOME="$SDK"
./gradlew assembleRelease -PreactNativeArchitectures=arm64-v8a

# 4. Check the artifact: label, version, models stored uncompressed, not the debug key.
"$BT/aapt2" dump badging "$APK" | grep -E "^package:|application-label:"
unzip -v "$APK" | grep "assets/models/" | awk '{print $2, $1, $8}'
if unzip -v "$APK" | grep "assets/models/" | grep -qv Stored; then
  echo "model assets are compressed" >&2; exit 1
fi
CERT="$("$BT/apksigner" verify --print-certs "$APK")"
echo "$CERT" | grep "certificate DN"
if echo "$CERT" | grep -q "CN=Android Debug"; then echo "signed with the debug key" >&2; exit 1; fi
ls -lh "$APK"
