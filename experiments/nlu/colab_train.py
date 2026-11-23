"""Self-contained Colab job: contrastive fine-tune of multilingual-e5 + blind-set evaluation.

Pasted into a Colab cell (the colab MCP has no file upload). Reads /content/payload.json
({"pools": [{id, texts}], "blind": [{qid, turns, style, acceptable, split}]}), built locally from
kb.load_entries(hubs=True) + kb.app_texts(conv=True) with every blind turn removed, so training and
the evaluation index never see a blind query. Same recipe as finetune.py; scoring as evaluate.py
(entry = mean of its best 3 row cosines; follow-ups fuse the previous turns' scores with w).

run(out, base, steps, batch, lr, temp) -> trains, saves, returns dev accuracy by style.
"""

import json
import random
import time
from collections import defaultdict

import numpy as np
import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer

PREFIX = "query: "
# T4 has no fast bf16: fp16 autocast + loss scaling there, bf16 on L4/A100.
DT = torch.bfloat16 if torch.cuda.is_bf16_supported() and torch.cuda.get_device_capability()[0] >= 8 else torch.float16
P = json.load(open("/content/payload.json"))
POOLS, BLIND = P["pools"], P["blind"]


def mean_pool(h, mask):
    m = mask.unsqueeze(-1).to(h.dtype)
    return (h * m).sum(1) / m.sum(1).clamp(min=1e-6)


def train(out, base="intfloat/multilingual-e5-base", steps=3000, batch=128, lr=3e-5, temp=0.05,
          max_len=64, seed=13, freeze_emb=True):
    random.seed(seed)
    torch.manual_seed(seed)
    tok = AutoTokenizer.from_pretrained(base)
    model = AutoModel.from_pretrained(base).cuda()
    if freeze_emb:
        model.embeddings.word_embeddings.weight.requires_grad_(False)
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.01)
    warm = max(1, steps // 10)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: (s + 1) / warm if s < warm else max(0.0, (steps - s) / max(1, steps - warm)))
    scaler = torch.amp.GradScaler(enabled=DT == torch.float16)
    pools = [p["texts"] for p in POOLS]
    usable = [i for i, p in enumerate(pools) if len(p) >= 2]

    def enc(texts):
        b = tok([PREFIX + t for t in texts], padding=True, truncation=True, max_length=max_len,
                return_tensors="pt").to("cuda")
        with torch.autocast("cuda", dtype=DT):
            h = model(**b).last_hidden_state
        return F.normalize(mean_pool(h.float(), b["attention_mask"]), dim=-1)

    model.train()
    t0 = time.time()
    for step in range(steps):
        ids = random.sample(usable, batch)
        pairs = [random.sample(pools[i], 2) for i in ids]
        qa, qb = enc([p[0] for p in pairs]), enc([p[1] for p in pairs])
        logits = qa @ qb.T / temp
        target = torch.arange(len(ids), device="cuda")
        loss = (F.cross_entropy(logits, target) + F.cross_entropy(logits.T, target)) / 2
        opt.zero_grad(set_to_none=True)
        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        scaler.step(opt)
        scaler.update()
        sched.step()
        if step % 500 == 0 or step == steps - 1:
            print(f"step {step} loss {loss.item():.4f} {time.time() - t0:.0f}s", flush=True)
    model.save_pretrained(out)
    tok.save_pretrained(out)
    return model, tok


@torch.no_grad()
def embed(model, tok, texts, bs=256, max_len=128):
    model.eval()
    out = []
    for i in range(0, len(texts), bs):
        b = tok([PREFIX + t for t in texts[i:i + bs]], padding=True, truncation=True, max_length=max_len,
                return_tensors="pt").to("cuda")
        with torch.autocast("cuda", dtype=DT):
            h = model(**b).last_hidden_state
        out.append(F.normalize(mean_pool(h.float(), b["attention_mask"]), dim=-1).cpu().numpy())
    return np.concatenate(out).astype(np.float32)


def evaluate(model, tok, split="dev", k=3, w=0.5, gate_words=None):
    texts, owner = [], []
    for n, p in enumerate(POOLS):
        texts += p["texts"]
        owner += [n] * len(p["texts"])
    owner = np.asarray(owner)
    V = embed(model, tok, texts)
    groups = [np.flatnonzero(owner == n) for n in range(len(POOLS))]
    rows = [r for r in BLIND if split == "all" or r["split"] == split]

    def scores(qs):
        sim = embed(model, tok, qs) @ V.T
        S = np.full((len(qs), len(POOLS)), -1.0, dtype=np.float32)
        for n, g in enumerate(groups):
            S[:, n] = np.sort(sim[:, g], 1)[:, ::-1][:, :k].mean(1)
        return S

    last = scores([r["turns"][-1] for r in rows])
    prev = scores([" ".join(r["turns"][:-1]) or r["turns"][-1] for r in rows])
    multi = np.array([len(r["turns"]) > 1 for r in rows])
    S = last.copy()
    S[multi] = (last[multi] + w * prev[multi]) / (1 + w)
    res = {}
    for T in np.arange(0.0, 0.96, 0.01):
        by = defaultdict(lambda: [0, 0])
        for r, s in zip(rows, S):
            t = int(s.argmax())
            pid = POOLS[t]["id"] if s[t] >= T else None
            acc = r["acceptable"]
            ok = (pid in acc) if acc else pid is None
            by[r["style"]][0] += ok
            by[r["style"]][1] += 1
        tot = sum(v[0] for v in by.values()) / sum(v[1] for v in by.values())
        if not res or tot > res["acc"]:
            res = {"acc": round(tot, 4), "T": round(float(T), 2),
                   "by_style": {s: round(v[0] / v[1], 3) for s, v in sorted(by.items())}}
    return res, (rows, S)


def run(out, **kw):
    model, tok = train(out, **kw)
    res, _ = evaluate(model, tok)
    print(out, kw, res, flush=True)
    return model, tok, res
