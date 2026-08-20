---
kind: paper
title: "SVGenius: Benchmarking LLMs in SVG Understanding, Editing and Generation"
authors: ["Siqi Chen", "Xinyu Dong", "Haolei Xu", "Xingyu Wu", "Fei Tang", "Hang Zhang", "Yuchen Yan", "Linjuan Wu", "Wenqi Zhang", "Guiyang Hou", "Yongliang Shen", "Weiming Lu", "Yueting Zhuang"]
institutions: ["Zhejiang University"]
year: 2025
venue: arXiv preprint (ACM format)
peer_reviewed: false
url: https://arxiv.org/abs/2506.03139
code_url: https://zju-real.github.io/SVGenius
citations: null
source: "raw/papers/chen2025svgenius.pdf"
added: "2026-08-20"
relevance: 4
credibility: 4
status: read
related_experiments: []
related_concepts: ["diagram-dsl-generation"]
tags: [svg, vector-graphics, benchmark, complexity-stratification, llm-evaluation, style-transfer]
---

# SVGenius: Benchmarking LLMs in SVG Understanding, Editing and Generation

## TL;DR

A 2,377-query benchmark over 22 models across three progressive dimensions — understanding (perceptual/semantic QA), editing (bug fixing, code optimization, style editing), generation (text-to-SVG, image-to-SVG, style transfer) — built on real Iconfont SVGs stratified into Easy/Medium/Hard; the headline result is that **every model degrades systematically as SVG complexity rises** (Claude-3.7-Sonnet 80.3% → 33.3% perceptual QA), and reasoning-enhanced training buys more than parameter scaling.

## Claims

- Existing SVG benchmarks are fragmented (one capability each), single-domain, and built on structurally trivial samples; a benchmark needs complexity stratification to say anything useful.
- **Complexity degradation is universal, not a small-model artifact.** All 22 models, proprietary included, fall off with path count / control points / command complexity — evidence of a fundamental limitation rather than a capacity gap.
- Degradation rate is task-dependent: *understanding* degrades steepest, *editing* moderately (10–30%), *generation* is most resilient.
- Reasoning-augmented training beats pure scaling: DS-R1-Qwen-32B (51.85% Easy SQA) edges out Qwen2.5-72B (50.54%); QwQ-32B's 91.14% style-editing accuracy beats GPT-4o's 78.48%.
- SVG-specialized models (Iconshop, StarVector) win narrowly in their one task and fail everything else — domain expertise purchased at the cost of general robustness.
- Style transfer is the hardest capability across the board, with no prior standardized benchmark.

## Methods

- Data: >100K Iconfont user-created icons → structural/semantic/compactness filtering → geometric normalization and attribute standardization → 927 SVGs; ten volunteers manually review rasterizations.
- Complexity stratification on three normalized indicators (path count, control points, complex commands), weighted and split 33/34/33 into Easy/Medium/Hard; 200 sampled then manually pruned to 100 per level → 300 balanced samples over 24 domains.
- 8 task categories, 18 metrics. Notable metric design: **rMSE** (MSE normalized by reference variance) because localized edits produce absolute differences too small to detect; **PSS** and **rCLIP** introduced for code-structure consistency and semantic preservation; perceptual quality via HPS/Aesthetic; image-to-SVG via LPIPS/SSIM/DINO.
- 22 models spanning proprietary (GPT-4o, Gemini-2.0-Flash, Claude-3.7-Sonnet), open-source (DeepSeek-R1, Qwen2.5/3, QwQ, Llama-3.2, Mistral-Small), and SVG-specialized; zero-shot, default configs, three runs per setting.

## Results

