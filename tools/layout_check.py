"""Rendered-layout QA for presentation pages: detect the defects humans
and evaluators keep flagging — overlapping SVG text, labels clipped at
the SVG edge, tiny type, and horizontal page overflow.

Renders the real page in Chromium (same env as screenshot.py) and works
on actual client rects, so fonts, CSS, and JS-driven final states are
all accounted for — unlike static SVG lints that estimate text width
from character counts.

Usage:
    uv run python tools/layout_check.py docs/presentations/<tc>/<ap>/index.html ...
    uv run python tools/layout_check.py --all
    uv run python tools/layout_check.py --json <paths|--all>

Exit code 1 if any ERROR-level issue is found (overlap/clip/overflow);
SMALL_TEXT is reported as a warning and does not fail the check.

Requires PLAYWRIGHT_BROWSERS_PATH=/mnt/projects/.playwright-browsers.
"""

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
PRESENTATIONS = ROOT / "docs" / "presentations"

# Two text rects "overlap" when they intersect by more than JITTER px in
# BOTH dimensions and the intersection covers more than AREA_FRAC of the
# smaller rect. Tolerances absorb antialiasing and deliberate snugness.
JITTER = 3.0
AREA_FRAC = 0.10
CLIP_TOLERANCE = 2.0
MIN_FONT_PX = 9.0

PAGE_JS = """
() => {
  const issues = [];
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return null;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') return null;
    if (parseFloat(s.opacity) < 0.05) return null;
    return r;
  };
  const label = (el) =>
    (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 40);

  for (const svg of document.querySelectorAll('svg')) {
    const svgRect = visible(svg);
    if (!svgRect) continue;
    const texts = [];
    for (const t of svg.querySelectorAll('text')) {
      const r = visible(t);
      if (!r || !label(t)) continue;
      texts.push({ el: t, r });
      // clipping: text escaping the rendered svg box (viewBox crop)
      const tol = %(clip)f;
      if (r.left < svgRect.left - tol || r.right > svgRect.right + tol ||
          r.top < svgRect.top - tol || r.bottom > svgRect.bottom + tol) {
        issues.push({ type: 'CLIPPED', text: label(t) });
      }
      const fs = parseFloat(getComputedStyle(t).fontSize);
      if (fs < %(minfont)f) {
        issues.push({ type: 'SMALL_TEXT', text: label(t), px: fs });
      }
    }
    for (let i = 0; i < texts.length; i++) {
      for (let j = i + 1; j < texts.length; j++) {
        if (texts[i].el.contains(texts[j].el) ||
            texts[j].el.contains(texts[i].el)) continue;
        const a = texts[i].r, b = texts[j].r;
        const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left);
        const oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
        if (ox > %(jitter)f && oy > %(jitter)f) {
          const inter = ox * oy;
          const minArea = Math.min(a.width * a.height, b.width * b.height);
          if (inter > %(areafrac)f * minArea) {
            issues.push({ type: 'OVERLAP',
                          a: label(texts[i].el), b: label(texts[j].el) });
          }
        }
      }
    }
  }
  const de = document.documentElement;
  if (de.scrollWidth > de.clientWidth + 1) {
    issues.push({ type: 'H_OVERFLOW',
                  scrollWidth: de.scrollWidth, clientWidth: de.clientWidth });
  }
  return issues;
}
""" % {"clip": CLIP_TOLERANCE, "minfont": MIN_FONT_PX,
       "jitter": JITTER, "areafrac": AREA_FRAC}

ERROR_TYPES = {"OVERLAP", "CLIPPED", "H_OVERFLOW"}


def targets_from_args(argv: list[str]) -> list[Path]:
    if argv and argv[0] == "--all":
        return sorted(PRESENTATIONS.glob("*/*/index.html"))
    return [Path(a).resolve() for a in argv]


def check_page(page, html: Path) -> list[dict]:
    issues = []
    for width, height, tag in ((1440, 900, "desktop"), (390, 844, "mobile")):
        page.set_viewport_size({"width": width, "height": height})
        page.goto(html.as_uri())
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)
        found = page.evaluate(PAGE_JS)
        if tag == "mobile":  # at 390px only overflow is contract-relevant
            found = [i for i in found if i["type"] == "H_OVERFLOW"]
        for i in found:
            i["viewport"] = tag
        issues.extend(found)
    return issues


def main() -> None:
    argv = sys.argv[1:]
    as_json = "--json" in argv
    argv = [a for a in argv if a != "--json"]
    targets = targets_from_args(argv)
    if not targets:
        sys.exit("no targets; pass paths or --all")

    report, failed = {}, False
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for html in targets:
            issues = check_page(page, html)
            rel = str(html.parent.relative_to(ROOT)) if html.is_relative_to(ROOT) else str(html)
            report[rel] = issues
            errors = [i for i in issues if i["type"] in ERROR_TYPES]
            warns = [i for i in issues if i["type"] not in ERROR_TYPES]
            failed |= bool(errors)
            if not as_json:
                status = "FAIL" if errors else ("warn" if warns else "ok")
                print(f"{status:4s} {rel}  ({len(errors)} errors, {len(warns)} warnings)")
                for i in errors + warns:
                    print(f"       {i}")
        browser.close()
    if as_json:
        print(json.dumps(report, indent=2))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
