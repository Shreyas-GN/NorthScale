# DESIGN.md

# AI Investment Research Terminal

Design System & UX Architecture

Version: 0.1
Design Philosophy: AI-Native Institutional Web3 Intelligence
Platform: Web
Theme: Dark-First

---

# 1. Design Philosophy

The application should feel like:

> “A private AI hedge-fund terminal redesigned with modern Web3 aesthetics.”

The interface must combine:

* institutional trust
* AI-native interactions
* futuristic visual depth
* premium fintech polish
* calm information density

The design should NEVER feel like:

* a traditional stock website
* a 1998 finance dashboard
* a noisy crypto casino
* an enterprise ERP
* a cluttered analytics panel

The system should instead feel:

* intelligent
* alive
* responsive
* modern
* layered
* cinematic
* minimal
* premium

---

# 2. Core UX Philosophy

# Narrative First

The interface prioritizes:

1. AI reasoning
2. contextual intelligence
3. investment thesis
4. supporting signals
5. raw metrics last

Users should understand:

* WHY a stock matters
* WHY conviction changed
* WHY risk increased

before being overwhelmed with numbers.

---

# 3. Design Inspirations

# Primary Design Systems

## Linear

Use for:

* layout rhythm
* spacing precision
* information hierarchy
* tab systems
* sidebar structure

---

## Raycast

Use for:

* command palette UX
* keyboard-first workflows
* AI interaction feel
* floating overlays

---

## Cursor

Use for:

* AI-native workflows
* modern intelligence surfaces
* contextual AI interactions

---

## Stripe

Use for:

* fintech polish
* premium typography
* sophisticated spacing
* elegant cards

---

## Supabase

Use for:

* Web3-style dark aesthetics
* subtle glow systems
* futuristic depth
* layered surfaces

---

## Claude

Use for:

* readable AI narratives
* editorial layouts
* calm information presentation

---

# 4. Visual Identity

# Core Identity

The visual identity should feel:

* stealth wealth
* institutional intelligence
* futuristic minimalism
* premium dark luxury
* high-trust fintech

---

# Emotional Keywords

Use constantly:

* intelligent
* calm
* premium
* futuristic
* focused
* layered
* cinematic
* precise
* analytical
* modern

Avoid:

* playful
* meme-like
* chaotic
* overly colorful
* retail-trader energy

---

# 5. Theme System

# Primary Theme

Dark-first.

NOT pure black.

The application should use:

* graphite surfaces
* layered shadows
* blurred depth
* soft gradients
* glassmorphism accents

---

# Surface Philosophy

Surfaces should feel:

* floating
* dimensional
* soft-lit
* layered

NOT:

* flat
* boxed
* corporate
* spreadsheet-like

---

# 6. Color System

# Core Backgrounds

Canvas:
#07090d

Primary Surface:
#0f1117

Secondary Surface:
#151922

Elevated Surface:
#1b2230

Hover Surface:
#232c3d

Overlay Surface:
rgba(15, 17, 23, 0.72)

---

# Border Colors

Hairline:
#283142

Strong Border:
#364153

Glow Border:
rgba(107, 124, 255, 0.28)

---

# Typography Colors

Primary:
#f5f7fb

Secondary:
#c5cede

Muted:
#8b97ab

Disabled:
#5f6878

---

# Accent Colors

# Primary Accent

Lavender Blue:
#6b7cff

Used for:

* active states
* focus rings
* AI highlights
* command palette
* selected tabs

---

# Secondary Accent

Electric Cyan:
#4fd1ff

Used sparingly for:

* AI glow
* premium gradients
* hover accents

---

# Semantic Colors

BUY:
#4ade80

HOLD:
#fbbf24

SELL:
#f87171

WATCHLIST:
#60a5fa

RISK:
#fb7185

---

# Gradient Philosophy

Gradients must remain:

* subtle
* premium
* low-opacity
* blurred

Allowed:

* graphite gradients
* indigo glows
* cyan edge lighting
* emerald highlights

NOT allowed:

* rainbow gradients
* oversaturated neon
* gaming aesthetics

---

# 7. Typography System

# Primary Font

Geist Sans

Fallback:
Inter

---

# Mono Font

Geist Mono

Used for:

* financial metrics
* command palette
* ticker symbols
* AI reasoning metadata

---

# Typography Philosophy

Typography must feel:

* precise
* calm
* technical
* premium

Use:

* tight tracking
* medium font weights
* large readable spacing

Avoid:

* giant bold headlines
* excessive uppercase
* tiny finance text

---

# Typography Scale

Display XL:
72px

Display Large:
56px

Heading 1:
40px

Heading 2:
32px

Heading 3:
24px

Body Large:
18px

Body:
16px

Caption:
13px

Micro:
11px

---

# 8. Layout Architecture

# Global Structure

```txt id="layoutsystem"}
LEFT SIDEBAR
MAIN CONTENT
RIGHT INTELLIGENCE PANEL
```

---

# Layout Philosophy

The application should feel:

* OS-like
* immersive
* layered
* intelligent

NOT:

* webpage-like
* dashboard-grid-heavy

---

# Sidebar

Width:
280px

Style:

* floating
* blurred
* semi-transparent
* glassmorphism-light

Contains:

* Portfolio
* Watchlists
* Alerts
* AI Queries
* Sectors
* Settings

Behavior:

* collapsible
* keyboard navigable
* icon-first

---

# Main Content Area

Primary analysis region.

Contains:

* stock header
* AI recommendation
* conviction score
* thesis
* financial tabs
* charts
* historical intelligence

