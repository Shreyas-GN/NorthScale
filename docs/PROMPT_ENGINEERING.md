# PROMPT_ENGINEERING.md

# AI Investment Research Terminal

Prompt Engineering Architecture

Version: 0.1
Primary Model Provider: Groq
Primary Architecture: Deterministic + AI Hybrid System

---

# 1. Prompt Engineering Philosophy

The AI layer exists to:

* explain
* contextualize
* synthesize
* summarize
* reason narratively

The AI layer does NOT exist to:

* invent financial truth
* calculate ratios
* determine authoritative metrics
* hallucinate investment conclusions

---

# Core Principle

Financial truth must ALWAYS originate from:

* deterministic engines
* validated financial datasets
* normalized historical snapshots
* structured recommendation systems

AI is an interpretation layer — NOT a source of truth.

---

# 2. AI System Goals

The prompting system must optimize for:

* explainability
* institutional tone
* concise reasoning
* deterministic compatibility
* low hallucination risk
* structured outputs
* investment clarity
* calm narrative presentation

---

# 3. Model Provider Strategy

# Primary Provider

Groq

# Preferred Models

| Model               | Primary Purpose   |
| ------------------- | ----------------- |
| DeepSeek R1 Distill | reasoning         |
| Llama 3.3 70B       | narrative quality |
| Mixtral             | fast summaries    |
| Gemma variants      | lightweight tasks |

# Model Selection Philosophy

Model routing should optimize for: latency, reasoning quality, structured JSON reliability, inference cost, and output consistency.

---

# 4. Prompt Architecture

# Prompt Pipeline

```txt
Structured Financial Data
        ↓
Deterministic Signals
        ↓
Sector Context
        ↓
Prompt Builder
        ↓
Groq Inference
        ↓
Structured AI Output
        ↓
Validation Layer
        ↓
Frontend Rendering
```

# Prompt Composition Layers

Every prompt must contain:

1. System Context
2. Financial Data
3. Deterministic Signals
4. Sector Context
5. Recommendation Context
6. Output Rules
7. Forbidden Behaviors

---

# 5. System Prompt Philosophy

# Core Tone

The AI must sound:

* institutional
* analytical
* calm
* precise
* explainable
* objective

NOT:

* emotional
* sensational
* hype-driven
* speculative
* meme-oriented

# Example Tone

Good:

> "The company demonstrates improving profitability, although current valuation appears elevated relative to historical norms."

Bad:

> "This stock is going to explode."

---

# 6. Prompt Input Rules

# Allowed Inputs

AI may receive:

* normalized financial metrics
* deterministic scoring outputs
* valuation metrics
* ownership changes
* historical recommendation context
* sector metadata
* risk summaries

# Forbidden Inputs

AI must NEVER receive:

* raw HTML
* unvalidated scraped text
* malformed data
* incomplete financial payloads
* conflicting metrics

---

# 7. Prompt Structure Standards

# Standard Prompt Structure

```txt
SYSTEM CONTEXT
↓
STOCK CONTEXT
↓
FINANCIAL METRICS
↓
DETERMINISTIC SIGNALS
↓
RISK SIGNALS
↓
SECTOR CONTEXT
↓
OUTPUT FORMAT RULES
↓
FORBIDDEN BEHAVIOR RULES
```

---

# 8. Recommendation Explanation Prompt

# Purpose

Generate: recommendation explanation, investment reasoning, valuation interpretation, and risk framing.

# Required Inputs

* recommendation category
* conviction score
* valuation metrics
* profitability metrics
* growth metrics
* ownership signals
* sector benchmarks

# Expected Output

Must include:

* bullish factors
* bearish factors
* valuation context
* confidence explanation
* key risks

---

# 9. AI Thesis Prompt

# Purpose

Generate: narrative investment thesis, business quality summary, and long-term investment perspective.

# Tone Requirements

The thesis must feel: institutional, concise, nuanced, and evidence-backed.

Avoid: exaggerated optimism, aggressive bearishness, certainty language.

---

# 10. Risk Analysis Prompt

# Purpose

Generate: structured risk summaries, weakness analysis, and uncertainty framing.

# Risk Categories

Must evaluate:

* valuation risk
* debt risk
* cyclical risk
* governance risk
* growth slowdown risk

---

# 11. Portfolio Intelligence Prompt

# Purpose

Generate: portfolio concentration warnings, sector overexposure insights, weakening conviction insights, and diversification observations.

# Important Rule

Portfolio AI must NEVER encourage gambling, leverage, or speculative trading.

---

# 12. Sector-Aware Prompting

Different sectors require different language, different KPIs, and different valuation framing.

## Banking

Focus on: CASA, GNPA, NIM

## FMCG

Focus on: pricing power, brand strength, margin stability

## SaaS

Focus on: growth quality, retention, operating leverage

---

# 13. Structured Output Philosophy

AI outputs MUST be structured.

Preferred format: JSON-compatible responses with clearly segmented outputs.

# Required Sections

Every major AI output must contain:

* thesis_summary
* bullish_factors
* bearish_factors
* risk_summary
* valuation_summary
* confidence_explanation

---

# 14. Hallucination Prevention

AI must NEVER:

* invent metrics
* fabricate financial statements
* generate unsupported claims
* override deterministic scoring

Prompts must:

* explicitly forbid fabricated numbers
* require metric referencing
* require probabilistic language
* require uncertainty disclosure

---

# 15. Confidence Generation Rules

Confidence should reflect: data quality, metric consistency, sector predictability, and scoring clarity — NOT AI certainty.

# Allowed Confidence Levels

* VERY_HIGH
* HIGH
* MODERATE
* LOW

---

# 16. AI Safety Rules

# Forbidden Behaviors

AI must NEVER:

* guarantee returns
* provide certainty language
* simulate insider knowledge
* encourage reckless investing
* present unsupported predictions

# Forbidden Phrases

* "guaranteed returns"
* "will definitely rise"
* "certain winner"
* "risk-free"
* "massive breakout incoming"

---

# 17. Prompt Validation Layer

# Before Inference

Validate:

* schema integrity
* required metrics
* sector classification
* recommendation availability
* freshness metadata

# After Inference

Validate:

* structured format
* missing sections
* hallucinated numbers
* tone compliance
* recommendation consistency

---

# 18. AI Failure Handling

If AI fails:

* retry once
* fallback to deterministic summaries
* preserve frontend rendering
* expose degraded state gracefully

Never:

* block stock analysis entirely
* fabricate fallback outputs
* hide missing AI responses

---

# 19. Prompt Versioning Strategy

Every prompt must include:

* prompt_version
* model_name
* generated_at

This enables: AI auditability, regression analysis, prompt optimization, and reproducibility.

---

# 20. Latency Optimization

| Operation           | Target |
| ------------------- | ------ |
| Cached AI Analysis  | < 1.5s |
| Fresh AI Generation | < 3s   |
| AI Command Queries  | < 2s   |

---

# 21. AI Command Interface Prompting

# Supported Commands

* Analyze TCS
* Compare Infosys vs TCS
* Find undervalued pharma companies
* Show high ROCE companies

# Command Rules

Commands must: remain deterministic-compatible, avoid speculative discovery, and reference validated datasets.

---

# 22. Long-Term Prompt Engineering Vision

The prompting system should evolve into:

> "An institutional-grade financial reasoning framework."

Supporting: AI portfolio copilots, autonomous monitoring agents, filing intelligence, thesis evolution tracking, and semantic investment memory — while preserving explainability, deterministic trust, institutional tone, and low hallucination risk.
