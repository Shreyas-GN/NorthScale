# SCORING_ENGINE.md

# AI Investment Research Terminal

Deterministic Financial Intelligence Engine

Version: 0.1
Architecture Style: Deterministic Scoring System
Primary Purpose: Explainable Investment Recommendation Generation

---

# 1. Scoring Engine Philosophy

The scoring engine is the:

> "deterministic brain of the platform."

It is responsible for:

* financial truth interpretation
* recommendation generation
* conviction scoring
* investment quality evaluation

The scoring system must prioritize:

* explainability
* auditability
* deterministic consistency
* sector-aware logic
* long-term investing quality
* reproducibility

---

# Core Principle

AI does NOT determine investment truth.

AI only:

* explains
* contextualizes
* narrates

The scoring engine determines:

* recommendation category
* conviction score
* financial quality assessment
* risk interpretation

---

# 2. Recommendation Philosophy

The system is designed for:

* long-term investing
* business quality analysis
* risk-aware investing
* institutional-style evaluation

The engine should NOT optimize for:

* momentum trading
* speculation
* meme stocks
* short-term volatility

---

# 3. Recommendation Categories

| Recommendation | Meaning                                    |
| -------------- | ------------------------------------------ |
| STRONG_BUY     | exceptional quality + attractive valuation |
| BUY            | strong long-term opportunity               |
| HOLD           | fairly valued / mixed signals              |
| WATCHLIST      | promising but insufficient conviction      |
| SELL           | weak fundamentals or elevated risk         |

---

# 4. Core Scoring Architecture

# Scoring Pipeline

```txt
Normalized Financial Data
        ↓
Sector Classification
        ↓
Metric Evaluation
        ↓
Weighted Scoring
        ↓
Risk Adjustments
        ↓
Conviction Calculation
        ↓
Recommendation Classification
        ↓
AI Narrative Layer
```

---

# 5. Weighted Scoring System

# Base Weighting Model

| Category          | Weight |
| ----------------- | ------ |
| Growth            | 25%    |
| Profitability     | 20%    |
| Valuation         | 20%    |
| Financial Health  | 20%    |
| Ownership Quality | 10%    |
| Risk Factors      | 5%     |

---

# Important Rule

Weights may vary by sector, business model, and capital intensity.

The engine must support sector-specific weighting overrides.

---

# 6. Growth Scoring

# Purpose

Evaluate business expansion quality, growth consistency, and scalability.

# Core Metrics

| Metric               | Importance |
| -------------------- | ---------- |
| Revenue CAGR         | HIGH       |
| Profit CAGR          | HIGH       |
| Earnings Consistency | HIGH       |
| Operating Leverage   | MEDIUM     |

# Philosophy

Prefer:

* steady compounding
* durable growth
* consistent execution

Avoid over-rewarding:

* unstable hypergrowth
* cyclical spikes

---

# 7. Profitability Scoring

# Purpose

Evaluate operational efficiency, capital efficiency, and margin quality.

# Core Metrics

| Metric           | Importance |
| ---------------- | ---------- |
| ROE              | HIGH       |
| ROCE             | VERY HIGH  |
| Operating Margin | HIGH       |
| Net Margin       | MEDIUM     |

# Philosophy

Strong businesses demonstrate high ROCE, margin consistency, and operational discipline.

---

# 8. Valuation Scoring

# Purpose

Determine relative attractiveness, valuation risk, and margin of safety.

# Core Metrics

| Metric                     | Importance |
| -------------------------- | ---------- |
| PE Ratio                   | HIGH       |
| PB Ratio                   | MEDIUM     |
| EV/EBITDA                  | HIGH       |
| Historical Valuation Range | VERY HIGH  |

# Important Rule

Valuation must ALWAYS be sector-aware, historically contextual, and business-model aware.

High PE may be acceptable for SaaS or premium compounders, but unacceptable for low-growth cyclicals.

---

# 9. Financial Health Scoring

# Purpose

Evaluate balance sheet quality, debt sustainability, and cash flow strength.

# Core Metrics

| Metric            | Importance |
| ----------------- | ---------- |
| Debt/Equity       | VERY HIGH  |
| Interest Coverage | HIGH       |
| Free Cash Flow    | HIGH       |
| Cash Conversion   | MEDIUM     |

# Philosophy

Prefer low leverage, strong cash generation, and resilient balance sheets.

