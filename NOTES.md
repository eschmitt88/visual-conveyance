# NOTES

Running log of work sessions. `/wrap` appends a new dated section at the
end of each session with **Did / Findings / Next** subsections. The
SessionEnd hook backstops this if you forget.

<!-- entries go below this line, newest at bottom -->

## 2026-07-02 (session spanned 07-01→07-02)

### Did

- Scaffolded project (public repo + Pages), set `agency: max`.
- Literature phase: /discover (12 candidates) → auto-ingested 7 sources
  (MermaidSeqBench, DiagramEval, IGenBench, Visualization JUDGE,
  glanceability thresholds, LIDA, Google Generative UI); 6 concepts seeded.
- Designed the Phase 1 study (ADR 0001): 7 approach specs (`approaches/`),
  6 test cases with held-out key facts (`testcases/`), eval rubric v1 +
  run protocol (`eval/`), Playwright screenshot harness (`tools/`).
- Ran experiments/2026-07-01-baseline-matrix: 42 generator subagents →
  42 static pages on Pages; 42 blind evaluator subagents (screenshot-first
  glance pass, per-fact accuracy audit) → metrics.json. One eval wave was
  lost to the 5h session-limit reset and relaunched.
- Built the human-eval gallery (rate 1–5 + notes + JSON export) and
  manifest with `human_evaluated` flags.

### Findings

- AI ranking: layered-dashboard 9.02 > interactive 8.73 > metaphor 8.43 >
  scrolly-slides 8.23 > prose control 7.95 > infographic 7.38 > mermaid 7.30.
- Dashboard won 5/6 test cases — suspiciously universal; flagged possible
  judge bias toward progressive disclosure.
- Infographic and mermaid scored BELOW prose even on glance — compression
  cost accuracy without buying glanceability; mermaid pages rendered
  small/illegible diagrams (a fixable spec bug, logged as next_candidate).
- Literature converged on judge-score decomposition + atomic fact
  verification (which rubric v1 does), and named glance-level communicative
  effectiveness as an unstudied gap — this project sits in it.

### Next

- Human ratings via the gallery (instructions in
  experiments/2026-07-01-baseline-matrix/results/human/README.md), then
  human-vs-AI rank correlation.
- v2 mermaid spec with minimum diagram size; hybrid dashboard+metaphor
  approach; multi-judge panel if the human pass disagrees with the sweep.
