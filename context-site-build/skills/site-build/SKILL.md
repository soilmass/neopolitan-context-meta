---
name: site-build
description: >
  Routes site-build deliverable-authoring prompts to the right atom in
  the site-build family. Dispatches across all 16 atoms covering
  Phase 1 discovery (vision / persona / kpi / ost / stakeholder /
  risk register), Phase 2 requirements (srs / adr / threat model /
  privacy / master schedule), Phase 3 design (design philosophy),
  Phase 5/6 hardening + launch (runbook), Phase 7 post-launch
  (baseline report / weekly report), and cross-phase change control.
  Use when the operator names a deliverable but no specific atom —
  e.g., "draft the vision", "write requirements", "we need a runbook",
  "log a change request". Do NOT use for: meta-pipeline lifecycle
  work (use the meta router in context-meta-pipeline); domains other
  than site-build (use that domain's router); authoring a skill (use
  skill-author); auditing a skill (use skill-audit); bootstrapping a
  new library (use library-bootstrap).
license: Apache-2.0
metadata:
  version: "0.1.2"
  archetype: router
  tags: [router, daily-use]
  changelog: |
    v0.1.2 — patch: 10 Tier 2/3 atoms now built (v0.2.0 of library);
            Routing Table extended to cover all 16 in-family atoms.
            "Atoms in This Family" no longer has Specced-Not-Yet-
            Built rows. Disambiguation Protocol extended for the
            new atoms. Description rewritten to enumerate the
            full atom set.
    v0.1.1 — patch: Routing Table no longer includes deferred Tier 2/3
            atoms (B8/A64) — 10 of 16 rows previously pointed at
            unbuilt skills, polluting routing-eval signal. Deferred
            atoms remain documented in "Atoms in This Family" and
            in `taxonomy.md`; Disambiguation Protocol covers the
            fall-back to user-invocable peers.
    v0.1.0 — initial. Authored as part of family-bootstrap Stage 4
            during the v0.7.0 first-real-consumer dogfood. Routing
            Table covered 6 Tier 1 atoms plus 10 deferred targets;
            v0.1.1 dropped the deferred rows.
---

# site-build

Per-family router for the site-build cluster in the context-site-build
library. Dispatches operator prompts to the deliverable-authoring atom
that owns the artifact.

## When to Use

- The operator names a deliverable (vision, persona, KPI, OST,
  stakeholder map, risk register, SRS, ADR, threat model, privacy
  plan, master schedule, design philosophy, runbook, baseline report,
  weekly report, change request) without specifying which atom should
  produce it.
- The operator describes a phase (Phase 1 discovery, Phase 2
  requirements, Phase 3 design, Phase 5/6 hardening + launch, Phase 7
  post-launch) and the next deliverable to produce isn't named.
- The operator says "draft the …", "write the …", "we need a …" for
  any artifact in the site-build SOP.
- The operator asks "which skill should I use to author X" where X
  is one of the 16 atoms claimed by this family.

## When NOT to Use

- The operator names a specific atom directly (`vision-author`,
  `persona-author`, etc.) — invoke that atom, no routing needed.
- The prompt is about the meta-pipeline lifecycle (authoring,
  auditing, refactoring, retiring skills) — that's the `meta`
  router in `context-meta-pipeline`.
- The prompt is about a non-site-build domain (git, postgres, etc.) —
  out of scope; route to that domain's router (when it exists).
- The prompt is about scaffolding a new project from scratch — the
  user-invocable `bootstrap-site-project` handles that.