---

# 10. Ownership Quality Scoring

# Purpose

Evaluate promoter conviction, institutional confidence, and ownership stability.

# Core Metrics

| Metric            | Importance |
| ----------------- | ---------- |
| Promoter Holding  | HIGH       |
| Promoter Increase | HIGH       |
| FII Trend         | MEDIUM     |
| DII Trend         | MEDIUM     |

# Philosophy

Prefer stable ownership, increasing promoter confidence, and healthy institutional participation.

---

# 11. Risk Scoring

# Purpose

Evaluate downside exposure, fragility, and uncertainty.

# Risk Categories

| Risk Type           | Importance |
| ------------------- | ---------- |
| Valuation Risk      | HIGH       |
| Debt Risk           | HIGH       |
| Governance Risk     | VERY HIGH  |
| Cyclical Risk       | MEDIUM     |
| Earnings Volatility | MEDIUM     |

# Important Rule

Risk scoring reduces conviction and recommendation quality even if growth appears strong.

---

# 12. Sector-Aware Intelligence

Different sectors require different KPIs, scoring thresholds, and valuation interpretation.

## Banking Sector

Prioritize: CASA, GNPA, NIM, credit quality

## FMCG Sector

Prioritize: pricing power, margin stability, distribution quality

## SaaS Sector

Prioritize: growth quality, retention, operating leverage

## Pharma Sector

Prioritize: approvals, pipeline strength, compliance quality

## Infrastructure Sector

Prioritize: debt quality, order book, execution consistency

---

# 13. Conviction Score System

# Scale: 1 → 10

| Score | Meaning     |
| ----- | ----------- |
| 9–10  | Exceptional |
| 7–8.9 | Strong      |
| 5–6.9 | Moderate    |
| 3–4.9 | Weak        |
| <3    | Poor        |

# Confidence Levels

| Confidence | Meaning                        |
| ---------- | ------------------------------ |
| VERY_HIGH  | highly consistent signals      |
| HIGH       | strong signals                 |
| MODERATE   | mixed signals                  |
| LOW        | unreliable or conflicting data |

---

# 14. Recommendation Thresholds

| Score Range | Recommendation |
| ----------- | -------------- |
| 8.5+        | STRONG_BUY     |
| 7–8.49      | BUY            |
| 5–6.99      | HOLD           |
| 3–4.99      | WATCHLIST      |
| <3          | SELL           |

Recommendation classification must also consider: risk penalties, governance concerns, sector conditions, and data quality.

---

# 15. Historical Comparison Logic

Track improving fundamentals, weakening quality, valuation expansion, and thesis deterioration.

Compare current metrics against historical averages, prior recommendations, and prior conviction scores.

---

# 16. Scoring Explainability

Every recommendation MUST explain:

* WHY recommendation exists
* WHICH metrics contributed
* WHICH risks reduced conviction
* WHY valuation matters

The engine must expose: weighted category scores, adjustment logic, risk penalties, and confidence rationale.

---

# 17. Data Quality Adjustments

Reduce confidence when:

* data freshness is weak
* financials are incomplete
* sources conflict
* sector classification uncertain

Low-quality data should reduce confidence and conviction — never silently pass.

---

# 18. Recommendation Auditability

Every recommendation must track:

* snapshot_date
* scoring_version
* source freshness
* sector profile
* weighted category scores

This enables: historical replay, deterministic verification, AI explanation consistency, and debugging.

---

# 19. Portfolio Intelligence Logic

The engine supports:

* concentration analysis
* sector overexposure
* weakening holdings
* valuation clustering
* conviction-weighted allocation

Portfolio risk signals include: excessive IT concentration, overvalued portfolio bias, weakening conviction trend.

---

# 20. AI Integration Rules

The AI layer receives ONLY:

* structured scoring outputs
* deterministic signals
* validated metrics
* confidence metadata

AI must NEVER override recommendation truth or invent scoring logic.

---

# 21. Future Expansion

* macroeconomic overlays
* factor investing
* cyclicality engines
* momentum overlays
* quality compounding models
* event-driven scoring
* autonomous monitoring agents

---

# 22. Long-Term Vision

The scoring engine should evolve into:

> "An explainable institutional-grade investment intelligence framework."

Supporting deterministic trust, AI-native workflows, portfolio intelligence, thesis evolution, historical replayability, and autonomous investment monitoring.
