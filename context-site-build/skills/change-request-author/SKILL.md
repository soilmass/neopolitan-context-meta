---
name: change-request-author
description: >
  Authors a single Change Request following the §11 workflow —
  documents the proposed change, its business justification, urgency,
  effort / schedule / budget / risk impact assessment, and the
  classification (Minor / Moderate / Major). Routes to the
  appropriate decision-maker (PM / PM+PO / CCB) and captures the
  decision. Writes to docs/change-requests/CR-NNNN-<slug>.md
  (site-build-procedure.md §11.1). Use whenever scope, schedule, or
  budget would change after a phase gate. Do NOT use for: recording
  an architectural decision (use adr-author — ADRs document the
  architecture, CRs document the scope/schedule/budget change);
  writing the SRS (use srs-author); writing the risk register (use
  risk-register-author); re-baselining the schedule (sibling §11.5
  workflow — out of scope here; this atom triggers re-baseline,
  doesn't perform it).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.2.0
            Tier 2/3 expansion pass. Modeled on the user-invocable
            draft-change-request skill but conformed to
            meta-pipeline frontmatter / required-section discipline.
---

# change-request-author

Cross-phase — produce one Change Request following the §11
workflow.

## When to Use

- A scope / schedule / budget change is being proposed after a
  phase gate has been approved (per §11 — pre-gate changes are
  absorbed in the working phase, not change-controlled).
- A stakeholder, team member, or customer (via account team)
  has requested a change and the PM is logging it in the
  change register.
- An incident or discovery has surfaced the need for a change
  that wasn't in the original plan.
- A vendor delivery slip or external dependency change forces
  a project-level adjustment.

## When NOT to Use

- Pre-gate changes during the working phase (Phase 1
  refinement, Phase 2 SRS edits, etc.) — these are absorbed
  in the phase, not change-controlled.
- **Recording an architectural decision** — `adr-author`. ADRs
  document architecture; CRs document scope/schedule/budget
  changes. They overlap when an architectural change has
  scope impact, in which case both are produced and
  cross-linked.
- Writing the SRS — `srs-author`. CRs may add or remove SRS
  rows but the SRS itself is the spec, not the change.
- Writing the risk register — `risk-register-author`. CRs
  may surface new risks; both are tracked separately.
- Schedule **re-baselining** itself (per §11.5) — that's a
  sibling workflow performed by `master-schedule-author`
  after a Major CR is approved. This atom triggers it; it
  doesn't perform it.
- "We'll fit it in" verbal absorption — that's the §11.4
  anti-trap. Every change goes through this atom, even
  30-min fixes (Minor CR with PM disposition).
- Logging an incident — that's an ops artifact.

## Capabilities Owned

- Capture the **CR submission** per §11.1 form fields:
  - **Title** (one-line summary).
  - **Description** (what's the change?).
  - **Business justification** (why now?).
  - **Urgency** (the operator's ask: Critical /
    Required-by-date / Nice-to-have).
  - **Requester** (named individual or team).
- Author the **impact assessment** (PM + Tech Lead + BA per
  §11.1.3):
  - **Effort** (person-days).
  - **Schedule impact** (days / weeks; affects critical
    path?).
  - **Budget impact** (dollars; in contingency or out?).
  - **Risk** (new risks introduced; existing risks
    affected — cross-link to `risk-register-author`).
  - **Cross-cutting concerns** — other in-flight work
    affected.
- Apply the **classification** per §11.3:
  - **Minor**: cosmetic, within sprint capacity, no scope
    impact → PM disposition.
  - **Moderate**: new work requiring displacing committed
    scope → PM + PdM/PO disposition with documented
    trade-off.
  - **Major**: materially changes scope / schedule / budget
    → CCB review required.
- Route to the appropriate decision-maker per classification;
  capture the **decision** (Approved / Rejected / Deferred)
  with rationale and date.
- Communicate **outcome** to requester per the SLA (typically
  3 business days for Moderate; 5 for Major).
- Trigger **re-baseline** when Major changes accumulate
  (hands off to `master-schedule-author` for the schedule
  + budget update).
- Assign the next sequential **CR number** (`NNNN`) by
  reading the existing `docs/change-requests/` directory.
- Write to `docs/change-requests/CR-NNNN-<slug>.md` where
  `<slug>` is a kebab-case three-to-six-word summary.

## Handoffs to Other Skills

- **From any project participant** — CRs originate from
  stakeholders, team members, or customers.
- **From `risk-register-author`** — when a risk fires and
  needs scope adjustment.
- **From an incident** — when an incident's resolution
  requires a scope change.
- **To `master-schedule-author`** — Major CRs trigger
  schedule + budget re-baseline per §11.5.
- **To `risk-register-author`** — every CR's impact
  assessment surfaces new risks tracked in the register.
- **To `adr-author`** — when a CR has architectural
  implications, an ADR is authored alongside.
- **To `srs-author`** — when a CR adds/removes/modifies SRS
  rows, the SRS is updated atomically with the CR's
  approval.
- **To the change register** — every CR (approved AND
  rejected) lands in the register for audit.
- **From the user-invocable `draft-change-request`** — peer
  skill.

## Edge Cases

- **Verbal "we'll fit it in" request.** Refuse to skip the
  CR. Even 30-min fixes get logged as Minor CRs. The §11.4
  anti-trap is the most common scope-creep mechanism; this
  atom's discipline is the antidote.
- **Requester withdraws mid-process.** Mark the CR
  Withdrawn with rationale; keep in register for audit.
  Don't delete.
- **Classification dispute** (PM thinks Minor; Tech Lead
  thinks Moderate). Default to the higher classification;
  the cost of over-classifying is one extra meeting. The
  cost of under-classifying is silent scope creep.
- **CR has no business justification.** Halt; refuse to
  proceed. "Stakeholder asked" is not a justification —
  what business outcome does the change serve?
- **Major CR approved but Sponsor isn't available for
  re-baseline sign-off.** Mark the CR Approved-Pending-
  Re-baseline; work doesn't begin until re-baseline lands.
- **Multiple Major CRs in flight simultaneously.** Bundle
  for a single CCB review where dependencies allow; the
  re-baseline is more efficient combined than serial.

## References

No external `references/*.md` files yet — the §11 workflow
is the spine. The canonical authority is
`internal://site-build-procedure.md` §11. The user-invocable
`draft-change-request` is a peer skill producing the same
artifact via a different procedure.

## Self-Audit

Before declaring a CR complete, confirm:
- Sequential number assigned (no collision).
- All form fields filled (title, description, business
  justification, urgency, requester).
- Impact assessment has all five fields (effort, schedule,
  budget, risk, cross-cutting).
- Classification is justified (a one-line rationale, not
  just a label).
- Decision-maker matches the classification (PM for Minor;
  PM + PdM/PO for Moderate; CCB for Major).
- Decision is captured (Approved / Rejected / Deferred /
  Withdrawn) with rationale.
- Cross-references to `risk-register-author`,
  `master-schedule-author`, `adr-author`, `srs-author` are
  present where applicable.
