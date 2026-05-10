"""
tests/ai/test_pipeline.py

Full Pipeline Test for AI Generation.
Tests the flow: Input -> Prompt -> Groq -> Validator -> Fallback -> Save
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import date

from engines.models import (
    ScoringResult, RecommendationCategory, ConvictionOutput, ConfidenceLevel, 
    ExplainabilityOutput, RiskOutput
)
from ai.generators.thesis_generator import ThesisGenerator

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

@patch('ai.generators.thesis_generator.AIPersistence')
@patch('ai.generators.thesis_generator.GroqClient')
def test_full_pipeline_success(mock_groq_class, mock_persistence_class):
    # Setup mock Groq response
    mock_groq_client = MagicMock()
    mock_response = MagicMock()
    
    valid_json = {
        "thesis_summary": "Great stock.",
        "bullish_factors": ["Growth"],
        "bearish_factors": ["None"],
        "risk_summary": "Low",
        "valuation_summary": "Fair",
        "overall_view": "Buy"
    }
    mock_response.content = json.dumps(valid_json)
    mock_response.latency_ms = 100
    mock_response.prompt_tokens = 50
    mock_response.completion_tokens = 50
    mock_groq_client.generate.return_value = mock_response
    mock_groq_class.return_value = mock_groq_client
    
    # Setup mock persistence
    mock_persistence = MagicMock()
    mock_persistence_class.return_value = mock_persistence

    generator = ThesisGenerator()
    result_data = generator.generate_thesis(create_mock_result())

    assert result_data is not None
    assert "thesis_summary" in result_data
    assert result_data["thesis_summary"] == "Great stock."
    
    # Verify persistence was called
    mock_persistence.save_thesis.assert_called_once()
    mock_persistence.log_generation.assert_called_once()

@patch('ai.generators.thesis_generator.AIPersistence')
@patch('ai.generators.thesis_generator.GroqClient')
def test_full_pipeline_fallback(mock_groq_class, mock_persistence_class):
    # Setup mock Groq to fail
    mock_groq_client = MagicMock()
    mock_groq_client.generate.side_effect = Exception("API Down")
    mock_groq_class.return_value = mock_groq_client
    
    # Setup mock persistence
    mock_persistence = MagicMock()
    mock_persistence_class.return_value = mock_persistence

    generator = ThesisGenerator()
    result_data = generator.generate_thesis(create_mock_result())

    assert result_data is not None
    assert result_data.get("is_fallback") is True
    assert "TCS" in result_data["thesis_summary"]
    
    # Verify fallback persistence was called
    mock_persistence.save_thesis.assert_called_once()
    mock_persistence.log_generation.assert_called_once()
