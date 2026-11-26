# T5b top-up writer — more reply paraphrases for entries below goal

Read `/home/cruz1122/dev/hacka-airplane/research_notes/depth_v1/briefs/T5b_writer.md` first: every rule
there applies (key facts, atoms, numbers, structures, registers, voice, safety). This file only
changes what you write.

## Per entry
- Write `need` NEW paraphrases of `canonical_L0`. pid: "<entry_id>#u01", "#u02", ...
- `approved` lists texts already accepted. Yours must differ from each of them AND from each other
  (no shared first 4 words, character-trigram similarity < 0.55). Do not copy their openings or their
  sentence order. If `approved` lacks a structure (`direct`, `context`, `advice`, `question_back`) or,
  with ≥2 complements, a second atom subset, cover it.

## Self-check (required)
`cd /home/cruz1122/dev/hacka-airplane/research_notes/depth_v1/tools && python3 check_replies.py <your output path> --base ../resolved/<shard>.base.jsonl`
Rewrite rejected rows in place, up to 4 rounds. Reply with one line:
"<output path> <rows> <entries below goal>".
