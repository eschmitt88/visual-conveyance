---
kind: concept
name: "Glanceability"
status: seedling
added: "2026-07-01"
sources:
  - "[[literature/papers/while2024glanceable]]"
related_concepts: ["llm-as-judge-for-visuals"]
related_experiments: []
tags: [perception, glanceability, comprehension, evaluation]
---

# Glanceability

## Definition

The property of a visual artifact that lets a viewer extract its intended information in a single brief exposure — operationally, the minimum exposure time at which a viewer performs the reading task above chance, measured per encoding type and complexity level.

## Why it matters here

Glance comprehension by non-experts is one of the two axes of our whole evaluation. Empirical anchors so far (While et al., CHI '24, smartwatch-scale 2AFC comparisons):

- Thresholds are real and type-dependent, spanning an order of magnitude: donut ~220–410 ms, bar ~380–700 ms, radial ~1.1–3.6 s (older adults; younger ~1.3–1.6x faster). A bad encoding choice costs ~7x in glance time.
- Encodings readable holistically/peripherally (proportion color patches, position/length) are glanceable; encodings requiring serial tracing (arcs, nested rings) are not — some become effectively unusable (participants quit; accuracy below staircase expectation).
- Element count is a budget: thresholds grow with 7→12→24 elements, and gaps widen for weaker readers.
- Audiences are heterogeneous: 65–74-year-olds perform near younger adults, 75+ decline sharply — "the non-expert reader" must be specified, not assumed.

Caveat: these thresholds cover minimal comparison tasks; message-level comprehension of a full presentation needs longer exposures (smartwatch sessions ~<5 s is a useful budget framing).

## Connections

- The glance axis of the two-axis eval; [[llm-as-judge-for-visuals]] must approximate these perceptual thresholds when estimating "what a reader gets in 5 seconds" — and whether MFM perception matches human glance perception is an open alignment question.
- Design levers for approaches: holistic encodings, low element counts, clear targets.
