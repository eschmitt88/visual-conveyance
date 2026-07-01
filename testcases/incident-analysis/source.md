---
slug: incident-analysis
version: 1
kind: source-material
title: "INC-1194 — Post-incident analysis: partial API outage, 2026-06-24"
---

# INC-1194 — Partial API outage, 2026-06-24 (14:02–18:19 UTC)

- **Severity:** SEV-1 (partial outage, customer-facing)
- **Duration:** 4 h 17 m (14:02–18:19 UTC, 257 minutes)
- **Status of this document:** Final — published 2026-07-01
- **Authors:** Incident review group (facilitated by the IC guild)
- **Review posture:** Blameless. This analysis names systems, tools, and
  process gaps, not people. Every decision described below was reasonable
  given what the responders could see at the time.

## 1. Executive summary

On June 24, 2026, ledgerline's invoicing API suffered a partial outage
lasting 4 hours 17 minutes. At peak, 31.2% of API requests were failing;
2,312 customer organizations were affected, and we expect to pay roughly
$41,300 in SLA credits.

There is no single root cause. Three independent weaknesses aligned:

1. **A query regression shipped at 14:02.** A refactor of invoice search
   (PR #8841) replaced an org-scoped, index-backed prefix lookup with a
   *leading-wildcard* `LIKE` that no B-tree index can serve. Every search
   became a sequential scan of the entire 274-million-row `invoices`
   table: ~0.4 ms per query became 24–31 seconds.
2. **Autovacuum debt from a backfill two days earlier.** A June 22 bulk
   backfill left 38.1 million dead tuples (12.2% bloat) in `invoices`.
   Postgres's autovacuum never triggered — the default threshold on a
   table this size requires ~54.9 M dead tuples. The extra bloat pushed
   scan times past the 30-second statement timeout, converting slow
   queries into errors.
3. **Connection-pool exhaustion amplified by a retry storm.** Each scan
   held a pooled database connection for up to 30 s. The pgbouncer pool
   (80 connections) saturated at 15:12. Clients retried failures on a
   fixed 1-second interval with no jitter or budget, multiplying inbound
   traffic 4.7× and pinning the pool, which took down every endpoint
   sharing it.

Diagnosis was slow: the first alert fired at 14:11, but responders spent
14:20–15:10 on a network hypothesis (anchored by a coincident cloud-provider
network advisory), and the database was not identified as the bottleneck
until 15:19 — 68 minutes after the first alert. Rollback failed at 15:40
because the release's migration had irreversibly dropped the old index.
Recovery came from a feature flag (17:05), a manual VACUUM (17:12–17:50),
and cache re-warm; all SLOs were met from 17:53 and the incident was closed
at 18:19 after 26 minutes of stable metrics.

## 2. Impact

| Measure | Value |
|---|---|
| Outage window | 2026-06-24 14:02–18:19 UTC (4 h 17 m / 257 min) |
| API error rate | 19.1% average across the window; peak 31.2% at 15:47 |
| Failed requests | ≈362,000 of ≈1.9 M requests in the window |
| Latency, affected endpoint groups | p50 85 ms → 2.9 s; p99 420 ms → 28.4 s |
| Customers affected | 2,312 organizations (24.4% of 9,480 active that day) |
| SLA credits | ≈$41,300 across 216 enterprise contracts |
| Data loss | None |
| Delayed webhooks | 37,400 queued deliveries, all replayed by 19:05 |

Notes on the numbers:

- Latency figures are for **completed** requests; requests that hit the
  30-second gateway timeout surfaced as 504s and are counted as errors,
  not in the latency percentiles.
- "Affected" means an organization saw at least one failed API request or
  dashboard action during the window. Endpoints served by read replicas
  (reporting) and the separately pooled auth service stayed healthy, which
  is why the platform-wide error rate peaked at 31.2% rather than higher.
- Invoice **writes** were never lost: creation goes through a durable
  queue, and webhook deliveries queued during the outage were replayed to
  completion by 19:05 with zero drops.

## 3. Timeline

All times UTC. Prologue rows give the pre-existing condition; the incident
clock runs 14:02–18:19 on June 24.

| Time | Event |
|---|---|
| Jun 22 09:04 | `tax_region` backfill begins: bulk UPDATE of 38.1 M historical rows in `invoices`. |
| Jun 22 14:37 | Backfill completes. Dead tuples: 38.1 M. Autovacuum threshold (≈54.9 M for this table) not crossed; no vacuum is scheduled. |
| Jun 24 14:02 | Release `2026-06-24.3` reaches 100%: PR #8841 (contains-style invoice search) + migration 0412. Canary was green. **Incident clock starts.** |
| 14:07 | (Retrospective) p99 on `GET /v2/invoices/search` jumps from 2.1 ms to >20 s in trace data. No alert exists on this signal. |
| 14:11 | First alert: api-gateway 5xx rate crosses the 2% / 5-min threshold. On-call paged. |
| 14:16 | On-call acknowledges. Error rate 4.1% and climbing; 504s visible across several endpoint groups, not just search. |
| 14:20 | **Misdiagnosis begins.** A cloud-provider advisory (14:05, "elevated packet loss" in one availability zone) plus the gateway-timeout pattern anchor a network hypothesis. Infra team engaged. |
| 14:38 | Gateway/NAT failover to the unaffected zone executed. No improvement. |
| 14:55 | Status page updated: "Degraded performance — invoicing API." (Updated every 30 min thereafter.) |
| 15:10 | Packet captures clean; provider confirms our zone was not impacted. Network hypothesis ruled out — 50 minutes after it was adopted. |
| 15:12 | (Retrospective) pgbouncer pool to the primary saturates: 80/80 server connections busy; client wait queue begins to grow. |
| 15:15 | A responder notices pgbouncer `cl_waiting` above 900 and climbing. |
| 15:19 | `pg_stat_activity` shows dozens of concurrent sequential scans from invoice search. **Database identified as the bottleneck; IC pivots.** 68 min after first alert. |
| 15:40 | Rollback attempted — and abandoned: migration 0412 dropped the covering index the old query needs; recreating it takes ~6 h. Code rollback alone would not restore performance. |
| 15:47 | Peak: error rate 31.2%; gateway inbound 15,020 rpm vs 3,200 rpm baseline (4.7×) as retry waves compound. |
| 16:05 | `CREATE INDEX CONCURRENTLY` started as insurance (it completes 21:48, after incident close). Options review settles on feature-flag disable as primary path. |
| 16:12 | Retry storm quantified: SDK and internal clients retry 5xx on a fixed 1 s interval, 3 attempts, no jitter, no budget — measured request multiplication 4.7×. |
| 16:20 | Emergency pool bump 80 → 200 tried; write p99 on the primary worsens (more concurrent scans, more I/O contention). Reverted at 16:31. |
| 16:35 | Staging verification that the exact-match search fallback uses the untouched unique index and not the dropped one. |
| 17:03 | Flag-off approved by IC. |
| 17:05 | **Mitigation:** feature flag `invoice_search_contains` set to 0%. Search falls back to exact invoice-number match. Error rate falls immediately. |
| 17:12 | Manual `VACUUM (ANALYZE)` on `invoices` started, cost limits disabled. |
| 17:15 | Error rate below 3%; pgbouncer wait queue fully drained by 17:18. Latency still above SLO (bloat + evicted caches). |
| 17:50 | VACUUM completes: 38.1 M dead tuples removed, statistics refreshed. (Disk space is marked reusable, not returned; a `pg_repack` is scheduled separately.) |
| 17:53 | All endpoint groups back within SLO (p99 < 1 s, error rate < 0.5%). |
| 18:19 | **Incident closed** after 26 minutes of stable, in-SLO metrics. Total: 4 h 17 m. |

## 4. Contributing cause 1 — the search query regression

**What changed.** PR #8841 upgraded invoice search from prefix matching
("starts with") to contains matching ("anywhere in the number"), a
long-requested feature. Two things changed at once in the ORM layer:

- The pattern gained a **leading wildcard**: `invoice_number LIKE $1 || '%'`
  became `invoice_number LIKE '%' || $1 || '%'`.
- Org scoping moved from the SQL `WHERE` clause into application-side
  post-filtering, so the query itself ran **unscoped** across all
  organizations. Results were identical after filtering, which is why the
  change passed review and its behavioral tests.

**Why that is catastrophic in Postgres.** A B-tree index can serve a
prefix pattern (it's a range scan), but a leading wildcard gives the index
nothing to anchor on — Postgres cannot use it at all. With the org filter
gone from SQL too, the planner's only option was a **sequential scan**: read
the entire table for every search.

**Evidence.** Query plans captured before/after (representative):

- Before: `Index Only Scan using idx_invoices_org_number on invoices
  (cost=0.56..8.44)` — mean 0.4 ms, p99 2.1 ms. The index *covered* the
  query: all needed columns lived in the index, so the heap was never
  touched.
- After: `Seq Scan on invoices (cost=0.00..6,214,891)`,
  `Filter: invoice_number ~~ '%…%'`, `Rows Removed by Filter: 312,344,806`,
  `Buffers: shared hit=3,214,556 read=24,661,020` — actual time
  **24,000–31,000 ms** per query. That is the whole table: 274.2 M live
  rows plus 38.1 M dead tuples (≈213 GB of heap, see cause 2).

Two mercies kept this from being even worse: Postgres synchronized
concurrent sequential scans (parallel searches shared one pass over the
table), and the heap was partially cached. Without those, scans would have
taken minutes, not tens of seconds.

**Why canary didn't catch it.** The canary environment's `invoices` table
holds ~2 M rows. The same seq scan there takes ~180 ms — slow, but under
every alert threshold. The regression is invisible until the query meets
production-scale data.

## 5. Contributing cause 2 — autovacuum debt from the June 22 backfill

*Gloss: in Postgres, an UPDATE doesn't overwrite a row — it writes a new
version and leaves the old one behind as a "dead tuple." A background
process, autovacuum, reclaims dead tuples. Until it runs, the table is
physically larger ("bloat"), and every full-table scan pays to read the
corpses.*

**What happened.** On June 22 — two days before the incident — a backfill
populated the new `tax_region` column on 38.1 M historical invoices. That
single job created 38.1 M dead tuples, growing the heap from 190 GB to
213 GB (+12%); dead tuples were 38.1 M of 312.3 M total tuples — 12.2%
bloat.

**Why autovacuum never ran.** Autovacuum triggers when dead tuples exceed
`scale_factor × live rows` — by default 20%. On a 274.2-million-row table
that threshold is ≈54.9 M dead tuples. The backfill's 38.1 M fell short,
so autovacuum — correctly, by its configuration — did nothing. The default
scale factor is sized for small tables; on very large tables it permits
tens of gigabytes of bloat. `ANALYZE` (statistics refresh) was likewise
never triggered, leaving the planner with pre-backfill statistics.

**Why it mattered.** Alone, this bloat was harmless — index-backed queries
skip dead tuples cheaply, and nothing scans this table in normal operation.
But once cause 1 turned every search into a full-table scan, the scan had
to read 312.3 M tuples instead of 274.2 M and ~23 GB of extra heap. That
pushed scan times from an estimated ~26 s (bloat-free) to the observed
24–31 s — **straddling the 30-second statement timeout**. During the
incident, ~57% of search queries were killed by the timeout
(`query_canceled`), surfacing to clients as 5xx. Bloat converted "slow" into
"failing" — and a killed query still held its pooled connection for the
full 30 seconds first.

## 6. Contributing cause 3 — pool exhaustion and the retry storm

*Gloss: the API doesn't open a Postgres connection per request; requests
borrow one of a fixed pool of server connections managed by pgbouncer. If
every connection is busy, new requests wait in a queue.*

**The arithmetic of exhaustion.** The pgbouncer pool to the primary is
sized at **80 server connections**, shared by invoice reads, writes, PDF
rendering, and webhook dispatch. Pre-incident, invoice search consumed a
negligible share (1.2 searches/s × 0.4 ms each). After the deploy, each
search held a connection for up to 30 s:

- 14:07–15:00 — organic search traffic alone (≈1.2/s × ~28 s) occupied
  ~34 of 80 connections: heavily degraded, but the pool held.
- Around 15:00, the day's largest cohort of hourly scheduled
  invoice-generation jobs landed, and retries (below) multiplied search
  arrivals to ≈5.6/s. Demand hit ≈160+ concurrent connections against a
  pool of 80. **Saturation at 15:12.** From then on, *every* endpoint
  sharing the pool queued behind 30-second scans: invoice creation, PDF
  rendering, webhook dispatch — the blast radius stopped being "search."

The client wait queue (`cl_waiting`) peaked at **1,437** at 15:58.

**The retry storm.** Our SDKs and internal service clients retried 5xx
responses on a **fixed 1-second interval, 3 attempts, no jitter, no retry
budget**. Under sustained failure this is traffic multiplication: gateway
inbound rose from a 3,200 rpm baseline to 15,020 rpm at peak — **4.7×** —
with visible 1-second-period oscillation as retry waves arrived in phase.
The retries themselves queued on the same exhausted pool, so extra load
produced zero extra successes; it only kept the pool pinned and the queue
full for nearly two hours (15:12–17:18).

**Why the pool bump backfired.** At 16:20 the pool was raised 80 → 200 as
an experiment. That admitted more concurrent sequential scans to the
primary, worsening I/O contention and write p99. It was reverted at 16:31.
The pool size was not the problem; the 30-second connection holds were.

## 7. How the three causes combined

The causal chain, in order:

1. The deploy made every search a 24–31 s full-table scan (**cause 1** —
   the trigger).
2. Backfill bloat pushed those scans past the 30 s statement timeout, so
   slow queries became failed queries (**cause 2** — first amplifier).
3. Failures triggered jitterless retries, multiplying search arrivals
   4.7× (**cause 3a** — second amplifier).
4. Multiplied 30-second connection holds exhausted the shared pool of 80,
   extending the failure to every endpoint behind the pool (**cause 3b**).
5. Those endpoints' failures also retried, sustaining the storm until the
   flag-off at 17:05 removed the scans entirely.

Remove any single leg and June 24 looks different: without the bloat,
searches are painfully slow but mostly *succeed*, retries stay rare, and
the pool (≈34/80 used) survives — a one-endpoint degradation. Without the
retry storm, demand stays near organic levels and the pool holds through
the 15:00 spike. Without the query change, nothing happens at all. This is
why the remediation plan (section 11) deliberately targets all three legs
rather than only the trigger.

## 8. Why detection and diagnosis were slow

68 minutes elapsed between the first alert (14:11) and the correct
diagnosis (15:19), of which 50 minutes (14:20–15:10) were spent actively
pursuing the network hypothesis. Contributing gaps, all systemic:

- **We alerted on error rate, not latency.** The only firing signal was
  "gateway 5xx > 2% over 5 min." Search p99 exploded at 14:07 — four
  minutes before that alert — but no latency SLO alert existed for the
  invoicing endpoint group (checkout had one; invoicing did not).
- **Latency dashboards sampled 1 in 100 requests.** At 1.2 searches/s,
  that is ~0.7 samples per minute — the search-latency panel looked like
  sparse noise, not a cliff, exactly when it mattered.
- **The deploy marker was broken.** The dashboard integration that
  annotates deploys had been broken since June 10 (a known ticket). The
  14:02 deploy was invisible on every graph responders looked at, removing
  the single strongest hint.
- **A plausible distractor arrived on cue.** The cloud provider's 14:05
  packet-loss advisory, plus gateway 504s that *look* like network
  timeouts, anchored the team. Given the missing deploy marker, the
  network theory was the most reasonable available explanation.

In retrospect, `pg_stat_activity` would have shown rows of identical
sequential scans as early as ~14:15. Nothing routed responders toward the
database until the pool queue became impossible to miss at 15:15.

## 9. Why rollback failed — and what worked instead

Release `2026-06-24.3` bundled migration 0412, which **dropped**
`idx_invoices_org_number` — the covering index the *old* query depended
on. The migration's rationale was reasonable at review time: the new query
shape no longer used the index, and it cost 31 GB and write overhead.

That made the deploy irreversible in practice:

- Rolling back the code would restore the old prefix query — which now
  also has no index to use, and would seq-scan just the same.
- Recreating the index on 274 M rows takes ~6 hours
  (`CREATE INDEX CONCURRENTLY`, started 16:05 as insurance; it finished at
  21:48, well after incident close).
- Rolling *forward* with a query fix was estimated at 50+ minutes of
  build/deploy under storm conditions, with its own risk.

**What worked: the feature flag.** The contains-search path had shipped
behind `invoice_search_contains`. After staging verification (16:35) that
the exact-match fallback used the untouched unique index
`uq_invoices_org_number`, the flag was set to 0% at 17:05. Errors fell
below 3% within ten minutes. Search ran in degraded, exact-match-only mode
until the index rebuild completed that evening; full contains search was
re-enabled (with the fixed, org-scoped query) on June 26.

The remaining recovery was cleanup: the manual VACUUM (17:12–17:50)
removed the 38.1 M dead tuples and refreshed statistics, and the buffer
caches that hours of 200-GB scans had evicted re-warmed. All SLOs were met
from 17:53; the incident closed at 18:19.

## 10. What went well

1. **Feature-flag discipline paid for itself.** Because the new query path
   shipped behind a flag, mitigation required no build, no deploy, and no
   schema change — the flip itself took 90 seconds once approved. On June
   24, flags — not the deploy pipeline — were the working safety net.
2. **No data was lost.** Invoice writes ride a durable queue and webhook
   deliveries are queued with replay: all 37,400 webhooks delayed during
   the outage were delivered by 19:05, and no customer record was dropped
   or corrupted. The blast radius was availability, not integrity.

## 11. Action items

Nine items: three P0 (this quarter, tracked weekly at the ops review),
three P1, three P2.

| # | Pri | Action | Owner | Target |
|---|-----|--------|-------|--------|
| 1 | P0 | Per-endpoint-group p99 latency SLO alerts (invoicing first); alert on latency, not only error rate | Priya N. (Observability) | Q3 2026 |
| 2 | P0 | pgbouncer saturation alerting (`cl_waiting` > 50 for 2 min) + pool sizing/isolation review so one endpoint can't starve the shared pool | Marcus T. (Infrastructure) | Q3 2026 |
| 3 | P0 | Standardize retries in all SDKs and internal clients: exponential backoff, full jitter, retry budgets | Dana K. (Platform) | Q3 2026 |
| 4 | P1 | Per-table autovacuum tuning for tables > 50 M rows (`autovacuum_vacuum_scale_factor` 0.2 → 0.01) + dead-tuple/bloat monitoring with alerts | Yuki O. (Data Eng) | Q3 2026 |
| 5 | P1 | Migration reversibility policy: destructive migrations (index/column drops) ship at least one release **after** the code that stops using them, never bundled | Marcus T. (Infrastructure) | Q3 2026 |
| 6 | P1 | CI query-plan regression check: EXPLAIN hot queries against production-scale statistics; block plans that flip to sequential scan | Alé G. (Billing Experience) | Q4 2026 |
| 7 | P2 | Production-scale query replay in canary (shadow traffic against a full-size dataset) so data-dependent regressions surface pre-deploy | Yuki O. (Data Eng) | Q4 2026 |
| 8 | P2 | Fix deploy markers on dashboards (broken since June 10) and raise latency-panel sampling 1/100 → 1/10 on tier-1 endpoints | Priya N. (Observability) | Q3 2026 |
| 9 | P2 | IC-guild training: hypothesis board + explicit deploy-correlation step in the first 15 minutes, to counter anchoring | Rotimi O. (IC guild) | Q4 2026 |

## 12. Lessons

- **Latent conditions are part of the system.** The bloat and the retry
  configuration were both known-shaped risks that were individually
  harmless for months. Outages of this class are conjunctions; reviews
  that stop at the trigger fix one third of the problem.
- **Alert on what the customer feels.** Customers felt latency at 14:07;
  our first signal was an error-rate threshold at 14:11, and our
  dashboards couldn't show the latency cliff at all. Detection gaps cost
  more minutes than any technical failure on June 24.
- **Treat irreversible changes as a category.** The engineers who bundled
  migration 0412 followed our existing norms; the norms were wrong. Schema
  changes that foreclose rollback need their own release policy (action
  item 5), not more reviewer vigilance.
- **Retries without jitter are a denial-of-service you ship to yourself.**
  A 4.7× traffic multiplier during failure is the worst possible time to
  add load. Backoff and budgets (action item 3) turn clients from
  amplifiers into dampers.
- **The responders did the right things in the wrong order because the
  system hid the right order.** With a working deploy marker and a latency
  alert, the 14:20 network detour likely never happens. We are fixing the
  instruments, not second-guessing the people who flew with them.
