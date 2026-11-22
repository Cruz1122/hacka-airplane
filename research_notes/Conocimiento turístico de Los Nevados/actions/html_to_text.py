"""Convert a saved HTML page to plain text for evidence reading.

Usage: python3 -I html_to_text.py <input.html> <output.txt>
Drops script/style blocks and collapses whitespace. Stdlib only.
"""

import html.parser
import re
import sys


class _TextExtractor(html.parser.HTMLParser):
    _SKIP = {"script", "style", "noscript", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ARG002
        if tag in self._SKIP:
            self._skip_depth += 1
        elif tag in {"p", "br", "li", "h1", "h2", "h3", "h4", "tr", "div", "section"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self._SKIP and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            self.parts.append(data)


def main() -> None:
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    parser = _TextExtractor()
    parser.feed(raw)
    text = "".join(parser.parts)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text).strip() + "\n"
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"wrote {dst}: {len(text)} chars")


if __name__ == "__main__":
    main()
