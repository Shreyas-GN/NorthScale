"""
engines/sectors/base.py

Abstract base class for all sector-specific scoring modules.
Each sector scorer must:
  - define its weighted scoring model
  - define sector KPIs
  - define valuation interpretation thresholds
  - produce a CategoryScore per category
  - return typed, explainable outputs
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from engines.models import CategoryScore, FinancialMetricsInput


class BaseSectorScorer(ABC):
    """
    Base sector scoring interface.
    All sector scorers must implement score_category for each dimension
    and produce the final sector_score_output.
    """

    sector_name: str
    sector_slug: str

    # Default weight overrides for this sector
    # Must sum to 1.0 — engines enforce this
    WEIGHTS: dict = {
        "growth": 0.25,
        "profitability": 0.20,
        "valuation": 0.20,
        "financial_health": 0.20,
        "ownership": 0.10,
    }

    @abstractmethod
    def score_growth(self, metrics: FinancialMetricsInput) -> CategoryScore:
        ...

    @abstractmethod
    def score_profitability(self, metrics: FinancialMetricsInput) -> CategoryScore:
        ...

    @abstractmethod
    def score_valuation(self, metrics: FinancialMetricsInput) -> CategoryScore:
        ...

    @abstractmethod
    def score_financial_health(self, metrics: FinancialMetricsInput) -> CategoryScore:
        ...

    @abstractmethod
    def score_ownership(self, metrics: FinancialMetricsInput) -> CategoryScore:
        ...

    def score_all(self, metrics: FinancialMetricsInput) -> List[CategoryScore]:
        """Run all category scorers and return typed list."""
        return [
            self.score_growth(metrics),
            self.score_profitability(metrics),
            self.score_valuation(metrics),
            self.score_financial_health(metrics),
            self.score_ownership(metrics),
        ]

    def composite_score(self, category_scores: List[CategoryScore]) -> float:
        """
        Weighted composite = sum(raw_score * weight) for all categories.
        Clamped to [0.0, 10.0].
        """
        total = sum(cs.weighted_contribution for cs in category_scores)
        return round(min(10.0, max(0.0, total)), 4)

    # ---------------------------------------------------------------------------
    # Shared scoring helpers
    # ---------------------------------------------------------------------------

    @staticmethod
    def _score_metric(
        value: float | None,
        thresholds: list[tuple[float, float, str]],
    ) -> tuple[float, list[str], list[str]]:
        """
        Generic band-based metric scorer.
        thresholds: [(min_val, score_pts, label), ...]  — evaluated in order
        Returns (score, positive_signals, negative_signals)
        """
        if value is None:
            return 0.0, [], ["Data unavailable"]
        for min_val, pts, label in thresholds:
            if value >= min_val:
                return pts, [label], []
        return 0.0, [], []
