# DATABASE_SCHEMA.md

# AI Investment Research Terminal

Database Schema — Supabase PostgreSQL

Version: 0.1
Status: Planning
Convention: snake_case for all tables and columns

---

# 1. Schema Philosophy

The database is the source of deterministic financial truth.

Principles:
- normalized schemas
- indexed for read-heavy workloads
- historical snapshots preserved immutably
- no financial logic inside the DB (computed in engine)
- all timestamps in UTC using `timestamptz`
- soft deletes via `is_deleted` where needed
- `created_at` and `updated_at` on every table

---

# 2. Schema Overview

```
stocks
stock_financial_snapshots
stock_price_snapshots
stock_ownership_snapshots
recommendations
recommendation_history
conviction_scores
conviction_history
ai_theses
ai_insights
portfolios
portfolio_holdings
portfolio_snapshots
watchlists
watchlist_stocks
alerts
sectors
sector_benchmarks
scraping_jobs
scraping_logs
ai_generation_logs
```

---

# 3. Core Tables

---

## 3.1 stocks

Master registry of all tracked NSE/BSE equities.

```sql
CREATE TABLE stocks (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ticker              TEXT NOT NULL UNIQUE,
  company_name        TEXT NOT NULL,
  exchange            TEXT NOT NULL CHECK (exchange IN ('NSE', 'BSE')),
  isin                TEXT UNIQUE,
  sector_id           UUID REFERENCES sectors(id),
  industry            TEXT,
  market_cap_category TEXT CHECK (market_cap_category IN ('LARGE_CAP', 'MID_CAP', 'SMALL_CAP', 'MICRO_CAP')),
  is_active           BOOLEAN NOT NULL DEFAULT TRUE,
  is_deleted          BOOLEAN NOT NULL DEFAULT FALSE,
  listed_at           DATE,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_stocks_ticker ON stocks(ticker);
CREATE INDEX idx_stocks_sector_id ON stocks(sector_id);
CREATE INDEX idx_stocks_exchange ON stocks(exchange);
CREATE INDEX idx_stocks_is_active ON stocks(is_active);
```

---

## 3.2 stock_financial_snapshots

Immutable point-in-time financial metric snapshots. Never updated — only inserted.

```sql
CREATE TABLE stock_financial_snapshots (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id              UUID NOT NULL REFERENCES stocks(id),
  snapshot_date         DATE NOT NULL,

  -- Profitability
  roe                   NUMERIC(8, 4),
  roce                  NUMERIC(8, 4),
  net_profit_margin     NUMERIC(8, 4),
  operating_margin      NUMERIC(8, 4),
  gross_margin          NUMERIC(8, 4),
  ebitda_margin         NUMERIC(8, 4),

  -- Growth
  revenue_1y_growth     NUMERIC(8, 4),
  revenue_3y_cagr       NUMERIC(8, 4),
  revenue_5y_cagr       NUMERIC(8, 4),
  profit_1y_growth      NUMERIC(8, 4),
  profit_3y_cagr        NUMERIC(8, 4),
  profit_5y_cagr        NUMERIC(8, 4),

  -- Financial Health
  debt_to_equity        NUMERIC(8, 4),
  current_ratio         NUMERIC(8, 4),
  interest_coverage     NUMERIC(8, 4),
  free_cash_flow        NUMERIC(18, 2),
  cash_and_equivalents  NUMERIC(18, 2),

  -- Valuation
  pe_ratio              NUMERIC(8, 4),
  pb_ratio              NUMERIC(8, 4),
  ev_to_ebitda          NUMERIC(8, 4),
  price_to_sales        NUMERIC(8, 4),
  enterprise_value      NUMERIC(18, 2),
  market_cap            NUMERIC(18, 2),
  cmp                   NUMERIC(12, 4),

  -- Revenue and Earnings
  revenue_ttm           NUMERIC(18, 2),
  net_profit_ttm        NUMERIC(18, 2),
  eps_ttm               NUMERIC(12, 4),
  book_value_per_share  NUMERIC(12, 4),

  -- Banking-Specific (nullable for non-banking stocks)
  casa_ratio            NUMERIC(8, 4),
  gnpa_ratio            NUMERIC(8, 4),
  nnpa_ratio            NUMERIC(8, 4),
  nim                   NUMERIC(8, 4),
  car_ratio             NUMERIC(8, 4),

  -- Source metadata
  data_source           TEXT NOT NULL,
  fetched_at            TIMESTAMPTZ NOT NULL,
  freshness_score       INTEGER CHECK (freshness_score BETWEEN 0 AND 100),

  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_financial_snapshots_stock_id ON stock_financial_snapshots(stock_id);
CREATE INDEX idx_financial_snapshots_date ON stock_financial_snapshots(snapshot_date DESC);
CREATE UNIQUE INDEX idx_financial_snapshots_stock_date ON stock_financial_snapshots(stock_id, snapshot_date);
```

