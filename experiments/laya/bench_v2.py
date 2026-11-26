"""Run paired retrieval/reranking measurements on the frozen blind split."""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import time
from collections import defaultdict
from pathlib import Path

import numpy as np

from retrieval import ROOT, Retriever

NONE = "ninguna de estas opciones"
MODEL_PATH = ROOT / "models/laya_ft_A/onnx/laya_ft.int8.onnx"
TARGET_WRONG_RATE = 0.03
TARGET_COVERAGE = 0.365


def wilson(successes: int, total: int) -> dict:
    if total == 0:
        return {"k": 0, "n": 0, "rate": None, "lo": None, "hi": None}
    z = 1.96
    rate = successes / total
    denom = 1 + z * z / total
    center = (rate + z * z / (2 * total)) / denom
    margin = z * math.sqrt(rate * (1 - rate) / total + z * z / (4 * total * total)) / denom
    return {"k": successes, "n": total, "rate": round(rate, 4), "lo": round(center - margin, 4), "hi": round(center + margin, 4)}


def read_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def is_correct(row: dict, prediction: str | None) -> bool:
    return prediction in set(row.get("acceptable", [])) if prediction is not None else False


def load_agent(path: Path):
    from laya.onnx_agent import ONNXAgent
    return ONNXAgent(str(path.parent.parent), onnx_path=str(path))


def run_laya(agent, question: str, candidates, shuffled: bool = False) -> tuple[dict[str, float], float]:
    options, label_to_id = [], {}
    for candidate in candidates:
        label = candidate.label
        if label in label_to_id or label == NONE:
            label = f"{label} ({candidate.section})"
        label_to_id[label] = candidate.id
        options.append(label)
    if shuffled:
        random.Random(6201).shuffle(options)
    options.append(NONE)
    item = {"topic": {"type": "choice", "instructions": "¿Qué tema contesta la pregunta del visitante?", "criteria": options}}
    output = agent.system_one(question, item)["answers"]["topic"]["probabilities"]
    return {label_to_id[label]: float(output.get(label, 0.0)) for label in label_to_id}, float(output.get(NONE, 0.0))


def choose(candidates, probabilities: dict[str, float], *, add_cosine: bool) -> str | None:
    if not candidates:
        return None
    return max(candidates, key=lambda candidate: (probabilities.get(candidate.id, 0.0) + (candidate.score if add_cosine else 0.0), candidate.id)).id


def is_rejected(prediction: dict, field: str) -> bool:
    return field != "e5" and prediction["none_pick"]


def predict(retriever: Retriever, rows: list[dict], vectors: np.ndarray, mode: str, agent, *, tau_gate: float, order_sample: set[int]) -> tuple[list[dict], list[float]]:
    predictions, latency = [], []
    for index, (row, vector) in enumerate(zip(rows, vectors, strict=True)):
        start = time.perf_counter()
        result = retriever.retrieve(vector, mode=mode, k=5, tau_gate=tau_gate, delta=0.05)
        candidates = result["candidates"]
        scores = result["scores"]
        ranked = [retriever.ids[position] for position in np.argsort(-scores, kind="stable")]
        probabilities, none_probability = run_laya(agent, row["q"], candidates) if candidates else ({}, 0.0)
        laya_pick = choose(candidates, probabilities, add_cosine=False)
        combined_pick = choose(candidates, probabilities, add_cosine=True)
        none_pick = none_probability >= max(probabilities.values(), default=0.0)
        confs = {
            "e5": max((candidate.score for candidate in candidates), default=0.0),
            "laya": probabilities.get(laya_pick, 0.0) if laya_pick else 0.0,
            "laya_cos": probabilities.get(combined_pick, 0.0) + next((candidate.score for candidate in candidates if candidate.id == combined_pick), 0.0) if combined_pick else 0.0,
        }
        latency.append((time.perf_counter() - start) * 1000)
        shuffled_pick = None
        if index in order_sample and candidates:
            shuffled_probs, _ = run_laya(agent, row["q"], candidates, shuffled=True)
            shuffled_pick = choose(candidates, shuffled_probs, add_cosine=True)
        predictions.append({
            "pool": [candidate.id for candidate in candidates],
            "ranked": ranked,
            "gate_sections": [section for section, _ in result["gates"]],
            "e5": candidates[0].id if candidates else None,
            "laya": laya_pick,
            "laya_cos": combined_pick,
            "none_pick": none_pick,
            "confidence": confs,
            "none_probability": none_probability,
            "shuffled_laya_cos": shuffled_pick,
        })
    return predictions, latency


