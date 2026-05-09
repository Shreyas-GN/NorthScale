# SCRAPING_STRATEGY.md

# AI Investment Research Terminal

Data Ingestion & Scraping Architecture

Version: 0.1
Primary Markets: NSE / BSE
Architecture Style: Background-Oriented Financial Data Ingestion

---

# 1. Scraping Philosophy

The scraping system must prioritize:

* reliability
* deterministic consistency
* normalized financial truth
* freshness
* fault tolerance
* auditability
* low-latency retrieval
* source redundancy

The ingestion layer should behave like:

> "A financial intelligence ingestion pipeline."

NOT:

* a fragile scraping script
* request-time scraping logic
* uncontrolled crawler architecture

---

# 2. Core Principles

# Background-Oriented Architecture

Financial data MUST be:

* scraped asynchronously
* normalized before usage
* cached before user access

The frontend should NEVER:

* trigger direct scraping
* wait for live scraping
* depend on blocking ingestion

---

# Deterministic Financial Truth

All recommendation logic depends on normalized financial datasets, validated financial metrics, and reproducible ingestion pipelines.

The ingestion layer is mission-critical.

---

# Multi-Source Validation

No single source should be treated as permanently reliable, authoritative forever, or failure-proof.

The system must support: source fallback, cross-source validation, and freshness scoring.

---

# 3. Supported Data Sources

# Primary Sources

| Source       | Purpose                    |
| ------------ | -------------------------- |
| NSE India    | exchange metadata, filings |
| BSE India    | exchange metadata          |
| Screener.in  | financial ratios           |
| Moneycontrol | ownership, metrics         |
| Tickertape   | market metrics             |
| Trendlyne    | trend intelligence         |

# Future Sources

* Tijori Finance
* ValueResearch
* annual reports
* earnings transcripts
* investor presentations

---

# 4. Source Responsibility Mapping

## NSE India

Responsible for: official exchange data, company filings, corporate actions, listing metadata.

Priority: HIGH

## BSE India

Responsible for: secondary exchange validation, listing verification, fallback exchange data.

Priority: MEDIUM

## Screener.in

Responsible for: ratios, financial statements, profitability metrics, valuation metrics.

Priority: VERY HIGH

## Moneycontrol

Responsible for: ownership patterns, news metadata, valuation support, financial summaries.

Priority: HIGH

## Tickertape

Responsible for: supplemental metrics, factor-based signals, quick overview metrics.

Priority: MEDIUM

## Trendlyne

Responsible for: trend intelligence, ownership movement, analyst-like insights.

Priority: LOW-MEDIUM

---

# 5. Ingestion Architecture

# Core Pipeline

```txt
Raw Source Fetch
        ↓
Validation Layer
        ↓
Normalization Layer
        ↓
Financial Snapshot Builder
        ↓
Deterministic Signal Engine
        ↓
Recommendation Engine
        ↓
AI Narrative Layer
        ↓
Cache Layer
        ↓
API Delivery
```

---

# 6. Scraping Modes

## Scheduled Scraping

Primary ingestion strategy. Runs periodically, asynchronously, in background workers.

## Trigger-Based Scraping

Triggered when: stale data detected, earnings released, ownership changes occur, recommendation invalidated.

## Manual Refresh

Optional force stock refresh / re-analysis workflows. Must still use queue system — avoid direct synchronous scraping.

---

# 7. Scraping Cadence

| Data Type                   | Frequency     |
| --------------------------- | ------------- |
| Price Data                  | Daily         |
| Financial Statements        | Quarterly     |
| Ownership Data              | Quarterly     |
| Recommendation Regeneration | Daily         |
| AI Theses                   | Trigger-Based |
| Sector Metrics              | Weekly        |

---

# 8. Freshness Philosophy

# Data Freshness Levels

| Freshness | Meaning            |
| --------- | ------------------ |
| HIGH      | recently validated |
| MEDIUM    | slightly stale     |
| LOW       | aging but usable   |
| STALE     | fallback-only      |

