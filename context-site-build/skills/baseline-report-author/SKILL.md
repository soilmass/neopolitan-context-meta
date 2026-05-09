---
name: baseline-report-author
description: >
  Authors the Post-Launch Baseline Report at T+8 weeks. Aggregates
  Phase-7 metrics (performance, a11y, SEO, conversion events, errors)
  and compares against the pre-launch baseline. Identifies wins and
  regressions vs targets, then recommends optimization-backlog seeds.
  Writes the artifact to docs/07-postlaunch/baseline-report.md
  (site-build-procedure.md §10.2.1). Use after stabilization completes
  (T+8 weeks). Do NOT use for: 30-day stabilization synthesis,
  win-vs-regression deep dive, Phase-7 diagnostic, or weekly /
  monthly cadence reports — these belong to the future site-operate
  family (the user-invocable draft-stabilization-report,
  draft-win-regression-report, diagnostic-sweep, weekly-metric-report,
  and monthly-stakeholder-report cover them now); authoring a runbook
  (use runbook-author).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.1 — patch: anti-triggers re-framed for out-of-scope siblings
            as future-site-operate-family pointers with user-invocable
            fallbacks (B6/A62 + B7/A63); cross-family Handoffs to
            optimization-backlog-author / optimization-loop reframed;
            "Authority surface" reframed; deferred references/
            template.md row dropped.
    v0.1.0 — initial. Authored via skill-author during the v0.7.0
            first-real-consumer dogfood. Modeled on the user-invocable
            draft-baseline-report skill.
---

# baseline-report-author

Phase 7 — produce the T+8-week Post-Launch Baseline Report.

## When to Use

- A project has reached T+8 weeks post-launch (the canonical
  stabilization window has closed) and the baseline-comparison
  report is due.
- A project is exiting hypercare and a single artifact is needed to
  hand off to ongoing operations / optimization workstreams.
- Re-baselining after a major re-platform or re-launch (e.g., a v2
  rebrand) when the original baseline no longer represents reality.

## When NOT to Use

- Inside the 30-day stabilization window — use
  `stabilization-report-author` (deferred) for the 4-week
  synthesis. The baseline is the *next* artifact, not a substitute.
- Deep-diving into one specific regression — `win-regression-
  report-author` (deferred) handles win/regression synthesis with
  more depth than the baseline summary.
- Running the diagnostic across all post-launch surfaces — that's
  `diagnostic-sweep` (deferred). The baseline *consumes* the sweep's
  outputs but isn't the sweep itself.
- Weekly or monthly stakeholder cadence — those are different atoms
  (`weekly-metric-report-author`, `monthly-stakeholder-report-
  author`, both deferred).
- Authoring runbooks — that's `runbook-author`.
- Recording an architectural decision triggered by the baseline —
  that's `adr-author`.

## Capabilities Owned

- Aggregate **performance metrics** (LCP, INP, CLS at p75) at T+8
  vs the pre-launch baseline; report deltas with significance.
- Aggregate **a11y posture** (WCAG conformance level, automated
  audit pass rate, manual issue count) vs the pre-launch baseline.
- Aggregate **SEO posture** (indexed pages, organic-traffic delta,
  rank for primary queries) vs the pre-launch baseline.
- Aggregate **conversion-event health** (primary CTA conversion
  rate, drop-offs, error-page rates) vs targets.
- Aggregate **error rates** (5xx, JS errors, support-ticket volume).
- Identify **wins** (improvements vs targets) and **regressions**
  (deteriorations vs baseline OR targets).
- **Recommend optimization-backlog seeds** — 3-7 candidate items
  with leverage estimates, handed off to `optimization-backlog-
  author` (deferred).
- Write the artifact to `docs/07-postlaunch/baseline-report.md`.

## Handoffs to Other Skills

- **From `runbook-author`** (transitively) — the deployment /
  incident runbooks named RTOs and SLOs that the baseline measures
  against.
- **From `srs-author`** — NFRs are the targets the baseline
  reports against.
- **From `kpi-author`** (Tier 2) — KPIs are the success criteria
  the baseline reports against.
- **To the future `site-operate` family** — the optimization
  backlog seeds and the regression list flow downstream when that
  family is bootstrapped. Until then, the user-invocable
  `draft-optimization-backlog` and `optimization-loop` are the
  peers that consume this report.
- **To `adr-author`** — when a regression triggers an architectural
  pivot (e.g., "perf regression forced us to swap our SSR strategy"),
  an ADR records the decision; the baseline references the ADR.

## Edge Cases

- **No pre-launch baseline exists** (the project never measured
  pre-launch metrics). Author the report as `## Status: First
  Baseline — no comparison`; the doc serves as the future T-0
  reference.
- **T+8 weeks falls during a holiday / seasonal anomaly**. Note
  the anomaly in the executive summary; consider a `## T+12
  Re-Run` flag rather than treating the anomaly-skewed numbers
  as the canonical baseline.
- **Some metric domain is missing** (e.g., the project has no
  conversion events). Mark the section as N/A with rationale; do
  not omit the section silently.
- **Wins and regressions cancel out** (net-zero progress). Report
  honestly; the optimization-backlog seeds become the project's
  next-quarter focus.

## References

No external `references/*.md` files yet. The canonical authority is
`internal://site-build-procedure.md` §10.2.1. The user-invocable
`draft-baseline-report` skill is a peer producing the same artifact
via a different procedure.

## Self-Audit

Before declaring the baseline report complete, confirm:
- All five metric domains have a section (perf / a11y / SEO /
  conversion / errors). Missing domains are explicit N/A, not silent.
- Comparison targets named explicitly (vs pre-launch baseline AND
  vs Phase-2 NFRs).
- ≥3 optimization-backlog seeds named.
- ≥1 regression flagged (if zero, the report's summary explicitly
  acknowledges that — projects with zero regressions at T+8 are
  rare enough to be flagged for re-verification).
- Doc is ≤6 pages rendered (a baseline isn't a deep dive).
