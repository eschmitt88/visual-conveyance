---
kind: concept
name: "Staged generation pipelines"
status: seedling
added: "2026-07-01"
sources:
  - "[[literature/papers/berger2024visualization]]"
  - "[[literature/papers/dibia2023lida]]"
related_concepts: ["llm-as-judge-for-visuals", "diagram-dsl-generation"]
related_experiments: []
tags: [pipelines, generate-check-refine, agents, visualization-generation]
---

# Staged generation pipelines

## Definition

Decomposing visual-artifact generation into explicit stages — e.g. understand the source material → set a communication goal → generate the artifact → render it → assess the render → revise — instead of a single prompt-to-artifact shot.

## Why it matters here

Our approaches are currently one-shot prompt specs; the literature suggests the biggest quality lever is closing the loop with a render-and-assess stage:

- Berger & Liu distinguish visualization *generation* (emit code — solved) from visualization *design* (iterate: conceive → implement → visually assess the render → re-conceive) and argue "visual perception will be critical in forming such an iterative improvement loop." An agent that never looks at its own render is assuming it can envision the result — an unvalidated assumption.
- LIDA (the canonical four-stage pipeline: summarize → explore goals → generate/execute/filter code → stylize) shows the *grounding-context stage dominates*: without a data summary, code-generation error rate is 96–99%; with a compact rules-based summary, ~3.5%. Also: forcing a goal-with-rationale step before generation yields more semantically meaningful outputs, and an execute-and-filter stage gives a free reliability metric (visualization error rate).

## Connections

- The assess stage is [[llm-as-judge-for-visuals]] turned inward: the same judge machinery used for evaluation can drive self-correction during generation — which also means a shared judge must not be both optimizer and final examiner (overfitting-to-judge risk).
- For [[diagram-dsl-generation]], the render stage gives a free syntax check before any judging happens.
