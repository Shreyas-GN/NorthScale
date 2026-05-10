from typing import Dict, Any, List, Optional
from engines.sectors.base import SectorScorer
from engines.sectors.it import ITScorer
from engines.sectors.banking import BankingScorer
from engines.sectors.fmcg import FMCGScorer
from engines.sectors.pharma import PharmaScorer
from engines.sectors.infrastructure import InfraScorer
from engines.risk.risk import evaluate_total_risk

def get_sector_scorer(sector_slug: str) -> Optional[SectorScorer]:
    scorers = {
        "it": ITScorer(),
        "banking": BankingScorer(),
        "fmcg": FMCGScorer(),
        "pharma": PharmaScorer(),
        "infrastructure": InfraScorer()
    }
    return scorers.get(sector_slug.lower())

def determine_recommendation_classification(conviction_score: float) -> str:
    if conviction_score >= 8.5: return "STRONG_BUY"
    if conviction_score >= 7.0: return "BUY"
    if conviction_score >= 5.0: return "HOLD"
    if conviction_score >= 3.0: return "WATCHLIST"
    return "SELL"

def determine_confidence_level(data_freshness: int, completeness: float) -> str:
    if data_freshness > 90 and completeness > 0.9: return "VERY_HIGH"
    if data_freshness > 70 and completeness > 0.7: return "HIGH"
    if data_freshness > 50 and completeness > 0.5: return "MODERATE"
    return "LOW"

def generate_recommendation(stock_metrics: Dict[str, Any], sector_slug: str) -> Dict[str, Any]:
    sector_scorer = get_sector_scorer(sector_slug)
    
    sector_score_res = {}
    if sector_scorer:
        sector_score_res = sector_scorer.score(stock_metrics)
        
    base_score = sector_score_res.get("normalized_score", 5.0)
    
    risk_res = evaluate_total_risk(stock_metrics, sector_slug.upper())
    risk_penalty = risk_res["total_risk_penalty"]
    
    conviction_score = max(0.0, min(10.0, base_score - (risk_penalty * 0.5)))
    
    recommendation = determine_recommendation_classification(conviction_score)
    
    freshness = stock_metrics.get("freshness_score", 100)
    # mock completeness for now based on key fields
    completeness = 1.0 if "pe_ratio" in stock_metrics and "roe" in stock_metrics else 0.5
    confidence = determine_confidence_level(freshness, completeness)
    
    return {
        "recommendation": recommendation,
        "conviction_score": round(conviction_score, 2),
        "confidence_level": confidence,
        "base_score": round(base_score, 2),
        "risk_penalty": round(risk_penalty, 2),
        "positive_signals": sector_score_res.get("positive_signals", []),
        "negative_signals": sector_score_res.get("negative_signals", []) + risk_res["risk_signals"],
        "sector_context": sector_score_res.get("risk_summary", "No sector context available.")
    }
