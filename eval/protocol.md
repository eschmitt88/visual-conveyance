---
kind: run-protocol
version: 1
---

# Run protocol v1 — how generator and evaluator agents are invoked

Recorded so a future run is comparable. The session drives one fresh
subagent per matrix cell, twice (generate, then evaluate).

## Generator prompt skeleton

Each generator receives exactly these inputs, verbatim, and nothing
else about the experiment:

1. `approaches/_contract.md` (output contract)
2. `approaches/<approach>.md` (the method)
3. `testcases/<tc>/brief.md` (audience + goals)
4. `testcases/<tc>/source.md` (the material)

Task line: "Create `docs/presentations/<tc>/<approach>/index.html`
following the method exactly and the contract strictly. The source is
the only content authority." Generators must NOT read
`testcases/*/key_facts.md`, other approaches, other cells' output, or
`eval/`. Generators do not run git.

## Render step

`make shots` (Playwright Chromium, 1440×900 viewport; glance.png =
above-the-fold, full.png = full page). Render failures are recorded in
the eval JSON (`render_issues`), not silently fixed.

Sanity gate before evaluation: a cell whose glance.png is blank or
whose HTML failed to write gets ONE regeneration with the failure
message appended; a second failure is recorded as a failed cell and
scored (visual_craft ≤ 2 per rubric).

## Evaluator prompt skeleton

Each evaluator receives:

1. `eval/rubric.md` (the rubric, including the two-pass ordering rule)
2. path to `glance.png` (must be viewed FIRST)
3. paths to `full.png`, `index.html`
4. `testcases/<tc>/key_facts.md`
5. `testcases/<tc>/brief.md` (audience definition)

Evaluators are NOT given the approach spec or told which method made
the page, and must not read `approaches/` or other evals. Output: the
rubric's JSON to `experiments/<run>/results/evals/<tc>--<approach>.json`.

## Aggregation

`tools/aggregate_evals.py` → experiment `metrics.json`:
per-cell `overall`, per-approach means of every score, per-testcase
means, approach ranking by mean overall, and rank-variance notes.

## Blindness limits (honest caveats)

- The evaluator can usually GUESS the approach from the artifact style;
  blindness only removes the spec's framing/hypothesis, not the style.
- Generator and evaluator share a base model — scores may share the
  model's taste. Human ratings are the authoritative check on exactly
  this bias.
