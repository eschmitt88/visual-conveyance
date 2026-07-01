"""Render presentation HTML files to PNGs for the AI glance/deep evaluation.

Usage:
    uv run python tools/screenshot.py docs/presentations/<tc>/<ap>/index.html ...
    uv run python tools/screenshot.py --all

For each index.html, writes alongside it:
    glance.png  — above-the-fold viewport shot, 1440x900
    full.png    — full-page shot (capped at 20000px tall)

Requires PLAYWRIGHT_BROWSERS_PATH=/mnt/projects/.playwright-browsers
(exported by the Makefile 'shots' target).
"""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PRESENTATIONS = ROOT / "docs" / "presentations"


def targets_from_args(argv: list[str]) -> list[Path]:
    if argv and argv[0] == "--all":
        return sorted(PRESENTATIONS.glob("*/*/index.html"))
    return [Path(a).resolve() for a in argv]


def main() -> None:
    targets = targets_from_args(sys.argv[1:])
    if not targets:
        sys.exit("no targets; pass paths or --all")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        for html in targets:
            page.goto(html.as_uri())
            # let Mermaid/KaTeX render; networkidle covers CDN fetches
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            page.screenshot(path=str(html.parent / "glance.png"))
            page.screenshot(path=str(html.parent / "full.png"), full_page=True)
            print(f"shot {html.parent.relative_to(ROOT)}")
        browser.close()


if __name__ == "__main__":
    main()
