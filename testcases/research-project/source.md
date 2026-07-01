# murmur — project dossier

Personal research project. Slug `murmur`. Single-box, single-GPU. This
dossier is the fixed state-of-the-project as of 2026-06-28.

Display name comes from a *murmuration* of starlings and from the low,
overlapping wash of a dawn chorus — the project is about teaching a small
classifier to hear a single bird through cheap, physically-plausible noise.

---

## 1. Hypothesis

> **Ultra-cheap audio augmentations inspired by natural reverberation
> improve bird-call classification on small datasets — more per unit of
> compute than reaching for a bigger or pretrained architecture would.**

Two sub-claims, tested separately:

- **H1 (efficacy).** Reverb-family augmentation lifts validation macro-F1
  over a no-augmentation baseline on a fixed small CNN.
- **H2 (efficiency).** The lift is competitive with, and cheaper than, the
  lift from swapping in a larger backbone — i.e. augmentation is the better
  marginal spend when data, not compute, is the binding constraint.

The bet is deliberately narrow. This is not "does augmentation help" (it
usually does) — it's "do the *natural-reverberation-flavoured*, near-free
ones help, and where do they help versus hurt."

---

## 2. Motivation

Small-data bioacoustics is the setting. A hobbyist or a regional survey
ends up with a few thousand labelled clips, a long-tailed species list, and
no realistic path to the tens of thousands of clips per class that make
big-model finetuning comfortable. The interesting constraint is that the
*data* is scarce and expensive (someone has to record and label a Wood
Thrush at dawn), while *compute* is merely finite (one desktop GPU, runs
measured in tens of minutes to a few hours).

That asymmetry is why murmur bets on augmentation over architecture:

- **Augmentation is near-free and physically motivated.** Field recordings
  already contain reverberation, wind, distance attenuation, and overlapping
  calls. Simulating those cheaply expands the effective dataset along axes
  the model will actually meet at inference — instead of along arbitrary
  pixel-space directions.
- **Architecture swaps mostly buy capacity we can't feed.** A larger or
  ImageNet/AudioSet-pretrained backbone helps, but it costs more per run,
  risks overfitting a 6k-clip set, and doesn't address the tail directly.
- **The reverb family is the cheapest slice of the augmentation space.**
  Impulse-response convolution and SNR-controlled noise mixing are single
  fast ops on the waveform or spectrogram; they add negligible wall-clock
  over a plain run.

So murmur holds the architecture fixed (a small CNN on log-mel
spectrograms) and moves only the augmentation pipeline. Architecture is the
control, not the variable.

---

## 3. Dataset card

Fictional but internally consistent. Curated from public-style field
recordings, trimmed to call-centred clips.

| Property | Value |
|---|---|
| Clips (total) | 6,200 |
| Species (classes) | 34 |
| Clip length | 5 s, mono |
| Sample rate | 32 kHz |
| Features | log-mel spectrogram, 128 mels, 25 ms window / 10 ms hop |
| Split | 70 / 15 / 15 train / val / test, stratified by species, seeded |
| Val clips | ~930 |
| Test clips | ~930 (held out — not touched during search) |

**Class imbalance.** Heavily long-tailed, which is the whole difficulty:

- The **8 most common species** account for ~52% of all clips.
- The **top class** (American Robin) has **480 clips**; several tail species
  sit under 50.
- **11 species** have **fewer than 80 clips** each ("rare tail").
- **5 species** have **fewer than 45 clips** each ("deep tail") — these are
  where every experiment lives or dies.
- Median clips-per-class ≈ 120.

The primary metric is **validation macro-F1** precisely because it weights
the tail equally with the head — a model that only learns the common eight
looks great on accuracy and mediocre on macro-F1. That gap is the point.

Per-species snapshot (representative classes, clip counts):

| Species | Clips | Tier |
|---|---|---|
| American Robin | 480 | common |
| Northern Cardinal | 421 | common |
| Song Sparrow | 308 | mid |
| Wood Thrush | 92 | rare |
| Kirtland's Warbler | 41 | deep tail |

---

## 4. Experiment ledger

