"""
engines/models.py

Typed Pydantic models for all engine inputs and outputs.
All scoring, recommendation, and risk outputs must conform to these schemas.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RecommendationCategory(str, Enum):
    STRONG_BUY = "STRONG_BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    WATCHLIST = "WATCHLIST"
    SELL = "SELL"
    AVOID = "AVOID"


class ConfidenceLevel(str, Enum):
    VERY_HIGH = "VERY_HIGH"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"


class ConvictionTier(str, Enum):
    EXCEPTIONAL = "EXCEPTIONAL"
    STRONG = "STRONG"
    MODERATE = "MODERATE"
    WEAK = "WEAK"
    POOR = "POOR"


# ---------------------------------------------------------------------------
# Input model — raw financial metrics fed into the scoring pipeline
# ---------------------------------------------------------------------------

class FinancialMetricsInput(BaseModel):
    """
    Structured financial snapshot used as input to all scoring engines.
    Sourced from stock_financial_snapshots + stock_ownership_snapshots.
    """

    stock_id: str
    ticker: str
    sector_slug: str

    snapshot_date: date
    financial_snapshot_id: Optional[str] = None
    ownership_snapshot_id: Optional[str] = None

    # Profitability
    roe: Optional[float] = None
    roce: Optional[float] = None
    net_profit_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    gross_margin: Optional[float] = None
    ebitda_margin: Optional[float] = None

    # Growth
    revenue_1y_growth: Optional[float] = None
    revenue_3y_cagr: Optional[float] = None
    revenue_5y_cagr: Optional[float] = None
    profit_1y_growth: Optional[float] = None
    profit_3y_cagr: Optional[float] = None
    profit_5y_cagr: Optional[float] = None

    # Financial Health
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    interest_coverage: Optional[float] = None
    free_cash_flow: Optional[float] = None
    cash_and_equivalents: Optional[float] = None
    net_profit_ttm: Optional[float] = None

    # Valuation
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
    price_to_sales: Optional[float] = None
    cmp: Optional[float] = None
    market_cap: Optional[float] = None

    # Ownership
    promoter_holding: Optional[float] = None
    promoter_pledge_pct: Optional[float] = None
    fii_holding: Optional[float] = None
    dii_holding: Optional[float] = None
    promoter_change_qoq: Optional[float] = None
    fii_change_qoq: Optional[float] = None
    dii_change_qoq: Optional[float] = None

    # Banking-specific
    casa_ratio: Optional[float] = None
    gnpa_ratio: Optional[float] = None
    nnpa_ratio: Optional[float] = None
    nim: Optional[float] = None
    car_ratio: Optional[float] = None

    # Data quality
    freshness_score: int = Field(default=100, ge=0, le=100)
    data_source: str = "UNKNOWN"

    @field_validator("freshness_score")
    @classmethod
    def clamp_freshness(cls, v: int) -> int:
        return max(0, min(100, v))

    def completeness_ratio(self) -> float:
        """Returns fraction of key fields populated."""
        key_fields = [
            self.roe, self.roce, self.pe_ratio, self.pb_ratio,
            self.debt_to_equity, self.revenue_3y_cagr, self.profit_3y_cagr,
            self.operating_margin, self.promoter_holding, self.free_cash_flow,
        ]
        filled = sum(1 for f in key_fields if f is not None)
        return filled / len(key_fields)


# ---------------------------------------------------------------------------
# Ratio output models
# ---------------------------------------------------------------------------

class ProfitabilityRatios(BaseModel):
    roe: Optional[float] = None
    roce: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    ebitda_margin: Optional[float] = None


class ValuationRatios(BaseModel):
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    ev_to_ebitda: Optional[float] = None
    price_to_sales: Optional[float] = None


class GrowthRatios(BaseModel):
    revenue_1y_growth: Optional[float] = None
    revenue_3y_cagr: Optional[float] = None
    revenue_5y_cagr: Optional[float] = None
    profit_1y_growth: Optional[float] = None
    profit_3y_cagr: Optional[float] = None
    profit_5y_cagr: Optional[float] = None


class FinancialHealthRatios(BaseModel):
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    interest_coverage: Optional[float] = None
    fcf_quality: Optional[float] = None  # FCF / Net Profit


class OwnershipMetrics(BaseModel):
    promoter_holding: Optional[float] = None
    promoter_pledge_pct: Optional[float] = None
    promoter_change_qoq: Optional[float] = None
    fii_holding: Optional[float] = None
    fii_change_qoq: Optional[float] = None
    dii_holding: Optional[float] = None
    dii_change_qoq: Optional[float] = None


# ---------------------------------------------------------------------------
# Category score model (used inside composite scoring)
# ---------------------------------------------------------------------------

class CategoryScore(BaseModel):
    """
    Represents a scored category with weighted contribution and
    a full list of contributing factors for explainability.
    """
    category: str
    raw_score: float = Field(ge=0.0, le=10.0)
    weight: float = Field(ge=0.0, le=1.0)
    weighted_contribution: float  # raw_score * weight
    positive_signals: List[str] = Field(default_factory=list)
    negative_signals: List[str] = Field(default_factory=list)
    data_available: bool = True


# ---------------------------------------------------------------------------
# Risk output model
# ---------------------------------------------------------------------------

class RiskOutput(BaseModel):
    leverage_risk: float = Field(default=0.0, ge=0.0, le=10.0)
    valuation_risk: float = Field(default=0.0, ge=0.0, le=10.0)
    governance_risk: float = Field(default=0.0, ge=0.0, le=10.0)
    cyclicality_risk: float = Field(default=0.0, ge=0.0, le=10.0)
    earnings_volatility_risk: float = Field(default=0.0, ge=0.0, le=10.0)
    ownership_risk: float = Field(default=0.0, ge=0.0, le=10.0)

    total_risk_penalty: float = Field(default=0.0, ge=0.0, le=10.0)
    risk_signals: List[str] = Field(default_factory=list)

    @property
    def risk_level(self) -> str:
        if self.total_risk_penalty >= 7:
            return "CRITICAL"
        if self.total_risk_penalty >= 4:
            return "HIGH"
        if self.total_risk_penalty >= 2:
            return "MODERATE"
        return "LOW"


# ---------------------------------------------------------------------------
# Explainability output model
# ---------------------------------------------------------------------------

class ExplainabilityOutput(BaseModel):
    """
    Every recommendation must expose this full explainability record.
    No black-box outputs allowed.
    """
    category_scores: List[CategoryScore]
    risk_output: RiskOutput
    positive_signals: List[str] = Field(default_factory=list)
    negative_signals: List[str] = Field(default_factory=list)
    sector_context: str = ""
    confidence_reasoning: str = ""
    data_quality_note: Optional[str] = None

    @property
    def top_positives(self) -> List[str]:
        return self.positive_signals[:5]

    @property
    def top_negatives(self) -> List[str]:
        return self.negative_signals[:5]


# ---------------------------------------------------------------------------
# Conviction output model
# ---------------------------------------------------------------------------

class ConvictionOutput(BaseModel):
    conviction_score: float = Field(ge=0.0, le=10.0)
    conviction_tier: ConvictionTier
    confidence_level: ConfidenceLevel
    composite_score: float = Field(ge=0.0, le=10.0)
    risk_adjusted_score: float = Field(ge=0.0, le=10.0)

    @classmethod
    def from_score(cls, score: float, confidence: ConfidenceLevel, composite: float) -> "ConvictionOutput":
        if score >= 9.0:
            tier = ConvictionTier.EXCEPTIONAL
        elif score >= 7.0:
            tier = ConvictionTier.STRONG
        elif score >= 5.0:
            tier = ConvictionTier.MODERATE
        elif score >= 3.0:
            tier = ConvictionTier.WEAK
        else:
            tier = ConvictionTier.POOR
        return cls(
            conviction_score=score,
            conviction_tier=tier,
            confidence_level=confidence,
            composite_score=composite,
            risk_adjusted_score=score,
        )


# ---------------------------------------------------------------------------
# Full scoring pipeline output
# ---------------------------------------------------------------------------

class ScoringResult(BaseModel):
    """
    Complete output of the deterministic scoring pipeline for a single stock.
    This is the authoritative, auditable record persisted to the database.
    """
    stock_id: str
    ticker: str
    sector_slug: str
    snapshot_date: date

    recommendation: RecommendationCategory
    conviction: ConvictionOutput
    explainability: ExplainabilityOutput

    # Category scores (stored individually for DB)
    growth_score: Optional[float] = None
    profitability_score: Optional[float] = None
    valuation_score: Optional[float] = None
    financial_health_score: Optional[float] = None
    ownership_score: Optional[float] = None
    risk_score: Optional[float] = None
    composite_score: float

    financial_snapshot_id: Optional[str] = None
    ownership_snapshot_id: Optional[str] = None

    scoring_version: str = "1.0.0"
    generated_at: datetime = Field(default_factory=datetime.utcnow)
