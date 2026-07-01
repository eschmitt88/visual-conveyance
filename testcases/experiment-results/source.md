# tessel — Onboarding Redesign ("Pathways") A/B Test: Final Readout

- **Experiment ID:** ONB-2026-014 — Growth Experimentation (fictional
  readout; test fixture)
- **Run window:** 2026-05-04 → 2026-06-14 (6 weeks of enrollment);
  conversion window closed 2026-06-28; readout 2026-06-30
- **Status:** Final. Pre-registered analysis plan v1.2 followed; one
  minor deviation noted in §8.4.

---

## 1. Executive summary

We tested a redesigned onboarding flow ("Pathways", arm B) against the
current flow (arm A) for six weeks across all new signups. The primary
metric — trial-to-paid conversion — moved from **11.4% (A) to 12.2% (B)**,
a difference of **+0.8pp with a 95% CI of [-0.3, +1.9] and p = 0.16**.
**This is not statistically significant.** The correct overall reading is
"inconclusive," not "B won."

The result that *is* actionable comes from the pre-registered platform
subgroups: **mobile-web conversion improved by +4.2pp (CI [+2.1, +6.3])**,
while **iOS regressed by -1.9pp (CI [-3.6, -0.2])**. Android was null.
These opposing effects partially cancel in the blended number, which is
why the overall result looks like a weak positive.

Two further findings shape the recommendation. First, the overall effect
decayed across the run — **+2.9pp in week 1 down to +0.1pp in week 6** —
consistent with a novelty effect; however, the mobile-web gain persists in
the late weeks, so it is not novelty alone. Second, the guardrail metric
(7-day retention) was **flat** (+0.2pp, CI [-0.2, +0.6]).

**Recommendation:** ship Pathways to **mobile-web only** (with a 5%
holdback), do **not** ship to iOS or Android, and run a targeted fix
experiment on iOS, where funnel data points at the new
notification-permission prompt at step 3 (drop-off 8.1% → 12.7%).

---

## 2. Experiment design

### 2.1 Hypothesis

The current onboarding flow (9 screens, permission prompt deferred to
day 2) loses users before they experience a first lesson. Pathways (B)
shortens the flow to 6 screens, adds a goal-setting quiz that personalizes
the starter course, moves the notification-permission ask to step 3, and
adds a social-proof screen. Hypothesis: **Pathways increases trial-to-paid
conversion by making the first-session experience faster and more
personally relevant.**

### 2.2 Primary metric

**Trial-to-paid conversion**: among users who start a free trial, the
share whose first payment succeeds within 14 days of trial start.
Denominator = trial starts; numerator = paid conversions. Note the
denominator is trial starters, not all randomized users (see §8.3 for the
check that arms enter this denominator at the same rate).

### 2.3 Sample and randomization

- **Randomized:** 184,204 new signups, split 50/50 at account creation
  (A: 92,114; B: 92,090).
- **Analyzed for primary metric (trial starters):** 13,249
  (A: 6,602; B: 6,647).
- Assignment sticky per account; no crossover observed (§8.2).

### 2.4 Power

The pre-experiment power analysis assumed an 11.5% baseline conversion and
~6,400 trial starters per arm over six weeks, giving **80% power to detect
an absolute lift of +1.55pp** at two-sided α = 0.05. The experiment was
**not** powered to confirm effects smaller than ~1.5pp overall — relevant
context for interpreting the +0.8pp point estimate (§9.1).

### 2.5 Pre-registered subgroups

The analysis plan (v1.2, filed 2026-04-28, before launch) pre-registered
exactly one subgroup dimension: **platform** (mobile-web / iOS / Android),
motivated by the differing payment surfaces (web checkout vs App Store vs
Play Store). No other subgroup cuts were pre-registered; any other cut in
this document is labeled exploratory.

### 2.6 Duration

Six weeks of enrollment, fixed in advance. No peeking-based early stop;
interim looks were monitoring-only (guardrails and SRM).

---

## 3. Primary result

| Arm | Trial starts | Paid conversions | Conversion |
|---|---|---|---|
| A (current) | 6,602 | 753 | 11.4% |
| B (Pathways) | 6,647 | 811 | 12.2% |

- **Difference (B − A): +0.8pp**
- **95% CI: [-0.3, +1.9]**
- **p = 0.16** (two-proportion z-test, two-sided)