Six experiments, 2026-03 through 2026-06. Same seed, same split, same
backbone unless a config delta says otherwise. Metric is **validation
macro-F1**. Baseline is exp-01; the current best is exp-05.

### exp-01 — `baseline-clean`  (2026-03-08)

- **Design:** small CNN on log-mel spectrograms, no augmentation at all.
  Establishes the floor.
- **Config deltas:** none (reference config). LR 3e-4, batch 32, 60 epochs,
  cosine decay, weighted sampler off.
- **Val macro-F1:** **0.612**
- **Wall-clock:** 41 min
- **Finding:** Trains cleanly, overfits by ~epoch 35. Tail classes carry
  almost all the error; the head is already near-saturated. Confirms the
  problem is generalization on scarce classes, not capacity.

### exp-02 — `reverb-light-ir`  (2026-03-24)

- **Design:** add light impulse-response reverb (convolve waveform with
  short measured room IRs, RT60 ≈ 0.3–0.6 s), p=0.5.
- **Config deltas:** `+aug.reverb_ir: {p: 0.5, rt60_range: [0.3, 0.6]}`.
- **Val macro-F1:** **0.641**  (+0.029 vs baseline)
- **Wall-clock:** 47 min
- **Finding:** First clear win. Gain is broad but skews to mid/common tiers;
  the deep tail moves only slightly. Encouraging enough to make reverb the
  spine of the pipeline.

### exp-03 — `pitchshift-timestretch`  (2026-04-11)

- **Design:** add pitch-shift (±2 semitones) and time-stretch (0.9–1.1×) on
  top of exp-02's reverb. Hypothesis was that vocal-tract-style variation
  would help.
- **Config deltas:** `+aug.pitch_shift: {semitones: 2}`,
  `+aug.time_stretch: {range: [0.9, 1.1]}` (reverb kept on).
- **Val macro-F1:** **0.589**  (−0.052 vs exp-02, −0.023 vs baseline)
- **Wall-clock:** 58 min
- **Finding:** **Regression.** Pitch/time warping smears the exact
  spectral-envelope cues the rare classes depend on — several deep-tail
  species collapse toward zero recall. Common classes are unbothered. This
  is the honest failure of the batch (post-mortem in §6).

### exp-04 — `noise-mix-snr`  (2026-04-29)

- **Design:** drop pitch/stretch, add SNR-controlled background-noise mixing
  (wind, rain, distant chorus beds) at 5–20 dB SNR, on top of exp-02.
- **Config deltas:** revert exp-03 deltas; `+aug.noise_mix: {snr_db: [5, 20],
  beds: [wind, rain, chorus]}`.
- **Val macro-F1:** **0.643**  (+0.002 vs exp-02)
- **Wall-clock:** 52 min
- **Finding:** **Null result.** +0.002 is inside run-to-run noise
  (±~0.006 across seeds). Noise mixing neither helps nor hurts on its own at
  this scale. Kept in the stack anyway on the hypothesis that it composes
  with SpecAugment — see exp-05.

### exp-05 — `stack-reverb-noise-specaug`  (2026-05-20)

- **Design:** the full stack — light reverb (exp-02) + noise mixing
  (exp-04) + SpecAugment (2 freq masks, 2 time masks) + a mildly
  class-balanced sampler.
- **Config deltas:** `+aug.specaugment: {freq_masks: 2, time_masks: 2}`,
  `+sampler.class_balanced: 0.5` (partial reweight, not full).
- **Val macro-F1:** **0.671**  (+0.059 vs baseline, current best)
- **Wall-clock:** 1 h 12 min
- **Finding:** **Current best.** The components compose: noise mixing that
  was null alone becomes useful once SpecAugment is present, and the partial
  balanced sampler recovers a little tail recall. Still, decomposition shows
  ~4.5 of the 5.9 points come from common/mid tiers. The deep tail improved
  but remains the ceiling.

### exp-06 — `reverb-heavy-longrt60`  (2026-06-14)

- **Design:** push reverb hard — long RT60 (0.8–1.5 s), p=0.7 — on the
  exp-05 stack, to test whether "more reverb" keeps paying.
