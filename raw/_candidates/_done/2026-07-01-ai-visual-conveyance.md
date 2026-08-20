---
kind: candidates
topic: "AI-generated visual communication of complex information — LLM diagram generation (Mermaid/Graphviz/D2), information visualization theory for glanceability and non-expert comprehension, LLM-as-judge evaluation of visualizations, automatic codebase/architecture visualization"
discovered: 2026-07-01
source: discover
n_requested: 12
n_returned: 12
curated: 2026-08-20
---

## 1. MermaidSeqBench: An Evaluation Benchmark for NL-to-Mermaid Sequence Diagram Generation

- url: https://arxiv.org/abs/2511.14967
- type: paper
- summary: Human-verified benchmark (132 core samples) for LLM→Mermaid sequence diagram generation, scored by LLM-as-judge on syntax correctness and practical usability, revealing large capability gaps across models.
- reason: Directly models our loop — LLM generates a diagramming-language artifact, LLM judges it on fine-grained rubrics; their rubric design is reusable for our eval.

## 2. DiagramEval: Evaluating LLM-Generated Diagrams via Graphs

- url: https://arxiv.org/pdf/2510.25761
- type: paper
- summary: Evaluates LLM-generated diagrams by parsing them into node/edge graphs and comparing structure rather than pixels, giving a more objective accuracy signal.
- reason: Offers an accuracy-scoring mechanism that separates structural faithfulness from visual style — exactly the accuracy half of our two-axis eval.

## 3. IGenBench: Benchmarking the Reliability of Text-to-Infographic Generation

- url: https://arxiv.org/pdf/2601.04498
- type: paper
- summary: Benchmark for text-to-infographic reliability, testing whether generated infographics preserve the source facts they claim to convey.
- reason: Infographic-style pages are one of our candidate approaches and fact-preservation is our core accuracy metric.

## 4. The Visualization JUDGE: Can Multimodal Foundation Models Guide Visualization Design Through Visual Perception?

- url: https://arxiv.org/abs/2410.04280
- type: paper
- summary: Position paper arguing multimodal foundation models are best used as visualization *judges* that critique and suggest improvements, with a taxonomy of what model outputs can guide design.
- reason: The strongest theoretical grounding for our "AI estimates human understanding" evaluator role, including its known failure modes.

## 5. Glanceable Data Visualizations for Older Adults: Establishing Thresholds

- url: https://arxiv.org/pdf/2403.12343
- type: paper
- summary: Empirically establishes how much information different visualization types convey at a glance and how thresholds differ across age groups.
- reason: Our headline human metric is "does a quick glance give a non-expert sufficient understanding" — this gives empirical footing for the glance test.

## 6. Swark — architecture diagrams from code via LLMs

- url: https://github.com/swark-io/swark
- type: repo
- summary: VS Code extension that feeds a codebase to an LLM and emits Mermaid architecture diagrams, language-agnostic because all logic lives in the model.
- reason: Working reference implementation for our "communicate codebase structure" test case using the diagram-language approach.

## 7. Code2UML: Agentic LLMs with context engineering for scalable software visualization

- url: https://arxiv.org/pdf/2605.24453
- type: paper
- summary: Five-agent pipeline (planner/analyzer/diagram/corrector/dependency) that generates UML from real repositories, with correction loops for syntax and fidelity.
- reason: Shows the value of a generate→check→correct loop for diagram fidelity, a pattern our generation harness can adopt.

## 8. Generative UI: a rich, custom, visual interactive user experience for any prompt (Google Research)

- url: https://research.google/blog/generative-ui-a-rich-custom-visual-interactive-user-experience-for-any-prompt/
- type: post
- summary: Google's production system where the model designs and codes a bespoke interactive page per prompt, deployed in Gemini/Search; discusses why walls of text fail users.
- reason: State-of-the-art industrial take on our exact problem (AI→human visual conveyance) and motivates the interactive-HTML end of our approach spectrum.

## 9. SVGenius: Benchmarking LLMs in SVG Understanding, Editing and Generation

