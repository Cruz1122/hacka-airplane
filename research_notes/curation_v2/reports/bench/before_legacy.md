# Before curation v2: LEGACY / NOT BLIND

This historical 1,790-row evaluation is diagnostic only. It did not inform thresholds or curation choices. Retrieval uses the same e5-base cache-backed implementation for both modes. Laya uses `models/laya_ft_A/onnx/laya_ft.gather_only.onnx` (embedding Gather quantized to int8, remaining layers fp32).

| Mode | Recall@1 | Recall@3 | Recall@5 | Gateway section recall | e5 top-1 | e5 + Laya + cosine | Laya none rejection | LAPTOP p50 / p95 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Flat | 63.25% | 82.15% | 87.61% | — | 63.25% | 69.26% | 55.00% | 194.9 / 254.2 ms |
| Gateway | 63.25% | 81.10% | 84.60% | 97.48% | 63.25% | 69.14% | 56.87% | 218.0 / 462.6 ms |

Top-1 intervals are Wilson 95%. Section-level breakdowns, false rejections, accepted-answer precision, unseen-topic slice, and option-order robustness are in [`before_legacy.json`](before_legacy.json). Latency is LAPTOP, ONNX inference only; retrieval and embedding are excluded.
