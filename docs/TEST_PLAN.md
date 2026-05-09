# TEST_PLAN.md

# AI Investment Research Terminal

Testing & Quality Assurance Strategy

Version: 0.1

---

# 1. Testing Philosophy

The system must prioritize:

* deterministic consistency
* explainability
* financial correctness
* AI reliability
* scraping stability
* API contract integrity
* historical reproducibility

This is NOT a typical SaaS app.

Incorrect recommendations or inconsistent scoring are considered:

> **critical failures.**

---

# 2. Core Testing Layers

The platform must test:

1. deterministic financial engine
2. scoring consistency
3. AI hallucination prevention
4. scraping reliability
5. API contracts
6. historical persistence
7. caching behavior
8. portfolio intelligence
9. sector-aware logic

---

# 3. Deterministic Engine Testing

## Objective

Ensure financial calculations remain reproducible, explainable, and deterministic.

## Validate

* ROE calculations
* ROCE calculations
* debt/equity calculations
* PE/PB normalization
* conviction scoring
* recommendation thresholds

## Critical Rule

Identical input datasets MUST produce identical recommendations, identical scores, and identical signals.

---

# 4. Recommendation Consistency Tests

## Validate

* recommendation thresholds
* score weighting
* sector-aware adjustments
* risk penalties

## Example Test Cases

| Scenario                   | Expected            |
| -------------------------- | ------------------- |
| High ROCE + low debt       | BUY/STRONG_BUY      |
| Weak cash flow + high debt | HOLD/SELL           |
| Conflicting metrics        | MODERATE confidence |

---

# 5. AI Hallucination Prevention Tests

## Objective

Ensure AI never invents metrics, fabricates risks, or contradicts deterministic outputs.

## Validate

* AI references supplied metrics only
* AI preserves recommendation truth
* AI uses probabilistic language
* AI avoids certainty claims

## Forbidden Output Tests

Reject outputs containing:

* guaranteed returns
* unsupported growth claims
* fabricated valuation metrics

---

# 6. Scraping Reliability Tests

## Validate

* parsing reliability
* fallback source logic
* retry behavior
* stale-data handling
* normalization consistency

## Simulated Failure Tests

| Failure        | Expected Behavior        |
| -------------- | ------------------------ |
| NSE timeout    | fallback source          |
| malformed HTML | graceful parsing failure |
| stale cache    | stale response warning   |

---

# 7. API Contract Testing

## Objective

Ensure frontend/backend consistency.

## Validate

* response shapes
* typed payloads
* pagination format
* error formats
* cache metadata

## Critical Rule

APIs must NEVER: change field names unexpectedly, return malformed JSON, or omit required metadata.

---

# 8. Portfolio Intelligence Testing

## Validate

* allocation calculations
* concentration warnings
* conviction-weighted summaries
* risk exposure logic

## Example

If 70% portfolio is in IT → expected: sector concentration warning.

---

# 9. Sector-Aware Logic Testing

## Objective

Ensure sector-specific rules apply correctly.

## Validate

* sector detection
* sector scoring overrides
* KPI interpretation

## Example

Banks: GNPA, CASA, NIM must influence scoring.

---

# 10. Historical Snapshot Testing

## Validate

* snapshots append correctly
* recommendations preserve history
* AI theses remain versioned
* old data never overwritten

## Critical Rule

Historical financial truth must remain immutable.

---

# 11. Caching Tests

## Validate

* Redis cache hits
* invalidation logic
* stale cache handling
* AI response caching

## Expected Behavior

Cache should: improve latency, preserve correctness, and invalidate intelligently.

---

# 12. Performance Testing

## Latency Targets

| Operation       | Target       |
| --------------- | ------------ |
| Cached analysis | < 1.5s       |
| Fresh analysis  | < 3s         |
| API responses   | < 500ms      |
| Command palette | near-instant |

## Validate

* concurrent requests
* large portfolio loading
* recommendation generation latency

---

# 13. Frontend Testing

## Validate

* narrative-first rendering
* recommendation visibility
* responsive layouts
* command palette behavior
* keyboard accessibility

## UI Rules

The UI must NEVER: hide risks, overload charts, or clutter recommendation visibility.

---

# 14. Security Testing

## Validate

* secrets isolation
* API key protection
* prompt sanitization
* malformed input handling

## Critical Rule

No secrets should EVER leak client-side, appear in logs, or appear in prompts.

---

# 15. Regression Testing

## Objective

Prevent scoring drift, recommendation inconsistencies, and API contract breakage.

## Re-Test On

* scoring changes
* prompt changes
* schema changes
* ingestion changes

---

# 16. Monitoring Validation

## Validate

* scraping logs
* AI failures
* retry frequency
* latency spikes
* cache failures

---

# 17. Future Testing Expansion

* autonomous AI evaluation
* portfolio simulation testing
* semantic search testing
* transcript analysis testing

---

# 18. Final Testing Principle

The platform must always prioritize:

* deterministic trust
* explainability
* reproducibility
* financial correctness

over: flashy features, rapid UI iteration, and experimental AI behavior.
