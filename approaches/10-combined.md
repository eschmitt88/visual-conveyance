---
id: 10
slug: combined
version: 1
status: active
hypothesis: >
  Given the full toolbox with no prescribed method — only the output
  contract and a mechanical layout-QA gate — the generator's own
  judgment about which channels fit the material matches or beats the
  best single prescribed approach. If it instead underperforms, method
  prescription (not tool availability) is where the earlier approaches'
  value lives.
---

# Approach 10 — combined (free choice of tools)

Communicate the material as well as you can. No method is prescribed:
you choose the structure, the media mix, and the length. Everything in
the output contract still binds.

## Available tools (a menu, not a checklist)

Use any, all, or none of:

- **Prose** — plain, linear text.
- **Mermaid diagrams** (the contract's allowed CDN).
- **Hand-authored inline SVG** — diagrams, charts, schematics.
- **KaTeX** (the contract's allowed CDN) if the material is mathematical.
- **CSS layout** — sections, grids, cards, whatever serves the reading.
- **Vanilla JS** — interactivity and/or animation, at your discretion.

Pick what the material needs. Combining channels is allowed; so is
using a single one.

## Required self-check (mechanical QA, not design guidance)

Before finishing, render-check your page:

```sh
PLAYWRIGHT_BROWSERS_PATH=/mnt/projects/.playwright-browsers \
  uv run python tools/layout_check.py <path-to-your-index.html>
```

It reports overlapping SVG text, labels clipped at an SVG edge, type
below 9px, and horizontal page overflow at desktop (1440) and mobile
(390) widths. Fix every ERROR and re-run until the page passes; treat
warnings as strong hints. A page that cannot pass does not ship.

## Glance zone

Per the contract: the above-the-fold region must carry the core
takeaways on its own. How you achieve that is up to you.
