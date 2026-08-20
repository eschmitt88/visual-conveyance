---
kind: paper
title: "Code2UML: Agentic LLMs with context engineering for scalable software visualization"
authors: ["Alin-Gabriel Văduva", "Anca-Ioana Andreescu", "Simona-Vasilica Oprea", "Adela Bâra"]
institutions: ["Bucharest University of Economic Studies"]
year: 2026
venue: arXiv preprint
peer_reviewed: false
url: https://arxiv.org/abs/2605.24453
code_url: null
citations: null
source: "raw/papers/vaduva2026code2uml.pdf"
added: "2026-08-20"
relevance: 3
credibility: 2
status: read
related_experiments: []
related_concepts: ["staged-generation-pipelines", "diagram-dsl-generation", "structural-fidelity-metrics"]
tags: [uml, plantuml, multi-agent, context-engineering, code-visualization, corrector-agent, claude-agent-sdk]
---

# Code2UML: Agentic LLMs with context engineering for scalable software visualization

## TL;DR

A five-agent pipeline (Planner → Analyzer → Diagram → Corrector, plus an out-of-band DependencyAnalyzer) built on the Claude Agent SDK generates PlantUML from real repositories, fronted by a deterministic importance-weighted compaction layer that shrinks the code IR to a diagram-specific view under a fixed byte budget with **no LLM calls**; across 12 repos × 7 diagram types it reports 91.5% syntactic validity, 0.858 relationship precision, 81.7/100 quality — but the ablation shows only **65.5% of outputs were valid before the Corrector touched them**.

## Claims

