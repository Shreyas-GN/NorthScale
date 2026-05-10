"""
engines/sectors/it.py

IT Sector Scoring Engine.

KPI priorities:
  - Growth quality (revenue CAGR, margin expansion)
  - Capital efficiency (ROE, ROCE — asset-light model)
  - Valuation (PE < 40 attractive, > 55 expensive for IT)
  - Balance sheet (IT is typically debt-free / low debt)
  - Ownership (promoter conviction matters)

Sector-specific valuation interpretation:
  - IT commands premium multiples due to high margins and recurring revenue
  - PE < 30: Deep value for quality IT
  - PE 30–45: Fair value
  - PE 45–60: Premium (acceptable for hyper-growth IT)
  - PE > 60: Stretched — needs exceptional growth to justify
"""

from __future__ import annotations

from engines.models import CategoryScore, FinancialMetricsInput
from engines.sectors.base import BaseSectorScorer


class ITScorer(BaseSectorScorer):
    sector_name = "Information Technology"
    sector_slug = "it"

    WEIGHTS = {
        "growth": 0.30,        # Growth is paramount for IT
        "profitability": 0.25,  # Margins matter
        "valuation": 0.20,
        "financial_health": 0.15,  # Usually clean balance sheets
        "ownership": 0.10,
    }

    def score_growth(self, metrics: FinancialMetricsInput) -> CategoryScore:
        pos, neg = [], []
        score = 0.0

        r3 = metrics.revenue_3y_cagr
        if r3 is not None:
            if r3 >= 20:
                score += 5.0; pos.append(f"Strong revenue CAGR: {r3:.1f}% (>20%)")
            elif r3 >= 15:
                score += 4.0; pos.append(f"Healthy revenue CAGR: {r3:.1f}% (15–20%)")
            elif r3 >= 10:
                score += 2.5; pos.append(f"Moderate revenue CAGR: {r3:.1f}% (10–15%)")
            elif r3 >= 5:
                score += 1.0; neg.append(f"Weak revenue CAGR: {r3:.1f}% (5–10%)")
            else:
                neg.append(f"Poor revenue CAGR: {r3:.1f}% (<5%)")
        else:
            neg.append("Revenue CAGR data unavailable")

        p3 = metrics.profit_3y_cagr
        if p3 is not None:
            if p3 >= 20:
                score += 3.0; pos.append(f"Excellent profit CAGR: {p3:.1f}%")
            elif p3 >= 12:
                score += 2.0; pos.append(f"Good profit CAGR: {p3:.1f}%")
            elif p3 >= 5:
                score += 0.5
            else:
                neg.append(f"Weak profit CAGR: {p3:.1f}%")

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
            if roce >= 30:
                score += 4.0; pos.append(f"Exceptional ROCE: {roce:.1f}% (>30%)")
            elif roce >= 20:
                score += 3.0; pos.append(f"Strong ROCE: {roce:.1f}% (>20%)")
            elif roce >= 15:
                score += 1.5; pos.append(f"Moderate ROCE: {roce:.1f}% (>15%)")
            else:
                neg.append(f"Weak ROCE: {roce:.1f}% (<15%)")

        roe = metrics.roe
        if roe is not None:
            if roe >= 25:
                score += 3.0; pos.append(f"Strong ROE: {roe:.1f}% (>25%)")
            elif roe >= 18:
                score += 2.0; pos.append(f"Good ROE: {roe:.1f}%")
            elif roe >= 12:
                score += 0.5
            else:
                neg.append(f"Weak ROE: {roe:.1f}% (<12%)")

        margin = metrics.operating_margin
        if margin is not None:
            if margin >= 25:
                score += 2.0; pos.append(f"Excellent operating margin: {margin:.1f}%")
            elif margin >= 18:
                score += 1.0; pos.append(f"Good operating margin: {margin:.1f}%")
            elif margin < 12:
                neg.append(f"Low operating margin: {margin:.1f}% (<12%)")

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
            if pe < 25:
                score += 5.0; pos.append(f"Attractive IT valuation: PE {pe:.1f}x (<25x)")
            elif pe < 35:
                score += 4.0; pos.append(f"Fair IT valuation: PE {pe:.1f}x (<35x)")
            elif pe < 45:
                score += 2.5; pos.append(f"Moderate valuation: PE {pe:.1f}x (<45x)")
            elif pe < 60:
                score += 1.0; neg.append(f"Premium valuation: PE {pe:.1f}x (45–60x)")
            else:
                neg.append(f"Expensive valuation: PE {pe:.1f}x (>60x)")

        ev_ebitda = metrics.ev_to_ebitda
        if ev_ebitda is not None and ev_ebitda > 0:
            if ev_ebitda < 15:
                score += 3.0; pos.append(f"Attractive EV/EBITDA: {ev_ebitda:.1f}x")
            elif ev_ebitda < 25:
                score += 1.5; pos.append(f"Fair EV/EBITDA: {ev_ebitda:.1f}x")
            elif ev_ebitda > 40:
                neg.append(f"High EV/EBITDA: {ev_ebitda:.1f}x")

        raw = min(10.0, score * 10 / 8.0)
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
                score += 5.0; pos.append(f"Net cash / zero debt: D/E {de:.2f}")
            elif de < 0.5:
                score += 3.5; pos.append(f"Very low debt: D/E {de:.2f}")
            elif de < 1.0:
                score += 2.0; pos.append(f"Low debt: D/E {de:.2f}")
            elif de > 1.5:
                neg.append(f"Elevated debt for IT: D/E {de:.2f}")

        fcf = metrics.free_cash_flow
        net = metrics.net_profit_ttm
        if fcf is not None and net is not None and net > 0:
            fcf_quality = fcf / net
            if fcf_quality >= 1.0:
                score += 3.0; pos.append(f"Excellent FCF quality: {fcf_quality:.2f}x (FCF > Net Profit)")
            elif fcf_quality >= 0.7:
                score += 1.5; pos.append(f"Good FCF conversion: {fcf_quality:.2f}x")
            elif fcf_quality < 0.4:
                neg.append(f"Poor FCF conversion: {fcf_quality:.2f}x")

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
            if promo >= 60:
                score += 4.0; pos.append(f"High promoter conviction: {promo:.1f}%")
            elif promo >= 45:
                score += 2.5; pos.append(f"Healthy promoter holding: {promo:.1f}%")
            elif promo < 25:
                neg.append(f"Low promoter holding: {promo:.1f}%")

        pledge = metrics.promoter_pledge_pct
        if pledge is not None:
            if pledge == 0:
                score += 3.0; pos.append("Zero promoter pledge")
            elif pledge < 5:
                score += 1.5; pos.append(f"Minimal pledge: {pledge:.1f}%")
            elif pledge > 15:
                neg.append(f"Significant pledge: {pledge:.1f}%")

        change = metrics.promoter_change_qoq
        if change is not None and change > 0.5:
            score += 2.0; pos.append(f"Promoter increasing stake: +{change:.2f}%")
        elif change is not None and change < -1.0:
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
