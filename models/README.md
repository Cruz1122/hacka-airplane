# models/

Model files are too large for git. Only this README is tracked: copy the files you receive into exactly this layout.

```text
models/
├── README.md                              (tracked)
├── knowledge/                             required by the app, ~719 MB
│   ├── e5-nlu-ft4-f16.gguf                563 MB  query embedder (fine-tuned multilingual-e5-base)
│   ├── index.f32.bin                       78 MB  index vectors
│   └── index_scorer.onnx                   78 MB  native scorer (one MatMul over the vectors)
└── laya/                                  optional, ~700 MB
    ├── onnx/laya_final.gather_int8.onnx   699 MB  Laya reorderer, int8
    ├── tokenizer/tokenizer.json            34 MB
    ├── tokenizer/tokenizer_config.json
    ├── encoder/config.json
    ├── questions.json
    ├── rl_agent_config.json
    └── train_report.json
```

## Check the files

From the repo root:

```bash
sha256sum -c models.sha256
```

All five lines must pass (`OK`, or the equivalent in your locale). If you skip Laya, its two lines fail, and that is expected.

## What uses each folder

| Folder | Used by | Can it be rebuilt? |
|---|---|---|
| `knowledge/` | The app on the phone (`mobile/scripts/push-knowledge.sh`), the web chat (`mobile/metro.config.js`), and the exporters in `experiments/` | The GGUF cannot: it was trained in Colab from a payload that is not in git, so keep a backup. The index and scorer are rebuilt from the GGUF by `experiments/nlu/export_nlu.py` (see `docs/architecture.md`) |
| `laya/` | Only when Laya is turned on (`policy.laya.enabled`, off by default): `push-knowledge.sh --with-laya` and the Python experiments in `experiments/laya/` | No, it comes from the Colab run `run_rlcd6` |

The app checks each file's byte size against `mobile/assets/data/knowledge/index.json`.
