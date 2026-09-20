# visual-conveyance

**How should an AI agent convey complex information to a human visually?
Benchmarking diagramming languages, static HTML, infographics, and interactive
pages.**

📂 **[Browse this repo →](https://eschmitt88.github.io/visual-conveyance/)** —
interactive, always-live view of experiments, concepts, literature, and maps of
content. Served via GitHub Pages from `docs/index.html`; reads the live file
tree, no build step.

## What this is

Text is the default output of an AI agent, and for anything with structure —
architectures, timelines, trade-off spaces, data — it is often the worst
channel. This project asks which visual forms an agent should reach for and
when. Phase 1 is a controlled comparison: a fixed set of *approaches* (prompt
specs in `approaches/`, from Mermaid-style diagrams to static HTML to
interactive pages) is applied to a fixed set of *test cases* (`testcases/`),
each rendered as a static GitHub-Pages presentation, scored by AI evaluators,
then ranked by the human. The design is in
`docs/decisions/0001-experiment-design.md`. Success is a defensible ranking of
approaches per kind of content, and the prompt specs that produce them.

## How it's organized

Plain Markdown + flat YAML frontmatter, cross-linked with `[[wikilinks]]`:

- `concepts/` / `mocs/` — atomic ideas; promoted to a map of content when ≥5 cluster.
- `literature/` — processed notes on papers, repos, posts (0–5 relevance scored).
- `experiments/YYYY-MM-DD-<slug>/` — self-contained runs (hypothesis → result, config, metrics, log).
- `raw/` — immutable source captures · `docs/decisions/` — ADRs · `_meta/` — index, log, templates.

## Local use

```sh
make env    # uv sync
make lint   # knowledge-graph / experiment health check
```

Part of a personal research framework
([claude-system](https://github.com/eschmitt88/claude-system)). See `CLAUDE.md`
for the agent-facing orientation and `~/.claude/CLAUDE.md` for the framework's
durable principles.
