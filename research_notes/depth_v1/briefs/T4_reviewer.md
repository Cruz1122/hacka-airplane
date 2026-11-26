# T4 reviewer — query variants

You check visitor questions written by another model for an offline park assistant. Each variant
must be answered by its entry's KEY facts alone (the first reply gives only those). A wrong variant
teaches the retriever the wrong answer, so be strict.

## Read only
- The shard and the variants file given in the task. Nothing else. No web.

## Output
Write ONLY the output path given in the task: JSONL, one row per variant, in input order, appended as
you go. Reply with one line: "<output path> <rows>".

{"vid": "...", "verdict": "ok|fix|drop", "entry_id": "<only for fix: the shard entry that answers it>", "note": "<short>"}

## Rules
1. `ok`: the entry's `key_facts` answer the variant directly and completely, and it reads like a real
   visitor in its bucket.
   A `fragment` row is SUPPOSED to be 1–4 words with no question form, like a search box
   ("tarifa estudiante", "frailejones páramo"): judge only whether those words point to this entry.
   Never drop a fragment for being incomplete.
2. `fix`: another entry IN THIS SHARD answers it better; give that `entry_id`.
3. `drop`: it needs a fact not in `key_facts`; it asks what a `do_not_ask` label covers; it is a
   bare continuation cue; it copies an example or the label; it is unnatural or not in its bucket
   (e.g. a "fragment" of 8 words, an "english" row in Spanish).
4. A `note` (≤12 words) is required for `fix` and `drop`.
