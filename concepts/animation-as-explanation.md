---
kind: concept
name: "Animation as explanation"
status: seedling
added: "2026-08-11"
sources:
  - "[[literature/repos/3b1b-manim]]"
related_concepts: ["glanceability", "generative-ui"]
related_experiments: []
tags: [animation, sequential-revelation, attention, motion, 3b1b]
---

# Animation as explanation

## Definition

Using motion as a semantic channel rather than decoration: elements enter
a persistent scene one at a time in argument order (sequential
revelation), representation changes are shown as morphs between old and
new forms (transformation over substitution), and the camera — not slide
cuts — moves attention. Motion appears only where it encodes meaning
(3Blue1Brown / manim grammar).

## Why it matters here

Static pages present the finished figure cold; the reader must find their
own path through it. The manim grammar claims the *ordering* of visual
information is itself explanatory content. That is a hypothesis our
harness can test: approach 09 ports the grammar to the static-HTML
contract (inline SVG + stepper-driven CSS/JS animation, no build step,
no video).

Tension with the glance axis: an animation's payoff needs playback time,
and our glance zone is a single 900px-tall screenshot. Approach 09 must
therefore land its final frame as a complete, self-sufficient picture —
the animation is a bonus for readers who press play, not the only path to
the message. If 09 scores well on studied comprehension but poorly on
glance, that split is itself a finding about where motion belongs.

## Connections

- [[glanceability]] — sequential revelation is attention steering over
  time; accent discipline (see [[editorial-design-constraints]]) is
  attention steering in space. Same goal, orthogonal channels.
- [[generative-ui]] — interactivity as the third steering channel; 09's
  stepper is the minimal interactive surface (play/step/scrub only).
- Phase 2 option: actually rendering manim video/GIF artifacts would need
  a contract revision (build step) — recorded in ADR 0002.