def fit_threshold(rows: list[dict], predictions: list[dict], field: str) -> tuple[float, dict]:
    values = sorted({prediction["confidence"][field] for prediction in predictions})
    best = (0, float("inf"), 0)
    for threshold in values:
        accepted = [(row, prediction) for row, prediction in zip(rows, predictions, strict=True)
                    if not is_rejected(prediction, field) and prediction["confidence"][field] >= threshold]
        wrong = sum(not is_correct(row, prediction[field]) for row, prediction in accepted)
        if accepted and wrong / len(accepted) <= TARGET_WRONG_RATE and len(accepted) > best[0]:
            best = (len(accepted), threshold, wrong)
    threshold = best[1]
    selected = [(row, prediction) for row, prediction in zip(rows, predictions, strict=True)
                if not is_rejected(prediction, field) and prediction["confidence"][field] >= threshold]
    wrong = sum(not is_correct(row, prediction[field]) for row, prediction in selected)
    return threshold, {"fit_rows": len(rows), "accepted": len(selected), "wrong": wrong, "wrong_rate": wrong / len(selected) if selected else None}


def categorize_misses(rows: list[dict], predictions: list[dict], mode: str) -> dict:
    misses: dict[str, list[str]] = defaultdict(list)
    known = ["e5_global_top5_miss", "e5_top1_miss", "laya_cos_selected_wrong", "laya_cos_pool_hit_rerank_miss", "none_case_not_rejected_by_laya", "ambiguous_case_not_clarified_by_laya"]
    known.extend(("gateway_section_miss", "gateway_candidate_pool_miss") if mode == "gateway" else ("flat_candidate_pool_miss",))
    for row, pred in zip(rows, predictions, strict=True):
        qid = row.get("qid", "unknown")
        acceptable = set(row.get("acceptable", []))
        if row.get("case") == "answerable":
            if not acceptable.intersection(pred["ranked"][:5]):
                misses["e5_global_top5_miss"].append(qid)
            if not acceptable.intersection(pred["pool"]):
                if mode == "gateway" and not acceptable.intersection(pred["gate_sections"]):
                    misses["gateway_section_miss"].append(qid)
                elif mode == "gateway":
                    misses["gateway_candidate_pool_miss"].append(qid)
                else:
                    misses["flat_candidate_pool_miss"].append(qid)
            elif pred["e5"] not in acceptable:
                misses["e5_top1_miss"].append(qid)
            if pred["laya_cos"] not in acceptable:
                misses["laya_cos_selected_wrong"].append(qid)
                if acceptable.intersection(pred["pool"]):
                    misses["laya_cos_pool_hit_rerank_miss"].append(qid)
        elif row.get("case") == "none" and not pred["none_pick"]:
            misses["none_case_not_rejected_by_laya"].append(qid)
        elif row.get("case") == "ambiguous" and not pred["none_pick"]:
            misses["ambiguous_case_not_clarified_by_laya"].append(qid)
    return {name: {"count": len(misses[name]), "qids": misses[name], "applicable": not name.startswith("gateway_") or mode == "gateway"} for name in sorted(set(known) | set(misses))}


