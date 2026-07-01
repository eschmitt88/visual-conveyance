"""Build docs/presentations/manifest.json from the on-disk matrix + evals.

Scans docs/presentations/<testcase>/<approach>/index.html, joins AI eval
scores from the experiment's results/evals/, and preserves any existing
human evaluation state (human_evaluated, human_rating, human_notes).

Usage: uv run python tools/build_manifest.py [experiments/<run>]
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRES = ROOT / "docs" / "presentations"
RUN = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "experiments" / "2026-07-01-baseline-matrix"


def main() -> None:
    manifest_path = PRES / "manifest.json"
    old = {}
    if manifest_path.exists():
        for cell in json.loads(manifest_path.read_text()).get("cells", []):
            old[(cell["testcase"], cell["approach"])] = cell

    cells = []
    for html in sorted(PRES.glob("*/*/index.html")):
        tc, ap = html.parent.parent.name, html.parent.name
        eval_path = RUN / "results" / "evals" / f"{tc}--{ap}.json"
        scores = None
        if eval_path.exists():
            scores = json.loads(eval_path.read_text()).get("scores")
        prev = old.get((tc, ap), {})
        cells.append({
            "testcase": tc,
            "approach": ap,
            "path": f"{tc}/{ap}/index.html",
            "ai_scores": scores,
            "ai_evaluated": scores is not None,
            "human_evaluated": prev.get("human_evaluated", False),
            "human_rating": prev.get("human_rating"),
            "human_notes": prev.get("human_notes"),
        })

    manifest = {
        "run": RUN.name,
        "rubric_version": 1,
        "testcases": sorted({c["testcase"] for c in cells}),
        "approaches": sorted({c["approach"] for c in cells}),
        "cells": cells,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    n_ai = sum(c["ai_evaluated"] for c in cells)
    n_h = sum(c["human_evaluated"] for c in cells)
    print(f"manifest: {len(cells)} cells, {n_ai} AI-evaluated, {n_h} human-evaluated")


if __name__ == "__main__":
    main()