- **Core claim:** the bottleneck in repo-scale diagram generation is the *data payload*, not the instruction text — deterministic, importance-weighted compaction of a structured IR beats stuffing or RAG-retrieving code into the prompt, and it costs milliseconds and zero tokens.
- Splitting the job across role-specialized agents (plan / analyze / generate / correct) beats one monolithic prompt doing all four, and localizes failures (a Corrector bug can't corrupt diagram structure).
- A dedicated syntax-correction pass is architecturally essential, not cosmetic: it lifts validity from 65.5% to 91.5%.
- Quality is scale-invariant while coverage is not: quality score stays in 77.5–83.6 from 31 to 4,578 IR entities, whereas entity recall falls monotonically with project size — framed as deliberate abstraction, not failure.
- Difficulty is a property of the **diagram type**, not the source language: the validity heatmap varies far more across columns (types) than rows (Java/JS/PHP/Python).

## Methods

- tree-sitter → language-agnostic IR; a pure-Python view generator ranks IR elements by a diagram-type-specific importance function (method/attribute counts, inheritance, call-chain participation, name heuristics), scales per-element detail inversely with element count, then iteratively halves the budget until the view fits 60 KB (SINGLE path) / 100 KB (DEEP path).
- Two-tier routing: structural overviews (component, deployment, system context) get one DiagramAgent from the view alone; behavioral/detailed types (class, sequence, activity, use case) get Planner → parallel Analyzers → parallel DiagramAgents with **pipelined** Correctors (each Corrector starts as its own diagram finishes).
- Prompt architecture: a shared base block (role, workflow, universal PlantUML rules, a readability size threshold) + per-diagram-type extensions mapping IR fields to PlantUML constructs; the Corrector's prompt is assembled from a base rule set plus type-specific known-pitfall rules.
- Five automated metrics: Entity Recall, Relationship Precision (both endpoints declared in the IR — a hallucination detector), Syntactic Validity Rate (= % needing no Corrector edit), a five-part Quality Score (density/connectivity/labeling/documentation/structure), and a Structural Complexity Index `E·log₂(1+2R/E)`.
- Corpus: 12 OSS repos across Java/Python/JS/PHP (31 → 4,578 IR entities) × 7 UML types = 84 observations. Backing model: Claude Sonnet 4.6.

## Results

- Means across 84 observations: validity 91.5%, entity recall 0.313, relationship precision 0.858, quality 81.7.
- Best/worst by type: component and deployment hit 100% validity; **system context collapses to 58.3%**, with 41.7% of its outputs *uncorrectable* because C4-style stereotypes fall outside the Corrector's rule set. Activity is the neediest type — 83.3% of batches required correction.
- Ablation (post-hoc, not a re-run): 55/84 needed no correction, 24/84 were partially corrected, 5/84 uncorrectable.
- Relationship precision is high everywhere (component 0.993, use case 0.933, class 0.917); the residual hallucinations are inferred intermediary components in sequence diagrams for large projects.
- Sub-metric decomposition exposes what the aggregate hides: activity diagrams score 68.1 overall almost entirely because **labeling is 3.9/100**; deployment scores 78.0 with structure at 11.7/100.

## Critique / open questions

- **The headline validity metric is circular.** "Syntactically valid" is defined as "the CorrectorAgent chose not to edit it," so the Corrector is simultaneously the fixer and the oracle. A silent Corrector on a broken file scores as a success; there is no independent PlantUML parse.
- **The ablation is a re-labelling, not an ablation** — the system was never run with the Corrector removed, so downstream effects (e.g. a Diagram agent that would have self-corrected) are invisible.
- No code or artifacts released; no human evaluation of whether any diagram actually communicates anything. Every metric is machine-computed from regex-parsed PlantUML.
- Quality Score weights are unstated ("weighted average") and the sub-scores are self-defined against unnamed "UML best-practice ranges" — unvalidated against any external standard.
- Internal inconsistency: the abstract reports cross-language quality variance of 3.1 points, the conclusion says 0.6.
- Preprint from a single group, not peer-reviewed, no citations yet. Treat the numbers as illustrative of the architecture, not as calibrated measurements.

## So what for visual-conveyance

- **Strongest transferable finding: the corrector pass, and the size of the gap it hides.** One in three raw generations was syntactically broken. Our `tools/layout_check.py` gate (ADR 0003) is the deterministic analogue, and this is evidence that the *unaided* generation rate is much worse than the post-gate rate — so any approach we score after a QA gate is being flattered. Worth logging pre-gate pass rate as a separate number, not just post-gate.
- **Failure is a property of the output form, not the input.** Their validity varies by diagram type, not by source language; our matrix shows the same shape — approaches (02-mermaid especially) fail consistently regardless of test case. That argues for spending spec-fixing effort per approach rather than per test case.
- **Rule-set coverage is the ceiling on any mechanical gate.** Their Corrector fixed everything *except* the C4 constructs its rules never anticipated (41.7% uncorrectable on that type). Our layout gate will have the same blind spot: it can only catch defect classes someone enumerated. A defect class outside the ruleset reads as a pass.
- **Relationship precision is a cheap hallucination probe we don't have.** "Both endpoints declared in the source" maps directly onto our `key_facts.md` contract: count entities/relations asserted by a page that appear nowhere in the ground truth. That's a *fabrication* metric, orthogonal to the coverage metric our accuracy score already computes.
- **The compaction contribution does not bite for us.** Our test-case source material fits comfortably in context; the "IR exceeds the window" problem is a repo-scale one. What generalizes is the weaker LIDA-shaped claim already in [[staged-generation-pipelines]]: a deliberate grounding/selection stage before generation dominates prompt wording.
- Sub-metric decomposition is a useful reporting discipline: their 68.1 activity score was one collapsed sub-dimension wearing a trenchcoat. Our composite 1–10 evaluator scores can hide the same thing.

## Trust signals

- **Credibility:** 2 — unreviewed arXiv preprint from a single group, no released code or artifacts, no human evaluation, all five metrics self-defined; the headline validity metric is circular (the Corrector grades itself), the "ablation" is a post-hoc re-labelling rather than a re-run, and the abstract and conclusion disagree on cross-language variance. The *architecture* is credible and clearly described; the *numbers* are not evidence.

## Follow-up

- **Relevance:** 3 — the corrector-pass ablation and the relationship-precision idea are directly actionable for our gate and our accuracy axis; capped at 3 because the central contribution (context compaction) targets a scale problem we don't have, and the measurements are too weakly validated to cite as results.
- Candidate metric: add a *fabrication rate* (asserted facts absent from `key_facts.md`) alongside the existing coverage-based accuracy score.
- Candidate protocol change: record pre-gate vs post-gate pass rate per approach, so the QA gate's contribution is visible instead of baked in.
