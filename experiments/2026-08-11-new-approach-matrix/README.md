---
kind: experiment
slug: "new-approach-matrix"
date: "2026-08-11"
status: running     # running | done | abandoned
hypothesis: "Approach 08 (editorial diagrams) beats both 02-mermaid (7.30) and 03-svg-infographic (7.38) on overall, showing 03's below-prose result was lack of design constraints, not the medium; approach 09 (motion explainer) scores top-3 on depth_comprehension while its glance score depends on the final-frame-first rule holding."
result: ""
related_concepts: ["editorial-design-constraints", "animation-as-explanation", "glanceability"]
related_literature: ["cathrynlavery-diagram-design", "3b1b-manim"]
tags: [visual-conveyance, matrix, ai-eval, phase-1, extension]
---

# new-approach-matrix

Extension of [[experiments/2026-07-01-baseline-matrix]]: the two new
approaches from ADR 0002 run against the same six test cases, same
contract v1, same rubric v1, same protocol v1 — 12 new cells appended
to the same Pages matrix.

## Hypothesis

1. 08-editorial-diagrams beats 03-svg-infographic on `overall` and on
   `visual_craft` (the constraint system is the missing ingredient) and
   beats 02-mermaid-diagrams on `glance_comprehension` (hand layout +
   accent discipline steers attention better than renderer layout).
2. 09-motion-explainer lands top-3 on `depth_comprehension` (sequential
   revelation aids studied reading) but does NOT lead on
   `glance_comprehension` — its glance score rests on the mandated
   final-frame-first resting state.
3. Neither new approach beats the baseline leader (layered-dashboard,
   9.02) on mean overall in this run; if 08 does, the
   editorial-constraint overlay becomes a priority for all approaches.

## Setup

- Config: `config.yaml` (12-cell matrix, model, input git SHA).
- Code: `tools/screenshot.py` (render), `tools/aggregate_evals.py`
  (metrics), subagent generation/evaluation per `eval/protocol.md` v1.
- Data: `testcases/*/` (unchanged since baseline, v1).
- Artifacts: `docs/presentations/<testcase>/<approach>/index.html`
  (+ glance.png/full.png), served by GitHub Pages.
- Evals: `results/evals/<testcase>--<approach>.json` → `metrics.json`.
- Baseline comparison caveat: 01–07 cells were generated 2026-07-01;
  cross-run rank comparisons carry model/date drift risk (noted in
  ADR 0002). Within-run comparisons (08 vs 09) are clean.

## Result

Fill in after the run. Point at `metrics.json`.

## Interpretation

What did you actually learn? What surprised you?

## Diagnostics

Fill in after the run. One line per field; leave `n/a` rather than
blank. `next_candidates` must list ≥2 concrete one-sentence proposals.
Every concrete claim below needs a **citation anchor** — a code
reference like `train.py:42-58`, a metrics file path like
`metrics.json:val_acc`, or a wikilink into `literature/`. Unanchored
assertions are flagged by `/lint` (Kosmos, arXiv 2511.02824).

Unless otherwise noted, metric numbers here reference `metrics.json`
(validation split). Cite `final_metrics.json` only if this experiment
is itself the final-scoring pass.

- intended_effect_confirmed: <yes | no | partial> — <one-line evidence with anchor>
- leakage_check: <method used> — <finding>
- overfitting_signal: train=<x> val=<y> gap=<z> — <interpretation> (from metrics.json)
- delta_from_prior: vs <related_prior_slug>, <metric_delta> attributed to <cause> (metrics.json)
- unexpected_findings: <one or two sentences, or "none">
- next_candidates:
  - <one-sentence proposal 1>
  - <one-sentence proposal 2>

## Follow-up

- ...
