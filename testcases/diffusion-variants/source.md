---
slug: diffusion-variants
version: 1
title: "Diffusion models and their variants: how modern image generators work"
---

# Diffusion models and their variants

Modern image generators — Stable Diffusion, Midjourney-class systems, DALL·E 3,
Flux — are built on *diffusion models*. The idea is simple to state and easy to
get wrong, so this explainer builds it up carefully: the core mechanism first,
then the family of variants, which mostly exist to make one thing cheaper —
sampling.

## 1. The core idea: destroy carefully, learn to rebuild

A diffusion model is defined by two processes that run in opposite directions.

**The forward (noising) process** is fixed and involves no learning. Take a
real image and add a small amount of Gaussian noise. Repeat, over and over —
in the original DDPM formulation, about **T = 1000 steps** — following a
predefined *noise schedule* that controls how much noise is added at each
step. Early steps barely change the image; by the final step essentially all
structure is gone, and the result is statistically indistinguishable from
pure Gaussian noise (like analog TV static). Crucially, this process is
gradual: at step 200 the image is slightly grainy, at step 600 only coarse
shapes survive, at step 1000 nothing survives.

**The reverse (denoising) process** is what gets learned. A neural network is
trained to undo one small step of the forward process: given a noisy image
and the step number *t* (the "timestep"), estimate what a slightly less noisy
version looks like. Removing *all* the noise in one jump would be nearly
impossible — there are countless clean images consistent with a very noisy
input — but removing *a little* noise is a tractable prediction problem, and
chaining many small denoising steps together is what makes the whole thing
work.

**Generation** then works like this: sample a fresh image of pure random
noise, and apply the learned denoising step repeatedly — t = 1000, 999, 998,
… down to 0. Structure emerges gradually: first blobs of tone, then coarse
layout, then object shapes, and finally fine texture. The output is a new
image that never existed anywhere; the only inputs were random numbers and
the network's learned weights.

Two points worth stressing, because they are the most commonly misunderstood:

- Generation **starts from pure noise**, not from a photograph. The model is
  not "cleaning up" or editing any real image (except in specialized
  image-to-image modes where a user deliberately supplies one).
- The training images are **not stored** in the model. A network of a few
  billion parameters trained on billions of images cannot and does not keep
  copies; what it stores is a statistical model of what plausible images look
  like at every noise level.

## 2. What the network actually predicts

The sentence "the network denoises the image" hides a design choice: what
exactly is the network's output? Three parameterizations are common, and they
are mathematically interchangeable — simple algebra converts one to another —
but they differ in training stability and convention:

- **Noise prediction (ε-prediction).** The network looks at the noisy image
  and predicts *the noise that was added*. Subtracting (a scaled version of)
  that prediction recovers an estimate of the clean image. This is the
  original DDPM choice and remains the most common.
- **Score prediction.** The network predicts the *score* — the gradient of
  the log-probability density of noisy images, i.e. the direction in pixel
  space that makes the image more probable. The predicted noise is just a
  negatively scaled score, so ε-prediction and score prediction are two
  descriptions of the same quantity.
- **Velocity prediction (v-prediction).** The network predicts a defined
  mixture of the image and the noise ("velocity"). Introduced with
  progressive distillation, it is numerically better behaved at very high
  noise levels and is used by several later models.

Whichever target is used, the network sees two inputs — the noisy image and
the timestep *t* — plus, in text-to-image models, a representation of the
prompt (Section 7). Architecturally the network is typically a **U-Net**
(a convolutional encoder-decoder with skip connections) in the
Stable-Diffusion-1/2 generation, or a **diffusion transformer (DiT)** in
newer systems like SD3 and Flux.

## 3. Training: a denoising exercise repeated billions of times

Training is remarkably simple compared to older generative approaches:

1. Draw a real image from the training set.
2. Draw a random timestep *t* (anywhere from light to total noise).
3. Add the corresponding amount of noise in one shot — a closed-form formula
   gives the correctly noised image for any *t* directly, without simulating
   the intermediate steps.
4. Ask the network to predict the noise that was added; penalize it with a
   simple **mean-squared error** between predicted and actual noise.

That is the entire objective (formally, it is a weighted variational bound on
the data likelihood, but the practical loss really is "guess the noise, MSE").
Each training example exercises one random noise level, so over billions of
examples the network learns denoising at *every* level: at high noise it
learns global composition ("where could a horizon plausibly go?"), at low
noise it learns fine texture. This objective is stable and scalable — no
adversarial game as in GANs, where a generator and discriminator must be kept
in delicate balance — and that stability is a big reason diffusion displaced
GANs for large-scale image generation.

## 4. Why sampling is slow — the original sin

Training looks at one noise level at a time, but *sampling* must walk the
whole chain. Naive DDPM sampling runs the full network once per step —
**~1000 sequential forward passes** per image. The steps cannot be
parallelized (each depends on the previous one), so even on a fast GPU a
single image took the better part of a minute in 2020. Nearly every major
variant since exists to attack this cost. It helps to read the rest of this
document as one long answer to the question: *how do we take fewer steps?*

