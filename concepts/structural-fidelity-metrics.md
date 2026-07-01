---
kind: concept
name: "Structural fidelity metrics"
status: seedling
added: "2026-07-01"
sources:
  - "[[literature/papers/liang2025diagrameval]]"
related_concepts: ["llm-as-judge-for-visuals", "diagram-dsl-generation"]
related_experiments: []
tags: [evaluation, graph-metrics, accuracy, diagrams]
---

# Structural fidelity metrics

## Definition

Scoring a generated visual by extracting its underlying structure — text elements as nodes, connections as directed edges — and comparing that graph against ground truth (node alignment, path/reachability alignment, P/R/F1), instead of comparing pixels, embeddings, or asking a model for a holistic score.

## Why it matters here

This is the most defensible implementation of our **factual-accuracy axis**: it is interpretable (which fact is missing, which relation is wrong), largely deterministic, and resistant to metric hacking. Evidence so far:

- DiagramEval's Node F1 / Path F1 correlate with human "same logic?" judgments at ~0.43/0.41 vs ~0.1 for CLIPScore, and expose that frontier LLMs' free-form diagrams have very low structural fidelity (F1 ~0.2–0.35).
- Embedding metrics (CLIPScore) are both oversensitive to style/layout and gameable by text-stuffing — the failure modes structural metrics avoid.
- For our test cases, the reference is `key_facts.md`, not a reference diagram: the adaptation is *coverage of ground-truth entities/relations* rather than alignment to a gold image.

## Connections

- Complements [[llm-as-judge-for-visuals]]: structure answers "is it right?"; a judge is still needed for "is it comprehensible at a glance?"
- Strengthens the case for [[diagram-dsl-generation]]: DSL source code makes the graph explicit, so extraction is lossless instead of a ~90%-accurate VLM step.
