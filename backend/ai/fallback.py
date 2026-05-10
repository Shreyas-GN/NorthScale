"""
ai/fallback.py

Deterministic Fallback Layer for AI Generation.
Graceful degradation if Groq API fails or validation fails repeatedly.
"""

from typing import Dict, Any

from engines.models import ScoringResult
from core.logging import logger

def build_thesis_fallback(result: ScoringResult) -> Dict[str, Any]:
    """
    Builds a structured thesis directly from deterministic outputs.
    Guarantees a response even if the LLM is down.
    """
    logger.warning(f"[FALLBACK] Triggering deterministic fallback for thesis generation on {result.ticker}")

    thesis_summary = (
        f"Deterministic recommendation for {result.ticker} is {result.recommendation.value} "
        f"with a conviction score of {result.conviction.conviction_score:.2f}."
    )

    bullish = result.explainability.positive_signals[:3] if result.explainability.positive_signals else ["No major bullish signals detected."]
    bearish = result.explainability.negative_signals[:3] if result.explainability.negative_signals else ["No major bearish signals detected."]

    risk_summary = f"Total risk penalty is {result.risk_score:.2f}. " + result.explainability.confidence_reasoning

    valuation_summary = "Valuation assessment based on deterministic metrics."
    if result.valuation_score:
        valuation_summary += f" Valuation score: {result.valuation_score}/10."

    return {
        "thesis_summary": thesis_summary,
        "bullish_factors": bullish,
        "bearish_factors": bearish,
        "risk_summary": risk_summary,
        "valuation_summary": valuation_summary,
        "overall_view": f"Maintains {result.recommendation.value} rating.",
        "is_fallback": True
    }

def build_insights_fallback(result: ScoringResult) -> list:
    """
    Fallback for insights generation.
    """
    logger.warning(f"[FALLBACK] Triggering deterministic fallback for insights on {result.ticker}")
    
    insights = []
    
    if result.recommendation.value in ["STRONG_BUY", "SELL"]:
        insights.append({
            "insight_type": "CONVICTION_CHANGE",
            "title": f"Strong Signal: {result.recommendation.value}",
            "body": f"System generated a {result.recommendation.value} rating based on recent data.",
            "severity": "INFO"
        })
        
    if result.risk_score >= 6.0:
        insights.append({
            "insight_type": "RISK_ALERT",
            "title": "Elevated Risk Detected",
            "body": "System flagged elevated risk factors for this stock.",
            "severity": "WARNING"
        })
        
    return insights