---

## 3.3 stock_price_snapshots

Daily price snapshots for historical tracking.

```sql
CREATE TABLE stock_price_snapshots (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id     UUID NOT NULL REFERENCES stocks(id),
  price_date   DATE NOT NULL,
  open         NUMERIC(12, 4),
  high         NUMERIC(12, 4),
  low          NUMERIC(12, 4),
  close        NUMERIC(12, 4) NOT NULL,
  volume       BIGINT,
  market_cap   NUMERIC(18, 2),
  data_source  TEXT NOT NULL,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_price_snapshots_stock_id ON stock_price_snapshots(stock_id);
CREATE INDEX idx_price_snapshots_date ON stock_price_snapshots(price_date DESC);
CREATE UNIQUE INDEX idx_price_snapshots_stock_date ON stock_price_snapshots(stock_id, price_date);
```

---

## 3.4 stock_ownership_snapshots

Shareholding pattern snapshots per quarter.

```sql
CREATE TABLE stock_ownership_snapshots (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id              UUID NOT NULL REFERENCES stocks(id),
  quarter_end_date      DATE NOT NULL,

  promoter_holding      NUMERIC(6, 4),
  promoter_pledge_pct   NUMERIC(6, 4),
  fii_holding           NUMERIC(6, 4),
  dii_holding           NUMERIC(6, 4),
  public_holding        NUMERIC(6, 4),
  mutual_fund_holding   NUMERIC(6, 4),

  -- Change from previous quarter
  promoter_change_qoq   NUMERIC(6, 4),
  fii_change_qoq        NUMERIC(6, 4),
  dii_change_qoq        NUMERIC(6, 4),

  data_source           TEXT NOT NULL,
  fetched_at            TIMESTAMPTZ NOT NULL,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ownership_snapshots_stock_id ON stock_ownership_snapshots(stock_id);
CREATE INDEX idx_ownership_snapshots_quarter ON stock_ownership_snapshots(quarter_end_date DESC);
CREATE UNIQUE INDEX idx_ownership_snapshots_stock_quarter ON stock_ownership_snapshots(stock_id, quarter_end_date);
```

---

# 4. Recommendation Engine Tables

---

## 4.1 recommendations

Current active recommendation per stock. Single live row per stock (upserted).

```sql
CREATE TABLE recommendations (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id              UUID NOT NULL REFERENCES stocks(id) UNIQUE,

  recommendation        TEXT NOT NULL CHECK (recommendation IN (
                          'STRONG_BUY', 'BUY', 'HOLD', 'WATCHLIST', 'SELL', 'AVOID'
                        )),
  conviction_score      NUMERIC(4, 2) NOT NULL CHECK (conviction_score BETWEEN 0 AND 10),
  confidence_level      TEXT NOT NULL CHECK (confidence_level IN (
                          'VERY_HIGH', 'HIGH', 'MODERATE', 'LOW'
                        )),

  -- Scoring breakdown (deterministic engine outputs)
  growth_score          NUMERIC(4, 2),
  profitability_score   NUMERIC(4, 2),
  valuation_score       NUMERIC(4, 2),
  financial_health_score NUMERIC(4, 2),
  ownership_score       NUMERIC(4, 2),
  risk_score            NUMERIC(4, 2),

  -- Weighted composite
  composite_score       NUMERIC(5, 4) NOT NULL,

  -- Snapshot reference for auditability
  financial_snapshot_id UUID REFERENCES stock_financial_snapshots(id),
  ownership_snapshot_id UUID REFERENCES stock_ownership_snapshots(id),

  generated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  valid_until           TIMESTAMPTZ,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_recommendations_stock_id ON recommendations(stock_id);
CREATE INDEX idx_recommendations_recommendation ON recommendations(recommendation);
CREATE INDEX idx_recommendations_conviction ON recommendations(conviction_score DESC);
```

