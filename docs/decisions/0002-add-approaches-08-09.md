# 0002 — Add approaches 08 (editorial diagrams) and 09 (motion explainer)

- status: accepted
- date: 2026-08-11

## Context

Two external repos were ingested as design sources
([[literature/repos/cathrynlavery-diagram-design]],
[[literature/repos/3b1b-manim]]), each carrying a coherent visual
philosophy absent from the Phase 1 approach set:

- **diagram-design** (Cathryn Lavery): an editorial design system for
  hand-authored SVG diagrams — single accent color on 1–2 focal
  elements, 4px spatial grid, hairlines/no shadows, density ~4/10,
  deletion-first. Its artifact contract (self-contained HTML+SVG, no JS,
  no external assets) matches ours almost exactly.
- **manim** (3Blue1Brown): the explanatory-animation grammar —
  sequential revelation of one persistent scene, morphs between
  representations, motion only where it encodes meaning.

The baseline matrix left an open question these speak to directly:
free-form SVG (03) scored *below* prose — is hand-authored visual layout
a dead end, or was it merely unconstrained?

## Decision

Add two approaches, leaving all existing specs untouched at version 1:

- **08-editorial-diagrams** — 03's medium (free-form inline SVG) under
  diagram-design's constraint system. The 03 vs 08 delta isolates the
  value of editorial design constraints; the 02 vs 08 delta compares
  renderer-laid-out DSL diagrams against hand-laid-out constrained ones
  (both at ≤150 words non-caption prose).
- **09-motion-explainer** — the manim grammar ported to the static
  contract: inline SVG + vanilla JS stepper, no video, no build step.
  First paint is the completed final frame so the glance axis is not
  gated on pressing play. Manim is used as a design language, not a
  toolchain.

This is additive: baseline-matrix comparisons among approaches 01–07
remain valid. The next matrix run covers 08–09 × all 6 test cases
(12 new cells); re-running 01–07 is optional (specs unchanged, but a
same-day generation batch controls for model drift if we want clean
cross-approach ranks).

## Consequences

- Concepts seeded: [[editorial-design-constraints]],
  [[animation-as-explanation]]; if 08 validates the constraint set, it
  should be trialed as an overlay on *all* HTML-emitting approaches.
- 09 tests the glance-vs-studied-comprehension split explicitly; a low
  glance / high depth result is a finding, not a failure.
- **Deferred (Phase 2 option):** using manim as an actual renderer
  (Python → video/frames embedded in the page) requires a contract
  revision — it violates "no build step" and would need video/image
  embedding rules. Revisit only if 09's static port shows motion has
  value worth the pipeline cost.
