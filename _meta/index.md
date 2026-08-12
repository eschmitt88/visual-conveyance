---
name: index
description: Entry-point index for this project's knowledge graph.
---

# Index

Orientation for the project knowledge graph. Updated by `/wrap`, `/ingest`,
and `/new-experiment`.

## Maps of Content

(promote a cluster of ≥5 related concepts into `mocs/<theme>.md`)

## Literature

- [[literature/papers/shbita2025mermaidseqbench]] — MermaidSeqBench: NL→Mermaid benchmark, six-dimension LLM-as-judge rubric (rel 4)
- [[literature/papers/liang2025diagrameval]] — DiagramEval: graph-based node/path alignment metrics for LLM diagrams, beats CLIPScore on human correlation (rel 5)
- [[literature/papers/tang2026igenbench]] — IGenBench: text-to-infographic reliability via atomic yes/no MLLM verification, Q-ACC vs I-ACC gap, data fidelity bottleneck (rel 5)
- [[literature/papers/berger2024visualization]] — Visualization JUDGE position paper: MFMs as perceiving judges, generation vs design loop, human-alignment open questions (rel 4)
- [[literature/papers/while2024glanceable]] — CHI '24 glanceability thresholds: donut ~300ms / bar ~500ms / radial ~2.2s, element-count budget, age heterogeneity (rel 4)
- [[literature/papers/dibia2023lida]] — LIDA: canonical four-stage LLM visualization pipeline, VER + SEVQ metrics, grounding-context ablation (rel 4)
- [[literature/posts/googleresearch2025generativeui]] — Google Generative UI: production bespoke-interactive-page generation, preference evals, accuracy + glance gaps = our niche (rel 5)
- [[literature/repos/cathrynlavery-diagram-design]] — diagram-design skill: editorial SVG design system (one accent, 4px grid, density 4/10), 27 types, same artifact contract as ours; basis of approach 08 (rel 5)
- [[literature/repos/3b1b-manim]] — manim/3b1b: explanatory-animation grammar (sequential revelation, morph transforms, persistent scene); grammar ported to static contract in approach 09 (rel 4)

## Active experiments

- [[experiments/2026-07-01-baseline-matrix]] — 7 approaches × 6 testcases; AI eval done (dashboard 9.02 leads), awaiting human ratings
- [[experiments/2026-08-12-combined-matrix]] — DONE: 10-combined 9.15 = NEW #1 (perfect 10.0 accuracy all cells, zero layout defects); choices converged on prose+SVG+CSS, animation 0/6; human pass pending
- [[experiments/2026-08-11-new-approach-matrix]] — DONE: 08 = 09 = 8.47 tie at #3 of 9; 08 beats sibling 03 by +1.09 (constraints vindicated); 09 = 2nd-best glance, weak depth (inverse of prediction); human pass pending

## Open questions

(anything you want to return to)
