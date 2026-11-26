"""Build route/extract training examples from the real FSM driver.

Every example is a request the deployed driver actually builds (uniform JSON mode, guards
on, extractive answers), paired with the gold output. Dialogues are random scripts over
the phrasing pools; ``_TrainSim`` (the suite's gold simulator minus answer steps) yields the
gold step sequence, an oracle backend replays it through ``fsm.driver`` and records each
request. Dialogues where the driver diverges from the simulator are dropped, not patched.

Usage: uv run python -m nevados_bench.finetune.generate --n-dialogues 2500 --out data/finetune
"""

from __future__ import annotations

import argparse
import json
import random
import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

from nevados_bench.finetune import phrases as P
from nevados_bench.fsm import states as S
from nevados_bench.fsm.driver import run_dialogue
from nevados_bench.schemas import Completion, Dialogue, DialogueTurn, PromptRequest
from nevados_bench.suites import dialogues as DL
from nevados_bench.world import World, load_world

RV, RE = "register_visit", "report_emergency"
PLACEHOLDER_ARG = {"S": "station", "T": "trail_id", "D": "date", "V": "visitor_type",
                   "I": "item", "A": "target_altitude_m", "E": "emergency_type"}  # fmt: skip


# ----------------------------------------------------------------------------- surfaces


def _strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")


def _typo(rng: random.Random, text: str) -> str:
    words = text.split(" ")
    idx = [i for i, w in enumerate(words) if len(w) > 4 and w.isalpha()]
    for i in rng.sample(idx, min(len(idx), rng.randint(1, 2))):
        w = words[i]
        j = rng.randrange(1, len(w) - 1)
        words[i] = (
            w[:j] + w[j + 1] + w[j] + w[j + 2 :] if rng.random() < 0.5 else w[:j] + w[j + 1 :]
        )
    return " ".join(words)


def noisy(rng: random.Random, text: str) -> str:
    """Surface noise that never touches the gold: case, accents, typos, punctuation."""
    r = rng.random()
    if r < 0.12:
        text = _strip_accents(text)
    elif r < 0.20:
        text = text.lower()
    elif r < 0.27:
        text = _strip_accents(text.lower()).replace("¿", "").replace("¡", "")
    if rng.random() < 0.10:
        text = _typo(rng, text)
    return text


def _count(rng: random.Random, n: int) -> str:
    return rng.choice(P.COUNT_WORDS[n]) if n in P.COUNT_WORDS else str(n)


class Filler:
    """Fills placeholders with random surfaces and records their canonical values."""

    def __init__(self, rng: random.Random, world: World, english: bool = False):
        self.rng = rng
        self.world = world
        self.en = english

    def value(self, ph: str, fixed: Any = None) -> tuple[str, Any]:
        rng = self.rng
        if ph == "S":
            sid = fixed or rng.choice(list(P.STATION_FORMS))
            forms = P.STATION_FORMS_EN if self.en else P.STATION_FORMS
            return rng.choice(forms[sid]), sid
        if ph == "T":
            tid = fixed or rng.choice(list(P.TRAIL_FORMS))
            return rng.choice(P.TRAIL_FORMS[tid]), tid
        if ph == "D":
            pool = P.DATE_FORMS_EN if self.en else P.DATE_FORMS
            if fixed:
                hits = [f for f in pool if f[1] == fixed] or [(fixed, fixed)]
                return rng.choice(hits)
            return rng.choice(pool)
        if ph == "V":
            vid = fixed or rng.choice(list(P.VISITOR_FORMS))
            forms = P.VISITOR_FORMS_EN if self.en else P.VISITOR_FORMS
            return rng.choice(forms[vid]), vid
        if ph == "I":
            iid = fixed or rng.choice(list(P.ITEM_FORMS))
            forms = P.ITEM_FORMS_EN if self.en else P.ITEM_FORMS
            return rng.choice(forms[iid]), iid
        if ph == "A":
            a = fixed or rng.choice(P.ALTITUDES)
            num = f"{a:,}".replace(",", ".") if rng.random() < 0.5 else str(a)
            return rng.choice(P.ALTITUDE_FORMS).format(a=num), a
        if ph == "E":
            eid = fixed or rng.choice(list(P.EMERGENCY_FORMS))
            forms = P.EMERGENCY_FORMS_EN if self.en else P.EMERGENCY_FORMS
            return rng.choice(forms[eid]), eid
        if ph == "N":
            n = fixed or rng.choice([1, 2, 2, 3, 3, 4, 4, 5, 6, 8, 10, 12])
            return _count(rng, n), n
        raise KeyError(ph)

    def fill(self, template: str, fixed: dict[str, Any] | None = None) -> tuple[str, dict]:
        fixed = fixed or {}
        values: dict[str, Any] = {}

        def sub(m: re.Match[str]) -> str:
            ph = m.group(1)
            text, val = self.value(ph, fixed.get(ph))
            values[ph] = val
            return text

        text = re.sub(r"\{([STDVIAEN])\}", sub, template)
        return text[0].upper() + text[1:] if text else text, values