**Verdict: not statistically significant.** The CI includes zero and
includes effects as negative as -0.3pp. This number should not be quoted
as a win. It also should not be quoted as "no effect" — the CI equally
includes +1.9pp; the honest overall statement is that the blended effect
is too small relative to noise (and too internally heterogeneous, §4) to
support a global ship decision either way.

---

## 4. Pre-registered subgroup analysis: platform

| Platform | n (A / B) | Conv. A | Conv. B | Δ (pp) | 95% CI | p |
|---|---|---|---|---|---|---|
| Mobile-web | 2,341 / 2,367 | 13.9% | 18.1% | **+4.2** | [+2.1, +6.3] | <0.0001 |
| iOS | 2,528 / 2,541 | 11.6% | 9.7% | **-1.9** | [-3.6, -0.2] | 0.027 |
| Android | 1,733 / 1,739 | 7.8% | 7.9% | +0.1 | [-1.7, +1.9] | 0.92 |

Reading:

- **Mobile-web is a large, unambiguous improvement.** +4.2pp on a 13.9%
  base is a ~30% relative lift, significant at any reasonable threshold,
  and it survives the multiple-comparison correction discussed in §9.1.
  Mobile-web converts from a web checkout with no app-store friction; it
  is also where the old flow was clumsiest (the 9-screen flow was designed
  for native and ported to web).
- **iOS is a significant regression.** -1.9pp on an 11.6% base is a ~16%
  relative *loss*. The CI excludes zero. §9.2 develops the mechanistic
  hypothesis (the step-3 permission prompt) with funnel evidence.
- **Android is null.** The point estimate is +0.1pp with a CI spanning
  [-1.7, +1.9]; no evidence of effect in either direction.

Consistency check: the subgroup effects, weighted by trial-start counts,
reconcile with the blended primary result — (2,354 × 4.2 − 2,535 × 1.9 +
1,736 × 0.1) / 6,625 ≈ +0.8pp. The overall number is not "a modest win
everywhere"; it is a strong win and a real loss averaging each other out.

---

## 5. Week-by-week trajectory (novelty decay)

Overall trial-to-paid conversion by enrollment week (all platforms):

| Week | Trial starts (A / B) | Conv. A | Conv. B | Δ (pp) |
|---|---|---|---|---|
| 1 (May 4–10) | 1,104 / 1,118 | 11.2% | 14.1% | **+2.9** |
| 2 (May 11–17) | 1,092 / 1,102 | 11.5% | 13.0% | +1.5 |
| 3 (May 18–24) | 1,110 / 1,109 | 11.3% | 11.9% | +0.6 |
| 4 (May 25–31) | 1,098 / 1,105 | 11.6% | 11.6% | 0.0 |
| 5 (Jun 1–7) | 1,101 / 1,111 | 11.5% | 11.1% | -0.4 |
| 6 (Jun 8–14) | 1,097 / 1,102 | 11.3% | 11.4% | +0.1 |

Cautions and reading:

- **Weekly CIs are wide** (~±2.7pp at these weekly sample sizes), so
  individual weekly deltas are noisy; the *pattern* — monotone-ish decay
  from +2.9 toward zero — is the signal, not any single cell.
- The decay is consistent with a **novelty effect**: the redesigned flow
  outperformed most among the earliest cohorts and converged toward the
  control as the run matured. **Any decision made on week-1 or week-2
  snapshots would have materially overstated B.** A mid-flight readout at
  the end of week 2 (blended +2.2pp, nominally significant at the time)
  circulated internally; this final readout supersedes it.
- **The platform split is not explained by novelty.** Exploratory pooled
  late-window checks (weeks 4–6): mobile-web remains **+3.8pp**
  (CI ≈ [+0.8, +6.8]); iOS remains negative at **-2.2pp**
  (CI ≈ [-4.6, +0.2], no longer individually significant at this halved
  sample). The mobile-web gain persists after novelty washes out; the iOS
  deficit does not recover.

---

## 6. Guardrails

