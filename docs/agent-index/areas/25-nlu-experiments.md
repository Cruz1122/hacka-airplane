# NLU experiments

## Purpose

`experiments/nlu/` fine-tunes and evaluates the multilingual-e5 retrieval embedder and exports the knowledge assets the phone loads. Scripts import `kb.py` for entries (`load_entries`, `load_hubs`), app-layer texts (`app_texts`), the filler cleaner (`clean`), and cached embeddings (`Embedder`, cache in `work/emb_cache/`).

## Start here

| Task | File | Environment |
|---|---|---|
| Export phone assets | `export_nlu.py` (`load`, `entry_scores`, `fuse`, `depth_assets`) | `experiments/laya` uv env. It imports `experiments/laya/export_knowledge.py` and needs the external `llama-embedding` binary |
| Phone-faithful replay | `gguf_eval.py`, `sweep_v4.py`, `gate_sweep.py`, `gateway_ab.py` | `experiments/laya` env plus a GGUF |
| Python-side eval | `evaluate.py` (`load_blind`, `Index`), `context_eval.py`, `head_eval.py`, `pseudo_dev.py`, `probe.py` | `experiments/nlu` env (`pyproject.toml`, Python 3.12, CUDA 12.6 torch) |
| Training | `finetune.py` (local), `colab_train.py` (pasted into Colab, reads `/content/payload.json`) | GPU |
| Training payload | `build_payload.py` | `experiments/nlu` env |

## Runtime or data flow

1. `build_payload.py` writes `{pools, blind}`. It drops every text whose folded key matches a turn of `research_notes/depth_v1/blind_v4/all_rows.jsonl`. That directory is untracked and exists only in the live checkout.
2. `colab_train.py` trains with symmetric InfoNCE and scores dev accuracy. No script here converts the model to GGUF.
3. `export_nlu.py --gguf ... --T --w --max-words --below` writes the generated `mobile/assets/data/knowledge/*.json`, `models/knowledge/{index.f32.bin,index_scorer.onnx}`, and fixtures in `mobile/src/core/knowledge/__fixtures__/`.

Work datasets by role:

- Blind eval: `work/queries_raw.jsonl` with `labels_[0-9]*.jsonl` and `labels_hub_*.jsonl` (`load_blind`, hash split dev or test), and `work/blind_v2/`, `work/blind_v3/` (`gate_sweep.load_v2`).
- Fixture probes: `export_nlu.py` also reads `queries_raw.jsonl`.
- Labeling hints: `candidates.py` writes `queries_with_candidates.jsonl`.
- Unread by these scripts: `aug/`, `conv/`, `natural*/`, `polish/`, `sec_view/`, `label_shard_*`, hub drafts. Their producer is not in this folder.

## Tests

No Python tests exist here. Jest parity tests consume the exported fixtures: `retrieve.test.ts`, `retrieve_sims.test.ts`, `engine.test.ts` (`retrieval.json`), `clean.test.ts` (`clean.json`), `continuation.test.ts` and `e2e_sigue.test.ts` (`continuation.json`), all in `mobile/src/core/knowledge/__tests__/`.

## Common change paths

- Scoring or follow-up change: edit `export_nlu.entry_scores` or `fuse` together with `mobile/src/core/knowledge/retrieve.ts` and `engine.ts`, then re-export to refresh the fixtures.
- Continuation cue: edit `CONT_CUE` in `export_nlu.py`, then re-export.

## Related docs

- [Regenerating the assets](../../architecture.md#regenerating-the-assets)
- [System map](../../system-map.md)
- [Retrieval architecture](../../retrieval-architecture.md)
