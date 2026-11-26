# Models, notebooks, and generated artifacts

## Purpose

Locate the model files the app loads, the tools that produce them, and the inputs that git cannot rebuild.

## Start here

- `models/README.md` lists the expected tree. `.gitignore` ignores `models/*` except that README.
- `models.sha256` pins five files. Check them with `sha256sum -c models.sha256`.
- `mobile/assets/data/knowledge/index.json` names the loaded files and their `bytes` under `embedder`, `vectors`, and `scorer`. It pins `e5-nlu-ft4-f16.gguf`.
- `research_notes/dataset_final/tools/` builds the Laya dataset package. `package_src/` holds the validators and docs that ship inside it.

## Runtime or data flow

1. `experiments/nlu/build_payload.py` writes an e5 training payload, `work/payload_ft5.json` in its usage line. `colab_train.py` trains in Colab.
2. `experiments/nlu/export_nlu.py --gguf ...` writes `index.f32.bin` and `index_scorer.onnx` to `models/knowledge/` and the JSON assets to `mobile/assets/data/knowledge/`. It calls an external `llama-embedding` binary.
3. `mobile/scripts/push-knowledge.sh` copies the files named in `index.json` to the phone. `--with-laya` adds the Laya ONNX and tokenizer.
4. `mobile/metro.config.js` serves the embedder and the vectors to the web chat. `mobile/src/llm/knowledgeRuntime.ts` and `knowledgeRuntime.web.ts` pass the manifest `bytes` to their loaders.

Laya has two separate training paths:

- `notebooks/finetune_laya.ipynb` reads `laya_ft.zip` from `experiments/laya/ft_data.py build`. It cannot read the `dataset_final` package.
- The package follows `package_src/reports/COLAB_HANDOFF.md`. No tracked notebook runs it. From `experiments/laya`, `build_dataset.py pools` writes `work/pairs_todo.jsonl`. `build_dataset.py build` reads `judgments/pairs.*.jsonl` and needs `finalize_knowledge.py` first. `package.py` writes `MANIFEST.json` and a zip under the ignored `out/`, then runs the four `package_src/scripts` checks in place and on the extracted zip.

## Tests

`loadVectors` in `mobile/src/core/knowledge/__fixtures__/load.ts` throws when `models/knowledge/index.f32.bin` is missing or its SHA-256 differs. `KNOWLEDGE_VECTORS` overrides the path. Five tests in `mobile/src/core/knowledge/__tests__/` call it. A grep found no test for `dataset_final/tools` or the notebook.

## Common change paths

- To swap the embedder, follow the blast-radius table linked below. `sweep_v4.py` names an ft5 GGUF, but `index.json` and `models.sha256` pin ft4.
- `experiments/laya/bench_v2.py`, `quant_sweep.py`, and `gguf_parity.py` read `models/laya_ft_A/` or `models/laya_final_rlcd6_raw/`. Neither directory is in `models/README.md` or `models.sha256`.

Git cannot rebuild the GGUF, the `llama-embedding` binary, `models/laya/`, or `research_notes/depth_v1/blind_v4/all_rows.jsonl`, an untracked `build_payload.py` input. `tools/build_g2_proposal.py` hardcodes an absolute `ROOT`.

## Related docs

- [models/README.md](../../../models/README.md)
- [System map: blast radius](../../system-map.md#blast-radius-if-you-change-x-redo-y)
- [System map: nodes that git cannot rebuild](../../system-map.md#nodes-that-are-not-rebuildable-from-git)
- [Laya dataset package README](../../../research_notes/dataset_final/package_src/README.md)
