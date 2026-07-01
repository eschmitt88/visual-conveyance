---
kind: eval-rubric
version: 1
---

# AI evaluation rubric (v1)

The evaluator is a fresh agent that has NOT seen the approach spec and
is not told which method produced the page. Inputs, in this exact
order, and the two passes must happen in this order:

## Pass 1 — glance (before seeing anything else)

Look ONLY at `glance.png` (the above-the-fold screenshot) for the
equivalent of ~10 seconds of human attention: the layout, the headline,
whatever is legible without effort. Then, before opening any other
file, write down:

- `glance_takeaway` — 2-3 sentences: what a non-expert would believe
  the page is about and what its main message is, based on the glance
  alone. Written as the reader's honest impression, not a guess at the
  author's intent.

Then read the test case's `key_facts.md` takeaways (T*) and score:

- `glance_comprehension` (0-10) — how much of the critical takeaways
  T1..Tn a non-expert would absorb from the glance alone. 10 = all
  takeaways land; 5 = topic clear + one takeaway; 0 = would not even
  know the topic. Judge from your recorded `glance_takeaway`, not from
  what you later learn the page contains.

## Pass 2 — deep read

Now open `full.png` and the raw `index.html`, plus the test case's
`key_facts.md`.

- **Fact audit**: for every fact F1..Fn, mark one of:
  - `conveyed` — a reader of the page would learn this fact correctly
  - `absent` — not on the page
  - `distorted` — present but meaning-alteringly imprecise/overstated
  - `contradicted` — the page says otherwise
  Record a one-line location/quote for anything not `absent`.
- `accuracy` (0-10) = 10 × (conveyed + 0.5·distorted_credit) / n, where
  distorted counts 0, contradicted counts −1 (floor the sum at 0).
  I.e. accuracy = 10 × max(0, conveyed − contradicted) / n.
- `depth_comprehension` (0-10) — after 2-3 minutes with the full page,
  how completely would a motivated non-expert understand the material?
- `structure_nav` (0-10) — can a reader find a specific thing again?
  Hierarchy, sectioning, wayfinding.
- `visual_craft` (0-10) — is the visual encoding honest, legible,
  purposeful (not decorative noise)? Broken rendering caps this at 2.
- `density_fit` (0-10) — is the information density right for the
  audience in `brief.md`? (Reported, not part of overall.)
- `caveat_fidelity` (true/false) — are the source's caveats/uncertainty
  visible on the page, or did it oversell? (Reported; overselling also
  shows up as `distorted` in the fact audit.)

## Overall

`overall = 0.35*accuracy + 0.30*glance_comprehension +
0.15*depth_comprehension + 0.10*structure_nav + 0.10*visual_craft`

## Output

One JSON file per presentation at
`experiments/<run>/results/evals/<testcase>--<approach>.json`:

```json
{
  "testcase": "...", "approach": "...", "rubric_version": 1,
  "glance_takeaway": "...",
  "scores": {"glance_comprehension": 0, "accuracy": 0,
             "depth_comprehension": 0, "structure_nav": 0,
             "visual_craft": 0, "density_fit": 0, "overall": 0},
  "fact_audit": {"F1": {"status": "conveyed", "note": "..."}},
  "caveat_fidelity": true,
  "render_issues": "none | description",
  "strengths": ["..."], "weaknesses": ["..."],
  "evaluator_notes": "..."
}
```

Scores are one decimal max. Be a harsh, honest grader; 8+ should be
rare. The glance pass ordering rule exists so the glance score cannot
be contaminated by knowledge of the full content — respect it.
