"""
tests/ai/test_fallback.py

Tests for the AI Fallback System.
Verifies that fallback responses are correctly generated from deterministic data.
"""

from datetime import date
from engines.models import (
    ScoringResult, RecommendationCategory, ConvictionOutput, ConfidenceLevel, 
    ExplainabilityOutput, RiskOutput
)
from ai.fallback import build_thesis_fallback, build_insights_fallback

def create_mock_result() -> ScoringResult:
    return ScoringResult(
        stock_id="test-id",
        ticker="TCS",
        sector_slug="it",
        snapshot_date=date(2024, 1, 1),
        recommendation=RecommendationCategory.STRONG_BUY,
        conviction=ConvictionOutput.from_score(8.5, ConfidenceLevel.VERY_HIGH, 9.0),
        explainability=ExplainabilityOutput(
            category_scores=[],
            risk_output=RiskOutput(risk_signals=[], total_risk_penalty=0.5, leverage_risk=0, valuation_risk=0, governance_risk=0, ownership_risk=0, cyclicality_risk=0, earnings_risk=0),
            positive_signals=["High ROE"],
            negative_signals=[],
            sector_context="IT context",
            confidence_reasoning="High confidence",
            data_quality_note=None
        ),
        growth_score=8.0,
        profitability_score=9.0,
        valuation_score=7.0,
        financial_health_score=9.0,
        ownership_score=8.0,
        risk_score=0.5,
        composite_score=9.0,
        financial_snapshot_id="fin-id-1",
        ownership_snapshot_id="own-id-1",
        scoring_version="1.0.0"
    )

def test_fallback_generates_response():
    result = create_mock_result()
    response = build_thesis_fallback(result)

    assert response is not None
    assert response["is_fallback"] is True
    assert "TCS" in response["thesis_summary"]
    assert "STRONG_BUY" in response["thesis_summary"]
    assert "High ROE" in response["bullish_factors"]