---

# Right Intelligence Panel

Sticky contextual intelligence feed.

Contains:

* AI observations
* ownership changes
* risk alerts
* earnings updates
* recommendation shifts
* valuation alerts

This panel should feel:

> “alive”

without becoming noisy.

---

# 9. Card Design System

# Card Philosophy

Cards should:

* float subtly
* feel layered
* use soft depth
* avoid heavy borders

NOT:

* flat white rectangles
* enterprise panels
* spreadsheet boxes

---

# Card Style

Background:
rgba(21, 25, 34, 0.72)

Backdrop Blur:
20px

Border:
1px solid rgba(255,255,255,0.06)

Radius:
22px

Shadow:
0 10px 40px rgba(0,0,0,0.28)

---

# Card Variants

## Standard Card

Normal content sections.

## Glow Card

Used for:

* recommendation
* AI insights
* portfolio intelligence

## Overlay Card

Floating command palette / modals.

---

# 10. Motion System

# Motion Philosophy

Motion should feel:

* intelligent
* fluid
* precise
* responsive

NOT:

* playful
* bouncy
* exaggerated

---

# Allowed Motion

* soft fades
* blur transitions
* glow fades
* hover elevation
* smooth tab transitions
* subtle scaling
* intelligent panel transitions

---

# Duration

120ms–220ms

---

# Easing

cubic-bezier(0.16, 1, 0.3, 1)

---

# Forbidden Motion

* bouncing cards
* overshooting springs
* exaggerated parallax
* crypto-casino effects
* flashing glows
* constant animations

---

# 11. AI-First UX

# Core Principle

The app is:

# AI-FIRST

NOT:

# dashboard-first

---

# Every Stock Page Must Begin With

1. Recommendation
2. Conviction
3. AI Thesis
4. Key Risks
5. Key Signals

ONLY THEN:

* detailed metrics
* peer comparisons
* charts
* filings

---

# Recommendation Card

This is the HERO component.

Contains:

* BUY / HOLD / SELL
* conviction score
* AI thesis
* confidence level
* supporting signals

Visual:

* subtle glow
* premium gradient
* elevated depth

NOT:

* giant casino green/red blocks

---

# 12. Command Palette

Inspired by:

* Raycast
* Cursor

Shortcut:
⌘K

---

# Capabilities

* Analyze stock
* Compare companies
* Search sectors
* Run AI queries
* Open portfolio
* Trigger re-analysis

---

# Style

* floating overlay
* blurred glass
* instant search
* keyboard-first
* AI suggestions

---

# 13. Dashboard Philosophy

# NOT Widget Chaos

Avoid:

* 100 tiny cards
* too many charts
* dense spreadsheets
* TradingView-style overload

Instead:

* narrative grouping
* intelligent hierarchy
* contextual presentation

---

# Dashboard Structure

Top:

* portfolio intelligence
* alerts
* recommendation changes

Middle:

* AI insights
* market observations

Bottom:

* deeper metrics
* watchlists
* historical movement

---

# 14. Tables

Tables must feel:

* institutional
* readable
* elegant

NOT:

* Excel clones

---

# Table Rules

* larger row heights
* muted separators
* sticky headers
* soft hover states
* no excessive borders

---

# 15. Charts

Charts are SECONDARY.

Rules:

* minimal
* dark themed
* low-clutter
* subtle gridlines

Preferred:

* muted indigo
* cyan accents
* emerald highlights

Avoid:

* rainbow charts
* overloaded indicators
* trading chaos

---

# 16. Glassmorphism Rules

Glass effects should be:

* subtle
* layered
* premium

Use ONLY for:

* overlays
* sidebars
* floating panels
* command palette

Avoid:

* excessive transparency
* blurry unreadable text

---

# 17. Spacing System

Base Unit:
4px

Scale:
4
8
12
16
24
32
48
64
96

---

# 18. Radius System

Small:
10px

Medium:
16px

Large:
22px

XL:
28px

Pill:
9999px

---

# 19. Shadows & Glow

# Philosophy

Depth should come from:

* soft lighting
* layered shadows
* subtle glows

NOT:

* harsh drop shadows

---

# Glow Usage

Allowed ONLY for:

* active states
* AI highlights
* recommendation card
* focused interactions

---

# 20. Responsive Behavior

# Desktop

Full:

* sidebar
* main panel
* intelligence panel

---

# Tablet

Collapse:

* right panel
* reduce sidebar width

---

# Mobile

Convert to:

* stacked layout
* bottom navigation
* swipe sections

Narrative-first structure MUST remain preserved.

---

# 21. Accessibility

Minimum:
WCAG AA

Requirements:

* high contrast text
* visible focus states
* keyboard navigation
* readable charts
* accessible touch targets

---

# 22. Design Non-Negotiables

# NEVER

* use generic dashboard templates
* create widget overload
* use crypto casino aesthetics
* overload charts
* clutter layouts
* prioritize metrics over intelligence

---

# ALWAYS

* prioritize narrative clarity
* preserve calm interfaces
* maintain futuristic elegance
* emphasize AI intelligence
* keep layouts breathable
* use layered depth carefully

---

# 23. Final Experience Goal

The final experience should feel like:

> “A billionaire investor’s private AI terminal.”

Users should feel:

* empowered
* informed
* intelligent
* calm
* in control

The application should consistently communicate:

* trust
* sophistication
* speed
* intelligence
* precision

without ever feeling:

* overwhelming
* noisy
* speculative
* chaotic
