---
id: 8
slug: editorial-diagrams
version: 1
status: active
source_repo: https://github.com/cathrynlavery/diagram-design
hypothesis: >
  Free-form SVG failed in the baseline (7.38, below prose) not because
  hand-authored visuals are weak but because they were unconstrained.
  A tight editorial design system (single accent, 4px grid, density
  cap, deletion-first) — the diagram-design discipline — recovers
  professional quality and beats both 03-svg-infographic and
  02-mermaid-diagrams on glance without losing accuracy.
---

# Approach 08 — editorial diagram suite

Hand-authored inline-SVG diagrams under the diagram-design editorial
discipline (cathrynlavery/diagram-design). Like 02 the diagrams carry the
message; like 03 the layout is free-form SVG — but every visual choice is
governed by a fixed design system. The craft is in what you delete.

## Method

- **Pick 2–4 diagram types** that fit the material's structure, from the
  diagram-design taxonomy: architecture (components + connections),
  flowchart (decision logic), sequence (messages over time), state
  machine, swimlane, timeline, quadrant / consultant 2×2, layer stack,
  pyramid/funnel, nested containment, tree, loop/flywheel, radar, bar,
  line, scatter. One diagram per section, one idea per diagram. Before
  drawing each, apply the repo's own test: *would the reader learn more
  from this than from a well-written paragraph?* Lists → a table.
  A single labeled box → a sentence.
- **Design tokens, declared once as CSS variables and never bypassed:**
  - `--paper` (page background), `--ink` (primary text/strokes),
    `--muted` (secondary text), `--accent` (ONE accent color),
    `--hairline` (1px borders). Pick an editorial pairing (e.g.
    warm off-white paper, near-black ink, one saturated accent).
  - Fonts from system stacks only (per contract): a serif stack for the
    title and italic editorial callouts, the system sans for node names,
    the system mono for technical sublabels ONLY (ports, paths, field
    types, exact figures) — mono is a semantic marker, not an aesthetic.
- **The accent rule:** the accent color appears on at most 1–2 focal
  elements per diagram — the thing the reader should see first. Never on
  decoration, never on more than 2 nodes.
- **The 4px grid:** every SVG coordinate, width, height, and gap is
  divisible by 4. This is mechanical and non-negotiable — it is the
  single biggest de-slop constraint.
- **Restraint set:** 1px hairline strokes, no drop shadows, no
  gradients, border-radius ≤10px, target density ~4/10 — if a diagram
  feels 6/10 full, delete nodes until it doesn't. Short node names
  (≤3 words) with detail in mono sublabels beneath.
- **Editorial annotations:** for the 1–2 places a caveat or insight
  matters, use the annotation primitive — an italic serif margin note
  with a dashed curved leader line into the diagram. Caveats and
  negative results from the source get this treatment (visible, not
  buried).
- **Page skeleton:** title + one-sentence standfirst, then diagram
  sections (heading, diagram, ≤2-sentence caption). First diagram is
  the overview — the whole story in one picture; later diagrams zoom in.
- Non-caption prose budget ≤150 words, matching 02 so the 02 vs 03 vs 08
  comparison isolates the visual channel.

## Hard constraints

- Pure HTML+CSS+inline SVG. No Mermaid, no JS, no external libraries,
  no external images or fonts.
- Every rendered number/label must be checkable against the source;
  proportions drawn to scale or replaced by the number.
- The 4px grid and single-accent rules are contract-level: violating
  them is a spec failure even if the page "looks fine".

## Glance zone

Title + standfirst + the overview diagram, fully visible at 1440×900,
with the accent marking the single most important element on the page.
