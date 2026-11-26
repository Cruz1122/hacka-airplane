# T3 layer verifier

Layer texts are what an offline park assistant says after the visitor asks "sigue". Each must
state only verified facts of its own entry.

## Read only
- The shard file (entries: `canonical_L0`, `key_facts`, `complements` with fids) and the layer rows
  file, both given in the task. Nothing else.

## Output
Write ONLY the output path given in the task. JSONL, one row per layer row, input order:
{"lid": "...", "verdict": "ok|drop", "note": "<= 12 words, required for drop>"}

## `ok` only if all hold, else `drop`
1. Every sentence states a tagged complement (`atoms`) or briefly restates a key fact / L0.
2. Each tagged complement is stated with identical numbers, units, dates and names, and with no
   change of meaning (no softening, hardening, generalising, or moving facts to another place).
3. Nothing is added: no reason, consequence, example, advice or comparison absent from the facts.
4. It reads as natural Colombian Spanish and is not padded with filler.
