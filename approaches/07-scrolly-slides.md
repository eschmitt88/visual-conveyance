---
id: 7
slug: scrolly-slides
version: 1
status: active
hypothesis: >
  Slide-like sequencing (one idea per screen, strong narrative order)
  trades glance breadth for controlled pacing — expected to win on
  guided understanding of arguments/narratives, lose on random-access
  reference use.
---

# Approach 07 — scrolly slides

A vertically scrolled deck: each viewport-height section is one slide
carrying exactly one idea, in deliberate narrative order.

## Method

- Write the narrative arc first: hook (why care) → context → core idea
  → development/evidence → complication/caveat → resolution → takeaway
  recap. 7–12 slides.
- Each slide: full-viewport section (`min-height:100vh`, CSS
  scroll-snap), a slide title (one line), ONE visual or one big
  statement, and ≤40 words of supporting text. If a slide needs more,
  split it.
- Slide 1 is the cover: the headline takeaway itself (not a teaser) —
  the glance zone must not be an empty title card.
- Final slide: recap of the 3–5 takeaways as a compact list + "where to
  look deeper" pointing at earlier slides.
- Navigation: scroll + a fixed dot/progress rail with slide titles on
  hover; keyboard up/down works via scroll-snap natively.
- Visuals per slide: simple inline SVG, a Mermaid diagram, a huge
  number, or a styled quote — whatever that single idea needs; keep a
  consistent template (title position, visual area, caption line).

## Hard constraints

- One idea per slide, enforced ruthlessly (≤40 words body text).
- No slide may depend on a previous slide's visual being remembered —
  re-show miniatures when referring back.
- JS ≤50 lines (progress rail only); scroll-snap does the rest.

## Glance zone

Slide 1 = cover with the actual takeaway + a visible cue that scrolling
reveals the story (subtle arrow + slide count).
