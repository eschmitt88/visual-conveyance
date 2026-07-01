---
slug: tradeoff-decision
version: 1
---

# Vector search for semantic product search — decision brief

- **Author:** Mara Okonkwo, tech lead, Search Platform
- **Date:** 2026-07-01
- **Status:** Proposed — decision checkpoint 2026-10-01, full review 2027-01-15
- **Audience:** Search Platform engineers; Engineering Director (budget owner)

## 1. Context

Fernwick's semantic product search ("natural-language search") went GA in
March 2026 on a prototype index that is now the top reliability risk in the
search stack. We must pick a production vector-search engine this quarter.

**Where we are.** The catalog currently embeds **4.1M active products**
(768-dimension vectors from our in-house `sable-embed-v2` model). The
embedded corpus has roughly **doubled every year** since the beta and we
plan for that to continue: ~8M by mid-2027, ~16M by mid-2028, and the
**100M-vector mark is a 4–5 year horizon** at this growth rate. Query
volume is 85 QPS steady-state, 120 QPS peak. **30% of queries carry
metadata filters** (category, price band, seller region, in-stock), and
that share has grown every quarter since faceted semantic search shipped.

**End-to-end budget.** The search page has a 250 ms end-to-end latency
budget; the vector-search stage is allotted 100 ms at p95.

### Must-have requirements

An option that misses any of these is out, regardless of its other merits:

- **M1 — Latency:** p95 ≤ 100 ms at 10M vectors under the production query
  mix, *including* the 30% filtered traffic.
- **M2 — Quality:** recall@10 ≥ 0.92 on unfiltered queries (vs exact
  brute-force ground truth).
- **M3 — Filtered search:** metadata filtering with recall@10 ≥ 0.90 down
  to 5% filter selectivity. Post-hoc filtering that silently drops recall
  does not satisfy this.
- **M4 — Data residency:** all product and query data stays in an EU
  region.
- **M5 — Budget ceiling:** ≤ $2,500/month run cost at the 12-month
  projected scale (~10M vectors). Set by the Engineering Director.

### Nice-to-haves

- **N1:** Runs inside our own cloud account (in-VPC) — likely required by
  future enterprise-seller contracts, not required today.
- **N2:** Full corpus re-index in under 30 minutes at 10M vectors (we
  re-embed the catalog after each embedding-model release).
- **N3:** Hybrid keyword + vector scoring in one query.
- **N4:** Multi-region read replicas (2027+ roadmap).

## 2. Methodology — the two-week bakeoff

All four candidates were evaluated in a structured bakeoff, 2026-06-08 to
2026-06-19, on identical data and comparable hardware:

- **Dataset:** one frozen snapshot of 10M product embeddings
  (`sable-embed-v2`, 768-dim float32; the 4.1M live corpus plus 5.9M
  synthetic-but-realistic products generated from historical listings) —
  10M is our 12-month scale, the scale the decision must hold at.
- **Hardware:** each self-hosted candidate (Hearth, pgnearest, Braid) got
  an identical allocation: up to 3 nodes of 16 vCPU / 64 GB RAM / NVMe.
  Quiver, being vendor-managed, was measured from inside our VPC via
  private peering to its EU-west region; the ~2 ms network hop is included
  in its numbers.
- **Load:** a 48-hour production query log replayed at 120 QPS with the
  live filter mix (30% filtered). Latencies are p95 over sustained 1-hour
  runs after warm-up.
- **Recall:** recall@10 against exact brute-force k-NN ground truth,
  computed on 10,000 sampled queries.
- **Ingest:** bulk-load of the full 10M snapshot, measured as sustained
  vectors/second including index build.
- **Costs:** vendor quotes (Quiver) and our cloud price list (the rest),
  normalized to $/month at three scales: 1M, 10M, 100M vectors. Figures
  are infrastructure/subscription only; ops labor is treated separately
  (§6) because it dominates the deltas.

