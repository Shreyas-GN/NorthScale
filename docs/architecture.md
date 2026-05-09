# ARCHITECTURE.md

# AI Investment Research Terminal

Technical Architecture Document

Version: 0.1
Status: Planning

---

# 1. Architecture Philosophy

The architecture must prioritize:

* modularity
* explainability
* deterministic behavior
* scalability
* AI reliability
* maintainability
* clean separation of concerns

The system should behave like:

> “An institutional-grade financial intelligence platform.”

NOT:

* a monolithic dashboard app
* an AI wrapper
* a frontend-heavy prototype
* a fragile scraping script

---

# 2. Core System Philosophy

## Hybrid Intelligence Architecture

The application uses:

### Deterministic Financial Engine

Responsible for:

* financial calculations
* scoring systems
* ratio computation
* valuation logic
* signal generation
* sector-specific rules

AND

### AI Narrative Engine

Responsible for:

* reasoning
* summarization
* explainability
* thesis generation
* contextual interpretation

---

# IMPORTANT RULE

AI MUST NEVER:

* invent financial numbers
* fabricate ratios
* hallucinate metrics
* create unsupported claims

All raw financial data must originate from:

* structured APIs
* scraping
* computed logic
* validated datasets

---

# 3. High-Level System Architecture

```txt id="archflow"}
User Interface
        ↓
Frontend Application (Next.js)
        ↓
Backend API Layer
        ↓
Financial Intelligence Engine
        ↓
Data Aggregation Layer
        ↓
Caching + Database Layer
        ↓
AI Narrative Layer
```

---

# 4. Technology Stack

# Frontend

## Core Stack

* Next.js 15
* React 19
* TypeScript
* TailwindCSS
* shadcn/ui

---

## UI Libraries

* Framer Motion
* Lucide Icons
* TanStack Table
* Recharts
* CMDK (command palette)

---

## State Management

### Global State

Use:

* Zustand

Purpose:

* user preferences
* portfolio state
* watchlists
* UI state

---

### Server State

Use:

* TanStack Query

Purpose:

* API caching
* stock data fetching
* async synchronization

---

# Backend

## Primary Backend

Preferred:

* FastAPI (Python)

Alternative:

* Node.js Fastify

---

## Why FastAPI Preferred

Because:

* financial analysis
* AI pipelines
* scraping
* data science workflows
* PDF parsing

are significantly easier in Python.

---

# AI Layer

## Provider

* Groq (Llama 3.3 70B, DeepSeek R1 Distill)

---

## Core Strategy

* Extremely low latency (Groq)
* Institutional-grade narratives
* Deterministic signal injection

*See Section 9 for detailed AI Architecture.*

---


# Database

## Primary Database

Supabase PostgreSQL

---

## Why Supabase

Supabase is preferred because it provides:

* managed PostgreSQL
* fast MVP iteration
* simple deployment
* excellent developer experience
* scalable relational storage
* built-in APIs if needed later

This aligns well with:
- personal-use architecture
- rapid AI-assisted development
- portfolio persistence
- historical recommendation storage

---

## Database Responsibilities

The database stores:

* stocks
* financial snapshots
* recommendations
* conviction history
* portfolio holdings
* watchlists
* AI-generated insights
* historical thesis changes

---

## ORM

Preferred:
- Prisma

Alternative:
- SQLAlchemy

---

## Current Architecture Style

The system currently follows:
- single-user architecture
- personal-use workflow
- simplified persistence model

Authentication is intentionally deferred until post-MVP.

## Future Use Cases

Potential future vector use:

* annual report embeddings
* earnings transcript search
* semantic filing search
* AI memory retrieval

---

# Caching Layer

Redis

Purpose:

* stock snapshots
* recommendation cache
* AI response cache
* scraping throttle
* session optimization

---

# Queue System

Preferred:

* Celery + Redis

Alternative:

* BullMQ

---

## Queue Responsibilities

Background jobs:

* scraping
* AI analysis
* recommendation generation
* earnings re-analysis
* historical snapshot creation

---

# 5. Folder Structure

# Frontend Structure

