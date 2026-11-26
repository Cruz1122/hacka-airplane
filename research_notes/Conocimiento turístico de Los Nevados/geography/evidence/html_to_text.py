"""Extract visible text from a saved HTML page into a sibling .txt (stdlib only).

Quotes in quotes.md are checked against these .txt files, which are derived from the raw HTML
kept next to them. Run: python3 -I html_to_text.py <file.html> ...
"""

import html
import sys
from html.parser import HTMLParser
from pathlib import Path

SKIP = {"script", "style", "noscript", "svg"}
BLOCK = {"p", "div", "li", "br", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "td", "th", "dt", "dd"}


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1
        elif tag in BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP and self.skip:
            self.skip -= 1
        elif tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def main():
    for name in sys.argv[1:]:
        source = Path(name)
        parser = Extractor()
        parser.feed(source.read_text(encoding="utf-8"))
        text = html.unescape("".join(parser.parts))
        lines = [" ".join(line.split()) for line in text.splitlines()]
        out = "\n".join(line for line in lines if line)
        source.with_suffix(".txt").write_text(out + "\n", encoding="utf-8")
        print(f"{source.name}: {len(out)} chars")


if __name__ == "__main__":
    main()
