---
kind: experiment
slug: "combined-matrix"
date: "2026-08-12"
status: done     # running | done | abandoned
hypothesis: "Given the full toolbox, only the contract, and the layout-QA gate, unguided generator judgment matches or beats the best prescribed approach (layered-dashboard, 9.02 baseline); its channel choices will vary by test case rather than converging on one format."
result: "10-combined scores 9.15 mean overall — new #1 of 10 (dashboard 9.02) — with perfect 10.0 accuracy on all six cells and every score dimension at or near field-best; channel choices converged (hand SVG 6/6 over Mermaid, animation 0/6, JS only when it encodes a real question) rather than varying by material; zero layout defects survived the QA gate."
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

AI-evaluation complete (6/6 cells, rubric v1, `metrics.json`).
**10-combined: 9.15 mean overall — new #1 of 10 approaches**
(layered-dashboard 9.02 was the previous leader). Profile: accuracy
**10.0** (perfect fact audit in all six cells — first approach to do
this), glance 8.67 (ties dashboard's field-best), depth 8.83 (new
field-best), structure_nav 8.33 (new field-best), visual_craft 8.67
(new field-best). Cells: incident 9.4 > codebase = research =
experiment-results 9.3 > tradeoff 8.9 > diffusion 8.7.

Layout-QA gate: 6/6 pages clean on independent re-check; the
generators' self-check loop caught and fixed 6 defects (3 CLIPPED, 1
OVERLAP, 1 mobile H_OVERFLOW, 1 CLIPPED) during generation — the
defect class that cost 09 three cells last run produced zero
evaluator complaints this run (log.md).

## Interpretation

- **Hypothesis 1 exceeded**: free choice + contract + QA gate didn't
  just match the best prescribed method, it beat it. Prescription is
  not where the remaining value lives; mechanical QA and tool
  availability are.
- **Hypothesis 2 wrong in an informative way**: choices converged
  instead of varying — every cell chose prose + hand SVG + CSS; all
  six declined Mermaid ("tighter control" with hand SVG) and
  animation; two declined all JS; the four JS uses each encode a real
  question (tabs per contribution type, CFG slider, counterfactual
  leg-removal toggle, chart↔table linking). Unguided, the generator
  independently converged on much of the human feedback (linearity,
  meaning-attached numbers, no forced interactivity) — see
  eval/human-feedback-2026-08-12.md, which it never saw.
- **Hypothesis 3 confirmed**: zero overlap/clipping complaints from
  evaluators (vs 3/6 cells for 09 in the prior run).
- Recurring evaluator nit across 4/6 cells: long single-scroll pages
  with no anchor navigation — the one structural idea from the
  prescribed approaches (04's layering) that free choice dropped.

## Caveats

Cross-run comparison to 01–09 carries generation-date drift; 10's
cells also had the layout-QA advantage 01–09 lacked (ADR 0003 notes
this for visual_craft comparisons). Single-judge scores; the judge
shares a base model with the generator. Human ratings remain the
authoritative check — especially given the judge ranked
tab-dependent content (codebase) high while the human finds tab
gating intimidating.

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

- intended_effect_confirmed: yes — 9.15 > 9.02 (metrics.json:by_approach.10-combined vs baseline metrics.json:by_approach.04-layered-dashboard); free choice ≥ best prescribed method
- leakage_check: generators never given key_facts.md; evaluators blind to approach spec; layout_check.py grants no content access (protocol v1 + ADR 0003 amendment)
- overfitting_signal: n/a — no train/val split; judge-taste caveat per eval/protocol.md, judge may share generator's format preferences
- delta_from_prior: vs 2026-08-11-new-approach-matrix, +0.68 over the 08/09 tie attributed jointly to free channel choice and the layout-QA loop (not separable in this design; metrics.json)
- unexpected_findings: channel choices converged (SVG-over-Mermaid 6/6, animation 0/6) instead of varying by material; the generator unguided reproduced most of the owner's stated preferences; accuracy hit 10.0 in all six cells for the first time.
- next_candidates:
  - Ablate the layout-QA loop (10 without self-check) to separate the free-choice effect from the QA effect on visual_craft/overall.
  - Add anchor-nav/TOC as a contract-level nudge (4/6 evaluator complaints) and re-run 10 to see if structure_nav closes the gap to dashboard-style layering.
  - Human rating wave over 10's six cells — decisive given the judge/human disagreement on tab-gated content and the untested animation channel.

## Follow-up

- ...
