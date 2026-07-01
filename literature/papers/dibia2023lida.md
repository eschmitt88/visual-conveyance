---
kind: paper
title: "LIDA: A Tool for Automatic Generation of Grammar-Agnostic Visualizations and Infographics using Large Language Models"
authors: ["Victor Dibia"]
institutions: ["Microsoft Research"]
year: 2023
venue: ACL 2023 (System Demonstrations)
peer_reviewed: true
url: https://arxiv.org/abs/2303.02927
code_url: https://microsoft.github.io/lida/
citations: null
source: "raw/papers/dibia2023lida.pdf"
added: "2026-07-01"
relevance: 4
credibility: 5
status: read
related_experiments: []
related_concepts: ["staged-generation-pipelines", "llm-as-judge-for-visuals"]
tags: [pipeline, visualization-generation, infographics, llm, self-evaluation, grammar-agnostic, microsoft]
---

# LIDA: Automatic Generation of Grammar-Agnostic Visualizations and Infographics using LLMs

## TL;DR

Canonical staged pipeline for LLM visualization generation: SUMMARIZER (data → compact NL context) → GOAL EXPLORER (question/visualization/rationale triples) → VISGENERATOR (code-scaffold fill-in + execute + filter/repair) → INFOGRAPHER (diffusion-model stylization). Introduces two eval metrics: visualization error rate (VER, ~3.5%) and GPT-4 self-evaluated visualization quality (SEVQ, 1–10 across six dimensions).

## Claims

- **Core claim:** Visualization/infographic generation is best posed as a *multi-stage* text-and-code generation problem; an orchestrated LLM pipeline eliminates subtask-specific models, works across any grammar/language (matplotlib, seaborn, Altair, Vega-Lite, ggplot, Bokeh, D3), and improves as the underlying LLM improves.
- Grounding context is decisive: generating code *without* a data summary catastrophically fails (VER 95.8–99.3%), while a rules-based summary drops VER to ~3.5–5.6%. LLM enrichment of the summary adds little beyond the base summary.
- Requiring the model to produce a *rationale* alongside each goal yields more semantically meaningful goals.
- LLMs (GPT-4) encode enough visualization best practices to critique generated visualizations across code accuracy, data transformation, goal compliance, visualization type, data encoding, and aesthetics — usable both as a metric (SEVQ) and for automatic repair.

## Methods

- **SUMMARIZER:** two-stage — rules extract atomic types/field stats/samples via pandas; optional LLM/user enrichment adds semantic descriptions. Goal: information-dense but compact grounding context.
- **GOAL EXPLORER:** multitask generation of JSON {question, visualization, rationale}.
- **VISGENERATOR:** code-scaffold constructor (imports + empty function stub per grammar) → fill-in-the-middle code generation of n candidates → executor with error filtering (discard non-compiling; optionally self-consistency voting or correctness-probability ranking). VizOps on the code representation: NL refinement, explanations/accessibility descriptions, self-evaluate-and-repair, recommendation.
- **INFOGRAPHER:** text-conditioned image-to-image diffusion over the rendered chart with an editable NL style library, plus post-processing (restore correct axes, remove grid lines) for data faithfulness.
- **Evaluation:** 57 vega-datasets, 5 goals each, 1 viz per goal, temperature 0, n=2280 generations (GPT-3.5); VER = % of generations with compilation errors; SEVQ = GPT-4 1–10 score + rationale across the six dimensions.

## Results

- VER ≈ 3.5% overall (seaborn, with summary); ablation (matplotlib/seaborn): no_enrich 5.61%/3.51%, LLM-enrich 7.72%/3.51%, schema-only 7.02%/9.47%, no_summary 95.79%/99.30%.
- Expressive, well-represented grammars (seaborn) yield lower VER.
- SEVQ shown identifying semantic issues (e.g. critiques a user-requested pie chart, recommends bar chart with rationale, offers auto-repair) — qualitative, no human-correlation validation.

## Critique / open questions

- SEVQ is self-evaluation with no human-agreement study — precisely the gap later work (IGenBench r=0.90 validation; MermaidSeqBench judge disagreement) shows matters. VER only measures "compiles," not "correct."
- 2023-era models (GPT-3.5 generation, GPT-4 judging); absolute numbers stale, architecture still relevant.
- Infographer stage trades data fidelity for style and needs post-processing to restore axes — early evidence of the T2I data-fidelity problem IGenBench later quantified.
- Depends on grammars being well-represented in training data (their Low Resource Grammars limitation) — relevant to picking mainstream DSLs (Mermaid yes, obscure D2 features maybe not).

## Trust signals

- **Credibility:** 5 — peer-reviewed (ACL 2023 demo), Microsoft Research, widely adopted open-source release (microsoft.github.io/lida), heavily cited in the follow-on literature we've ingested.

## So what for visual-conveyance

- The reference architecture for our generation harness: our approaches map onto LIDA's stages — testcase material plays the SUMMARIZER output role, an explicit communication-goal step before artifact generation is LIDA's GOAL EXPLORER, and generate→execute→filter/repair is the VISGENERATOR loop. The ablation lesson transfers directly: *what grounding context the generator sees dominates output quality* — our approach prompt specs should treat source-material summarization as a first-class stage, not a preamble.
- Goal-with-rationale is a cheap, proven trick for our prompt specs: force the approach to state "what question does this presentation answer and why this form" before emitting HTML/DSL.
- VER has a direct analogue for us: % of approach outputs that render (HTML validates, Mermaid compiles) — a free reliability floor metric per approach for metrics.json, separate from the two quality axes.
- SEVQ is the pattern our AI evaluators generalize (multi-dimension 1–10 scoring with rationale), but its missing human validation is the cautionary tale: we validate against human ranking in Phase 1.
- The Infographer's fidelity/post-processing struggle reinforces our code-first (HTML/SVG/DSL) approach family over image-generation approaches.

## Follow-up

- **Relevance:** 4 — canonical staged-pipeline prior art that shapes our harness structure and contributes the VER metric; its eval metrics are superseded by the validated methods in newer ingests.
- Add a render/compile-rate (VER-analogue) field to our experiment metrics.json schema.
- Steal the goal-with-rationale JSON structure for approach prompt specs.
