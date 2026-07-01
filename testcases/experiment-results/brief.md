---
slug: experiment-results
version: 1
audience: >
  A product manager at tessel (a language-learning app) with basic stats
  literacy — comfortable with conversion rates, confidence intervals, and
  "statistically significant," but not a statistician. They own the
  ship/no-ship decision for the redesigned onboarding flow and will act on
  whatever impression the presentation leaves. The failure mode to avoid at
  all costs: walking away believing "B won overall, ship it everywhere."
reading_goal: >
  In a couple of minutes, understand that the overall result is NOT
  significant and must not be read as a win; that the real, credible story
  is a platform split (mobile-web up strongly, iOS down); that the early
  weeks overstated the effect because of novelty decay; that the guardrail
  held; and therefore that the right decision is a narrow ship (mobile-web
  only) plus an iOS fix experiment — not a full rollout and not a kill.
required_takeaways:
  - >
    The overall conversion difference (+0.8pp, 95% CI [-0.3, +1.9],
    p=0.16) is NOT statistically significant. Do not read this experiment
    as "B won" — the honest overall verdict is "can't tell."
  - >
    The real story is a pre-registered platform split: mobile-web improved
    strongly (+4.2pp, CI [+2.1, +6.3]) while iOS significantly regressed
    (-1.9pp, CI [-3.6, -0.2]); Android was null. The two effects partially
    cancel in the overall number.
  - >
    A novelty effect decayed over the run (week 1: +2.9pp overall; week 6:
    +0.1pp), so early snapshots overstated B — but the mobile-web gain
    persists in the late weeks, so it is not just novelty.
  - >
    The recommendation is narrow: ship B to mobile-web only (with a
    holdback), do NOT ship iOS, and run a fix experiment for the likely
    culprit — the new notification-permission prompt at onboarding step 3,
    where iOS drop-off jumped from 8.1% to 12.7%.
---

# Reading brief: tessel onboarding A/B readout

This is the fixed source dossier for the results readout of a 6-week A/B
test at **tessel**, a fictional language-learning app: redesigned
onboarding flow "Pathways" (B) versus the current flow (A). Everything a
presentation method needs to convey lives in `source.md`; the atomic,
checkable claims live in `key_facts.md`.

The audience is the deciding PM. This dossier is deliberately easy to
oversimplify: the headline delta is positive but not significant, the
subgroup effects point in opposite directions, and the weekly trajectory
means "when you look" changes what you see. A good presentation makes the
uncertainty visible at a glance — CIs that straddle zero must *look*
different from CIs that don't — surfaces the platform split as the main
event rather than a footnote, shows the novelty decay, and lands the
narrow recommendation. A presentation that leaves the impression "B is up
0.8 points, ship it" has failed on this material, no matter how polished
it looks.
