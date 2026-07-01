---
source_url: https://arxiv.org/html/2403.12343
abs_url: https://arxiv.org/abs/2403.12343
fetched: 2026-07-01
title: "Glanceable Data Visualizations for Older Adults: Establishing Thresholds and Examining Disparities Between Age Groups"
authors: ["Zack While", "Tanja Blascheck", "Yujie Gong", "Petra Isenberg", "Ali Sarvghad"]
format: html-md
---

# Glanceable Data Visualizations for Older Adults: Establishing Thresholds and Examining Disparities Between Age Groups

**Authors:** Zack While (UMass Amherst), Tanja Blascheck (University of Stuttgart), Yujie Gong (Smith College), Petra Isenberg (Université Paris-Saclay, CNRS, Inria, LIS), Ali Sarvghad (UMass Amherst)
**Venue:** CHI '24 (ACM Conference on Human Factors in Computing Systems), May 2024. 17 pages. Supplementary materials on OSF. CC BY 4.0.
**ArXiv ID:** 2403.12343 (March 2024)

## Abstract

This replication study examines smartwatch visualizations with participants aged 65 and older. The research replicates prior work by Blascheck et al. investigating how visualization type and data point quantity influence perception speed. While older adults demonstrated the same performance ranking across visualization types as younger participants (Donut fastest, followed by Bar, then Radial), they exhibited consistently slower response times. The study identified particularly pronounced differences for participants aged 75 and older. The authors provide empirical thresholds for older adult performance and discuss methodological considerations for research with this population.

## 1. Introduction

- Glanceable visualizations: concise graphical information designed for rapid insight without extensive analysis; most smartwatch interactions are viewing sessions under five seconds.
- Aging affects perception/cognition: presbyopia affects nearly all adults 65+; visual acuity declines after 50; memory, attention, processing speed may diminish.
- Conceptual replication of Blascheck et al.'s perceptual study: time thresholds across three visualization designs (Bar, Donut, Radial) and three data sizes (7, 12, 24 data points) on smartwatch displays. Original study: ages 19–64; this study: 65+.
- Headline: older adults fastest with Donut (312 ms overall), then Bar (485 ms), then Radial (2211 ms) — same ranking as younger adults but consistently slower in all nine conditions; strong evidence of differences in 5/9 conditions, weak in 2/9. Younger vs old-old (≥75) gaps widen substantially; younger vs young-old (65–74) show minimal differences in 8/9 conditions.

## 2. Motivation

- Older adult population → 16% globally by 2050, 24% by 2100; older adults outnumber children in the US by 2060.
- Conceptual replication tests generalizability; original study chosen for fundamental smartwatch perception focus, basic comparison tasks, multiple types/sizes, and directly comparable younger-participant data.

## 3. Related work (selected)

- Bar/radial-bar watch faces outperform text progress displays; bar charts more accurate but radial aesthetically preferred.
- Neshati et al.: condensed sparklines improve accuracy on smartwatches.
- Le et al.: for older adults, bar charts familiar but high cognitive load; wellness polygons complex; partitioned donuts adequate for trends but effortful. Multiple visual cues can impair older adults' processing.
- Cajamarca et al.: older Chilean adults more accurate WITHOUT progress indicators (distraction); higher tech proficiency → better accuracy/speed.
- Khakurel et al.: screen size and font size critical usability factors for older adults on smartwatches.

## 4. Study design

- **Participants:** 24 older adults (19 F, 4 M, 1 NA), ages 65–96 (M=73, SD=8); 22 with ≥bachelor's; 13/24 no prior visualization familiarity. Chart familiarity (1–5): Bar 4.1, Donut 3.2, Radial 1.5. Original study: M age 35.0 (SD 13.0).
- **Apparatus:** Sony SmartWatch 3, 320×320 px, 1.6-inch; stand at ~28 cm horizontal / 20 cm vertical (adjustable after pilots, M=25.2 cm).
- **Task:** two-alternative forced choice — two black dots mark elements; pick which marks the larger value (tallest bar / largest donut region / most complete radial circle). 396 stimulus images from original authors.
- **Staircase:** weighted 3-down-1-up; +100 ms after incorrect, −300 ms after three consecutive correct → ~63% expected accuracy (original study miscalculated as ~91%). Condition ends at 15th reversal or 198th trial. 9 conditions = 3 chart types × 3 data sizes.
- Practice trials with initial exposures 1700–5100 ms. Modifications during study: Radial-24 skippable (7 of 22 quit it); keyboard replaced with two mechanical keys.

## 5. Results

