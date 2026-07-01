---
id: 5
slug: interactive-explainer
version: 1
status: active
hypothesis: >
  Light interactivity (tabs, toggles, hover reveals, clickable diagram
  nodes) lets one page adapt to the reader's questions — best depth and
  engagement, but glance value depends on the resting (initial) state.
---

# Approach 05 — interactive explainer

A static-host-compatible explorable: vanilla JS interactions that let
the reader interrogate the material instead of scrolling past it.

## Method

- Design the RESTING STATE first: before any interaction the page must
  already show the headline takeaway and core structure (it is also the
  glance zone). Interactivity adds resolution, it never gates the
  basics.
- Pick 2–4 interaction patterns that fit the material:
  - tabs or segmented control to switch between variants/options/views
  - hover/tap tooltips on diagram nodes or terms (definitions, numbers)
  - toggle switches that visibly transform a diagram or comparison
    (before/after, with/without)
  - a slider stepping through stages of a process, updating one shared
    visual
  - click-to-expand nodes in a schematic (SVG onclick)
- Every interactive element must LOOK interactive (affordance: cursor,
  subtle shadow, "click me" hint on first paint) and must degrade
  gracefully: with JS off, all content should still be reachable
  (render hidden panels as stacked sections via `<noscript>` or CSS
  fallback).
- Keep state simple: no frameworks, no persistence, ≤200 lines of JS.

## Hard constraints

- Zero external JS libraries (Mermaid allowed for diagrams; interactions
  are your own vanilla JS).
- No interaction that hides a critical takeaway behind it.
- Must be fully usable via keyboard (tab/enter) — basic a11y.

## Glance zone

The resting state above the fold: headline + core visual + visible
affordances hinting at what can be explored.
