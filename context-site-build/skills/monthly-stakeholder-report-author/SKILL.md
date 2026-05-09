---
name: monthly-stakeholder-report-author
description: >
  Authors the monthly stakeholder report consolidating four
  weekly memos plus deeper qualitative summary — quantitative
  KPI summary, experiment portfolio, content highlights, SEO +
  AEO movement, customer feedback themes, product roadmap update,
  risks + asks. Audience is extended stakeholders + leadership.
  Writes to docs/07-postlaunch/monthly-reports/<YYYY-MM>.md (SOP
  §10.5.2). Use first business day of each month during Phase 7.
  Do NOT use for: weekly metric report (use weekly-metric-report-
  author in site-build family — monthly consolidates four
  weeklies); the quarterly business review (use quarterly-
  business-review-author Tier 2 — that is deeper); annual
  retrospective (use annual-retrospective-author Tier 3); the
  T+8 baseline (use baseline-report-author in site-build family);
  win-regression report (use win-regression-report-author Tier 2).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [weekly]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. Modeled on the
            user-invocable monthly-stakeholder-report skill but
            conformed to meta-pipeline frontmatter / required-section
            discipline.
---

# monthly-stakeholder-report-author

Phase 7 — produce the monthly stakeholder report.

## When to Use

- First business day of a new month during Phase 7; the prior
  month's four weekly memos are available; consolidation is
  due.
- A re-launch or major event during a month warrants a
  combined-monthly-plus-event-summary report.
- Strategic review demands the consolidated monthly artifact
  (e.g., quarterly board meeting; the QBR consumes 3 monthly
  reports plus the QBR's own deeper analysis).

## When NOT to Use

- Weekly metric report — `weekly-metric-report-author`
  (site-build family). Monthly consolidates four weeklies;
  doesn't replace them.
- Quarterly business review — `quarterly-business-review-
  author` (Tier 2 here). QBR is deeper; takes 3 monthlies as
  input and adds ROI + competitive analysis.
- Annual retrospective — `annual-retrospective-author`
  (Tier 3). Annual is yearly + roadmap.
- T+8 baseline report — `baseline-report-author` (site-build).
- Win-regression report — `win-regression-report-author`
  (Tier 2). Win-regression is at T+8 paired with baseline.
- Crisis / incident communication — those go through the
  runbook's incident-response process, not a monthly cadence.

## Capabilities Owned

- Consolidate **four weekly memos** into a deeper monthly
  view per SOP §10.5.2:
  - **Quantitative summary** — KPIs (with monthly delta vs
    prior month and target), traffic, conversion,
    performance (p75 LCP / INP / CLS), errors.
  - **Experiment portfolio summary** — running count,
    decided this month (won / lost / inconclusive),
    learnings.
  - **Content highlights** — what got published, top
    performers, content velocity vs plan.
  - **SEO + AEO movement** — month-over-month in classic
    rankings + AI search citation rate.
  - **Customer feedback themes** — patterns across support
    + survey + interview signal.
  - **Product roadmap update** — what shipped this month +
    what's next.
  - **Risks + asks** — escalations, decisions needed.
- Maintain **stakeholder posture** — audience is extended
  stakeholders + leadership (not the working trio).
  Polished tone; complete sentences; chart-friendly tables.
- Cite the **four weekly memos** by ISO week number + the
  KPI doc + the optimization backlog + the experiment log
  by stable IDs.
- Document **status** (GREEN / YELLOW / RED) at month
  granularity with one-paragraph rationale.
- Write to `docs/07-postlaunch/monthly-reports/<YYYY-MM>.md`.

## Handoffs to Other Skills

- **From `weekly-metric-report-author`** (site-build family) —
  four weekly memos are the input.
- **From `optimization-loop-author`** (Tier 1 here) —
  experiment decisions feed the experiment portfolio
  section.
- **From `optimization-backlog-author`** (Tier 1 here) —
  backlog state informs the roadmap update.
- **From `kpi-author`** (site-build) — KPI definitions + targets.
- **To `quarterly-business-review-author`** (Tier 2 here) —
  three monthly reports are inputs to the QBR.
- **To stakeholder broadcast channel** — the memo is the
  stakeholder visibility artefact.
- **From the user-invocable `monthly-stakeholder-report`** —
  peer skill producing the same artifact via a different
  procedure.

## Edge Cases

- **A weekly memo was missed.** Note the gap explicitly in
  the monthly; the consolidation can't fabricate the
  missing data. Surface as a finding for the cadence.
- **Status is RED.** The monthly's tone shifts to action-
  oriented — lead with the issue + escalation status; KPI
  table follows but is not the headline.
- **Major incident this month.** Full incident summary
  with timeline + root cause + remediation; the metric
  table notes the impact window.
- **Customer feedback themes contradict KPI improvement.**
  Surface honestly — KPIs may be measuring the wrong
  thing or showing a Goodhart effect. Recommend a
  discovery-tick to investigate.
- **Stakeholder demands the report become a presentation
  deck.** Refuse silent format change; the working memo
  stays. A presentation can be derived for specific
  meetings but the memo remains canonical.
- **Roadmap update conflicts with prior month's
  commitments.** Document the change + the reason
  (priority shift / capacity / new evidence); refuse
  silent drift.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §10.5.2.
The user-invocable `monthly-stakeholder-report` is a peer
skill producing the same artifact via a different procedure.

## Self-Audit

Before declaring a monthly report complete, confirm:
- All 7 sections covered (KPI / experiment portfolio /
  content / SEO+AEO / feedback / roadmap / risks+asks).
- Status (GREEN / YELLOW / RED) with one-paragraph
  rationale.
- Four weekly memos cited by ISO week + month gaps
  surfaced.
- Cross-references to optimization backlog, experiment
  log, KPI doc by stable ID.
- Tone is polished (audience is extended stakeholders).
- Length is reasonable for monthly cadence (≤4 pages
  rendered).
