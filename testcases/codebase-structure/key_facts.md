---
slug: codebase-structure
version: 1
kind: key-facts
---

# Ground truth — codebase-structure

Every fact below is atomic and literally verifiable against `source.md`
(v1). Evaluators score a presentation on whether each fact is conveyed
correctly (or at least not contradicted), and whether the four takeaways
survive a glance at the above-the-fold region.

## Facts

- **F1.** The backend consists of six Python packages under `meridian/`
  — `api`, `pipeline`, `queue`, `store`, `render`, `cli` — plus a
  vanilla-JS `web/` frontend with no framework and no build step.
- **F2.** The fetch pipeline runs in this order: scheduler → fetcher →
  extractor → dedup → store → FTS index.
- **F3.** Only `store/writer.py` writes the database: every INSERT,
  UPDATE, and DELETE in the codebase lives in that one file; all other
  code reads via `store/reader.py`.
- **F4.** The extractor is pure: no network, no disk, no DB, no clock;
  the same HTML input always produces the same Article.
- **F5.** The codebase has exactly one known dependency-rule violation:
  `pipeline/extractor.py` imports `clean_html()` from
  `render/sanitize.py` (a sideways pipeline → render edge, present since
  v0.8, tracked as issue #214).
- **F6.** `store/` is the bottom layer: it imports no other meridian
  package, and nothing anywhere imports `api/` or `cli/`.
- **F7.** The largest single file in the repo is
  `pipeline/extractor.py` at 1,140 LOC, containing 14 inlined
  site-specific extraction heuristics.
- **F8.** The backend totals 13,710 LOC of Python; the largest module is
  `pipeline/` at 4,180 LOC.
- **F9.** Backend test coverage is 77% overall — highest in `store/`
  (91%), lowest in `cli/` (41%) — and the `web/` frontend has no
  automated tests at all.
- **F10.** There are 412 tests (348 unit + 64 integration) and the full
  suite runs in about 41 seconds.
- **F11.** Deduplication uses a 64-bit simhash with Hamming distance ≤ 3
  meaning duplicate; about 7% of incoming items are flagged and dropped.
- **F12.** Adding a new source type touches exactly 4 files:
  `pipeline/sources/base.py`, `pipeline/sources/__init__.py`, a
  migration in `store/migrations/`, and `cli/commands/add.py`.
- **F13.** The job queue is a SQLite `jobs` table — no external broker —
  served by 8 worker threads; typical depth is 30–60 jobs with an alert
  threshold of 500.
- **F14.** The read path is API → `store/reader` → `render/template` →
  `render/annotations`, with a p50 of 28 ms end to end.
- **F15.** The FTS5 index `articles_fts` is updated only by SQLite
  triggers defined in `schema.sql`; application code never writes it.

## Critical takeaways (what a glance MUST convey)

- **T1 — Shape.** meridian is a one-way ingest pipeline feeding a single
  SQLite store, read back out through a small HTTP API, a thin
  vanilla-JS reader, and a CLI. The store is the hub; everything else is
  layered on top of it.
- **T2 — Where changes start.** A newcomer's first change lands in one
  of two places: a new source type via the 4-file recipe centered on
  `pipeline/sources/`, or a new endpoint in `api/routes.py`. The store
  and queue layers are stable and rarely touched.
- **T3 — The scary hotspot.** `pipeline/extractor.py` is the file to
  fear: the repo's largest (1,140 LOC), 14 embedded site heuristics, and
  home to the codebase's only layering violation.
- **T4 — The discipline.** The system stays testable because of hard
  invariants: single-writer store (`store/writer.py` only),
  pure extractor, trigger-maintained FTS, strict import layering.
  Breaking these is breaking the codebase.