## 5. DDIM: same model, fewer and deterministic steps

DDIM (Denoising Diffusion Implicit Models, 2020) was the first big win. Two
observations:

- The DDPM sampler injects fresh randomness at every step, but one can define
  an alternative sampler — using the *same trained network, unchanged* — that
  is **deterministic**: fix the initial noise and you get exactly the same
  image every time.
- This deterministic sampler tolerates much larger jumps. Instead of visiting
  all 1000 timesteps, visit a subsequence — **20-50 steps is the typical
  practical range** — with only a modest quality loss.

Determinism has side benefits beyond speed: the mapping from initial noise to
final image becomes a well-defined function, so you can *invert* a generated
image back to its noise (useful for editing) and smoothly interpolate between
two images by interpolating their noise. When an image tool exposes a
"steps" slider defaulting to something like 30, it is exposing exactly this
tradeoff.

## 6. The score-based / SDE view: one lens that unifies everything

In 2021, a parallel line of work (score-based generative models) was shown to
be the *same thing* as diffusion in a continuous-time limit, and the merged
view is the field's standard mental model today:

- The forward noising process is a **stochastic differential equation
  (SDE)** — a continuous random drift of images toward noise.
- Reversing it requires exactly one learned quantity: the **score** (the
  gradient of log-density from Section 2). With the score in hand there are
  two ways back: a reverse-time SDE (random, like DDPM) or a **probability
  flow ODE** — an ordinary differential equation that is fully deterministic
  and produces the same distribution of images. DDIM is essentially a
  discretization of this ODE.

Why a non-ML reader should care: once sampling is "just solving an ODE," the
entire toolbox of numerical ODE solvers applies. Purpose-built higher-order
solvers (DPM-Solver and successors) get good samples in **~10-20 steps** with
no retraining. This view also explains, in one picture, why so many variants
coexist: they are different discretizations, different paths, or different
parameterizations of the same underlying object.

## 7. Latent diffusion: do it in compressed space

Everything so far operates directly on pixels, and pixels are expensive: a
512×512 RGB image is 512 × 512 × 3 = **786,432 numbers**, and the denoising
network must process all of them at every one of dozens-to-hundreds of steps.

**Latent diffusion** (2022) adds a compression stage. A separately trained
**variational autoencoder (VAE)** — an encoder-decoder pair — maps each image
into a much smaller *latent* representation and back. In Stable Diffusion the
encoder downsamples 8× in each spatial dimension: a 512×512×3 image becomes a
**64×64 latent with 4 channels = 16,384 numbers — roughly 48× fewer values**.
The compression is perceptual, not lossless: the VAE is trained so the
reconstruction looks essentially identical, discarding imperceptible detail.

The diffusion process — forward noising, training, and sampling exactly as
described above — then runs entirely in this latent space. Generation becomes:

1. Sample random noise *in latent space* (e.g. 64×64×4).
2. Run the learned denoising loop there (every step ~48× cheaper than in
   pixel space).
3. Decode the final clean latent through the VAE decoder — one single pass —
   to obtain the full-resolution image.

This is the change that made Stable-Diffusion-class models run on consumer
GPUs and is why the model is called "latent." The costs are minor: a slight
quality ceiling from the compression bottleneck (historically visible in fine
text and small faces, much improved in newer VAEs), and one extra decode pass.
Note the division of labor: the VAE is only a compressor/decompressor — the
diffusion model in the middle is what generates.

## 8. Classifier-free guidance: steering with the prompt

Text conditioning gets the prompt *into* the network (as embeddings from a
text encoder such as CLIP or T5, attended to at each denoising step), but
conditioning alone tends to produce images that only loosely follow the
prompt. **Classifier-free guidance (CFG)** is the fix used by essentially
every modern text-to-image system:

- **At training time**, the prompt is randomly dropped (replaced by an empty
  prompt) for a small fraction of examples — typically **~10-20%** — so one
  network learns both prompt-conditioned and unconditional denoising.
- **At sampling time**, every step runs the network **twice**: once with the
  prompt, once without. The two predictions are blended by *extrapolation*:

  > guided = unconditional + s × (conditional − unconditional)

  The difference between the two predictions is "the direction the prompt
  pulls," and the **guidance scale s** exaggerates it. s = 1 means no
  guidance; **s ≈ 7.5 is a common default** in Stable-Diffusion-class models.

The tradeoff is real and visible: higher s gives stronger prompt adherence
and cleaner-looking, more "typical" images, but reduces diversity and — when
pushed too far (roughly s > 12-15 in classic SD) — produces oversaturated
colors and burned-in artifacts. CFG also **doubles the network evaluations
per step**, which matters when counting sampling cost.

