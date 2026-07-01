---
kind: concept
name: "Diagram-DSL generation"
status: seedling
added: "2026-07-01"
sources:
  - "[[literature/papers/shbita2025mermaidseqbench]]"
related_concepts: ["llm-as-judge-for-visuals", "structural-fidelity-metrics"]
related_experiments: []
tags: [mermaid, graphviz, d2, diagram-generation, dsl]
---

# Diagram-DSL generation

## Definition

Having an LLM emit a textual diagramming language (Mermaid, PlantUML, Graphviz/DOT, D2) that a deterministic renderer turns into the visual, instead of the model producing pixels or free-form SVG/HTML directly.

## Why it matters here

Diagram DSLs are one of our core approach families. Their key property: the artifact is text, so it is cheap to generate, diff, verify (does it render?), and evaluate structurally. Evidence so far:

- Syntax correctness saturates early with model scale (~90% for 7B+ models on Mermaid sequence diagrams), while *semantic* fidelity — control flow, activation lifecycles, error paths — lags well behind (MermaidSeqBench). Expect renderable-but-subtly-wrong as the dominant failure mode, not syntax errors.
- Structured NL input (purpose / components / interactions) is the input contract that makes generation and evaluation tractable (MermaidSeqBench).

## Connections

- The DSL's renderer gives a free binary "compiles" check; deeper accuracy needs [[structural-fidelity-metrics]] or [[llm-as-judge-for-visuals]].
- Trade-off vs free-form HTML/SVG approaches: constrained expressiveness but verifiable structure.
