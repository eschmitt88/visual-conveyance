---
kind: concept
name: "Staged generation pipelines"
status: seedling
added: "2026-07-01"
sources:
  - "[[literature/papers/berger2024visualization]]"
  - "[[literature/papers/dibia2023lida]]"
  - "[[literature/posts/googleresearch2025generativeui]]"
  - "[[literature/papers/vaduva2026code2uml]]"
related_concepts: ["llm-as-judge-for-visuals", "diagram-dsl-generation"]
related_experiments: []
tags: [pipelines, generate-check-refine, agents, visualization-generation, context-engineering, multi-agent]
---

# Staged generation pipelines

## Definition

Decomposing visual-artifact generation into explicit stages — e.g. understand the source material → set a communication goal → generate the artifact → render it → assess the render → revise — instead of a single prompt-to-artifact shot.

## Why it matters here

Our approaches are currently one-shot prompt specs; the literature suggests the biggest quality lever is closing the loop with a render-and-assess stage:

- Berger & Liu distinguish visualization *generation* (emit code — solved) from visualization *design* (iterate: conceive → implement → visually assess the render → re-conceive) and argue "visual perception will be critical in forming such an iterative improvement loop." An agent that never looks at its own render is assuming it can envision the result — an unvalidated assumption.
- LIDA (the canonical four-stage pipeline: summarize → explore goals → generate/execute/filter code → stylize) shows the *grounding-context stage dominates*: without a data summary, code-generation error rate is 96–99%; with a compact rules-based summary, ~3.5%. Also: forcing a goal-with-rationale step before generation yields more semantically meaningful outputs, and an execute-and-filter stage gives a free reliability metric (visualization error rate).
- Google's production Generative UI keeps the same shape at scale: crafted system instructions (planning framework + concrete output examples + error-avoidance tips) → tool calls → HTML/CSS/JS emission → dedicated post-processors for common failure modes. Even at frontier-model quality, the pipeline stages (not the bare model) carry reliability.

- Code2UML instantiates the whole shape agentically (Planner → parallel Analyzers → parallel Diagram agents → pipelined Correctors) and contributes two things the others don't. **(a) The correction stage is load-bearing and measurable**: 65.5% of raw outputs were syntactically valid, 91.5% after correction — the stage is worth ~26 points, which is also the size of the gap any post-gate measurement conceals. **(b) The grounding stage can be deterministic**: their importance-weighted IR compaction picks what the generator sees using pure Python, no LLM calls, milliseconds. That is LIDA's data-summary finding generalized — the stage that decides *what goes into the prompt* dominates the stage that decides *how the prompt is worded*.
- The corollary is the failure mode: a mechanical check stage is bounded by its rule set. Code2UML's corrector could not touch C4 constructs nobody had written rules for (41.7% of that type left broken), and SVGenius shows models breaking rendering while "optimizing" code — a revision stage that isn't render-verified can destroy the artifact it was meant to improve.

## Connections

- The assess stage is [[llm-as-judge-for-visuals]] turned inward: the same judge machinery used for evaluation can drive self-correction during generation — which also means a shared judge must not be both optimizer and final examiner (overfitting-to-judge risk).
- For [[diagram-dsl-generation]], the render stage gives a free syntax check before any judging happens.
