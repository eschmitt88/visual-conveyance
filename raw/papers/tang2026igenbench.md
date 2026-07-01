---
source_url: https://arxiv.org/html/2601.04498
abs_url: https://arxiv.org/abs/2601.04498
fetched: 2026-07-01
title: "IGenBench: Benchmarking the Reliability of Text-to-Infographic Generation"
authors: ["Yinghao Tang", "Xueding Liu", "Boyuan Zhang", "Tingfeng Lan", "Yupeng Xie", "Jiale Lao", "Yiyao Wang", "Haoxuan Li", "Tingting Gao", "Bo Pan", "Luoxuan Weng", "Xiuqi Huang", "Minfeng Zhu", "Yingchaojie Feng", "Yuyu Luo", "Wei Chen"]
format: html-md
---

# IGenBench: Benchmarking the Reliability of Text-to-Infographic Generation

**Institutions:** State Key Lab of CAD&CG Zhejiang University; UESTC; University of Virginia; HKUST(GZ); Cornell University; Zhejiang University; National University of Singapore
**ArXiv ID:** 2601.04498 (January 2026)
**Project site / dataset:** https://igen-bench.vercel.app/

## Abstract

Infographics combine data visualizations with textual and illustrative elements for information communication. While recent text-to-image (T2I) models generate aesthetically appealing images, their reliability for infographic generation remains uncertain. Generated outputs may appear correct but contain overlooked issues like distorted data encoding or incorrect text. The authors present IGenBench, the first benchmark evaluating text-to-infographic generation reliability, comprising 600 curated test cases spanning 30 infographic types. The evaluation framework decomposes reliability verification into atomic yes/no questions based on 10 question types, employing multimodal large language models (MLLMs) to verify each question. Results yield question-level accuracy (Q-ACC) and infographic-level accuracy (I-ACC). Comprehensive evaluation of 10 state-of-the-art T2I models reveals: (i) a three-tier performance hierarchy with the top model achieving Q-ACC of 0.90 but I-ACC of only 0.49; (ii) data-related dimensions emerging as universal bottlenecks (e.g., Data Completeness: 0.21); and (iii) the challenge of achieving end-to-end correctness.

## 1. Introduction (key points)

- Infographics = "composite visual artifacts that integrate data visualizations with textual and illustrative elements, such as pictograms, thematic icons, semantic text, and metaphorical imagery."
- T2I models suffer inherent uncertainty; generated charts may appear correct but contain "distorted data encoding (e.g., incorrect bar heights) or textual errors" that mislead users.
- No prior benchmark targets text-to-infographic generation; existing chart-generation evals rely on holistic MLLM scoring with limited interpretability.
- IGenBench: 600 curated cases across 30 types / 6 categories, built from 40K+ real-world infographics via clustering, sampling, quality filtering. Design intent + underlying data extracted per case and synthesized into self-contained prompts.
- Verification decomposed into atomic self-contained yes/no questions from (i) prompt-explicit constraints and (ii) expert-informed seed dimensions (data completeness, ordering, encoding). MLLM verifies each question → Q-ACC and I-ACC.

## 2. Related Work (key points)

- Text-code-chart paradigm (LLM generates D3.js etc.): requires extensive manual templates, tightly coupled to asset libraries, struggles with free-form pictograms/icons/metaphorical imagery.
- T2I approaches now mainstream for infographics (BizGen layout-guided cross-attention; Nanobanana-Pro etc.).
- Existing benchmarks: PartiPrompt, DrawBench, TIFA, T2I-CompBench (natural images); VisJudge-Bench, VIS-Shepherd, MatplotBench (holistic MLLM chart scoring); VISEval (rule-based chart legality); StructBench, ChartMark. None jointly evaluate semantic alignment + data-encoding correctness for infographics.

## 3. Dataset Construction

