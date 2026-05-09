---
name: annual-retrospective-author
description: >
  Authors the annual retrospective + roadmap proposal at the
  one-year mark of post-launch operations. Synthesizes the four
  QBRs, the optimization backlog cumulative impact, the
  experiment portfolio's win rate + magnitude, and customer
  feedback themes into a strategic year-in-review with named
  next-year priorities. Writes to docs/07-postlaunch/annual-retro/<YYYY>.md
  (SOP §10 named in §12 Standard Deliverables Index). Use at
  one-year mark + every subsequent year. Do NOT use for: quarterly
  business review (use quarterly-business-review-author Tier 2 —
  annual consumes 4 QBRs); monthly stakeholder report (use
  monthly-stakeholder-report-author Tier 2); a strategic roadmap
  authoring document (PdM-driven; this atom proposes priorities,
  doesn't author the roadmap document itself); the T+8 baseline
  (use baseline-report-author in site-build); win-regression (use
  win-regression-report-author Tier 2).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. Modeled on the
            user-invocable annual-retro skill but conformed to
            meta-pipeline frontmatter / required-section discipline.
---

# annual-retrospective-author

Phase 7 — produce the annual retrospective + roadmap proposal.

## When to Use

- One-year mark of post-launch operations; four QBRs are
  available; the annual retro consolidates the year and
  proposes priorities for the next.
- Year 2+ annual retro at each subsequent year mark.
- A major strategic pivot mid-year (rare) warrants an off-
  cycle annual-grade retro to reset.

## When NOT to Use

- Quarterly business review — `quarterly-business-review-
  author` (Tier 2 here). Annual consumes four QBRs;
  doesn't replace them.
- Monthly stakeholder report — `monthly-stakeholder-report-
  author` (Tier 2).
- A strategic roadmap authoring document — that's PdM-driven
  roadmap work that this atom *proposes priorities for*. The
  roadmap document itself is a separate artefact.
- T+8 baseline report — `baseline-report-author` (site-build).
- Win-regression report — `win-regression-report-author`
  (Tier 2).
- Per-team performance reviews — adjacent to but separate
  from the project annual retro.
- Sales / financial year-in-review — finance / commercial
  team owns; this atom may reference them.

## Capabilities Owned

- Author **year-in-review synthesis**:
  - **KPI trajectory** across the year (quarterly snapshots
    rolled up).
  - **Major shipped work** by quarter (features / content /
    optimizations).
  - **Experiment portfolio** — total experiments run, win
    rate, magnitude of wins, learnings (per SOP §10.3.2
    portfolio management metrics).
  - **Customer feedback themes** at year scale.
  - **Operational health** — uptime, error rate trend,
    incidents.
  - **Team narrative** — what was hard, what worked, what
    surprised the team.
- Author **named next-year priorities**:
  - 3-5 named priorities with rationale grounded in the
    year's evidence.
  - Resource asks (headcount, budget, tooling).
  - Trade-offs explicit (what gets dropped to accommodate
    priorities).
  - Cross-functional dependencies (other teams whose work
    enables / blocks priorities).
- Author **strategic re-framing** if warranted:
  - Vision update recommendation if the year's evidence
    shifts the business model materially.
  - KPI re-baselining recommendation if KPIs proved
    gameable or wrong.
  - Persona update recommendation if user behavior
    contradicts model.
- Cite **vision** + **KPIs** + **OST** + four QBRs +
  cumulative experiment portfolio + optimization backlog
  by stable name.
- Maintain **executive-tier discipline** — audience is
  Sponsor + leadership + sometimes board. Polished
  presentation-grade; ≤20 pages rendered; reads in 45-60
  minutes.
- Write to `docs/07-postlaunch/annual-retro/<YYYY>.md`.

## Handoffs to Other Skills

- **From `quarterly-business-review-author`** (Tier 2 here)
  — four QBRs are inputs.
- **From `optimization-backlog-author`** (Tier 1 here) —
  cumulative backlog state.
- **From `optimization-loop-author`** (Tier 1) — annual
  experiment portfolio rollup.
- **From `vision-author`** + **`kpi-author`** + **`ost-
  author`** + **`persona-author`** (site-build) — the
  strategic upstream that the retro evaluates.
- **To strategic roadmap authoring** — operator / PdM-
  driven; the retro's priorities feed the next-year
  roadmap document.
- **To `vision-author`** (site-build) — vision-update
  recommendation triggers a re-author.
- **To `kpi-author`** (site-build) — KPI re-baselining
  recommendation triggers a re-author.
- **From the user-invocable `annual-retro`** — peer skill
  producing the same artifact via a different procedure.

## Edge Cases

- **Year 1 results are dramatically below expectations.**
  Sponsor needs the honest message; the retro leads with
  the gap analysis + remediation thinking. Refuse to
  spin.
- **Team turnover during the year** affecting continuity
  of analysis. Document the limitation; named-but-departed
  contributors get credit via Git history / project
  records.
- **Strategic pivot mid-year.** Two retros — a "year as
  planned" + "year as pivoted" framing. Don't pretend the
  pivot didn't happen.
- **No QBRs were authored** (cadence broke down). The
  annual retro can't fabricate the missing context.
  Surface as a discipline finding; reconstruct as best
  possible from monthly reports.
- **Stakeholder demands the retro become a presentation
  deck.** Refuse silent format change; the working memo
  stays canonical. Derive presentations from it for
  specific audiences.
- **Year-2+ retro shows zero-progress or regression on
  prior priorities.** Surface honestly; assess whether
  priorities themselves were wrong or execution faltered.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §10
(Phase 7) named in §12 Standard Deliverables Index. The
user-invocable `annual-retro` is a peer skill producing
the same artifact via a different procedure.

## Self-Audit

Before declaring an annual retrospective complete,
confirm:
- All 6 year-in-review sections covered (KPI trajectory /
  shipped work / experiment portfolio / feedback themes /
  operational health / team narrative).
- 3-5 named next-year priorities with rationale + asks +
  trade-offs.
- Strategic re-framing recommendations stated where the
  year's evidence warrants.
- Four QBRs cited by stable ID.
- Cross-references to vision + KPIs + OST + persona +
  experiment portfolio + backlog.
- Executive-tier presentation discipline (≤20 pages;
  charts + tables; reads in 45-60 min).