```txt id="frontendstruct"}
/app
/components
/features
/hooks
/lib
/providers
/services
/store
/styles
/types
/utils
```

---

# Backend Structure

```txt id="backendstruct"}
/api
/core
/services
/engines
/ai
/scrapers
/jobs
/db
/models
/schemas
/utils
/tests
```

---

# Feature-Based Organization

Features must remain modular.

Example:

```txt id="featuremod"}
/features/stock-analysis
/features/portfolio
/features/watchlist
/features/ai-chat
```

Each feature owns:

* components
* hooks
* services
* types
* API logic

---

# 6. Core System Layers

# Layer 1 — Presentation Layer

Responsible for:

* rendering UI
* user interactions
* dashboard visualization
* command palette
* responsive layouts

Must NEVER:

* contain business logic
* compute recommendations
* contain financial rules

---

# Layer 2 — API Layer

Responsible for:

* request validation
* authentication
* data orchestration
* response formatting

Must NEVER:

* contain UI logic

---

# Layer 3 — Financial Intelligence Engine

Responsible for:

* ratios
* scoring
* valuation
* sector rules
* conviction scoring

This is the HEART of the application.

---

# Layer 4 — AI Narrative Engine

Responsible for:

* thesis generation
* risk explanation
* contextual summaries
* narrative synthesis

---

# Layer 5 — Data Aggregation Layer

Responsible for:

* scraping
* normalization
* ingestion
* validation
* historical storage

---

# Layer 6 — Persistence Layer

Responsible for:

* PostgreSQL storage
* Redis cache
* snapshot history
* portfolios
* watchlists

---

# 7. Financial Intelligence Engine

# Core Principle

Financial logic must remain deterministic.

---

# Responsibilities

The engine computes:

* ROE
* ROCE
* debt metrics
* valuation metrics
* growth consistency
* profitability scores
* sector benchmarks

---

# Sector Rule System

Different sectors require different logic.

Examples:

## Banking

* CASA
* GNPA
* NIM

## FMCG

* pricing power
* margins

## Pharma

* approvals
* pipeline

## SaaS

* growth quality
* retention

---

# Recommendation Pipeline

```txt id="recommendflow"}
Raw Data
    ↓
Normalization
    ↓
Signal Generation
    ↓
Sector Rule Engine
    ↓
Scoring Engine
    ↓
Recommendation Engine
    ↓
AI Narrative Layer
```

---

# 8. Data Ingestion Architecture

# Data Sources

Primary:

* NSE India
* BSE India
* Screener
* Moneycontrol
* Tickertape
* Trendlyne

---

# Scraping Strategy

Use:

* Playwright
* BeautifulSoup
* request-based scraping where possible

---

# IMPORTANT RULE

Never scrape during active user request if avoidable.

Instead:

* pre-fetch
* cache
* background-refresh

---

# Normalization Layer

All external data must map into:

* internal schemas
* normalized structures
* validated formats

---

# Example

External APIs may differ:

```json
{
  "roe": 18
}
```

vs

```json
{
  "returnOnEquity": 18
}
```

Internal system ALWAYS stores:

```json
{
  "roe": 18
}
```

---

# Freshness Tracking

Every dataset must include:

* source
* fetched_at
* freshness_score

---

# 9. AI Layer

# Model Provider

Primary Provider:

* Groq

---

# Why Groq

Groq is preferred because it provides:

* extremely low latency
* ultra-fast inference
* real-time AI responses
* cost-efficient inference
* excellent structured output performance

This aligns with the product goals of:

* instant stock analysis
* responsive AI interactions
* low-friction research workflows
* AI-native user experience

The application should feel:

> "fast, alive, and responsive"

rather than:

> "waiting for AI generation."

---

# Preferred Models

Primary Models:

* DeepSeek R1 Distill
* Llama 3.3 70B
* Mixtral
* Gemma variants

Model selection may vary depending on:

* reasoning quality
* latency requirements
* cost optimization
* structured JSON reliability
* inference complexity

---

# AI Layer Responsibilities

The AI layer is responsible ONLY for:

* narrative synthesis
* investment thesis generation
* explainability
* contextual reasoning
* risk framing
* recommendation explanation
* insight summarization
* portfolio intelligence narratives

