---
name: optimization-loop-author
description: >
  Authors a single Phase 7 experimentation cycle — hypothesize,
  design, build, run, analyze, decide, iterate. Produces an
  experiment plan + analysis with named primary metric, guardrail
  metrics, sample size, pre-registered analysis plan, and the
  decision (win / loss / inconclusive). Writes to
  docs/07-postlaunch/experiments/<exp-id>.md (SOP §10.3.1). Use
  per experiment from the optimization backlog. Do NOT use for:
  the prioritized backlog itself (use optimization-backlog-author
  Tier 1 — that is the queue; this is per-experiment); the
  diagnostic sweep that seeds the backlog (use diagnostic-sweep-
  author Tier 2); the win-regression synthesis (use
  win-regression-report-author Tier 2); recurring monthly /
  quarterly reports (use the corresponding cadence atoms).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [weekly]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. Modeled on the
            user-invocable optimization-loop skill but conformed to
            meta-pipeline frontmatter / required-section discipline.
---

# optimization-loop-author

Phase 7 — produce + execute one experimentation cycle.

## When to Use

- Phase 7 weeks 8+; the optimization backlog has a top item
  ready to enter testing.
- A high-confidence discovery-tick finding is ready to test
  immediately (skip the backlog queue with an explicit fast-
  track).
- A regression has surfaced and a counter-experiment is being
  scoped (test whether reverting a prior change recovers
  the metric).
- A monthly experimentation cycle is committed; today is the
  next experiment kickoff.

## When NOT to Use

- The prioritized backlog itself —
  `optimization-backlog-author` (Tier 1). The backlog is the
  queue; this skill is per-experiment.
- The diagnostic sweep — `diagnostic-sweep-author` (Tier 2).
  Sweep finds problems; loop tests solutions.
- Win-regression synthesis — `win-regression-report-author`
  (Tier 2). Win-regression looks across many metrics at T+8;
  loop is per-experiment.
- Recurring reports (monthly / quarterly / annual) —
  separate cadence atoms.
- An A/B test without sample-size discipline — refuse;
  per SOP §10.6 anti-pattern "A/B test theater" — without
  sample size + pre-registered analysis, the test is
  decoration.
- A discovery activity (interview, survey) — that's
  upstream of the backlog; doesn't go through the loop.

## Capabilities Owned

- Walk the **7-step experimentation loop** per SOP §10.3.1:

  1. **Hypothesize** — *"We believe <change> will <effect>
     for <users> because <evidence>. We will know we're
     right if <signal> within <time>. We are wrong if
     <counter-signal>."*
  2. **Design** — experiment type (A/B / multivariate /
     holdout / before-after with adjustment), variants,
     **sample size calculation**, primary metric, guardrail
     metrics (≥2), **pre-registered analysis plan**.
  3. **Build** — variants implemented behind feature flag,
     allocation logic, tracking events configured.
  4. **Run** — begin allocation, monitor for trip wires
     (rollback if critical metric tanks), run for
     pre-determined duration (typically 2-4 weeks).
     **Don't peek at significance early** (multiple-
     comparison hell per §10.6 anti-pattern).
  5. **Analyze** — reach pre-determined sample size,
     calculate lift + confidence interval, investigate
     guardrail metrics, investigate per-segment effects.
  6. **Decide** — Win → ship to 100% + remove flag once
     stable. Loss → revert + capture learning.
     Inconclusive → extend, redesign, or document and
     move on.
  7. **Iterate** — insights feed the next hypothesis.

- Capture metadata:
  - **Stable experiment ID** (`EXP-NNNN`).
  - **Backlog item** the experiment derives from (or fast-
    track justification).
  - **Owner** — PdM or CRO Lead accountable.
  - **Start / end dates** — pre-determined; not adjusted
    based on interim results.
  - **Sample size + power calculation** — explicit, with
    minimum detectable effect.
- Document **decision rationale** at conclusion — even
  "inconclusive" is logged with what would change before
  retest.
- Refuse **peeking** (analyzing before sample size reached
  unless trip-wire fires) per §10.6.
- Refuse **single-metric optimization** without guardrails
  per §10.6 anti-pattern.
- Cite **backlog item** + **target metric source** by
  stable ID.
- Write to `docs/07-postlaunch/experiments/<EXP-NNNN>.md`.

## Handoffs to Other Skills

- **From `optimization-backlog-author`** (Tier 1) —
  backlog item is the input.
- **From `discovery-tick-author`** (site-design family) —
  fast-track items skip the backlog queue.
- **From `baseline-report-author`** (site-build family) —
  regressions identified there feed counter-experiments.
- **To `optimization-backlog-author`** — at decision,
  the item is removed from active and the next is
  promoted; learnings update related items' confidence
  scores.
- **To `win-regression-report-author`** (Tier 2) — at
  T+8, ongoing experiments contribute to the synthesis.
- **To `monthly-stakeholder-report-author`** (Tier 2) —
  monthly memo summarizes experiments decided this month.
- **To `quarterly-business-review-author`** (Tier 2) —
  experiment portfolio + cumulative impact featured.
- **From the user-invocable `optimization-loop`** — peer
  skill producing the same artifact via a different
  procedure.

## Edge Cases

- **Sample size too small to reach significance.**
  Don't ship a "directional" win; mark inconclusive.
  Either extend (if budget allows) or document the
  failure to power.
- **Trip-wire fires** (critical metric tanks). Roll back
  the experiment immediately; document as terminated;
  capture the learning.
- **Concurrent experiments interact** (per §10.3.2
  portfolio management). Mutually-exclusive groups when
  needed; document interaction risk in the experiment plan.
- **Stakeholder pressures peeking.** Hold the line; cite
  §10.6. Multiple-comparisons inflation will produce
  false positives.
- **Win on primary metric, regression on guardrail.**
  Don't ship blindly. Investigate; either drop the change
  or accept the trade-off with explicit Sponsor sign-off.
- **Inconclusive result** repeatedly on the same
  hypothesis. Document; move on; don't keep retrying with
  marginal tweaks (§10.6 anti-pattern "test theater").

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §10.3.1
(experimentation loop) + §10.3.2 (portfolio management) +
§10.6 (anti-patterns). The user-invocable `optimization-loop`
is a peer skill producing the same artifact via a different
procedure.

## Self-Audit

Before declaring an experiment cycle complete, confirm:
- All 7 loop steps documented (hypothesize → iterate).
- Hypothesis in standard form (signal + counter-signal).
- Sample size calculation explicit.
- Primary metric + ≥2 guardrail metrics named.
- Pre-registered analysis plan.
- Decision rationale at conclusion (win / loss /
  inconclusive).
- No peeking before sample size (or trip-wire
  documented).
- Cross-references to backlog item + target metric.