- The prompt asks to author a SKILL.md itself — that's `skill-
  author` in `context-meta-pipeline`.

## Routing Table

| Intent | Target atom |
|---|---|
| Project vision / value proposition / why-the-project-exists | `vision-author` |
| Persona for one audience segment | `persona-author` |
| KPI / measurement contract / success metrics | `kpi-author` |
| Opportunity Solution Tree / persona pains → opportunities → solutions | `ost-author` |
| Stakeholder map / RACI / decision matrix | `stakeholder-map-author` |
| Risk register / premortem / risk × likelihood × impact | `risk-register-author` |
| Software Requirements Specification / FR + NFR / spec | `srs-author` |
| Single architectural decision / ADR / record-this-decision | `adr-author` |
| Threat model / STRIDE / security baseline | `threat-model-author` |
| Privacy plan / DPIA / consent management | `privacy-plan-author` |
| Master schedule / budget / critical path | `master-schedule-author` |
| Design philosophy / brand expression / tone | `design-philosophy-author` |
| Deployment / incident / launch runbook | `runbook-author` |
| Post-launch baseline report at T+8 weeks | `baseline-report-author` |
| Weekly metric memo for Sponsor + product trio | `weekly-metric-report-author` |
| Change request / scope / schedule / budget change | `change-request-author` |

The 16 atoms cover the methodology spine of the site-build SOP.
Phases 3 (Design specialists beyond design-philosophy), Phase 4
(continuous discovery), Phase 5 (a11y conformance), Phase 6 (launch
comms), and Phase 7 long-tail (stabilization, hypercare, win-
regression, optimization-loop, monthly / quarterly / annual reports)
are out of scope for this family — see `coverage.md` Out of Scope
for the future `site-design` and `site-operate` families that will
absorb them. User-invocable peers exist for those out-of-scope
deliverables (`draft-design-system-tokens`, `discovery-tick`,
`draft-conformance-statement`, `draft-launch-comms`,
`draft-stabilization-report`, etc.).

## Disambiguation Protocol

When two atoms could plausibly handle a prompt:

- **Vision vs persona**: vision is a one-page why-the-project-exists
  artifact; persona is per-segment evidence-backed. If the prompt
  describes the project, route to `vision-author`. If the prompt
  describes a user, route to `persona-author`.
- **Vision vs KPI**: vision is qualitative success criteria; KPI is
  measurable thresholds. "Why this project exists" → vision; "how
  we'll know it succeeded numerically" → KPI.
- **Persona vs stakeholder map**: persona = end-user segments;
  stakeholder map = internal decision-makers and external
  influencers. Don't conflate.
- **OST vs SRS**: OST is opportunities → candidate solutions
  (working artifact, refined throughout); SRS is the locked
  functional + non-functional spec. Solutions in the OST become
  candidate FRs in the SRS only after pruning.
- **SRS vs ADR**: SRS captures FR/NFR rows; ADR captures one
  architectural decision. If the prompt names a *requirement* or
  *acceptance criterion*, route to `srs-author`. If the prompt
  names a *choice between alternatives*, route to `adr-author`.
- **Threat model vs risk register**: threat model is security-
  focused (STRIDE per component); risk register is strategic
  (commercial, organizational, regulatory, schedule). Both
  cross-link when a risk overlaps a threat.
- **Threat model vs privacy plan**: threat model is attacker-
  capability focused; privacy plan is lawful-basis + data-flow
  focused. Both overlap on PII handling.
- **Risk register vs change request**: risk register tracks what
  *might* go wrong; change request tracks what's *being* changed.
  A risk firing may trigger a CR.
- **Master schedule vs change request**: master schedule is the
  baseline plan; change requests can re-baseline it. Major CRs
  hand off to `master-schedule-author` for the re-baseline.
- **Runbook vs ADR**: ADR records the decision (e.g., "we deploy
  via canary"); runbook records the procedure (e.g., "the canary
  deploy steps are 1, 2, 3 with rollback at step 2"). Decision
  → ADR; procedure → runbook.
- **Runbook vs baseline report**: runbook is forward-looking
  (what to do); baseline report is backward-looking (what
  happened).
- **Baseline report vs weekly report**: baseline is the T+8-week
  one-time snapshot; weekly is the recurring memo. Different
  cadences, different depths, different audiences.
- **Baseline report vs out-of-scope reports**: monthly /
  quarterly / annual / win-regression / stabilization reports
  belong to the future `site-operate` family. User-invocable
  peers cover them now.
- **Design philosophy vs vision**: vision is business-outcome
  focused; design philosophy is visual / experiential focused.
  Both exist and cross-reference.
- **When the prompt spans phases**: ask the operator which
  deliverable they're producing right now. The router does not
  fan out across multiple deliverables.

## Atoms in This Family

All 16 atoms are built and live (v0.2.0 of library).

**Phase 1 — Discovery & Strategy:**

- `vision-author`
- `persona-author`
- `kpi-author`
- `ost-author`
- `stakeholder-map-author`
- `risk-register-author`

**Phase 2 — Requirements & Architecture:**

- `srs-author`
- `adr-author`
- `threat-model-author`
- `privacy-plan-author`
- `master-schedule-author`

**Phase 3 — Design (spine only):**

- `design-philosophy-author`

**Phase 5 / 6 — Hardening + Launch (spine only):**

- `runbook-author`

**Phase 7 — Post-Launch (spine only):**

- `baseline-report-author`
- `weekly-metric-report-author`

**Cross-phase:**

- `change-request-author`

Other Phase 3 / 4 / 5 / 6 / 7 deliverables are out-of-scope for
this family (see `coverage.md` Out of Scope) and will live in
future `site-design` and `site-operate` families. User-invocable
peers cover them now.

## Self-Audit

Before declaring a routing decision:

- The chosen atom's `## When to Use` section names the prompt's
  trigger phrasing OR a clear paraphrase.
- The chosen atom's `## When NOT to Use` does NOT exclude the
  current prompt.
- If two atoms could fit, the **Disambiguation Protocol** above
  was consulted and the choice is justified.
- If the prompt is for an out-of-scope deliverable (Phase 3 design
  specialist, Phase 4/5/6/7 long-tail), the operator is told
  explicitly that this family doesn't cover it and pointed at the
  user-invocable peer or the future family.
