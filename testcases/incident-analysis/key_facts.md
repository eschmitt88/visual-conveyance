---
slug: incident-analysis
version: 1
kind: key-facts
note: >
  Ground truth for evaluators only. Held out from generators. Facts are
  atomic and checkable against source.md; takeaways are the critical
  synthesis a reader must leave with.
---

# Key facts — INC-1194 (ledgerline June 24 outage RCA)

## Facts

- **F1 — Window and duration.** Partial outage on 2026-06-24, 14:02–18:19
  UTC: 4 h 17 m (257 minutes). Severity SEV-1.
- **F2 — Error impact.** API error rate averaged 19.1% across the window,
  peaking at 31.2% at 15:47; ≈362,000 of ≈1.9 M requests failed.
- **F3 — Latency impact.** Affected endpoint groups: p50 85 ms → 2.9 s,
  p99 420 ms → 28.4 s (completed requests; timeouts surfaced as 504s at
  30 s and count as errors).
- **F4 — Customer and business impact.** 2,312 organizations affected
  (24.4% of 9,480 active that day); ≈$41,300 in SLA credits across 216
  enterprise contracts. Zero data loss; 37,400 delayed webhooks all
  replayed by 19:05.
- **F5 — Cause 1 (trigger): query regression.** PR #8841 changed invoice
  search from an org-scoped prefix lookup on a covering index to an
  unscoped leading-wildcard LIKE, which no B-tree index can serve — every
  search became a sequential scan of the full `invoices` table. EXPLAIN
  cost 8.44 → ≈6.2 M; per-query time 0.4 ms → 24–31 s; ~312.3 M tuples
  read per scan.
- **F6 — Canary blind spot.** The canary passed because its `invoices`
  table holds ~2 M rows; the same seq scan takes ~180 ms there — under
  every threshold. The regression only appears at production scale.
- **F7 — Cause 2 (amplifier): autovacuum debt.** A June 22 backfill
  (38.1 M-row UPDATE, two days pre-incident) left 38.1 M dead tuples in
  `invoices` — 12.2% bloat, heap 190 GB → 213 GB. Autovacuum never
  triggered: the default 20% scale factor needs ≈54.9 M dead tuples on a
  274.2 M-row table.
- **F8 — The bloat-timeout interaction.** The extra dead tuples pushed
  scans from an estimated ~26 s (bloat-free) to 24–31 s, straddling the
  30-second statement timeout: ~57% of searches were killed
  (`query_canceled`), turning slow queries into errors — and a killed
  query still held its connection the full 30 s.
- **F9 — Cause 3 (amplifier): pool exhaustion.** The pgbouncer pool to the
  primary (80 connections, shared by invoice reads/writes, PDF rendering,
  webhook dispatch) saturated at 15:12 when 30-second connection holds ×
  retry-multiplied search arrivals (≈5.6/s) demanded 160+ concurrent
  connections. Client wait queue (`cl_waiting`) peaked at 1,437 at 15:58.
  Pool sharing is what widened the blast radius beyond search.
- **F10 — Retry storm.** Clients retried 5xx on a fixed 1 s interval, 3
  attempts, no jitter, no budget: inbound traffic multiplied 4.7× (3,200 →
  15,020 rpm), producing zero extra successes while pinning the pool for
  ~2 hours. An emergency pool bump to 200 (16:20) made write latency worse
  and was reverted (16:31).
- **F11 — Misdiagnosis.** Responders pursued a network hypothesis
  14:20–15:10 (50 minutes), anchored by a coincident cloud-provider
  packet-loss advisory (14:05), gateway 504s that resembled network
  timeouts, and deploy markers broken since June 10. Total time from first
  alert (14:11) to correct diagnosis of the database as bottleneck
  (15:19): 68 minutes.
- **F12 — Rollback was impossible.** Migration 0412, bundled in the
  release, dropped the covering index (`idx_invoices_org_number`) the old
  query needed; code rollback alone would still seq-scan. Rebuild took ~6
  hours (`CREATE INDEX CONCURRENTLY` started 16:05, finished 21:48, after
  incident close).
- **F13 — What actually mitigated.** Feature flag
  `invoice_search_contains` set to 0% at 17:05 (after 16:35 staging
  verification that the exact-match fallback used the untouched unique
  index). Error rate fell below 3% by 17:15; the flag flip took 90 seconds
  once approved. Search ran exact-match-only until the rebuilt index
  allowed re-enable on June 26.
- **F14 — Recovery tail.** Manual VACUUM (ANALYZE) ran 17:12–17:50,
  removing the 38.1 M dead tuples and refreshing statistics; with caches
  re-warmed, all SLOs were met from 17:53; incident closed at 18:19 after
  26 minutes of stable metrics.
- **F15 — Detection gaps.** The only firing alert was error-rate based
  (gateway 5xx > 2% / 5 min, fired 14:11); no latency SLO alert existed
  for the invoicing endpoint group even though search p99 exploded at
  14:07. Latency dashboards sampled 1/100 requests (~0.7 samples/min for
  search), and the broken deploy marker hid the 14:02 deploy from every
  graph.
- **F16 — Remediation plan.** 9 action items (3 P0 / 3 P1 / 3 P2) with
  named owners and target quarters. The three P0s, all Q3 2026:
  per-endpoint p99 latency SLO alerts (Priya N., Observability); pgbouncer
  saturation alerting + pool isolation review (Marcus T., Infrastructure);
  standardized retries with exponential backoff, full jitter, and retry
  budgets (Dana K., Platform). P1s include the migration-reversibility
  policy (destructive migrations ship one release after the code stops
  using them), per-table autovacuum tuning for >50 M-row tables, and CI
  query-plan regression checks.

## Critical takeaways

- **T1 — No single cause: three independent weaknesses aligned.** A
  triggering query change plus two pre-existing latent amplifiers (vacuum
  debt from the backfill; jitterless retries on a shared pool) combined to
  turn a one-endpoint regression into a platform-wide 4 h 17 m outage.
  Remove any one leg and it's a degradation, not an outage — which is why
  the remediation targets all three legs, not just the trigger.
- **T2 — Detection lag dominated: 68 minutes lost to misdiagnosis.** The
  system alerted on error rate, not latency, sampled latency 1/100, and
  hid the deploy marker — so responders reasonably chased a network theory
  for 50 minutes while the actual cause (the 14:02 deploy) sat unmarked on
  every graph.
- **T3 — Rollback wasn't possible; feature flags saved the day.** The
  bundled migration had irreversibly dropped the needed index (~6 h to
  rebuild), so the deploy pipeline offered no way back; the 17:05 flag-off
  — a 90-second change — is what ended the bleeding.
- **T4 — The fixes are layered, scheduled, and blameless.** Three P0 items
  land in Q3 2026, one per failure leg — latency SLO alerts (detection),
  pool-saturation alerting (visibility), retry backoff + jitter
  (amplification) — plus policy changes (migration reversibility,
  autovacuum tuning) that fix the system rather than blaming the
  responders, who acted reasonably on what their instruments showed.
