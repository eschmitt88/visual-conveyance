---
slug: experiment-results
version: 1
---

# Key facts: tessel onboarding A/B readout

Atomic, checkable claims from `source.md`. A presentation is scored on
whether these facts survive intact (correct numbers, correct direction,
correct significance status) and whether the takeaways are the impression
a reader actually leaves with.

## Facts

- **F1** — Primary metric is trial-to-paid conversion: A 11.4% vs
  B 12.2%, a difference of **+0.8pp**.
- **F2** — The primary difference is **not statistically significant**:
  95% CI **[-0.3, +1.9]**, p = 0.16. The CI includes zero.
- **F3** — Sample: **184,204** users randomized ~50/50
  (A 92,114 / B 92,090); primary metric computed on **13,249** trial
  starters (A 6,602 / B 6,647).
- **F4** — The experiment was powered (80%, α = 0.05) to detect a
  **+1.55pp** overall effect; +0.8pp is below the detectable size.
- **F5** — Platform was the **single pre-registered subgroup dimension**
  (registered before launch), so the platform findings are credible
  signals, not post-hoc fishing.
- **F6** — **Mobile-web improved strongly**: 13.9% → 18.1%, **+4.2pp**,
  95% CI **[+2.1, +6.3]**, p < 0.0001 (survives Bonferroni correction).
- **F7** — **iOS regressed**: 11.6% → 9.7%, **-1.9pp**, 95% CI
  **[-3.6, -0.2]**, p = 0.027 (significant, though it does not survive
  strict Bonferroni; pre-registration + mechanism make it actionable).
- **F8** — **Android was null**: +0.1pp, 95% CI [-1.7, +1.9], p = 0.92.
- **F9** — The subgroup effects reconcile with the blended result: the
  overall +0.8pp is a mobile-web win and an iOS loss **partially
  canceling**, not a modest win everywhere.
- **F10** — **Novelty decay**: the weekly overall delta fell from
  **+2.9pp in week 1 to +0.1pp in week 6** (weeks 1–6: +2.9, +1.5, +0.6,
  0.0, -0.4, +0.1); early snapshots overstated B.
- **F11** — The platform split is **not** explained by novelty: in the
  pooled late window (weeks 4–6) mobile-web is still **+3.8pp** and iOS
  is still negative (-2.2pp).
- **F12** — Guardrail held: **7-day retention is flat** (31.2% vs 31.4%,
  +0.2pp, CI [-0.2, +0.6]); support tickets rose +12% in weeks 1–2 then
  returned to normal.
- **F13** — Secondary win: median **time-to-first-lesson fell 38 seconds**
  (292s → 254s, CI [-45, -31], significant); trial-start rate was flat
  (7.17% vs 7.22%), so the primary metric's denominator is unbiased.
- **F14** — iOS mechanism evidence: **step-3 drop-off** (the relocated
  notification-permission prompt, an OS system dialog on iOS) rose from
  **8.1% (A) to 12.7% (B)** on iOS, with no comparable shift on
  mobile-web (3.2% → 3.4%) or Android (5.0% → 5.6%).
- **F15** — Recommendation: **ship Pathways to mobile-web only** (with a
  5% holdback), **do not ship iOS or Android**, and run an iOS follow-up
  experiment with the permission prompt reverted/softened. Diagnostics
  were clean (SRM χ² p = 0.96; no instrumentation issues).

## Takeaways

- **T1** — The overall effect is **not significant** — a reader must NOT
  walk away thinking "B won overall" or citing +0.8pp as a win.
- **T2** — The real story is the **platform split**: mobile-web up
  strongly, iOS significantly down, Android flat — two real effects
  hiding inside a null-looking blend.
- **T3** — A **novelty effect** means the early weeks overstated B;
  decisions based on week-1/2 numbers would have been wrong, but the
  mobile-web gain outlasts the novelty.
- **T4** — The right action is **narrow**: ship to mobile-web only, hold
  iOS/Android, and fix-and-retest the iOS permission-prompt step.
