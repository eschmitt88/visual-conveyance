---
slug: tradeoff-decision
version: 1
---

# Key facts — tradeoff-decision

Ground truth for evaluators. Facts F1–F15 are atomic, checkable claims; a
presentation conveys a fact if a reader would come away believing it
(exact wording not required, numbers and directionality are). Takeaways
T1–T4 are the critical structural conclusions.

## Facts

- **F1.** Must-have requirements: p95 ≤ 100 ms at 10M vectors including
  filtered traffic (M1); recall@10 ≥ 0.92 unfiltered (M2); filtered
  recall@10 ≥ 0.90 down to 5% selectivity (M3); EU data residency (M4);
  ≤ $2,500/month at ~10M vectors (M5).
- **F2.** Current scale is ~4.1M product vectors, doubling roughly every
  year; ~10M is the 12-month planning scale and 100M is a 4–5 year
  horizon. 30% of queries carry metadata filters, and that share is
  growing.
- **F3.** The evidence comes from a two-week bakeoff (June 2026) on the
  same frozen 10M-vector dataset for all four options, identical hardware
  for the self-hosted ones, replaying a 48-hour production query log at
  120 QPS; recall measured against exact brute-force ground truth.
- **F4.** Unfiltered p95 latencies at 10M: Braid 12 ms, Quiver 18 ms,
  Hearth 41 ms, pgnearest 95 ms. All are within the 100 ms ceiling
  unfiltered; the ordering is Braid fastest, pgnearest slowest.
- **F5.** Recall@10 unfiltered: Braid 0.98, Quiver 0.97, Hearth 0.94,
  pgnearest 0.89. Only pgnearest is below the 0.92 must-have floor.
- **F6.** pgnearest is eliminated on must-haves: its filtered p95 is
  110 ms (fails M1) and its recall@10 is 0.89 (fails M2).
- **F7.** Braid is eliminated on a single must-have: it has no native
  filtered search, and post-hoc filtering collapses its recall@10 to 0.71
  at 5% filter selectivity (fails M3) — despite having the best raw speed
  and recall in the bakeoff.
- **F8.** Quiver and Hearth pass all five must-haves; Hearth passes M3
  with zero margin (filtered recall exactly 0.90 at 5% selectivity,
  degrading to 0.86 at 1%), while Quiver holds 0.95 even at 1%
  selectivity.
- **F9.** Monthly infra cost at 1M vectors: Quiver is the cheapest option
  at $180 (Hearth $520, pgnearest $240, Braid $210).
- **F10.** Monthly infra cost at 10M: Hearth $1,400 vs Quiver $1,900
  (both within the $2,500 ceiling); at 100M: Hearth $6,800 vs Quiver
  $23,000 — roughly 3.4× — with pgnearest ~$13,500 and Braid ~$4,200 as
  unvalidated estimates for already-eliminated options.
- **F11.** The infra-only cost crossover between Quiver and Hearth sits
  around 3M vectors — already behind the company's current 4.1M — but
  counting Hearth's ~0.2 FTE steady-state ops labor (~$2,800/mo loaded),
  the total-cost crossover moves out to roughly 30M vectors, around 2029
  at current growth.
- **F12.** Operational burden is the survivors' key non-cost difference:
  Quiver is effectively zero FTE (vendor-managed, 99.9% SLA), while
  Hearth needs ~0.5 FTE in the first quarter, ~0.2 FTE steady-state, and
  a ≥4-engineer on-call rotation, all resting on an approved-but-unfilled
  infra hire (req PLAT-7).
- **F13.** Lock-in and residency cut against Quiver: proprietary query
  DSL with an exit estimated at ~3 engineer-weeks and growing, and
  in-VPC deployment is permanently unavailable — a problem if 2027
  enterprise contracts require it. Hearth is low lock-in and runs
  in-VPC.
- **F14.** The recommendation is conditional: adopt Hearth IF the PLAT-7
  hire has signed and started by 2026-10-01 AND a ≥4-engineer on-call
  rotation is committed by the same date; if either fails, adopt Quiver
  with a mandatory exit plan (vendor-neutral `SearchIndex` adapter,
  quarterly export drill into a scratch Hearth cluster, standing
  ~3 engineer-week migration budget, re-evaluation at 30M vectors or
  first renewal).
- **F15.** A standing sensitivity trigger overrides both branches: if
  filtered queries exceed ~60% of traffic or facet selectivity commonly
  drops below ~2%, the recommendation flips to Quiver even if the hire
  lands, because Hearth's filtered recall has no margin there. Headcount
  checkpoint 2026-10-01; full decision review 2027-01-15.

## Critical takeaways

- **T1.** There is no dominant option: two of the four are eliminated by
  must-have failures, and the surviving pair trade directly — Hearth wins
  cost trajectory, lock-in, and residency; Quiver wins operational
  simplicity and filtered-recall margin.
- **T2.** The recommendation is conditional, not a winner: Hearth if the
  infra headcount materializes by 2026-10-01, otherwise Quiver with an
  explicit exit plan — and a filter-share trigger can flip it to Quiver
  regardless.
- **T3.** The cost ranking inverts with scale: Quiver is cheapest at 1M
  vectors and most expensive at 10M and 100M; the infra crossover
  (~3M vectors) is already past, and the labor-adjusted crossover
  (~30M, ~2029) is inside this decision's lifetime.
- **T4.** Benchmarks alone would pick the wrong option: the fastest,
  highest-recall candidate (Braid) fails the filtered-search must-have,
  and the real decision hinges on operations, cost trajectory, and
  lock-in — not raw speed.
