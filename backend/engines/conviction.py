"""
engines/conviction.py

Deterministic Conviction Scoring Engine.

Computes a conviction score (1–10) from weighted category scores
and risk-adjusts it using the risk engine output.

Conviction is distinct from the raw composite score:
  - Composite = weighted average of category scores
  - Conviction = risk-adjusted composite + confidence modifier

No randomness. No AI influence. No hallucination.
"""

from __future__ import annotations

from engines.models import (
    CategoryScore,
    ConfidenceLevel,
    ConvictionOutput,
    FinancialMetricsInput,
    RiskOutput,
)


def determine_confidence_level(
    freshness_score: int,
    completeness_ratio: float,
    risk_output: RiskOutput,
) -> ConfidenceLevel:
    """
    Confidence is a function of:
      - data freshness (how recent is the snapshot)
      - data completeness (fraction of key fields populated)
      - risk level (high risk reduces confidence even with good data)
    """
    # Downgrade confidence if data is stale or incomplete
    if freshness_score < 40 or completeness_ratio < 0.4:
        return ConfidenceLevel.LOW

    if freshness_score < 65 or completeness_ratio < 0.6:
        return ConfidenceLevel.MODERATE

    # High risk environments → downgrade confidence
    if risk_output.governance_risk >= 4.0:
        return ConfidenceLevel.MODERATE

    if freshness_score >= 80 and completeness_ratio >= 0.8:
        if risk_output.total_risk_penalty < 3.0:
            return ConfidenceLevel.VERY_HIGH
        return ConfidenceLevel.HIGH

    return ConfidenceLevel.MODERATE


def compute_conviction(
    category_scores: list[CategoryScore],
    risk_output: RiskOutput,
    metrics: FinancialMetricsInput,
) -> ConvictionOutput:
    """
    Compute the final conviction score from:
      1. Weighted composite of all category scores
      2. Risk penalty reduction
      3. Confidence level classification

    Returns a fully typed ConvictionOutput.
    """
    # Step 1: Weighted composite (sum of weighted_contribution per category)
    composite = sum(cs.weighted_contribution for cs in category_scores)
    composite = round(min(10.0, max(0.0, composite)), 4)

    # Step 2: Risk-adjust the composite
    # Risk penalty is dampened: full penalty would be too aggressive
    # We apply 40% of the total risk penalty as a reduction
    risk_reduction = risk_output.total_risk_penalty * 0.40
    conviction_score = max(0.0, round(composite - risk_reduction, 4))
    conviction_score = min(10.0, conviction_score)

    # Step 3: Determine confidence based on data quality
    confidence = determine_confidence_level(
        freshness_score=metrics.freshness_score,
        completeness_ratio=metrics.completeness_ratio(),
        risk_output=risk_output,
    )

    # Step 4: Build typed output
    return ConvictionOutput.from_score(
        score=conviction_score,
        confidence=confidence,
        composite=composite,
    )
