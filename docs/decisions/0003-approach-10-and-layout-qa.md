# 0003 — Approach 10 (combined, free-choice) and the layout-QA gate

- status: accepted
- date: 2026-08-12

## Context

First qualitative human pass over approaches 01–09
(`eval/human-feedback-2026-08-12.md`) found: 09's progressive
disclosure works; context-free numeric stat cards fail; plain text's
linearity is a real advantage; hover-only interactivity is often
pointless; diagrams keep shipping with overlapping/clipped elements.
The owner asked for (a) an approach that may use any of the tools
explored so far with only a nudge about availability, and (b) a robust
self-checking tool for diagram layout.

On (b): no suitable off-the-shelf tool exists for rendered HTML+SVG
pages — Stencila's `lint-svg` estimates text boxes from character
counts without rendering, and visual-regression tools (Percy et al.)
only diff against prior screenshots. The bounding-box-intersection
approach from the diagram-eval literature applied to *real* Chromium
client rects is strictly more accurate and fits our existing
Playwright harness.

## Decision

1. **`tools/layout_check.py`** — renders each page in Chromium and
   reports ERROR-level `OVERLAP` (SVG text-text intersection > 3px both
   axes and >10% of the smaller box), `CLIPPED` (text escaping the SVG
   client box), `H_OVERFLOW` (page-level horizontal scroll at 1440 or
   390 width), and warning-level `SMALL_TEXT` (<9px). Validated against
   run-2 ground truth: reproduces every evaluator-cited collision
   (diffusion×09, research×09), agrees on clean pages, and found one
   collision the evaluator missed (codebase×08).
2. **`approaches/10-combined.md`** — free choice: lists the available
   channels (prose, Mermaid, hand SVG, KaTeX, CSS, vanilla JS) with no
   method prescription beyond the contract. The human-feedback lessons
   are deliberately NOT encoded in the spec — 10 tests what the
   generator chooses unguided; feeding it the owner's preferences would
   contaminate that question.
3. **Protocol amendment for 10 only**: the generator may run
   `tools/layout_check.py` on its own output and iterate until clean.
   This is mechanical QA (like "the Mermaid must render"), not design
   guidance. Generators still never see key_facts, other approaches, or
   other cells.
4. The layout checker also becomes a **harness gate** for future runs
   of any approach: a page failing with ERRORs gets one regeneration
   with the report appended, mirroring the blank-screenshot gate.

## Consequences

- 01–09 comparisons remain valid (additive change; existing specs
  untouched).
- 10's cells are generated with layout QA that 01–09's cells did not
  have; when comparing visual_craft across approaches, note that
  advantage.
- If 10 ≥ best prescribed approach, Phase 1's product is a toolbox +
  contract + QA gate, not a method spec. If 10 loses, prescription
  itself is load-bearing — either way the run is informative.
