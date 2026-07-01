---
kind: concept
name: "LLM-as-judge for visuals"
status: seedling
added: "2026-07-01"
sources:
  - "[[literature/papers/shbita2025mermaidseqbench]]"
related_concepts: ["diagram-dsl-generation", "structural-fidelity-metrics"]
related_experiments: []
tags: [evaluation, llm-as-judge, visualization]
---

# LLM-as-judge for visuals

## Definition

Using an LLM (or multimodal foundation model) as the scoring function for generated visual artifacts — diagrams, charts, infographics, UIs — typically via a fine-grained rubric with per-dimension 0–1 scores rather than a single holistic grade.

## Why it matters here

Our Phase-1 loop scores every approach×testcase presentation with AI evaluators before human ranking. The whole experiment design stands or falls on whether an AI judge's score tracks (a) factual accuracy and (b) what a non-expert human would actually comprehend at a glance. Known properties from the literature so far:

- Rubric decomposition (syntax / logic / completeness / usability as separate 0–1 dimensions) discriminates better than holistic scores (MermaidSeqBench).
- Judge identity matters a lot: two judge models can differ by 20+ points on identical outputs, and stricter judges punish weaker generators disproportionately (MermaidSeqBench). Cross-approach rankings should use ≥2 judges or a validated single judge.

## Connections

- Feeds the accuracy axis of our two-axis eval; the glance axis needs judges that model *perception*, not just content — see [[glanceability]].
- Contrast with [[structural-fidelity-metrics]], which replace the judge with deterministic graph comparison where possible.