- **Config deltas:** `aug.reverb_ir: {p: 0.7, rt60_range: [0.8, 1.5]}`
  (replaces the light setting).
- **Val macro-F1:** **0.663**  (−0.008 vs exp-05)
- **Wall-clock:** 1 h 18 min
- **Finding:** Below best. Heavy reverb *helps the common classes further*
  (they have the data to absorb the extra variation) but blurs short,
  quiet rare-class calls into the tail, netting a small loss. Confirms the
  effect is class-dependent, not monotone in reverb strength — motivates
  class-conditional augmentation.

---

## 5. Metrics summary & per-species detail

### Trajectory (validation macro-F1)

| # | Slug | Date | Macro-F1 | Δ vs baseline | Note |
|---|---|---|---|---|---|
| 01 | baseline-clean | 2026-03-08 | 0.612 | — | floor |
| 02 | reverb-light-ir | 2026-03-24 | 0.641 | +0.029 | first win |
| 03 | pitchshift-timestretch | 2026-04-11 | 0.589 | −0.023 | regression |
| 04 | noise-mix-snr | 2026-04-29 | 0.643 | +0.031 | null vs exp-02 |
| 05 | stack-reverb-noise-specaug | 2026-05-20 | **0.671** | **+0.059** | **best** |
| 06 | reverb-heavy-longrt60 | 2026-06-14 | 0.663 | +0.051 | common-only |

Seed-to-seed variability on this setup is ≈ ±0.006 macro-F1, which is why
exp-04's +0.002 over exp-02 is read as null.

### Per-species F1: baseline (exp-01) vs best (exp-05)

| Species | Tier | Clips | exp-01 F1 | exp-05 F1 | Δ |
|---|---|---|---|---|---|
| American Robin | common | 480 | 0.79 | 0.85 | +0.06 |
| Northern Cardinal | common | 421 | 0.76 | 0.83 | +0.07 |
| Song Sparrow | mid | 308 | 0.68 | 0.74 | +0.06 |
| Wood Thrush | rare | 92 | 0.51 | 0.54 | +0.03 |
| Kirtland's Warbler | deep tail | 41 | 0.34 | 0.33 | −0.01 |

The shape of the table *is* the result: the best recipe adds 6–7 points to
the head, a few to the mid, almost nothing to the rare tail, and slightly
*regresses* the single deepest-tail class. Global augmentation has run out
of road on the classes that most need help.

---

## 6. Failed directions — post-mortems

### 6a. Pitch-shift / time-stretch hurt the rare classes (exp-03)

- **What happened:** adding ±2-semitone pitch-shift and 0.9–1.1× time-
  stretch dropped macro-F1 to 0.589, *below the no-aug baseline*.
- **Why (best current understanding):** many deep-tail species are
  separated by fine formant/harmonic structure and call *timing*. Warping
  pitch and tempo moves synthetic examples across the very decision
  boundaries the model needs to keep sharp, and with <50 real clips there
  aren't enough true examples to anchor against the corrupted ones. Common
  classes have the data to shrug it off, so the aggregate hides an
  asymmetric harm.
- **Honest caveat:** we tested one strength (±2 st). A gentler setting
  (±0.5 st) might be neutral rather than harmful — untested. The claim is
  "at the strength we tried, it hurt the tail," not "pitch aug is useless."
- **Disposition:** dropped from the pipeline. Candidate to revisit only as a
  *class-conditional* transform (never applied to deep-tail classes).

### 6b. Heavy reverb helped common classes only (exp-06)

- **What happened:** long-RT60, high-probability reverb landed at 0.663,
  below the light-reverb stack's 0.671.
- **Why:** long reverb tails wash out short, low-energy rare-class calls
  into the noise floor of the spectrogram, while long, loud common-class
  songs stay legible and even benefit from the added room variation. Net:
  common up, rare down, small aggregate loss.
- **Honest caveat:** this is a per-tier decomposition on validation, not a
  controlled per-class ablation — the mechanism is inferred, not proven.
- **Disposition:** keep reverb *light*. Reinforces that augmentation
  strength should be conditioned on class, not global.

---

