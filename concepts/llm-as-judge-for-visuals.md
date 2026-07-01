---
kind: concept
name: "LLM-as-judge for visuals"
status: seedling
added: "2026-07-01"
sources:
  - "[[literature/papers/shbita2025mermaidseqbench]]"
  - "[[literature/papers/liang2025diagrameval]]"
  - "[[literature/papers/tang2026igenbench]]"
  - "[[literature/papers/berger2024visualization]]"
  - "[[literature/papers/dibia2023lida]]"
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
- Model-dependent scores are gameable: a diagram that stuffs in all the caption text with zero actual data flow can achieve a perfect model-similarity score (DiagramEval's metric-hacking case study) — keep judge scores separated from, and cross-checked by, structural metrics.
- Atomic yes/no question decomposition makes a judge both interpretable and human-aligned: IGenBench's Gemini-2.5-Pro verifier hits Pearson r=0.90 with expert annotators, and rankings stay stable (ρ≥0.95) across judges from three providers even when absolute scores differ. Judge validity should be *validated once* against humans, then per-dimension error rates tracked (their verifier is over-positive on data-encoding questions, 12% disagreement).
- Report two granularities: per-question accuracy (Q-ACC) and all-questions-correct rate (I-ACC) — the gap between them (0.90 vs 0.49 for the best model in IGenBench) is where "looks mostly right" hides "unusable."
- Judge the *rendered image*, not the source code/spec: judging specs assumes the model "can envision the resulting visualization," which is unvalidated (Berger & Liu). And a perceptual judge's human-alignment is itself an open question — summary/ensemble extraction, preattentive salience, and just-noticeable differences may all diverge from human vision (ViT coarse spatial grids) — so AI-vs-human rank agreement must be measured, not assumed.
- Earliest instance of the pattern: LIDA's SEVQ (GPT-4 scores 1–10 with rationale across code accuracy / data transformation / goal compliance / visualization type / data encoding / aesthetics) — usable for critique and auto-repair, but shipped with *no* human-agreement validation, the gap all later work had to close.

## Connections

- Feeds the accuracy axis of our two-axis eval; the glance axis needs judges that model *perception*, not just content — see [[glanceability]].
- Contrast with [[structural-fidelity-metrics]], which replace the judge with deterministic graph comparison where possible.