---

## 4.2 recommendation_history

Immutable historical log of every recommendation state. Never updated.

```sql
CREATE TABLE recommendation_history (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id              UUID NOT NULL REFERENCES stocks(id),
  recommendation_id     UUID REFERENCES recommendations(id),

  recommendation        TEXT NOT NULL CHECK (recommendation IN (
                          'STRONG_BUY', 'BUY', 'HOLD', 'WATCHLIST', 'SELL', 'AVOID'
                        )),
  conviction_score      NUMERIC(4, 2) NOT NULL,
  confidence_level      TEXT NOT NULL,

  growth_score          NUMERIC(4, 2),
  profitability_score   NUMERIC(4, 2),
  valuation_score       NUMERIC(4, 2),
  financial_health_score NUMERIC(4, 2),
  ownership_score       NUMERIC(4, 2),
  risk_score            NUMERIC(4, 2),
  composite_score       NUMERIC(5, 4),

  -- What changed from the previous recommendation
  previous_recommendation TEXT,
  change_reason           TEXT,

  financial_snapshot_id UUID REFERENCES stock_financial_snapshots(id),
  generated_at          TIMESTAMPTZ NOT NULL,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_rec_history_stock_id ON recommendation_history(stock_id);
CREATE INDEX idx_rec_history_generated_at ON recommendation_history(generated_at DESC);
```

---

# 5. AI Layer Tables

---

## 5.1 ai_theses

AI-generated investment theses. Linked to a specific recommendation snapshot.

```sql
CREATE TABLE ai_theses (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id              UUID NOT NULL REFERENCES stocks(id),
  recommendation_id     UUID REFERENCES recommendations(id),
  financial_snapshot_id UUID REFERENCES stock_financial_snapshots(id),

  -- AI-generated narrative fields
  thesis_summary        TEXT NOT NULL,
  business_quality      TEXT,
  key_strengths         TEXT[],
  key_risks             TEXT[],
  valuation_perspective TEXT,
  overall_view          TEXT,

  -- AI metadata
  model_id              TEXT NOT NULL,
  model_provider        TEXT NOT NULL DEFAULT 'groq',
  prompt_version        TEXT,
  input_token_count     INTEGER,
  output_token_count    INTEGER,
  generation_latency_ms INTEGER,

  -- Trust signal
  is_fallback           BOOLEAN NOT NULL DEFAULT FALSE,
  confidence_note       TEXT,

  generated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ai_theses_stock_id ON ai_theses(stock_id);
CREATE INDEX idx_ai_theses_generated_at ON ai_theses(generated_at DESC);
```

---

## 5.2 ai_insights

Contextual intelligence feed entries (right panel).

```sql
CREATE TABLE ai_insights (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id     UUID REFERENCES stocks(id),
  insight_type TEXT NOT NULL CHECK (insight_type IN (
                  'OWNERSHIP_CHANGE', 'VALUATION_SHIFT', 'RISK_ALERT',
                  'EARNINGS_OBSERVATION', 'RECOMMENDATION_CHANGE',
                  'GROWTH_SIGNAL', 'PORTFOLIO_INTELLIGENCE', 'SECTOR_OBSERVATION'
                )),
  title        TEXT NOT NULL,
  body         TEXT NOT NULL,
  severity     TEXT CHECK (severity IN ('INFO', 'WARNING', 'CRITICAL')),
  is_read      BOOLEAN NOT NULL DEFAULT FALSE,

  model_id     TEXT,
  model_provider TEXT DEFAULT 'groq',
  generated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ai_insights_stock_id ON ai_insights(stock_id);
CREATE INDEX idx_ai_insights_generated_at ON ai_insights(generated_at DESC);
CREATE INDEX idx_ai_insights_type ON ai_insights(insight_type);
CREATE INDEX idx_ai_insights_is_read ON ai_insights(is_read);
```

---

## 5.3 ai_generation_logs

Audit log for all AI inference calls.

