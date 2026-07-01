---
source_url: https://arxiv.org/html/2511.14967
abs_url: https://arxiv.org/abs/2511.14967
fetched: 2026-07-01
title: "MermaidSeqBench: An Evaluation Benchmark for NL-to-Mermaid Sequence Diagram Generation"
authors: ["Basel Shbita", "Farhan Ahmed", "Chad DeLuca"]
format: html-md
---

# MermaidSeqBench: An Evaluation Benchmark for NL-to-Mermaid Sequence Diagram Generation

**Authors:** Basel Shbita, Farhan Ahmed, Chad DeLuca
**Affiliation:** IBM Research, San Jose, CA, USA
**ArXiv ID:** 2511.14967v2 (v1: 2025-11-18, v2: 2026-04-25)
**Subjects:** cs.SE, cs.AI, cs.LG

## Abstract

The paper introduces MermaidSeqBench, addressing a gap in evaluating large language models' ability to generate Mermaid sequence diagrams from natural language descriptions. The benchmark comprises 132 samples developed through human verification, LLM-based augmentation, and rule-based expansion. An LLM-as-a-Judge methodology assesses generation across six metrics: syntax correctness, activation handling, error handling, and practical usability. Evaluations on state-of-the-art models reveal significant capability gaps, establishing correctness standards for production software engineering deployment.

## 1. Introduction

LLMs have demonstrated strong capabilities in code generation, documentation, and structured diagram creation. Sequence diagrams represent critical software engineering artifacts showing how objects, components, and processes interact over time. While existing work shows LLMs can generate Mermaid sequence diagrams, "systematic evaluations for assessing an LLM's correctness in producing sequence diagrams remains largely underdeveloped."

The authors emphasize that mission-critical applications require flawless syntax and logic, making evaluation essential. The paper addresses this by introducing MermaidSeqBench — a reproducible, scalable evaluation framework with both a dataset and systematic assessment methodology using LLM-as-a-Judge evaluation.

**Key motivation:** Lack of existing benchmarks hinders reliable LLM deployment in production environments for diagram generation tasks.

## 2. Related Work

Prior research on LLM-generated diagrams focuses primarily on PlantUML representations, with limited work on Mermaid syntax specifically. Existing evaluations employ:

- Simple compliance and visualization checks (Saxena et al., Guernsey)
- Statistical validation methods for UML class diagrams (Rouabhia & Hadjadj)
- Statistical methods for PlantUML sequence diagrams (Ferrari et al.)
- LLM-as-a-Judge approaches for NL-to-PlantUML tasks (Ahmed et al.)

The authors note that "no formal benchmark or even public dataset exists for evaluating an LLM's capabilities on producing Mermaid sequence diagrams," positioning their work as the first systematic benchmark in this specific space.

## 3. Methodology

### 3.1 Dataset Construction

The 132-sample dataset was constructed through a three-stage hybrid pipeline:

#### 3.1.1 Initial Dataset Seeds

Ten Mermaid sequence diagrams were manually crafted by subject matter experts (SMEs) based on natural language descriptions. Each diagram underwent verification for syntax correctness, semantic plausibility, and completeness, establishing a high-quality foundation.

#### 3.1.2 Synthetic Expansion

The team employed Scalable Synthetic Data Generation (SDG) using Mistral-Large-Instruct (123B) as the primary generator. The process:

- Leveraged in-context examples of valid Mermaid sequence diagrams
- Generated additional diagram flows while maintaining syntactic fidelity
- Selected 30 samples for dual verification:
  - Manual rendering via Mermaid Live Editor for syntax verification
  - SME verification for completeness and constraint adherence

#### 3.1.3 Rule-Based Variation Augmentation

Deterministic augmentation rules created approximately four-fold coverage expansion through:

- Programmatic detection and reordering of conditional constructs (alt, else, end blocks)
- Support for nested alternatives while preserving logical meaning
- Normalization of participant identifiers into canonical forms
- Consistent propagation of substitutions across declarations and references

#### 3.1.4 Natural Language Descriptions

Each diagram paired with structured NL descriptions containing:
- **Purpose:** Overall intent
- **Main Components:** Participants and roles
- **Interactions:** Ordered messages and control-flow constructs

This yielded 132 NL-Mermaid pairs grounded in clear, unambiguous documentation.

### 3.2 Evaluation Method

#### 3.2.1 Inference on Input Prompts

