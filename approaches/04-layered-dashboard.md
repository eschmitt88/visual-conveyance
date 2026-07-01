---
id: 4
slug: layered-dashboard
version: 1
status: active
hypothesis: >
  Progressive disclosure — a glance layer, a skim layer, and a detail
  layer on one page — scores well on BOTH glance comprehension and
  accuracy/depth, because no layer has to compromise for another.
---

# Approach 04 — layered dashboard (progressive disclosure)

Three explicit layers of the same story on one page. The reader chooses
their depth; each layer is complete at its own resolution.

## Method

- **Layer 1 — glance (top band, fits above the fold):** headline
  takeaway sentence, 3–5 stat tiles / verdict chips, and one compact
  hero visual (simple SVG or Mermaid) showing the core structure. This
  layer alone must deliver the brief's critical takeaways.
- **Layer 2 — skim (card grid):** one card per major topic. Card =
  icon/title, 2–3 sentence summary, one small visual or key number.
  Reading only titles + bold lead-ins tells the whole story.
- **Layer 3 — detail:** each card expands (native `<details>` or a
  small JS toggle) into full prose, tables, per-topic diagrams, caveats.
  All facts from the source that matter live somewhere in layer 3.
- Persistent affordances: a thin sticky nav with section links; expand
  all / collapse all.
- Visual consistency: one accent palette; stat tiles share geometry;
  caveats get a single consistent "warning" style across layers.

## Hard constraints

- Layer 1 must not exceed one viewport (1440×900).
- Every critical takeaway appears in BOTH layer 1 (compressed) and
  layer 3 (full fidelity) — consistency between layers is part of
  accuracy.
- JS optional and minimal; the page must still work with JS disabled
  (`<details>` fallback).

## Glance zone

Layer 1, by construction.
