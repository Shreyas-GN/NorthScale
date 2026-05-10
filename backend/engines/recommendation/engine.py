"""
engines/recommendation/engine.py

Deterministic Recommendation Engine.

Classifies stocks into STRONG_BUY / BUY / HOLD / WATCHLIST / SELL / AVOID
based entirely on:
  - weighted category scores from sector scorers
  - risk-adjusted conviction score
  - confidence level from data quality

All outputs are:
  - deterministic
  - explainable
  - typed
  - auditable
  - reproducible

No AI. No randomness. No hallucination.
"""

from __future__ import annotations

from engines.models import ConvictionOutput, RecommendationCategory


# Conviction score thresholds (from SCORING_ENGINE.md)
_THRESHOLDS: list[tuple[float, RecommendationCategory]] = [
    (8.5, RecommendationCategory.STRONG_BUY),
    (7.0, RecommendationCategory.BUY),
    (5.0, RecommendationCategory.HOLD),
    (3.0, RecommendationCategory.WATCHLIST),
    (0.0, RecommendationCategory.SELL),
]


def classify_recommendation(conviction: ConvictionOutput) -> RecommendationCategory:
    """
    Map conviction score to recommendation category.
    Uses descending threshold matching — first match wins.

    Score thresholds from SCORING_ENGINE.md:
      8.5+ → STRONG_BUY
      7.0–8.49 → BUY
      5.0–6.99 → HOLD
      3.0–4.99 → WATCHLIST
      <3.0 → SELL
    """
    score = conviction.conviction_score

    # Downgrade STRONG_BUY to BUY if confidence is LOW
    # (prevents recommending STRONG_BUY when data is unreliable)
    if conviction.confidence_level.value == "LOW" and score >= 8.5:
        return RecommendationCategory.BUY

    for threshold, category in _THRESHOLDS:
        if score >= threshold:
            return category

    return RecommendationCategory.SELL
