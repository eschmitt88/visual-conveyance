---
kind: output-contract
version: 1
---

# Shared output contract (all approaches)

Every generator, regardless of approach, must satisfy this contract. The
approach file says HOW to communicate; this file says what a valid
artifact IS.

## Artifact

- Exactly one file: `index.html`. Self-contained: all CSS and JS inline.
- Allowed external resources (CDN only, nothing else):
  - Mermaid: `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js`
  - KaTeX (if math is needed): jsdelivr `katex@0.16` css+js.
- No external images, no fonts beyond system stacks, no fetch() calls,
  no build step. The page must render correctly when served from a
  GitHub Pages subdirectory and when opened as a local file.
- Renders sensibly at 1440×900 desktop and 390px-wide mobile.
- Dark-mode friendly is nice but optional; never unreadable in either.

## Content rules

- The ONLY content source is the test case's `source.md` + `brief.md`.
  Do not import outside knowledge that adds new facts; general knowledge
  may be used to explain, never to extend the fact set. Every claim on
  the page must be traceable to the source.
- Audience: the non-expert described in `brief.md`. Jargon needed for
  precision gets a one-line gloss.
- The above-the-fold region (first 900px at 1440 wide) is the glance
  zone: a reader who sees ONLY that region should leave with the
  brief's core takeaways. Design it deliberately.
- No filler ("In today's fast-paced world…"), no meta-text about the
  page itself, no "AI generated" boilerplate.

## Honesty rules

- Uncertainty, caveats, and negative results in the source are part of
  the message — conveying them counts toward accuracy; hiding them is a
  distortion.
- Numbers are copied exactly; rounding only when the source's precision
  is preserved in spirit and the rounding is marked (≈).

## Footer

- Last line of the page, small print: test case slug, approach slug,
  approach version, generation date. Nothing else about provenance.