LLM evaluation used a fixed schema containing:
- Task directive and general guidelines
- Mermaid syntax rules with examples
- Purpose, main components, and interactions specification

All outputs generated using greedy decoding (temperature = 0) with 1,024 token maximum for reproducibility.

#### 3.2.2 LLM-as-a-Judge Assessments

Judge LLMs assess generated outputs across six dimensions on a 0.0–1.0 scale:

1. **Syntax:** Proper MermaidJS syntax, participant declarations, balanced activation/deactivation, correct alt/else/end block closure
2. **Mermaid Only:** Strict containment of Mermaid code without extraneous explanation, wrapped in valid Markdown blocks
3. **Logic:** Completeness of request-response pairs, alternate flow representation, nested branch handling
4. **Completeness:** Coverage of all participants, request/response pairs, decision points, and described behaviors
5. **Activation Handling:** Proper use of activate/deactivate keywords, appropriate participant deactivation, absence of unnecessary deactivation statements
6. **Error & Status Tracking:** Explicit status updates, clear separation of success/failure flows, effective error-case representation, state tracking of key entities

Judge prompts follow standardized structure, present generated and reference diagrams without requiring verbatim match, and output numerical scores with brief explanations.

## 4. Experiments and Discussion

### 4.1 Experimental Setup

Two evaluation categories:

**1. Cross-Family and Cross-Scale Comparisons:**
- Three model families at similar sizes: Llama-3.1-8B-Instruct, Qwen-2.5-7B-Instruct, Granite-3.3-8B-Instruct
- Smaller variants from same families: Llama-3.2-1B-Instruct, Qwen-2.5-1.5B-Instruct, Granite-3.3-2B-Instruct

**2. Intra-Family Scaling Ablation:**
- Qwen-2.5 instruction-tuned models at seven sizes: 0.5B, 1.5B, 3B, 7B, 14B, 32B, 72B parameters
- Controls for architectural differences, isolates scaling effects

**Judge Models:** DeepSeek-V3 (671B), GPT-OSS (120B)

### 4.2 Results

#### 4.2.1 Cross-Family and Cross-Scale Comparisons

**Table 1 (DeepSeek-V3 Judge Results):**

| Model | Syntax | Mermaid Only | Logic | Completeness | Activation | Error & Status |
|-------|--------|--------------|-------|--------------|------------|-----------------|
| Llama-3.1-8B | 92.01% | 96.36% | 87.35% | 89.43% | 79.17% | 81.82% |
| Qwen-2.5-7B | 91.29% | 95.98% | 87.23% | 88.90% | 79.55% | 81.70% |
| Granite-3.3-8B | 86.97% | 94.13% | 83.03% | 83.75% | 74.13% | 76.97% |
| Llama-3.2-1B | 68.98% | 60.68% | 52.27% | 60.57% | 39.85% | 52.35% |
| Qwen-2.5-1.5B | 61.59% | 64.55% | 47.31% | 51.61% | 46.06% | 47.77% |
| Granite-3.3-2B | 75.27% | 90.98% | 70.23% | 74.55% | 63.71% | 71.86% |

**Table 1 (GPT-OSS Judge Results):**

| Model | Syntax | Mermaid Only | Logic | Completeness | Activation | Error & Status |
|-------|--------|--------------|-------|--------------|------------|-----------------|
| Llama-3.1-8B | 68.89% | 93.85% | 67.71% | 77.50% | 57.99% | 74.90% |
| Qwen-2.5-7B | 85.97% | 97.05% | 70.56% | 77.37% | 64.04% | 69.81% |
| Granite-3.3-8B | 65.15% | 88.35% | 58.90% | 65.08% | 47.08% | 63.24% |
| Llama-3.2-1B | 46.15% | 46.23% | 18.86% | 25.92% | 17.29% | 24.14% |
| Qwen-2.5-1.5B | 56.07% | 85.22% | 30.49% | 40.26% | 33.99% | 41.53% |
| Granite-3.3-2B | 39.60% | 78.59% | 34.11% | 46.50% | 29.01% | 53.97% |

**Key Findings:**

- Consistent scaling effects across families: larger models outperform smaller variants
- Llama and Qwen achieve highest scores across most criteria
- Granite exhibits strong syntactic/Mermaid-only performance but lags on activation handling
- DeepSeek-V3 assigns higher, more consistent scores; GPT-OSS is stricter, particularly for smaller models
- Cross-judge variability highlights importance of multiple evaluators