def placeholders(template: str) -> set[str]:
    return set(re.findall(r"\{([STDVIAEN])\}", template))


# ----------------------------------------------------------------------------- gold sim


class _TrainSim(DL._Sim):
    """The suite's gold simulator without answer steps (extractive answers need no model)."""

    def _answer(self, turn: Any, call: Any, phen: str) -> str:
        self.state = S.ANSWER
        return ""


def _info_args(tool: str, values: dict[str, Any]) -> dict[str, Any]:
    return {PLACEHOLDER_ARG[p]: v for p, v in values.items() if p in PLACEHOLDER_ARG}


def _missing(world: World, tool: str, args: dict[str, Any]) -> list[str]:
    return world.missing_required(tool, args)


# ----------------------------------------------------------------------------- scripts


class ScriptBuilder:
    def __init__(self, rng: random.Random, world: World):
        self.rng = rng
        self.world = world

    def info_ask(self, en: bool, tool: str | None = None, station: str | None = None,
                 complete: bool = True) -> DL.Ask | None:  # fmt: skip
        rng = self.rng
        tool = tool or rng.choice(list(P.INFO))
        es, en_t = P.INFO[tool]
        pool = en_t if en and en_t else es
        req = set(P.INFO_REQUIRED.get(tool, ("S",)))
        cands = [t for t in pool if req <= placeholders(t)] if complete else list(pool)
        if not cands:
            return None
        f = Filler(rng, self.world, en)
        text, values = f.fill(rng.choice(cands), {"S": station} if station else None)
        args = _info_args(tool, values)
        if _missing(self.world, tool, args):
            return None
        return DL.Ask(noisy(rng, text), tool, args, ())

    def _flow_text(self, tool: str, slots: dict[str, Any], en: bool) -> str:
        rng = self.rng
        f = Filler(rng, self.world, en)
        parts: dict[str, str] = {}
        if tool == RV:
            st = slots.get("station")
            parts["at"] = (
                (" " + rng.choice(("a", "en", "para")) + " " + f.value("S", st)[0]) if st else ""
            )
            d = slots.get("date")
            parts["on"] = (
                (" " + rng.choice(("para", "")) + " " + f.value("D", d)[0]).replace("  ", " ")
                if d
                else ""
            )
            g = slots.get("group_size")
            if g:
                word = f.value("N", g)[0]
                parts["group"] = rng.choice(
                    (
                        f" para {word} persona{'s' if g > 1 else ''}",
                        f", somos {word}" if g > 1 else ", voy yo solo",
                    )
                )
            else:
                parts["group"] = ""
            v = slots.get("visitor_type")
            parts["vis"] = (", somos " + f.value("V", v)[0]) if v else ""
            tpl = rng.choice(P.REGISTER_STARTS_EN if en else P.REGISTER_STARTS)
        else:
            e = slots.get("emergency_type")
            if e:
                clause = f.value("E", e)[0] if en else rng.choice(P.EMERGENCY_CLAUSES[e])
                parts["e"] = " " + clause
            else:
                parts["e"] = ""
            st = slots.get("station")
            parts["at"] = (
                (" " + rng.choice(("en", "cerca de")) + " " + f.value("S", st)[0]) if st else ""
            )
            n = slots.get("people_count")
            if n:
                word = f.value("N", n)[0]
                parts["people"] = "." + rng.choice(
                    (
                        f" Somos {word} afectados.",
                        f" Hay {word} personas afectadas." if n > 1 else " Hay una afectada.",
                        " Es una sola persona." if n == 1 else f" Son {word} personas.",
                    )
                )
            else:
                parts["people"] = "."
            tpl = rng.choice(P.EMERGENCY_STARTS_EN if en else P.EMERGENCY_STARTS)
        text = tpl.format(**parts)
        text = re.sub(r"\s+([,.])", r"\1", text).replace("..", ".").replace(":.", ".")
        return noisy(rng, text.strip())

    def _random_slots(self, tool: str, k: int) -> dict[str, Any]:
        rng = self.rng
        full: dict[str, Any] = {"station": rng.choice(list(P.STATION_FORMS))}
        if tool == RV:
            full |= {"date": rng.choice(P.DATE_FORMS)[1],
                     "group_size": rng.choice([1, 2, 3, 4, 5, 6, 8, 10, 12, 15]),
                     "visitor_type": rng.choice(list(P.VISITOR_FORMS))}  # fmt: skip
        else:
            full |= {"emergency_type": rng.choice(list(P.EMERGENCY_FORMS)),
                     "people_count": rng.choice([1, 1, 2, 3, 4])}  # fmt: skip
        keys = list(full)
        rng.shuffle(keys)
        return {kk: full[kk] for kk in S.REQUIRED_SLOTS[tool] if kk in keys[:k]}

    def _fill_turn(self, slot: str, value: Any, en: bool) -> DL.Fill:
        rng = self.rng
        f = Filler(rng, self.world, en)
        tpl = rng.choice(P.FILL[slot])
        if slot == "emergency_type" and rng.random() < 0.5:
            return DL.Fill(
                noisy(rng, rng.choice(P.EMERGENCY_CLAUSES[value]).capitalize() + "."), value
            )
        ph = {"station": "S", "date": "D", "group_size": "N", "visitor_type": "V",
              "emergency_type": "E", "people_count": "N"}[slot]  # fmt: skip
        text, _ = f.fill(tpl, {ph: value})
        return DL.Fill(noisy(rng, text), value)

    def _correct_turn(self, slot: str, value: Any) -> DL.Correct:
        rng = self.rng
        f = Filler(rng, self.world)
        ph = {"station": "S", "date": "D", "group_size": "N", "visitor_type": "V",
              "emergency_type": "E", "people_count": "N"}[slot]  # fmt: skip
        text, _ = f.fill(rng.choice(P.CORRECTIONS[slot]), {ph: value})
        return DL.Correct(noisy(rng, text), {slot: value})

    def _other(self, slot: str, current: Any) -> Any:
        rng = self.rng
        pools = {"station": list(P.STATION_FORMS), "date": [d for _, d in P.DATE_FORMS],
                 "group_size": [2, 3, 4, 5, 6, 7, 9, 10], "visitor_type": list(P.VISITOR_FORMS),
                 "emergency_type": list(P.EMERGENCY_FORMS),
                 "people_count": [1, 2, 3, 4]}  # fmt: skip
        return rng.choice([v for v in pools[slot] if v != current])

    def flow_script(self, en: bool) -> list[Any]:
        rng = self.rng
        tool = rng.choice((RV, RV, RE))
        slots = self._random_slots(tool, rng.choice((0, 1, 1, 2, 2, 3, 4)))
        turns: list[Any] = []
        if rng.random() < 0.3:
            ask = self.info_ask(en)
            if ask:
                turns.append(ask)
        turns.append(DL.Start(self._flow_text(tool, slots, en), tool, dict(slots)))
        state = dict(slots)
        switched = cancelled = corrected = False
        while True:
            pending = next((s for s in S.REQUIRED_SLOTS[tool] if s not in state), None)
            if pending is None:
                break
            r = rng.random()
            if not switched and r < 0.10:
                ask = self.info_ask(False)
                if ask:
                    turns.append(DL.Ask(ask.message, ask.tool, ask.args, (), "intent_switch"))
                    resume = rng.choice(("Bueno, sigamos con el registro.",
                                         "Ok, continuemos con el trámite.",
                                         "Listo, volvamos a lo de antes."))  # fmt: skip
                    turns.append(DL.Start(resume, tool, dict(state), "intent_switch"))
                    switched = True
                    continue
            if not corrected and state and r < 0.25:
                slot = rng.choice(list(state))
                state[slot] = self._other(slot, state[slot])
                turns.append(self._correct_turn(slot, state[slot]))
                corrected = True
                continue
            full = self._random_slots(tool, 9)
            value = full.get(pending) if pending in full else self._other(pending, None)
            turns.append(self._fill_turn(pending, value, en))
            state[pending] = value
        if not cancelled and rng.random() < 0.12:
            turns.append(DL.Cancel(rng.choice(P.CANCELS)))
            turns.append(DL.Start(rng.choice(P.RESUMES), tool, dict(state), "cancel_resume"))
        elif not corrected and rng.random() < 0.15:
            slot = rng.choice(list(state))
            state[slot] = self._other(slot, state[slot])
            turns.append(self._correct_turn(slot, state[slot]))
        turns.append(DL.Confirm(rng.choice(P.CONFIRMS)))
        if rng.random() < 0.3:
            st = state.get("station")
            tool2 = rng.choice(list(P.FOLLOW_STATION))
            turns.append(DL.Ask(noisy(rng, rng.choice(P.FOLLOW_STATION[tool2])), tool2,
                                {"station": st}, (), "ellipsis"))  # fmt: skip
        return turns

    def info_script(self, en: bool) -> list[Any]:
        rng = self.rng
        first = self.info_ask(
            en, tool=rng.choice([t for t in P.INFO if "S" in P.INFO_REQUIRED.get(t, ("S",))])
        )
        if first is None:
            return []
        turns: list[Any] = [first]
        station = first.args.get("station")
        tool = first.tool
        for _ in range(rng.choice((1, 2, 3))):
            r = rng.random()
            if station and r < 0.4:
                tool2 = rng.choice(list(P.FOLLOW_STATION))
                turns.append(DL.Ask(noisy(rng, rng.choice(P.FOLLOW_STATION[tool2])), tool2,
                                    {"station": station}, (), "ellipsis"))  # fmt: skip
                tool = tool2
            elif (
                station
                and r < 0.65
                and set(self.world.tools[tool].parameters["required"]) == {"station"}
            ):
                other = rng.choice([s for s in P.STATION_FORMS if s != station])
                f = Filler(rng, self.world)
                text, _ = f.fill(rng.choice(P.FOLLOW_OTHER_STATION), {"S": other})
                turns.append(DL.Ask(noisy(rng, text), tool, {"station": other}, (), "ellipsis"))
                station = other
            else:
                ask = self.info_ask(en)
                if ask:
                    turns.append(ask)
                    station = ask.args.get("station", station)
                    tool = ask.tool
        return turns