## 3. The options

Four candidates, four architectures:

1. **Quiver** — managed vector-search SaaS. Vendor-operated, usage-priced,
   EU-west region available. The "pay to not think about it" option.
2. **Hearth** — self-hosted open-source vector-search engine (4 years old,
   ~28k GitHub stars, quarterly releases, optional paid support at
   $1,500/mo). Runs as a clustered service on our nodes.
3. **pgnearest** — a vector-index extension for Postgres (v0.9). Rides our
   existing Postgres fleet and DBA practice; queries are plain SQL.
4. **Braid** — an embedded approximate-nearest-neighbor library, linked
   directly into the search service process. 8 years old, battle-tested as
   a library; everything around it (serving, replication, sharding) is DIY.

## 4. Deep dives

### 4.1 Quiver (managed SaaS)

- **Latency:** 18 ms p95 unfiltered; **22 ms p95 filtered**. Its native
  pre-filtering engine barely flinches at selective filters.
- **Recall@10:** **0.97** unfiltered; 0.96 filtered at 5% selectivity, and
  it held **0.95 even at 1% selectivity** — the best filtered-recall curve
  in the bakeoff.
- **Ingest:** 8,000 vectors/s (tier rate limit) → full 10M re-index in
  **~21 minutes**. Meets N2.
- **Cost:** $180/mo at 1M (Growth tier); the quote at our current 4.1M is
  **$740/mo**; **$1,900/mo at 10M**; **$23,000/mo at 100M** (above 50M
  vectors their pricing forces a dedicated-cluster Enterprise plan, which
  is where the number balloons). 12-month price lock; renewal pricing is
  not locked.
- **Ops burden:** effectively **zero FTE**. Vendor on-call, 99.9% SLA
  (≈43 min/month allowed downtime).
- **Residency:** EU-west vendor region satisfies M4. **In-VPC deployment
  is not offered** — N1 unsatisfiable, ever, on this option.
- **Ecosystem:** 6-year-old commercial product; polished SDKs and docs;
  hybrid keyword+vector scoring built in (N3 ✓).
- **Lock-in:** the highest of the four. Query DSL and hybrid-scoring API
  are proprietary; bulk export (JSONL) is supported and our vectors are
  reproducible from our own embedding pipeline, so exit is feasible but
  real: estimated **~3 engineer-weeks today**, growing as we adopt more of
  their proprietary features.
- **Must-haves:** M1 ✓ M2 ✓ M3 ✓ M4 ✓ M5 ✓ (all pass).

### 4.2 Hearth (self-hosted OSS)

- **Latency:** 41 ms p95 unfiltered; **48 ms p95 filtered**. Comfortably
  inside the 100 ms ceiling; projected ~55 ms at 20M vectors on scaled
  nodes — headroom is fine through the planning horizon.
- **Recall@10:** **0.94** unfiltered; 0.93 filtered at typical
  selectivity; **0.90 at 5% selectivity — exactly at the M3 floor** — and
  it degraded to 0.86 at 1% selectivity in our stress test. Passes M3, but
  with no margin if our facets get more selective.
- **Ingest:** 25,000 vectors/s → full 10M re-index in **~7 minutes**
  (N2 ✓, best-in-class among the service-shaped options).
- **Cost:** minimum HA deployment is a 3-node cluster at **$520/mo**,
  which covers us to roughly 5M vectors; **$1,400/mo at 10M** (3 larger
  nodes); **$6,800/mo at 100M** (9 nodes). Optional vendor support
  ($1,500/mo) not included in these figures.
- **Ops burden:** the real price. **~0.5 FTE for the first quarter**
  (deployment, tuning, runbooks, dashboards), settling to **~0.2 FTE
  steady-state**, plus a **≥4-engineer on-call rotation**. The Platform
  team has an approved infra hire (req PLAT-7) whose duties would include
  this; the req is approved but **not yet filled**.