# Freshness Rules

The API should: prefer stale data over total failure, expose freshness metadata, and allow graceful degradation.

---

# 9. Normalization Layer

All external data MUST normalize into: internal schemas, deterministic field naming, and validated formats.

# Example

External source:

```json
{
  "returnOnEquity": 18
}
```

Internal normalized schema:

```json
{
  "roe": 18
}
```

# Normalization Rules

Always: standardize field names, percentages, currencies, and date formats.

Never: expose raw external structures internally.

---

# 10. Validation Layer

Every ingestion cycle must validate:

* numeric ranges
* missing fields
* impossible values
* timestamp consistency
* schema integrity

# Example Invalid Data

Reject: negative market cap, impossible ROE, malformed financial statements.

# Cross-Source Validation

Compare ratios, market cap, and ownership values across multiple providers.

---

# 11. Retry Strategy

External sources WILL fail. The ingestion system must retry intelligently, avoid source overload, and preserve cached results.

| Failure Type       | Strategy            |
| ------------------ | ------------------- |
| Timeout            | retry               |
| Rate limit         | exponential backoff |
| Parsing failure    | alternate parser    |
| Source unavailable | fallback source     |

# Retry Limits

* max retries: 3
* exponential delay
* circuit breaker support

---

# 12. Anti-Ban Strategy

Avoid: aggressive scraping, synchronized requests, suspicious traffic patterns.

Required protections:

* randomized intervals
* rotating user agents
* request throttling
* caching
* staggered scheduling

Never: scrape aggressively during market hours, spam identical endpoints, or trigger large burst requests.

---

# 13. Queue System

# Recommended Stack

Celery + Redis (Alternative: BullMQ)

# Queue Responsibilities

Queues handle: scraping, retries, AI generation, recommendation refresh, ownership refresh.

# Queue Priority Levels

| Priority | Purpose                |
| -------- | ---------------------- |
| HIGH     | active stock analysis  |
| MEDIUM   | recommendation refresh |
| LOW      | historical backfill    |

---

# 14. Caching Strategy

Cache: stock snapshots, AI theses, recommendation outputs, normalized financial data.

Use: Redis

# Cache Invalidation

Invalidate when: new financials detected, ownership changes detected, or recommendation regenerated.

---

# 15. Historical Snapshot Strategy

NEVER overwrite historical truth.

Always: append snapshots, preserve recommendation history, preserve ownership history, preserve AI thesis history.

Historical data enables: thesis evolution, recommendation replay, confidence tracking, and historical comparison.

---

# 16. Failure Handling

On source failure:

* fallback to cached data
* fallback to secondary source
* expose stale status
* continue partial analysis if possible

NEVER: block frontend entirely, delete previous valid data, or return hallucinated metrics.

---

# 17. Observability & Monitoring

Track: scraping failures, retry counts, stale data frequency, parsing failures, latency, and source reliability.

| Metric              | Purpose               |
| ------------------- | --------------------- |
| scrape_success_rate | source health         |
| retry_frequency     | instability detection |
| freshness_score     | data quality          |
| parse_failure_rate  | parser quality        |

---

# 18. AI Compatibility Rules

The ingestion layer must provide: validated structured JSON, deterministic signals, normalized ratios, and freshness metadata.

The AI layer must NEVER: consume raw HTML, consume malformed datasets, or infer missing financial truth.

---

# 19. Future Expansion

* earnings transcript ingestion
* annual report parsing
* semantic filing extraction
* vector embeddings
* autonomous monitoring agents
* event-driven recommendation refresh

---

# 20. Long-Term Vision

The ingestion layer should evolve into:

> "A continuously updating institutional financial intelligence pipeline."

Supporting deterministic investing workflows, AI-native analysis, historical thesis evolution, explainable recommendations, and autonomous portfolio monitoring.
