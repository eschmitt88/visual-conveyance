---
kind: experiment
slug: "new-approach-matrix"
date: "2026-08-11"
status: done     # running | done | abandoned
hypothesis: "Approach 08 (editorial diagrams) beats both 02-mermaid (7.30) and 03-svg-infographic (7.38) on overall, showing 03's below-prose result was lack of design constraints, not the medium; approach 09 (motion explainer) scores top-3 on depth_comprehension while its glance score depends on the final-frame-first rule holding."
result: "Both new approaches tie at 8.47 mean overall (#3 of 9 behind dashboard 9.02 and interactive 8.73); 08 crushes its unconstrained sibling 03 (+1.09) confirming the editorial-constraint hypothesis; 09 inverts prediction — 2nd-best glance (8.33) of all approaches but weak depth (7.75)."
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

AI-evaluation complete (12/12 cells, rubric v1, `metrics.json`). Both new
approaches land at **8.47 mean overall**, tied at #3 of 9 against the
baseline run (dashboard 9.02 > interactive 8.73 > **08 = 09 = 8.47** >
metaphor 8.43). Profiles differ sharply:

- **08-editorial-diagrams**: glance 7.58, accuracy 9.55, depth 8.25.
  vs 03-svg-infographic (7.38 overall): +1.09 overall, +1.00 glance,
  +1.53 accuracy. vs 02-mermaid (7.30): +1.17 overall.
- **09-motion-explainer**: glance **8.33** — 2nd-highest of all nine
  approaches (only dashboard's 8.67 is higher) — accuracy 9.43, but
  depth 7.75 and structure_nav 7.50 (both near the bottom of the field).

## Interpretation

- **Hypothesis 1 confirmed decisively**: 03's below-prose result was
  lack of design constraints, not the free-form-SVG medium. Same medium
  + the diagram-design constraint system = +1.09 overall, with accuracy
  recovering from 8.02 to 9.55 (metrics.json:by_approach). Evaluators
  repeatedly praised "verified-honest" encodings — the constraint set
  appears to discipline content, not just style.
- **Hypothesis 2 inverted**: 09 was predicted to win depth and risk
  glance; it did the opposite. The mandated final-frame-first rule made
  the completed scene an excellent static artifact (glance 8.33), but
  one dense SVG canvas gives poor wayfinding for studied reading
  (structure_nav 7.50; "no scannable sections" — codebase-structure
  eval), and the animation's explanatory payload is invisible to a
  screenshot-based eval. The rubric cannot see the build-up — motion's
  actual value is untested by this harness and needs the human pass.
- **Hypothesis 3 confirmed**: neither beats layered-dashboard (9.02).
- Recurring 09 defect: SVG text collisions/clipping at fixed viewBox
  (3 of 6 cells cited; drags visual_craft to 7.50) — a fixable spec bug,
  same category as baseline's mermaid-sizing bug.

## Caveats

Cross-run comparison carries generation-date drift risk (same model
slug, 6 weeks apart; ADR 0002). Within-run 08-vs-09 comparisons are
clean. Screenshot-first evaluation structurally undervalues 09's
animation channel.

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

- intended_effect_confirmed: partial — 08 beat 03 by +1.09 overall as predicted (metrics.json:by_approach.08-editorial-diagrams), but 09's predicted depth win came out as a glance win instead (metrics.json:by_approach.09-motion-explainer)
- leakage_check: generators never given key_facts.md (prompt-level exclusion per eval/protocol.md); evaluators blind to approach specs — same protocol v1 as baseline
- overfitting_signal: n/a — no train/val split; single-judge scores, judge-taste bias caveat per eval/protocol.md "Blindness limits"
- delta_from_prior: vs 2026-07-01-baseline-matrix, 08 +1.09 overall over 03 attributed to the editorial constraint system (only changed variable — same medium, same testcases, same rubric; metrics.json vs baseline metrics.json); cross-run date drift caveat (ADR 0002)
- unexpected_findings: 09's final-frame-first rule made it the 2nd-best glance approach of all nine while depth/nav lagged — the exact inverse of the hypothesis; screenshot-based evals cannot see the animation channel at all.
- next_candidates:
  - Apply the editorial-constraint overlay (accent discipline, 4px grid, density cap) to 04-layered-dashboard — the current leader — and test whether constraints stack with progressive disclosure.
  - v2 of 09 with overflow-safe SVG text layout (measured labels, collision pass) to fix the 3/6-cell clipping defect before judging the approach itself.
  - Human eval wave over 08/09 cells (gallery already covers them) prioritizing 09, whose animation payload the AI screenshot eval structurally cannot score.

## Follow-up

- ...
