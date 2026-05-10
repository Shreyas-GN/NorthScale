import os

BASE = r"c:\Users\Shreyas Hegde\Desktop\Northscale\NorthScale\backend\engines"

risk_logic = """from typing import Dict, Any, List

def calculate_leverage_risk(debt_equity: float, interest_coverage: float) -> Dict[str, Any]:
    risk_score = 0.0
    signals = []
    
    if debt_equity > 2.0:
        risk_score += 3.0
        signals.append("High leverage: D/E > 2.0")
    elif debt_equity > 1.0:
        risk_score += 1.0
        signals.append("Moderate leverage: D/E > 1.0")
        
    if interest_coverage < 2.0:
        risk_score += 4.0
        signals.append("Poor interest coverage < 2.0x")
        
    return {"risk_penalty": min(5.0, risk_score), "signals": signals}

def calculate_valuation_risk(pe_ratio: float, pb_ratio: float, sector: str) -> Dict[str, Any]:
    risk_score = 0.0
    signals = []
    
    if sector == "IT" and pe_ratio > 40:
        risk_score += 2.0
        signals.append("Elevated IT Valuation")
    elif sector == "FMCG" and pe_ratio > 70:
        risk_score += 2.0
        signals.append("Elevated FMCG Valuation")
    elif sector not in ["IT", "FMCG"] and pe_ratio > 35:
        risk_score += 3.0
        signals.append("Elevated General Valuation")
        
    if pb_ratio > 10:
        risk_score += 1.0
        signals.append("High P/B Ratio (> 10)")
        
    return {"risk_penalty": min(4.0, risk_score), "signals": signals}

def calculate_governance_risk(promoter_pledge_pct: float) -> Dict[str, Any]:
    risk_score = 0.0
    signals = []
    
    if promoter_pledge_pct > 25:
        risk_score += 5.0
        signals.append("Severe governance risk: High promoter pledge (>25%)")
    elif promoter_pledge_pct > 10:
        risk_score += 2.0
        signals.append("Moderate promoter pledge (>10%)")
        
    return {"risk_penalty": min(5.0, risk_score), "signals": signals}

def evaluate_total_risk(metrics: Dict[str, Any], sector: str) -> Dict[str, Any]:
    total_penalty = 0.0
    all_signals = []
    
    debt_eq = metrics.get('debt_to_equity')
    int_cov = metrics.get('interest_coverage')
    if debt_eq is not None and int_cov is not None:
        lev_risk = calculate_leverage_risk(debt_eq, int_cov)
        total_penalty += lev_risk["risk_penalty"]
        all_signals.extend(lev_risk["signals"])
        
    pe = metrics.get('pe_ratio')
    pb = metrics.get('pb_ratio')
    if pe is not None and pb is not None:
        val_risk = calculate_valuation_risk(pe, pb, sector)
        total_penalty += val_risk["risk_penalty"]
        all_signals.extend(val_risk["signals"])
        
    pledge = metrics.get('promoter_pledge_pct')
    if pledge is not None:
        gov_risk = calculate_governance_risk(pledge)
        total_penalty += gov_risk["risk_penalty"]
        all_signals.extend(gov_risk["signals"])
        
    return {
        "total_risk_penalty": min(10.0, total_penalty),
        "risk_signals": all_signals
    }
"""

recommendation_logic = """from typing import Dict, Any, List, Optional
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
"""

with open(os.path.join(BASE, "risk", "risk.py"), "w") as f: f.write(risk_logic)
with open(os.path.join(BASE, "recommendation", "recommendation.py"), "w") as f: f.write(recommendation_logic)
