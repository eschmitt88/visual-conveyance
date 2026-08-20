---
kind: repo
name: "Swark — automatic architecture diagrams from code"
url: https://github.com/swark-io/swark
commit:
source: "raw/repos/swark-io-swark.md"
added: "2026-08-20"
relevance: 2
status: scanned
related_experiments: []
related_concepts: ["diagram-dsl-generation"]
tags: [mermaid, vscode-extension, architecture-diagrams, code-visualization, copilot, agpl]
---

# Swark — automatic architecture diagrams from code

## Purpose

VS Code extension that turns a selected folder into a Mermaid architecture
diagram by prompting an LLM through the VS Code Language Model API (GitHub
Copilot as the backend, so no API key). Positioned for onboarding to an
unfamiliar codebase, reviewing AI-generated projects, keeping docs fresh,
and spotting unwanted dependencies. AGPL-3.0.

## Shape

Four stages, deliberately thin:

1. **File retrieval** — collect code files under the chosen folder,
   auto-trimming the count to fit the model's token limit
   (`swark.maxFiles`, `swark.fileExtensions`, `swark.excludePatterns`).
2. **Prompt building** — inline the retrieved files plus diagram
   instructions.
3. **LLM request** — one call via the VS Code Language Model API.
4. **Preview** — write a Markdown file containing the Mermaid block and
   render it, plus a sibling log file recording config and files used.

No IR, no parsing, no retrieval index — the pitch is explicitly that
"all the logic is encapsulated within the LLM," which is what buys
language-agnosticism for free.

## Useful bits

- **`swark.fixMermaidCycles`** — a shipped setting that automatically
  rewrites cycles in the generated Mermaid because they cause *rendering
  failures*. A production tool found the class of defect worth a
  dedicated post-processor, which is a small independent confirmation
  that raw LLM Mermaid needs a mechanical repair pass before it renders
  — the same lesson [[literature/papers/vaduva2026code2uml]] draws for
  PlantUML at much greater length.
- **Token budget handled by truncating the file set**, not by ranking or
  compacting it — the naive baseline that Code2UML's importance-weighted
  compaction is arguing against. Useful as the contrast case.
- **Every run emits a log file** (config + file list) next to the diagram.
  Cheap provenance discipline for a generation pipeline; our
  presentation cells record their channel choices for the same reason.
- Prior art for the `codebase-structure` test case: a real tool doing
  the same job we ask an approach to do, and doing it with exactly one
  LLM call and no render-check loop.

## Follow-up

- **Relevance:** 2 — a working reference implementation for one test
  case and a useful naive-baseline contrast, but it makes no measured
  claims, ships no evaluation, and sits on the Mermaid path our matrix
  already ranks last (02-mermaid 7.30, below the prose control). Nothing
  here changes an approach spec.
- Not worth a deeper pass unless we revisit `codebase-structure` and
  want a human-built comparator page for the same repo.

## Trust signals

**Credibility:** 4 — real, actively maintained open-source tool (AGPL-3.0,
published on the VS Code Marketplace, public issue tracker and
contribution guide) with an honest, unembellished README that states its
privacy and telemetry behaviour plainly. This is a 4 as an *artifact*,
not as evidence: it reports no benchmarks, no accuracy numbers, and no
evaluation of whether its diagrams are correct or useful.
