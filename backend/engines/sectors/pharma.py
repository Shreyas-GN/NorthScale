"""
engines/sectors/pharma.py

Pharma Sector Scoring Engine.

KPI priorities:
  - Regulatory compliance strength (proxied via margin stability)
  - Export-led vs domestic revenue mix (approximated via growth patterns)
  - Pipeline quality (proxied via revenue consistency)
  - Operating margins (>20% preferred — API/formulation mix indicator)

Sector-specific valuation interpretation:
  - Pharma PE 20–30: Deep value
  - PE 30–45: Fair
  - PE 45–60: Premium (justify with strong pipeline/ANDA approvals)
  - PE > 60: Expensive unless high-growth specialty pharma
"""

from __future__ import annotations

from engines.models import CategoryScore, FinancialMetricsInput
from engines.sectors.base import BaseSectorScorer


class PharmaScorer(BaseSectorScorer):
    sector_name = "Pharma"
    sector_slug = "pharma"

    WEIGHTS = {
        "growth": 0.25,
        "profitability": 0.30,
        "valuation": 0.20,
        "financial_health": 0.15,
        "ownership": 0.10,
    }

    def score_growth(self, metrics: FinancialMetricsInput) -> CategoryScore:
        pos, neg = [], []
        score = 0.0

        r3 = metrics.revenue_3y_cagr
        if r3 is not None:
            if r3 >= 15:
                score += 5.0; pos.append(f"Strong pharma revenue growth: {r3:.1f}%")
            elif r3 >= 10:
                score += 3.5; pos.append(f"Healthy growth: {r3:.1f}%")
            elif r3 >= 5:
                score += 1.5
            else:
                neg.append(f"Slow pharma growth: {r3:.1f}% (<5%)")

        p3 = metrics.profit_3y_cagr
        if p3 is not None:
            if p3 >= 18:
                score += 3.0; pos.append(f"Strong earnings CAGR: {p3:.1f}%")
            elif p3 >= 10:
                score += 1.5
            elif p3 < 0:
                neg.append(f"Declining profits: {p3:.1f}%")

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
            if roce >= 20:
                score += 4.0; pos.append(f"Strong ROCE: {roce:.1f}%")
            elif roce >= 15:
                score += 2.5; pos.append(f"Healthy ROCE: {roce:.1f}%")
            elif roce < 10:
                neg.append(f"Weak ROCE: {roce:.1f}%")

        margin = metrics.operating_margin
        if margin is not None:
            if margin >= 25:
                score += 4.0; pos.append(f"Excellent operating margin: {margin:.1f}% — strong formulation mix")
            elif margin >= 18:
                score += 2.5; pos.append(f"Good margin: {margin:.1f}%")
            elif margin >= 12:
                score += 0.5
            else:
                neg.append(f"Weak pharma margin: {margin:.1f}% (<12%)")

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
            if pe < 25:
                score += 5.0; pos.append(f"Attractive pharma valuation: PE {pe:.1f}x")
            elif pe < 38:
                score += 3.5; pos.append(f"Fair pharma PE: {pe:.1f}x")
            elif pe < 55:
                score += 1.5; pos.append(f"Premium pharma valuation: PE {pe:.1f}x")
            else:
                neg.append(f"Expensive pharma valuation: PE {pe:.1f}x (>55x)")

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
        pos, neg = [], []
        score = 0.0

        de = metrics.debt_to_equity
        if de is not None:
            if de < 0.3:
                score += 5.0; pos.append(f"Very low debt: D/E {de:.2f}")
            elif de < 0.8:
                score += 3.0
            elif de > 1.5:
                neg.append(f"High debt for pharma: D/E {de:.2f}")

        cr = metrics.current_ratio
        if cr is not None:
            if cr >= 2.0:
                score += 3.0; pos.append(f"Strong liquidity: Current Ratio {cr:.2f}x")
            elif cr >= 1.5:
                score += 1.5
            elif cr < 1.0:
                neg.append(f"Liquidity concern: CR {cr:.2f}x")

        raw = min(10.0, score * 10 / 8.0)
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
                score += 5.0; pos.append(f"High promoter holding: {promo:.1f}%")
            elif promo >= 40:
                score += 3.0
            elif promo < 25:
                neg.append(f"Low promoter holding: {promo:.1f}%")

        pledge = metrics.promoter_pledge_pct
        if pledge is not None:
            if pledge == 0:
                score += 3.0; pos.append("No promoter pledge")
            elif pledge > 15:
                neg.append(f"Promoter pledge risk: {pledge:.1f}%")

        change = metrics.promoter_change_qoq
        if change is not None and change > 0.5:
            score += 2.0; pos.append(f"Promoter buying: +{change:.2f}%")
        elif change is not None and change < -1.0:
            neg.append(f"Promoter selling: {change:.2f}%")

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