- **Residency:** in our VPC, EU region — M4 ✓ and N1 ✓.
- **Ecosystem:** active OSS, 4 years old, quarterly releases. One breaking
  index-format change in its history (v3→v4, 2025, forced a full
  re-index). Hybrid keyword scoring exists as a beta plugin (N3 partial).
- **Lock-in:** low. Open API, data on our disks, standard deployment.
- **Must-haves:** M1 ✓ M2 ✓ M3 ✓ (at the floor) M4 ✓ M5 ✓ (all pass).

### 4.3 pgnearest (Postgres extension)

- **Latency:** **95 ms p95 unfiltered** — passing M1's ceiling with 5 ms
  to spare — but **110 ms p95 filtered**, which **fails M1** under the
  production mix. Filtering in SQL is exact and expressive, but the query
  planner's index-scan + filter interplay is what blows the budget.
- **Recall@10:** **0.89**, unfiltered and filtered alike (SQL filtering
  doesn't change recall; the index itself is the limit). **Fails M2**
  (≥0.92) and, by the same 0.89, misses M3's 0.90 floor.
- **Ingest:** 3,000 vectors/s → full 10M re-index in **~56 minutes**
  (misses N2).
- **Cost:** cheap-ish at small scale by riding the existing fleet:
  ~$240/mo marginal at 1M (upsizing the primary + replica one size);
  **$1,150/mo at 10M** (dedicated 64 GB memory-class pair); **~$13,500/mo
  estimated at 100M** — at 300 GB of index it would need a 4-shard
  partitioned fleet we did not validate, and projected latency fails
  anyway.
- **Ops burden:** the lowest marginal ops of any self-hosted option
  (~0.1 FTE) — it's just Postgres, and we already run Postgres well.
- **Ecosystem:** young — v0.9, two years old, effectively one core
  maintainer. A v1.0 with a new index type "targeting recall parity with
  dedicated engines" is on the public roadmap, undated.
- **Lock-in:** minimal. It's SQL.
- **Must-haves:** **fails M1 (filtered) and M2** → eliminated. Everything
  else about it is moot for this decision.

### 4.4 Braid (embedded library)

- **Latency:** **12 ms p95 unfiltered — the fastest thing we measured**
  (in-process, no network hop). 31 ms with post-filtering.
- **Recall@10:** **0.98 unfiltered — also the best in the bakeoff.** But
  Braid has no native filtered search; filtering is post-hoc, so recall
  collapses as filters get selective: 0.94 at 50% selectivity, **0.71 at
  5% selectivity** — far below M3's 0.90 floor. This is structural, not
  tunable: the index doesn't know about metadata.
- **Ingest:** 60,000 vectors/s → full 10M index build in **~3 minutes**.
- **Cost:** cheapest infrastructure at every scale: ~$210/mo at 1M (extra
  RAM across the 6 search-service replicas + snapshot storage), $700/mo at
  10M, ~$4,200/mo estimated at 100M — but the 100M figure assumes a
  sharding-and-replication layer **we would have to build ourselves**
  (estimated ~2 engineer-quarters), which is not in the number.
- **Ops burden:** highest engineering cost of the four: ~1.5 FTE for two
  quarters to build serving, snapshots, replication, and a filtering
  layer, then ~0.3 FTE. In-process memory pressure also couples index
  health to search-service health.
- **Ecosystem:** mature and widely used *as a library*; everything
  service-shaped is on us.
- **Lock-in:** medium — proprietary index format (rebuildable from our
  vectors) and in-process code coupling.
- **Must-haves:** **fails M3** (filtered recall 0.71) → eliminated. Its
  chart-topping speed and recall never get to matter.

## 5. Criteria matrix

Scores: ✓ pass / ✗ **must-have fail** / ~ marginal. Numbers at 10M vectors.

| Criterion                        | Quiver (SaaS) | Hearth (self-host) | pgnearest (PG ext) | Braid (embedded) |
| -------------------------------- | ------------- | ------------------ | ------------------- | ---------------- |
| p95 latency, unfiltered          | 18 ms ✓       | 41 ms ✓            | 95 ms ~             | **12 ms** ✓      |
| p95 latency, filtered (M1)       | 22 ms ✓       | 48 ms ✓            | **110 ms ✗**        | 31 ms ✓          |
| Recall@10, unfiltered (M2)       | 0.97 ✓        | 0.94 ✓             | **0.89 ✗**          | **0.98** ✓       |
| Filtered recall @5% sel. (M3)    | 0.96 ✓        | 0.90 ~ (at floor)  | 0.89 ✗              | **0.71 ✗**       |
| Ingest (full 10M re-index)       | 21 min ✓      | **7 min** ✓        | 56 min ~            | **3 min** ✓      |
| Cost @1M ($/mo)                  | **$180**      | $520               | $240                | $210             |
| Cost @10M ($/mo, M5 ≤ $2,500)    | $1,900 ✓      | **$1,400** ✓       | $1,150 ✓            | $700 ✓           |
| Cost @100M ($/mo)                | $23,000       | **$6,800**         | ~$13,500 (est.)     | ~$4,200 (est.+DIY) |
| EU residency (M4)                | ✓ (vendor EU) | ✓ (in-VPC)         | ✓ (in-VPC)          | ✓ (in-VPC)       |
| In-VPC (N1)                      | ✗ never       | ✓                  | ✓                   | ✓                |
| Ops burden (steady-state)        | **~0 FTE**    | ~0.2 FTE + on-call | ~0.1 FTE            | ~0.3 FTE after 2-qtr build |
| Ecosystem maturity               | High (6 yr commercial) | High (4 yr OSS) | Low (v0.9)      | High as library / DIY as service |
| Migration lock-in                | **High**      | Low                | Minimal             | Medium           |
| **Must-have verdict**            | **PASS**      | **PASS**           | **FAIL (M1, M2)**   | **FAIL (M3)**    |

The matrix says what the deep dives say: **pgnearest and Braid are
eliminated on must-haves**; the decision is Quiver vs Hearth, and between
them no column dominates — cost trajectory and lock-in favor Hearth,
operational simplicity and filtered-recall margin favor Quiver.

## 6. The cost picture, honestly

Two crossovers matter, and they point in different directions:

- **Infra-only:** Quiver is cheapest at 1M ($180 vs Hearth's $520 HA
  floor), but the curves cross **around 3M vectors** — at our current 4.1M
  the quote is already $740 vs $520, and the gap widens to $1,900 vs
  $1,400 at 10M and **$23,000 vs $6,800 (3.4×) at 100M**. On infra alone,
  self-hosting is already the cheaper option today.
- **Labor-adjusted:** Hearth's ~0.2 FTE steady-state is ≈ $2,800/mo of
  loaded engineer cost. Counting that, Quiver stays cheaper in total until
  roughly **30M vectors — around 2029** at 2×/yr growth. Anyone arguing
  "the SaaS is cheaper" is right until 2029 *if* the labor is truly
  marginal; it is not, if PLAT-7 is hired anyway for broader platform
  duties.

So the cost argument for Hearth is a bet on our own growth curve: at
2×/yr the corpus reaches the labor-adjusted crossover in ~3 years, and
every year on Quiver past that point costs more and deepens lock-in.

## 7. Sensitivity analysis — what flips the decision

- **S1 — Filtered search becomes primary.** If filtered queries exceed
  ~60% of traffic, or facets commonly get more selective than ~2%,
  Hearth's filtered recall (0.90 at 5% selectivity, 0.86 at 1%) sits at or
  below the floor while Quiver holds 0.95 even at 1%. **This flips the
  recommendation to Quiver regardless of headcount.** Filter share is
  trending up; this is the standing trigger to watch.
- **S2 — The ops headcount doesn't materialize.** Hearth without PLAT-7
  means on-call and tuning land on four product engineers who already own
  the search stack. That converts Hearth's cost advantage into unbudgeted
  attrition risk. **Flips to Quiver** (see §9's fallback).
- **S3 — Growth accelerates to 3×/yr.** 100M arrives in ~2.5 years, the
  labor-adjusted crossover moves under 2 years out, and Quiver's
  Enterprise-tier pricing dominates the picture. **Strengthens Hearth.**
- **S4 — Quiver renewal repricing.** Our quote is locked for 12 months
  only. A 25% renewal increase (their published list moved ~20% last year)
  moves the labor-adjusted crossover from ~30M to ~20M vectors.
  **Strengthens Hearth**, and is why the Quiver fallback carries a
  mandatory exit plan rather than open-ended commitment.
- **S5 — pgnearest v1.0 ships recall parity.** If its new index type
  actually reaches ≥0.92 recall and fixes filtered latency, the cheapest
  low-ops option re-enters. Worth a 1-week re-benchmark when v1.0 exists;
  not worth waiting for on an undated roadmap.

## 8. Risks by option

- **Quiver:** renewal repricing (S4); lock-in compounds as we adopt
  proprietary hybrid-scoring features; in-VPC never possible if enterprise
  contracts demand it; 99.9% SLA means up to ~43 min/month down without
  recourse beyond credits.
- **Hearth:** the hire (PLAT-7) is approved, not filled — the whole plan
  leans on it; one historical breaking index-format change (v3→v4) means
  major upgrades must be treated as migrations; filtered recall has no
  margin (0.90 at the 0.90 floor) if facet selectivity tightens.
- **pgnearest:** recall is an index-architecture ceiling, not a tuning
  problem; single-maintainer risk; eliminated today regardless.
- **Braid:** filtered search would require building an inverted-index
  layer (~2 engineer-quarters) just to attempt M3; in-process coupling
  puts index memory pressure inside the search service's blast radius;
  eliminated today regardless.

## 9. Recommendation — conditional, with explicit triggers

**Primary: adopt Hearth (self-hosted),** contingent on ALL of the
following holding at the **2026-10-01 checkpoint**:

1. The approved platform-infra hire (req PLAT-7) has **signed and
   started** by 2026-10-01.
2. A **≥4-engineer on-call rotation** for the search-infra service is
   committed by the Platform team, in writing, by the same date.

**Fallback: if either condition fails, adopt Quiver — with a mandatory
exit plan,** not as an open-ended commitment:

- All query construction stays behind our internal `SearchIndex`
  interface; no Quiver-proprietary DSL outside the adapter.
- Quarterly export drill: full JSONL export restored into a scratch Hearth
  cluster, timed and logged.
- A standing ~3 engineer-week migration budget, re-estimated at each
  renewal.
- Re-evaluate at **30M vectors or the first contract renewal, whichever
  comes first.**

**Standing flip trigger (overrides both):** if filtered queries exceed 60%
of traffic or common facet selectivity drops below ~2% (S1), the
recommendation becomes Quiver even if the hire lands, because Hearth's
filtered recall has no margin there.

**Why Hearth first and not the reverse:** at our growth rate the
labor-adjusted cost crossover (~30M vectors, ~2029) is inside the lifetime
of this decision; lock-in cost on Quiver compounds with every proprietary
feature we adopt; and in-VPC residency (N1) is plausibly a hard
requirement for 2027 enterprise contracts — a door Quiver keeps closed
permanently. Quiver is the better engine today on almost every soft
criterion; Hearth is the better position to be standing in come 2029. The
condition exists because that position is only reachable with the
headcount to hold it.

**Dates:** headcount checkpoint **2026-10-01**; full decision review
**2027-01-15** (re-check S1 filter-share trend, PLAT-7 status, Quiver
renewal posture, pgnearest v1.0 status).