## 9. Distillation and consistency models: 1-4 steps

Fast samplers plateau around 10-20 steps. Going lower requires *training* a
model to take big jumps rather than cleverly scheduling small ones:

- **Progressive distillation** trains a student network to match, in one
  step, what a teacher does in two — then repeats, halving the step count
  each round (1000 → 500 → … → 4).
- **Consistency models** (2023) train the network so that *any* noisy point
  on a given trajectory maps directly to the same clean endpoint. That
  self-consistency property allows **1-step generation**, with 2-4 steps as a
  refinement option. Latent consistency models (LCMs) apply this to
  Stable-Diffusion-class latents, giving ~4-step generation.
- **Adversarial distillation** (SDXL-Turbo-style) adds a GAN-like critic to
  sharpen few-step outputs.

The tradeoff: distilled few-step models trade some quality and diversity for
speed — outputs tend to be slightly softer or less varied than the 20-50-step
teacher — and the extra training stage adds pipeline complexity. This is the
technology behind "real-time" generation demos that redraw as you type.

## 10. Flow matching and rectified flow: straighter paths

The newest mainstream reformulation asks: why follow the curved paths that
Gaussian noising dictates at all? **Flow matching** trains a network to
predict a **velocity field** that transports noise to data along prescribed
paths; **rectified flow** chooses the simplest possible ones — **straight
lines**. A training point is just a linear blend of an image and a noise
sample, and the regression target is the constant velocity (their
difference) along that line.

Why this matters: solving an ODE along nearly straight paths needs far fewer
steps than along curved ones, and the formulation drops the diffusion-specific
scaffolding (noise schedules, timestep-dependent scalings) for a cleaner
recipe. Mathematically it is a close sibling of diffusion — with Gaussian
paths, flow matching recovers diffusion's probability-flow ODE, and the score
/ noise / velocity quantities remain interconvertible — so it is best read as
a *reframing that generalizes*, not a rival mechanism. **Stable Diffusion 3
and Flux-class models are trained this way**, combined with transformer
backbones and latent-space operation.

## 11. Variants at a glance: steps vs. quality

| Family | Typical steps | Character |
| --- | --- | --- |
| DDPM (ancestral) | ~1000 | Original formulation; excellent quality; impractically slow |
| DDIM | 20-50 | Same trained model; deterministic; the everyday workhorse range |
| ODE solvers (DPM-Solver++ etc.) | 10-20 | Better numerics, no retraining; near-DDIM quality |
| Rectified flow / flow matching | ~20-30 (fewer viable) | Retrained objective; straight paths; SD3/Flux generation |
| Distilled / consistency / LCM | 1-4 | Retrained for big jumps; fastest; mild quality & diversity cost |

Rules of thumb: below ~10 steps, undistilled models degrade visibly; above
~50, returns diminish rapidly. "More steps" is refinement of the *same*
trajectory, not a search over more images — and remember CFG doubles the
per-step cost.

## 12. Common misconceptions

- **"It searches a database and collages existing images."** False. No
  training images are stored or consulted at generation time; the model's
  weights encode statistics, not copies, and sampling starts from random
  noise. (Nuance: rare near-duplication of training images *has* been
  demonstrated, essentially for images repeated many times in the training
  set — a real but exceptional memorization failure mode, not the mechanism.)
- **"It denoises a real photo."** False for text-to-image generation, which
  starts from pure synthetic noise. Image-to-image and inpainting modes *do*
  start from a user-supplied image — by partially noising it and denoising
  back — but that is an explicit variant, not the default mechanism.
- **"The VAE is the generator."** No; the VAE only compresses and
  decompresses. The diffusion model operating in latent space does the
  generating.
- **"More steps always means better images."** Only up to a point; see
  Section 11. Past the workhorse range, extra steps refine imperceptibly —
  and for distilled models, the intended step count is part of the design.
- **"The guidance scale is a 'quality' knob."** It is an
  adherence-vs-diversity knob with an artifact regime at high values;
  "better" depends on what you want.
- **"Diffusion, DDIM, score-based models, and flow matching are competing
  technologies."** They are one framework: identical or interconvertible
  training targets, different samplers, paths, and parameterizations.

## 13. Glossary

- **Timestep (t):** position along the noising process; high t = more noise.
- **Noise schedule:** the predefined recipe for how much noise each forward
  step adds.
- **ε / score / velocity:** three interconvertible choices of network output.
- **Sampler:** the algorithm that turns many network predictions into an
  image (DDPM, DDIM, DPM-Solver, …).
- **Latent space:** the VAE-compressed representation where latent diffusion
  operates (e.g. 64×64×4 for a 512×512 image).
- **CFG scale (s):** strength of classifier-free guidance extrapolation.
- **Distillation:** training a fast student model to imitate a slow teacher.
- **NFE (number of function evaluations):** how many times the network runs
  during sampling — the honest cost metric (CFG doubles it per step).
