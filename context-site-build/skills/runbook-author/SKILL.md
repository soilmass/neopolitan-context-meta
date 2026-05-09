---
name: runbook-author
description: >
  Authors a runbook scaffold for one of three kinds — deployment,
  incident response, or launch. Captures pre-conditions, step-by-step
  procedure, rollback, escalation contacts, and observable signals at
  each step. Writes docs/05-hardening/runbooks/<kind>.md per
  site-build-procedure.md §8.8 and §9.3. Used at Phase 5 hardening
  and Phase 6 launch readiness. Do NOT use for: writing the SRS
  (use srs-author); recording an architectural decision (use
  adr-author); writing the launch communications (handled by the
  future site-operate family; the user-invocable draft-launch-comms
  covers it now); writing the post-launch baseline report (use
  baseline-report-author); ongoing daily / weekly operations digests
  (handled by the future site-operate family; the user-invocable
  hypercare-digest and weekly-metric-report cover it now).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.1 — patch: anti-triggers re-framed for out-of-scope siblings
            as "future site-operate family; user-invocable peer covers
            it now" rather than "(when built)" (B6/A62 + B7/A63);
            "Authority surface" reframed; deferred references/
            template.md row dropped.
    v0.1.0 — initial. Authored via skill-author during the v0.7.0
            first-real-consumer dogfood. Modeled on the user-invocable
            draft-runbook skill.
---

# runbook-author

Phase 5 / 6 — produce one runbook (deployment, incident, or launch).

## When to Use

- Phase 5 hardening; the production deploy procedure needs a
  documented runbook before it goes live.
- An on-call rotation is being established and the team needs an
  incident response runbook (alert → triage → mitigation →
  postmortem path).
- Phase 6 launch is ≤2 weeks out and a launch-day runbook (cutover
  steps, comms, rollback decision tree) is required.
- An existing runbook is failing in practice (steps are skipped, the
  rollback path doesn't work) — re-author rather than patch.

## When NOT to Use

- Documenting requirements — `srs-author`.
- Documenting a single decision that informed the runbook — that
  decision is an `adr-author` artifact; the runbook references it.
- Writing the launch announcement / status-page entry — that's
  `launch-comms-author` (deferred to a future `site-operate` family;
  the user-invocable `draft-launch-comms` covers it now). Runbook-
  author handles the *operations*, not the *messaging*.
- Writing a post-launch report — `baseline-report-author`.
- Setting up a recurring digest cadence — handled by the future
  `site-operate` family. The user-invocable `hypercare-digest` and
  `weekly-metric-report` cover it now.
- Patching one runbook step — edit the doc directly.

## Capabilities Owned

- Author one of three runbook kinds, identified at intake:
  - **deployment**: routine deploy/release procedure.
  - **incident**: alert → triage → mitigation → postmortem.
  - **launch**: one-time cutover (Phase 6).
- Capture **pre-conditions**: required state, required permissions,
  on-call expectations.
- Author the **step-by-step procedure** as a numbered list. Each step
  has: action, expected observable signal (log line, metric, UI
  state), and the named human or system that performs it.
- Document the **rollback path** explicitly — every deploy/incident/
  launch runbook has one; refuses to ship without it.
- Document **escalation contacts** by named role (not by personal
  contact info — those go in a separate ops-roster file).
- Note **time-bounding**: expected duration, SLA on intermediate
  steps, total deadline before rollback decision.
- Write to `docs/05-hardening/runbooks/<kind>.md` where `<kind>` ∈
  {deployment, incident, launch}.

## Handoffs to Other Skills

- **From `srs-author`** — operational NFRs (RTO, RPO, alerting
  thresholds) hand off into runbook authoring.
- **From `adr-author`** — ADRs that affect operations (e.g., "we
  deploy via canary") feed the runbook's procedure section.
- **To `baseline-report-author`** — Phase 7 baseline references
  what the runbook claimed about RTO/RPO; the baseline measures
  actual.
- **To external ops tooling** — runbooks are the source of truth
  for Pagerduty / Opsgenie / status-page playbooks. The atom does
  not author those tools' content; it authors the source doc the
  tools mirror.

## Edge Cases

- **The team has no rollback path** (e.g., destructive migration
  with no reverse). Author the runbook with a `## Rollback: NONE
  — pre-flight gate`, and surface the gap loudly. The runbook
  refuses to ship clean if rollback is "we hope this works."
- **Runbook is for a one-off (like a launch) with no precedent**.
  Mark `## Status: First Run`; explicitly note that the runbook is
  hypothetical until executed. Re-author after the first run with
  observed-vs-expected diffs.
- **Multiple deploy environments** (staging, prod, DR). Author one
  runbook per environment if the procedures differ; author one
  shared runbook with an environment-keyed parameter table if they
  don't.
- **On-call coverage is unstaffed at the planned launch time**. Halt;
  this is a `comms-plan-author` / `stakeholder-map-author` problem
  before this atom can author honestly.

## References

No external `references/*.md` files yet — one template per kind
(deployment / incident / launch) becomes the obvious reference set
on the first real authoring run. The canonical authority is
`internal://site-build-procedure.md` §8.8 and §9.3.

## Self-Audit

Before declaring a runbook complete, confirm:
- Kind declared at the top (deployment / incident / launch).
- Rollback path present and concretely actionable (not "revert the
  deploy" — name how).
- Each step has an observable signal an operator can look for.
- Escalation contacts are by role (not personal).
- Time-bound: expected duration + abort-decision deadline named.
