---
slug: codebase-structure
version: 1
kind: source
title: "meridian — codebase structure dossier"
---

# meridian — codebase structure dossier

**meridian** is a self-hosted read-later / RSS service. You point it at
feeds, pages, or a mail drop; it fetches, extracts readable article text,
deduplicates, stores everything in a single SQLite database with
full-text search, and serves it back through a small HTTP API, a
vanilla-JS web reader, and a CLI. One process runs the API; one process
runs the workers; there is no external broker, cache, or database server.

A typical instance tracks ~200 feeds, holds ~120,000 articles, and runs
from one 1.8 GB SQLite file in WAL mode.

This dossier is written for a developer meeting the codebase for the
first time: shape first, then flows, then rules, then where to dig.

---

## 1. Annotated repository tree

```
meridian/
├── pyproject.toml              # uv-managed; Python 3.12; 11 runtime deps
├── meridian.toml.example       # annotated config template (copy to ~/.config/meridian.toml)
├── Makefile                    # dev entry points: make run / make workers / make test
├── meridian/                   # the backend package (13,710 LOC Python total)
│   ├── __init__.py             # version string only (30 LOC)
│   ├── config.py               # TOML config loading + validation (210 LOC)
│   ├── client.py               # thin HTTP client for the API; used by cli/ and tests (330 LOC)
│   ├── api/                    # HTTP layer — ASGI app, 31 REST endpoints (2,940 LOC)
│   │   ├── app.py              # ASGI app assembly, middleware, startup (240 LOC)
│   │   ├── routes.py           # ALL 31 endpoint handlers in one file (830 LOC) ← hotspot
│   │   ├── schemas.py          # request/response dataclasses + validation (690 LOC)
│   │   ├── auth.py             # token auth; single-user model (310 LOC)
│   │   ├── pagination.py       # cursor pagination helpers (280 LOC)
│   │   ├── opml.py             # OPML import/export of feed lists (470 LOC)
│   │   └── errors.py           # error types → HTTP status mapping (120 LOC)
│   ├── pipeline/               # ingest pipeline stages (4,180 LOC — largest module)
│   │   ├── scheduler.py        # 60 s tick; picks feeds due for polling (310 LOC)
│   │   ├── fetcher.py          # HTTP fetching; conditional GET, 20 s timeout (620 LOC)
│   │   ├── extractor.py        # readable-text extraction; PURE (1,140 LOC) ← hotspot
│   │   ├── dedup.py            # 64-bit simhash near-duplicate detection (380 LOC)
│   │   └── sources/            # source-type adapters (registry pattern)
│   │       ├── __init__.py     # SOURCE_REGISTRY mapping type → adapter (140 LOC)
│   │       ├── base.py         # SourceAdapter ABC — subclass to add a type (190 LOC)
│   │       ├── rss.py          # RSS/Atom feeds (410 LOC)
│   │       ├── html_page.py    # single-page "save this URL" source (520 LOC)
│   │       └── mailbox.py      # newsletter-by-email via IMAP drop (470 LOC)
│   ├── queue/                  # SQLite-backed job queue — no external broker (1,120 LOC)
│   │   ├── broker.py           # jobs table polling (500 ms), leasing, ack (460 LOC)
│   │   ├── worker.py           # worker pool; 8 threads by default (430 LOC)
│   │   └── retry.py            # exponential backoff: 1 min / 5 min / 30 min, then dead (230 LOC)
│   ├── store/                  # persistence — the ONLY module that touches SQLite (2,310 LOC)
│   │   ├── db.py               # connection management; WAL mode; pragmas (340 LOC)
│   │   ├── writer.py           # ALL INSERT/UPDATE/DELETE lives here (610 LOC)
│   │   ├── reader.py           # all read queries; returns frozen dataclasses (720 LOC)
│   │   ├── schema.sql          # 9 tables + articles_fts (FTS5) + triggers (280 LOC)
│   │   └── migrations/         # 7 numbered migration scripts (360 LOC)
│   ├── render/                 # turning stored articles into display HTML (1,610 LOC)
│   │   ├── template.py         # article HTML assembly, typography (520 LOC)
│   │   ├── sanitize.py         # HTML cleaning: clean_html(), tag allowlist (480 LOC)
│   │   └── annotations.py      # merges highlights into rendered HTML spans (610 LOC)
│   └── cli/                    # command-line client; talks HTTP via client.py (980 LOC)
│       ├── main.py             # arg parsing; auto-discovers commands/ (160 LOC)
│       └── commands/           # one module per subcommand
│           ├── add.py          # `meridian add <url> [--type]` (180 LOC)
│           ├── sync.py         # `meridian sync` — trigger + watch a poll cycle (200 LOC)
│           ├── search.py       # `meridian search <query>` over FTS (220 LOC)
│           └── export.py       # `meridian export` — articles to markdown/JSON (220 LOC)
├── web/                        # vanilla-JS frontend; no framework, no build step (3,280 lines)
│   ├── index.html              # single page shell (140 lines)
│   ├── js/
│   │   ├── app.js              # boot, routing between list/reader views (430 LOC)
│   │   ├── api.js              # fetch() wrappers, one per endpoint used (310 LOC)
│   │   ├── list.js             # article list, filters, keyboard nav (640 LOC)
│   │   ├── reader.js           # reading view + highlight UI (920 LOC) ← hotspot
│   │   └── settings.js         # feeds management, OPML upload (460 LOC)
│   └── css/
│       └── style.css           # single stylesheet, light/dark via media query (380 lines)
├── tests/                      # pytest; 6,240 LOC total
│   ├── unit/                   # 348 tests, mirrors package layout (3,910 LOC)
│   ├── integration/            # 64 tests; real SQLite file + live ASGI app (1,880 LOC)
│   └── fixtures/               # 1,400 captured HTML pages + helpers (450 LOC of helpers)
└── docs/
    ├── architecture.md         # prose version of the layering rules
    └── adding-a-source-type.md # the 4-file recipe, step by step
```

