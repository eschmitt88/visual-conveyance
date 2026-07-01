---
slug: diffusion-variants
version: 1
audience: >
  A technically literate professional with no machine-learning background —
  think a mechanical engineer or a physicist-turned-manager. Comfortable with
  calculus-level math ideas (gradients, differential equations, compression
  ratios) when they are explained, but has never trained a neural network and
  does not know ML jargon.
reading_goal: >
  Genuinely understand how image-generation diffusion models work and how the
  main variants differ — well enough to explain the core mechanism to a
  colleague and to make sense of terms like "DDIM steps", "latent diffusion",
  "CFG scale", and "flow matching" when they appear in tool settings or
  articles.
---

# Brief: Diffusion models and their variants

Explain, to a smart non-ML professional, how modern image-generation
diffusion models work and why the major variants exist. The reader is not
trying to implement anything; they want a correct mental model.

## What the reader should come away with

1. **The core mechanism.** Generation is the learned reversal of a gradual
   noising process: a fixed forward process destroys images into noise, a
   trained network runs that destruction backwards, and every generated image
   starts from pure random noise — not from any existing photo.

2. **Why sampling is slow, and what fixes it.** Naive (DDPM) sampling takes
   on the order of a thousand sequential network evaluations. Most of the
   variant zoo — DDIM, ODE solvers, distillation, consistency models,
   rectified flow — exists to cut that cost, from ~1000 steps down to as few
   as 1-4, with characteristic quality tradeoffs at each tier.

3. **What latent diffusion changed.** Running diffusion in a VAE-compressed
   latent space (e.g. 64×64×4 instead of 512×512×3 — roughly 48× fewer
   values) is what made Stable-Diffusion-class models cheap enough for
   consumer GPUs, at the cost of a slight compression bottleneck.

4. **How guidance steers generation.** Classifier-free guidance blends two
   predictions (with and without the prompt) and exaggerates their
   difference; the guidance scale (~7.5 is a common default) trades sample
   diversity and naturalness for prompt adherence.

## Tone and scope notes

- Every claim must stay standard-textbook-true as of 2025; no hand-waving
  that becomes technically false.
- Use concrete representative numbers (step counts, dimensions, guidance
  scales) rather than vague qualifiers.
- Debunking the common misconceptions ("it collages images from a
  database", "it cleans up a real photo") is in scope and valuable.
