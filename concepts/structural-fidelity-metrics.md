---
kind: concept
name: "Structural fidelity metrics"
status: seedling
added: "2026-07-01"
sources:
  - "[[literature/papers/liang2025diagrameval]]"
  - "[[literature/papers/tang2026igenbench]]"
  - "[[literature/papers/vaduva2026code2uml]]"
related_concepts: ["llm-as-judge-for-visuals", "diagram-dsl-generation"]
related_experiments: []
tags: [evaluation, graph-metrics, accuracy, diagrams, hallucination, precision-recall]
---

# Structural fidelity metrics

## Definition

Scoring a generated visual by extracting its underlying structure — text elements as nodes, connections as directed edges — and comparing that graph against ground truth (node alignment, path/reachability alignment, P/R/F1), instead of comparing pixels, embeddings, or asking a model for a holistic score.

## Why it matters here

This is the most defensible implementation of our **factual-accuracy axis**: it is interpretable (which fact is missing, which relation is wrong), largely deterministic, and resistant to metric hacking. Evidence so far:

- DiagramEval's Node F1 / Path F1 correlate with human "same logic?" judgments at ~0.43/0.41 vs ~0.1 for CLIPScore, and expose that frontier LLMs' free-form diagrams have very low structural fidelity (F1 ~0.2–0.35).
- Embedding metrics (CLIPScore) are both oversensitive to style/layout and gameable by text-stuffing — the failure modes structural metrics avoid.
- For our test cases, the reference is `key_facts.md`, not a reference diagram: the adaptation is *coverage of ground-truth entities/relations* rather than alignment to a gold image.
- Atomic yes/no question decomposition (IGenBench) is the constraint-level analogue when no graph is extractable: split ground truth into self-contained binary checks, verify each with an MLLM, and report both per-question accuracy and an all-checks-pass rate. Data completeness/encoding/ordering are the dimensions where generators fail hardest (0.21–0.27 avg across 10 T2I models).

- **Coverage and fabrication are different metrics and we only compute one.** Code2UML pairs Entity Recall (how much of the source appears) with Relationship Precision (do both endpoints of each asserted relation exist in the source) — the second is a direct hallucination probe, and it is the axis where their system scores well (0.858) while recall is deliberately low (0.313). Our accuracy score is recall-shaped: it asks whether `key_facts.md` entries are covered, not whether a page asserts things absent from the ground truth. A fabrication rate is the missing half.
- Low recall is not automatically a defect. Both Code2UML (use-case recall 0.165 "by design") and any good summary omit deliberately; recall must be read against the artifact's declared abstraction level, or it punishes exactly the editing our approaches are supposed to do.
- **Composite scores hide collapsed sub-dimensions.** Code2UML's activity diagrams score 68.1/100 almost entirely because labeling is 3.9/100; deployment scores 78.0 with structure at 11.7/100. Any aggregate we report — including our 1–10 evaluator scores — should be decomposable, or a single catastrophic dimension will read as mediocrity.
- A validator must not also be the oracle: their "syntactic validity" is defined as "the corrector chose not to edit it," so a silent corrector scores as success. Same hazard for us if `tools/layout_check.py` ever both fixes and grades.

## Connections

- Complements [[llm-as-judge-for-visuals]]: structure answers "is it right?"; a judge is still needed for "is it comprehensible at a glance?"
- Strengthens the case for [[diagram-dsl-generation]]: DSL source code makes the graph explicit, so extraction is lossless instead of a ~90%-accurate VLM step.
