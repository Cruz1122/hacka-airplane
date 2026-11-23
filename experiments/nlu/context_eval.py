"""Follow-up gating: when should the previous turn's entry scores be fused into the new message's?

Two populations, both from the blind set:
  followup  multi-turn rows: the last turn needs the earlier ones;
  switch    single-turn rows preceded by an unrelated earlier turn (another row's first turn):
            fusing must not drag the answer back to the old topic.
A gate that helps the first and hurts the second is useless in the chat, where every message after
the first has a previous turn.

usage: python context_eval.py [--model M] [--split dev] [--mode top3]
"""

from __future__ import annotations

import argparse
import random

import numpy as np

from evaluate import Index, load_blind
from kb import Embedder, app_texts, load_entries


def correct(pid: str | None, acceptable: list[str]) -> bool:
    return (pid in acceptable) if acceptable else pid is None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="intfloat/multilingual-e5-base")
    ap.add_argument("--split", default="dev")
    ap.add_argument("--mode", default="top3")
    ap.add_argument("--hubs", action="store_true")
    ap.add_argument("--strip", action="store_true", help="strip chat fillers (kb.clean) before embedding")
    a = ap.parse_args()

    blind = load_blind()
    rows = [r for r in blind if r["split"] == a.split]
    banned = {t.strip().lower() for r in blind for t in r["turns"]}
    entries = load_entries(hubs=a.hubs)
    emb = Embedder(a.model, strip_fillers=a.strip)
    idx = Index(emb, entries, app_texts(conv=True), banned)

    multi = [r for r in rows if len(r["turns"]) > 1]
    single = [r for r in rows if len(r["turns"]) == 1]
    rnd = random.Random(7)
    firsts = [r["turns"][0] for r in rows if len(r["turns"]) > 1] + [r["turns"][0] for r in single]
    switch = []
    for r in single:
        prev = rnd.choice([f for f in firsts if f != r["turns"][0]])
        switch.append({**r, "turns": [prev, r["turns"][0]]})

    def scores(group):
        last = idx.scores(emb.encode([r["turns"][-1] for r in group]), a.mode)
        prev = idx.scores(emb.encode([" ".join(r["turns"][:-1]) for r in group]), a.mode)
        return last, prev

    pops = {"followup": (multi, *scores(multi)), "switch": (switch, *scores(switch))}
    nwords = lambda t: len(t.split())  # noqa: E731

    def run(gate, w: float, T: float) -> dict[str, float]:
        out = {}
        for name, (group, sl, sp) in pops.items():
            ok = 0
            for r, l, p in zip(group, sl, sp):
                s = (l + w * p) / (1 + w) if gate(r, l, p) else l
                top = int(s.argmax())
                pid = idx.entries[top].id if s[top] >= T else None
                ok += correct(pid, r["acceptable"])
            out[name] = ok / len(group)
        return out

    gates = {
        "never": lambda r, l, p: False,
        "always": lambda r, l, p: True,
        **{f"words<={n}": (lambda n: lambda r, l, p: nwords(r["turns"][-1]) <= n)(n) for n in (3, 4, 5, 6)},
        **{f"top<{t}": (lambda t: lambda r, l, p: l.max() < t)(t) for t in (0.88, 0.9, 0.92)},
        "words<=5|top<0.9": lambda r, l, p: nwords(r["turns"][-1]) <= 5 or l.max() < 0.9,
    }
    print(f"followup n={len(multi)} switch n={len(switch)} mode={a.mode}")
    for T in (0.0, 0.8, 0.85):
        for name, g in gates.items():
            for w in (0.3, 0.5, 0.8):
                if name == "never" and w != 0.3:
                    continue
                res = run(g, w, T)
                # Weight the populations as the chat sees them: most messages are new questions.
                blend = 0.3 * res["followup"] + 0.7 * res["switch"]
                print(f"T={T:.2f} {name:10s} w={w:.1f} followup={res['followup']:.3f} "
                      f"switch={res['switch']:.3f} blend={blend:.3f}")


if __name__ == "__main__":
    main()