### 5.1 Time thresholds (younger from original study vs older, ms)

| Condition | Younger | Older | Difference |
|-----------|---------|-------|------------|
| Donut 7 | 167 | 218 | 51 |
| Donut 12 | 263 | 349 | 86 |
| Donut 24 | 382 | 414 | 32 |
| Bar 7 | 267 | 383 | 116 |
| Bar 12 | 411 | 574 | 163 |
| Bar 24 | 544 | 695 | 151 |
| Radial 7 | 656 | 1135 | 479 |
| Radial 12 | 1045 | 1599 | 554 |
| Radial 24 | 2022 | 3577 | 1555 |

- Overall older adult thresholds: Donut 312 ms, Bar 485 ms, Radial 2211 ms.
- Evidence of younger/older differences (95% BCa bootstrap CIs, Bonferroni, interval-overlap analysis): strong for Bar 7/12/24 and Radial 12/24; weak for Donut 12 and Radial 7; insufficient for Donut 7 and Donut 24.
- Young-old (65–74) vs old-old (≥75): strong differences for Bar all sizes, Donut 24, Radial 24; weak Donut 7/12; insufficient Radial 7/12.
- Younger vs young-old: minimal differences in 8/9 conditions. Younger vs old-old: strong differences in nearly all conditions. Decline appears non-linear, accelerating with advanced age.

### 5.2 Accuracy (staircase expectation ~63%)

| Condition | Young-Old | Old-Old |
|-----------|-----------|---------|
| Bar 7 | 77% | 75% |
| Bar 12 | 71% | 72% |
| Bar 24 | 69% | 68% |
| Donut 7 | 79% | 77% |
| Donut 12 | 77% | 74% |
| Donut 24 | 74% | 70% |
| Radial 7 | 68% | 68% |
| Radial 12 | 64% | 63% |
| Radial 24 | 63% | 56% |

### 5.3 Strategies (self-reported)

- Bar: one-target estimation (8/24), two-target comparison (7/24), overall distribution shape (6/24), local shape (5/24).
- Donut: holistic single view / peripheral scan for larger color patch (13/24), one-element focus (8/24), dot-location comparison (6/24).
- Radial: inner-bar focus (12/24), cluster comparison (4/24), arc-following (2/24).

### 5.4 Preference and confidence (rank 1 = best)

- Older adults' preference: size 7 — Donut 63%, Bar 38%, Radial 0%; sizes 12 and 24 — Donut 79%, Bar 13%, Radial 8%.
- Confidence: size 7 — Donut 58%, Bar 42%; size 12 — Donut 88%; size 24 — Donut 83%; Radial 0% at all sizes.
- Younger adults (original): Bar highest at size 7 (56%); Donut highest at 12 (56%) and 24 (67%).

### 5.5 Smartwatch ownership

6/24 own smartwatches; 5 of 6 owners prefer numerical data over visualization. Non-ownership reasons: no need (11/18), privacy (7/18), cost (6/18). Most-wanted data: blood pressure (17/24).

## 6. Discussion

- **Similar trends, slower times:** basic pattern recognition appears stable with age; speed declines. Candidate explanations: visual-search decline (finding small dot markers), working-memory decline (unmeasured). Gaps widen with data size (except Donut 24).
- **Practical significance is contextual:** in dynamic contexts (walking, health tracking during exercise) extended glance duration matters (fall risk); sitting indoors, less so.
- **Defining "old":** 65–74 ≈ younger-adult performance; ≥75 accelerated decline — treat age as nuanced, not binary; a threshold may exist where physiological impacts intensify.
- **Methodological flexibility:** heterogeneity demands adaptive protocols (skippable conditions, ergonomic inputs).

### Design implications

1. Prioritize Donut over Radial for quick comparisons among older adults.
2. Manage visual complexity: 7–12 data points, not 24.
3. Accommodate variable capability (young-old vs old-old): scale complexity or provide simplified alternatives.
4. Optimize for visual search: clearer/larger target marking.
5. Health-context designs deserve particular attention.
6. Preference aligns with performance for Donut (mutual reinforcement).

## 7. Limitations

n=24; highly educated sample; single device (Sony SmartWatch 3); lab context; working memory unmeasured; 7 participants skipped Radial 24 (results from 17/24); moderate tech proficiency (M=2.6/5).

## 8. Conclusion

Same visualization-type ranking as younger adults (Donut > Bar > Radial) with consistently slower thresholds; declines pronounced and possibly accelerating after 75. Contributions: empirical time thresholds for older adults, evidence for age's influence on graphical perception, methodological guidance for research with older populations.
