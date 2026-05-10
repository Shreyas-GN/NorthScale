"""
tests/ai/test_validator.py

Tests for the AI Output Validator.
Verifies rejection of invalid structures and missing fields.
"""

from ai.validators.output_validator import validate_thesis_json, validate_insights_json

def test_invalid_json_fails():
    bad_data = '{ "summary": "missing quotes }'
    result = validate_thesis_json(bad_data)
    assert result.is_valid is False
    assert "Invalid JSON format" in result.error

def test_missing_fields_fails():
    bad_data = '''
    {
      "thesis_summary": "good stock",
      "bullish_factors": ["Growth"]
    }
    '''
    result = validate_thesis_json(bad_data)
    assert result.is_valid is False
    assert "Missing field" in result.error

def test_valid_thesis_succeeds():
    good_data = '''
    {
      "thesis_summary": "Strong buy.",
      "bullish_factors": ["Growth"],
      "bearish_factors": ["None"],
      "risk_summary": "Low risk.",
      "valuation_summary": "Fairly valued.",
      "overall_view": "Solid."
    }
    '''
    result = validate_thesis_json(good_data)
    assert result.is_valid is True