#### 4.2.2 Intra-Family Scaling Ablation Analysis

**Table 2 (DeepSeek-V3 Judge Results):**

| Model | Syntax | Mermaid Only | Logic | Completeness | Activation | Error & Status |
|-------|--------|--------------|-------|--------------|------------|-----------------|
| Qwen-2.5-0.5B | 58.90% | 77.12% | 36.93% | 44.39% | 26.52% | 38.07% |
| Qwen-2.5-1.5B | 61.59% | 64.55% | 47.31% | 51.61% | 46.06% | 47.77% |
| Qwen-2.5-3B | 62.20% | 69.39% | 60.57% | 63.64% | 55.91% | 58.94% |
| Qwen-2.5-7B | 91.29% | 95.98% | 87.23% | 88.90% | 79.55% | 81.70% |
| Qwen-2.5-14B | 83.79% | 88.94% | 84.77% | 85.19% | 72.31% | 70.55% |
| Qwen-2.5-32B | 87.92% | 89.39% | 86.29% | 86.82% | 75.21% | 72.16% |
| Qwen-2.5-72B | 88.56% | 90.00% | 86.33% | 86.36% | 75.91% | 72.46% |

**Table 2 (GPT-OSS Judge Results):**

| Model | Syntax | Mermaid Only | Logic | Completeness | Activation | Error & Status |
|-------|--------|--------------|-------|--------------|------------|-----------------|
| Qwen-2.5-0.5B | 48.95% | 65.45% | 13.91% | 18.41% | 13.85% | 15.90% |
| Qwen-2.5-1.5B | 56.07% | 85.22% | 30.49% | 40.26% | 33.99% | 41.53% |
| Qwen-2.5-3B | 66.80% | 92.67% | 46.86% | 55.35% | 49.92% | 58.87% |
| Qwen-2.5-7B | 85.97% | 97.05% | 70.56% | 77.37% | 64.04% | 69.81% |
| Qwen-2.5-14B | 80.87% | 97.50% | 76.65% | 80.06% | 63.06% | 70.97% |
| Qwen-2.5-32B | 90.32% | 97.73% | 78.72% | 83.23% | 80.20% | 70.55% |
| Qwen-2.5-72B | 87.14% | 97.95% | 83.38% | 87.69% | 80.85% | 70.66% |

**Key Findings:**

- Clear, consistent improvement across all six criteria as model scale increases
- Most pronounced gains from 3B to 14B variants, particularly in logic, completeness, and activation handling
- Larger variants (32B/72B) approach saturation on syntax/Mermaid-only criteria
- Incremental improvements continue on semantically demanding dimensions
- Trends remain stable across both judge models
- GPT-OSS exhibits stricter scoring at smaller scales
- Demonstrates MermaidSeqBench sensitivity to fine-grained performance differences

## 5. Future Work

1. Extend benchmark beyond Mermaid sequence diagrams to flowcharts, Gantt charts, class diagrams, user journey diagrams
2. Expand evaluation categories to determine whether capability gaps are more prominent across additional criteria
3. Strengthen benchmark for systematically probing LLM limits in structured diagram generation for reliable production deployment

## 6. Conclusion

MermaidSeqBench establishes the first systematic benchmark for evaluating LLM capabilities in generating precise, structured, logically consistent Mermaid sequence diagrams. The hybrid construction combining human verification with rule-based and LLM-driven expansion enables assessment of critical metrics including syntax, logic, completeness, activation handling, and error/status tracking. Evaluations reveal significant performance gaps that hinder operational reliability, underscoring the necessity for specialized benchmarks to identify model weaknesses and establish correctness standards for real-world software engineering workflows.

## Limitations

- **Limited seed set:** Ten manually crafted diagrams may introduce SME inductive bias
- **Mermaid-specific:** Findings limited to Mermaid syntax; generalization to PlantUML or other formats uncertain
- **Evaluation criteria scope:** Six dimensions explored; other categories remain unexplored
- **LLM-as-judge limitations:** Potential biases and inconsistencies in ill-defined settings with multiple valid solutions

## Additional Resources

- **Code Repository:** https://github.com/IBM/MermaidSeqBench-Eval
- **Dataset:** https://huggingface.co/datasets/ibm-research/MermaidSeqBench
- **License:** CC BY 4.0