---

## 2. Top-level modules and responsibilities

Seven parts: six Python packages under `meridian/` plus the `web/`
frontend.

| Module | Responsibility | LOC | Coverage |
|---|---|---|---|
| `pipeline/` | Ingest: schedule polls, fetch, extract readable text, dedup. Produces articles, never serves them. | 4,180 | 84% |
| `api/` | HTTP surface: 31 REST endpoints, auth, pagination, OPML. Enqueues work; never fetches inline. | 2,940 | 62% |
| `store/` | All persistence. Owns the SQLite file, schema, migrations, FTS. The only module that touches the DB. | 2,310 | 91% |
| `render/` | Stored article → display HTML: sanitize, template, merge annotations. | 1,610 | 76% |
| `queue/` | Job queue on a SQLite table. Broker, worker pool, retry policy. No Redis, no Celery. | 1,120 | 88% |
| `cli/` | User-facing commands. Talks to the API over HTTP via `client.py`; imports no backend package. | 980 | 41% |
| shared (`config.py`, `client.py`, `__init__.py`) | Config loading and the HTTP client both ends share. | 570 | 79% |

Backend Python total: **13,710 LOC**. Overall backend line coverage:
**77%** (pytest-cov). The `web/` frontend (2,760 LOC of JS + 380 CSS +
140 HTML = 3,280 lines) has **no automated tests** — there is no JS test
harness at all. Tests add 6,240 LOC, so the whole repo is ~23,230 lines.

---

## 3. Runtime data flows

### Flow A — the fetch pipeline (write path)

```
scheduler → [jobs table] → fetcher → extractor → dedup → store → FTS index
```

1. **`pipeline/scheduler.py`** ticks every 60 s, finds feeds whose poll
   interval (default 30 min) has elapsed, and enqueues one fetch job per
   feed. Typical queue depth is 30–60 jobs; the health endpoint alerts
   at 500.
2. **`queue/broker.py`** polls the `jobs` table every 500 ms and leases
   jobs to **8 worker threads** (`queue/worker.py`). Failures retry with
   backoff at 1 min / 5 min / 30 min (`queue/retry.py`), then dead-letter.
3. **`pipeline/fetcher.py`** does the HTTP work: conditional GET
   (ETag/Last-Modified), 20 s timeout, per-host politeness delay.
4. **`pipeline/extractor.py`** turns raw HTML into a structured Article
   (title, byline, body, word count). It is **pure**: p50 45 ms,
   p95 320 ms per article, no I/O of any kind.
5. **`pipeline/dedup.py`** computes a 64-bit simhash of the body;
   Hamming distance ≤ 3 against stored hashes marks a duplicate. About
   7% of incoming items are flagged and dropped.
6. **`store/writer.py`** persists each surviving article in a single
   transaction. SQLite **triggers** defined in `schema.sql` update the
   `articles_fts` FTS5 index — application code never writes the index.

End-to-end, p50 from job dequeue to the article being searchable is
**2.1 s** (dominated by the network fetch).

### Flow B — the read path

```
browser / CLI → api → store/reader → render/template → render/annotations → response
```

`GET /articles/{id}` hits `api/routes.py`, which reads the stored
article via `store/reader.py` (6 ms p50), assembles display HTML in
`render/template.py` (14 ms), then `render/annotations.py` merges the
user's highlights — stored as character offsets into the rendered text —
into `<mark>` spans (8 ms). Total **p50 28 ms**. The web reader
(`web/js/reader.js`) and the CLI consume the same endpoints; neither has
a private backdoor into the database.

