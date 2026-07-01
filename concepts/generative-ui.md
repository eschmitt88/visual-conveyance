---
kind: concept
name: "Generative UI"
status: seedling
added: "2026-07-01"
sources:
  - "[[literature/posts/googleresearch2025generativeui]]"
related_concepts: ["staged-generation-pipelines", "glanceability"]
related_experiments: []
tags: [generative-ui, interactive, html, audience-adaptation]
---

# Generative UI

## Definition

Having the model generate not just content but the entire user experience — a bespoke interactive HTML/CSS/JS page whose layout, features, and interactivity are designed per prompt and per audience, instead of pouring content into a fixed template or returning text.

## Why it matters here

Generative UI is the maximal point on our approach spectrum (diagram DSL → static HTML → infographic → interactive page), and it now has production-scale validation:

- Google's system (Gemini 3 Pro + agentic coding + tools + post-processors, shipped in Gemini Dynamic View and Search AI Mode) beats text, markdown, and search results in human preference by "a substantial gap," second only to human-expert-built sites.
- Audience adaptation is intrinsic: the same content gets a different interface for a 5-year-old than for an adult — reader-tailoring as a generation-time design axis, not a post-hoc filter.
- Known open problems are exactly our evaluation axes: factual inaccuracies (admitted, unmeasured by their preference evals) and no measure of what a reader actually absorbs — preference ≠ comprehension.
- Practical constraint: generation latency (a minute or more) and strong dependence on underlying model quality.

## Connections

- Built as a [[staged-generation-pipelines]] instance: system instructions with planning framework + examples, tool calls, post-processing stages.
- Interactivity trades against [[glanceability]]: a rich explorable page may bury the headline message that a static glanceable artifact surfaces immediately — a core tension our two-axis eval should expose.
