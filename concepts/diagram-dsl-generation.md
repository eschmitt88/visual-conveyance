---
kind: concept
name: "Diagram-DSL generation"
status: seedling
added: "2026-07-01"
sources:
  - "[[literature/papers/shbita2025mermaidseqbench]]"
  - "[[literature/papers/vaduva2026code2uml]]"
  - "[[literature/papers/chen2025svgenius]]"
  - "[[literature/repos/swark-io-swark]]"
related_concepts: ["llm-as-judge-for-visuals", "structural-fidelity-metrics", "staged-generation-pipelines"]
related_experiments: []
tags: [mermaid, graphviz, d2, plantuml, svg, diagram-generation, dsl]
---

# Diagram-DSL generation

## Definition

Having an LLM emit a textual diagramming language (Mermaid, PlantUML, Graphviz/DOT, D2) that a deterministic renderer turns into the visual, instead of the model producing pixels or free-form SVG/HTML directly.

## Why it matters here

Diagram DSLs are one of our core approach families. Their key property: the artifact is text, so it is cheap to generate, diff, verify (does it render?), and evaluate structurally. Evidence so far:

- Syntax correctness saturates early with model scale (~90% for 7B+ models on Mermaid sequence diagrams), while *semantic* fidelity — control flow, activation lifecycles, error paths — lags well behind (MermaidSeqBench). Expect renderable-but-subtly-wrong as the dominant failure mode, not syntax errors.
- Structured NL input (purpose / components / interactions) is the input contract that makes generation and evaluation tractable (MermaidSeqBench).
- **The "compiles" check is not free — someone has to pay for the repair pass.** Code2UML's ablation puts raw PlantUML at 65.5% valid before a dedicated CorrectorAgent lifts it to 91.5%, and Swark, a production Mermaid tool, ships a `fixMermaidCycles` post-processor because cycles break rendering outright. Roughly a third of first-shot DSL output needs mechanical repair. Any measurement taken *after* a repair pass flatters the generator.
- **A repair pass can only fix defect classes its rules anticipate.** Code2UML's corrector left 41.7% of C4-stereotyped system-context diagrams uncorrectable — outside the rule set is indistinguishable from a pass.
- Hand-authored **SVG** belongs on this spectrum too, as the least-constrained DSL: no renderer to reject it, so no free syntax check at all, and SVGenius shows model competence degrading systematically with path/control-point complexity. The gain in expressiveness is paid for in lost verifiability.

## Connections

- The DSL's renderer gives a free binary "compiles" check; deeper accuracy needs [[structural-fidelity-metrics]] or [[llm-as-judge-for-visuals]].
- Trade-off vs free-form HTML/SVG approaches: constrained expressiveness but verifiable structure. The trade is monotone — Mermaid/PlantUML reject bad syntax, SVG accepts anything, and verifiability drops accordingly.
- The repair pass is a [[staged-generation-pipelines]] stage, and its size is the honest measure of how far raw generation actually is from usable.
