---
source_url: https://arxiv.org/html/2410.04280
abs_url: https://arxiv.org/abs/2410.04280
fetched: 2026-07-01
title: "The Visualization JUDGE: Can Multimodal Foundation Models Guide Visualization Design Through Visual Perception?"
authors: ["Matthew Berger", "Shusen Liu"]
format: html-md
---

# The Visualization JUDGE: Can Multimodal Foundation Models Guide Visualization Design Through Visual Perception?

**Authors:** Matthew Berger (Vanderbilt University), Shusen Liu (Lawrence Livermore National Laboratory)
**ArXiv ID:** 2410.04280 (October 2024), cs.HC, position paper
**License:** CC BY 4.0

## Abstract

The paper investigates whether multimodal foundation models (MFMs) — systems capable of processing both vision and language — can effectively guide data visualization design through visual perception capabilities. Rather than using these models purely as generative tools for creating visualizations, the authors propose viewing MFMs as "visualization judges" that can critique designs and recommend improvements. The research characterizes two distinct model classes (text-to-image generative models and multimodal large language models) and examines how their outputs enable different visualization optimization strategies. The authors argue that MFMs offer a promising avenue for automation-assisted design that leverages their broad perceptual knowledge while acknowledging current limitations in visualization-specific understanding.

## 1. Introduction

- Visualization design = sequential choices about data representation, visual encoding, spatial arrangement, interaction — conceptualized as *search* through a design space. Requires iterating: perceive current visualization → reflect on strengths/weaknesses → update design choices.
- Prior LLM-for-visualization work operates solely on textual inputs (dataset descriptions, intent) *without perceiving the produced visualization image* — a critical gap.
- MFMs overcome this: (1) image-based perception matching human cognition, (2) reasoned judgment about quality relative to goals, (3) actionable guidance for improvement.
- Central thesis: position MFMs as **judges**, not generators — receive evidence (image + goals), analyze, render judgment (critique), issue rulings (improvements). Preserves human creativity while automating perceptual/evaluative tasks.

## 2. How Effective Are MFMs at Perceiving Visualizations?

- MFMs are trained mostly on natural images; visualization is a niche category → visualization-specific knowledge is limited relative to general visual understanding.
- Early evidence of non-trivial visualization knowledge: SDXL renders a plausible "juxtaposed multiple-view visualization" (stacked bars/areas, consistent color encoding); an MLLM correctly reads a bar chart ("Shanghai has the most metro stations…").

### Research needs: measuring human–AI perceptual alignment

1. **Summary extraction:** do MFMs do ensemble processing (mean/variance at a glance) like humans, or extract-and-compute shortcuts? Use control tasks (count marks), vary marks/channels/counts.
2. **Preattentive features:** measure whether MFMs identify preattentively salient features; 200ms exposure doesn't translate to machines, so prompting strategy (open-ended "what stands out") is the analogue.
3. **Just-noticeable difference (JND):** MFMs use vision transformers over coarse spatial grids → may struggle with low-level visual queries (color equivalence, bar-length differences, correlation in scatterplots). Adapt psychophysics staircasing to models.

### Adapting capabilities

- Fine-tuning on human-annotated preference data works but risks catastrophic forgetting.
- Prompting/in-context personas steer capable models without fine-tuning costs.

## 3. MFMs as Visualization Judges (court analogy)

- **Input (evidence):** visualization image + text goals. Images beat specifications: a 2,000-point scatterplot is more analyzable as an image than as 2,000 tabular items. T2I text = low-level visual pattern descriptions; MLLM text = patterns + data attributes + high-level analytic objectives.
- **Analysis (judgment):** T2I models used as *density estimators* — conditional likelihood p(image | goal text) as a continuous score of goal satisfaction. MLLMs output continuous scores (not necessarily calibrated), binary responses, multiple-choice selections, or free-form critiques. Output must remain **actionable**.
- **Action (ruling):** T2I likelihoods are differentiable → gradient-based optimization ∇log p_θ(I|c) over visualization parameters. MLLMs give no gradients → (1) designer specifies a structured design/action space the model selects from, or (2) autoregressive iterative updates.

