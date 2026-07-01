---
kind: paper
title: "IGenBench: Benchmarking the Reliability of Text-to-Infographic Generation"
authors: ["Yinghao Tang", "Xueding Liu", "Boyuan Zhang", "Tingfeng Lan", "Yupeng Xie", "Jiale Lao", "Yiyao Wang", "Haoxuan Li", "Tingting Gao", "Bo Pan", "Luoxuan Weng", "Xiuqi Huang", "Minfeng Zhu", "Yingchaojie Feng", "Yuyu Luo", "Wei Chen"]
institutions: ["Zhejiang University (State Key Lab of CAD&CG)", "UESTC", "University of Virginia", "HKUST(GZ)", "Cornell University", "National University of Singapore"]
year: 2026
venue: arXiv preprint (2601.04498)
peer_reviewed: false
url: https://arxiv.org/abs/2601.04498
code_url: https://igen-bench.vercel.app/
citations: null
source: "raw/papers/tang2026igenbench.md"
added: "2026-07-01"
relevance: 5
credibility: 4
status: read
related_experiments: []
related_concepts: ["llm-as-judge-for-visuals", "structural-fidelity-metrics"]
tags: [benchmark, infographics, text-to-image, evaluation, atomic-questions, data-fidelity, mllm-verifier]
---

# IGenBench: Benchmarking the Reliability of Text-to-Infographic Generation

## TL;DR

First reliability benchmark for text-to-infographic generation: 600 real-world-derived test cases across 30 infographic types, verified by decomposing each prompt into atomic yes/no questions answered by an MLLM (Gemini-2.5-Pro, human correlation r=0.90). Best model gets 0.90 question-level accuracy but only 0.49 fully-correct infographics; data fidelity (completeness 0.21 avg, encoding 0.26) is the universal bottleneck.

## Claims

- **Core claim:** T2I models produce aesthetically convincing infographics that are factually unreliable, and this can be measured interpretably by atomic-question decomposition (Q-ACC) plus an all-questions-correct gate (I-ACC).
- Data-related dimensions (completeness, encoding, ordering: 0.21/0.26/0.27 avg) are far harder than aesthetic dimensions (decorative 0.66, titles 0.54) for every model tested.
- High component-level accuracy does not imply usable output: Q-ACC→I-ACC collapses (0.90→0.49 for the best model; 0.61→0.06 for the runner-up). One wrong dimension invalidates the artifact.
- A single strong MLLM verifier can stand in for humans on this task (r=0.90 with experts) — but it is the *only* verifier tested that clears r>0.8, and it still misses subtle data-encoding violations (12.1% disagreement, over-positive).
- Visual-similarity metrics (CLIP/SSIM/PSNR/LPIPS) carry little signal vs QA-based evaluation.

## Methods

- Dataset: 42,315 infographics from Statista / Visual Capitalist / ChartGalaxy → taxonomy of 6 categories, 30 types → k-means clustering + stratified sampling + manual quality filter → 600 cases.
- Human-in-the-loop prompt build: MLLM extracts structural design description + underlying data table (both manually verified), fused into a self-contained prompt ending "The given data is: {data}."
- Evaluation: prompt decomposed sentence-by-sentence into atomic yes/no questions (10 expert-defined types) + expert-informed augmentation for implicit requirements (data completeness/ordering/encoding). Strict binary scoring — ambiguity = 0. 5,259 questions total, 7–11 per infographic.
- 10 T2I models (Nanobanana-Pro, GPT-Image-1.5, Seedream-4.5, FLUX.1-dev, Qwen-Image, etc.); verifier Gemini-2.5-Pro.

## Results

- Three-tier hierarchy: Nanobanana-Pro Q-ACC 0.90 >> Seedream-4.5 0.61 / GPT-Image-1.5 0.55 >> the rest <0.48 (avg 0.39).
- I-ACC: 0.49 best; near-zero for 7 of 10 models.
- Verifier robustness: three verifiers from three providers give pairwise ranking Spearman ρ ≥ 0.95; no self-preference detected.
- Chart-type difficulty: canonical types (pie 0.53) >> unconventional encodings (bump 0.25).
- Contamination check: GPT-Image-1.5 drops 0.52→0.29 on post-cutoff infographics.

## Critique / open questions

- Explicitly does NOT measure communicative effectiveness — whether a human actually gets the message — which is our second axis. They frame reliability as the prerequisite; we need both.
- Evaluates pixel-generating T2I models only; our approaches generate HTML/SVG/DSL, where text and data are programmatically correct by construction. The relevant transfer is the *evaluation method*, not the model rankings.
- Strict-binary scoring penalizes ambiguity, which is defensible but conflates verifier uncertainty with generator error.
- MLLM verifier is over-positive exactly on the hardest dimension (data encoding) — the residual 12% error sits where it hurts most.

## Trust signals

- **Credibility:** 4 — large multi-institution team (Zhejiang CAD&CG, HKUST(GZ), Cornell, NUS), dataset + gallery released, strong human-agreement validation; arXiv preprint, not yet peer-reviewed.

## So what for visual-conveyance

- **Atomic-question decomposition is the best evaluation recipe we've seen for our factual-accuracy axis:** decompose each testcase's `key_facts.md` into atomic yes/no questions, have an MLLM verify each against the rendered presentation, report both Q-ACC and an I-ACC-style "all facts survive" gate. It is interpretable (which fact failed), validated against humans (r=0.90), and robust across verifier choice at the ranking level.
- The Q-ACC/I-ACC gap is a framing insight for our scoring: an approach that is 90% right per-fact may still produce mostly-unusable artifacts. Our metrics.json should carry both a per-fact score and an all-facts-correct rate per approach.
- Strong argument for our code-based approaches over image generation: T2I fails precisely on data fidelity, which programmatic HTML/SVG/DSL rendering gets for free. If someone proposes an image-model approach for Phase 2, this paper is the counter-evidence.
- Verifier guidance: use a frontier multimodal judge and validate it once against human spot-checks; expect residual over-positivity on data-encoding questions; rankings are stable across judges even when absolute scores are not.
- Their limitation section hands us our niche: communicative effectiveness / glance comprehension is exactly what they leave to future work — our second axis is the unstudied half.

## Follow-up

- **Relevance:** 5 — provides the canonical mechanism (atomic yes/no fact verification, Q-ACC + I-ACC) for our accuracy axis and the strongest published human-validation of an MLLM verifier on info-graphics.
- Prototype key-facts→atomic-questions decomposition for one testcase and compare against a holistic judge score.
- Browse the case gallery (igen-bench.vercel.app) for failure taxonomies worth copying into our eval prompts.