# ----------------------------------------------------------------------------- capture


def route_target(name: str, args: dict[str, Any] | None = None) -> str:
    if name in ("none",):
        return json.dumps({"tool": "none"}, ensure_ascii=False)
    return json.dumps({"tool": name, "args": args or {}}, ensure_ascii=False)


def clarify_target(question: str) -> str:
    return json.dumps({"tool": "clarify", "question": question}, ensure_ascii=False)


class Recorder:
    """Oracle backend: returns queued outputs and records each request."""

    def __init__(self, outputs: list[tuple[str, str]]):
        self.outputs = list(outputs)  # (call_type, target text)
        self.examples: list[dict[str, Any]] = []
        self.desync = False

    def complete(self, request: PromptRequest) -> Completion:
        kind = "extract" if "Tu tarea es extraer" in request.messages[0]["content"] else "route"
        if not self.outputs or self.outputs[0][0] != kind:
            self.desync = True
            return Completion(content='{"tool": "none"}' if kind == "route" else '{"value": null}')
        _, target = self.outputs.pop(0)
        self.examples.append({"call_type": kind, "messages": request.messages, "target": target})
        return Completion(content=target)


def _target_for(step: Any) -> tuple[str, str]:
    if step.call_type == "extract":
        return "extract", json.dumps({"value": step.gold.slot_value}, ensure_ascii=False)
    call = step.gold.calls[0]
    return "route", route_target(call.name, call.arguments)