---

## 4. Module dependency rules

The layering is strict and documented in `docs/architecture.md`:

- `store/` is the bottom layer: it imports **no other meridian
  package** (stdlib + `sqlite3` only).
- `queue/` may import `store/`.
- `pipeline/` may import `store/` and `queue/`.
- `render/` may import `store/`.
- `api/` may import `store/`, `render/`, and `queue/`.
- `cli/` imports only `client.py` (it speaks HTTP; it never imports
  backend packages).
- **Nothing** imports `api/` or `cli/`.

**The one known violation:** `pipeline/extractor.py` (line 41) imports
`clean_html()` from `meridian/render/sanitize.py` — a sideways
pipeline → render edge that has existed since v0.8. It means a change to
the *display* sanitizer can silently change what gets *stored*, and it
is the reason two extractor purity tests are marked `xfail`. Fixing it
(moving `clean_html()` down into a shared location) is tracked as
issue #214 and is the top item in `docs/architecture.md`'s debt list.

---

## 5. Key invariants

1. **The extractor is pure.** Bytes in → Article out. No network, no
   disk, no DB, no clock. Deterministic: the same HTML always yields the
   same Article. A property test replays all 1,400 fixture pages on
   every CI run to enforce this.
2. **Only `store/writer.py` writes the database.** Every INSERT, UPDATE,
   and DELETE in the codebase lives in that one 610-LOC file. Everything
   else reads through `store/reader.py`.
3. **The FTS index is trigger-maintained.** `articles_fts` is updated
   only by SQLite triggers in `schema.sql`; no Python code ever touches
   it directly, so the index can never drift from the articles table.
4. **Queue jobs are idempotent.** Replaying any job must not create
   duplicate articles — dedup plus the writer's upsert keys guarantee it,
   which is what makes the retry policy safe.
5. **The API never fetches inline.** "Fetch this now" requests enqueue a
   job and return `202 Accepted`; only workers touch the network.

---

## 6. Tech-debt hotspots

1. **`meridian/pipeline/extractor.py` — the scary one.** 1,140 LOC, the
   largest file in the repo. Contains **14 site-specific extraction
   heuristics** inlined as if/elif chains (max cyclomatic complexity 38),
   plus the layering violation described above. Nearly every extraction
   bug fix lands here, and each one risks changing output for the other
   13 heuristics. The 1,400-page fixture corpus is the only safety net.
2. **`meridian/api/routes.py`.** All 31 endpoints in one 830-LOC file.
   `auth.py` exists, but 11 routes inline their own copy-pasted auth
   check instead of using it. File-level coverage is 54%, below even the
   module's 62%.
3. **`web/js/reader.js`.** 920 LOC of vanilla JS with zero tests.
   Highlight anchoring uses character offsets into the rendered HTML, so
   any markup change in `render/template.py` silently corrupts existing
   highlight positions. This coupling has caused 3 of the last 10 user-
   reported bugs.

---

## 7. Tests

- **412 tests total: 348 unit + 64 integration.** Full suite runs in
  ~41 s locally.
- `tests/unit/` mirrors the package layout one-to-one; the extractor's
  property test replays the 1,400 captured pages in `tests/fixtures/`.
- `tests/integration/` runs against a real temporary SQLite file and a
  live in-process ASGI app — no mocks at the store boundary.
- Coverage by module (backend, line): store 91%, queue 88%,
  pipeline 84%, shared 79%, render 76%, api 62%, cli 41% —
  **77% overall**. The frontend has no test harness (0%).

---

## 8. Contribution hot paths

**Adding a new source type** (the most common contribution) touches
exactly 4 files, per `docs/adding-a-source-type.md`:

1. `meridian/pipeline/sources/base.py` — subclass `SourceAdapter`
   (implement `discover()` and `fetch_items()`).
2. `meridian/pipeline/sources/__init__.py` — register the class in
   `SOURCE_REGISTRY`.
3. `meridian/store/migrations/` — one migration extending the
   `source_type` CHECK constraint.
4. `meridian/cli/commands/add.py` — expose the new `--type` value.

Plus a fixture-backed test under `tests/unit/pipeline/`. The three
existing adapters (`rss.py`, `html_page.py`, `mailbox.py`) each followed
this recipe.

**Adding an API endpoint** touches `api/routes.py` + `api/schemas.py`,
and `web/js/api.js` if the frontend consumes it.

**Adding a CLI command** is one new module in `cli/commands/` —
`main.py` auto-discovers it.

A newcomer's first change almost never touches `store/` or `queue/`;
those layers are stable (91% and 88% covered) and change only with
schema migrations.
