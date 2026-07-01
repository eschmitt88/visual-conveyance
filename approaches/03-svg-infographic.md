---
id: 3
slug: svg-infographic
version: 1
status: active
hypothesis: >
  A poster-style infographic (big numbers, icons, strong visual
  hierarchy, hand-authored SVG) maximizes glance comprehension, at some
  risk to accuracy and depth as content is compressed.
---

# Approach 03 — SVG infographic poster

One continuous scrollable poster in the style of a good conference
infographic: the page is a designed composition, not a document.

## Method

- Establish a visual identity first: 2 accent colors + neutrals, one
  display size for hero numbers, consistent icon stroke style. Declare
  CSS variables and stick to them.
- Lead with a hero band: the single most important takeaway as a short
  headline + the most important number/relationship rendered huge.
- Then 4–7 poster sections, each ONE idea expressed visually:
  - big-number stat tiles with one-line labels
  - hand-authored inline SVG: simple icons, flow arrows, proportional
    bars/donuts, small schematic drawings
  - comparison strips (side-by-side mini-panels)
- Proportions must be honest: if a bar is 2× longer, the quantity is 2×
  larger. If data can't be drawn honestly at this size, use a number
  instead of a shape.
- Keep SVG simple and hand-checkable — rects, circles, paths with few
  points, text elements. No generated filter/gradient soup.
- Prose budget: labels, one-liners, and at most one 40-word caveat box.
  Total words on page ≤250.

## Hard constraints

- No Mermaid, no external libraries at all (pure HTML+CSS+SVG, zero JS
  or trivial JS only for nothing essential).
- No walls of text; if a section needs a paragraph, it's the wrong
  approach for that section — compress or cut (but never cut caveats
  that change the message; render them as a visible warning chip).

## Glance zone

Hero band + first stat row. A 10-second viewer should get the headline
takeaway and the one killer number.
