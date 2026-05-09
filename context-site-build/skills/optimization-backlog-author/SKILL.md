---
name: optimization-backlog-author
description: >
  Authors the prioritized optimization backlog at T+8 weeks
  derived from diagnostic findings, scored via RICE. Top 10-20
  items become the optimization roadmap. Output at
  docs/07-postlaunch/optimization-backlog.md (SOP §10.2.5). Use
  at T+8 after diagnostic-sweep-author runs and ongoing through
  Phase 7 as findings accumulate. Do NOT use for: running a
  single experiment from the backlog (use optimization-loop-
  author — that is the per-experiment skill); the diagnostic
  sweep itself (use diagnostic-sweep-author); the T+8 baseline
  report (use baseline-report-author in site-build family);
  weekly metric report (use weekly-metric-report-author in
  site-build family); change requests (use change-request-author
  in site-build family).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [weekly]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. Modeled on the
            user-invocable draft-optimization-backlog skill but
            conformed to meta-pipeline frontmatter / required-section
            discipline.
---

# optimization-backlog-author

Phase 7 — produce + maintain the prioritized optimization backlog.

## When to Use

- T+8 weeks; the diagnostic sweep has produced findings; the
  baseline report has identified wins + regressions; the
  optimization backlog seeds from those.
- Weekly during ongoing Phase 7 as new findings accumulate
  (discovery-tick memos, support tickets, user feedback,
  experiment results) — re-prioritize.
- Quarterly during quarterly business review; backlog feeds
  the strategic roadmap conversation.
- A discovery-tick memo surfaces a high-confidence opportunity
  that warrants immediate backlog placement.

## When NOT to Use

- Running a single experiment — `optimization-loop-author`.
  The backlog is the queue; the loop is per-experiment
  execution.
- Diagnostic sweep — `diagnostic-sweep-author` (Tier 2). The
  sweep is the source of findings; the backlog prioritizes.
- T+8 baseline report — `baseline-report-author` (site-build
  family). Baseline is the snapshot; backlog is the action
  list.
- Weekly metric report — `weekly-metric-report-author`
  (site-build family). Weekly reports current state; backlog
  is forward-looking.
- Change requests — `change-request-author` (site-build).
  Backlog items become Change Requests when they cross a
  scope threshold (Major).
- Phase 4 sprint backlog — that's the build phase's working
  backlog. Optimization backlog is post-launch.

## Capabilities Owned

- Capture each backlog item per SOP §10.2.5 with **RICE**
  scoring:
  - **Reach** — how many users affected per period.
  - **Impact** — estimated effect size (0.25 / 0.5 / 1 / 2 / 3).
  - **Confidence** — % (0.5 / 0.8 / 1.0).
  - **Effort** — person-weeks.
  - **RICE score** = Reach × Impact × Confidence ÷ Effort.
- Capture each item with metadata:
  - **Stable ID** (`OPT-NNNN`).
  - **Hypothesis** in standard form (per §10.3.1):
    *"We believe <change> will <effect> for <users>
    because <evidence>."*
  - **Source** — which finding from diagnostic-sweep or
    baseline or discovery-tick or support-tickets.
  - **Owner** — named individual accountable.
  - **Target experiment date** — when this enters the
    optimization-loop.
- Maintain the **top 10-20 items** as the active roadmap;
  items below that line are watch-listed.
- Re-score **monthly** as new evidence comes in; re-rank;
  retire items that have been tested + decided.
- Tag items with **theme** (perf / SEO / AEO / conversion /
  content / a11y / motion) for portfolio balance.
- Cross-reference each item's **source finding** by stable
  ID.
- Write to `docs/07-postlaunch/optimization-backlog.md`
  (single file maintained continuously; not per-week).

## Handoffs to Other Skills

- **From `diagnostic-sweep-author`** (Tier 2) — sweep findings
  seed the backlog.
- **From `baseline-report-author`** (site-build family) — the
  baseline's regression list seeds optimization items.
- **From `win-regression-report-author`** (Tier 2) — win/
  regression analysis surfaces items.
- **From `discovery-tick-author`** (site-design family) —
  weekly discovery-tick memos produce 1-3 backlog candidates
  in hypothesis form.
- **From support / sales / customer-success** — operator-
  driven channels feed items.
- **To `optimization-loop-author`** (Tier 1 here) — top-
  ranked items enter the experimentation loop.
- **To `quarterly-business-review-author`** (Tier 2 here) —
  backlog summary feeds the QBR's strategic recommendations.
- **To `change-request-author`** (site-build) — items that
  cross the Major scope threshold become CRs.
- **From the user-invocable `draft-optimization-backlog`** —
  peer skill producing the same artifact via a different
  procedure.

## Edge Cases

- **Backlog has 100+ items.** Force a cut to top 20 active +
  watch-list. The discipline of removal is the work.
- **Two items have the same RICE score.** Tie-break by
  theme balance (don't ship 3 perf experiments in a row;
  spread across themes per §10.3.2 portfolio management).
- **Item's hypothesis has weak evidence** (RICE Confidence
  < 0.5). Don't promote to active; either gather more
  evidence (re-enter discovery) or de-prioritize.
- **Item is impossible to test** (no traffic, no
  measurement). Move to a "blocked — needs measurement
  setup" sub-list.
- **Stakeholder demands their pet item be top-ranked.**
  Hold the line on RICE scoring; refuse manual override
  unless Sponsor signs off + the override is logged.
- **An item failed in optimization-loop** but stakeholder
  wants to retry. Document the failure; re-test only with
  changed hypothesis or new evidence (per §10.6 anti-
  pattern "A/B test theater").

## References

No external `references/*.md` files yet — first real
authoring run will produce a template worth promoting. The
canonical authority is `internal://site-build-procedure.md`
§10.2.5. The user-invocable `draft-optimization-backlog` is
a peer skill producing the same artifact via a different
procedure.

## Self-Audit

Before declaring an optimization backlog update complete,
confirm:
- Each new item has all 5 RICE fields + hypothesis +
  source + owner + target date.
- Top 10-20 items identified explicitly.
- Theme distribution balanced (no single theme > 50% of
  active backlog).
- Source findings cross-referenced by stable ID.
- Stale items (older than 90 days un-tested) flagged for
  re-scoring or retirement.
- File maintained as single living artifact (not
  per-week).
