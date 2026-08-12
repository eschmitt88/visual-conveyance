# Log — combined-matrix

2026-08-12 generation complete: 6/6 cells, all passed layout_check (self-check + independent harness gate, 0 errors 0 warnings each).
Self-check catches during generation: codebase (1 CLIPPED fixed), incident (1 CLIPPED + 1 OVERLAP fixed), diffusion (2 CLIPPED fixed), experiment-results (1 mobile H_OVERFLOW fixed), research + tradeoff clean first try.

Channel choices (generator-reported):
- codebase-structure:  prose + svg + css-layout + js-interactive (tab switcher per contribution type); declined mermaid/katex/animation
- diffusion-variants:  prose + svg + css-layout + js-interactive (CFG slider); stat tiles WITH attached meaning; declined mermaid/katex/animation
- research-project:    prose + svg + css-layout + js-interactive (tooltips, ledger↔chart linking); declined mermaid/katex
- incident-analysis:   prose + svg + css-layout + js-interactive (counterfactual "remove a leg" toggle, non-gating); declined mermaid/katex/animation
- tradeoff-decision:   prose + svg + css-layout only; declined all JS
- experiment-results:  prose + svg + css-layout only; declined all JS ("caveats read more honestly than any interaction")
Convergent pattern: hand SVG chosen over Mermaid 6/6 ("tighter control"); animation chosen 0/6; JS only where it encodes a real question.
