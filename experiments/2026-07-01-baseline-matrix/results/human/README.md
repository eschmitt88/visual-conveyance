# Human evaluation — how to submit ratings

Status: **0/42 rated**. Human ranking is the authoritative signal;
the AI scores in `../..​/metrics.json` are the search signal only.

## Procedure

1. Open the gallery: https://eschmitt88.github.io/visual-conveyance/presentations/
   (or `docs/presentations/index.html` locally).
2. For each cell: open it, give it an honest ~10-second glance, note
   what you absorbed, then read properly. Rate 1–5 stars in the gallery
   (saved to your browser's localStorage) + optional notes. Rows
   (same material, different method) are the most useful comparisons —
   you don't need all 42; even 2–3 full rows is a strong signal.
3. Click **Export ratings** and paste the JSON blob to Claude in a
   session in this project.

Claude then writes the blob to `results/human/ratings-YYYY-MM-DD.json`,
flips `human_evaluated` flags in `docs/presentations/manifest.json`,
computes human-vs-AI rank correlation into `metrics.json`, and updates
the experiment README.

## What to judge (mirrors the AI rubric, eval/rubric.md)

- Did the glance land? (the project's headline metric)
- Is it accurate and honest once you read deeply?
- Would you want your AI to communicate with you like this?
