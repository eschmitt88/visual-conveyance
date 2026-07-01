---
kind: paper
title: "Glanceable Data Visualizations for Older Adults: Establishing Thresholds and Examining Disparities Between Age Groups"
authors: ["Zack While", "Tanja Blascheck", "Yujie Gong", "Petra Isenberg", "Ali Sarvghad"]
institutions: ["University of Massachusetts Amherst", "University of Stuttgart", "Smith College", "Université Paris-Saclay / CNRS / Inria"]
year: 2024
venue: CHI '24
peer_reviewed: true
url: https://arxiv.org/abs/2403.12343
code_url: null
citations: null
source: "raw/papers/while2024glanceable.md"
added: "2026-07-01"
relevance: 4
credibility: 4
status: read
related_experiments: []
related_concepts: ["glanceability"]
tags: [glanceability, perception, smartwatch, older-adults, chi, empirical-study, thresholds]
---

# Glanceable Data Visualizations for Older Adults: Establishing Thresholds

## TL;DR

CHI '24 replication study establishing empirical exposure-time thresholds for reading simple comparisons from small-screen visualizations: donut charts are readable in ~200–400 ms, bar charts ~380–700 ms, radial charts 1.1–3.6 s for adults 65+, with the same type ranking but consistently slower times than younger adults — and decline accelerates sharply after age 75.

## Claims

- **Core claim:** "at a glance" is quantifiable — each visualization type × data-size combination has a measurable exposure-time threshold at which a comparison task can be performed, and these thresholds vary by an order of magnitude across chart types (donut ~312 ms vs radial ~2211 ms overall for older adults).
- Chart-type ranking (Donut > Bar > Radial) is stable across age groups; *speed* degrades with age while relative perceptual structure is preserved.
- Data-point count is a first-order glanceability factor: thresholds grow with 7→12→24 points, and age gaps widen with complexity (Radial 24: 2022 ms younger vs 3577 ms older).
- "Older adult" is not one population: 65–74 performs near younger-adult level in 8/9 conditions; ≥75 shows strong declines — decline is non-linear.
- Preference tracks performance: donut is both fastest and most preferred/most confidence-inspiring for older adults (79% rank-1 preference at larger sizes; radial 0% confidence at all sizes).

## Methods

- Conceptual replication of Blascheck et al. with 24 adults aged 65–96 (M=73) on a Sony SmartWatch 3 (320×320, 1.6").
- 2AFC task: two dot-marked elements, pick the larger; 3 chart types (bar, donut, radial) × 3 data sizes (7/12/24 points) = 9 conditions.
- Adaptive staircase on exposure time (+100 ms wrong / −300 ms after 3 correct, ~63% expected accuracy), until 15 reversals or 198 trials; thresholds via BCa-bootstrapped 95% CIs with Bonferroni correction.

## Results

- Older-adult thresholds (ms): Donut 218/349/414; Bar 383/574/695; Radial 1135/1599/3577 (for 7/12/24 points). Younger: Donut 167/263/382; Bar 267/411/544; Radial 656/1045/2022.
- Strong evidence of age differences in 5/9 conditions (all Bar, Radial 12/24); donut most age-robust (insufficient evidence at 7 and 24 points).
- 7 of 22 older participants gave up entirely on Radial 24; old-old accuracy there fell below the staircase's expected 63% (56%) — a chart type can be effectively unusable at a glance.
- Self-reported strategies: donut works via holistic/peripheral color-patch perception (13/24), the most "glance-like" mechanism; radial forces serial arc-tracing.

## Critique / open questions

- Small (n=24), highly educated sample; lab setting; single smartwatch device — thresholds are anchors, not universal constants.
- Task is a minimal comparison (which of two marked elements is larger) — far simpler than "did the reader get the main message of an infographic," which is our actual glance test. Thresholds here are lower bounds for real comprehension.
- Smartwatch-scale stimuli; our GitHub-Pages presentations are desktop-scale. Relative type rankings likely transfer; absolute ms values do not.
- Doesn't test text vs visualization or mixed layouts.

## Trust signals

- **Credibility:** 4 — peer-reviewed at CHI '24, strong vis/HCI groups (Isenberg, Blascheck), preregistered with OSF supplementary materials; no code but full experimental provenance; replication design adds confidence.

## So what for visual-conveyance

- Gives our **glance-comprehension axis** its empirical footing: glanceability is a measurable threshold (exposure time × task success), not a vibe. Our eval rubric can define glance comprehension operationally, e.g. "what would a reader extract in a ~5-second view?" (their smartwatch-session framing) rather than an unanchored "is this clear?".
- Concrete design priors for our approaches: encodings readable via holistic/peripheral perception (donut-like proportion patches, position/length) beat encodings requiring serial tracing (radial/arc-following) by ~7x in exposure time; element count is a budget — beyond ~12 comparable elements, glanceability collapses.
- The audience-heterogeneity result generalizes: "non-expert" is not one population either. Our evaluator prompt personas should specify the reader (and possibly test a "low-bandwidth reader" persona), since thresholds shift substantially across sub-populations.
- Judge-design implication: an AI judge estimating glance comprehension should penalize serial-scan-demanding layouts and high element counts explicitly — these are the empirically validated glanceability killers.

## Follow-up

- **Relevance:** 4 — seeds the glanceability concept with the only quantitative thresholds we have; the task gap (comparison vs message comprehension) keeps it from a 5.
- Encode "element-count budget" and "holistic vs serial encoding" as scored dimensions in the glance-axis rubric.
- Look up the original Blascheck et al. thresholds paper if we need younger-adult baselines in detail.
