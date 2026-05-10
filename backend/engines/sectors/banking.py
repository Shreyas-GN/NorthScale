"""
engines/sectors/banking.py

Banking Sector Scoring Engine.

KPI priorities (banking-specific):
  - CASA Ratio: Low-cost deposit franchise quality
  - GNPA/NNPA: Asset quality — the single biggest risk
  - NIM (Net Interest Margin): Core profitability
  - CAR (Capital Adequacy Ratio): Regulatory health
  - Valuation: P/B is the primary banking valuation metric

Sector-specific valuation interpretation:
  - P/E is less relevant for banks (use P/B and P/ABV)
  - P/B < 1.0: Distressed or value
  - P/B 1.0–2.0: Fairly valued
  - P/B 2.0–3.5: Premium franchise
  - P/B > 4.0: Exceptional quality or expensive
"""

from __future__ import annotations

from engines.models import CategoryScore, FinancialMetricsInput
from engines.sectors.base import BaseSectorScorer


class BankingScorer(BaseSectorScorer):
    sector_name = "Banking"
    sector_slug = "banking"

    WEIGHTS = {
        "growth": 0.15,           # Growth matters but less than quality
        "profitability": 0.30,    # NIM + GNPA are the core
        "valuation": 0.20,
        "financial_health": 0.25,  # Leverage is structural for banks — CAR matters
        "ownership": 0.10,
    }

    def score_growth(self, metrics: FinancialMetricsInput) -> CategoryScore:
        pos, neg = [], []
        score = 0.0

        r3 = metrics.revenue_3y_cagr
        if r3 is not None:
            if r3 >= 18:
                score += 5.0; pos.append(f"Strong loan book growth: {r3:.1f}% 3Y CAGR")
            elif r3 >= 12:
                score += 3.0; pos.append(f"Healthy growth: {r3:.1f}% 3Y CAGR")
            elif r3 >= 8:
                score += 1.5
            elif r3 < 5:
                neg.append(f"Stagnant growth: {r3:.1f}% 3Y CAGR")

        p3 = metrics.profit_3y_cagr
        if p3 is not None:
            if p3 >= 20:
                score += 4.0; pos.append(f"Strong profit CAGR: {p3:.1f}%")
            elif p3 >= 12:
                score += 2.0; pos.append(f"Good profit growth: {p3:.1f}%")
            elif p3 < 0:
                neg.append(f"Negative profit growth: {p3:.1f}%")

        raw = min(10.0, score * 10 / 9.0)
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
        """Core banking profitability — NIM, GNPA, CASA are the key levers."""
        pos, neg = [], []
        score = 0.0

        nim = metrics.nim
        if nim is not None:
            if nim >= 4.0:
                score += 4.0; pos.append(f"Excellent NIM: {nim:.2f}% (>4.0%)")
            elif nim >= 3.0:
                score += 3.0; pos.append(f"Healthy NIM: {nim:.2f}% (>3.0%)")
            elif nim >= 2.0:
                score += 1.0; pos.append(f"Moderate NIM: {nim:.2f}%")
            else:
                neg.append(f"Weak NIM: {nim:.2f}% (<2.0%)")

        gnpa = metrics.gnpa_ratio
        if gnpa is not None:
            if gnpa < 1.0:
                score += 5.0; pos.append(f"Best-in-class asset quality: GNPA {gnpa:.2f}%")
            elif gnpa < 2.0:
                score += 3.5; pos.append(f"Strong asset quality: GNPA {gnpa:.2f}%")
            elif gnpa < 3.5:
                score += 1.5; pos.append(f"Acceptable GNPA: {gnpa:.2f}%")
            elif gnpa < 5.0:
                score += 0.5; neg.append(f"Elevated GNPA: {gnpa:.2f}%")
            else:
                neg.append(f"High NPA risk: GNPA {gnpa:.2f}% (>5%)")

        casa = metrics.casa_ratio
        if casa is not None:
            if casa >= 45:
                score += 3.0; pos.append(f"Excellent CASA franchise: {casa:.1f}%")
            elif casa >= 35:
                score += 1.5; pos.append(f"Good CASA ratio: {casa:.1f}%")
            elif casa < 25:
                neg.append(f"Weak CASA ratio: {casa:.1f}%")

        raw = min(10.0, score * 10 / 12.0)
        weight = self.WEIGHTS["profitability"]
        return CategoryScore(
            category="profitability",
            raw_score=round(raw, 2),
            weight=weight,
            weighted_contribution=round(raw * weight, 4),
            positive_signals=pos,
            negative_signals=neg,
            data_available=metrics.nim is not None or metrics.gnpa_ratio is not None,
        )

    def score_valuation(self, metrics: FinancialMetricsInput) -> CategoryScore:
        """Banking valuation is P/B-driven, not P/E-driven."""
        pos, neg = [], []
        score = 0.0

        pb = metrics.pb_ratio
        if pb is not None:
            if pb < 1.0:
                score += 5.0; pos.append(f"Deeply attractive bank valuation: P/B {pb:.2f}x")
            elif pb < 1.8:
                score += 4.0; pos.append(f"Attractive bank valuation: P/B {pb:.2f}x")
            elif pb < 2.5:
                score += 2.5; pos.append(f"Fair bank valuation: P/B {pb:.2f}x")
            elif pb < 3.5:
                score += 1.0; neg.append(f"Premium banking valuation: P/B {pb:.2f}x")
            else:
                neg.append(f"Expensive banking valuation: P/B {pb:.2f}x (>3.5x)")

        pe = metrics.pe_ratio
        if pe is not None and pe > 0:
            if pe < 12:
                score += 3.0; pos.append(f"Low PE for banking: {pe:.1f}x")
            elif pe < 18:
                score += 1.5; pos.append(f"Moderate PE: {pe:.1f}x")
            elif pe > 28:
                neg.append(f"High PE for banking: {pe:.1f}x")

        raw = min(10.0, score * 10 / 8.0)
        weight = self.WEIGHTS["valuation"]
        return CategoryScore(
            category="valuation",
            raw_score=round(raw, 2),
            weight=weight,
            weighted_contribution=round(raw * weight, 4),
            positive_signals=pos,
            negative_signals=neg,
            data_available=metrics.pb_ratio is not None,
        )

    def score_financial_health(self, metrics: FinancialMetricsInput) -> CategoryScore:
        """Banking health = CAR, NNPA, and leverage context."""
        pos, neg = [], []
        score = 0.0

        car = metrics.car_ratio
        if car is not None:
            if car >= 18:
                score += 5.0; pos.append(f"Well-capitalised: CAR {car:.1f}% (>18%)")
            elif car >= 15:
                score += 3.0; pos.append(f"Adequately capitalised: CAR {car:.1f}%")
            elif car >= 12:
                score += 1.5
            else:
                neg.append(f"Undercapitalised risk: CAR {car:.1f}% (<12%)")

        nnpa = metrics.nnpa_ratio
        if nnpa is not None:
            if nnpa < 0.5:
                score += 4.0; pos.append(f"Excellent net NPA: {nnpa:.2f}%")
            elif nnpa < 1.5:
                score += 2.5; pos.append(f"Good net NPA: {nnpa:.2f}%")
            elif nnpa > 3.0:
                neg.append(f"High net NPA: {nnpa:.2f}%")

        raw = min(10.0, score * 10 / 9.0)
        weight = self.WEIGHTS["financial_health"]
        return CategoryScore(
            category="financial_health",
            raw_score=round(raw, 2),
            weight=weight,
            weighted_contribution=round(raw * weight, 4),
            positive_signals=pos,
            negative_signals=neg,
            data_available=metrics.car_ratio is not None or metrics.nnpa_ratio is not None,
        )

    def score_ownership(self, metrics: FinancialMetricsInput) -> CategoryScore:
        pos, neg = [], []
        score = 0.0

        promo = metrics.promoter_holding
        if promo is not None:
            if promo >= 50:
                score += 4.0; pos.append(f"High promoter ownership: {promo:.1f}%")
            elif promo >= 30:
                score += 2.5; pos.append(f"Reasonable promoter holding: {promo:.1f}%")
            elif promo < 15:
                neg.append(f"Very low promoter holding: {promo:.1f}%")

        fii = metrics.fii_holding
        if fii is not None and fii >= 20:
            score += 3.0; pos.append(f"Strong FII confidence: {fii:.1f}%")
        elif fii is not None and fii >= 10:
            score += 1.5

        change = metrics.promoter_change_qoq
        if change is not None and change > 0.5:
            score += 2.0; pos.append(f"Promoter increasing stake: +{change:.2f}%")
        elif change is not None and change < -1.5:
            neg.append(f"Promoter reducing stake: {change:.2f}%")

        raw = min(10.0, score * 10 / 9.0)
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
