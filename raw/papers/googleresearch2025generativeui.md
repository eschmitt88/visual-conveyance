---
source_url: https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/
fetched: 2026-07-01
title: "Generative UI: A rich, custom, visual interactive user experience for any prompt"
authors: ["Yaniv Leviathan", "Dani Valevski", "Vishnu Natchu", "Yossi Matias", "et al. (Google Research)"]
published: 2025-11-18
format: html-md
kind: post
---

# Generative UI: A Rich, Custom, Visual Interactive User Experience for Any Prompt

**Publication Date:** November 18, 2025
**Authors/Team:** Yaniv Leviathan (Google Fellow), Dani Valevski (Senior Staff Software Engineer), Vishnu Natchu (Principal Engineer), Yossi Matias (VP & Head of Google Research), with co-authors Matan Kalman, Danny Lumen, Eyal Segalis, Eyal Molad, Shlomi Pasternak, Valerie Nygaard, Srinivasan Venkatachary, and James Manyika. Work across Google Research, Google Search, and Gemini teams (~25+ contributors).

## Overview

Google Research introduces an implementation of generative UI enabling AI models to dynamically create immersive visual experiences and interactive interfaces — web pages, games, tools, applications — customized in real time for any user prompt. Rather than presenting content through static, predefined interfaces, the approach generates entirely new user experiences "automatically designed and fully customized in response to any question, instruction, or prompt."

## Core Motivation

Traditional AI outputs — "walls of text" and predefined response formats — fail to provide optimal user experiences for diverse contexts. Different scenarios demand different interfaces: explaining complex concepts to children vs adults requires distinct content organization and feature sets; a social media gallery differs fundamentally from a travel itinerary. Generative UI treats UI creation as an inherent capability of large language models.

## What Generative UI Accomplishes

"Generative UI is a powerful capability in which an AI model generates not only content but an entire user experience." Interfaces are:

- Fully customized to specific prompts and user needs
- Dynamically generated on demand rather than selected from predefined templates
- Interactive and immersive rather than static text
- Scalable from single-word prompts to detailed instructions

## Technical Implementation

1. **Model foundation:** Gemini 3 Pro with agentic coding capabilities — the system writes and executes code that generates interactive experiences.
2. **Tool access:** a server provides image generation, web search, and other external services; results can be routed back to the model for quality improvement or streamed directly to the user's browser for efficiency.
3. **System instructions:** "carefully crafted" — clear goals and planning frameworks, concrete examples of desired outputs, technical specifications (formatting requirements, tool manuals), tips for avoiding common errors.
4. **Post-processing:** outputs pass through "a set of post-processors to address potential common issues" for reliability and consistency.
5. **Styling configuration:** products can configure consistent styling for all users; otherwise the system picks a style or accepts user style preferences.

**Workflow:** user prompt → system instructions guide reasoning → model uses tools for information/assets → output is HTML/CSS/JavaScript → browser renders the interactive interface directly.

## Evaluation Results

- Compared against: websites designed by human experts for specific prompts; top Google Search results; baseline LLM raw-text outputs; standard markdown responses.
- Preference hierarchy: human-expert sites ranked highest, followed closely by generative UI with "a substantial gap from all other output methods" (text/markdown/search). Evaluation excluded generation-speed considerations.
- "The performance of generative UI strongly depends on the performance of the underlying model, and our newest models perform substantially better."
- **PAGEN dataset:** expert-made websites, to be released to the research community for standardized evaluations.
- Companion research paper: "Generative UI: LLMs are Effective UI Generators."

## Use Cases

- Educational: probability concepts, interactive fractal exploration, gamified math, explaining transcription in prokaryotic vs eukaryotic cells.
- Practical tools: Thanksgiving event planning, fashion advice, travel itineraries, social-media galleries for businesses.
- Creative: Van Gogh gallery curation with context, game-based learning, interactive simulations.

## Deployment Surfaces

- **Gemini app** (two experiments rolling out): *Dynamic View* — Gemini "designs and codes a fully customized interactive response for each prompt, using Gemini's agentic coding capabilities"; understands that "explaining the microbiome to a 5 year old requires different content and a different set of features than explaining it to an adult." *Visual Layout* — complementary layout customization.
- **Google Search AI Mode:** Gemini 3 builds bespoke generative UIs from prompt intent; available to Google AI Pro and Ultra subscribers in the US via the "Thinking" model option.

## Limitations and Future Directions

- **Generation speed:** "can sometimes take a minute or more to generate results."
- **Accuracy:** the system occasionally produces "inaccuracies in the outputs" — explicitly flagged as needing research attention.
- Future: wider set of services, adapting to additional context and human feedback, increasingly helpful visual and interactive interfaces.