- Sources: Statista, Visual Capitalist, real-world portion of ChartGalaxy — 42,315 infographics total.
- Taxonomy: 6 categories, 30 types — Composition (pie, donut, semicircle donut, stacked bar, treemap, Voronoi treemap, waffle, proportional area); Categorical Comparison (vertical/horizontal/grouped bar, lollipop, radar, pictorial, dot); Trend & Evolution (line, stepped line, area, layered area, stacked area, bump); Deviation & Gap (diverging bar, pyramid, dumbbell, slope, span); Correlation & Flow (bubble, heatmap, alluvial); Bonus (multi-panel layouts).
- Clustering & sampling: MLLM assigns type + semantic description; intra-type dedup; k-means C=10 clusters; K=5 samples per type; manual quality checks.
- Human-in-the-loop prompt generation: MLLM extracts (1) structural design description ("Create an infographic that…", no colors/fonts/watermarks) and (2) the underlying data table; both manually verified; fused into a single prompt ending "The given data is: {data}."

## 4. Evaluation Protocol

**Question taxonomy (10 types, by expert consensus over 300 samples):** Title & Subtitle; Chart/Diagram Type; Decorative/Non-data Elements; Annotations & Callouts; Axes & Scales; Legend & Category Mapping; Data Marks; Data Completeness; Data Ordering; Data Encoding.

**Prompt decomposition:** prompt split into sentences; LLM converts each into a self-contained yes/no question answerable solely by inspecting the infographic. Expert-informed augmentation adds chart-specific questions instantiating data completeness / ordering / encoding. Final Q(p) = Q_p(p) ∪ Q_e(p).

**Verification:** strict binary — any ambiguity, partial satisfaction, or missing visual evidence scores 0.

**Metrics:**
- Q-ACC = fraction of satisfied questions over all questions.
- I-ACC = fraction of infographics where ALL associated questions are satisfied.

**Statistics:** 600 prompts; 5,259 verification questions; typically 7–11 questions per infographic; prompt lengths 1–2 orders of magnitude longer than typical T2I prompts.

## 5. Experiments

**Models (10):** open-source — Qwen-Image, HiDream-I1, FLUX.1-dev, Z-Image-Turbo; closed-source — Seedream 4.5, Nanobanana, Nanobanana-Pro, GPT-Image-1.5, Image-01, P-Image. Verifier: Gemini-2.5-Pro.

**Table 1 (per-question-type Q-ACC, overall Q-ACC, I-ACC):**

| Model | Comp. | Enc. | Order | Marks | Anno. | Axes | Leg. | Chart | Title | Deco. | Q-ACC | I-ACC |
|-------|-------|------|-------|-------|-------|------|------|-------|-------|-------|-------|-------|
| Nanobanana-Pro | 0.84 | 0.86 | 0.90 | 0.87 | 0.93 | 0.93 | 0.96 | 0.92 | 0.98 | 0.94 | 0.90 | 0.49 |
| Seedream-4.5 | 0.34 | 0.37 | 0.47 | 0.48 | 0.70 | 0.70 | 0.81 | 0.68 | 0.95 | 0.84 | 0.61 | 0.06 |
| GPT-Image-1.5 | 0.38 | 0.48 | 0.44 | 0.57 | 0.50 | 0.54 | 0.57 | 0.68 | 0.60 | 0.80 | 0.55 | 0.12 |
| Nanobanana | 0.18 | 0.31 | 0.27 | 0.44 | 0.54 | 0.57 | 0.52 | 0.60 | 0.65 | 0.81 | 0.48 | 0.02 |
| Qwen-Image | 0.10 | 0.13 | 0.19 | 0.29 | 0.43 | 0.37 | 0.51 | 0.48 | 0.56 | 0.78 | 0.36 | 0.01 |
| Z-Image-Turbo | 0.10 | 0.16 | 0.16 | 0.25 | 0.38 | 0.31 | 0.58 | 0.42 | 0.61 | 0.73 | 0.35 | 0.00 |
| P-Image | 0.08 | 0.15 | 0.19 | 0.27 | 0.36 | 0.28 | 0.54 | 0.43 | 0.58 | 0.68 | 0.34 | 0.00 |
| Image-01 | 0.01 | 0.05 | 0.04 | 0.10 | 0.10 | 0.14 | 0.03 | 0.22 | 0.14 | 0.47 | 0.13 | 0.00 |
| HIDream-I1 | 0.01 | 0.03 | 0.03 | 0.10 | 0.07 | 0.14 | 0.10 | 0.26 | 0.19 | 0.20 | 0.11 | 0.00 |
| FLUX.1-dev | 0.00 | 0.03 | 0.01 | 0.08 | 0.06 | 0.06 | 0.01 | 0.24 | 0.09 | 0.39 | 0.10 | 0.00 |
| **Average** | **0.21** | **0.26** | **0.27** | **0.35** | **0.40** | **0.40** | **0.46** | **0.49** | **0.54** | **0.66** | **0.39** | **0.07** |