| Guardrail | A | B | Δ | 95% CI | Status |
|---|---|---|---|---|---|
| 7-day retention (all randomized users) | 31.2% | 31.4% | +0.2pp | [-0.2, +0.6] | **Flat — pass** |
| Onboarding support tickets / 1k signups, weeks 1–2 | 4.1 | 4.6 | +12% | — | Elevated, then resolved |
| Onboarding support tickets / 1k signups, weeks 3–6 | 4.0 | 4.0 | 0% | — | **Normal — pass** |

- **7-day retention is flat.** Measured on all 184k randomized users (not
  just trialists), the CI is tight around zero: Pathways neither helps nor
  harms whether users come back in week one. The conversion story does not
  come at a retention cost — and equally, the mobile-web conversion gain
  is *not* accompanied by a retention gain.
- **Support tickets rose +12% in the first two weeks** (driven by
  confusion around the goal-quiz "skip" affordance, per ticket tagging), a
  copy fix shipped 2026-05-15 to both arms' shared components, and volume
  normalized from week 3 onward. Treated as a launch-quality blip, not a
  standing cost of the design.

---

## 7. Secondary metrics

| Metric | A | B | Δ | 95% CI | p |
|---|---|---|---|---|---|
| Median time-to-first-lesson | 4m 52s (292s) | 4m 14s (254s) | **-38s** | [-45, -31] | <0.001 |
| Trial-start rate (of randomized) | 7.17% | 7.22% | +0.05pp | [-0.19, +0.29] | 0.69 |
| Lessons completed, first 7 days (mean) | 3.9 | 4.0 | +0.1 | [-0.1, +0.3] | 0.24 |

- **Time-to-first-lesson improved by 38 seconds** (median; bootstrap CI),
  the one secondary that is clearly significant. The shorter flow does
  what it was designed to do mechanically — users reach a lesson faster —
  but this did not translate into a blended conversion or retention win.
- Trial-start rate is flat between arms, which matters for the primary
  metric's validity: see §8.3.

---

## 8. Diagnostics

### 8.1 Sample-ratio mismatch (SRM)

Randomized counts A: 92,114 vs B: 92,090 against a 50/50 target;
χ² p = 0.96. **No SRM.** Weekly SRM monitoring never alarmed.

### 8.2 Instrumentation

Assignment and exposure logging were verified against the payments ledger
on a 2% audit sample (n = 3,684): zero cross-arm contamination, zero
duplicate assignment, conversions reconciled within 0.1%. No issues.

### 8.3 Denominator integrity

Because the primary metric conditions on trial start, a treatment that
changed *who* starts trials would bias the comparison. Trial-start rate is
statistically flat (7.17% vs 7.22%, p = 0.69) and platform mix among
trialists is near-identical across arms (within 0.4pp per platform), so
the conditioned comparison is sound.

### 8.4 Deviation from plan

One: a planned supplementary Bayesian shrinkage estimate of weekly deltas
was dropped for time, replaced by the pooled late-window checks in §5. No
registered primary or subgroup analysis was altered.

---

## 9. Interpretation

### 9.1 How seriously to take the subgroups

Subgroup results are where A/B readouts usually go wrong, so two cautions
are owed. First, **multiple comparisons**: three platform tests were run.
Under a Bonferroni-adjusted threshold (α = 0.0167), mobile-web
(p < 0.0001) survives easily; iOS (p = 0.027) does **not** survive the
strict correction. Second, and cutting the other way: platform was the
**single pre-registered subgroup dimension**, chosen in advance for a
stated mechanistic reason (different payment surfaces), not discovered by
scanning many cuts. Pre-registration plus a coherent mechanism (§9.2)
makes the iOS regression a **credible signal that warrants action** —
specifically a targeted follow-up experiment — while stopping short of
proof. The mobile-web result needs no such hedging.

### 9.2 The iOS regression: permission-prompt hypothesis

Pathways moved the notification-permission ask from day 2 (a soft
in-product card) to **onboarding step 3**, where iOS fires the system
permission dialog. Funnel step data (exploratory, but directly on the
hypothesized mechanism):

- **iOS step-3 drop-off: 8.1% (A) vs 12.7% (B)** — users abandoning
  onboarding at the permission step, out of iOS users reaching step 3
  (A: 31,240 reached, 2,530 dropped; B: 31,020 reached, 3,940 dropped).
