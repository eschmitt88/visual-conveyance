---
slug: diffusion-variants
version: 1
---

# Key facts: diffusion-variants

Ground truth for evaluators. Held out from generators. Each fact is atomic
and checkable against `source.md`.

## Facts

- **F1.** A diffusion model pairs a *fixed* forward process that gradually
  adds Gaussian noise to images with a *learned* reverse process that removes
  noise one small step at a time; generation runs the learned reverse process
  starting from pure random noise.
- **F2.** The forward process in the original DDPM formulation uses on the
  order of **1000 steps**, governed by a predefined noise schedule; by the
  final step the image is statistically indistinguishable from pure Gaussian
  noise.
- **F3.** The network's inputs are the noisy image and the timestep t (plus a
  prompt representation in text-to-image models); its output target is one of
  three interconvertible parameterizations: the added **noise (ε)**, the
  **score** (gradient of the log-density of noisy images), or a **velocity**
  (a defined mixture of image and noise).
- **F4.** Training draws a real image and a random timestep, noises the image
  in one closed-form shot, and penalizes the network's noise prediction with
  a simple **mean-squared error** — a stable objective with no adversarial
  game, unlike GANs.
- **F5.** Naive DDPM sampling requires ~1000 *sequential* full network
  evaluations per image (steps cannot be parallelized), which is why the
  original method was slow and why most variants target sampling cost.
- **F6.** **DDIM** uses the *same trained network* with a different,
  **deterministic** sampler that tolerates larger jumps, reducing sampling to
  a typical practical range of **20-50 steps** with modest quality loss.
- **F7.** DDIM's determinism makes noise → image a well-defined function,
  enabling inversion of images back to their noise and smooth interpolation
  between images.
- **F8.** In the score-based/SDE view, forward noising is a stochastic
  differential equation and sampling can follow either a reverse-time SDE
  (stochastic) or a deterministic **probability flow ODE**; DDIM is
  essentially a discretization of that ODE, and purpose-built ODE solvers
  (e.g. DPM-Solver) reach good quality in **~10-20 steps** without
  retraining.
- **F9.** **Latent diffusion** runs the entire diffusion process in the
  compressed latent space of a separately trained **VAE**, whose decoder
  converts the final clean latent to a full-resolution image in a single
  pass.
- **F10.** Representative latent-diffusion numbers: a 512×512×3 image
  (786,432 values) is encoded 8×-downsampled to a **64×64×4 latent (16,384
  values), ≈ 48× fewer values**, making every denoising step correspondingly
  cheaper — the change that made Stable-Diffusion-class models feasible on
  consumer GPUs.
- **F11.** **Classifier-free guidance** trains one network with the prompt
  randomly dropped (~10-20% of training examples), then at sampling runs the
  network twice per step (with and without the prompt) and *extrapolates*:
  guided = unconditional + s × (conditional − unconditional). This doubles
  network evaluations per step.
- **F12.** The guidance scale trades diversity for prompt adherence: s = 1
  means no guidance, **s ≈ 7.5 is a common default**, and pushing s much
  higher (roughly >12-15 in classic Stable Diffusion) yields oversaturation
  and artifacts.
- **F13.** **Distillation** (progressive distillation, adversarial
  distillation) and **consistency models** retrain a network to take big
  jumps — consistency models map any noisy point on a trajectory directly to
  its clean endpoint — enabling **1-4 step** generation at some cost in
  quality and diversity relative to the many-step teacher.
- **F14.** **Flow matching / rectified flow** trains the network to predict a
  velocity field transporting noise to data along (in rectified flow)
  **straight-line paths**, needing fewer ODE steps; it is mathematically a
  close sibling/generalization of diffusion, not a rival mechanism, and is
  the training formulation of **Stable Diffusion 3 and Flux-class models**.
- **F15.** Generated images are not retrieved or collaged from a database and
  text-to-image generation does not start from any real photo: no training
  images are stored in the weights (rare memorization of heavily duplicated
  training images is a documented exception, not the mechanism), and only
  explicit image-to-image / inpainting modes start from a user-supplied
  image.

## Critical takeaways

What a ~10-second glance at a presentation must convey:

- **T1.** Generation = the learned reversal of gradual noising — start from
  pure random noise, denoise step by step until an image emerges.
- **T2.** The variants mainly attack sampling cost: ~1000 steps (DDPM) →
  20-50 (DDIM) → 10-20 (ODE solvers) → 1-4 (distillation/consistency), with
  quality tradeoffs shrinking the step count.
- **T3.** Latent diffusion = do the same thing in a VAE-compressed space
  (~48× fewer values) — the change that made it run on consumer hardware.
- **T4.** Guidance steers generation toward the prompt by exaggerating the
  difference between prompted and unprompted predictions; its scale trades
  diversity for prompt-fit.
