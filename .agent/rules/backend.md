# Backend Rules

# Backend Stack

Use:

* FastAPI
* PostgreSQL
* Supabase
* Redis
* Celery

---

# Backend Philosophy

The backend is the source of:

* financial truth
* recommendation logic
* deterministic intelligence
* normalized data

The backend must remain:

* modular
* auditable
* deterministic
* scalable

---

# Financial Engine Rules

Financial logic must ALWAYS be deterministic.

Never:

* delegate scoring to AI
* allow random recommendation generation
* mix AI with authoritative calculations

---

# Data Validation Rules

All external data MUST:

* be normalized
* validated
* sanitized
* schema-checked

Never trust scraped data directly.

---

# Scraping Rules

Use:

* background jobs
* retries
* caching
* throttling

Never:

* scrape during blocking UI requests
* overload sources
* tightly couple scrapers to UI

---

# API Rules

All APIs must:

* be typed
* versionable
* validated
* consistent

---

# Error Handling Rules

Always:

* return structured errors
* log failures
* handle timeouts gracefully

Never:

* expose stack traces
* leak secrets
* silently fail

---

# Security Rules

Never:

* expose API keys
* expose Groq secrets
* trust client inputs blindly

Always:

* validate requests
* sanitize prompts
* isolate secrets server-side

---

# AI Integration Rules

AI receives ONLY:

* validated structured JSON
* deterministic signals
* normalized financial metrics

AI never receives:

* raw unvalidated scraped HTML
* malformed datasets

---

# Database Rules

Use:

* normalized schemas
* indexed tables
* historical snapshots
* deterministic relationships

Avoid:

* duplicated storage
* denormalized chaos
* inconsistent schemas

---

# Logging Rules

Track:

* scraping failures
* AI failures
* latency
* recommendation generation
* retries
* ingestion status

---

# Final Principle

The backend must behave like:

> "A deterministic financial intelligence engine."

NOT:

* a random AI wrapper
* a fragile scraping script
