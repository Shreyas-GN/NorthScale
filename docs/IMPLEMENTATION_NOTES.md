# IMPLEMENTATION_NOTES.md

# AI Investment Research Terminal

Implementation Notes & Engineering Decisions

Version: 0.1

---

# Current Architecture Decisions

## Frontend

* Next.js 15
* React 19
* TailwindCSS
* shadcn/ui
* Zustand
* TanStack Query

---

## Backend

* FastAPI
* Python-first architecture
* deterministic financial engine

---

## Database

* Supabase PostgreSQL
* normalized relational schema
* historical snapshot strategy

---

## AI Stack

* Groq
* DeepSeek R1 Distill
* Llama 3.3 70B

---

# MVP Constraints

Current MVP intentionally excludes:

* multi-user auth
* OAuth
* mobile apps
* real-time streaming
* brokerage integrations
* trade execution

---

# Engineering Priorities

Current priorities:

1. deterministic engine quality
2. recommendation explainability
3. scraping reliability
4. AI consistency
5. historical persistence

NOT:

* advanced dashboards
* animations
* social features

---

# Current Known Risks

## Scraping Reliability

Risk: NSE/BSE anti-bot protection

Mitigation:

* caching
* retries
* staggered scraping

---

## AI Hallucinations

Risk: fabricated reasoning

Mitigation:

* structured prompts
* deterministic grounding
* validation layer

---

## Recommendation Drift

Risk: scoring inconsistency over time

Mitigation:

* versioned scoring engine
* deterministic calculations

---

# Deferred Features

Deferred until post-MVP:

* authentication
* vector search
* semantic retrieval
* AI memory systems
* mobile apps
* autonomous monitoring agents

---

# Current Implementation Order

```txt
1. Supabase setup
2. FastAPI scaffold
3. DB models
4. Scraping pipeline
5. Normalization engine
6. Scoring engine
7. Recommendation engine
8. Groq integration
9. REST APIs
10. Stock analysis UI
```

---

# Important Architectural Rules

## NEVER

* allow AI to generate financial truth
* overwrite historical snapshots
* scrape synchronously in frontend
* hardcode recommendation logic in UI

---

## ALWAYS

* preserve explainability
* preserve deterministic trust
* validate external data
* version recommendations

---

# Future Expansion Notes

Potential future additions:

* autonomous AI copilot
* filing intelligence
* transcript analysis
* portfolio optimization
* semantic investment search

---

# Final Principle

This platform should evolve into:

> "An institutional-grade AI investment intelligence terminal."

while preserving:

* explainability
* calm UX
* deterministic trust
* narrative-first workflows