- url: https://arxiv.org/html/2506.03139v1
- type: paper
- summary: Benchmark across SVG understanding/editing/generation showing where LLMs' vector-graphics abilities break down as complexity rises.
- reason: Calibrates how much hand-drawn SVG we can trust inside our HTML approaches versus leaning on diagram DSLs.

## 10. LIDA: Automatic Generation of Grammar-Agnostic Visualizations and Infographics using LLMs

- url: https://arxiv.org/abs/2303.02927
- type: paper
- summary: Microsoft's four-stage pipeline (summarize → goal → visgenerator → infographer) treating visualization generation as multi-stage code generation with self-evaluation.
- reason: Canonical staged-pipeline design and its eval metrics (visualization error rate, self-evaluated quality) inform our harness structure.

## 11. Design practices in visualization-driven data exploration for non-expert audiences

- url: https://www.sciencedirect.com/science/article/pii/S1574013725000085
- type: paper
- summary: Survey formalizing the HCI design practices that make data exploration work for non-expert audiences.
- reason: Our target reader is explicitly a non-expert at a glance; this grounds the "estimated human understanding" rubric in documented design practice.

## 12. awesome-generative-ui — curated resource list

- url: https://github.com/narrowin/awesome-generative-ui
- type: repo
- summary: Curated list of systems where LLMs dynamically create, compose, and render UI components.
- reason: Cheap breadth — a maintained map of the generative-UI space to mine for approach ideas beyond our initial set.

## Curation

Curated 2026-08-20. Twelve items; the seven ingested on 2026-07-01 were
re-checked against `literature/**` `url:` fields and confirmed present.

| # | Item | Disposition |
|---|------|-------------|
| 1 | MermaidSeqBench | already in graph → `shbita2025mermaidseqbench` |
| 2 | DiagramEval | already in graph → `liang2025diagrameval` |
| 3 | IGenBench | already in graph → `tang2026igenbench` |
| 4 | The Visualization JUDGE | already in graph → `berger2024visualization` |
| 5 | Glanceable Data Visualizations for Older Adults | already in graph → `while2024glanceable` |
| 6 | Swark | ingested → `literature/repos/swark-io-swark` (rel 2) |
| 7 | Code2UML | ingested → `vaduva2026code2uml` (rel 3, cred 2) |
| 8 | Google Generative UI | already in graph → `googleresearch2025generativeui` |
| 9 | SVGenius | ingested → `chen2025svgenius` (rel 4, cred 4) |
| 10 | LIDA | already in graph → `dibia2023lida` |
| 11 | Design practices in visualization-driven data exploration for non-expert audiences | declined — Elsevier paywall, `HTTP 403` on fetch; no accessible full text, and the framing is already covered by [[literature/papers/while2024glanceable]] for the non-expert-audience angle |
| 12 | awesome-generative-ui | declined — curated link list, no substantive content of its own; the approach set is closed by ADR 0002/0003, so breadth-mining for new approach ideas has no consumer this phase |

**Totals:** ingested 3, declined 2, already in graph 7.

### Notes on the ingests

- **Code2UML** was ingested for its corrector-pass ablation (65.5% → 91.5%
  syntactic validity) and its Relationship Precision metric, not for its
  headline numbers — credibility 2: the validity metric is circular (the
  corrector grades its own work), the "ablation" is a post-hoc re-labelling,
  and the abstract and conclusion disagree on cross-language variance.
- **SVGenius** is the highest-value item of the three: it is the only
  quantitative footing we have for the inline-SVG channel that approach
  10-combined selected in 6/6 cells, and its complexity stratifier (path
  count / control points / complex commands) is directly computable over
  our 60 manifest cells.
- **Swark** was ingested as prior art for the `codebase-structure` test case
  and as the naive contrast to Code2UML's compaction (it truncates the file
  set rather than ranking it). Its `fixMermaidCycles` setting independently
  corroborates that raw LLM diagram-DSL output needs a mechanical repair pass.
