"""Contrastive fine-tune of multilingual-e5-base so visitor messages land next to their entry.

Each step samples B distinct entries and two texts of each (label, examples, augmented queries),
then applies symmetric InfoNCE: the other text of the same entry is the positive, every other
entry in the batch a negative. Distinct entries per batch means no in-batch false negatives.
The 250k-token word-embedding matrix is frozen (192M of the 278M parameters): it keeps the model
inside a 4 GB GPU and protects the vocabulary the corpus never shows.

usage: python finetune.py --out work/models/ft1 [--holdout 2] [--aug work/aug] [--steps 3000]
"""

from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer

from kb import ROOT, app_texts, clean, load_entries

BASE = "intfloat/multilingual-e5-base"
PREFIX = "query: "



def mean_pool(h: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    m = mask.unsqueeze(-1).to(h.dtype)
    return (h * m).sum(1) / m.sum(1).clamp(min=1e-6)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--holdout", type=int, default=2, help="last N examples per entry kept out (pseudo-dev)")
    ap.add_argument("--no-conv", action="store_true", help="leave the 2-turn conversations out")
    ap.add_argument("--hubs", action="store_true")
    ap.add_argument("--strip", action="store_true", help="train on kb.clean() texts (as the index embeds them)")
    ap.add_argument("--exclude", type=Path, help="jsonl of texts never to train on (blind eval turns)")
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-5)
    ap.add_argument("--temp", type=float, default=0.05)
    ap.add_argument("--max-len", type=int, default=64)
    ap.add_argument("--seed", type=int, default=13)
    a = ap.parse_args()

    random.seed(a.seed)
    torch.manual_seed(a.seed)
    entries = load_entries(hubs=a.hubs)
    aug = app_texts(conv=not a.no_conv)
    banned: set[str] = set()
    if a.exclude and a.exclude.exists():
        for line in a.exclude.read_text().splitlines():
            if line.strip():
                banned.update(t.strip().lower() for t in json.loads(line)["turns"])
    pools = []
    for e in entries:
        ex = e.examples[: len(e.examples) - a.holdout] if a.holdout else e.examples
        pool = [t for t in [e.label, *ex, *aug.get(e.id, [])] if t.strip().lower() not in banned]
        if a.strip:
            pool = list(dict.fromkeys(clean(t) for t in pool))
        pools.append(pool)
    n_texts = sum(map(len, pools))
    print(f"entries={len(entries)} texts={n_texts} aug_entries={len(aug)} banned={len(banned)}", flush=True)

    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(BASE)
    model = AutoModel.from_pretrained(BASE).to(dev)
    model.embeddings.word_embeddings.weight.requires_grad_(False)
    model.gradient_checkpointing_enable()
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=a.lr, weight_decay=0.01)
    warm = max(1, a.steps // 10)
    # Linear warmup over the first 10 % of steps, then linear decay to 0.
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: (s + 1) / warm if s < warm else max(0.0, (a.steps - s) / max(1, a.steps - warm)))
    scaler = torch.amp.GradScaler(enabled=dev.type == "cuda")

    def enc(texts: list[str]) -> torch.Tensor:
        b = tok([PREFIX + t for t in texts], padding=True, truncation=True, max_length=a.max_len, return_tensors="pt").to(dev)
        with torch.autocast(dev.type, dtype=torch.float16, enabled=dev.type == "cuda"):
            h = model(**b).last_hidden_state
        return F.normalize(mean_pool(h.float(), b["attention_mask"]), dim=-1)

    usable = [i for i, p in enumerate(pools) if len(p) >= 2]
    model.train()
    t0 = time.time()
    for step in range(a.steps):
        ids = random.sample(usable, a.batch)
        pairs = [random.sample(pools[i], 2) for i in ids]
        qa = enc([p[0] for p in pairs])
        qb = enc([p[1] for p in pairs])
        logits = qa @ qb.T / a.temp
        target = torch.arange(len(ids), device=dev)
        loss = (F.cross_entropy(logits, target) + F.cross_entropy(logits.T, target)) / 2
        opt.zero_grad(set_to_none=True)
        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        scaler.step(opt)
        scaler.update()
        sched.step()
        if step % 200 == 0 or step == a.steps - 1:
            print(f"step {step} loss {loss.item():.4f} lr {sched.get_last_lr()[0]:.2e} {time.time() - t0:.0f}s", flush=True)

    a.out.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(a.out)
    tok.save_pretrained(a.out)
    (a.out / "train_args.json").write_text(json.dumps({k: str(v) for k, v in vars(a).items()}, indent=1))
    print("saved", a.out, flush=True)


if __name__ == "__main__":
    main()
