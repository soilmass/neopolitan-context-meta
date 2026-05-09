---
name: weekly-metric-report-author
description: >
  Authors the Phase-7 weekly metric report — a lightweight memo for
  Sponsor + product trio with overall status (GREEN / YELLOW / RED),
  KPIs, ops metrics (uptime, error rate, p75 LCP), experiments
  decided this week, content shipped, in-flight issues, and named
  asks. Writes to docs/07-postlaunch/weekly-reports/<YYYY-WW>.md
  (site-build-procedure.md §10.5.1). Use weekly during Phase 7
  post-launch. Do NOT use for: writing the 30-day stabilization
  report (Phase 7 §10.1; out of scope here); writing the post-
  launch baseline report (use baseline-report-author); writing the
  monthly stakeholder report (Phase 7 §10.5.2; out of scope here);
  writing the quarterly business review (Phase 7 §10.5.3; out of
  scope here); KPI definition (use kpi-author).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.2.0
            Tier 2/3 expansion pass. Modeled on the user-invocable
            weekly-metric-report skill but conformed to
            meta-pipeline frontmatter / required-section discipline.
---

# weekly-metric-report-author

Phase 7 — produce the weekly metric memo.

## When to Use

- Phase 7 post-launch; the project has exited the 30-day
  stabilization window AND the team has committed to a weekly
  cadence.
- A regular weekly memo is the agreed-upon Sponsor cadence
  (per `comms-plan-author` output) for keeping the project
  visible after launch.
- The end of a week has arrived; metrics are in (Mon-Sun
  rollup typical); time to write the memo.

## When NOT to Use

- Phase 7 is in the **stabilization window** (weeks 1–4) —
  the hypercare cadence is daily, not weekly. The
  stabilization report is the Phase-7 §10.1 deliverable
  (sibling atom, not authored yet — defer to a future
  `site-operate` family per `coverage.md` Out of Scope).
- Writing the **30-day stabilization report** — that's a
  different artifact (different audience, different cadence).
- Writing the **post-launch baseline report** at T+8 weeks
  — that's `baseline-report-author`.
- Writing the **monthly stakeholder report** (per §10.5.2)
  or **quarterly business review** (per §10.5.3) — both are
  separate Phase 7 cadences with deeper depth and broader
  audience. Out of this atom's scope.
- KPI definition — `kpi-author`. The weekly memo *reports*
  on KPI movement; the KPI doc defines the targets.
- Experiment design — that's a separate Phase 7 artifact
  (the user-invocable `optimization-loop` covers it now).

## Capabilities Owned

- Author the weekly memo per the SOP §10.5.1 template:
  - **Overall status**: GREEN / YELLOW / RED with a one-line
    rationale.
  - **KPIs**: per KPI from the project's KPI doc — current
    value, delta vs target, target-by-EoQ.
  - **Ops**: uptime, error rate, p75 LCP (mobile), against
    NFR thresholds. Pass/fail per row.
  - **Experiments**: running count, decided-this-week count
    with named results (one-line per win/loss).
  - **Content**: published count, top performer with metrics.
  - **Issues**: in-flight issues with severity + ETA.
  - **Asks**: named, specific items the Sponsor needs to
    decide or unblock. Empty `<none>` is acceptable.
- Cite KPIs by stable name from `kpi-author`'s output.
- Cite NFR thresholds by stable ID from `srs-author`'s
  output.
- Maintain **memo discipline**: lightweight (≤1 page rendered);
  not a stakeholder presentation. The audience is Sponsor +
  product trio, who need scanability.
- Write to `docs/07-postlaunch/weekly-reports/<YYYY-WW>.md`
  (ISO week numbering).

## Handoffs to Other Skills

- **From `kpi-author`** — KPIs are the memo's spine.
- **From `srs-author`** — NFR thresholds are the ops row's
  pass/fail criteria.
- **From `baseline-report-author`** — once the T+8 baseline
  exists, weekly memos compare against it for delta context.
- **From the running experiments / content / ops streams** —
  the memo aggregates their state; doesn't generate it.
- **To `comms-plan-author`** (deferred sibling) — the comms
  plan specifies this memo's cadence + channel + audience;
  this atom executes against that spec.
- **To `monthly-stakeholder-report-author`** (deferred,
  future `site-operate` family) — monthly reports
  consolidate four weekly memos.
- **From the user-invocable `weekly-metric-report`** — peer
  skill.

## Edge Cases

- **A KPI is missing data** (analytics misconfig, attribution
  break). Mark the row `data quality issue — see #N`; don't
  fabricate. The integrity of the memo is the memo's whole
  value.
- **Status is RED.** The memo's tone shifts from informational
  to action-oriented. Lead with the issue + named owner +
  ETA + escalation path. Don't bury the lede.
- **No experiments running this week.** Acceptable; mark
  "Running: 0 (next experiment kicks off Mon)." Empty
  experimentation is a fact to surface, not hide.
- **Sponsor is on vacation / unavailable.** Memo still
  ships; it lands in the doc set + Slack channel and the
  Sponsor catches up on return. Skipping memos because the
  primary reader is out is the §10.6 anti-pattern
  "stakeholder reports stop."
- **Weekly cadence has lapsed (skipped 2+ weeks).** Re-enter
  by combining the missed weeks into a single catch-up memo
  with explicit "weeks W-X covered" + a re-commitment to
  weekly cadence. Don't paper over the gap.

## References

No external `references/*.md` files yet — the SOP §10.5.1
template is the spine. The canonical authority is
`internal://site-build-procedure.md` §10.5.1. The
user-invocable `weekly-metric-report` is a peer skill
producing the same artifact via a different procedure.

## Self-Audit

Before declaring a weekly memo complete, confirm:
- Overall status is GREEN / YELLOW / RED with a one-line
  rationale (not just a color).
- Every KPI from the project's KPI doc is reported (or
  explicitly marked "data quality issue").
- Ops row reports uptime, error rate, p75 LCP at minimum.
- Experiments section names this week's decided experiments
  with one-line outcome.
- Issues section gives ETAs (not just "in flight").
- Asks section is concrete (named individual + named decision)
  or explicitly `<none>`.
- Memo is ≤1 page rendered.