The AI layer is NOT responsible for:

* raw financial calculations
* deterministic scoring
* ratio computation
* valuation formulas
* authoritative financial truth
* generating unsupported metrics

All financial truth must originate from:

* validated datasets
* deterministic financial engines
* normalized scraped data
* structured financial calculations

---

# AI Prompt Strategy

All prompts MUST:

* use structured JSON inputs
* receive validated financial metrics
* receive deterministic scoring signals
* include sector context
* include risk context
* forbid unsupported claims
* forbid fabricated numbers
* avoid investment guarantees

Prompts should prioritize:

* explainability
* concise reasoning
* institutional tone
* signal clarity
* structured responses

---

# AI Pipeline

```txt id="groqflow"}
Structured Financial Data
        ↓
Financial Intelligence Engine
        ↓
Signal Generation
        ↓
Sector Context Builder
        ↓
Prompt Builder
        ↓
Groq LLM Inference
        ↓
Narrative Output
        ↓
Recommendation Explanation
        ↓
Frontend Presentation
```

---

# AI Output Requirements

AI outputs must:

* remain explainable
* avoid hallucinations
* reference supplied metrics
* use probabilistic language
* avoid certainty claims
* remain concise and information-dense
* preserve institutional tone
* avoid exaggerated bullish/bearish language

---

# Example Output Standards

Good Output:

> "The company demonstrates strong profitability and improving cash generation, although current valuation appears elevated relative to historical averages."

Bad Output:

> "This stock will definitely outperform and double soon."

---

# Latency Goals

Target AI response generation:

* under 1.5 seconds for cached analysis
* under 3 seconds for fresh analysis
* near-instant command palette interactions

The system should prioritize:

* responsiveness
* smooth research flow
* rapid stock iteration
* low-friction UX

---

# AI Failure Handling

If Groq inference fails:

* retry once
* fallback to deterministic summaries
* display graceful degraded UI
* never block full page rendering
* preserve financial data visibility

---

# AI Caching Strategy

Use Redis for:

* AI response caching
* recommendation caching
* portfolio intelligence caching
* repeated analysis optimization
* prompt throttling

Cache:

* AI-generated theses
* recommendation explanations
* portfolio summaries
* AI insight panels

---

# AI Safety Rules

The AI system must NEVER:

* fabricate financial data
* invent company metrics
* guarantee investment returns
* generate unsupported claims
* hide uncertainty
* override deterministic engine outputs

The AI system must ALWAYS:

* explain reasoning
* surface uncertainty
* remain auditable
* reference deterministic signals
* preserve user trust

---

# Future AI Expansion

Potential future additions:

* local reasoning models
* hybrid inference routing
* multi-model consensus
* specialized finance agents
* transcript-specific models
* annual-report summarization models
* filing intelligence systems
* autonomous monitoring agents
* semantic financial search

---

# Long-Term AI Vision

The long-term AI layer should evolve into:

> "A real-time institutional investment copilot."

The system should eventually support:

* continuous portfolio monitoring
* thesis evolution tracking
* autonomous alerting
* sector-aware intelligence
* contextual investment memory
* AI-driven opportunity discovery

while preserving:

* explainability
* deterministic trust
* narrative clarity
* institutional reliability

---


# 10. Recommendation System

# Recommendation Categories

* STRONG BUY
* BUY
* HOLD
* WATCHLIST
* SELL / AVOID

---

# Recommendation Generation

Recommendations combine:

* financial quality
* valuation
* growth
* debt
* ownership
* sector context
* risks

---

# Scoring Philosophy

Weighted scoring model.

Example:

| Category         | Weight |
| ---------------- | ------ |
| Growth           | 25%    |
| Profitability    | 20%    |
| Valuation        | 20%    |
| Financial Health | 20%    |
| Ownership        | 10%    |
| Risks            | 5%     |

---

# 11. API Architecture

# API Style

REST-first.

Potential future:

* GraphQL

---

# Naming Rules

Endpoints:

* kebab-case

Examples:

```txt id="apiex"}
/api/stocks
/api/portfolio
/api/watchlists
/api/recommendations
```

---

# Response Rules

