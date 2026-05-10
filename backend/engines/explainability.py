"""
engines/explainability.py

Deterministic Explainability Layer.

Every recommendation output must expose:
  - contributing category scores with signals
  - positive signals aggregated across all categories
  - negative signals aggregated across all categories
  - risk summary
  - sector context
  - confidence reasoning

No black-box outputs. Every conviction and recommendation
must be fully traceable to deterministic inputs.
"""

from __future__ import annotations

from typing import List

from engines.models import (
    CategoryScore,
    ConfidenceLevel,
    ConvictionOutput,
    ExplainabilityOutput,
    FinancialMetricsInput,
    RecommendationCategory,
    RiskOutput,
)


def build_confidence_reasoning(
    conviction: ConvictionOutput,
    metrics: FinancialMetricsInput,
    risk_output: RiskOutput,
) -> str:
    """
    Produce a human-readable, deterministic confidence reasoning statement.
    This is structured text — not AI generated.
    """
    parts: List[str] = []

    freshness = metrics.freshness_score
    completeness = round(metrics.completeness_ratio() * 100, 0)

    if freshness >= 80:
        parts.append(f"Data freshness is strong ({freshness}/100).")
    elif freshness >= 50:
        parts.append(f"Data freshness is moderate ({freshness}/100).")
    else:
        parts.append(f"Data freshness is low ({freshness}/100) — confidence reduced.")

    parts.append(f"Key metric completeness: {completeness:.0f}%.")

    if risk_output.governance_risk >= 4.0:
        parts.append("Governance risk is elevated — confidence capped at MODERATE.")
    elif risk_output.total_risk_penalty >= 6.0:
        parts.append("Multiple material risks identified — confidence downgraded.")
    elif risk_output.total_risk_penalty < 2.0:
        parts.append("Risk profile is clean — no major risk flags.")

    tier_msg = {
        "EXCEPTIONAL": "Conviction is EXCEPTIONAL — all signals strongly positive.",
        "STRONG": "Conviction is STRONG — majority of signals positive with manageable risks.",
        "MODERATE": "Conviction is MODERATE — mixed signals or moderate risks present.",
        "WEAK": "Conviction is WEAK — multiple concerns or limited positive signals.",
        "POOR": "Conviction is POOR — fundamentals are weak or risks are critical.",
    }
    parts.append(tier_msg.get(conviction.conviction_tier.value, ""))

    return " ".join(p for p in parts if p)


def build_sector_context(sector_slug: str, risk_output: RiskOutput) -> str:
    """
    Return sector-specific context note for the explainability output.
    Deterministic, no AI.
    """
    contexts = {
        "it": "IT sector scored on growth quality, capital efficiency, and margin sustainability. "
              "Asset-light model allows high ROCE. Valuation premium acceptable for consistent compounders.",
        "banking": "Banking sector evaluated on CASA franchise, NPA quality, NIM, and CAR. "
                   "P/B is the primary valuation metric. NPA trajectory is the single biggest risk factor.",
        "fmcg": "FMCG evaluated on pricing power, distribution strength, and margin consistency. "
                "Premium PE multiples justified by compounding nature and brand moat.",
        "pharma": "Pharma evaluated on margin quality, export pipeline health, and regulatory risk proxy. "
                  "USFDA compliance and product pipeline are primary qualitative overlays.",
        "infrastructure": "Infrastructure evaluated with heavy weight on leverage quality and interest coverage. "
                          "Execution risk proxied by revenue CAGR consistency.",
        "finance": "Finance sector evaluated similarly to banking — NPA quality, NIM, and P/B primary.",
        "cement": "Cement evaluated as capital-intensive infra play — leverage and ROCE are primary.",
    }
    base = contexts.get(sector_slug.lower(), f"No specific sector context for {sector_slug.upper()}.")

    cyc_note = ""
    if risk_output.cyclicality_risk >= 3.5:
        cyc_note = f" ⚠ {sector_slug.upper()} is a highly cyclical sector — scoring adjusts for cycle position."
    elif risk_output.cyclicality_risk >= 2.5:
        cyc_note = f" Note: {sector_slug.upper()} has moderate cyclicality — monitor macro headwinds."

    return base + cyc_note


def build_explainability(
    category_scores: List[CategoryScore],
    risk_output: RiskOutput,
    conviction: ConvictionOutput,
    metrics: FinancialMetricsInput,
    sector_slug: str,
) -> ExplainabilityOutput:
    """
    Assemble the full explainability record from all engine outputs.
    """
    # Aggregate signals across all categories
    all_positives: List[str] = []
    all_negatives: List[str] = []

    for cs in category_scores:
        all_positives.extend(cs.positive_signals)
        all_negatives.extend(cs.negative_signals)

    # Add risk-level signals to negatives
    all_negatives.extend(risk_output.risk_signals)

    data_quality_note: str | None = None
    completeness = metrics.completeness_ratio()
    if completeness < 0.5:
        data_quality_note = (
            f"Warning: Only {round(completeness * 100, 0):.0f}% of key financial metrics are available. "
            f"Scoring quality is reduced. Confidence adjusted to {conviction.confidence_level.value}."
        )

    return ExplainabilityOutput(
        category_scores=category_scores,
        risk_output=risk_output,
        positive_signals=all_positives,
        negative_signals=all_negatives,
        sector_context=build_sector_context(sector_slug, risk_output),
        confidence_reasoning=build_confidence_reasoning(conviction, metrics, risk_output),
        data_quality_note=data_quality_note,
    )
