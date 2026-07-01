---
kind: experiment
slug: "baseline-matrix"
date: "2026-07-01"
status: running     # running | done | abandoned
hypothesis: "Visual presentation approaches differ measurably in glance comprehension and accuracy; at least one visual approach beats the prose control on overall score, and no single approach wins across all six material types."
result: ""
related_concepts: ["glanceability", "llm-as-judge-for-visuals", "diagram-dsl-generation"]
related_literature: []
tags: [visual-conveyance, matrix, ai-eval, phase-1]
---

# baseline-matrix

## Hypothesis

State precisely what we expect, before running anything:

1. Every visual approach (02–07) beats the prose control (01) on
   `glance_comprehension`, averaged over test cases.
2. At least one approach beats prose on `overall` (which weights
   accuracy most) — i.e. visuals don't have to cost accuracy.
3. There is an approach × material interaction: diagram-centric
   approaches win on structural material (codebase, incident), while
   density-honest approaches (layered dashboard) win on nuanced
   material (experiment-results, tradeoff-decision).
4. The infographic approach (03) shows the largest gap between
   `glance_comprehension` and `accuracy` (compression costs fidelity).

## Setup

- Config: `config.yaml` (matrix definition, generator/evaluator model,
  input git SHA)
- Code: `tools/screenshot.py` (rendering); generation and evaluation
  are subagent runs driven from the session, prompts defined by
  `approaches/*.md` and `eval/rubric.md` v1.
- Data: `testcases/*/` (source + held-out key_facts), all tracked in
  git (small text).
- Artifacts: `docs/presentations/<testcase>/<approach>/index.html`
  (+ glance.png/full.png) — served by GitHub Pages.
- Evals: `results/evals/<testcase>--<approach>.json`; aggregates in
  `metrics.json` (AI scores = search signal). Human ratings land in
  `results/human/` and are the authoritative signal.

## Result

Fill in after the run.

## Interpretation

Fill in after the run.

## Diagnostics

Fill in after the run. One line per field; leave `n/a` rather than
blank. `next_candidates` must list ≥2 concrete one-sentence proposals.
Every concrete claim below needs a **citation anchor** — a code
reference, a metrics file path like `metrics.json:by_approach`, or a
wikilink into `literature/`.

Unless otherwise noted, metric numbers here reference `metrics.json`
(AI-evaluator scores). Human ratings in `results/human/` are reported
separately once collected.

- intended_effect_confirmed: n/a
- leakage_check: n/a
- overfitting_signal: n/a
- delta_from_prior: n/a
- unexpected_findings: n/a
- next_candidates:
  - n/a
  - n/a

## Follow-up

- Collect human ratings via the gallery; compare AI vs human ranking
  (rank correlation) — disagreement is itself a Phase 1 finding.
