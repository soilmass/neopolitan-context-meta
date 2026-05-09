---
name: master-schedule-author
description: >
  Authors the project's Master Schedule and Budget plan. Records
  milestones with dates, dependencies (internal and external),
  critical path, resource allocation, and 10–20% schedule
  contingency; alongside direct and indirect costs, contingency
  budget, and burn-rate projection. Writes to
  docs/02-requirements/master-schedule.md and
  docs/02-requirements/budget.md (site-build-procedure.md §5.7.1
  and §5.7.2). Use at Phase 2 close, when scope and architecture
  are stable enough to estimate. Do NOT use for: authoring the SRS
  (use srs-author); recording an architectural decision (use
  adr-author); risk tracking (use risk-register-author); sprint
  planning (Phase 4 ceremony — out of scope here); the
  communications plan (Phase 2 §5.7.4 — out of scope here).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.2.0
            Tier 2/3 expansion pass. Modeled on the user-invocable
            draft-master-schedule skill but conformed to meta-pipeline
            frontmatter / required-section discipline.
---

# master-schedule-author

Phase 2 — produce the project's Master Schedule and Budget plan.

## When to Use

- Phase 2 Requirements & Architecture is closing; the SRS scope
  and architecture are stable enough to estimate; the master
  schedule is a Gate 2 deliverable.
- A scope change has been approved (per `change-request-author`)
  and the schedule must be **re-baselined**.
- A new resource constraint (team-member departure, vendor
  delay) has surfaced and the critical path needs to be re-cut.
- The original schedule's contingency has been consumed and the
  Sponsor needs an honest re-baseline.

## When NOT to Use

- SRS or architecture is undefined — they're prerequisites.
  Estimating against unknowns produces fiction.
- Writing the SRS — `srs-author`.
- Recording an architectural decision — `adr-author`.
- Tracking risks — `risk-register-author`. Schedule risks
  inform the contingency size; the register is the artifact
  that holds them.
- **Sprint planning** — that's a Phase 4 ceremony, not a
  Phase 2 master-schedule deliverable. Sprints are the unit
  inside the master schedule, not its output.
- The communications plan (per §5.7.4 of the SOP) — sibling
  Phase 2 deliverable; consider authoring its dedicated atom
  (deferred) or the user-invocable `draft-comms-plan`.

## Capabilities Owned

- Author the **master schedule** per SOP §5.7.1:
  - **Milestones** with dates (kickoff, gates, launch, post-
    launch checkpoints).
  - **Dependencies** — both internal (sequenced work) and
    external (vendor deliveries, decision-window closures,
    integration partners).
  - **Critical path** identified explicitly (the longest chain
    of dependent activities; slippage here slips the launch).
  - **Resource allocation** — named individuals or roles per
    workstream, with utilization assumptions.
  - **Schedule contingency** — 10–20% built in (per SOP).
- Author the **budget plan** per SOP §5.7.2:
  - **Direct costs** — team time, vendor fees, tooling
    subscriptions, infrastructure (hosting + CDN + monitoring).
  - **Indirect costs** — overhead allocation if the org
    accounts for it.
  - **Contingency** — 10–20% (per SOP) for the unknown-unknowns.
  - **Burn-rate projection** — monthly run rate; cumulative
    spend curve; alarm thresholds.
- Cross-reference: every schedule risk surfaces in
  `risk-register-author`; every cost-driving architectural
  decision surfaces in `adr-author`.
- Maintain re-baseline discipline: when a Major change is
  approved (per `change-request-author`), the schedule and
  budget are re-baselined explicitly with old plan archived.
- Write to `docs/02-requirements/master-schedule.md` and
  `docs/02-requirements/budget.md`.

## Handoffs to Other Skills

- **From `srs-author`** — scope drives estimation.
- **From `adr-author`** — architectural decisions drive cost
  and risk.
- **From `risk-register-author`** — schedule risks inform the
  contingency size.
- **To phase-gate reviews** — the Sponsor approves schedule
  and budget at Gate 2.
- **To `change-request-author`** — when a change is Major,
  the CR's impact assessment cites schedule + budget impact
  from this artifact, and the schedule is re-baselined per
  §11.5.
- **To weekly status memos** — the schedule is the spine of
  the weekly stakeholder update.
- **From the user-invocable `draft-master-schedule`** — peer
  skill.

## Edge Cases

- **Aggressive launch window** (Sponsor has a fixed external
  date — campaign tie-in, regulatory deadline, contract
  expiry). Build the schedule backward from the date; surface
  the descope or doubled contingency required to hit it.
  Refuse to ship a schedule that's mathematically impossible
  without naming what's giving way.
- **Vendor delivery dates are TBD.** Insert placeholder dates
  with explicit ranges + a re-baseline trigger when the vendor
  confirms.
- **Resource conflict** with another in-flight project. Halt;
  this is a portfolio-level decision the Sponsor (or PMO)
  resolves before this atom can ship.
- **Contingency consumed mid-build.** Re-enter this atom for
  a re-baseline rather than silently drifting. Per §11.5,
  re-baseline is healthy adaptation; silent drift is failure.
- **No historical estimate base** (greenfield team / stack).
  Use industry benchmarks; widen the contingency to 25–30%;
  document the assumption explicitly so the Sponsor knows
  the estimate's confidence is lower.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §5.7.1
(schedule) and §5.7.2 (budget). The user-invocable
`draft-master-schedule` is a peer skill producing the same
artifact via a different procedure.

## Self-Audit

Before declaring a master schedule + budget complete, confirm:
- Every milestone has a date AND a named approver.
- Critical path is explicitly identified (not just "we'll see").
- Schedule contingency ≥10% (≥20% recommended for greenfield
  or aggressive windows).
- Resource allocation names individuals or roles (no "the
  team will figure it out").
- Budget contingency ≥10%.
- Burn-rate projection has alarm thresholds (not just totals).
- Cross-references to `risk-register-author` and `adr-author`
  are present.
- Re-baseline trigger is named (e.g., "if any Major CR is
  approved").
