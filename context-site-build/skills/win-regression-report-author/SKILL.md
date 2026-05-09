---
name: win-regression-report-author
description: >
  Authors the Win/Regression Report at T+8 weeks — wins (metrics
  improved vs pre-launch baseline), regressions (metrics declined,
  with attribution), surprises (patterns nobody predicted), and
  stable metrics (didn't move; success or null result). Output
  at docs/07-postlaunch/win-regression-<YYYY-MM-DD>.md (SOP
  §10.2.4). Use at T+8 paired with baseline-report-author. Do
  NOT use for: the T+8 baseline report (use baseline-report-
  author in site-build family — baseline is the snapshot; this
  is the improvement-vs-decline analysis); diagnostic sweep (use
  diagnostic-sweep-author — sweep finds problems; this reports
  them to sponsor); 30-day stabilization report (use
  stabilization-report-author); monthly stakeholder report (use
  monthly-stakeholder-report-author).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. Modeled on the
            user-invocable draft-win-regression-report skill but
            conformed to meta-pipeline frontmatter / required-section
            discipline.
---

# win-regression-report-author

Phase 7 — produce the Win/Regression Report at T+8 weeks.

## When to Use

- T+8 weeks; the baseline report has been authored and the
  diagnostic sweep is complete; the win/regression analysis
  is the interpretive layer.
- A re-launch (rebrand / re-platform) at T+8 against the new
  baseline.
- A specific dispute or contention about whether the project
  succeeded warrants a focused win/regression analysis with
  attribution.

## When NOT to Use

- T+8 baseline report — `baseline-report-author` (site-build
  family). Baseline is the snapshot of metrics; win/regression
  is the interpretation.
- Diagnostic sweep — `diagnostic-sweep-author` (Tier 2 here).
  Sweep finds problems; win/regression reports patterns to
  sponsor.
- 30-day stabilization report — `stabilization-report-author`
  (Tier 1 here). Stabilization is at T+30; win/regression is
  at T+8 (about a month later).
- Monthly stakeholder report — `monthly-stakeholder-report-
  author` (Tier 2 here). Monthly is recurring cadence;
  win/regression is a one-time T+8 deep analysis.
- Optimization-backlog seeding — that's
  `optimization-backlog-author`'s job; win/regression
  surfaces patterns; backlog acts on them.
- Quarterly business review — `quarterly-business-review-
  author` (Tier 2). QBR runs quarterly with broader scope.

## Capabilities Owned

- Author the **wins section** per SOP §10.2.4:
  - Metrics that improved vs pre-launch baseline.
  - Magnitude of improvement (absolute + relative).
  - Statistical confidence in the improvement.
  - Most-likely cause attribution (with calibrated
    confidence — "high" / "medium" / "low" not
    "definitely").
- Author the **regressions section**:
  - Metrics that declined vs baseline OR vs Phase-2 NFR
    targets.
  - Magnitude of decline.
  - Most-likely cause (often easier to attribute than
    wins because regressions tend to have specific
    triggers).
  - Severity classification (must-fix-immediately /
    should-address-soon / accept-trade-off).
- Author the **surprises section**:
  - Patterns nobody predicted at Phase 1 KPI definition.
  - Counter-intuitive signals (KPI A improved while
    related KPI B declined).
  - User behavior that contradicts persona model.
- Author the **stable metrics section**:
  - Metrics that didn't move.
  - Per metric: was no-movement the success outcome (e.g.,
    error rate stayed low) or a null result (KPI was
    expected to move and didn't)?
- Document **next-step recommendations** — what the
  win/regression analysis suggests for the next 3 months.
- Maintain **sponsor-and-stakeholder audience posture** —
  shareable; chart-heavy; honest tone; calibrated
  attribution.
- Cite **vision** + **KPIs** + **baseline-report** + **OST**
  by stable name.
- Write to `docs/07-postlaunch/win-regression-<YYYY-MM-DD>.md`.

## Handoffs to Other Skills

- **From `baseline-report-author`** (site-build family) — the
  T+8 baseline is the upstream artefact this interprets.
- **From `diagnostic-sweep-author`** (Tier 2 here) — sweep
  findings inform the regressions section.
- **From `kpi-author`** (site-build) — KPI definitions and
  targets.
- **From `vision-author`** (site-build) — vision states the
  success outcomes.
- **To `optimization-backlog-author`** (Tier 1 here) —
  regressions and surprises seed backlog candidates.
- **To `quarterly-business-review-author`** (Tier 2 here) —
  win/regression feeds the quarterly synthesis.
- **To `monthly-stakeholder-report-author`** (Tier 2 here) —
  the month containing T+8 references this report.
- **From the user-invocable `draft-win-regression-report`** —
  peer skill producing the same artifact via a different
  procedure.

## Edge Cases

- **Wins outnumber regressions 5:1.** Audit the analysis —
  either the project genuinely went well, or attribution
  is over-claiming. Re-check causal confidence.
- **Regressions outnumber wins 5:1.** Sponsor needs the
  honest message; the report leads with the regressions
  and the remediation plan. Refuse to bury the lede.
- **Net-zero progress** (wins and regressions cancel out).
  Surface honestly; sponsor wants to know the project's
  true delta.
- **Causal confidence is low across the board.** Document
  the limitation; acknowledge that without controlled
  experiments, observational data only suggests
  associations. Recommend experiments via
  `optimization-loop-author` to test hypotheses.
- **A regression appears tied to a Phase 4 ADR.** Cross-
  link to the ADR; surface the ADR's "Consequences"
  section's "negative" predictions vs reality.
- **The KPI definition itself is the problem.** Surface;
  recommend re-baselining the KPI in the next quarter
  via `kpi-author` re-author.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §10.2.4.
The user-invocable `draft-win-regression-report` is a peer
skill producing the same artifact via a different procedure.

## Self-Audit

Before declaring a win/regression report complete,
confirm:
- All 4 sections covered (wins / regressions / surprises /
  stable).
- Each metric movement has magnitude + confidence in
  attribution.
- Severity per regression (must-fix-immediately / should-
  address-soon / accept-trade-off).
- Stable-metrics distinguishes success-no-movement from
  null-result.
- Next-step recommendations stated.
- Audience-appropriate tone (sponsor + stakeholders).
- Cross-references to baseline + KPIs + vision + OST.
