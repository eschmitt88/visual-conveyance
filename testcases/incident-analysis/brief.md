---
slug: incident-analysis
version: 1
audience: >
  An engineering manager at ledgerline — technically competent (reads code,
  understands services, queues, deploys) but not a database specialist, and
  was not on call during the incident. They know Postgres and pgbouncer by
  name, not by internals. Any DB-specific mechanism (autovacuum, dead
  tuples, covering indexes, connection pooling) needs a one-line gloss.
reading_goal: >
  In a few minutes, understand what happened during the June 24 outage, why
  it happened (the full three-way causal story, not a one-line root cause),
  how bad it was for customers and the business, why it took 4h17m to
  resolve, and what concrete changes are being made — well enough to brief
  their own team and defend the P0 priorities in planning.
required_takeaways:
  - >
    There was no single root cause. A triggering change (a search query
    rewritten to a leading-wildcard LIKE that abandoned its index) combined
    with two pre-existing latent weaknesses — autovacuum debt from a bulk
    backfill two days earlier, and jitterless client retries — to turn a
    one-endpoint regression into a platform-wide 4h17m partial outage.
    Remove any one leg and the outage shrinks to a degradation.
  - >
    Detection and diagnosis lag dominated the timeline: 68 minutes were lost
    between the first alert (14:11) and the correct diagnosis (15:19),
    mostly spent on a wrong network hypothesis, because alerting watched
    error rate rather than latency and latency dashboards sampled 1 in 100
    requests.
  - >
    Rollback was not possible — the release's migration had irreversibly
    dropped the old index (rebuild: ~6 hours) — so the feature flag, not
    the deploy pipeline, was what actually stopped the bleeding at 17:05.
  - >
    The remediation is layered and scheduled, not aspirational: three P0
    action items land in Q3 2026 — per-endpoint latency SLO alerts,
    connection-pool saturation alerting, and standardized retries with
    exponential backoff and jitter — each targeting a different leg of the
    failure.
---

# Reading brief: the June 24 ledgerline outage RCA

This is the fixed source document for a **post-incident analysis** (RCA) of
a 4-hour-17-minute partial outage at ledgerline, a B2B invoicing SaaS.
Everything a presentation must convey lives in `source.md`; the atomic,
checkable claims live in `key_facts.md`.

The material is deliberately hard to present: a dense causal narrative with
a ~20-entry timeline, three interacting causes each backed by quantitative
evidence (query-plan costs, dead-tuple counts, pool-saturation numbers,
retry multiplication), a misdiagnosis subplot, and a 9-item remediation
plan. A good presentation makes the *causal structure* legible — trigger
plus two amplifiers, and where the time actually went — rather than
flattening it into a list. The tone of the source is blameless; a faithful
presentation preserves that (systems and tooling failed, not people).
