import os

BASE = r"c:\Users\Shreyas Hegde\Desktop\Northscale\NorthScale\backend\engines"

sector_base = """from typing import Dict, Any, Optional

class SectorScorer:
    def __init__(self, name: str):
        self.name = name

    def score(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Must implement score logic")
"""

sector_it = """from typing import Dict, Any
from .base import SectorScorer

class ITScorer(SectorScorer):
    def __init__(self):
        super().__init__("IT")

    def score(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        factors = []
        
        roe = metrics.get('roe')
        if roe and roe > 20:
            score += 2
            factors.append("Strong ROE (>20%)")
            
        growth = metrics.get('revenue_3y_cagr')
        if growth and growth > 15:
            score += 3
            factors.append("High Revenue CAGR (>15%)")
            
        pe = metrics.get('pe_ratio')
        if pe and pe < 30:
            score += 2
            factors.append("Reasonable valuation (PE < 30)")
            
        return {
            "score": score,
            "max_score": 7.0,
            "normalized_score": min(10.0, (score / 7.0) * 10),
            "positive_signals": factors,
            "negative_signals": [],
            "risk_summary": "Standard IT execution risks."
        }
"""

sector_banking = """from typing import Dict, Any
from .base import SectorScorer

class BankingScorer(SectorScorer):
    def __init__(self):
        super().__init__("BANKING")

    def score(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        factors = []
        risks = []
        
        casa = metrics.get('casa_ratio')
        if casa and casa > 40:
            score += 3
            factors.append("Strong CASA ratio (>40%)")
        elif casa and casa < 30:
            risks.append("Weak CASA ratio (<30%)")
            
        gnpa = metrics.get('gnpa_ratio')
        if gnpa and gnpa < 1.5:
            score += 3
            factors.append("Excellent Asset Quality (GNPA < 1.5%)")
        elif gnpa and gnpa > 3.0:
            risks.append("Asset Quality Concerns (GNPA > 3%)")
            
        nim = metrics.get('nim')
        if nim and nim > 3.5:
            score += 2
            factors.append("Healthy NIM (>3.5%)")
            
        pb = metrics.get('pb_ratio')
        if pb and pb < 2.0:
            score += 2
            factors.append("Attractive valuation (P/B < 2.0)")
            
        return {
            "score": score,
            "max_score": 10.0,
            "normalized_score": min(10.0, (score / 10.0) * 10),
            "positive_signals": factors,
            "negative_signals": risks,
            "risk_summary": "Monitored NPA and credit cycle risks."
        }
"""

sector_fmcg = """from typing import Dict, Any
from .base import SectorScorer

class FMCGScorer(SectorScorer):
    def __init__(self):
        super().__init__("FMCG")

    def score(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        factors = []
        
        roce = metrics.get('roce')
        if roce and roce > 30:
            score += 4
            factors.append("Exceptional ROCE (>30%)")
            
        pe = metrics.get('pe_ratio')
        if pe and pe < 45:
            score += 2
            factors.append("Reasonable valuation for FMCG")
            
        margin = metrics.get('operating_margin')
        if margin and margin > 20:
            score += 2
            factors.append("Strong operating margins")
            
        return {
            "score": score,
            "max_score": 8.0,
            "normalized_score": min(10.0, (score / 8.0) * 10),
            "positive_signals": factors,
            "negative_signals": [],
            "risk_summary": "Volume growth and raw material inflation risks."
        }
"""

sector_pharma = """from typing import Dict, Any
from .base import SectorScorer

class PharmaScorer(SectorScorer):
    def __init__(self):
        super().__init__("PHARMA")

    def score(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        factors = []
        
        roce = metrics.get('roce')
        if roce and roce > 15:
            score += 2
            factors.append("Healthy ROCE (>15%)")
            
        margin = metrics.get('operating_margin')
        if margin and margin > 20:
            score += 2
            factors.append("Strong operating margins")
            
        revenue_growth = metrics.get('revenue_3y_cagr')
        if revenue_growth and revenue_growth > 10:
            score += 2
            factors.append("Consistent revenue growth")
            
        return {
            "score": score,
            "max_score": 6.0,
            "normalized_score": min(10.0, (score / 6.0) * 10),
            "positive_signals": factors,
            "negative_signals": [],
            "risk_summary": "Regulatory and USFDA compliance risks."
        }
"""

sector_infra = """from typing import Dict, Any
from .base import SectorScorer

class InfraScorer(SectorScorer):
    def __init__(self):
        super().__init__("INFRASTRUCTURE")

    def score(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        score = 0.0
        factors = []
        risks = []
        
        debt_equity = metrics.get('debt_to_equity')
        if debt_equity and debt_equity < 1.0:
            score += 3
            factors.append("Conservative leverage (D/E < 1.0)")
        elif debt_equity and debt_equity > 2.0:
            risks.append("High leverage risk (D/E > 2.0)")
            
        interest_cov = metrics.get('interest_coverage')
        if interest_cov and interest_cov > 3.0:
            score += 2
            factors.append("Comfortable interest coverage (> 3.0x)")
            
        roce = metrics.get('roce')
        if roce and roce > 12:
            score += 2
            factors.append("Acceptable ROCE for infra (>12%)")
            
        return {
            "score": score,
            "max_score": 7.0,
            "normalized_score": min(10.0, (score / 7.0) * 10),
            "positive_signals": factors,
            "negative_signals": risks,
            "risk_summary": "Execution delays and working capital intensity."
        }
"""

with open(os.path.join(BASE, "sectors", "base.py"), "w") as f: f.write(sector_base)
with open(os.path.join(BASE, "sectors", "it.py"), "w") as f: f.write(sector_it)
with open(os.path.join(BASE, "sectors", "banking.py"), "w") as f: f.write(sector_banking)
with open(os.path.join(BASE, "sectors", "fmcg.py"), "w") as f: f.write(sector_fmcg)
with open(os.path.join(BASE, "sectors", "pharma.py"), "w") as f: f.write(sector_pharma)
with open(os.path.join(BASE, "sectors", "infrastructure.py"), "w") as f: f.write(sector_infra)