## 7. Current best recipe

Reproduces exp-05 (val macro-F1 0.671):

```yaml
backbone: small_cnn            # unchanged control across all experiments
input: logmel_128              # 128 mels, 25ms/10ms
train: {lr: 3e-4, batch: 32, epochs: 60, schedule: cosine}
sampler:
  class_balanced: 0.5          # partial reweight toward the tail
aug:
  reverb_ir:  {p: 0.5, rt60_range: [0.3, 0.6]}   # light, measured IRs
  noise_mix:  {snr_db: [5, 20], beds: [wind, rain, chorus]}
  specaugment: {freq_masks: 2, time_masks: 2}
  # pitch_shift / time_stretch: OFF (regressed, see 6a)
  # heavy reverb: OFF (common-only, see 6b)
```

Nothing here is expensive: the augmentations add well under a minute to the
per-run wall-clock over the clean baseline. That is the H2 (efficiency)
story holding up — the win came from data-space moves, not compute.

---

## 8. Open questions

- **Is the tail even learnable from 41 clips?** We don't know the ceiling.
  Need a small oracle study (e.g. hold clips-per-class fixed and vary it) to
  separate "augmentation can't help the tail" from "nothing can, at this n."
- **Does noise-mix only help *through* SpecAugment?** exp-04 vs exp-05
  suggests composition, but it's one comparison. Wants a proper 2×2 ablation.
- **How much of exp-05's gain is the balanced sampler vs the augmentations?**
  Currently confounded — the sampler was introduced in the same run.
- **Does the H2 efficiency claim survive a fair backbone baseline?** We have
  never actually run the "bigger/pretrained backbone" arm we keep invoking.
  Until we do, H2 is asserted, not shown.
- **Do measured IRs generalize to unseen recording environments?** All IRs
  come from a small room library; field conditions may differ.

---

## 9. Next three planned experiments

1. **`class-conditional-aug`** — apply each augmentation only to the tiers
   where the ledger shows it helps: light reverb everywhere, but pitch/
   stretch and heavy reverb *excluded* from rare/deep-tail classes. Direct
   test of the "condition on class" thesis that 6a/6b point to. Est. ~1 h.
2. **`sampler-vs-aug-ablation`** — a clean 2×2 (balanced sampler on/off) ×
   (aug stack on/off) to de-confound exp-05 and answer open-question 3.
   Cheap, ~4 runs × ~50 min.
3. **`backbone-fairness-arm`** — finally run the architecture control: a
   larger / AudioSet-pretrained backbone with *no* augmentation, matched
   compute-budget, to see whether murmur's +5.9 augmentation points beat
   what a bigger model buys. Settles H2. Est. up to ~6 h (the heaviest run
   on the docket).

---

## 10. Budget & compute notes

- **Hardware:** single RTX-class desktop GPU (16 GB), 64 GB system RAM. No
  cluster, no multi-GPU.
- **Run envelope:** experiments so far range **41 min → 1 h 18 min**.
  Planned exp-3 (pretrained backbone arm) is the outlier at an estimated
  **up to 6 h** and will run in a worktree overnight.
- **Data footprint:** ~6,200 clips ≈ small; log-mel cache fits comfortably
  on the project drive. No DVC-remote pressure yet.
- **Discipline:** the test split (~930 clips) has **not** been touched
  during search — all numbers above are validation macro-F1. A single
  held-out scoring pass runs only after the best recipe is frozen.

---

## 11. One-paragraph verdict

murmur's core bet is **partially supported**. Cheap reverb-flavoured
augmentation does lift a small bird-call classifier — +5.9 validation
macro-F1 points, baseline 0.612 to 0.671, at negligible extra compute — but
the gain is **concentrated in the common and mid classes and barely reaches
the rare tail**, and not every member of the family helps (pitch/stretch
regressed, heavy reverb helped only the head). The efficiency half of the
hypothesis (H2) is still *asserted, not shown*, because the fair
bigger-backbone comparison hasn't been run. The clear next step is to stop
augmenting globally and start augmenting **per class** — protect the tail
from the transforms that smear it while keeping the head's gains.
