import os

BASE = r"c:\Users\Shreyas Hegde\Desktop\Northscale\NorthScale\backend\engines"

ratios_profitability = """from typing import Optional

def calculate_roe(net_profit: Optional[float], equity: Optional[float]) -> Optional[float]:
    if net_profit is None or equity is None or equity <= 0: return None
    return (net_profit / equity) * 100

def calculate_roce(ebit: Optional[float], capital_employed: Optional[float]) -> Optional[float]:
    if ebit is None or capital_employed is None or capital_employed <= 0: return None
    return (ebit / capital_employed) * 100

def calculate_operating_margin(op_profit: Optional[float], revenue: Optional[float]) -> Optional[float]:
    if op_profit is None or revenue is None or revenue <= 0: return None
    return (op_profit / revenue) * 100

def calculate_net_margin(net_profit: Optional[float], revenue: Optional[float]) -> Optional[float]:
    if net_profit is None or revenue is None or revenue <= 0: return None
    return (net_profit / revenue) * 100
"""

ratios_valuation = """from typing import Optional

def calculate_pe(price: Optional[float], eps: Optional[float]) -> Optional[float]:
    if price is None or eps is None or eps <= 0: return None
    return price / eps

def calculate_pb(price: Optional[float], bvps: Optional[float]) -> Optional[float]:
    if price is None or bvps is None or bvps <= 0: return None
    return price / bvps

def calculate_ev_ebitda(ev: Optional[float], ebitda: Optional[float]) -> Optional[float]:
    if ev is None or ebitda is None or ebitda <= 0: return None
    return ev / ebitda
"""

ratios_growth = """from typing import Optional

def calculate_cagr(start_value: Optional[float], end_value: Optional[float], years: int) -> Optional[float]:
    if start_value is None or end_value is None or years <= 0 or start_value <= 0: return None
    return ((end_value / start_value) ** (1 / years) - 1) * 100
"""

ratios_financial_health = """from typing import Optional

def calculate_debt_equity(total_debt: Optional[float], total_equity: Optional[float]) -> Optional[float]:
    if total_debt is None or total_equity is None or total_equity <= 0: return None
    return total_debt / total_equity

def calculate_fcf_quality(fcf: Optional[float], net_profit: Optional[float]) -> Optional[float]:
    if fcf is None or net_profit is None or net_profit <= 0: return None
    return fcf / net_profit
"""

ratios_ownership = """from typing import Optional

def calculate_promoter_holding_trend(current: Optional[float], previous: Optional[float]) -> Optional[float]:
    if current is None or previous is None: return None
    return current - previous
"""

with open(os.path.join(BASE, "ratios", "profitability.py"), "w") as f: f.write(ratios_profitability)
with open(os.path.join(BASE, "ratios", "valuation.py"), "w") as f: f.write(ratios_valuation)
with open(os.path.join(BASE, "ratios", "growth.py"), "w") as f: f.write(ratios_growth)
with open(os.path.join(BASE, "ratios", "financial_health.py"), "w") as f: f.write(ratios_financial_health)
with open(os.path.join(BASE, "ratios", "ownership.py"), "w") as f: f.write(ratios_ownership)