```sql
CREATE TABLE ai_generation_logs (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  context_type       TEXT NOT NULL,
  stock_id           UUID REFERENCES stocks(id),
  model_id           TEXT NOT NULL,
  model_provider     TEXT NOT NULL DEFAULT 'groq',
  prompt_version     TEXT,
  status             TEXT NOT NULL CHECK (status IN ('SUCCESS', 'FAILED', 'FALLBACK', 'TIMEOUT')),
  latency_ms         INTEGER,
  input_token_count  INTEGER,
  output_token_count INTEGER,
  error_message      TEXT,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ai_logs_stock_id ON ai_generation_logs(stock_id);
CREATE INDEX idx_ai_logs_status ON ai_generation_logs(status);
CREATE INDEX idx_ai_logs_created_at ON ai_generation_logs(created_at DESC);
```

---

# 6. Portfolio Tables

---

## 6.1 portfolios

Portfolio containers.

```sql
CREATE TABLE portfolios (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  description TEXT,
  is_default  BOOLEAN NOT NULL DEFAULT FALSE,
  is_deleted  BOOLEAN NOT NULL DEFAULT FALSE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 6.2 portfolio_holdings

Individual stock holdings within a portfolio.

```sql
CREATE TABLE portfolio_holdings (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  portfolio_id      UUID NOT NULL REFERENCES portfolios(id),
  stock_id          UUID NOT NULL REFERENCES stocks(id),

  quantity          NUMERIC(14, 4) NOT NULL,
  avg_buy_price     NUMERIC(12, 4) NOT NULL,
  buy_date          DATE,
  notes             TEXT,

  is_deleted        BOOLEAN NOT NULL DEFAULT FALSE,
  created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  UNIQUE (portfolio_id, stock_id)
);

