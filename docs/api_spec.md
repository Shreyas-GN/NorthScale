# API_SPEC.md

# AI Investment Research Terminal

REST API Architecture Specification

Version: 0.1
Architecture Style: REST-First
API Style: Typed JSON APIs
Primary Backend: FastAPI
Primary Database: Supabase PostgreSQL

---

# 1. API Philosophy

The API layer must prioritize:

* deterministic consistency
* explainability
* predictable contracts
* typed responses
* auditability
* modularity
* future scalability

The API should behave like:

> "A financial intelligence service layer."

NOT:

* a thin frontend wrapper
* a loosely typed prototype API
* an AI-only gateway

---

# 2. Core API Principles

## Deterministic First

All recommendation truth must originate from: deterministic financial engines, validated financial datasets, and normalized historical snapshots.

AI APIs only provide: narrative synthesis, explainability, and contextual interpretation.

## Typed Response Architecture

Every response must: be strongly typed, follow consistent structures, and support predictable frontend rendering.

Responses must NEVER: change field names unpredictably, mix inconsistent schemas, or return malformed payloads.

## API Versioning

Current version: `/api/v1/`

Future: `/api/v2/`, `/api/v3/`

---

# 3. Base API Structure

```txt
/api/v1
    /stocks
    /analysis
    /recommendations
    /portfolio
    /watchlists
    /insights
    /alerts
    /search
    /ai
```

---

# 4. Response Standards

## Success Response Format

```json
{
  "success": true,
  "data": {},
  "meta": {}
}
```

## Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "DATA_FETCH_FAILED",
    "message": "Unable to fetch stock data",
    "details": null
  }
}
```

## Meta Object Standard

```json
{
  "cached": true,
  "generated_at": "2026-05-07T10:00:00Z",
  "data_freshness": "HIGH",
  "source_count": 4
}
```

---

# 5. Status Code Conventions

| Status Code | Meaning                   |
| ----------- | ------------------------- |
| 200         | Success                   |
| 201         | Resource created          |
| 400         | Validation error          |
| 401         | Unauthorized (future)     |
| 404         | Resource not found        |
| 409         | Conflict                  |
| 422         | Invalid financial payload |
| 429         | Rate limited              |
| 500         | Internal server error     |
| 503         | External data unavailable |

---

# 6. Pagination Standards

Cursor-based pagination preferred. Fallback: page-based.

```json
{
  "success": true,
  "data": [],
  "pagination": {
    "next_cursor": "abc123",
    "has_more": true
  }
}
```

Required for: insights, alerts, historical recommendations, historical theses.

---

# 7. Filtering & Sorting Standards

Common filters: `sector`, `market_cap`, `recommendation`, `valuation`, `conviction_score`, `exchange`, `risk_level`

Example: `/api/v1/stocks?sector=IT&recommendation=BUY`

Sorting: `?sort=conviction_score&order=desc`

---

# 8. Caching Philosophy

# Cache Durations

| Data Type           | Cache Duration |
| ------------------- | -------------- |
| Stock Analysis      | 15 min         |
| AI Thesis           | 30 min         |
| Portfolio Summary   | 5 min          |
| Financial Snapshots | 1 hour         |
| Ownership Data      | 1 day          |

Responses must expose:

```json
{
  "cached": true,
  "cache_age_seconds": 180
}
```

---

# 9. Stale Data Handling

The API should prefer slightly stale data OVER request failure.

If fresh ingestion fails: return latest valid snapshot, mark response as stale, expose freshness metadata.

```json
{
  "data_freshness": "STALE"
}
```

---

# 10. Stock APIs

## GET /api/v1/stocks

Returns stock registry list.

Query parameters: `search`, `sector`, `exchange`, `market_cap`

```json
{
  "success": true,
  "data": [
    {
      "ticker": "TCS",
      "company_name": "Tata Consultancy Services",
      "sector": "IT",
      "exchange": "NSE"
    }
  ]
}
```

## GET /api/v1/stocks/{ticker}

Returns detailed stock metadata including: company metadata, sector classification, latest market info, exchange metadata.

---

# 11. Analysis APIs

## GET /api/v1/analysis/{ticker}

Primary stock analysis endpoint — the MOST important API.

Returns: recommendation, conviction score, deterministic signals, AI thesis, valuation summary, risks, ownership summary, key metrics.

```json
{
  "success": true,
  "data": {
    "ticker": "TCS",
    "recommendation": "BUY",
    "conviction_score": 8.2,
    "confidence": "HIGH",
    "valuation_summary": {},
    "growth_summary": {},
    "risk_summary": {},
    "ai_thesis": {}
  }
}
```

## GET /api/v1/analysis/{ticker}/history

Returns historical recommendation timeline including: historical recommendations, historical conviction, historical AI theses, historical risks.

---

# 12. Recommendation APIs

## GET /api/v1/recommendations/{ticker}

Returns deterministic recommendation output.

```json
{
  "recommendation": "BUY",
  "conviction_score": 8.1,
  "valuation_score": 7.4,
  "growth_score": 8.8,
  "profitability_score": 9.0
}
```

---

# 13. AI APIs

## GET /api/v1/ai/thesis/{ticker}

Returns AI-generated investment thesis including: bullish factors, bearish factors, valuation reasoning, risk reasoning, confidence explanation.

## POST /api/v1/ai/query

AI command interface endpoint for: conversational analysis, AI search, AI commands, contextual research.

```json
{
  "query": "Compare Infosys vs TCS"
}
```

Response:

```json
{
  "success": true,
  "data": {
    "type": "comparison",
    "response": {}
  }
}
```

---

# 14. Portfolio APIs

## GET /api/v1/portfolio

Returns: holdings, allocation, recommendation distribution, AI insights, risk exposure.

## POST /api/v1/portfolio/holdings

```json
{
  "ticker": "TCS",
  "quantity": 10,
  "average_buy_price": 3200
}
```

## DELETE /api/v1/portfolio/holdings/{id}

Remove holding.

## GET /api/v1/portfolio/intelligence

Returns AI-generated portfolio insights: concentration risk, sector exposure, weakening conviction, valuation concerns.

---

# 15. Watchlist APIs

## GET /api/v1/watchlists

Returns all watchlists.

## POST /api/v1/watchlists

Create watchlist.

## POST /api/v1/watchlists/{id}/stocks

Add stock to watchlist.

## DELETE /api/v1/watchlists/{id}/stocks/{ticker}

Remove stock from watchlist.

---

# 16. Insights APIs

## GET /api/v1/insights

Returns contextual AI insights: ownership changes, earnings developments, valuation alerts, AI observations.

Supports filtering by: ticker, importance, sector, date.

---

# 17. Alerts APIs

## GET /api/v1/alerts

Returns active alerts.

Alert types: recommendation changes, conviction drops, valuation expansion, ownership changes, earnings alerts.

---

# 18. Search APIs

## GET /api/v1/search

Unified search endpoint supporting: ticker search, company search, sector search, AI-assisted discovery.

```json
{
  "results": []
}
```

---

# 19. AI Command Interface APIs

## POST /api/v1/ai/commands

Supports:

* Analyze TCS
* Compare Infosys vs TCS
* Find undervalued pharma companies

Commands must: parse intent, remain deterministic-compatible, and avoid hallucinated stock discovery.

---

# 20. Rate Limiting

| Endpoint Type | Limit   |
| ------------- | ------- |
| Analysis APIs | 60/min  |
| AI Query APIs | 20/min  |
| Search APIs   | 100/min |

---

# 21. Security Rules

The API must NEVER: expose Groq API keys, expose Supabase secrets, or expose scraping credentials.

All secrets remain server-side only.

---

# 22. Auditability Requirements

Every recommendation response must expose:

* generated_at
* snapshot_date
* model_version
* scoring_version
* freshness metadata

This enables: historical replay, deterministic verification, AI auditability.

---

# 23. Long-Term API Vision

The API layer should evolve into:

> "A modular financial intelligence platform."

Supporting: mobile clients, autonomous monitoring agents, AI copilots, institutional workflows, semantic financial search, and future multi-user systems.
