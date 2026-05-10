import os

BASE = r"c:\Users\Shreyas Hegde\Desktop\Northscale\NorthScale\backend\tests\engines"

test_ratios = """import pytest
from engines.ratios.profitability import calculate_roe, calculate_roce
from engines.ratios.valuation import calculate_pe, calculate_pb
from engines.ratios.growth import calculate_cagr

def test_calculate_roe():
    assert calculate_roe(10, 100) == 10.0
    assert calculate_roe(None, 100) is None
    assert calculate_roe(10, 0) is None

def test_calculate_roce():
    assert calculate_roce(15, 150) == 10.0
    assert calculate_roce(15, -10) is None

def test_calculate_pe():
    assert calculate_pe(100, 5) == 20.0
    assert calculate_pe(100, 0) is None

def test_calculate_cagr():
    assert round(calculate_cagr(100, 133.1, 3), 2) == 10.0
    assert calculate_cagr(0, 100, 3) is None
"""

test_sectors = """import pytest
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
"""

test_recommendation = """import pytest
from engines.recommendation.recommendation import generate_recommendation, determine_recommendation_classification

def test_determine_recommendation_classification():
    assert determine_recommendation_classification(9.0) == "STRONG_BUY"
    assert determine_recommendation_classification(7.5) == "BUY"
    assert determine_recommendation_classification(5.5) == "HOLD"
    assert determine_recommendation_classification(4.0) == "WATCHLIST"
    assert determine_recommendation_classification(2.0) == "SELL"

def test_generate_recommendation():
    metrics = {
        "roe": 25, "revenue_3y_cagr": 20, "pe_ratio": 25,
        "debt_to_equity": 0.5, "interest_coverage": 5.0,
        "freshness_score": 100
    }
    
    res = generate_recommendation(metrics, "it")
    assert res["base_score"] == 10.0
    assert res["risk_penalty"] == 0.0
    assert res["conviction_score"] == 10.0
    assert res["recommendation"] == "STRONG_BUY"
    assert res["confidence_level"] == "VERY_HIGH"

def test_generate_recommendation_with_risk():
    metrics = {
        "roe": 25, "revenue_3y_cagr": 20, "pe_ratio": 45, # High PE risk for IT
        "debt_to_equity": 2.5, # High debt risk
        "interest_coverage": 1.5, # Poor coverage
        "freshness_score": 60
    }
    
    res = generate_recommendation(metrics, "it")
    assert res["risk_penalty"] > 0
    assert res["conviction_score"] < res["base_score"]
    assert res["confidence_level"] == "MODERATE"
    assert len(res["negative_signals"]) > 0
"""

with open(os.path.join(BASE, "test_ratios.py"), "w") as f: f.write(test_ratios)
with open(os.path.join(BASE, "test_sectors.py"), "w") as f: f.write(test_sectors)
with open(os.path.join(BASE, "test_recommendation.py"), "w") as f: f.write(test_recommendation)
