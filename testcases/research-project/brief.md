---
slug: research-project
version: 1
audience: >
  A technical friend and potential collaborator — comfortable with ML and
  small-data training, but has never seen the "murmur" project. They want a
  fast, honest read on the state of the work: what the bet is, what has been
  tried, what happened, and whether it's actually working.
reading_goal: >
  In a couple of minutes, understand murmur's hypothesis, the shape of the
  experiment ledger (baseline through current best), the one regression and
  the one null result, the current best recipe, and the honest verdict —
  then know what the next three experiments are and whether it's worth
  collaborating on.
required_takeaways:
  - >
    The hypothesis is partially supported, not cleanly confirmed: the best
    recipe lifts validation macro-F1 from 0.612 to 0.671 (+5.9 points), but
    the gain is concentrated in common species and barely touches the rare
    tail.
  - >
    Not every "natural-reverb-inspired" augmentation helped. Pitch/time
    stretch actively regressed the model (down to 0.589) by smearing the
    rare classes, and SNR-controlled background-noise mixing was a null
    result (+0.002 over reverb-only, inside noise).
  - >
    The current best recipe is a stack — light impulse-response reverb +
    background-noise mixing + SpecAugment — not any single augmentation;
    heavy reverb (long RT60) helped common classes only and came in below
    the stack.
  - >
    The clear next move is class-conditional augmentation: apply the helpful
    transforms only where they help and protect the rare tail, since global
    augmentation has plateaued on the common classes.
---

# Reading brief: the "murmur" project

This is the fixed source dossier for a personal ML research project called
**murmur**. Everything a presentation method needs to convey lives in
`source.md`; the atomic, checkable claims live in `key_facts.md`.

The audience is a technical collaborator seeing the project cold. They are
not looking for a tutorial on bioacoustics or augmentation — they want the
research state: the bet, the ledger, the honest verdict, and the plan. A
good presentation of this material should make the metric trajectory legible
(baseline → best, with the dip and the flat one visible), and should not
oversell: the headline is "partially works, and here's exactly where it
doesn't."
