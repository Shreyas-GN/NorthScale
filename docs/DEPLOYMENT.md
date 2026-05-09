# DEPLOYMENT.md

# AI Investment Research Terminal

Deployment & Infrastructure Architecture

Version: 0.1

---

# 1. Deployment Philosophy

The infrastructure must prioritize:

* reliability
* low latency
* deterministic consistency
* deployment simplicity
* observability
* scalability readiness

The system should feel:

> "fast, stable, and production-ready"

even during MVP phase.

---

# 2. Infrastructure Stack

## Frontend

Platform: Vercel

Responsibilities:

* Next.js hosting
* edge delivery
* static asset optimization
* frontend deployment pipeline

---

## Backend

Platform: Railway (Alternatives: Render, Fly.io)

Responsibilities:

* FastAPI hosting
* recommendation engine APIs
* scraping orchestration
* AI pipelines

---

## Database

Platform: Supabase PostgreSQL

Responsibilities:

* relational persistence
* historical snapshots
* portfolio storage
* recommendation history
* AI metadata persistence

---

## Cache Layer

Platform: Upstash Redis

Responsibilities:

* AI response caching
* stock analysis caching
* scraping throttle support
* low-latency retrieval

---

## AI Layer

Provider: Groq

Responsibilities:

* thesis generation
* explainability
* contextual reasoning
* narrative synthesis

---

# 3. Environment Architecture

## Development

Purpose: local engineering, feature iteration, debugging.

## Staging

Purpose: integration testing, API validation, scoring verification.

## Production

Purpose: stable personal-use deployment, reliable portfolio monitoring, deterministic recommendation generation.

---

# 4. Environment Variables

## Frontend Variables

```env
NEXT_PUBLIC_API_URL=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
```

## Backend Variables

```env
DATABASE_URL=
REDIS_URL=
GROQ_API_KEY=
SUPABASE_SERVICE_ROLE_KEY=
```

## Security Rules

Secrets must NEVER:

* exist client-side
* appear in logs
* appear in AI prompts
* be hardcoded

---

# 5. Deployment Pipeline

## Frontend Deployment Flow

```txt
Git Push
    ↓
Vercel Build
    ↓
Static Optimization
    ↓
Production Deployment
```

## Backend Deployment Flow

```txt
Git Push
    ↓
Railway Build
    ↓
Container Deployment
    ↓
Health Checks
    ↓
Production Release
```

---

# 6. Database Deployment Rules

NEVER:

* manually mutate production tables
* overwrite historical snapshots
* bypass migrations

ALWAYS:

* preserve historical integrity
* backup before schema changes
* validate recommendation persistence

---

# 7. Redis Deployment Rules

## Cache Priorities

Cache: stock analysis responses, recommendation outputs, AI theses, portfolio intelligence.

## Cache Invalidation

Invalidate when: new financial data arrives, recommendation regenerates, or ownership changes detected.

---

# 8. Backend Runtime Architecture

FastAPI handles: deterministic scoring, recommendation generation, scraping orchestration, AI prompt pipelines, portfolio intelligence, and API delivery.

## Important Rule

Frontend must NEVER: compute recommendation logic, expose AI secrets, or directly scrape sources.

---

# 9. Scraping Deployment Strategy

Scraping must run: asynchronously, in background workers, and queue-driven.

## Recommended Worker System

Celery + Redis (Alternative: BullMQ)

## Queue Responsibilities

* scraping jobs
* retries
* recommendation refresh
* AI synthesis refresh

---

# 10. Observability & Monitoring

## Monitor

* scraping failures
* API latency
* cache failures
* AI failures
* retry frequency
* recommendation generation time

## Future Monitoring Stack

* Sentry
* PostHog
* OpenTelemetry

---

# 11. Performance Goals

| Operation         | Target  |
| ----------------- | ------- |
| Cached analysis   | < 1.5s  |
| Fresh analysis    | < 3s    |
| API latency       | < 500ms |
| Portfolio loading | < 1s    |

---

# 12. Deployment Safety Rules

NEVER deploy:

* unvalidated scoring changes
* untested prompt changes
* schema-breaking API updates

ALWAYS:

* test recommendation consistency
* validate deterministic outputs
* preserve API contracts

---

# 13. Backup Philosophy

Must support: historical replay, recommendation recovery, snapshot restoration.

| System      | Frequency |
| ----------- | --------- |
| PostgreSQL  | Daily     |
| Redis       | Optional  |
| AI metadata | Daily     |

---

# 14. Scaling Philosophy

Current MVP optimizes for: personal use, fast iteration, and deterministic reliability.

NOT: massive concurrency or enterprise scaling.

Architecture should remain ready for: multi-user systems, AI copilots, autonomous monitoring agents, and semantic financial search.

---

# 15. CI/CD Philosophy

Goals: stable deployments, deterministic consistency, rapid iteration, rollback safety.

Future CI/CD additions:

* GitHub Actions
* automated testing
* deployment validation
* scoring regression tests

---

# 16. Disaster Recovery

If scraping, Groq, or APIs fail — the system should: fallback gracefully, preserve cached analysis, and expose stale-data state.

NEVER: hallucinate missing financial data or hide degraded system state.

---

# 17. Long-Term Infrastructure Vision

The infrastructure should evolve into:

> "A reliable institutional-grade AI financial intelligence platform."

Supporting: deterministic investing workflows, explainable AI analysis, portfolio intelligence, historical thesis evolution, and autonomous monitoring systems.
