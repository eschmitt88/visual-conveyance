# 0001 — Phase 1 experiment design: static-site conveyance matrix

- status: accepted
- date: 2026-07-01

## Context

Goal: find the most effective way for an AI agent to communicate complex
information to a human **visually**. Phase 1 restricts the medium to
**static sites viewable on GitHub Pages** (no build step, no server; CDN
scripts like Mermaid allowed).

## Decision

Run a full factorial matrix: every **approach** applied to every **test
case**, then a two-stage evaluation (AI first, human second).

### Units

- **Approach** (`approaches/<id>-<slug>.md`) — a reusable *method prompt
  spec*: the instructions handed to a generator agent, plus a strict
  output contract (one self-contained `index.html`). The approach file IS
  the method; changing one after a run invalidates comparisons (new ADR +
  version bump).
- **Test case** (`testcases/<slug>/`) — fixed dummy source material:
  - `brief.md` — what the reader should come away with, and who they are.
  - `source.md` — the full material to communicate (the ONLY content
    input the generator sees).
  - `key_facts.md` — enumerated ground-truth facts (F1..Fn) + critical
    takeaways (T1..Tn). **Held out from generators**; used only by
    evaluators, so generated pages can't teach to the test's phrasing.
- **Presentation** — one generated artifact at
  `docs/presentations/<testcase>/<approach>/index.html`, served by Pages.

### Generation protocol

- One fresh subagent per (approach × testcase) cell. Input: the approach
  spec + the test case `brief.md` + `source.md`. No key facts, no sight
  of other approaches' output.
- Output contract: single `index.html`, self-contained except allowed
  CDNs (Mermaid, KaTeX), no external images, works offline-ish, renders
  on desktop and mobile.

### AI evaluation protocol

- One fresh evaluator subagent per presentation; it never sees the
  approach spec and is not told which method produced the page.
- Inputs: rendered **screenshots** (above-the-fold "glance" shot at
  1440×900 + full-page shot, captured headlessly via Playwright
  Chromium) plus the raw HTML, plus `key_facts.md`.
- Two-pass reading, scored 0–10 each in `results/evals/<testcase>--<approach>.json`:
  1. **Glance pass** (screenshot of above-the-fold only, before seeing
     anything else): what would a non-expert absorb in ~10 seconds?
     → `glance_comprehension`, plus a free-text "glance takeaway" that is
     itself checked against the critical takeaways.
  2. **Deep pass** (full page + HTML): per-fact accuracy audit — each
     key fact marked conveyed / absent / distorted / contradicted →
     `accuracy` (weighted fact coverage, contradictions penalized 2×);
     plus `depth_comprehension`, `structure_nav`, `visual_craft`,
     `density_fit` (is the info density right for the audience).
  - `overall` = 0.35·accuracy + 0.30·glance + 0.15·depth + 0.10·structure
    + 0.10·visual (density_fit reported, not weighted).
- Aggregates land in the experiment's `metrics.json`: per-approach means
  across test cases, per-cell scores.

### Human evaluation

- `docs/presentations/manifest.json` tracks every cell with
  `human_evaluated: false` until the user rates it.
- The gallery (`docs/presentations/index.html`) lets the user browse the
  matrix, rate each presentation 1–5 + notes (stored in localStorage),
  and export a JSON blob to paste back into a session; that ingests into
  `experiments/<run>/results/human/` and flips the manifest flags.
- Human ranking is the **authoritative** signal; AI scores are the
  search signal. Disagreement between them is itself a finding.

## Consequences

- Matrix is 7 approaches × 6 test cases = 42 presentations, all public
  on Pages. Generation and evaluation are subagent-parallel.
- Approach/test-case files are versioned inputs; the experiment folder
  records the exact git SHA used.
- Phase 2 (later): interactivity beyond static pages, live-repo inputs
  instead of dummy material, human 5-second tests done properly.
