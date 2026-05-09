---
name: privacy-plan-author
description: >
  Authors the project's Privacy and Compliance Plan. Documents
  applicable laws by jurisdiction (GDPR, CCPA/CPRA, Quebec Law 25,
  LGPD, DPDP, PIPL), data flow map, lawful basis per category,
  DPIA scaffold for high-risk processing, consent management UX,
  cookie audit, DSAR handling, sub-processor list, DPA review,
  privacy policy draft, and breach notification process. Writes to
  docs/02-requirements/privacy-plan.md (site-build-procedure.md
  §5.6). Use during Phase 2 after the data model is sketched. Do
  NOT use for: writing the threat model (use threat-model-author —
  that is attacker-capability focused, not lawful-basis focused);
  writing the full SRS (use srs-author); recording an architectural
  decision (use adr-author); strategic risk tracking (use
  risk-register-author).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.2.0
            Tier 2/3 expansion pass. Modeled on the user-invocable
            draft-privacy-plan skill but conformed to meta-pipeline
            frontmatter / required-section discipline.
---

# privacy-plan-author

Phase 2 — produce the project's Privacy and Compliance Plan with
optional DPIA scaffold.

## When to Use

- Phase 2 Requirements & Architecture is in progress; the data
  model (§5.3.3) is sketched; the privacy plan is the next
  privacy/legal deliverable.
- The project crosses jurisdictions (multi-region, cross-border
  data transfers) and the lawful-basis analysis must be
  documented per region.
- A new data-collection feature is scoped (analytics, surveys,
  user uploads, AI prompts containing PII) and requires DPIA-
  grade review.
- A regulator inquiry or breach has surfaced a gap; re-author or
  extend.

## When NOT to Use

- The data model is undefined — sketch it first (which entities
  exist, what fields per entity, what's PII).
- **Threat modeling** — `threat-model-author`. Privacy is about
  lawful basis and data flows; threats are about attacker
  capability. Both artifacts overlap on PII handling but are
  distinct.
- Writing the full SRS — `srs-author`. Privacy NFRs reference
  this plan but the SRS is its own artifact.
- Recording an architectural decision — `adr-author`.
- Strategic risk tracking — `risk-register-author`. Privacy
  risks (regulatory, reputational) appear in both, cross-linked.
- Drafting the **public-facing privacy policy** — that's a legal
  deliverable, downstream of this plan. This atom produces the
  internal plan; legal authors the public policy from it.
- Cookie consent banner UI — that's a Phase 3/4 design+build
  deliverable. This plan specifies the UX requirements.

## Capabilities Owned

- Document the **applicable laws by jurisdiction** per SOP §5.6:
  GDPR (EU/EEA + UK), CCPA/CPRA (California), Quebec Law 25
  (Canada), LGPD (Brazil), DPDP (India), PIPL (China), plus any
  emerging-jurisdiction laws relevant to the project's footprint.
- Author the **data flow map**: every personal-data category
  (identifiers, behavioral, financial, biometric, AI-prompt
  contents), where it's collected, where it flows, where it's
  stored, who can access it, retention period.
- Per data category capture **lawful basis**: GDPR options
  (consent, contract, legal obligation, vital interests, public
  task, legitimate interests). For consent: granularity, opt-in
  mechanism, audit trail.
- Produce a **DPIA scaffold** when high-risk processing is
  present: large-scale profiling, sensitive categories, vulnerable
  populations, automated decision-making with legal effect.
- Specify **consent management UX requirements**: banner shape,
  granular controls (analytics / marketing / functional), persist
  + audit-trail discipline.
- Author the **cookie audit** — every cookie set by the site or
  its sub-processors, classified by purpose.
- Document **DSAR handling** (Data Subject Access Request): how
  a user requests, who fulfills, SLA per jurisdiction.
- List **sub-processors** — every vendor that touches user
  data; require **DPA** (Data Processing Agreement) review per
  vendor.
- Document the **breach notification process**: who detects,
  who decides notification, statutory windows per jurisdiction
  (GDPR 72h, etc.), customer + regulator + employee
  communications.
- Write to `docs/02-requirements/privacy-plan.md`.

## Handoffs to Other Skills

- **From `srs-author`** — privacy NFRs hand off here for
  jurisdiction-specific analysis.
- **From `threat-model-author`** — overlapping concerns at PII
  handling and breach notification.
- **From `risk-register-author`** — privacy/regulatory risks
  hand off for DPIA-grade analysis.
- **To `srs-author`** — privacy NFR rows reference plan
  sections by stable ID.
- **To legal review** — the public-facing privacy policy is
  drafted by Privacy/Legal from this plan.
- **To `runbook-author`** — incident-response runbooks include
  the breach notification process.
- **From the user-invocable `draft-privacy-plan`** — peer skill.

## Edge Cases

- **Project doesn't process personal data.** Document that
  explicitly with a "no PII collected" stance + the boundaries
  that prevent PII collection (no analytics, no forms, no auth).
  Single-page plan instead of a full one.
- **Sub-processor refuses DPA review.** Halt; either find an
  alternative or capture as an accepted risk (Sponsor sign-off
  required).
- **Cross-border transfer with no SCC** (Standard Contractual
  Clauses) — halt; the transfer mechanism must be documented
  before the data flows.
- **AI integration** (per §5.5) collecting prompts. Add explicit
  prompt-PII handling (what's redacted before submission, what's
  retained by the model provider, model-provider DPA).
- **Cookie audit produces 50+ cookies.** Bucket by purpose;
  each purpose category gets a consent control. Refuse to ship
  100 toggle switches.

## References

No external `references/*.md` files yet. The canonical authority
is `internal://site-build-procedure.md` §5.6. The user-invocable
`draft-privacy-plan` is a peer skill producing the same artifact
via a different procedure.

## Self-Audit

Before declaring a privacy plan complete, confirm:
- Every applicable jurisdiction is named and addressed.
- Every personal-data category has a lawful basis.
- DPIA scaffold present if any high-risk processing is in scope.
- Consent UX requirements are concrete (granular categories,
  persist + audit-trail).
- Sub-processor list is complete with DPA-status per vendor.
- Breach notification process names statutory windows + named
  decision-maker for notification.
- DSAR handling specifies the SLA per jurisdiction.
