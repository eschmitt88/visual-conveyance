---
slug: codebase-structure
version: 1
audience: >
  A competent software developer (comfortable with Python, HTTP APIs, and
  SQL) who has NEVER seen this codebase. They have just been asked to start
  contributing to it. They are not an expert in feed readers, content
  extraction, or SQLite internals.
reading_goal: >
  At a glance (the above-the-fold region), grasp the overall shape of the
  system — what the major parts are and how data moves through them. After
  a few minutes with the full page, know where their first change would go,
  which files matter most, and which part of the codebase to treat with
  caution.
---

# Brief: the structure of the `meridian` codebase

The source material describes **meridian**, a self-hosted read-later /
RSS service: a Python backend organized as an ingest pipeline feeding a
SQLite store, a small HTTP API, a vanilla-JS web frontend, and a CLI.
The presentation must communicate the *structure* of this codebase — its
modules, data flows, rules, and hotspots — not teach feed-reading as a
domain.

## What the reader must come away with

1. **The shape of the system.** One-way ingest pipeline
   (scheduler → fetcher → extractor → dedup → store → index) writing into
   a single SQLite database, read back out through a small API, a thin
   vanilla-JS reader, and a CLI. The store is the hub; everything layers
   on top of it.

2. **Where changes usually start.** The two contribution hot paths:
   adding a new source type (a known 4-file recipe centered on
   `pipeline/sources/`) and adding an API endpoint (centered on
   `api/routes.py`). A new contributor's first change almost certainly
   lands in one of those two places, not in the store layer.

3. **The one scary hotspot.** `pipeline/extractor.py` — the largest file
   in the repo, stuffed with site-specific heuristics, and home to the
   codebase's single known layering violation. The reader should leave
   knowing to tread carefully there, and roughly why.

4. **The rules that keep it sane.** The load-bearing invariants: only
   `store/writer.py` writes to the database, the extractor is pure, the
   full-text index is maintained only by SQLite triggers, and the import
   layering (store at the bottom, nothing imports `api` or `cli`). These
   are what make the pipeline testable and replayable — a contributor
   who breaks them breaks the codebase's core discipline.

## Notes for generators

- Numbers in the source (LOC, coverage %, timings, queue depths) are
  exact and mutually consistent; copy them exactly per the output
  contract.
- The dependency violation and the untested frontend are *negative*
  facts. They are part of the message — do not sand them off.