- No comparable drop-off shift on mobile-web, where step 3 is a soft
  email opt-in with no OS dialog (3.2% A vs 3.4% B), or on Android,
  where the OS dialog is lower-friction (5.0% A vs 5.6% B).
- iOS users who dismissed the step-3 dialog in B converted at 7.9% vs
  10.4% for those who accepted — consistent with the prompt souring or
  filtering the marginal user, though this comparison is confounded by
  user intent and is not causal evidence on its own.

The concentration of the regression at exactly the changed step, on
exactly the platform with the highest-friction system dialog, is why the
recommendation is "fix and re-test on iOS" rather than "abandon iOS."

### 9.3 What this readout does NOT support

- Not "B increased conversion by 0.8 points": the blended effect is not
  significant, and the blend averages a win with a loss.
- Not a platform-wide ship: iOS would likely pay a real conversion cost
  (best estimate -1.9pp on the highest-revenue platform).
- Not "the redesign failed": mobile-web is a large, durable,
  pre-registered, mechanism-consistent win.
- Not the early-week numbers: the +2.9pp week-1 snapshot reflects novelty
  that fully decayed and should not be cited.

---

## 10. Recommendation and next steps

1. **Ship Pathways to mobile-web only**, target 2026-07-06, with a **5%
   holdback** for 8 weeks to confirm the +4.2pp effect out-of-experiment
   and monitor for post-novelty drift.
2. **Do not ship iOS.** Launch a follow-up experiment (ONB-2026-019,
   draft) testing Pathways-on-iOS with the permission prompt reverted to
   the day-2 soft ask (and a second arm with a pre-permission explainer
   screen). Primary metric unchanged; powered for a ±1.5pp iOS-only
   effect, est. 8 weeks.
3. **Do not ship Android.** Null result; revisit after the iOS fix
   experiment settles the prompt question, since Android shares the flow.
4. **Retire the week-2 interim readout** from internal decks; this
   document supersedes it.
5. Re-estimate revenue impact for the mobile-web ship using the
   late-window +3.8pp (conservative) to full-run +4.2pp range.

---

## Appendix A: Full numbers table

### A.1 Assignment and funnel

| Quantity | A (current) | B (Pathways) |
|---|---|---|
| Randomized users | 92,114 | 92,090 |
| Trial starts | 6,602 | 6,647 |
| Trial-start rate | 7.17% | 7.22% |
| Paid conversions | 753 | 811 |
| Trial-to-paid conversion | 11.4% | 12.2% |

### A.2 Primary and subgroup effects (B − A, pp)

| Scope | n (A / B) | Conversions (A / B) | Conv. A | Conv. B | Δ | 95% CI | p |
|---|---|---|---|---|---|---|---|
| **Overall** | 6,602 / 6,647 | 753 / 811 | 11.4% | 12.2% | +0.8 | [-0.3, +1.9] | 0.16 |
| Mobile-web | 2,341 / 2,367 | 325 / 428 | 13.9% | 18.1% | +4.2 | [+2.1, +6.3] | <0.0001 |
| iOS | 2,528 / 2,541 | 293 / 246 | 11.6% | 9.7% | -1.9 | [-3.6, -0.2] | 0.027 |
| Android | 1,733 / 1,739 | 135 / 137 | 7.8% | 7.9% | +0.1 | [-1.7, +1.9] | 0.92 |

(Platform conversion counts sum to the overall counts: 325+293+135 = 753;
428+246+137 = 811.)

### A.3 Weekly overall deltas (pp)

| Week | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Δ (B − A) | +2.9 | +1.5 | +0.6 | 0.0 | -0.4 | +0.1 |

Weekly CIs approximately ±2.7pp; see §5 for cautions.

### A.4 Guardrails and secondaries

| Metric | A | B | Δ | 95% CI |
|---|---|---|---|---|
| 7-day retention | 31.2% | 31.4% | +0.2pp | [-0.2, +0.6] |
| Median time-to-first-lesson | 292s | 254s | -38s | [-45, -31] |
| iOS step-3 drop-off | 8.1% | 12.7% | +4.6pp | — |
| Mobile-web step-3 drop-off | 3.2% | 3.4% | +0.2pp | — |
| Android step-3 drop-off | 5.0% | 5.6% | +0.6pp | — |

*All names, users, and numbers are fictional; the dossier is a fixed test
fixture for presentation methods.*
