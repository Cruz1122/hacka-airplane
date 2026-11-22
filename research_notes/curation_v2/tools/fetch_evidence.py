"""Download an evidence source and record provenance so quotes can be checked against real bytes.

    python3 research_notes/curation_v2/tools/fetch_evidence.py --section rules --name res-207-2023 URL

Writes research_notes/curation_v2/evidence/<section>/raw/<name>.<ext> (raw bytes, gitignored),
evidence/<section>/<name>.txt (text extracted from those bytes, tracked) and <name>.meta.json (URL,
HTTP status, sha256 of raw and text). The proposal's evidence `path` must point to the .txt file. verify_evidence.py re-derives the text
from the raw bytes, so editing the .txt by hand fails verification.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "research_notes/curation_v2/evidence"
UA = "Mozilla/5.0 (X11; Linux x86_64) evidence-fetch/1.0"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{2,80}$")


def html_to_text(raw: bytes) -> str:
    from html.parser import HTMLParser

    class P(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.out, self.skip = [], 0

        def handle_starttag(self, tag, attrs):
            if tag in ("script", "style", "noscript", "svg"):
                self.skip += 1
            elif tag in ("p", "br", "div", "li", "tr", "h1", "h2", "h3", "h4", "h5", "td", "section"):
                self.out.append("\n")

        def handle_endtag(self, tag):
            if tag in ("script", "style", "noscript", "svg") and self.skip:
                self.skip -= 1

        def handle_data(self, data):
            if not self.skip:
                self.out.append(data)

    p = P()
    p.feed(raw.decode("utf-8", errors="replace"))
    lines = [" ".join(line.split()) for line in "".join(p.out).splitlines()]
    return "\n".join(line for line in lines if line) + "\n"


def extract_text(raw: bytes, content_type: str) -> str:
    if raw[:5] == b"%PDF-" or "pdf" in content_type:
        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(raw)
            f.flush()
            out = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True,
                                 check=True)
        return out.stdout.decode("utf-8", errors="replace")
    if "html" in content_type or raw.lstrip()[:1] == b"<":
        return html_to_text(raw)
    return raw.decode("utf-8", errors="replace")


def fetch(url: str) -> tuple[bytes, dict]:
    with tempfile.TemporaryDirectory() as d:
        body, head = Path(d) / "body", Path(d) / "head"
        cmd = ["curl", "-sSL", "--max-time", "60", "-A", UA, "-D", str(head), "-o", str(body),
               "-w", "%{http_code} %{url_effective} %{content_type}", url]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            sys.exit(f"curl failed ({res.returncode}): {res.stderr.strip()}")
        code, final, *ctype = res.stdout.split(" ")
        return body.read_bytes(), {"status": int(code), "final_url": final,
                                   "content_type": " ".join(ctype).lower()}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--section", required=True)
    ap.add_argument("--name", required=True, help="lowercase slug, e.g. res-207-2023")
    a = ap.parse_args()
    if not NAME_RE.match(a.name) or not re.match(r"^[a-z_]+$", a.section):
        sys.exit("invalid --name or --section")
    raw, info = fetch(a.url)
    if info["status"] >= 400:
        sys.exit(f"HTTP {info['status']} for {a.url}; nothing saved")
    ext = "pdf" if raw[:5] == b"%PDF-" else ("html" if "html" in info["content_type"] else "bin")
    out = EVIDENCE / a.section
    (out / "raw").mkdir(parents=True, exist_ok=True)
    if (out / f"{a.name}.txt").exists():
        sys.exit(f"{a.name} already exists in {a.section}; choose another --name")
    text = extract_text(raw, info["content_type"])
    (out / "raw" / f"{a.name}.{ext}").write_bytes(raw)
    (out / f"{a.name}.txt").write_text(text, encoding="utf-8")
    meta = {
        "url": a.url,
        **info,
        "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "raw_file": f"raw/{a.name}.{ext}",
        "sha256_raw": sha(raw),
        "sha256_txt": sha(text.encode("utf-8")),
        "bytes": len(raw),
        "tool": "fetch_evidence.py/1",
    }
    (out / f"{a.name}.meta.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    print(json.dumps({"txt": str((out / f"{a.name}.txt").relative_to(ROOT)), **meta},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
