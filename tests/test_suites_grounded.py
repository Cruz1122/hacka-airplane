import re
from collections import Counter, defaultdict

import pytest

from nevados_bench.fsm import prompts
from nevados_bench.schemas import CONTEXT_LEVEL_TOKENS
from nevados_bench.suites import grounded as G
from nevados_bench.values import contains_named_value, extract_values, normalize_text
from nevados_bench.world import load_world

# Achievable tolerance of the prompt-size estimate around the level target: the assembler
# reserves 80 suffix tokens and overshoots by at most one filler passage.
TOKEN_TOLERANCE = 100


@pytest.fixture(scope="module")
def world():
    return load_world()


@pytest.fixture(scope="module")
def cases(world):
    return G.generate_grounded_qa(world)


def _recoverable(text: str, value: str) -> bool:
    if re.fullmatch(r"\d+|\d{2}:\d{2}", value):
        return value in extract_values(text)
    return contains_named_value(text, value)


def test_question_composition(world):
    qs = G.QUESTIONS
    assert len(qs) == 96
    assert len({q.qid for q in qs}) == 96
    assert sum(q.answerable for q in qs) == 60
    safety = [q for q in qs if G.is_safety(world, q)]
    assert len(safety) == 24
    assert any(q.answerable for q in safety) and any(not q.answerable for q in safety)
    assert {q.qtype for q in qs} == set(G.QUESTION_TYPES)
    english = sum(q.lang == "en" for q in qs)
    assert 8 <= english <= 12
    assert sum(q.lang == "es" for q in qs) >= 80
    strata = Counter(s for q in qs for s in q.strata)
    assert strata["colloquial"] >= 3 and strata["typos"] >= 2
    kinds = Counter(q.kind for q in qs if not q.answerable)
    assert kinds["lure"] >= 20 and kinds["nowhere"] >= 5
    # Counterfactual passages are exercised by safety-critical questions.
    cf_safety = [q for q in safety if q.ref and world.passages[q.ref].prior_values]
    assert len(cf_safety) >= 12


def test_gold_values_recoverable_from_gold_passage(world):
    for q in G.QUESTIONS:
        if q.answerable:
            assert q.values, q.qid
            text = world.passages[q.gold].text
            for value in q.values:
                assert value in world.passages[q.gold].values, (q.qid, value)
                assert _recoverable(text, value), (q.qid, value)
        else:
            assert not q.values, q.qid
            assert G.lure_candidates(world, q), q.qid


def test_case_counts(cases):
    by_level = Counter(c.context_level for c in cases if not c.tags["injection"])
    assert by_level[None] == 96
    for level in ("2k", "4k", "8k"):
        assert by_level[level] == 96
    assert by_level["1k"] >= 70
    assert by_level["0.5k"] >= 20
    assert sum(c.tags["injection"] for c in cases) == 12
    # Each question at most once per level (injection cases aside).
    seen = Counter(
        (c.tags["base_question_id"], c.context_level) for c in cases if not c.tags["injection"]
    )
    assert max(seen.values()) == 1


def test_case_ids_unique_and_stable(world, cases):
    ids = [c.case_id for c in cases]
    assert len(ids) == len(set(ids))
    assert "gqa-q012-4k" in ids and "gqa-q012-closed" in ids
    assert [c.model_dump() for c in G.generate_grounded_qa(world)] == [
        c.model_dump() for c in cases
    ]


def test_case_fields_and_tags(cases):
    required = {
        "gold_position", "distractors_n", "question_type", "safety", "counterfactual",
        "base_question_id", "closed_book", "injection",
    }  # fmt: skip
    for c in cases:
        assert c.suite == "grounded_qa" and c.call_type == "answer" and c.fsm_state == "ANSWER"
        assert required <= set(c.tags), c.case_id
        assert c.tags["gold_position"] in {"start", "middle", "end", "absent"}


def test_answerable_cases_contain_gold(world, cases):
    for c in cases:
        if c.gold.answerable:
            assert c.gold.gold_passage_id in c.passage_ids, c.case_id
            assert c.tags["gold_position"] != "absent"
            for value in c.gold.gold_values:
                assert value in world.passages[c.gold.gold_passage_id].values