### Trade-offs (Figure 2)

- **T2I models:** constrained design space (low-level continuous parameters: mark size, opacity, color transfer functions, positions) but effective gradient optimization.
- **MLLMs:** expansive design space (data transformations, encodings, view arrangements) but no optimization direction; success depends entirely on the model's text output.
- **Comparative judgments (ranking):** the middle ground.

## 4. Visualization Design with T2I Models

- Formalized as inverse problem: maximize log p_θ(V(D, v) | c) over parameter vector v, where V is the visualization function, c the user's goal text. The model is a *prior*; optimization is grounded in hypothesis-driven goals (correlation, clusters, trends, outliers).
- Optimizable parameters: data-independent choices (mark size/color/opacity for memorability or overplotting reduction); visual encodings (data-domain subsetting, parameterized mapping functions, visual range bounds, design-principle-respecting color functions); multi-view arrangement (position/size under layout constraints); technique parameters (UMAP/t-SNE neighborhood size, layout iterations).
- Example from prior work: transfer-function optimization for volume rendering from descriptions like "show the tree with warm colors."
- **Differentiable visualization challenge:** rasterizing marks produces step functions; needs differentiable rendering, anti-aliased soft edges, graphics-inspired methods. Designer must declare V respecting differentiability.

## 5. Visualization Design with MLLMs

### 5.1 Explicit optimization

- Zeroth-order optimization: present candidates, ask for rankings/scores; preferences drive parameter updates. Gets much harder as parameter space grows; domain constraints narrow the search.
- **AVA example (Liu et al.):** autonomous visualization agents where MLLMs iteratively refine visualizations; model must understand domain concepts (e.g. "circle of Willis") and perceive issues like overplotting that are hard to mathematize.

### 5.2 Evaluation and recommendation

- LLM-as-evaluator precedent from NLP ("LLM evaluator performs similarly to the human experts on textual input").
- Key critique of existing rec systems (LLM4Vis etc.): they recommend from intermediate representations *without viewing actual visualizations* — "an implicit assumption has been made, i.e., the LLM can envision the resulting visualization." Evidence for that assumption is insufficient; quality depends on the *combined effect of data and design* visible only in the rendered image. "The inclusion of visual perception represents the most straightforward process that best resembles how humans approach such tasks."

### 5.3 Visualization generation vs visualization design

- **Generation** (code/spec production) is mechanistically achievable by text LLMs. **Design** is the iterative loop: conceive → implement → *visually assess the render* → identify weaknesses → re-conceive.
- "Visual perception will be critical in forming such an iterative improvement loop." Requires an autonomous visualization agent coordinating multiple model components (MLLM conception/assessment + T2I parameter refinement).

## 6. Discussion and Research Directions

- **Robustness:** optimized designs are brittle to data resampling — bootstrap-style consistency of MFM judgments across resampled candidates as a robustness criterion.
- **Diverse design sets:** "visualization is subjective; a visualization considered 'optimal' by one person might not be for another" — sample from posterior over parameters instead of single-point optimization; return sets of good designs.
- **Image+text goal specification:** support reference visualizations and sketches as goals, not just text.
- **Visualization for machine comprehension:** design visualizations optimized for *machine* readers — images reduce long-context comprehension challenges; LLMs visualizing their reasoning shows encouraging effects.

## Conclusions

1. Reframe MFMs as judgment-bearing critics that perceive, evaluate, recommend — not generators.
2. T2I = gradient-scored low-level parameter optimization; MLLM = broad design choices via language, zeroth-order search only.
3. Research agenda: human–AI perceptual alignment (ensemble processing, preattentive features, JND), robustness, diverse design discovery, machine-centric visualization.
4. Leverage MFMs while recognizing limited visualization-specific knowledge; keep human-in-the-loop.