def metric_bundle(rows: list[dict], preds: list[dict], field: str, threshold: float, mode: str) -> dict:
    answers = [(row, pred) for row, pred in zip(rows, preds, strict=True) if row.get("case") == "answerable"]
    none_rows = [(row, pred) for row, pred in zip(rows, preds, strict=True) if row.get("case") == "none"]
    answered = [(row, pred) for row, pred in zip(rows, preds, strict=True)
                if not is_rejected(pred, field) and pred["confidence"][field] >= threshold]
    correct = sum(is_correct(row, pred[field]) for row, pred in answered)
    by_sections: dict[str, list[tuple[dict, dict]]] = defaultdict(list)
    by_scenarios: dict[str, list[tuple[dict, dict]]] = defaultdict(list)
    for row, pred in zip(rows, preds, strict=True):
        section = (row.get("gold") or (row.get("acceptable") or ["unknown"])[0]).split(".")[0]
        by_sections[section].append((row, pred))
        by_scenarios[row.get("scenario", "unknown")].append((row, pred))

    def group_metrics(group):
        group_rows = [row for row, _ in group]
        group_preds = [pred for _, pred in group]
        group_answer_rows = [(row, pred) for row, pred in group if row.get("case") == "answerable"]
        group_accepted = [(row, pred) for row, pred in group if not is_rejected(pred, field) and pred["confidence"][field] >= threshold]
        group_correct = sum(is_correct(row, pred[field]) for row, pred in group_accepted)
        return {
            "n": len(group), "answerable": sum(row.get("case") == "answerable" for row in group_rows),
            "none": sum(row.get("case") == "none" for row in group_rows),
            "ambiguous": sum(row.get("case") == "ambiguous" for row in group_rows),
            "recall_at_1": wilson(sum(bool(set(row.get("acceptable", [])) & set(pred["pool"][:1])) for row, pred in group_answer_rows), len(group_answer_rows)),
            "recall_at_3": wilson(sum(bool(set(row.get("acceptable", [])) & set(pred["pool"][:3])) for row, pred in group_answer_rows), len(group_answer_rows)),
            "recall_at_5": wilson(sum(bool(set(row.get("acceptable", [])) & set(pred["pool"][:5])) for row, pred in group_answer_rows), len(group_answer_rows)),
            "selected_accuracy": wilson(sum(is_correct(row, pred[field]) for row, pred in group_answer_rows), len(group_answer_rows)),
            "accepted_precision": wilson(group_correct, len(group_accepted)),
            "coverage": wilson(len(group_accepted), len(group)),
        }

    return {
        "threshold": threshold if math.isfinite(threshold) else None,
        "threshold_fit_on": "dev_gate only",
        "threshold_objective": "maximize dev_gate answered rows with observed wrong rate <= 3%; none-picked rows remain rejected",
        "accepted_precision": wilson(correct, len(answered)),
        "accepted_wrong_rate": wilson(len(answered) - correct, len(answered)),
        "coverage": wilson(len(answered), len(rows)),
        "accepted_rows": len(answered),
        "answerable_rows": len(answers),
        "false_rejections": sum(is_rejected(pred, field) or pred["confidence"][field] < threshold for row, pred in answers),
        "none_case_rejection_rate": wilson(sum(is_rejected(pred, field) or pred["confidence"][field] < threshold for _, pred in none_rows), len(none_rows)),
        "e5_only_top1_accuracy": wilson(sum(is_correct(row, pred["e5"]) for row, pred in answers), len(answers)),
        "laya_top1_accuracy": wilson(sum(is_correct(row, pred["laya"]) for row, pred in answers), len(answers)),
        "laya_cos_accuracy": wilson(sum(is_correct(row, pred["laya_cos"]) for row, pred in answers), len(answers)),
        "reranking_gain_vs_e5_top1": round((sum(is_correct(row, pred["laya_cos"]) for row, pred in answers) - sum(is_correct(row, pred["e5"]) for row, pred in answers)) / len(answers), 4) if answers else None,
        "recall_at_1": wilson(sum(bool(set(row.get("acceptable", [])) & set(pred["pool"][:1])) for row, pred in answers), len(answers)),
        "recall_at_3": wilson(sum(bool(set(row.get("acceptable", [])) & set(pred["pool"][:3])) for row, pred in answers), len(answers)),
        "recall_at_5": wilson(sum(bool(set(row.get("acceptable", [])) & set(pred["pool"][:5])) for row, pred in answers), len(answers)),
        "gateway_section_recall": wilson(sum(bool({item.split(".")[0] for item in row.get("acceptable", [])} & set(pred["gate_sections"])) for row, pred in answers), len(answers)) if mode == "gateway" else wilson(0, 0),
        "order_robustness": wilson(sum(pred["shuffled_laya_cos"] == pred["laya_cos"] for row, pred in answers if pred["shuffled_laya_cos"] is not None), sum(pred["shuffled_laya_cos"] is not None for row, pred in answers)),
        "by_section": {key: group_metrics(group) for key, group in sorted(by_sections.items())},
        "by_scenario": {key: group_metrics(group) for key, group in sorted(by_scenarios.items())},
        "miss_categories": categorize_misses(rows, preds, mode),
    }