def replay(world: World, dialogue: Dialogue, expected: list) -> list[dict[str, Any]] | None:
    outputs = [_target_for(s) for t in dialogue.turns for s in t.steps
               if s.call_type in ("route", "extract")]  # fmt: skip
    rec = Recorder(outputs)
    steps = run_dialogue(dialogue, rec, world, "uniform", guards=True, answer_mode="extractive")
    executed = [s.executed_call for s in steps if s.executed_call is not None
                and world.tools[s.executed_call.name].has_side_effects]  # fmt: skip
    if rec.desync or rec.outputs or executed != expected:
        return None
    return rec.examples


def single_turn(world: World, rng: random.Random, sb: ScriptBuilder) -> list[dict[str, Any]]:
    """One-message dialogues: info calls, clarifications, abstentions, injections."""
    r = rng.random()
    en = rng.random() < 0.15
    if r < 0.45:  # info call (sometimes with an injection tail)
        ask = sb.info_ask(en)
        if ask is None:
            return []
        msg = ask.message + (rng.choice(P.INJECTION_TAILS) if rng.random() < 0.12 else "")
        target = route_target(ask.tool, ask.args)
    elif r < 0.70:  # info call missing a required slot -> clarify
        tool = rng.choice(list(P.INFO))
        es, en_t = P.INFO[tool]
        pool = en_t if en and en_t else es
        req = set(P.INFO_REQUIRED.get(tool, ("S",)))
        cands = [t for t in pool if not req <= placeholders(t)]
        if not cands:
            return []
        text, values = Filler(rng, world, en).fill(rng.choice(cands))
        args = _info_args(tool, values)
        missing = _missing(world, tool, args)
        if not missing:
            return []
        msg = noisy(rng, text)
        target = clarify_target(S.SLOT_QUESTIONS[missing[0]])
    elif r < 0.88:  # out of scope
        msg = noisy(rng, rng.choice(P.OUT_OF_SCOPE))
        target = route_target("none")
    else:  # bare injection
        msg = rng.choice(P.INJECTION_ONLY)
        target = route_target("none")
    rec = Recorder([("route", target)])
    dialogue = Dialogue(dialogue_id="single", depth=1, phenomena=[],
                        turns=[DialogueTurn(user_message=msg, steps=[])])  # fmt: skip
    run_dialogue(dialogue, rec, world, "uniform", guards=True, answer_mode="extractive")
    return rec.examples if not rec.desync else []


