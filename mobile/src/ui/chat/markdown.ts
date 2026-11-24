// The Markdown subset a chat reply may use: paragraphs (split by blank lines), `- ` and `1. ` list
// items (a line of their own, also straight under a paragraph line, the way catalog answers write
// them) and `**bold**`. Parsed once into flat blocks of spans; the bubble reveals a prefix of that
// model by visible characters, so a half-written `**` never reaches the screen.
import { parseCitations } from './citations';

export interface Span {
  text: string;
  bold: boolean;
}

export interface Block {
  /** `null` for a paragraph; `•` or the source's own number (`2.`) for a list item. */
  marker: string | null;
  spans: Span[];
}

export interface MdDoc {
  blocks: Block[];
  /**
   * Visible length at the end of each word and the whitespace after it, counted over the blocks'
   * span text only (a block break counts nothing): where a word-by-word reveal may stop.
   */
  stops: number[];
  /** Every visible character, one block per line with its marker: the bubble's accessible label. */
  text: string;
}

const ITEM = /^(?:(-)|(\d{1,3})\.)[ \t]+(\S.*)$/;

export function parseMarkdown(source: string): MdDoc {
  const groups: { marker: string | null; lines: string[] }[] = [];
  let open: (typeof groups)[number] | null = null;
  for (const raw of source.replace(/\r\n?/g, '\n').split('\n')) {
    const line = raw.trim();
    if (!line) {
      open = null;
      continue;
    }
    const item = ITEM.exec(line);
    if (item) {
      open = { marker: item[1] ? '•' : `${item[2]}.`, lines: [item[3]] };
      groups.push(open);
      continue;
    }
    // A plain line under an item starts a paragraph: catalog items are one line each, and a
    // closing sentence after a list belongs to no bullet.
    if (!open || open.marker !== null) {
      open = { marker: null, lines: [] };
      groups.push(open);
    }
    open.lines.push(line);
  }
  const blocks = groups
    .map((g) => ({ marker: g.marker, spans: parseInline(g.lines.join('\n')) }))
    .filter((b) => b.spans.length > 0);

  const stops: number[] = [];
  let offset = 0;
  const lines: string[] = [];
  for (const b of blocks) {
    const text = b.spans.map((s) => s.text).join('');
    for (const word of text.matchAll(/\S+\s*/g)) stops.push(offset + word.index + word[0].length);
    offset += text.length;
    lines.push(b.marker ? `${b.marker} ${text}` : text);
  }
  return { blocks, stops, text: lines.join('\n') };
}

/** `**` pairs toggle bold; `\*` and `\\` are literal; an unpaired last `**` stays as text. */
function parseInline(source: string): Span[] {
  const parts: string[] = [];
  let buf = '';
  for (let i = 0; i < source.length; i++) {
    const c = source[i];
    const next = source[i + 1];
    if (c === '\\' && (next === '*' || next === '\\')) {
      buf += next;
      i++;
    } else if (c === '*' && next === '*') {
      parts.push(buf);
      buf = '';
      i++;
    } else {
      buf += c;
    }
  }
  parts.push(buf);
  if (parts.length % 2 === 0) {
    const tail = parts.pop()!;
    parts[parts.length - 1] += `**${tail}`;
  }
  const spans: Span[] = [];
  parts.forEach((text, i) => {
    if (!text) return;
    const bold = i % 2 === 1;
    const last = spans.at(-1);
    if (last?.bold === bold) last.text += text;
    else spans.push({ text, bold });
  });
  return spans;
}

/** The first `chars` visible characters of `doc`, as blocks; unchanged blocks keep their identity. */
export function sliceDoc(doc: MdDoc, chars: number): Block[] {
  const out: Block[] = [];
  let left = chars;
  for (const block of doc.blocks) {
    if (left <= 0) break;
    const spans: Span[] = [];
    for (const span of block.spans) {
      if (left <= 0) break;
      spans.push(
        left >= span.text.length ? span : { text: span.text.slice(0, left), bold: span.bold },
      );
      left -= span.text.length;
    }
    const whole = spans.length === block.spans.length && left >= 0;
    out.push(whole ? block : { marker: block.marker, spans });
  }
  return out;
}

const LETTER = /[\p{L}\p{M}]/u;
const isLetter = (c: string | undefined) => c !== undefined && LETTER.test(c);

/**
 * Where `keyword` first occurs in `text` as whole words (no letter runs on across its edges), or
 * -1. A keyword with a line break, or blank edges, never matches: bold never spans two blocks.
 */
export function findKeyword(text: string, keyword: string): number {
  if (!keyword || keyword.trim() !== keyword || keyword.includes('\n')) return -1;
  const first = keyword[0];
  const last = keyword[keyword.length - 1];
  for (let at = text.indexOf(keyword); at >= 0; at = text.indexOf(keyword, at + 1)) {
    const end = at + keyword.length;
    const openOk = !(isLetter(first) && isLetter(text[at - 1]));
    const closeOk = !(isLetter(last) && isLetter(text[end]));
    if (openOk && closeOk) return at;
  }
  return -1;
}

const escapeMarkdown = (s: string) => s.replace(/[\\*]/g, '\\$&');

/**
 * Plain text as Markdown with each keyword's first whole-word occurrence in bold: longest first,
 * and a keyword whose first occurrence sits inside a longer one's stays plain. The text's own `*`
 * and `\` are escaped, so they show as written.
 */
export function emphasize(plain: string, keywords: readonly string[]): string {
  const ranges: [number, number][] = [];
  for (const keyword of [...keywords].sort((a, b) => b.length - a.length)) {
    const at = findKeyword(plain, keyword);
    const end = at + keyword.length;
    if (at < 0 || ranges.some(([s, e]) => at < e && s < end)) continue;
    ranges.push([at, end]);
  }
  ranges.sort((a, b) => a[0] - b[0]);
  let out = '';
  let from = 0;
  for (const [start, end] of ranges) {
    out += `${escapeMarkdown(plain.slice(from, start))}**${escapeMarkdown(plain.slice(start, end))}**`;
    from = end;
  }
  return out + escapeMarkdown(plain.slice(from));
}

/** An assistant reply as shown: citation markers out, keywords in bold, Markdown parsed. */
export function replyDoc(text: string, keywords: readonly string[]): MdDoc {
  return parseMarkdown(emphasize(parseCitations(text).prose, keywords));
}