Responses must:

* be typed
* consistent
* versionable

---

# Error Response Standard

```json
{
  "success": false,
  "error": {
    "code": "DATA_FETCH_FAILED",
    "message": "Unable to fetch stock data"
  }
}
```

---

# 12. Workspace Architecture

# Current Architecture Strategy

The application currently uses:
- single-user architecture
- personal-use workflow
- local workspace persistence

Authentication is intentionally excluded from MVP.

---

# Current Persistence Model

User-specific data includes:

* portfolio holdings
* watchlists
* cached analyses
* recommendation history
* UI preferences

---

# Why Authentication Is Deferred

Authentication is intentionally postponed because:

* the application is personal-use
* rapid iteration is prioritized
* infrastructure complexity should remain minimal
* no public multi-user workflows currently exist

---

# Future Expansion

Authentication may later support:

* multi-user workspaces
* cloud sync
* collaborative investing
* mobile synchronization
* advanced permissions

# 13. Portfolio System Architecture

# Portfolio Model

Users can:

* create multiple portfolios
* add holdings
* track allocations
* monitor recommendations

---

# Snapshot System

Historical snapshots must store:

* recommendation
* conviction
* thesis
* risk summary

This enables:

* thesis evolution
* recommendation history
* AI change tracking

---

# 14. Performance Architecture

# Performance Goals

* stock analysis under 3s
* cached loads under 1s
* fast command palette
* minimal blocking requests

---

# Performance Strategy

Use:

* Redis caching
* server components
* background jobs
* incremental loading
* optimistic rendering

---

# 15. Frontend Rules

# NEVER

* place business logic in components
* directly call external APIs from UI
* hardcode financial calculations
* duplicate API logic

---

# ALWAYS

* use typed responses
* use feature modules
* isolate reusable components
* separate UI and business logic

---

# 16. Backend Rules

# NEVER

* trust external scraped data blindly
* expose secrets
* mix AI prompts with raw UI code
* skip validation

---

# ALWAYS

* validate inputs
* normalize data
* cache expensive operations
* log ingestion failures

---

# 17. UI Architecture

# UI Philosophy

Narrative-first.

NOT dashboard chaos.

---

# Layout Structure

```txt id="uilayout"}
LEFT SIDEBAR
MAIN CONTENT
RIGHT INTELLIGENCE PANEL
```

---

# UI Principles

* calm interfaces
* premium dark surfaces
* AI-first workflows
* minimal clutter
* readable typography

---

# 18. Logging & Monitoring

# Logging

Track:

* scraping failures
* AI failures
* API latency
* recommendation generation
* user actions

---

# Monitoring

Future:

* Sentry
* PostHog
* OpenTelemetry

---

# 19. Testing Strategy

# Frontend Testing

* Playwright
* Vitest

---

# Backend Testing

* Pytest
* integration tests
* API contract tests

---

# Critical Test Areas

* recommendation consistency
* financial calculations
* scraping reliability
* AI output validation
* portfolio snapshots

---

# 20. Scalability Strategy

# Current Focus

Personal-use MVP.

Optimization priorities:

* reliability
* iteration speed
* modularity

NOT:

* massive horizontal scaling

---

# Future Scalability

Future-ready architecture for:

* multiple users
* larger datasets
* automated monitoring
* AI memory systems

---

# 21. Deployment Architecture

# Frontend

Vercel

---

# Backend

Railway / Render / Fly.io

---

# Database

Supabase PostgreSQL or Neon

---

# Redis

Upstash Redis

---

# 22. Architectural Non-Negotiables

# RULES

## Financial logic MUST remain deterministic.

## AI MUST remain explainable.

## UI MUST remain narrative-first.

## Data MUST be normalized.

## Scraping MUST remain background-oriented.

## Recommendations MUST remain auditable.

## The application MUST avoid dashboard clutter.

---

# 23. Long-Term Architectural Vision

The long-term system should evolve into:

* AI portfolio copilot
* thesis evolution engine
* autonomous monitoring system
* intelligent alert infrastructure
* institutional-grade research platform

while preserving:

* explainability
* calm UX
* deterministic trust
* modern AI-native workflows
