"""
engines/sectors/fmcg.py

FMCG Sector Scoring Engine.

KPI priorities:
  - Pricing power and margin stability
  - Volume growth consistency
  - ROCE (strong for asset-light FMCG)
  - Distribution quality (approximated via revenue growth consistency)
  - Valuation: FMCG commands premium multiples

Sector-specific valuation interpretation:
  - FMCG justifies high PE due to compounding, brand moat, cash generation
  - PE < 35: Deep value for quality FMCG
  - PE 35–55: Fair value
  - PE 55–80: Premium
  - PE > 80: Very expensive, requires exceptional moat justification
"""

from __future__ import annotations

from engines.models import CategoryScore, FinancialMetricsInput
from engines.sectors.base import BaseSectorScorer


class FMCGScorer(BaseSectorScorer):
    sector_name = "FMCG"
    sector_slug = "fmcg"

    WEIGHTS = {
        "growth": 0.20,
        "profitability": 0.30,    # Margin quality is core for FMCG
        "valuation": 0.20,
        "financial_health": 0.20,  # Cash generation is key
        "ownership": 0.10,
    }

    def score_growth(self, metrics: FinancialMetricsInput) -> CategoryScore:
        pos, neg = [], []
        score = 0.0

        r3 = metrics.revenue_3y_cagr
        if r3 is not None:
            if r3 >= 15:
                score += 5.0; pos.append(f"Strong FMCG revenue growth: {r3:.1f}% 3Y CAGR")
            elif r3 >= 10:
                score += 3.5; pos.append(f"Steady FMCG growth: {r3:.1f}% 3Y CAGR")
            elif r3 >= 6:
                score += 1.5; pos.append(f"Moderate volume growth: {r3:.1f}%")
            else:
                neg.append(f"Below-average FMCG growth: {r3:.1f}% (<6%)")

        p3 = metrics.profit_3y_cagr
        if p3 is not None:
            if p3 >= 15:
                score += 3.0; pos.append(f"Strong earnings growth: {p3:.1f}%")
            elif p3 >= 10:
                score += 1.5
            elif p3 < 5:
                neg.append(f"Weak earnings growth: {p3:.1f}%")

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
            if roce >= 40:
                score += 5.0; pos.append(f"Exceptional ROCE: {roce:.1f}% — premium FMCG quality")
            elif roce >= 30:
                score += 4.0; pos.append(f"Excellent ROCE: {roce:.1f}%")
            elif roce >= 20:
                score += 2.5; pos.append(f"Good ROCE: {roce:.1f}%")
            elif roce < 12:
                neg.append(f"Weak ROCE for FMCG: {roce:.1f}%")

        margin = metrics.operating_margin
        if margin is not None:
            if margin >= 25:
                score += 4.0; pos.append(f"Strong operating margin: {margin:.1f}%")
            elif margin >= 18:
                score += 2.5; pos.append(f"Good operating margin: {margin:.1f}%")
            elif margin >= 12:
                score += 1.0
            else:
                neg.append(f"Weak FMCG margin: {margin:.1f}% (<12%)")

        raw = min(10.0, score * 10 / 9.0)
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
            if pe < 35:
                score += 5.0; pos.append(f"Attractive FMCG valuation: PE {pe:.1f}x (<35x)")
            elif pe < 50:
                score += 3.5; pos.append(f"Fair FMCG valuation: PE {pe:.1f}x")
            elif pe < 70:
                score += 1.5; pos.append(f"Premium FMCG multiple: PE {pe:.1f}x")
            elif pe < 90:
                score += 0.5; neg.append(f"Expensive FMCG valuation: PE {pe:.1f}x (>70x)")
            else:
                neg.append(f"Very expensive FMCG: PE {pe:.1f}x (>90x)")

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
            if de < 0.1:
                score += 5.0; pos.append(f"Zero/negligible debt: D/E {de:.2f}")
            elif de < 0.5:
                score += 3.5; pos.append(f"Low debt: D/E {de:.2f}")
            elif de > 1.0:
                neg.append(f"Elevated debt for FMCG: D/E {de:.2f}")

        fcf = metrics.free_cash_flow
        net = metrics.net_profit_ttm
        if fcf is not None and net is not None and net > 0:
            fcf_quality = fcf / net
            if fcf_quality >= 0.9:
                score += 4.0; pos.append(f"Excellent cash conversion: FCF/PAT {fcf_quality:.2f}x")
            elif fcf_quality >= 0.7:
                score += 2.5
            elif fcf_quality < 0.4:
                neg.append(f"Weak cash conversion: {fcf_quality:.2f}x")

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
            if promo >= 65:
                score += 5.0; pos.append(f"Strong promoter backing: {promo:.1f}%")
            elif promo >= 50:
                score += 3.0
            elif promo < 30:
                neg.append(f"Low promoter holding: {promo:.1f}%")

        pledge = metrics.promoter_pledge_pct
        if pledge is not None:
            if pledge == 0:
                score += 3.0; pos.append("Zero promoter pledge")
            elif pledge > 10:
                neg.append(f"Promoter pledge concern: {pledge:.1f}%")

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
