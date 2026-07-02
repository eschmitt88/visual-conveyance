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

AI-evaluation phase complete (42/42 cells, rubric v1, `metrics.json`).
Ranking by mean overall: **layered-dashboard 9.02** > interactive-explainer
8.73 > visual-metaphor 8.43 > scrolly-slides 8.23 > **prose control 7.95** >
svg-infographic 7.38 > mermaid-diagrams 7.30. Layered-dashboard won 5 of 6
test cases outright (interactive-explainer took research-project by 0.1).
Human ratings: pending (0/42) — gallery at
https://eschmitt88.github.io/visual-conveyance/presentations/.

## Interpretation

Per the AI judge (all anchors in `metrics.json`):

- **H1 (all visuals beat prose on glance): partial.** Dashboard (8.67),
  interactive (8.05), metaphor (7.67), slides (7.00) beat prose (6.92);
  infographic and mermaid (both 6.58) LOST to well-structured prose at
  a glance — the two "most visual" approaches underdelivered.
- **H2 (a visual approach beats prose on overall): confirmed.** Four do.
- **H3 (approach × material interaction, no universal winner): refuted**
  at this granularity — layered-dashboard was near-universal. Caveat:
  a single-model judge may systematically favor progressive disclosure
  (everything present + designed glance layer scores well on every
  rubric axis); this is exactly what the human pass should test.
- **H4 (infographic trades accuracy for glance): half right.** Its
  accuracy did crater (8.02, lowest tier) but the glance payoff never
  materialized (6.58). Compression cost fidelity without buying
  glanceability. Mermaid failed similarly: diagram-DSL pages rendered
  small/unlegible-at-a-glance diagrams (see codebase-structure--02 eval).
- Prose is a strong baseline on accuracy (9.88) — visuals mainly move
  the glance axis, which was the motivating axis of this project.

## Diagnostics

Fill in after the run. One line per field; leave `n/a` rather than
blank. `next_candidates` must list ≥2 concrete one-sentence proposals.
Every concrete claim below needs a **citation anchor** — a code
reference, a metrics file path like `metrics.json:by_approach`, or a
wikilink into `literature/`.

Unless otherwise noted, metric numbers here reference `metrics.json`
(AI-evaluator scores). Human ratings in `results/human/` are reported
separately once collected.

- intended_effect_confirmed: partial — visuals beat prose overall (metrics.json:approach_ranking_by_overall) but H1/H3 deviations noted in Interpretation
- leakage_check: generators never saw key_facts.md (eval/protocol.md separation); evaluators never saw approach specs — enforced by prompt contract, spot-checked in agent transcripts
- overfitting_signal: n/a for this run — single-pass matrix, no iteration on the eval signal yet; guard is the pending human pass (results/human/)
- delta_from_prior: n/a — first experiment in project
- unexpected_findings: the two most "visual" approaches (infographic, mermaid) scored WORST — below the prose control on glance (metrics.json:by_approach); dashboard's near-universal win may be judge bias toward progressive disclosure
- next_candidates:
  - Human-vs-AI rank correlation once ratings land; if dashboard's sweep doesn't replicate in human ranking, study judge bias directly (multi-judge panel, lens-diverse verify per [[llm-as-judge-for-visuals]])
  - Fix the diagram-size failure mode: regenerate mermaid cells with a min-diagram-height constraint in the approach spec (v2) and re-evaluate the delta
  - Hybrid approach spec: dashboard glance layer + metaphor hero visual, testing whether metaphor adds glance value on top of progressive disclosure

## Follow-up

- Collect human ratings via the gallery; compare AI vs human ranking
  (rank correlation) — disagreement is itself a Phase 1 finding.
