---
kind: post
title: "Generative UI: A rich, custom, visual interactive user experience for any prompt"
author: "Yaniv Leviathan, Dani Valevski, Vishnu Natchu, Yossi Matias, et al. (Google Research)"
url: https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/
source: "raw/papers/googleresearch2025generativeui.md"
added: "2026-07-01"
relevance: 5
related_experiments: []
related_concepts: ["generative-ui", "staged-generation-pipelines"]
tags: [generative-ui, google, gemini, interactive, html-generation, production-system, evaluation]
---

# Generative UI (Google Research, Nov 2025)

## TL;DR

Google's production system where the model designs and codes a bespoke interactive HTML/CSS/JS experience per prompt (Gemini 3 Pro + agentic coding + tools + post-processors), shipped in the Gemini app (Dynamic View) and Search AI Mode. In human preference evals, generated UIs beat text, markdown, and search results by "a substantial gap," trailing only human-expert-designed sites.

## Key points

- **Core claim:** "walls of text" are the wrong default output; treating the *entire user experience* as generable — content, layout, interactivity — is both feasible with current models and strongly preferred by users. This is the industrial-scale version of our project's thesis.
- **The method:** the AI-to-human conveyance problem is solved with a staged system, not a bare prompt: (1) carefully crafted system instructions (goals, planning framework, concrete output examples, tool manuals, error-avoidance tips), (2) tool access (image gen, web search) with results routed to model or browser, (3) HTML/CSS/JS as the output medium, (4) post-processors for common failure modes, (5) configurable consistent styling.
- **Audience adaptation is a headline capability:** "explaining the microbiome to a 5 year old requires different content and a different set of features than explaining it to an adult" — reader-tailoring is a first-class design axis, matching our non-expert-reader focus.
- **Evaluation:** preference ranking vs four baselines (expert sites > generative UI >> markdown/text/search). Quality "strongly depends on the underlying model." PAGEN dataset of expert-made websites announced for standardized evaluation.
- **Known weaknesses:** latency ("a minute or more") and *accuracy* — Google explicitly flags factual inaccuracies in generated experiences as an open problem. Preference evals measure appeal, not correctness or comprehension.

## So what for visual-conveyance

- Strongest external validation of the project premise: the biggest search company concluded that bespoke generated visual/interactive pages beat text answers for conveying information, and shipped it. Our "interactive HTML page" approach family is their architecture in miniature; their system-instruction structure (planning framework + concrete examples + error tips) is a template for our approach prompt specs.
- Equally important is what they *didn't* solve: their eval is holistic human preference — no factual-accuracy axis (they admit inaccuracies) and no glance-comprehension measurement. Our two-axis eval (atomic fact verification + glance comprehension for non-experts) evaluates exactly the dimensions their deployed system lacks. That's the gap this project lives in.
- Their model-dependency finding cuts both ways for us: approach rankings may shift with generator model — worth pinning the generator model per experiment (config.yaml) and treating model as a variable, not a constant.
- Watch for the PAGEN dataset release — expert-made websites as references could serve as calibration material for our judges or as an approach-quality ceiling.

## Follow-up

- **Relevance:** 5 — production-scale prior art for our exact problem; seeds the generative-ui concept and frames our niche (accuracy + glanceability evaluation) precisely.
- Fetch the companion paper "Generative UI: LLMs are Effective UI Generators" (PAGEN details, preference numbers) for a future ingest.
- Mirror their system-instruction anatomy in our `approaches/` prompt specs; consider a latency field per approach since they flag generation time as the practical constraint.
