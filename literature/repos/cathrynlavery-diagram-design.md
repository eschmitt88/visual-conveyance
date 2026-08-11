---
kind: repo
name: "diagram-design (Cathryn Lavery)"
url: https://github.com/cathrynlavery/diagram-design
commit:
source: "raw/repos/cathrynlavery-diagram-design.md"
added: "2026-08-11"
relevance: 5
status: explored
related_experiments: []
related_concepts: ["editorial-design-constraints", "diagram-dsl-generation", "glanceability"]
tags: [diagrams, svg, design-system, editorial, claude-skill, hand-authored]
institutions: ["independent (Cathryn Lavery / BestSelf.co)"]
peer_reviewed: false
code_url: https://github.com/cathrynlavery/diagram-design
citations: null
credibility: 3
---

# diagram-design (Cathryn Lavery)

## Purpose

A Claude Code skill that makes LLMs produce *editorial-quality* diagrams as
self-contained HTML+SVG — 27 diagram types (architecture, flowchart,
sequence, swimlane, quadrant, layers, pyramid, radar, loop/flywheel, Gantt,
ER, …) — instead of the "generic rounded-box thing" LLMs draw by default.
The core bet: a tight, opinionated design system, enforced through prompt
constraints, is what separates professional-looking output from
AI-slop output.

## Shape

- `SKILL.md` — philosophy, type-selection guide, checklist. Progressive
  disclosure: only the chosen type's reference file is loaded per task.
- `references/type-<name>.md` × 27 — per-type grammar and layout rules.
- `references/style-guide.md` — single source of truth for color/font
  tokens (semantic roles: paper, ink, muted, accent, link).
- `primitives/` — annotation callouts (italic serif + dashed Bézier
  leader), sketchy hand-drawn SVG filter, terminal-window frame, 55
  monochrome `currentColor` icons.
- Onboarding flow maps a website's palette/fonts onto the semantic tokens,
  with automatic WCAG AA contrast checks at diagram type sizes (9–12px).
- `scripts/lint-skin.py` — deterministic skin-compliance lint.

## Useful bits — the design system itself

The distilled rules (README + SKILL.md) are directly liftable into an
approach spec:

- **One accent color, 1–2 focal elements per diagram.** The accent is
  reserved for what the reader should look at first. Everything else is
  ink/muted/hairline.
- **"The highest-quality move is usually deletion."** Every node earns its
  place; target density 4/10.
- **4px grid** — every coordinate, width, and gap divisible by 4; named as
  the single biggest de-AI-ifying constraint.
- **1px hairline borders, no shadows, border-radius ≤10px.**
- Three type roles: serif for titles/editorial callouts, sans for node
  names, mono *only* for technical sublabels (ports, URLs, field types) —
  not a blanket dev aesthetic.
- Self-contained HTML, no JS, no external images — same artifact contract
  as ours.
- Explicit anti-use guidance: lists → table; one-shape diagrams → a
  sentence. "Would a reader learn more from this than from a well-written
  paragraph?"

## Follow-up

**Relevance:** 5 — directly seeds [[editorial-design-constraints]] and is
the basis of a new generation approach (08); its artifact contract
(self-contained HTML+SVG, no JS, no external assets) matches ours almost
exactly, and it stakes out the free-form-SVG end of the design space where
our 03-svg-infographic underperformed.

## Trust signals

**Credibility:** 3 — independent practitioner (no peer review, no
citations), but the entire artifact set is released and directly
inspectable (27×3 example pages, lint script, gallery), so reproducibility
is maximal; the claims are design opinions we will test, not empirical
results we must trust.
