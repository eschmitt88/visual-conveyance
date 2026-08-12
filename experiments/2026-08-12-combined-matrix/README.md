---
kind: experiment
slug: "combined-matrix"
date: "2026-08-12"
status: running     # running | done | abandoned
hypothesis: "Given the full toolbox, only the contract, and the layout-QA gate, unguided generator judgment matches or beats the best prescribed approach (layered-dashboard, 9.02 baseline); its channel choices will vary by test case rather than converging on one format."
result: ""
related_concepts: ["editorial-design-constraints", "animation-as-explanation", "glanceability", "generative-ui"]
related_literature: []
tags: [visual-conveyance, matrix, ai-eval, phase-1, free-choice, layout-qa]
---

# combined-matrix

Approach 10 (free choice of all channels, ADR 0003) × the same six test
cases. Two questions: (1) does unguided tool choice match prescribed
methods, and (2) what does the generator choose per material type —
the choices themselves are data.

## Hypothesis

1. 10-combined lands ≥ 8.47 (the 08/09 tie) on mean overall; the
   interesting outcome is whether it approaches layered-dashboard
   (9.02).
2. Channel choices vary by test case (diagram-heavy for
   codebase/incident, chart+prose for experiment-results/research)
   rather than converging on one format.
3. With the layout-QA gate, zero evaluator-cited overlap/clipping
   defects (vs 3/6 cells for 09 in the previous run).

## Setup

- Config: `config.yaml` (6-cell matrix, model, input git SHA).
- Code: `tools/screenshot.py`, `tools/layout_check.py` (NEW — generator
  self-check + harness gate, ADR 0003), `tools/aggregate_evals.py`;
  protocol v1 with the ADR 0003 amendment (generator may run
  layout_check on its own output).
- Data: `testcases/*/` (unchanged, v1).
- Artifacts: `docs/presentations/<testcase>/10-combined/index.html`.
- Evals: `results/evals/<testcase>--10-combined.json` → `metrics.json`.
- Channel-choice tally recorded in `log.md` after generation.

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
