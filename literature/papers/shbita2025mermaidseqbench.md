---
kind: paper
title: "MermaidSeqBench: An Evaluation Benchmark for NL-to-Mermaid Sequence Diagram Generation"
authors: ["Basel Shbita", "Farhan Ahmed", "Chad DeLuca"]
institutions: ["IBM Research"]
year: 2025
venue: arXiv preprint (2511.14967)
peer_reviewed: false
url: https://arxiv.org/abs/2511.14967
code_url: https://github.com/IBM/MermaidSeqBench-Eval
citations: null
source: "raw/papers/shbita2025mermaidseqbench.md"
added: "2026-07-01"
relevance: 4
credibility: 4
status: read
related_experiments: []
related_concepts: ["llm-as-judge-for-visuals", "diagram-dsl-generation"]
tags: [benchmark, mermaid, sequence-diagrams, llm-as-judge, diagram-generation, evaluation]
---

# MermaidSeqBench: An Evaluation Benchmark for NL-to-Mermaid Sequence Diagram Generation

## TL;DR

First systematic benchmark (132 human-verified + synthetically expanded samples) for NL→Mermaid sequence diagram generation, scored by LLM-as-judge on six 0–1 rubric dimensions; reveals large capability gaps by model scale and substantial disagreement between judge models.

## Claims

- **Core claim:** LLMs' ability to emit correct Mermaid sequence diagrams can be measured reliably with a fixed dataset plus an LLM-as-judge rubric, and current models show significant, scale-dependent capability gaps.
- No prior formal benchmark or public dataset existed for Mermaid sequence diagram generation (prior work centered on PlantUML).
- Fine-grained rubric dimensions (syntax, mermaid-only output, logic, completeness, activation handling, error/status tracking) discriminate model quality better than pass/fail rendering checks.
- Judge choice matters: DeepSeek-V3 scores higher and more consistently; GPT-OSS-120B is stricter, especially on small models — cross-judge variability argues for multiple evaluators.

## Methods

- Dataset: 10 SME-crafted seed diagrams → LLM synthetic expansion (Mistral-Large-123B, SME + Mermaid Live Editor verification of 30) → rule-based augmentation (~4x, reordering alt/else blocks, participant renaming) → 132 NL–Mermaid pairs.
- Each NL input is structured: Purpose / Main Components / Interactions.
- Generation at temperature 0, 1,024 max tokens for reproducibility.
- LLM-as-judge (DeepSeek-V3 671B and GPT-OSS 120B) scores each output 0.0–1.0 on six dimensions against a reference diagram, without requiring verbatim match, outputting score + brief explanation.

## Results

- Key numbers (DeepSeek-V3 judge): Llama-3.1-8B 92.0% syntax / 87.4% logic / 79.2% activation; Qwen-2.5-7B nearly identical; small models collapse (Llama-3.2-1B: 52.3% logic, 39.9% activation).
- Qwen-2.5 scaling sweep 0.5B→72B: monotone improvement on all six criteria; biggest jump 3B→7/14B; syntax saturates near 88–90% while semantic dimensions (activation, error tracking) keep improving — semantics is the bottleneck, not syntax.
- Even the best 7–8B models leave ~20% on the table for activation/error handling — logical fidelity lags syntactic fidelity.

## Critique / open questions

- Only sequence diagrams; unclear generalization to flowcharts/architecture diagrams (our more common needs).
- Judge scores are never validated against human judgments in this paper — the judges disagree substantially with each other, which is a warning for our own AI-evaluator design.
- No frontier models (GPT-4/5, Claude, Gemini) in the generation matrix; capability gaps at 1–8B scale may be irrelevant to an agent running Opus-class models.
- 132 samples derived from 10 seeds → limited structural diversity.

## Trust signals

- **Credibility:** 4 — IBM Research authors, code + dataset released (GitHub + HuggingFace, CC BY 4.0), but arXiv preprint, not peer-reviewed, no established citation count.

## So what for visual-conveyance

- Direct template for our accuracy axis when an approach emits a diagram DSL: a multi-dimension 0–1 LLM-judge rubric (syntax / output hygiene / logic / completeness) instead of a single holistic score. Their rubric decomposition is reusable almost verbatim for Mermaid-based approaches.
- The judge-disagreement finding (DeepSeek vs GPT-OSS gaps of 20+ points on the same outputs) says our AI evaluator scores are judge-relative: we should either use ≥2 judge models or anchor judges with rubric examples before trusting cross-approach rankings.
- The syntax-saturates / semantics-lags pattern predicts where our Mermaid approaches will fail: renderable diagrams that are subtly wrong — which is exactly why our two-axis eval keeps factual accuracy separate from glance comprehension.
- Caveat for us: this benchmark measures conveying *specs to diagrams*, not *diagrams to humans* — it covers the generation-fidelity half only, nothing about whether a non-expert understands the result at a glance.

## Follow-up

- **Relevance:** 4 — directly seeds our LLM-as-judge-for-visuals concept and provides a reusable rubric structure for the accuracy axis of the two-axis eval.
- Consider adopting their six-dimension rubric shape for our `results/evals/` scoring of diagram-DSL approaches.
- Check the IBM repo for judge prompt templates we can adapt.
