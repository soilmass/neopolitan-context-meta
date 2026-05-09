---
name: threat-model-author
description: >
  Authors the project's Threat Model + Security Baseline. Uses
  STRIDE (or similar) per architectural component to enumerate
  threats; documents mitigations, security headers baseline,
  authentication and session model, authorization model, secret
  management, supply-chain hardening, and vulnerability disclosure
  policy. Writes to docs/02-requirements/threat-model.md
  (site-build-procedure.md §5.3.7). Use during Phase 2 after the
  technical architecture is sketched. Do NOT use for: writing the
  full SRS (use srs-author); recording an architectural decision
  (use adr-author); writing the privacy plan (use privacy-plan-author
  — that is privacy/DPIA-focused, not threat-focused); writing the
  strategic risk register (use risk-register-author).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.2.0
            Tier 2/3 expansion pass. Modeled on the user-invocable
            draft-threat-model skill but conformed to meta-pipeline
            frontmatter / required-section discipline.
---

# threat-model-author

Phase 2 — produce the project's STRIDE-shaped threat model and
security baseline.

## When to Use

- Phase 2 Requirements & Architecture is in progress; the
  technical architecture (§5.3.1 stack selection) and integration
  map (§5.3.5) are sketched; the threat model is the next
  security deliverable.
- A new high-impact integration is added mid-build (e.g.,
  payments, identity provider, third-party data) and its threat
  surface needs analysis.
- A regulatory milestone (SOC 2 prep, ISO 27001, EU AI Act) has
  surfaced a need for documented threat enumeration.
- A security incident has revealed a gap in the existing model;
  re-author or extend.

## When NOT to Use

- The technical architecture is undefined — sketch it first
  (see `srs-author` Phase 2 Architecture sub-section) before
  enumerating threats against missing components.
- Writing the full SRS — `srs-author`. Security NFRs reference
  this threat model but the SRS is its own artifact.
- Recording an architectural decision (e.g., "we adopt OAuth
  via Auth.js") — `adr-author`. ADRs are decisions; threat
  models are analyses against decisions.
- Privacy / DPIA work — `privacy-plan-author`. Privacy is
  data-flow + lawful-basis focused; the threat model is
  attacker-capability focused. They overlap on PII handling but
  are distinct artifacts.
- Strategic risk tracking — `risk-register-author`. Threats and
  risks overlap; both artifacts cross-reference each other.
- Penetration test reports — those are Phase 5 hardening
  artifacts, downstream of this model.

## Capabilities Owned

- Enumerate threats per component using **STRIDE** (or a similar
  framework — DREAD, PASTA, OWASP ASVS): **Spoofing**,
  **Tampering**, **Repudiation**, **Information disclosure**,
  **Denial of service**, **Elevation of privilege**.
- For each threat: assign **severity** (Critical / High /
  Medium / Low), document **mitigations** with named owner.
- Document the **security baseline** per SOP §5.3.7:
  - **Security headers** (CSP, X-Frame-Options, X-Content-Type-Options,
    Referrer-Policy, Permissions-Policy, HSTS w/ preload).
  - **Authentication and session model** (provider, MFA policy,
    SSO posture, session lifetime, password policy).
  - **Authorization model** (RBAC / ABAC / both).
  - **Secret management** (vault tool, rotation policy, never-in-
    repo discipline).
  - **Supply-chain hardening** (dependency pinning, SBOM
    generation, signed releases).
  - **Vulnerability disclosure policy** (security.txt, disclosure
    contact, response SLA).
- Cite the **OWASP Top 10** mitigations explicitly per item.
- Cross-reference: each threat that maps to an architectural
  decision links to the relevant `adr-author` artifact; each
  threat that overlaps a strategic risk links to the
  `risk-register-author` artifact.
- Write to `docs/02-requirements/threat-model.md`.

## Handoffs to Other Skills

- **From `srs-author`** — security NFRs hand off here for
  per-threat coverage.
- **From `adr-author`** — ADRs that affect security posture
  (auth choice, hosting model, integration patterns) feed the
  threat enumeration.
- **From `risk-register-author`** — security-flavored risks
  hand off for STRIDE-grade analysis.
- **To `srs-author`** — security NFR rows reference threat
  model rows by stable ID.
- **To `runbook-author`** — incident-response runbooks reference
  the threat model for triage paths.
- **To `privacy-plan-author`** — overlapping concerns at PII
  handling, breach notification, and consent integrity.
- **From the user-invocable `draft-threat-model`** — peer skill.

## Edge Cases

- **No architecture yet.** Halt; the threat model needs concrete
  components to enumerate against. Sketch the architecture first
  (or do a high-level threat sketch, marked provisional, with
  re-enter after architecture lands).
- **Component is a third-party SaaS.** Document the boundary;
  enumerate threats at the boundary (data flowing in/out,
  authentication, fallback when unavailable per §5.3.5).
- **Threat enumeration produces 100+ rows.** Bucket by
  severity; require mitigation owners only for Critical/High;
  Medium/Low get a "watch" disposition that re-evaluates at
  Phase 5 hardening.
- **Mitigation is "accept the risk".** Acceptable if and only
  if Sponsor sign-off is captured + the risk is logged in the
  risk register's accepted-risks section.
- **AI integration** present (per §5.5). Add prompt-injection,
  PII-leak-in-prompts, and model-availability threats explicitly.

## References

No external `references/*.md` files yet. The canonical authority
is `internal://site-build-procedure.md` §5.3.7. The user-invocable
`draft-threat-model` is a peer skill producing the same artifact
via a different procedure.

## Self-Audit

Before declaring a threat model complete, confirm:
- Every architectural component has at least one row of STRIDE
  enumeration (or an explicit "no threats applicable" with
  justification).
- Every Critical/High threat has a named owner + a mitigation
  (no `TBD` for Critical/High).
- OWASP Top 10 mitigations are documented per item.
- Security headers baseline is concrete (named policy strings,
  not "tighten CSP").
- Cross-references to `adr-author` and `risk-register-author`
  are present where applicable.
