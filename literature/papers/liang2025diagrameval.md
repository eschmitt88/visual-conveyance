---
kind: paper
title: "DiagramEval: Evaluating LLM-Generated Diagrams via Graphs"
authors: ["Chumeng Liang", "Jiaxuan You"]
institutions: ["University of Illinois Urbana-Champaign"]
year: 2025
venue: EMNLP 2025 Main
peer_reviewed: true
url: https://arxiv.org/abs/2510.25761
code_url: https://github.com/ulab-uiuc/diagram-eval
citations: null
source: "raw/papers/liang2025diagrameval.md"
added: "2026-07-01"
relevance: 5
credibility: 4
status: read
related_experiments: []
related_concepts: ["structural-fidelity-metrics", "llm-as-judge-for-visuals"]
tags: [evaluation, diagrams, graph-metrics, svg, structural-fidelity, clipscore, metric-hacking]
---

# DiagramEval: Evaluating LLM-Generated Diagrams via Graphs

## TL;DR

Evaluates LLM-generated (SVG) diagrams by parsing them into text-attributed graphs — text elements as nodes, connections as directed edges — then scoring node alignment and path alignment (precision/recall/F1) against a reference diagram. Correlates with human "same logic?" judgments ~4x better than CLIPScore.

## Claims

- **Core claim:** Diagram accuracy should be measured on structure (which elements exist, which are connected/reachable), not on image-embedding similarity; graph-based node/path alignment is more interpretable, harder to game, and better human-aligned.
- CLIPScore is oversensitive to layout/color/style and gameable: a diagram with all caption text but zero data flow scores a perfect CLIPScore-Text while Path F1 = 0.
- Path alignment (reachability between matched nodes, not just direct edges) exposes a weakness no prior metric surfaced: state-of-the-art LLMs are bad at expressing *relationships* in diagrams.

## Methods

- Task: generate a paper's overview diagram as SVG from paper context + captions; compare against ground-truth diagram.
- Graph construction: (1) SVG parse groups text items into node drafts via spatial rules (y-diff < 1.5×font size, x-overlap > 0.2); (2) lightweight VLM (Gemini-2.0-Flash-lite) merges/adds/removes nodes; (3) VLM reads the rendered image + node list to extract directed edges from arrows/lines/proximity.
- Metrics: Node P/R/F1 (text-similarity matching of nodes) and Path P/R/F1 (existence of paths between matched node pairs in generated vs reference graph).
- Dataset: 361 diagrams from CVPR 2025 papers (post-cutoff). Generators: Llama 4 Maverick, Gemini 2.5 Pro, Claude 3.7 Sonnet.

## Results

- Node F1 ≈ 0.33–0.35 and Path F1 ≈ 0.20–0.24 for all three frontier models — absolute structural fidelity of LLM-generated diagrams is *low*.
- Claude 3.7 Sonnet: best on 4/6 metrics; overgenerates (31.7 nodes avg vs Gemini 21.4, Llama 10.7) → high node recall (0.51), poor precision (0.29).
- Human correlation (50 pairs, "same logic?"): Node F1 0.4316, Path F1 0.4052 vs CLIPScore-Text 0.1065, CLIPScore-Image 0.0831.
- Edge-extraction step itself validated at 85.9% (reference) / 90% (generated) accuracy by human check.
- Human raters scored the Gemini-generated diagrams at only 0.33 average similarity to reference; nearly half scored 0.

## Critique / open questions

- Reference-based: needs a ground-truth diagram. Our test cases have `key_facts.md` ground truth, not reference diagrams — we'd match extracted graph elements against key facts instead, which changes the metric from alignment to coverage.
- The pipeline still leans on a VLM for edge extraction (85–90% accurate), so "deterministic" is only ~90% true; errors deflate scores for dense diagrams.
- Path-existence (reachability) is permissive: a spurious hub node could make many pairs reachable and inflate path recall.
- Human eval is small (50 pairs, 2 raters) and only against Gemini outputs.

## Trust signals

- **Credibility:** 4 — peer-reviewed (EMNLP 2025 Main), UIUC group, code + dataset released; citation count not yet established.

## So what for visual-conveyance

- This is the strongest candidate mechanism for our **factual-accuracy axis** on diagram-like artifacts: extract the node/edge graph from the generated presentation, then check coverage of `key_facts.md` entities and relations — structure-checking instead of asking a judge "is this accurate?".
- The metric-hacking case study is a direct warning for our AI-evaluator design: any model-based holistic score can be gamed by approaches that stuff text into the artifact. Keeping accuracy structural (facts present + relations correct) and comprehension separate is exactly the mitigation.
- Baseline expectation-setting: frontier models achieve only ~0.2–0.35 structural F1 on free-form SVG diagram generation. This argues for diagram DSLs (Mermaid/D2), where structure is explicit in the source text and extraction is lossless — no VLM edge-extraction needed.
- Their node/edge extraction pipeline is reusable for scoring our HTML/SVG approaches where structure is *not* explicit.

## Follow-up

- **Relevance:** 5 — provides the canonical evidence and mechanism for our structural-fidelity-metrics concept; directly shapes the accuracy half of the two-axis eval.
- Adapt node/path alignment to key-facts coverage scoring (no reference diagram needed) for our eval harness.
- Look at ulab-uiuc/diagram-eval code for the SVG parsing + VLM edge-extraction prompts.
