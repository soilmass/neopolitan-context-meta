---
name: risk-register-author
description: >
  Authors the project's Risk Register — risk × likelihood × impact ×
  owner × mitigation × residual, with categories Technical,
  Commercial, Organizational, Regulatory, Schedule, External. Uses
  the premortem technique. Writes to docs/01-discovery/risk-register.md
  (live spreadsheet form per site-build-procedure.md §4.2.8 and
  §5.7.3). Use during Phase 1 Discovery and at every phase boundary
  to add new risks. Do NOT use for: writing the project vision (use
  vision-author); persona authoring (use persona-author); writing
  the KPI set (use kpi-author); writing the threat model (use
  threat-model-author — that is security-focused, not strategic);
  writing the privacy plan (use privacy-plan-author); recording an
  architectural decision (use adr-author).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [rare]
  changelog: |
    v0.1.0 — initial. Authored via skill-author during the v0.2.0
            Tier 2/3 expansion pass. Modeled on the user-invocable
            draft-risk-register skill but conformed to meta-pipeline
            frontmatter / required-section discipline.
---

# risk-register-author

Phase 1 onward — produce and maintain the project Risk Register.

## When to Use

- Phase 1 Discovery; the initial risk register is one of the eight
  Phase 1 deliverables (Gate 1 requires top-five risks with
  mitigations + owners).
- A phase boundary has been crossed and new risks have surfaced
  (Phase 2 architecture decisions, Phase 4 sprint reality, etc.).
- A premortem session has surfaced new risks the operator wants
  captured.
- An incident or near-miss has surfaced a risk that should now
  be tracked.

## When NOT to Use

- Project vision is undefined — `vision-author` first.
- Persona authoring — `persona-author`.
- KPI / measurement work — `kpi-author`. KPI degradation may be a
  risk, but the KPI doc is its own artifact.
- **Threat modeling** — `threat-model-author`. The threat model is
  security-focused (STRIDE per component); the risk register is
  strategic (commercial, organizational, regulatory, schedule).
  These are different artifacts with different audiences.
- Privacy / DPIA work — `privacy-plan-author`.
- Recording an architectural decision — `adr-author`.
- Logging an incident — that's an ops artifact, not a risk
  register entry. Risks become incidents only when they fire.

## Capabilities Owned

- Capture each risk with all six fields: **risk statement**
  (one sentence), **likelihood** (Low / Medium / High or numeric
  1–5), **impact** (same scale), **owner** (named individual),
  **mitigation strategy**, **residual risk** after mitigation.
- Categorize each risk per SOP §4.2.8: **Technical**, **Commercial**,
  **Organizational**, **Regulatory**, **Schedule**, **External**.
- Run a **premortem** when bootstrapping the register: *"It's 6
  months from now. The project failed. Why?"* — silent writing
  for 5 minutes per participant; group themes; rank.
- Maintain the register as a **live spreadsheet** (or
  spreadsheet-shaped markdown table) — risks are added, mitigated,
  retired, or escalated to incidents over the project lifecycle.
- Cross-reference: every risk that maps to an architectural
  decision links to the relevant `adr-author` artifact; every
  security-flavored risk links to the `threat-model-author`
  artifact (or notes that one will exist at Phase 2).
- Identify **top-five risks** explicitly — these are the ones the
  Sponsor reviews at every phase gate.
- Write to `docs/01-discovery/risk-register.md` (initial in
  Phase 1; updated continuously through Phase 7).

## Handoffs to Other Skills

- **From `vision-author`** — the vision's stated outcome surfaces
  the risks of *not achieving* it.
- **From the kickoff workshop** (initial risk surface per §4.2.1).
- **To `master-schedule-author`** — schedule risks feed the
  schedule's contingency budget (10–20% per §5.7.1).
- **To `adr-author`** — risks that can only be mitigated by an
  architectural decision hand off here.
- **To `threat-model-author`** — security-flavored risks hand off
  for STRIDE-grade analysis.
- **To `privacy-plan-author`** — privacy/regulatory risks hand
  off for DPIA-grade analysis.
- **To phase-gate reviews** — top-5 risks are reviewed by Sponsor
  at every gate (Phase 1: top-5 with mitigations + owners is a
  Gate 1 criterion).
- **From the user-invocable `draft-risk-register`** — peer skill.

## Edge Cases

- **Premortem produces 50+ risks.** Bucket them; pick top-15;
  rank top-5; defer the rest to a "watch" list. The register is
  not a brainstorm dump.
- **A risk is also a security threat.** Both artifacts exist;
  cross-link. The risk register row says "see threat model
  T-007"; the threat model row says "see risk register R-014."
- **A risk fires (becomes an incident).** Move it from "active
  risk" to "realized risk — see incident #N"; the register
  retains the row for project archeology.
- **A risk has no owner.** Halt; refuse to ship the row. An
  unowned risk is a risk that won't be mitigated.
- **A risk has no mitigation.** Acceptable if and only if the
  risk is genuinely accepted (Sponsor sign-off). Default state
  must be "mitigation TBD with deadline."

## References

No external `references/*.md` files yet. The canonical authority
is `internal://site-build-procedure.md` §4.2.8 (initial) and
§5.7.3 (Phase 2 update). The user-invocable `draft-risk-register`
is a peer skill producing the same artifact via a different
procedure.

## Self-Audit

Before declaring a risk register update complete, confirm:
- Top-5 risks are explicitly named (the Sponsor-review set).
- Each risk has all six fields filled (no `TBD` mitigations
  without a deadline).
- Each risk has an owner (named individual; not "the team").
- Categories are one of the six per SOP §4.2.8 (no novel
  categories without an explicit ADR).
- Cross-references to `adr-author` / `threat-model-author` /
  `privacy-plan-author` are present where the risk overlaps
  those artifacts.