def rate_text(metric: dict) -> str:
    return "n/a" if metric["rate"] is None else f'{metric["rate"]:.1%} [{metric["lo"]:.1%}, {metric["hi"]:.1%}] (n={metric["n"]})'


def markdown_report(report: dict) -> str:
    lines = ["# Curation v2 retrieval benchmark", "", "- Same `test_blind` split is used for before and after.", "- Thresholds are fit independently on `dev_gate` for each corpus and prediction variant; `test_blind` is report-only.", "- The acceptance target is at most 3% wrong among answered and coverage above 36.5%.", "- Wilson intervals are 95% row-level intervals. One deterministic pass was run; they do not represent run-to-run variance.", "- LAPTOP latency is warm retrieval + Laya ONNX per test row. Query embedding and model/index startup are excluded.", "- Historical 1,790-row evaluation: legacy, not blind; it selects no configuration and contributes no threshold.", "- Phone RAM/latency: not measured, no adb device.", ""]
    for corpus_name, corpus in report["corpora"].items():
        lines.extend([f"## {corpus_name.title()} corpus", ""])
        for mode, mode_data in corpus["modes"].items():
            variant = mode_data["variants"]["laya_cos"]
            metrics = variant["test_blind"]
            fit = variant["dev_gate_fit"]
            lines.extend([f"### {mode.title()} reference pool", "", f"Threshold: `{metrics['threshold']}` (fit rows {fit['fit_rows']}, dev accepted {fit['accepted']}, dev wrong {fit['wrong']}).", ""])
            lines.extend(["| Measure | Result |", "|---|---:|"])
            for key, label in (("recall_at_1", "R@1"), ("recall_at_3", "R@3"), ("recall_at_5", "R@5"), ("gateway_section_recall", "Gateway section recall"), ("e5_only_top1_accuracy", "e5-only top-1"), ("laya_top1_accuracy", "Laya top-1"), ("laya_cos_accuracy", "e5 + Laya + cosine"), ("accepted_precision", "Accepted precision"), ("accepted_wrong_rate", "Wrong among answered (target ≤3%)"), ("coverage", "Coverage (target >36.5%)"), ("none_case_rejection_rate", "None-case rejection"), ("order_robustness", "Option-order robustness")):
                lines.append(f"| {label} | {rate_text(metrics[key])} |")
            lines.append(f"| Reranking gain vs e5 | {metrics['reranking_gain_vs_e5_top1']:+.1%} |" if metrics["reranking_gain_vs_e5_top1"] is not None else "| Reranking gain vs e5 | n/a |")
            lines.append(f"| False rejections | {metrics['false_rejections']} / {metrics['answerable_rows']} |")
            latency = mode_data["laptop_latency_ms"]
            lines.append(f"| LAPTOP p50 / p95 | {latency['p50']} / {latency['p95']} ms (n={latency['n']}) |")
            for axis in ("by_section", "by_scenario"):
                lines.extend(["", f"#### {axis.replace('_', ' ').title()}", "", "| Group | n answerable | R@1 | R@3 | R@5 | Selected accuracy | Accepted precision | Coverage |", "|---|---:|---:|---:|---:|---:|---:|---:|"])
                for name, group in metrics[axis].items():
                    lines.append(f"| {name} | {group['answerable']} | {rate_text(group['recall_at_1'])} | {rate_text(group['recall_at_3'])} | {rate_text(group['recall_at_5'])} | {rate_text(group['selected_accuracy'])} | {rate_text(group['accepted_precision'])} | {rate_text(group['coverage'])} |")
            lines.extend(["", "#### Miss categories", "", "Counts can overlap; exact affected `qid`s are listed in the JSON report.", "", "| Category | Count |", "|---|---:|"])
            for category, data in metrics["miss_categories"].items():
                lines.append(f"| {category} | {data['count']} |")
            if not metrics["miss_categories"]:
                lines.append("| None | 0 |")
            lines.append("")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--before", type=Path, required=True)
    parser.add_argument("--after", type=Path, required=True)
    parser.add_argument("--dev-gate", type=Path, required=True)
    parser.add_argument("--test-blind", type=Path, required=True)
    parser.add_argument("--laya-model", type=Path, default=MODEL_PATH)
    parser.add_argument("--tau-gate", type=float, default=-1.0)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    dev_rows, test_rows = read_rows(args.dev_gate), read_rows(args.test_blind)
    agent = load_agent(args.laya_model)
    order_sample = set(np.linspace(0, max(0, len(test_rows) - 1), min(200, len(test_rows)), dtype=int).tolist())
    output = {
        "evaluation": "sealed curation v2; test_blind report only",
        "thresholds": {"accept_wrong_rate_target": TARGET_WRONG_RATE, "coverage_target": TARGET_COVERAGE},
        "limits": ["Single deterministic pass; Wilson 95% intervals describe row-sampling uncertainty, not run-to-run variance.", "LAPTOP timings exclude query embedding and model/index startup; include retrieval plus Laya ONNX for each test row.", "Phone RAM/latency not measured; no adb device."],
        "test_blind_path": str(args.test_blind),
        "machine": {"logical_cpus": os.cpu_count(), "load_average_at_start": list(os.getloadavg()) if hasattr(os, "getloadavg") else None, "onnx_provider": "CPUExecutionProvider"},
        "corpora": {},
    }
    prepared = {}
    for label, directory in (("before", args.before), ("after", args.after)):
        retriever = Retriever(directory)
        vectors = retriever.embed([row["q"] for row in [*dev_rows, *test_rows]])
        dev_vectors, test_vectors = vectors[:len(dev_rows)], vectors[len(dev_rows):]
        output["corpora"][label] = {"sections_dir": str(directory), "modes": {}}
        prepared[label] = (retriever, dev_vectors, test_vectors)
    for mode in ("flat", "gateway"):
        for label in ("before", "after"):
            retriever, dev_vectors, test_vectors = prepared[label]
            dev_predictions, _ = predict(retriever, dev_rows, dev_vectors, mode, agent, tau_gate=args.tau_gate, order_sample=set())
            test_predictions, latency = predict(retriever, test_rows, test_vectors, mode, agent, tau_gate=args.tau_gate, order_sample=order_sample)
            per_variant = {}
            for field in ("e5", "laya", "laya_cos"):
                threshold, fit_metrics = fit_threshold(dev_rows, dev_predictions, field)
                per_variant[field] = {"dev_gate_fit": fit_metrics, "test_blind": metric_bundle(test_rows, test_predictions, field, threshold, mode)}
            output["corpora"][label]["modes"][mode] = {
                "threshold_parameters": {"k": 5, "tau_gate": args.tau_gate, "delta": 0.05, "max_sections": 5},
                "variants": per_variant,
                "laptop_latency_ms": {"label": "LAPTOP", "scope": "warm retrieval + Laya ONNX; query embeddings and startup excluded", "p50": round(float(np.percentile(latency, 50)), 2) if latency else None, "p95": round(float(np.percentile(latency, 95)), 2) if latency else None, "n": len(latency)},
            }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    args.out.with_suffix(".md").write_text(markdown_report(output))
    print(json.dumps({"output": str(args.out), "test_rows": len(test_rows), "corpora": list(output["corpora"])}, ensure_ascii=False))


if __name__ == "__main__":
    main()
