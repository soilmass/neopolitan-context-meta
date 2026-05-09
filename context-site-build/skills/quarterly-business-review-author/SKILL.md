---
name: quarterly-business-review-author
description: >
  Authors the Quarterly Business Review (QBR) — comprehensive
  metrics with trends, ROI assessment of the project (vs
  investment, vs forecast), competitive position update,
  strategic recommendations for the next quarter, and resource
  needs. Writes to docs/07-postlaunch/qbr/<YYYY-Q>.md (SOP
  §10.5.3). Use at quarter close during Phase 7. Do NOT use for:
  monthly stakeholder report (use monthly-stakeholder-report-
  author Tier 2 — QBR consumes 3 monthlies + adds depth);
  weekly metric report (use weekly-metric-report-author in
  site-build family); annual retrospective (use annual-
  retrospective-author Tier 3); T+8 baseline (use
  baseline-report-author in site-build); win-regression report
  (use win-regression-report-author Tier 2 — that is paired
  with baseline at T+8, not quarterly).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. Modeled on the
            user-invocable quarterly-business-review skill but
            conformed to meta-pipeline frontmatter / required-section
            discipline.
---

# quarterly-business-review-author

Phase 7 — produce the Quarterly Business Review.

## When to Use

- Quarter close during Phase 7; three monthly reports are
  available; the QBR consolidates + adds depth.
- A board / executive meeting demands the consolidated
  quarterly artifact.
- A re-baselining decision (after major scope change or
  organizational shift) warrants a QBR-grade synthesis to
  reset expectations.

## When NOT to Use

- Monthly stakeholder report — `monthly-stakeholder-report-
  author` (Tier 2 here). QBR consumes three monthlies + adds
  ROI + competitive + strategic recommendations.
- Weekly metric report — `weekly-metric-report-author`
  (site-build family).
- Annual retrospective — `annual-retrospective-author`
  (Tier 3 here). Annual is yearly + roadmap; QBR is per-
  quarter.
- T+8 baseline report — `baseline-report-author` (site-build).
- Win-regression report — `win-regression-report-author`
  (Tier 2 here). Win-regression is paired with baseline at
  T+8; not quarterly.
- Strategic roadmap authoring — that's PdM-driven roadmap
  work feeding into the QBR's recommendations section, not
  the QBR itself.
- Sales / financial reporting — adjacent artifacts owned by
  finance / business teams; QBR references them but doesn't
  produce them.

## Capabilities Owned

- Author the **comprehensive metrics with trends** per SOP
  §10.5.3:
  - All KPIs trended quarter-over-quarter and year-over-
    year.
  - Performance baseline trajectory (p75 LCP / INP / CLS).
  - SEO + AEO citation trajectory.
  - Conversion / engagement trajectory.
  - Customer satisfaction (NPS / CSAT / support volume).
- Author the **ROI assessment**:
  - Investment to date (build cost + ongoing operations
    cost).
  - Forecast vs actual (what was projected at Phase 1
    budget; what actually happened).
  - Returns measured against the original business
    outcomes the vision stated.
  - Per-experiment ROI rollup (win-rate × magnitude per
    §10.3.2 portfolio management).
- Author the **competitive position update**:
  - Competitor benchmarks re-scanned this quarter.
  - Where we gained share / lost share.
  - New entrants or threats.
  - AI search competitive landscape.
- Author the **strategic recommendations for next quarter**:
  - 3-5 named priorities with rationale.
  - Resource asks (headcount, budget, tooling).
  - Trade-offs explicitly stated (what gets dropped to
    accommodate priorities).
- Cite **vision** + **KPIs** + **OST** + **monthly reports**
  + **experiment portfolio** + **optimization backlog** by
  stable name.
- Maintain **executive-tier discipline** — audience is
  Sponsor + leadership + sometimes board. Polished
  presentation-grade; charts + tables; reads in 30 minutes;
  has an executive summary.
- Write to `docs/07-postlaunch/qbr/<YYYY-Q>.md`.

## Handoffs to Other Skills

- **From `monthly-stakeholder-report-author`** (Tier 2 here)
  — three monthly reports are the input.
- **From `kpi-author`** (site-build) — KPIs + targets.
- **From `vision-author`** (site-build) — the vision frames
  ROI assessment.
- **From `ost-author`** (site-build) — strategic
  recommendations land on OST opportunity branches.
- **From `optimization-backlog-author`** (Tier 1 here) —
  cumulative backlog state.
- **From `optimization-loop-author`** (Tier 1 here) —
  experiment portfolio for ROI rollup.
- **From `aeo-baseline-author`** (Tier 2 here) — AEO
  trajectory.
- **To `annual-retrospective-author`** (Tier 3 here) — four
  QBRs feed the annual retro.
- **From the user-invocable `quarterly-business-review`** —
  peer skill producing the same artifact via a different
  procedure.

## Edge Cases

- **ROI is negative this quarter.** Document honestly with
  attribution analysis; recommend specific corrective
  actions; refuse to spin. Sponsor / board credibility
  comes from honest reporting.
- **A KPI is being gamed.** Surface the Goodhart concern;
  recommend re-baselining the KPI or adding a
  guardrail metric.
- **Competitive position deteriorating.** Honest analysis
  of why; recommendations for response (defend / pivot /
  re-position).
- **Strategic recommendations conflict with sponsor's
  expressed priorities.** Surface the conflict; provide
  the recommendation with rationale + the alternative
  the sponsor prefers; sponsor decides on the record.
- **Three-month period had a major outage / incident.**
  Full incident impact accounting; remediation status;
  trend lines annotated.
- **First QBR after launch** (quarter ends pre-T+8).
  QBR-mode shifts to "stabilization-and-baseline" framing;
  defer some sections to next QBR when more data is
  available.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §10.5.3.
The user-invocable `quarterly-business-review` is a peer
skill producing the same artifact via a different procedure.

## Self-Audit

Before declaring a QBR complete, confirm:
- All 4 sections covered (metrics with trends / ROI /
  competitive / strategic recommendations).
- Executive summary at top (≤1 page).
- Charts + tables for key trends (not just prose).
- Investment-to-date + forecast-vs-actual stated
  explicitly.
- 3-5 named strategic priorities with rationale + asks.
- Trade-offs explicit (what's deferred).
- Three monthly reports cited by stable ID.
- Cross-references to vision + KPIs + OST + backlog +
  experiments by stable name.
- Length: ≤12 pages rendered (quarterly cadence justifies
  depth, but exec audience needs scanability).