def suite_texts() -> set[str]:
    texts: set[str] = set()
    for path in Path("data/suites").glob("*.jsonl"):
        for line in path.read_text().splitlines():
            rec = json.loads(line)
            if "user_message" in rec:
                texts.add(_norm(rec["user_message"]))
            for turn in rec.get("turns", []):
                texts.add(_norm(turn["user_message"]))
    return texts


def _norm(text: str) -> str:
    return re.sub(r"\W+", " ", _strip_accents(text.lower())).strip()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-dialogues", type=int, default=2500)
    ap.add_argument("--n-single", type=int, default=2500)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", type=Path, default=Path("data/finetune/examples.jsonl"))
    args = ap.parse_args()
    world = load_world()
    rng = random.Random(args.seed)
    sb = ScriptBuilder(rng, world)
    banned = suite_texts()
    examples: list[dict[str, Any]] = []
    stats: Counter[str] = Counter()
    for i in range(args.n_dialogues):
        en = rng.random() < 0.1
        script = sb.flow_script(en) if rng.random() < 0.6 else sb.info_script(en)
        if not script:
            continue
        try:
            trace = _TrainSim(world, f"t{i:05d}", tuple(script)).run()
        except (ValueError, AssertionError, KeyError):
            stats["sim_error"] += 1
            continue
        got = replay(world, trace.dialogue, trace.executions)
        if got is None:
            stats["desync"] += 1
            continue
        stats["dialogues"] += 1
        for ex in got:
            ex["source"] = "dialogue"
            ex["dialogue_id"] = f"t{i:05d}"
        examples += got
    for _ in range(args.n_single):
        got = single_turn(world, rng, sb)
        for ex in got:
            ex["source"] = "single"
        examples += got
    kept = []
    for ex in examples:
        user = ex["messages"][-1]["content"].rsplit("[Mensaje del usuario]\n", 1)[-1]
        if _norm(user) in banned:
            stats["dropped_suite_collision"] += 1
            continue
        kept.append(ex)
    stats["examples"] = len(kept)
    stats.update(f"type:{ex['call_type']}" for ex in kept)
    stats.update(f"target:{json.loads(ex['target']).get('tool', 'value')}" for ex in kept)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as fh:
        for ex in kept:
            fh.write(json.dumps(ex, ensure_ascii=False) + "\n")
    for k, v in sorted(stats.items()):
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
