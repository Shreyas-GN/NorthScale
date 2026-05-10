"""
tests/ai/test_ai_layer.py

Deterministic validation tests for AI Layer.
Testing validation layer, fallback logic, and structure.
"""

import pytest
from datetime import date

from engines.models import (
    ScoringResult, RecommendationCategory, ConvictionOutput, ConfidenceLevel, 
    ExplainabilityOutput, RiskOutput, CategoryScore
)
from ai.validators.output_validator import validate_thesis_json, validate_insights_json
from ai.fallback import build_thesis_fallback, build_insights_fallback

def create_mock_scoring_result() -> ScoringResult:
    return ScoringResult(
        stock_id="test-stock-1",
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
            confidence_reasoning="High confidence due to good data.",
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

def test_validate_thesis_json_valid():
    content = '''
    {
      "thesis_summary": "Strong buy.",
      "bullish_factors": ["Growth"],
      "bearish_factors": ["None"],
      "risk_summary": "Low risk.",
      "valuation_summary": "Fairly valued.",
      "overall_view": "Solid."
    }
    '''
    result = validate_thesis_json(content)
    assert result.is_valid is True

def test_validate_thesis_json_invalid_json():
    content = '{ "thesis_summary": "Missing quotes }'
    result = validate_thesis_json(content)
    assert result.is_valid is False
    assert "Invalid JSON format" in result.error

def test_validate_thesis_json_missing_field():
    content = '''
    {
      "thesis_summary": "Strong buy.",
      "bullish_factors": ["Growth"],
      "bearish_factors": ["None"],
      "risk_summary": "Low risk.",
      "overall_view": "Solid."
    }
    '''
    result = validate_thesis_json(content)
    assert result.is_valid is False
    assert "Missing field: valuation_summary" in result.error

def test_validate_insights_json_valid():
    content = '''
    [
      {
        "insight_type": "OWNERSHIP_CHANGE",
        "title": "Promoter holding up",
        "body": "Promoters increased stake by 1%.",
        "severity": "INFO"
      }
    ]
    '''
    result = validate_insights_json(content)
    assert result.is_valid is True
    
def test_validate_insights_json_invalid_type():
    content = '''
    [
      {
        "insight_type": "INVALID_TYPE",
        "title": "Bad Insight",
        "body": "Test",
        "severity": "INFO"
      }
    ]
    '''
    result = validate_insights_json(content)
    assert result.is_valid is False
    assert "Invalid insight type" in result.error

def test_fallback_activation():
    mock_result = create_mock_scoring_result()
    fallback_data = build_thesis_fallback(mock_result)
    
    assert fallback_data["is_fallback"] is True
    assert "TCS" in fallback_data["thesis_summary"]
    assert "STRONG_BUY" in fallback_data["thesis_summary"]
    assert "High ROE" in fallback_data["bullish_factors"]

def test_insights_fallback_activation():
    mock_result = create_mock_scoring_result()
    fallback_insights = build_insights_fallback(mock_result)
    
    assert len(fallback_insights) > 0
    assert fallback_insights[0]["insight_type"] == "CONVICTION_CHANGE"
    assert "STRONG_BUY" in fallback_insights[0]["title"]
