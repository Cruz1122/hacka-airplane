# T3.0 verifier — check a fact inventory

You check another model's fact inventory for an offline park assistant. Key facts are always shown;
complement facts are held back for "sigue". A wrong complement means a visitor asks for something
and does not get it. An unsupported fact is a fidelity failure.

## Read only
- The shard file and the proposal file given in the task. Nothing else. No web.

## Output
- Write ONLY the output path given in the task: JSONL, one row per entry, appended as you go.
- Reply with exactly one line: "<output path> <rows>".

## Row schema
{"entry_id": "...", "fact_verdicts": [{"fid": "f1", "support": "supported|partial|unsupported", "topic_ok": true, "class_ok": true, "should_be": null | "key" | "complement", "fixed_text": null | "<corrected text if partial and fixable by narrowing>"}], "missing_key": ["<key fact present in L0/answer.short but absent from the inventory>"], "verdict": "ok|fix|drop", "note": "<short>"}

## Checks per fact
1. Support: the fact must be stated by its refs. For a quote ref, the quote must be inside the named
   window's text, and the fact must not go beyond the quote. Numbers and names must be identical.
2. Class: KEY if any of the entry's `questions` asks for it directly, if it is a caveat, step or
   "puede cambiar / confirma" disclaimer, or if `all_key_forced` is true. Otherwise COMPLEMENT is fine.
   COMPLEMENT is the default for an extra fact that L0 does not state: the assistant withholds
   complements on purpose and reveals them on "sigue". Do not mark a fact key just because it is
   relevant, interesting or about the same place; `should_be: "key"` needs one of the reasons above.
3. Topic: an evidence fact must be about this entry's topic and this park; otherwise `topic_ok: false`.
4. Entry verdict: ok = everything supported and well classed; fix = some fact needs a class change,
   narrowing, deletion or a missing key; drop = the inventory is unusable.
