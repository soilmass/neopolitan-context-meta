---
name: launch-comms-author
description: >
  Authors launch communications at Phase 6 — internal Slack /
  all-hands brief + customer-facing email / blog / social /
  in-product announcement + status-page entry for any maintenance
  window. Output at docs/06-launch/comms/{internal, external,
  status-page}.md (SOP §9.4). Use across Phase 6 launch readiness,
  T-1d through T+3d. Do NOT use for: launch-day runbook (use
  runbook-author in site-build family — that is operational, this
  is messaging); incident communications (use the runbook's
  incident-response section); ongoing weekly stakeholder updates
  (use weekly-metric-report-author in site-build family);
  customer support documentation (separate artifact; out of scope
  here).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.4.0
            site-operate family bootstrap. Modeled on the
            user-invocable draft-launch-comms skill but conformed
            to meta-pipeline frontmatter / required-section
            discipline.
---

# launch-comms-author

Phase 6 — produce launch communications.

## When to Use

- Phase 6 launch is ≤7 days out; communications need drafting
  + sponsor approval before T-1d.
- A re-launch or major feature drop is upcoming and needs
  parallel comms.
- A planned-downtime cutover needs a status-page entry +
  customer email pre-staged.

## When NOT to Use

- Launch-day runbook — `runbook-author` (site-build family).
  Comms is the messaging layer; runbook is the operational
  procedure (deploy steps, rollback, escalation contacts).
- Incident communications — those live inside the incident-
  response runbook; not a separate launch artifact.
- Ongoing weekly stakeholder updates —
  `weekly-metric-report-author` (site-build family).
- Customer support documentation (help center / FAQ) —
  separate artifact; content team / support team owns it.
- Internal training / employee onboarding for a new feature —
  not a launch comms artifact.
- Marketing campaigns extending beyond the launch window — out
  of scope; comms here is the launch-and-immediate-followup
  set, not the ongoing nurture.

## Capabilities Owned

- Author the **internal communications** per SOP §9.4.1:
  - **Pre-launch** — scheduled all-hands brief content.
  - **Launch-day** — real-time launch channel content
    (dedicated Slack channel or equivalent).
  - **Post-launch** — company-wide announcement (short;
    includes thanks; includes link).
  - **Postmortem invite** — scheduled within 7 days
    regardless of outcome.
- Author the **customer / external communications** per §9.4.2:
  - **Pre-launch teaser** (when appropriate) — build
    anticipation.
  - **Launch announcement** — email + blog + social + product
    surface.
  - **In-product communication** — what's-new modal, banner,
    or notification dot.
  - **Documentation update** — help center / docs site
    reflects changes.
  - **Follow-up nurture** plan over 1-2 weeks for adoption.
- Author the **status-page entry** per §9.4.3:
  - Pre-staged maintenance window if planned.
  - Update template for any unplanned incident.
  - Cadence (every 30 min during incident).
  - Tone (honest; no spin).
- Maintain **versioned drafts** — internal + external + status
  copy goes through review (sponsor for the framing; legal
  for any compliance language; brand for tone).
- Cite **vision** + **launch plan** + **runbook** by stable
  name — comms reflects the project's positioning.
- Write to `docs/06-launch/comms/{internal, external,
  status-page}.md`.

## Handoffs to Other Skills

- **From `vision-author`** (site-build) — vision frames the
  external announcement.
- **From `master-schedule-author`** (site-build) — launch date
  + windows.
- **From `runbook-author`** (site-build) — launch-day runbook
  references the comms artifacts; status-page updates are
  triggered by runbook events.
- **To `stabilization-report-author`** — comms posture during
  hypercare references the launch comms baseline.
- **To `awards-submission-author`** (Tier 3) — launch comms
  artefacts (the announcement post, the blog, the social
  thread) become inputs to the awards submission package.
- **From the user-invocable `draft-launch-comms`** — peer
  skill producing the same artifact via a different
  procedure.

## Edge Cases

- **Stealth launch** — minimal external comms; internal
  Slack-only. Document the stealth posture explicitly so
  the next launch knows what was tried.
- **Coordinated cross-product launch** (multi-team). Comms
  needs cross-team review; surface the dependency early
  (T-2w minimum lead time).
- **Regulated industry** (healthcare, finance) requiring
  legal review on every external comm. Build the review
  cycle into the schedule; refuse to ship without
  documented sign-off.
- **In-product comms collide with active feature flags**
  (modal shown to users who don't have the feature).
  Coordinate with the feature-flag rollout via
  `optimization-loop-author` to gate the modal.
- **Status page goes down during incident.** Have a backup
  channel (Twitter / X, customer email) pre-arranged in
  the incident-response runbook.
- **Post-launch announcement goes out before launch
  completes** (timezone error). Pre-schedule everything
  with conditional hold-pending-go signals; refuse silent
  publishing.

## References

No external `references/*.md` files yet. The canonical
authority is `internal://site-build-procedure.md` §9.4. The
user-invocable `draft-launch-comms` is a peer skill producing
the same artifact via a different procedure.

## Self-Audit

Before declaring launch comms complete, confirm:
- Internal: pre-launch + launch-day + post-launch + postmortem
  comms drafted.
- External: pre-launch teaser (if applicable) + launch
  announcement (≥3 channels: email/blog/social) + in-product
  comm + docs update + follow-up nurture plan.
- Status page: pre-staged maintenance + incident update
  template + cadence rule.
- Legal / brand / sponsor reviews captured per regulatory
  context.
- Cross-references to vision + master schedule + runbook.
- Backup status channel if status page goes down.
