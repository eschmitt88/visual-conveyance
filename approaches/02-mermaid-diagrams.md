---
id: 2
slug: mermaid-diagrams
version: 1
status: active
hypothesis: >
  Diagram-DSL output (Mermaid) is the cheapest visual channel for an LLM
  to produce reliably; structure-heavy material (systems, flows,
  taxonomies) should benefit most, text-heavy nuance least.
---

# Approach 02 — Mermaid diagram suite

The diagrams carry the message; prose is reduced to captions and
connective tissue.

## Method

- Decompose the material into 3–6 diagrammable structures and pick the
  right Mermaid type for each: `flowchart` (processes, architectures),
  `sequenceDiagram` (interactions over time), `classDiagram` (type/module
  relationships), `stateDiagram-v2` (lifecycles), `timeline` (history),
  `quadrantChart` (tradeoffs), `mindmap` (taxonomies), `xychart-beta`
  (simple quantitative series).
- Page = title + one-sentence framing, then one section per diagram:
  a heading, the diagram, and a caption of at most 2 sentences stating
  what to see in it.
- The FIRST diagram is the overview — the whole story in one picture;
  later diagrams zoom into parts. Above the fold: title + overview
  diagram.
- Style diagrams deliberately: meaningful node grouping (subgraphs),
  consistent color classes for categories (define with `classDef`),
  short node labels (≤4 words) with detail pushed to edge labels or
  captions.
- Initialize Mermaid with a neutral theme and `securityLevel:'loose'`
  off; just default init is fine.

## Hard constraints

- Total non-caption prose ≤150 words.
- No hand-written SVG, no charts outside Mermaid, no interactivity
  beyond what Mermaid renders natively.
- Every diagram must actually render — invalid Mermaid syntax is a
  contract failure. Prefer simple constructs over exotic ones.

## Glance zone

Title + the overview diagram, fully visible at 1440×900.
