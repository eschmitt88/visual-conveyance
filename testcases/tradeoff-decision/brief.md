---
slug: tradeoff-decision
version: 1
audience: >
  A tech lead at a mid-size e-commerce company who must make — and then
  defend — an infrastructure choice to two very different rooms: their own
  engineers (who care about benchmarks, ops burden, and lock-in) and a
  budget-conscious engineering director (who cares about $/month now, the
  cost trajectory, and headcount commitments). Technically fluent; short on
  time; will be challenged on "why not the cheaper one?"
reading_goal: >
  In a couple of minutes, hold the whole tradeoff space in their head: four
  options, which two fail the must-haves and exactly why, how the surviving
  two trade cost trajectory against operational burden, where the cost
  ranking inverts as the corpus grows, and — critically — the *conditional*
  recommendation: which option is primary, what concrete trigger flips it
  to the fallback, and when that trigger gets checked. They should be able
  to answer "what would change your mind?" without re-reading.
required_takeaways:
  - >
    There is no dominant option. The two must-have survivors (Quiver and
    Hearth) trade directly against each other — Hearth wins the cost
    trajectory and lock-in, Quiver wins operational simplicity — and the
    other two options are eliminated by must-have failures, not by taste.
  - >
    The recommendation is genuinely conditional: Hearth (self-hosted) is
    primary IF the approved platform-infra hire starts by 2026-10-01 and a
    ≥4-engineer on-call rotation is committed; otherwise it flips to Quiver
    (managed SaaS) with an explicit, budgeted exit plan.
  - >
    The cost ranking inverts with scale: Quiver is the cheapest option at
    1M vectors ($180/mo) and the most expensive at 10M and 100M ($1,900 and
    $23,000/mo vs Hearth's $1,400 and $6,800). On infra alone the crossover
    (~3M vectors) is already behind us; counting ops labor it sits around
    30M vectors, roughly 2029 at current growth.
  - >
    Raw benchmark performance did not decide this. The fastest,
    highest-recall option (Braid, 12 ms p95, 0.98 recall@10) is disqualified
    because its filtered-search recall collapses to 0.71, and the decision
    between the survivors hinges on cost and operations, not speed.
---

# Reading brief: choosing a vector-search engine

This is the fixed source dossier for an internal engineering decision brief
at **Fernwick**, a fictional e-commerce marketplace, choosing the vector
database behind its semantic product-search feature. Everything a
presentation method needs to convey lives in `source.md`; the atomic,
checkable claims live in `key_facts.md`.

This test case is a **multi-criteria decision structure**, not a narrative
or a tutorial. The hard part is conveying relationships, not facts:

- a 4-option × ~9-criteria comparison matrix that must stay scannable;
- must-have **eliminations** (two options fail hard requirements) as
  distinct from soft tradeoffs between the survivors;
- a **cost crossover** — the cheapest option at small scale becomes the
  most expensive at large scale, with the flip point relative to the
  company's own growth curve;
- a **conditional recommendation** with explicit triggers and dates — an
  IF/THEN, not a winner.

A good presentation makes the elimination logic and the condition visible
at a glance, and lets the reader defend the decision under the two obvious
attacks: "the SaaS is cheaper" (only below ~3M vectors on infra, ~30M
counting labor) and "the library benchmarks best" (it fails a must-have).
Presenting this as a flat feature list, or as an unconditional "we chose
X", is a failure even if every number is reproduced correctly.
