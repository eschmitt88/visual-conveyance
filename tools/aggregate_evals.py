"""Aggregate per-cell eval JSONs into the experiment's metrics.json.

Usage: uv run python tools/aggregate_evals.py [experiments/<run>]
"""

import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUN = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "experiments" / "2026-07-01-baseline-matrix"

SCORE_KEYS = ["overall", "glance_comprehension", "accuracy",
              "depth_comprehension", "structure_nav", "visual_craft",
              "density_fit"]


def main() -> None:
    evals = sorted((RUN / "results" / "evals").glob("*.json"))
    cells = []
    for path in evals:
        data = json.loads(path.read_text())
        cells.append({"testcase": data["testcase"], "approach": data["approach"],
                      **{k: data["scores"][k] for k in SCORE_KEYS}})

    def group_means(key):
        out = {}
        for group in sorted({c[key] for c in cells}):
            rows = [c for c in cells if c[key] == group]
            out[group] = {k: round(statistics.mean(r[k] for r in rows), 2)
                          for k in SCORE_KEYS}
            out[group]["n"] = len(rows)
        return out

    by_approach = group_means("approach")
    ranking = sorted(by_approach, key=lambda a: -by_approach[a]["overall"])

    metrics = {
        "n_cells": len(cells),
        "rubric_version": 1,
        "approach_ranking_by_overall": ranking,
        "by_approach": by_approach,
        "by_testcase": group_means("testcase"),
        "cells": {f"{c['testcase']}--{c['approach']}": c["overall"] for c in cells},
    }
    (RUN / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(f"aggregated {len(cells)} evals -> {RUN / 'metrics.json'}")
    for a in ranking:
        print(f"  {a}: overall {by_approach[a]['overall']} "
              f"(glance {by_approach[a]['glance_comprehension']}, "
              f"acc {by_approach[a]['accuracy']})")


if __name__ == "__main__":
    main()
