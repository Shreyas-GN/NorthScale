# Global Engineering Rules

# Core Philosophy

This project is an institutional-grade AI investment research terminal.

The application must prioritize:

* explainability
* deterministic trust
* modularity
* narrative-first UX
* maintainability
* calm interfaces
* institutional quality

---

# General Engineering Rules

## ALWAYS

* use TypeScript strictly
* use fully typed APIs
* prefer composition over duplication
* create modular feature-based architecture
* separate UI from business logic
* use reusable utilities
* use async-safe patterns
* use clear naming conventions
* optimize for readability first

---

## NEVER

* hardcode financial calculations inside components
* mix AI logic with UI rendering
* duplicate business logic
* directly fetch external APIs from frontend
* create monolithic files
* use `any` types unnecessarily
* bypass validation
* use magic numbers

---

# Architecture Rules

Business logic belongs ONLY in:

* backend services
* engines
* utility layers

NOT:

* UI components
* pages
* layouts

---

# Financial Data Rules

Financial truth must ALWAYS come from:

* deterministic calculations
* validated datasets
* normalized scraped data

AI must NEVER generate authoritative financial truth.

---

# AI Rules

AI is responsible ONLY for:

* narrative synthesis
* explainability
* contextual reasoning
* summarization

AI must NEVER:

* fabricate metrics
* invent valuation data
* generate certainty claims

---

# Performance Rules

Prioritize:

* responsiveness
* caching
* progressive rendering
* background processing

Avoid:

* blocking requests
* unnecessary rerenders
* excessive animations

---

# UI Philosophy

The UI must remain:

* calm
* premium
* narrative-first
* minimal
* layered
* futuristic
* institutional

Avoid:

* dashboard clutter
* crypto casino aesthetics
* excessive charts
* visual noise

---

# Code Quality Rules

## File Size

Avoid files larger than:

* 250 lines for components
* 400 lines for services

Split aggressively into modules.

---

# Naming Conventions

## Components

PascalCase

## Hooks

useSomething

## Constants

UPPER_SNAKE_CASE

## Database

snake_case

## APIs

kebab-case

---

# Documentation Rules

All major systems must include:

* purpose
* inputs
* outputs
* constraints
* edge cases

---

# Final Principle

The application should always feel like:

> "A private institutional AI investment terminal."

NOT:

* a retail trading app
* a crypto dashboard
* a generic AI wrapper