def test_unanswerable_cases_lack_gold_and_contain_lure(world, cases):
    by_id = {q.qid: q for q in G.QUESTIONS}
    for c in cases:
        q = by_id[c.tags["base_question_id"]]
        if c.tags["closed_book"]:
            assert c.passage_ids == [] and c.bundle_id == "closed" and c.context_level is None
            assert c.gold.answerable is False
            assert c.gold.gold_values == list(q.values)
            continue
        if q.answerable:
            continue
        assert c.gold.answerable is False
        assert c.tags["gold_position"] == "absent"
        if q.absent:
            assert q.absent not in c.passage_ids, c.case_id
        lures = [p for p in c.passage_ids if p in G.lure_candidates(world, q)]
        assert lures, c.case_id
        assert c.gold.lure_values, c.case_id
        assert set(c.gold.lure_values) <= {v for p in lures for v in world.passages[p].values}


def test_prior_values_exercised(world, cases):
    with_priors = [c for c in cases if c.gold.prior_values]
    assert sum(c.tags["safety"] for c in with_priors) >= 40
    for c in with_priors:
        assert c.tags["counterfactual"]
        assert c.gold.prior_values == world.passages[c.gold.gold_passage_id].prior_values


def test_gold_positions_cover_every_level(cases):
    positions = defaultdict(set)
    for c in cases:
        if c.gold.answerable:
            positions[c.context_level].add(c.tags["gold_position"])
    for level in G.LEVELS:
        assert positions[level] == {"start", "middle", "end"}, level


def test_bundles_are_three_per_level_and_consistent(cases):
    bundles = defaultdict(list)
    for c in cases:
        if c.context_level and not c.tags["injection"]:
            bundles[c.bundle_id].append(c)
    per_level = Counter(group[0].context_level for group in bundles.values())
    assert per_level == {level: 3 for level in G.LEVELS}
    for group in bundles.values():
        assert len({tuple(c.passage_ids) for c in group}) == 1
        assert len({c.context_level for c in group}) == 1
        assert not any(world_pid.startswith("INJ-") for world_pid in group[0].passage_ids)


def test_bundle_prefix_identity(world, cases):
    groups = defaultdict(list)
    for c in cases:
        groups[c.bundle_id].append(c)
    for bundle_id, group in groups.items():
        systems = {prompts.build_request(c, world, "native").messages[0]["content"] for c in group}
        assert len(systems) == 1, bundle_id


def test_token_estimates_within_level_target(world, cases):
    seen = set()
    for c in cases:
        if c.context_level is None or c.bundle_id in seen:
            continue
        seen.add(c.bundle_id)
        tokens = prompts.estimate_request_tokens(prompts.build_request(c, world, "native"))
        target = CONTEXT_LEVEL_TOKENS[c.context_level]
        assert abs(tokens - target) <= TOKEN_TOLERANCE, (c.bundle_id, tokens)


def test_build_request_works_for_every_case(world, cases):
    for c in cases:
        request = prompts.build_request(c, world, "uniform")
        assert request.messages[-1]["content"] == c.user_message


def test_distractor_tags(world, cases):
    for c in cases:
        if c.tags["closed_book"]:
            assert c.tags["distractors_n"] == 0
    assert max(c.tags["distractors_n"] for c in cases) >= 3


def test_injection_cases(world, cases):
    inj = [c for c in cases if c.tags["injection"]]
    assert len(inj) == 12
    corpus = [p for p in world.passages.values() if not p.id.startswith("INJ-")]
    for c in inj:
        marker = c.tags["injection_marker"]
        injected = [p for p in c.passage_ids if p.startswith("INJ-")]
        assert len(injected) == 1
        assert contains_named_value(world.passages[injected[0]].text, marker)
        assert not any(contains_named_value(p.text, marker) for p in corpus)
        assert "injection" in c.strata and c.gold.answerable
    markers = {normalize_text(c.tags["injection_marker"]) for c in inj}
    assert len(markers) == 6


def test_priority_safety_first_and_levels_round_robin(cases):
    ordered = sorted(cases, key=lambda c: c.priority)
    n_safety = sum(c.tags["safety"] for c in cases)
    assert all(c.tags["safety"] for c in ordered[:n_safety])
    head = ordered[: n_safety + 12]
    assert {c.context_level for c in head} >= set(G.LEVELS)
    assert {c.context_level for c in ordered[:6]} >= set(G.LEVELS)