- Understanding, Easy → Hard perceptual QA: Claude-3.7-Sonnet 80.25 → 33.33; GPT-4o 82.72 → 42.22; Gemini-2.0-Flash 77.78 → 31.11. Roughly **half the accuracy lost** moving from simple to complex icons.
- Semantic QA is more robust than perceptual QA at Hard (Claude 71.11 vs 33.33) — reading *what an icon means* survives complexity better than counting/locating its parts.
- Editing: Claude-3.7-Sonnet leads bug fixing (76% Easy, 75% Medium); QwQ-32B leads style editing (91.14% Easy). Code optimization shows wild RLD variance (Qwen3-8B 221.88, DeepSeek-R1 1227.70 at Medium) — models break rendering while compressing.
- Generation: GPT-4o best (20.35 HPS, 19.72 PSS text-to-SVG; 23.43 PSS multimodal). Multimodal input consistently beats text-only for spatial reasoning.
- Scaling within a family is real but sublinear: Qwen3 1.7B → 32B moves Easy bug fixing 22.34% → 56.12%.

## Critique / open questions

- **The corpus is icons.** 300 Iconfont samples, 24 domains, ~10 paths mean — the most complex sample here is far below a hand-authored explanatory diagram with labeled axes, text runs, and annotated regions. "Hard" in SVGenius is not hard in our sense.
- Understanding tasks are answered **from SVG code as text**, so perceptual QA measures a model's ability to mentally rasterize path data — a strange proxy that may under-report what a model can do when it also *sees* its render.
- No human evaluation of generation quality; HPS/Aesthetic are learned reward models with their own biases, and the newly introduced PSS/rCLIP metrics are validated only in the appendix.
- ACM template with placeholder venue ("Conference'17") — a preprint, not an accepted paper, at capture time.
- Model set is now dated (GPT-4o, Claude-3.7-Sonnet, Gemini-2.0-Flash). Absolute numbers are a 2025 snapshot; the *shape* of the degradation curve is the durable finding.

## So what for visual-conveyance

- **Direct calibration for approach 10-combined**, which converged on prose + hand-authored inline SVG + CSS in 6/6 cells. This is the evidence base for how far to trust that channel: generation is the *most* complexity-resilient of the three dimensions, which supports the choice — but resilience is relative, and the corpus tops out at icon complexity, so it does not license arbitrarily intricate SVG.
- **Complexity is the axis to control, and it's measurable.** Their three indicators (path count, control points, complex commands) are cheap to compute on our generated pages. A page whose SVG complexity sits in their Hard band is in the regime where models demonstrably lose the plot — that's a candidate mechanical check to add alongside `tools/layout_check.py`, and a candidate covariate for explaining per-cell accuracy variance.
- **Semantic robustness > perceptual robustness** cuts in our favor: what survives complexity is meaning-level reasoning, what collapses is precise counting and spatial placement. Predicts our SVG failure mode is *misplaced/miscounted elements in a page that still reads as the right idea* — exactly the "renderable but subtly wrong" pattern already noted in [[diagram-dsl-generation]] for Mermaid. Worth checking whether our per-fact accuracy audits show quantity/position errors specifically.
- **Models break rendering while optimizing it.** The code-optimization RLD blowups are a warning about any self-editing or compaction stage we add to a generation pipeline: an edit pass that isn't render-verified can silently destroy the artifact.
- **Judge-side caution.** If an AI evaluator's ability to read SVG code degrades with complexity the way these models' does, our evaluators are least reliable exactly on the most elaborate pages. Argues for keeping the screenshot-first eval protocol (rubric v1 already does this) rather than ever letting a judge score from source.

## Trust signals

- **Credibility:** 4 — large, carefully constructed benchmark (real-world corpus, principled complexity stratification, ten-person manual review, three runs per setting, 22 models spanning all model classes), with data and code released at zju-real.github.io/SVGenius from an established Zhejiang University group. Held below 5 by preprint status (no peer review at capture), no human evaluation of generation, and two of the headline metrics being self-introduced and appendix-validated.

## Follow-up

- **Relevance:** 4 — the only quantitative footing we have for the inline-SVG channel that our best approach now leans on, and it hands us a computable complexity stratifier. Not a 5 because the corpus is icons rather than explanatory diagrams, so the thresholds transfer as direction, not magnitude.
- Compute path count / control points / complex-command counts over the SVG in our 60 manifest cells; test whether SVG complexity predicts per-cell accuracy or layout-gate failures.
- If it does, that's a v2 spec constraint for approach 10 (an SVG complexity budget, mirroring the element-count budget [[glanceability]] already gives us).
