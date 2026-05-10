"""
tests/ai/test_prompt_builder.py

Tests for the AI Prompt Builder.
Ensures correct prompt construction and constraint inclusion.
"""

from datetime import date
from engines.models import (
    ScoringResult, RecommendationCategory, ConvictionOutput, ConfidenceLevel, 
    ExplainabilityOutput, RiskOutput
)
from ai.prompt_builder import PromptBuilder

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

def test_prompt_builds_correctly():
    builder = PromptBuilder()
    system_prompt = builder.build_thesis_system_prompt()
    
    assert "CRITICAL RULES" in system_prompt
    assert "MUST NOT invent financial facts" in system_prompt
    
    user_prompt = builder.build_thesis_user_prompt(create_mock_result())
    
    assert "TCS" in user_prompt
    assert "STRONG_BUY" in user_prompt
    assert "High ROE" in user_prompt