CREATE INDEX idx_portfolio_holdings_portfolio_id ON portfolio_holdings(portfolio_id);
CREATE INDEX idx_portfolio_holdings_stock_id ON portfolio_holdings(stock_id);
```

---

## 6.3 portfolio_snapshots

Historical point-in-time snapshots of the entire portfolio state.

```sql
CREATE TABLE portfolio_snapshots (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  portfolio_id    UUID NOT NULL REFERENCES portfolios(id),
  snapshot_date   DATE NOT NULL,

  total_value     NUMERIC(18, 2),
  total_invested  NUMERIC(18, 2),
  unrealized_pnl  NUMERIC(18, 2),

  -- AI-generated portfolio intelligence
  ai_summary      TEXT,
  risk_summary    TEXT,
  sector_exposure JSONB,

  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_portfolio_snapshots_portfolio_id ON portfolio_snapshots(portfolio_id);
CREATE INDEX idx_portfolio_snapshots_date ON portfolio_snapshots(snapshot_date DESC);
```

---

# 7. Watchlist Tables

---

## 7.1 watchlists

```sql
CREATE TABLE watchlists (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  description TEXT,
  is_deleted  BOOLEAN NOT NULL DEFAULT FALSE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

---

## 7.2 watchlist_stocks

```sql
CREATE TABLE watchlist_stocks (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  watchlist_id UUID NOT NULL REFERENCES watchlists(id),
  stock_id     UUID NOT NULL REFERENCES stocks(id),
  notes        TEXT,
  added_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  UNIQUE (watchlist_id, stock_id)
);

CREATE INDEX idx_watchlist_stocks_watchlist_id ON watchlist_stocks(watchlist_id);
CREATE INDEX idx_watchlist_stocks_stock_id ON watchlist_stocks(stock_id);
```

---

# 8. Alerts Table

```sql
CREATE TABLE alerts (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  stock_id     UUID REFERENCES stocks(id),
  alert_type   TEXT NOT NULL CHECK (alert_type IN (
                  'RECOMMENDATION_CHANGE', 'CONVICTION_DROP',
                  'VALUATION_EXPANSION', 'EARNINGS_MISS',
                  'OWNERSHIP_CHANGE', 'CUSTOM'
                )),
  title        TEXT NOT NULL,
  body         TEXT,
  severity     TEXT NOT NULL CHECK (severity IN ('INFO', 'WARNING', 'CRITICAL')),
  is_read      BOOLEAN NOT NULL DEFAULT FALSE,
  is_dismissed BOOLEAN NOT NULL DEFAULT FALSE,
  triggered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_alerts_stock_id ON alerts(stock_id);
CREATE INDEX idx_alerts_is_read ON alerts(is_read);
CREATE INDEX idx_alerts_triggered_at ON alerts(triggered_at DESC);
```

---

# 9. Sector Tables

---

## 9.1 sectors

```sql
CREATE TABLE sectors (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name          TEXT NOT NULL UNIQUE,
  slug          TEXT NOT NULL UNIQUE,
  sector_type   TEXT CHECK (sector_type IN (
                  'BANKING', 'FMCG', 'PHARMA', 'IT', 'INFRA',
                  'AUTO', 'ENERGY', 'SAAS', 'TELECOM', 'REALESTATE', 'OTHER'
                )),
  description   TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sectors_slug ON sectors(slug);
```

---

## 9.2 sector_benchmarks

Sector-level KPI benchmarks for comparison.

```sql
CREATE TABLE sector_benchmarks (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  sector_id             UUID NOT NULL REFERENCES sectors(id),
  benchmark_date        DATE NOT NULL,

  median_pe             NUMERIC(8, 4),
  median_pb             NUMERIC(8, 4),
  median_ev_ebitda      NUMERIC(8, 4),
  median_roe            NUMERIC(8, 4),
  median_roce           NUMERIC(8, 4),
  median_debt_equity    NUMERIC(8, 4),
  median_revenue_growth NUMERIC(8, 4),
  median_profit_growth  NUMERIC(8, 4),

  -- Banking-specific benchmarks
  median_nim            NUMERIC(8, 4),
  median_gnpa           NUMERIC(8, 4),
  median_casa           NUMERIC(8, 4),

  data_source           TEXT,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW(),

  UNIQUE (sector_id, benchmark_date)
);

CREATE INDEX idx_sector_benchmarks_sector_id ON sector_benchmarks(sector_id);
CREATE INDEX idx_sector_benchmarks_date ON sector_benchmarks(benchmark_date DESC);
```

---

# 10. Data Ingestion Tables

---

## 10.1 scraping_jobs

Background scraping job registry.

```sql
CREATE TABLE scraping_jobs (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_type      TEXT NOT NULL CHECK (job_type IN (
                  'FINANCIAL_SNAPSHOT', 'PRICE_SNAPSHOT',
                  'OWNERSHIP_SNAPSHOT', 'SECTOR_BENCHMARK', 'FULL_REFRESH'
                )),
  stock_id      UUID REFERENCES stocks(id),
  status        TEXT NOT NULL CHECK (status IN (
                  'PENDING', 'RUNNING', 'SUCCESS', 'FAILED', 'RETRYING', 'CANCELLED'
                )),
  priority      INTEGER NOT NULL DEFAULT 5,
  retry_count   INTEGER NOT NULL DEFAULT 0,
  max_retries   INTEGER NOT NULL DEFAULT 3,
  scheduled_at  TIMESTAMPTZ,
  started_at    TIMESTAMPTZ,
  completed_at  TIMESTAMPTZ,
  error_message TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_scraping_jobs_status ON scraping_jobs(status);
CREATE INDEX idx_scraping_jobs_stock_id ON scraping_jobs(stock_id);
CREATE INDEX idx_scraping_jobs_scheduled_at ON scraping_jobs(scheduled_at);
```

---

## 10.2 scraping_logs

Detailed scraping attempt audit trail.

```sql
CREATE TABLE scraping_logs (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id         UUID REFERENCES scraping_jobs(id),
  stock_id       UUID REFERENCES stocks(id),
  source         TEXT NOT NULL,
  status         TEXT NOT NULL CHECK (status IN ('SUCCESS', 'FAILED', 'PARTIAL', 'BLOCKED')),
  records_saved  INTEGER DEFAULT 0,
  latency_ms     INTEGER,
  error_message  TEXT,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_scraping_logs_job_id ON scraping_logs(job_id);
CREATE INDEX idx_scraping_logs_stock_id ON scraping_logs(stock_id);
CREATE INDEX idx_scraping_logs_status ON scraping_logs(status);
CREATE INDEX idx_scraping_logs_created_at ON scraping_logs(created_at DESC);
```

---

# 11. Automated Timestamps

Apply to all mutable tables via trigger:

```sql
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to all tables with updated_at:
CREATE TRIGGER trg_stocks_updated_at
  BEFORE UPDATE ON stocks
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_recommendations_updated_at
  BEFORE UPDATE ON recommendations
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_portfolios_updated_at
  BEFORE UPDATE ON portfolios
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_portfolio_holdings_updated_at
  BEFORE UPDATE ON portfolio_holdings
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_watchlists_updated_at
  BEFORE UPDATE ON watchlists
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();

CREATE TRIGGER trg_scraping_jobs_updated_at
  BEFORE UPDATE ON scraping_jobs
  FOR EACH ROW EXECUTE FUNCTION set_updated_at();
```

---

# 12. Entity Relationship Summary

```
stocks (1) ──< stock_financial_snapshots (many)
stocks (1) ──< stock_price_snapshots (many)
stocks (1) ──< stock_ownership_snapshots (many)
stocks (1) ──1 recommendations (one active)
stocks (1) ──< recommendation_history (many)
stocks (1) ──< ai_theses (many)
stocks (1) ──< ai_insights (many)
stocks (1) ──< alerts (many)
stocks (1) ──< scraping_jobs (many)
stocks (N) ──< watchlist_stocks >── watchlists (N)
stocks (N) ──< portfolio_holdings >── portfolios (N)
portfolios (1) ──< portfolio_snapshots (many)
sectors (1) ──< stocks (many)
sectors (1) ──< sector_benchmarks (many)
recommendations (1) ──< ai_theses (many)
scraping_jobs (1) ──< scraping_logs (many)
```

---

# 13. Historical Snapshot Strategy

## Rule

All snapshot tables are **append-only** (never updated):

- `stock_financial_snapshots`
- `stock_price_snapshots`
- `stock_ownership_snapshots`
- `recommendation_history`
- `portfolio_snapshots`

## Why

- enables thesis evolution tracking
- enables recommendation change history
- enables conviction drift analysis
- preserves auditability of the deterministic engine
- supports the Historical Thesis Tracking feature

## Freshness Tracking

Every financial snapshot includes:
- `data_source` — origin (Screener, Moneycontrol, NSE, etc.)
- `fetched_at` — when the raw data was scraped
- `freshness_score` — 0–100 quality confidence score

---

# 14. Data Integrity Rules

```sql
-- Prevent financial snapshots from having future dates
ALTER TABLE stock_financial_snapshots
  ADD CONSTRAINT chk_snapshot_date_not_future
  CHECK (snapshot_date <= CURRENT_DATE);

-- Ensure conviction score range
ALTER TABLE recommendations
  ADD CONSTRAINT chk_conviction_range
  CHECK (conviction_score BETWEEN 0 AND 10);

-- Ensure ownership adds up to approximately 100%
-- (enforced at application layer, not DB constraint due to rounding)
```

---

# 15. Supabase-Specific Notes

## Row Level Security (RLS)

MVP intentionally defers authentication.

RLS to be enabled post-MVP when multi-user architecture is introduced.

For MVP: RLS disabled, single-user access assumed.

## Realtime

Enable Supabase Realtime on:
- `alerts`
- `ai_insights`
- `recommendations`

This powers the live intelligence panel in the right panel.

## Storage

Supabase Storage (future use):
- annual report PDFs
- filing documents
- transcript uploads

## Migrations

Use Supabase CLI migrations:

```
supabase/migrations/
  20260101000001_create_stocks.sql
  20260101000002_create_financial_snapshots.sql
  20260101000003_create_recommendations.sql
  20260101000004_create_ai_tables.sql
  20260101000005_create_portfolio_tables.sql
  20260101000006_create_watchlist_tables.sql
  20260101000007_create_sector_tables.sql
  20260101000008_create_scraping_tables.sql
  20260101000009_create_triggers.sql
```

---

# 16. Non-Negotiables

- Financial logic MUST NOT live in the database
- AI output MUST NOT be the source of financial columns
- Snapshot tables MUST remain append-only
- All timestamps MUST use `TIMESTAMPTZ`
- All IDs MUST use `UUID` with `gen_random_uuid()`
- All columns MUST use `snake_case`
- All financial amounts MUST use `NUMERIC`, never `FLOAT`
