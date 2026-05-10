"""
ai/prompt_builder.py

Structured JSON prompt construction for the NorthScale AI Layer.
Versioned prompts, sector-aware augmentation, deterministic signal injection.
"""

import json
from typing import Any, Dict

from engines.models import ScoringResult

PROMPT_VERSION = "1.0.0"

class PromptBuilder:
    def __init__(self):
        pass

    def build_thesis_system_prompt(self) -> str:
        return f"""You are NorthScale AI, an institutional-grade investment research assistant.
Your task is to synthesize deterministic financial signals into a professional, explainable investment thesis.

PROMPT_VERSION: {PROMPT_VERSION}

CRITICAL RULES (NON-NEGOTIABLE):
1. You MUST NOT calculate financial metrics.
2. You MUST NOT invent financial facts or numbers.
3. You MUST NOT override the provided deterministic recommendation.
4. You MUST use probabilistic language (e.g., "suggests", "indicates") rather than certainty claims (e.g., "will", "guarantees").
5. You MUST base your synthesis ONLY on the provided deterministic data.
6. Return output in valid JSON format.
"""

    def build_thesis_user_prompt(self, result: ScoringResult) -> str:
        
        # Format the deterministic data into structured JSON format for the prompt
        structured_data = {
            "metadata": {
                "ticker": result.ticker,
                "sector": result.sector_slug,
                "snapshot_date": result.snapshot_date.isoformat(),
            },
            "deterministic_recommendation": {
                "recommendation": result.recommendation.value,
                "conviction_score": float(result.conviction.conviction_score),
                "confidence_level": result.conviction.confidence_level.value,
                "composite_score": float(result.composite_score),
                "risk_score": float(result.risk_score),
            },
            "category_scores": {
                "growth": float(result.growth_score) if result.growth_score else None,
                "profitability": float(result.profitability_score) if result.profitability_score else None,
                "valuation": float(result.valuation_score) if result.valuation_score else None,
                "financial_health": float(result.financial_health_score) if result.financial_health_score else None,
                "ownership": float(result.ownership_score) if result.ownership_score else None,
            },
            "signals": {
                "positive": result.explainability.positive_signals,
                "negative": result.explainability.negative_signals,
            },
            "sector_context": result.explainability.sector_context,
            "confidence_reasoning": result.explainability.confidence_reasoning,
        }
        
        return f"""
Please synthesize an investment thesis based on the following deterministic data.

DETERMINISTIC DATA:
{json.dumps(structured_data, indent=2)}

OUTPUT FORMAT:
Your response MUST be a valid JSON object matching the following structure exactly:
{{
  "thesis_summary": "A concise 2-3 sentence overview of the investment thesis.",
  "bullish_factors": ["String 1", "String 2"],
  "bearish_factors": ["String 1", "String 2"],
  "risk_summary": "A 1-2 sentence summary of key risks.",
  "valuation_summary": "A 1-2 sentence contextualization of the valuation.",
  "overall_view": "A final synthesis confirming the deterministic recommendation."
}}

Make sure all fields are populated and accurate to the deterministic data.
"""

    def build_insights_system_prompt(self) -> str:
        return """You are NorthScale AI, an institutional-grade investment research assistant.
Your task is to generate concise, contextual insights from deterministic financial signals.
CRITICAL RULES:
1. Insights must be derived from the provided deterministic data.
2. No hallucinated observations.
3. Output MUST be valid JSON.
"""

    def build_insights_user_prompt(self, result: ScoringResult) -> str:
        structured_data = {
            "ticker": result.ticker,
            "recommendation": result.recommendation.value,
            "positive_signals": result.explainability.positive_signals,
            "negative_signals": result.explainability.negative_signals,
            "sector_context": result.explainability.sector_context,
        }
        return f"""
Please generate impactful insights for the following stock data.

DETERMINISTIC DATA:
{json.dumps(structured_data, indent=2)}

OUTPUT FORMAT:
Return a JSON array of insight objects. Maximum 3 insights.
[
  {{
    "insight_type": "OWNERSHIP_CHANGE" | "VALUATION_SHIFT" | "RISK_ALERT" | "EARNINGS_OBSERVATION" | "CONVICTION_CHANGE",
    "title": "Short title",
    "body": "Concise observation (1 sentence)",
    "severity": "INFO" | "WARNING" | "CRITICAL"
  }}
]
"""
