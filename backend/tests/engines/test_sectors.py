import pytest
from engines.sectors.it import ITScorer
from engines.sectors.banking import BankingScorer

def test_it_scorer():
    scorer = ITScorer()
    metrics = {"roe": 25, "revenue_3y_cagr": 20, "pe_ratio": 25}
    res = scorer.score(metrics)
    assert res["score"] == 7.0
    assert res["normalized_score"] == 10.0
    assert len(res["positive_signals"]) == 3

def test_banking_scorer():
    scorer = BankingScorer()
    metrics = {"casa_ratio": 45, "gnpa_ratio": 1.0, "nim": 4.0, "pb_ratio": 1.5}
    res = scorer.score(metrics)
    assert res["score"] == 10.0
    assert "Strong CASA ratio (>40%)" in res["positive_signals"]
    assert len(res["negative_signals"]) == 0
    
    bad_metrics = {"casa_ratio": 20, "gnpa_ratio": 4.0}
    bad_res = scorer.score(bad_metrics)
    assert bad_res["score"] == 0.0
    assert len(bad_res["negative_signals"]) == 2