**Key findings:**

- Three-tier hierarchy: Nanobanana-Pro (0.90) >> Seedream-4.5 / GPT-Image-1.5 (0.61 / 0.55) >> rest (<0.48). Average Q-ACC only 0.39.
- Data fidelity is the universal bottleneck: Data Completeness 0.21 avg, Data Encoding 0.26, Ordering 0.27 — vs decorative elements 0.66, titles 0.54. Models excel at aesthetics, fail at faithful data encoding.
- Q-ACC ≠ reliability: best model 0.90 Q-ACC → only 0.49 I-ACC; Seedream 0.61→0.06; GPT-Image-1.5 0.55→0.12; most models near-zero I-ACC. "Long-tail" failure mode: one or two wrong dimensions invalidate the whole infographic.
- Conclusion: current T2I models cannot be trusted to autonomously generate reliable infographics; human verification/post-editing necessary.

**Human alignment (5.3):** Gemini-2.5-Pro automatic scores vs expert annotators, 100 resampled 25-example subsets: Pearson r = 0.90, p = 7.54e-37. IGenBench vs LMArena rankings: Spearman ρ = 0.78 (p=0.04); Seedream-4.5 4th on LMArena but 2nd on IGenBench; GPT-Image-1.5 1st on LMArena, 3rd on IGenBench.

**Evaluator selection (5.4):** Gemini-2.5-Pro is the only evaluator with human correlation > 0.8 (0.90); GPT-5-mini 0.70; GLM-4.5v 0.75; most open-source MLLMs < 0.5.

**Case study (5.5):** proportional area chart, 15 bubbles required — Nanobanana-Pro generates 16 with wrong color encoding; Seedream and Qwen-Image show wrong ranking order and garbled text.

## Appendix highlights

- **D.1 Chart-type breakdown:** canonical types easier (Pie avg Q-ACC 0.53) vs complex encodings much harder (Bump chart 0.25). Model rankings stable across types (avg Spearman 0.92).
- **D.2 Data leakage:** on 100 post-Dec-2025 Visual Capitalist infographics, most models stable (avg change 0.7%); GPT-Image-1.5 drops 0.52→0.29, suggesting contamination.
- **D.3 Evaluator error analysis:** Data Encoding hardest for the verifier — 12.12% disagreement with humans (over-positive: misses subtle encoding violations); Title & Subtitle 2.50%, Data Completeness 2.50%, Ordering 0.00%.
- **D.4 Evaluator bias:** three verifiers from three providers, rankings pairwise Spearman ρ ≥ 0.95; Gemini does not favor Google generators.
- **D.5 Visual-similarity metrics** (CLIP, SSIM, PSNR, LPIPS) have limited discriminative power and inconsistent rankings; QA-based evaluation captures substantially more than visual resemblance.

## Limitations

Does not assess communicative effectiveness (whether the infographic conveys the intended message), accessibility, or aesthetics — reliability is treated as a foundational prerequisite for those. Those dimensions need user studies / perceptual modeling. Only a selected set of models due to cost; living benchmark planned.
