---
kind: concept
name: "Editorial design constraints"
status: seedling
added: "2026-08-11"
sources:
  - "[[literature/repos/cathrynlavery-diagram-design]]"
related_concepts: ["diagram-dsl-generation", "glanceability"]
related_experiments: []
tags: [design-system, constraints, svg, aesthetics, prompting]
---

# Editorial design constraints

## Definition

Imposing a tight, opinionated design system on LLM visual output through
prompt-level constraints — a fixed token palette with semantic roles, one
accent color reserved for 1–2 focal elements, a hard spatial grid (all
coordinates divisible by 4), hairline borders, capped radii, typography
assigned by role — so that free-form SVG/HTML stops looking
"AI-generated" and starts looking editorially designed.

## Why it matters here

Our baseline matrix showed free-form visual approaches (03-svg-infographic)
scoring *below* prose: compression cost accuracy without buying
glanceability. The diagram-design repo's bet is that the failure mode is
not free-form SVG per se but *unconstrained* free-form SVG, and that a
small set of mechanical rules (4px grid, single accent, density 4/10,
"deletion is the highest-quality move") recovers professional quality.
This is directly testable in our harness: approach 08 is 03 re-run under
these constraints, so the delta isolates the value of the design system.

Also notable: the accent-discipline rule ("1–2 focal elements the reader
should look at first") is a concrete design lever for the glance axis —
it operationalizes attention steering without animation.

## Connections

- Sits at the opposite pole from [[diagram-dsl-generation]]: full layout
  freedom with style constrained, vs. constrained structure with style
  delegated to a renderer.
- [[glanceability]] — accent discipline and density caps are exactly the
  "holistic encodings, low element counts, clear targets" levers.
- If approach 08 beats 03 cleanly, the constraint set should be considered
  for *all* HTML-emitting approaches (it is orthogonal to layout method).
