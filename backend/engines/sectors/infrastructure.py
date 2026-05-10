"""
engines/sectors/infrastructure.py

Infrastructure Sector Scoring Engine.

KPI priorities:
  - Debt quality (leverage is structural for infra; level matters enormously)
  - Order book execution (proxied via revenue consistency)
  - Interest coverage (safety net for leverage-heavy model)
  - Working capital efficiency (high WC intensity is a key risk)
  - Valuation: Infra trades at lower multiples — PE 15–25 is fair

Sector-specific valuation interpretation:
  - PE < 15: Deep value or distressed
  - PE 15–22: Fair for infra
  - PE 22–35: Premium for high-quality infra
  - PE > 35: Expensive for traditional infra
"""

from __future__ import annotations

from engines.models import CategoryScore, FinancialMetricsInput
from engines.sectors.base import BaseSectorScorer


class InfraScorer(BaseSectorScorer):
    sector_name = "Infrastructure"
    sector_slug = "infrastructure"

    WEIGHTS = {
        "growth": 0.20,
        "profitability": 0.20,
        "valuation": 0.15,
        "financial_health": 0.35,  # Leverage is critical for infra
        "ownership": 0.10,
    }

    def score_growth(self, metrics: FinancialMetricsInput) -> CategoryScore:
        pos, neg = [], []
        score = 0.0

        r3 = metrics.revenue_3y_cagr
        if r3 is not None:
            if r3 >= 20:
                score += 5.0; pos.append(f"Strong order book execution: {r3:.1f}% CAGR")
            elif r3 >= 12:
                score += 3.5; pos.append(f"Healthy infra growth: {r3:.1f}%")
            elif r3 >= 7:
                score += 1.5
            elif r3 < 0:
                neg.append(f"Revenue contraction: {r3:.1f}%")

        p3 = metrics.profit_3y_cagr
        if p3 is not None:
            if p3 >= 20:
                score += 3.0; pos.append(f"Strong profit CAGR: {p3:.1f}%")
            elif p3 >= 10:
                score += 1.5
            elif p3 < 0:
                neg.append(f"Profit decline: {p3:.1f}%")

        raw = min(10.0, score * 10 / 8.0)
        weight = self.WEIGHTS["growth"]
        return CategoryScore(
            category="growth",
            raw_score=round(raw, 2),
            weight=weight,
            weighted_contribution=round(raw * weight, 4),
            positive_signals=pos,
            negative_signals=neg,
            data_available=metrics.revenue_3y_cagr is not None,
        )

    def score_profitability(self, metrics: FinancialMetricsInput) -> CategoryScore:
        pos, neg = [], []
        score = 0.0

        roce = metrics.roce
        if roce is not None:
            if roce >= 18:
                score += 4.0; pos.append(f"Strong infra ROCE: {roce:.1f}% (>18%)")
            elif roce >= 12:
                score += 2.5; pos.append(f"Adequate ROCE: {roce:.1f}%")
            elif roce >= 8:
                score += 1.0
            else:
                neg.append(f"Weak ROCE for infra: {roce:.1f}% (<8%)")

        margin = metrics.operating_margin
        if margin is not None:
            if margin >= 18:
                score += 4.0; pos.append(f"Strong operating margin: {margin:.1f}%")
            elif margin >= 12:
                score += 2.0; pos.append(f"Acceptable margin: {margin:.1f}%")
            elif margin < 8:
                neg.append(f"Thin margins: {margin:.1f}% (<8%)")

        raw = min(10.0, score * 10 / 8.0)
        weight = self.WEIGHTS["profitability"]
        return CategoryScore(
            category="profitability",
            raw_score=round(raw, 2),
            weight=weight,
            weighted_contribution=round(raw * weight, 4),
            positive_signals=pos,
            negative_signals=neg,
            data_available=metrics.roce is not None,
        )

    def score_valuation(self, metrics: FinancialMetricsInput) -> CategoryScore:
        pos, neg = [], []
        score = 0.0

        pe = metrics.pe_ratio
        if pe is not None and pe > 0:
            if pe < 15:
                score += 5.0; pos.append(f"Deep value infra: PE {pe:.1f}x")
            elif pe < 22:
                score += 3.5; pos.append(f"Fair infra valuation: PE {pe:.1f}x")
            elif pe < 32:
                score += 1.5; pos.append(f"Premium infra: PE {pe:.1f}x")
            else:
                neg.append(f"Expensive for infra: PE {pe:.1f}x (>32x)")

        raw = min(10.0, score * 10 / 5.0)
        weight = self.WEIGHTS["valuation"]
        return CategoryScore(
            category="valuation",
            raw_score=round(raw, 2),
            weight=weight,
            weighted_contribution=round(raw * weight, 4),
            positive_signals=pos,
            negative_signals=neg,
            data_available=metrics.pe_ratio is not None,
        )

    def score_financial_health(self, metrics: FinancialMetricsInput) -> CategoryScore:
        """Leverage is the critical dimension for infrastructure companies."""
        pos, neg = [], []
        score = 0.0

        de = metrics.debt_to_equity
        if de is not None:
            if de < 0.5:
                score += 5.0; pos.append(f"Conservative infra leverage: D/E {de:.2f}")
            elif de < 1.0:
                score += 3.5; pos.append(f"Manageable leverage: D/E {de:.2f}")
            elif de < 1.5:
                score += 2.0; pos.append(f"Moderate leverage: D/E {de:.2f}")
            elif de < 2.0:
                score += 0.5; neg.append(f"High leverage: D/E {de:.2f}")
            else:
                neg.append(f"Dangerous leverage for infra: D/E {de:.2f} (>2.0)")

        ic = metrics.interest_coverage
        if ic is not None:
            if ic >= 5.0:
                score += 4.0; pos.append(f"Comfortable interest coverage: {ic:.2f}x")
            elif ic >= 3.0:
                score += 2.5; pos.append(f"Adequate coverage: {ic:.2f}x")
            elif ic >= 2.0:
                score += 0.5; pos.append(f"Tight but adequate coverage: {ic:.2f}x")
            else:
                neg.append(f"Weak interest coverage: {ic:.2f}x (<2.0x)")

        raw = min(10.0, score * 10 / 9.0)
        weight = self.WEIGHTS["financial_health"]
        return CategoryScore(
            category="financial_health",
            raw_score=round(raw, 2),
            weight=weight,
            weighted_contribution=round(raw * weight, 4),
            positive_signals=pos,
            negative_signals=neg,
            data_available=metrics.debt_to_equity is not None,
        )

    def score_ownership(self, metrics: FinancialMetricsInput) -> CategoryScore:
        pos, neg = [], []
        score = 0.0

        promo = metrics.promoter_holding
        if promo is not None:
            if promo >= 55:
                score += 5.0; pos.append(f"High promoter ownership: {promo:.1f}%")
            elif promo >= 40:
                score += 3.0
            elif promo < 25:
                neg.append(f"Low promoter holding: {promo:.1f}%")

        pledge = metrics.promoter_pledge_pct
        if pledge is not None:
            if pledge == 0:
                score += 3.0; pos.append("No promoter pledge")
            elif pledge > 20:
                neg.append(f"Critical pledge for infra: {pledge:.1f}%")

        change = metrics.promoter_change_qoq
        if change is not None and change > 0.5:
            score += 2.0; pos.append(f"Promoter increasing: +{change:.2f}%")
        elif change is not None and change < -1.0:
            neg.append(f"Promoter reducing: {change:.2f}%")

        raw = min(10.0, score * 10 / 10.0)
        weight = self.WEIGHTS["ownership"]
        return CategoryScore(
            category="ownership",
            raw_score=round(raw, 2),
            weight=weight,
            weighted_contribution=round(raw * weight, 4),
            positive_signals=pos,
            negative_signals=neg,
            data_available=metrics.promoter_holding is not None,
        )
