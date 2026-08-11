---
kind: repo
name: "manim (3b1b / ManimGL)"
url: https://github.com/3b1b/manim
commit:
source: "raw/repos/3b1b-manim.md"
added: "2026-08-11"
relevance: 4
status: scanned
related_experiments: []
related_concepts: ["animation-as-explanation", "glanceability"]
tags: [animation, math-visualization, 3blue1brown, python, explanatory]
institutions: ["independent (Grant Sanderson / 3Blue1Brown)"]
peer_reviewed: false
code_url: https://github.com/3b1b/manim
citations: null
credibility: 5
---

# manim (3b1b / ManimGL)

## Purpose

"An engine for precise programmatic animations, designed for creating
explanatory math videos" — the tool behind 3Blue1Brown. Two lineages:
this repo (ManimGL, Grant Sanderson's personal version) and the
community fork (ManimCE, more stable/tested). Python 3.10+, renders via
FFmpeg/OpenGL, optional LaTeX.

## Shape

- Scene-based API: a `Scene` class per animation; `manimgl file.py
  SceneName` renders it. Flags for write-to-file, final-frame-only,
  skip-to-nth-animation.
- `example_scenes.py` + the 3b1b/videos repo (all video code public)
  are the corpus of the visual grammar in practice.
- `custom_config.yml` for output, style, and quality defaults.

## Useful bits — the explanatory grammar, not the renderer

Under our Phase 1 contract (single static HTML, no build step) we cannot
run manim in the generation pipeline. What transfers is the *grammar*
that made 3Blue1Brown the reference point for explanation-by-animation:

- **Sequential revelation**: a scene starts nearly empty and elements are
  written/drawn/faded in one at a time, so attention is steered — the
  viewer never faces the finished complex figure cold.
- **Transformation over substitution**: when a representation changes
  (equation → graph, matrix → geometric action), the old form *morphs*
  into the new one, visually asserting "these are the same thing."
- **One persistent scene**, camera moves and zooms instead of slide cuts;
  spatial continuity carries the argument's thread.
- **Precision**: animations are computed from the actual math/data, never
  decorative easing on stock shapes — motion is only used where it encodes
  meaning.
- Recognizable austere aesthetic: dark canvas, few saturated hues each
  with a consistent semantic binding, math set properly (KaTeX suffices
  for us).

All of this is reproducible in a static page with inline SVG + CSS/Web
Animations driven by a stepper — which is what approach 09 does.

## Follow-up

**Relevance:** 4 — seeds [[animation-as-explanation]] and grounds a new
approach (09) that ports the manim grammar to the static-HTML contract.
Not a 5 because the tool itself is unusable under the Phase 1 contract
(build step, video output); a manim-rendered-video approach would need a
contract revision (noted in ADR 0002 as a Phase 2 option).

## Trust signals

**Credibility:** 5 — canonical open-source project (MIT) by the field's
best-known practitioner of explanatory animation; fully released code,
massive community (dedicated subreddit/Discord, community fork), and a
decade of published output demonstrating the grammar works.
