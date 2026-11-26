# T5b second review — safety, rule and emergency reply paraphrases

These texts already passed one review. They answer visitors in a national park with volcanoes,
altitude and emergencies, so every one gets a second, independent check.

## Read only
- The paraphrases file given in the task. Each row carries `entry{canonical_L0,key_facts,complements}`; judge against it, never without it.

## Output
Write ONLY the output path given in the task: JSONL, one row per paraphrase, in input order:
{"pid": "...", "verdict": "ok|drop", "emergency_ok": true|false, "note": "<≤12 words, required for drop or emergency_ok false>"}

## Rules
1. `ok` only if the text states every key fact with identical numbers, names and phone numbers;
   keeps every caveat, warning and condition; keeps every step (an action the visitor performs);
   keeps the canonical order of steps that depend on each other (one must happen before the next,
   e.g. stop, then descend, then call); steps that do not depend on each other, caveats and context
   sentences may move when the text stays coherent and natural; does not move
   who does what; does not soften or harden any requirement; adds nothing outside the key facts, its
   `atoms` complements and `canonical_L0`. Otherwise `drop`.
2. `emergency_ok` (meaningful when the row has `"emergency": true`; set false otherwise): true only
   if the text keeps 100 % of the caveats and 100 % of the steps of `canonical_L0`, in order, with the
   emergency number exactly as given. Any doubt: false.
