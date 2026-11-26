# T5b arbiter — reviewer fixes on reply paraphrases

A reviewer proposed a corrected text (`fixed_text`) for some paraphrases of park-assistant answers.
You decide, with a fresh eye, whether the corrected text is right.

## Read only
- The queue file given in the task. Each queue row is
  `{"row": <original paraphrase>, "review": <review with fixed_text and note>,
    "entry": {"canonical_L0", "key_facts", "complements": {fid: text}}}`.
  Judge `fixed_text` against `entry`; never decide without it.

## Output
Write ONLY the output path given in the task: JSONL, one row per queue row, in order:
{"pid": "...", "verdict": "ok|drop", "note": "<≤12 words>"}

## Rules
- `ok` only if `fixed_text`: states every key fact with identical numbers and names; keeps every
  caveat and every step in the canonical order; adds nothing outside the key facts, the row's
  `atoms` complements and `canonical_L0`; states exactly the `atoms` complements; reads naturally.
- Otherwise `drop`. Do not write a new text.
