"""Write a decoded .txt next to each raw download so quotes can be matched byte-for-byte.

Usage: python3 -I extract_text.py <raw file> [<raw file> ...]
HTML: tags stripped, entities decoded, block tags turned into newlines.
JSON list of SGC records: title, dates and description (tags stripped) per record.
Other text files: copied unchanged. PDFs are handled with pdftotext outside this script.
Scripts live here, downloads live in evidence/raw/; never run this from inside raw/.
"""

import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

BLOCK = {"p", "br", "li", "tr", "div", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "td", "th"}


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        elif tag in BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self.skip = max(0, self.skip - 1)
        elif tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def strip_html(fragment: str) -> str:
    parser = _Text()
    parser.feed(fragment)
    text = "".join(parser.parts).replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def decode_bytes(raw: bytes) -> str:
    for enc in ("utf-8", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1")


def convert(path: Path) -> Path:
    out = path.with_suffix(".txt") if path.suffix != ".txt" else path
    if path.suffix == ".json":
        out = path.with_suffix(".json.txt")
        records = json.loads(decode_bytes(path.read_bytes()))
        lines = []
        if isinstance(records, list):
            for rec in records:
                if not isinstance(rec, dict):
                    continue
                lines.append(f"{rec.get('title', '')}")
                lines.append(f"fecha_inicial: {rec.get('fecha_inicial')}")
                lines.append(strip_html(rec.get("descripcion") or ""))
                lines.append("")
        else:
            lines.append(strip_html(json.dumps(records, ensure_ascii=False)))
        out.write_text("\n".join(lines), encoding="utf-8")
    elif path.suffix in (".html", ".htm"):
        out = path.with_suffix(".html.txt")
        out.write_text(strip_html(decode_bytes(path.read_bytes())) + "\n", encoding="utf-8")
    elif path.suffix == ".txt":
        return path
    else:
        raise SystemExit(f"unsupported type, no text written: {path}")
    return out


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        print(convert(Path(arg)))
