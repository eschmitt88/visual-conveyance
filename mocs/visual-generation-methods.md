---
kind: moc
name: "Visual generation methods"
description: "How an agent actually produces a visual artifact — the structure-vs-freedom spectrum, motion as a channel, and process as the cross-cutting lever."
status: active
added: "2026-08-20"
concepts:
  - "[[concepts/diagram-dsl-generation]]"
  - "[[concepts/editorial-design-constraints]]"
  - "[[concepts/generative-ui]]"
  - "[[concepts/animation-as-explanation]]"
  - "[[concepts/staged-generation-pipelines]]"
related_experiments:
  - "[[experiments/2026-07-01-baseline-matrix]]"
  - "[[experiments/2026-08-11-new-approach-matrix]]"
  - "[[experiments/2026-08-12-combined-matrix]]"
tags: [moc, visual-generation-methods, generation, approaches, phase-1]
---

# Visual generation methods

The question this theme answers: **when an agent has to say something
visually, what should it actually emit, and how should it get there?**
These five concepts are the generation side of the project — the levers
that produce a page. They are deliberately separated from the scoring
side ([[concepts/glanceability]], [[concepts/llm-as-judge-for-visuals]],
[[concepts/structural-fidelity-metrics]]), which is a smaller cluster
still awaiting its own map.

They cluster because each answers the same question differently: how much
of the artifact does the model author directly, and what constrains it.
Our ten `approaches/` specs are instances drawn from this map, so the map
doubles as the design space the Phase-1 matrix samples.

## The structure–freedom spectrum

The load-bearing axis. Moving along it trades **verifiability** for
**expressiveness**, monotonically.

- [[concepts/diagram-dsl-generation]] — the constrained pole: emit
  Mermaid/PlantUML/DOT text and let a deterministic renderer own layout.
  The renderer's parser is a free correctness gate, but only a syntactic
  one — semantic fidelity lags well behind syntax
  ([[literature/papers/shbita2025mermaidseqbench]]), and roughly a third
  of first-shot output needs mechanical repair before it renders at all
  ([[literature/papers/vaduva2026code2uml]],
  [[literature/repos/swark-io-swark]]). Hand-authored SVG sits at the far
  end of the same spectrum: no parser to reject it, so no free check, and
  competence degrades with path complexity
  ([[literature/papers/chen2025svgenius]]).
- [[concepts/editorial-design-constraints]] — the middle: full layout
  freedom, style locked down by prompt-level rules (one accent, 4px grid,
  density cap, "deletion is the highest-quality move";
  [[literature/repos/cathrynlavery-diagram-design]]). This is the cluster's
  clearest empirical win — approach 08 is 03 re-run under the constraint
  set and beats it by +1.09 overall (8.47 vs 7.38), which isolates the
  design system as the cause.
- [[concepts/generative-ui]] — the free pole: the model designs the whole
  interface, per prompt and per audience. Production-validated on human
  preference ([[literature/posts/googleresearch2025generativeui]]), but its
  two admitted open problems — factual accuracy and what a reader actually
  absorbs — are precisely our two eval axes. Preference is not
  comprehension.

## Motion and attention as a separate channel

- [[concepts/animation-as-explanation]] — ordering as content: sequential
  revelation, morphs instead of cuts, camera as pointer
  ([[literature/repos/3b1b-manim]]). This is orthogonal to the spectrum
  above — it steers attention in *time* where accent discipline steers it
  in *space* — and the project's glance axis puts it under real strain,
  since a single screenshot cannot contain playback. The measured split
  matched that tension inversely to prediction: approach 09 took
  second-best glance (8.33) on the strength of its final frame while
  scoring weakest of the new pair on depth.

## Process as the cross-cutting lever

- [[concepts/staged-generation-pipelines]] — not a rival to the above but
  a multiplier on any of them: ground → goal → generate → render → assess
  → revise. The literature is consistent that the stages, not the bare
  model, carry reliability — LIDA's grounding ablation moves code-error
  rate from 96–99% to ~3.5% ([[literature/papers/dibia2023lida]]),
  Code2UML's corrector moves validity 65.5% → 91.5%, and Berger & Liu
  argue an agent that never looks at its own render is assuming it can
  envision the result ([[literature/papers/berger2024visualization]]).
  The counterweight: a check stage is bounded by its rule set, and a
  validator that also grades itself is not a validator.

## Open thread

Every one of our approach specs is still a **one-shot prompt**. The single
exception is the layout-QA loop added in ADR 0003, where generators ran
`tools/layout_check.py` on their own output — and that lone check stage
coincides with the best result in the project (10-combined, 9.15, perfect
accuracy on all six cells, zero surviving layout defects). One stage, one
run, confounded with everything else approach 10 changed; it is a hint,
not a finding.

That makes the standing hypothesis: **the remaining headroom is in the
pipeline, not the prompt.** The clean test is a render-and-assess stage
bolted onto an *existing* approach spec, so the delta isolates the stage
rather than the toolbox. A second thread runs the other way — approach 10's
free choice converged (hand SVG 6/6, animation 0/6) rather than varying by
material, which suggests the spectrum's poles may not be equally live once
a generator is allowed to pick.
