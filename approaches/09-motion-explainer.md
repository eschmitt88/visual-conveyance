---
id: 9
slug: motion-explainer
version: 1
status: active
source_repo: https://github.com/3b1b/manim
hypothesis: >
  The manim/3Blue1Brown grammar — sequential revelation of one
  persistent scene, morphing between representations, motion only where
  it encodes meaning — ported to static HTML, produces the best studied
  comprehension of any approach; glance score depends entirely on the
  final frame standing alone as a static picture.
---

# Approach 09 — motion explainer (manim grammar, static contract)

An animated build-up of ONE persistent diagram, in the explanatory
grammar of 3b1b/manim — but rendered as inline SVG animated by vanilla
JS/CSS, because the contract allows no build step and no video. Manim is
the design language here, not the toolchain.

## Method

- **One scene, not slides.** A single inline-SVG canvas holds the entire
  explanation. Elements are positioned where they will finally live;
  the animation reveals and connects them in argument order. No carousel,
  no separate figures.
- **Script the build as 4–8 steps.** Each step = one beat of the
  argument: an element (or group) is drawn/faded/slid in, an existing
  element transforms, or the viewport pans/zooms to a region (animate the
  SVG `viewBox` or a group transform). Write the step list before writing
  any code — it is the storyboard.
- **Transformation over substitution.** When the material changes
  representation (table → chart, before → after, plan → outcome), morph
  the old form into the new one (animate position/size/opacity of the
  same elements) instead of swapping pictures. The morph visually asserts
  "these are the same thing".
- **Motion is semantic.** Nothing moves for decoration. If a step's
  motion doesn't encode a fact or relation from the source, cut it.
  Easing subtle, durations 400–900ms, one thing moving at a time.
- **Synchronized captions.** A fixed one-line caption region under the
  scene updates each step with ≤20 words stating what just appeared and
  why it matters — the narration track. The step list doubles as a
  progress dots row.
- **First paint = final frame.** The page loads with the build COMPLETE:
  the finished scene plus captions' final state, with a prominent
  "▶ replay the build-up" control. Playing resets the scene to empty and
  steps through. (Evaluators and skimmers see a finished picture; the
  animation is the deep-reading path, never a gate.)
- **Controls:** play/pause, step forward/back, and the progress dots
  jump to a step. Keyboard: space/arrows. `prefers-reduced-motion`:
  steps swap instantly with no tweening.
- **Aesthetic:** manim-style austere — dark canvas (near-black, e.g.
  #111–#1a1a2e), light strokes/text, 3–4 saturated hues each bound to
  one meaning for the whole page (bind them in a small legend). KaTeX
  from the allowed CDN if the material is mathematical; otherwise none.
- Prose outside the scene: title + one-sentence framing + captions only.

## Hard constraints

- No video, no GIF, no image files, no animation libraries — vanilla
  JS (≤300 lines) + CSS transitions/Web Animations API on inline SVG.
- The final frame must satisfy the contract's glance rules ON ITS OWN:
  a reader who never presses play gets the core takeaways.
- Every caption fact traceable to the source; the step order must follow
  the material's logic, not theatrical suspense — caveats appear in the
  step where their subject appears, not at the end.
- All content reachable with JS off: scene renders in final state,
  captions render as a visible ordered list.

## Glance zone

The completed scene + final caption + replay affordance at 1440×900.
It should read as a strong static diagram that happens to be playable.
