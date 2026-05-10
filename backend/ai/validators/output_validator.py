"""
ai/validators/output_validator.py

AI Validation Layer to ensure structured JSON output adheres to rules.
Prevents hallucinations and structural errors.
"""

import json
from typing import Any, Dict

from core.logging import logger

class ValidationResult:
    def __init__(self, is_valid: bool, data: Dict[str, Any] = None, error: str = None):
        self.is_valid = is_valid
        self.data = data or {}
        self.error = error

def validate_thesis_json(content: str) -> ValidationResult:
    """
    Validates thesis generation JSON response.
    Ensures required fields are present and structurally correct.
    """
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"[VALIDATOR] JSON decode error: {e}")
        return ValidationResult(is_valid=False, error="Invalid JSON format")

    required_fields = [
        "thesis_summary",
        "bullish_factors",
        "bearish_factors",
        "risk_summary",
        "valuation_summary",
        "overall_view"
    ]

    for field in required_fields:
        if field not in data:
            logger.error(f"[VALIDATOR] Missing required field: {field}")
            return ValidationResult(is_valid=False, error=f"Missing field: {field}")

    if not isinstance(data.get("bullish_factors"), list) or not isinstance(data.get("bearish_factors"), list):
        logger.error("[VALIDATOR] bullish/bearish factors must be lists")
        return ValidationResult(is_valid=False, error="bullish/bearish factors must be lists")

    # Could add more deterministic validation here (e.g., checking if it contains certainty claims)
    # For MVP, structural validation is key.
    
    return ValidationResult(is_valid=True, data=data)

def validate_insights_json(content: str) -> ValidationResult:
    """
    Validates insights generation JSON response.
    """
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"[VALIDATOR] JSON decode error: {e}")
        return ValidationResult(is_valid=False, error="Invalid JSON format")

    if not isinstance(data, list):
        logger.error("[VALIDATOR] Insights must be a JSON array")
        return ValidationResult(is_valid=False, error="Insights must be a list")

    valid_types = {"OWNERSHIP_CHANGE", "VALUATION_SHIFT", "RISK_ALERT", "EARNINGS_OBSERVATION", "CONVICTION_CHANGE", "GROWTH_SIGNAL", "PORTFOLIO_INTELLIGENCE", "SECTOR_OBSERVATION"}
    valid_severities = {"INFO", "WARNING", "CRITICAL"}

    for insight in data:
        required_fields = ["insight_type", "title", "body", "severity"]
        for field in required_fields:
            if field not in insight:
                return ValidationResult(is_valid=False, error=f"Missing field in insight: {field}")
        
        if insight["insight_type"] not in valid_types:
            return ValidationResult(is_valid=False, error=f"Invalid insight type: {insight['insight_type']}")
            
        if insight["severity"] not in valid_severities:
            return ValidationResult(is_valid=False, error=f"Invalid severity: {insight['severity']}")

    return ValidationResult(is_valid=True, data={"insights": data})
