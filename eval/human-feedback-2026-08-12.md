---
kind: human-feedback
date: 2026-08-12
scope: qualitative, cross-approach (01-09, both runs)
---

# Human feedback — approaches 01–09 (2026-08-12)

Verbatim-in-spirit notes from the project owner after reviewing the
matrix. This is the authoritative human signal the AI evals are checked
against; approach 10 (ADR 0003) is designed from it.

1. **Progressive disclosure of 09 works.** The staged build-up "is more
   natural when coming into a topic fresh." (Note: the AI eval could not
   see this channel at all — screenshot-only. Human and AI signal
   genuinely diverge here.)
2. **Numeric stat cards fail.** "They try to convey a number, but the
   user has no idea what this number means unless they already are
   totally familiar with the topic." Numbers need comparison,
   denominator, or consequence attached — a big number alone is not
   information.
3. **Plain text has a real advantage: linearity.** It matches how a
   reader actually consumes. "Too many tabs or dropdowns actually makes
   things quite intimidating."
4. **Interactivity is often forced.** Hover/highlight effects that don't
   change what the reader knows are pointless.
5. **Diagrams help but layout breaks.** "We often get overlapping or
   poorly laid out elements" — matches the AI evals (3/6 cells of 09
   cited collisions/clipping). Wants a robust rendering/checking tool →
   `tools/layout_check.py`.

## Implications recorded

- Glance ≠ whole story: 09's animation value is invisible to the
  screenshot eval; human pass must weight it.
- A "number without a referent" is an accuracy-adjacent failure mode the
  rubric doesn't currently name; consider a rubric v2 item.
- Linearity is a feature, not a fallback — layered/tabbed designs pay an
  intimidation cost the AI judges did not charge (they ranked
  layered-dashboard #1).
