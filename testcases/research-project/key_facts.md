---
slug: research-project
version: 1
---

# key_facts — murmur

Atomic, checkable claims (F1–F15) and top-level takeaways (T1–T4). Every
number here must match `source.md` exactly.

## Facts

- **F1 — Hypothesis.** murmur tests whether ultra-cheap audio augmentations
  inspired by natural reverberation improve bird-call classification on
  small datasets, and whether that lift beats spending the same compute on a
  bigger architecture.
- **F2 — Dataset size.** 6,200 clips across 34 species; 5-second mono clips
  at 32 kHz, features are 128-mel log-mel spectrograms.
- **F3 — Split.** 70/15/15 train/val/test, stratified by species and
  seeded; ~930 validation clips and ~930 held-out test clips.
- **F4 — Imbalance.** Long-tailed: top class (American Robin) has 480 clips;
  11 species have fewer than 80 clips; 5 species have fewer than 45; median
  ≈ 120 clips/class. The 8 most common species are ~52% of the data.
- **F5 — Metric.** Primary metric is validation macro-F1 (weights the tail
  equally with the head). Seed-to-seed variability ≈ ±0.006.
- **F6 — exp-01 baseline-clean (2026-03-08).** No augmentation. Val
  macro-F1 = 0.612. The floor.
- **F7 — exp-02 reverb-light-ir (2026-03-24).** Light impulse-response
  reverb (RT60 0.3–0.6 s, p=0.5). Val macro-F1 = 0.641 (+0.029). First win.
- **F8 — exp-03 pitchshift-timestretch (2026-04-11).** Added ±2-semitone
  pitch-shift and 0.9–1.1× time-stretch on top of reverb. Val macro-F1 =
  0.589 — a regression, below the 0.612 baseline.
- **F9 — exp-04 noise-mix-snr (2026-04-29).** SNR-controlled background-
  noise mixing (5–20 dB) instead of pitch/stretch. Val macro-F1 = 0.643,
  only +0.002 over exp-02 — a null result (inside noise).
- **F10 — exp-05 stack-reverb-noise-specaug (2026-05-20).** Full stack:
  light reverb + noise mix + SpecAugment + partial class-balanced sampler.
  Val macro-F1 = 0.671 — the current best, +0.059 over baseline.
- **F11 — exp-06 reverb-heavy-longrt60 (2026-06-14).** Long-RT60 (0.8–1.5 s,
  p=0.7) reverb on the exp-05 stack. Val macro-F1 = 0.663, below best;
  helped common classes, hurt rare ones.
- **F12 — The regression and its cause.** exp-03 regressed because pitch/
  time warping smears the fine spectral and timing cues rare classes depend
  on; with <50 real clips there aren't enough true examples to anchor
  against the corrupted synthetic ones. Common classes were unaffected.
- **F13 — The null result.** exp-04's noise mixing alone was +0.002 over
  reverb-only — inside the ±0.006 seed noise — so it is read as null on its
  own; it was kept only because it composes with SpecAugment in exp-05.
- **F14 — Best config.** Small CNN (unchanged control) + log-mel-128 +
  light reverb (p=0.5, RT60 0.3–0.6 s) + noise mix (5–20 dB) + SpecAugment
  (2 freq / 2 time masks) + class_balanced sampler at 0.5; pitch/stretch and
  heavy reverb OFF.
- **F15 — Where the gain lands.** Per-species, exp-01→exp-05: American Robin
  0.79→0.85, Northern Cardinal 0.76→0.83, Song Sparrow 0.68→0.74, Wood
  Thrush 0.51→0.54, Kirtland's Warbler 0.34→0.33 (−0.01). ~4.5 of the 5.9
  points come from common/mid tiers; the deep tail barely moves and the
  deepest class slightly regresses.

## Takeaways

- **T1 — Partially supported.** The hypothesis holds but weakly: +5.9
  validation macro-F1 points (0.612 → 0.671) at negligible extra compute,
  but concentrated in the common classes, not the rare tail.
- **T2 — One augmentation actively hurt.** Pitch-shift/time-stretch
  regressed the model below baseline (0.589) by smearing rare-species cues —
  the family is not uniformly helpful.
- **T3 — Best result is a stack, and reverb strength is class-dependent.**
  The win comes from composing light reverb + noise + SpecAugment; more
  reverb (heavy RT60) helped only the head and lost overall.
- **T4 — Next: class-conditional augmentation.** Stop augmenting globally —
  apply helpful transforms per class and shield the rare tail from the ones
  that smear it; also finally run the fair bigger-backbone arm to test the
  still-unproven efficiency claim.
