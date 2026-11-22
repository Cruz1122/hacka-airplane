import numpy as np
from retrieval import Retriever
from bench_v2 import is_correct
from splits_v2 import SEED, filter_verified, split

def test_gateway_opens_sections_within_delta_and_limits_five(tmp_path):
    import json
    for i in range(7):
        data={"id":f"s{i}","description":f"desc{i}","retrieval":{"top_k":2},"entries":[{"id":f"s{i}.e","label":f"label{i}","examples":[f"example{i}"]}]}
        (tmp_path/f"s{i}.json").write_text(json.dumps(data))
    # The fixture controls each section's description vector and provides identical FAQ vectors.
    def embed(texts,**kwargs):
        out=[]
        for t in texts:
            n=int(t[-1]);score=1.0-.02*n;out.append(np.array([score,(1-score**2)**.5],np.float32))
        return np.stack(out)
    r=Retriever(tmp_path,embedder=embed);result=r.retrieve(np.array([1.,0.]),mode="gateway",k=5)
    assert [s for s,_ in result["gates"]]==["s0","s1","s2"]
    assert len(result["candidates"])==3

def test_acceptability_scoring_accepts_any_valid_faq_id():
    row={"acceptable":["fauna.birds","fauna.mammals"]}
    assert is_correct(row,"fauna.mammals")
    assert not is_correct(row,"fauna.fish")


def test_split_filters_dropped_and_leaked_rows_before_family_assignment(tmp_path):
    source = tmp_path / "verified.jsonl"
    rows = [
        (source, {"qid": "kept-1", "family": "f1", "label_status": "verified"}),
        (source, {"qid": "leaked", "family": "f2", "label_status": "verified"}),
        (source, {"qid": "dropped", "family": "f3", "label_status": "dropped"}),
        (source, {"qid": "kept-2", "family": "f4", "label_status": "verified"}),
    ]
    eligible, dropped, leaked = filter_verified(rows, {"leaked"})
    dev, test = split(eligible, 0.5, SEED)
    assert [row[1]["qid"] for row in dropped] == ["dropped"]
    assert [row[1]["qid"] for row in leaked] == ["leaked"]
    assert {row[1]["qid"] for row in dev + test} == {"kept-1", "kept-2"}
    assert {row[1]["family"] for row in dev}.isdisjoint({row[1]["family"] for row in test})


def test_wilson_interval_reports_empty_denominator():
    from bench_v2 import wilson
    assert wilson(0, 0) == {"k": 0, "n": 0, "rate": None, "lo": None, "hi": None}
