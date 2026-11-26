# Colab handoff: retrain Laya once

Target: one fine-tune of `telepatia-ai/laya-pt-es-nli` (revision
`71459abd38f4e439b2f4e3a2dae87573ae40c77e`) on `train/train.jsonl`. Model and configuration
decisions use `validation/checkpoint_selection.jsonl` only. App thresholds use
`validation/calibration.jsonl` only. The sealed splits are evaluated once, at the end.

Expected time on a Colab T4: about 5 minutes for setup and validation. Training time was not
measured: no training was run while this dataset was being built.

## 1. Setup

```python
!unzip -q LOS_NEVADOS_LAYA_FINAL_DATASET.zip
%cd LOS_NEVADOS_LAYA_FINAL_DATASET
!pip install -q -r requirements.txt     # keep Colab's preinstalled torch
```

`!cd` does not persist in Colab, so use `%cd`. Every later command and every relative path,
including `eval_data`, assumes the working directory is `LOS_NEVADOS_LAYA_FINAL_DATASET/`. In a
notebook, prefix the bash lines below with `!`, and write `$BASE` as `{BASE}`.

## 2. Validate the package (all must exit 0)

```bash
python scripts/verify_manifest.py
python scripts/validate_dataset.py
python scripts/validate_splits.py
python scripts/check_leakage.py
python scripts/check_leakage.py --semantic   # optional; downloads intfloat/multilingual-e5-base
```

Then check that laya 0.5.1's own loader accepts every training row:

```python
from huggingface_hub import snapshot_download
BASE = snapshot_download("telepatia-ai/laya-pt-es-nli", revision="71459abd38f4e439b2f4e3a2dae87573ae40c77e")
```
```bash
python scripts/validate_dataset.py --laya "$BASE"   # expects 8275 train items, 0 skipped
```

## 3. Baseline before training

Score the base model and the "always option 1" baseline (= e5 top-1) on the selection split:

```bash
python scripts/predict.py "$BASE" validation/checkpoint_selection.jsonl --out preds_base_sel.jsonl
python scripts/evaluate_predictions.py preds_base_sel.jsonl
python scripts/evaluate_predictions.py preds_base_sel.jsonl --baseline first_option
```

If you have the previous fine-tuned checkpoint, run the same commands on it now. All later
comparisons must use the same files.

## 4. Fine-tune (once)

```python
from laya.train import TrainConfig, finetune
cfg = TrainConfig(
    shuffle_options=("choice",),          # required: 71% of positive train targets are option 1 (e5 order)
    eval_data="validation/checkpoint_selection.jsonl",
    seed=20261126,
)
summary = finetune("train/train.jsonl", BASE, "laya_nevados_ft", config=cfg, device="cuda")
print(summary)
```

What laya 0.5.1 `finetune` does, as read from its source:

- It holds out 10% of the train items (capped at 400, `calib_seed`) as an internal calibration
  slice. On that slice it fits the temperature and its own abstention thresholds (`target_error=0.1`).
  It never uses `eval_data` for fitting.
- `eval_data` is scored only before and after training, giving the before/after metrics in
  `summary`. Every row of `checkpoint_selection` is disjoint from train, so laya reports it as
  `held_out`. If `summary` says `overlapping_eval`, stop and report it.
- It writes `output_dir/checkpoint_latest` after each epoch (overwritten) and the final model to
  `output_dir`. There is no per-epoch best-checkpoint selection.

Keep the other `TrainConfig` defaults: 4 epochs, `micro_batch=8`, `grad_accum=8`, and `max_len`
and `head_max_len` from the checkpoint (512 and 192).

- Do not add any other split to `data` or `eval_data`.
- If you compare configurations (for example 3 vs 4 epochs), choose using `checkpoint_selection`
  metrics only.
- Without `shuffle_options` the model can learn "pick option 1". The first-option baseline
  catches this.

## 5. Calibrate (calibration split only)

```bash
python scripts/predict.py laya_nevados_ft validation/calibration.jsonl --out preds_cal.jsonl
python scripts/evaluate_predictions.py preds_cal.jsonl
```

laya's internal thresholds come from train-distribution items. The app's answer, clarify and
abstain thresholds are fitted on `preds_cal.jsonl` only, using `probabilities`:

1. Answer directly when the top option's probability is at least `t_answer`.
2. Show the top-3 clarification menu (labels from `knowledge/clarification_labels.json`) when the
   probability is between `t_clarify` and `t_answer`.
3. Abstain below `t_clarify`, or when the top choice is `ninguna de estas opciones`.

Do not tune on unseen, adversarial, final or retrospective files.

## 6. Final evaluation (once, after thresholds are frozen)

```bash
python scripts/predict.py laya_nevados_ft validation/unseen_topics.jsonl evaluation/adversarial.jsonl \
  evaluation/final_test_SEALED.jsonl evaluation/retrospective_test_blind_READ_ONLY.jsonl --out preds_final.jsonl
python scripts/evaluate_predictions.py preds_final.jsonl
python scripts/evaluate_predictions.py preds_final.jsonl --baseline first_option
```

The output is accuracy with Wilson 95% intervals, by file, outcome, `none_cause`, scenario and
provenance, plus top-3 containment for `clarify` and `multi_positive` rows. Report:

- `final_test_SEALED`: the headline number.
- `unseen_topics`: generalisation to FAQs with no training examples.
- `adversarial`: robustness.
- `retrospective`: comparison with earlier checkpoints only.
- `none_cause=retrieval_miss` vs `true_out_of_scope`: abstention quality.

`historical_READ_ONLY.jsonl` uses pools from an older corpus. Use it only to compare checkpoints,
never as a quality claim.

## 7. App contract (must match the dataset)

- Retrieval follows `knowledge/sections.json → retrieval_contract`:
  - e5-base with the `query: ` prefix.
  - Gateway: up to 5 sections within 0.05 of the best section score.
  - Each section's `retrieval.top_k`, capped at 5 candidates.
  - **Flat fill up to 3 candidates** when the gateway yields fewer.
  - Option text is the label, or `label (section)` on collision. The last option is `ninguna de estas opciones`.
- **Emergency bypass**: show the answer at once, with no clarification menu, when either of these
  has policy `emergency_direct` in `knowledge/answer_policy.json` (40 ids):
  - the selected FAQ;
  - e5's top candidate, when Laya abstains.
- No answer text claims that the device contacts rescue or registers a visit. Keep it that way
  in any edit made after this dataset.

## 8. Hand back

Return all of these:

- `summary`, including before/after on checkpoint_selection and the loss history
- the chosen thresholds
- the output of both `evaluate_predictions.py` runs in step 6, with and without `--baseline`
- the checkpoint directory
