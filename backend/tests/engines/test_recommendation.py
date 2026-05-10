import pytest
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
