---
name: site-build
description: >
  Routes site-build deliverable-authoring prompts to the right atom in
  the site-build family. Dispatches between vision-author / persona-
  author / srs-author / adr-author / runbook-author / baseline-report-
  author (Tier 1) plus the Tier 2 / 3 specialist atoms when they exist.
  Use when the operator names a phase deliverable but no specific
  atom — e.g., "draft the vision", "write requirements", "we need a
  runbook". Do NOT use for: meta-pipeline lifecycle work (use the
  meta router in context-meta-pipeline); domains other than site-
  build (use that domain's router); authoring a skill (use skill-
  author); auditing a skill (use skill-audit); bootstrapping a new
  library (use library-bootstrap).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: router
  tags: [router, daily-use]
  changelog: |
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

- The operator names a deliverable (vision, persona, SRS, ADR,
  runbook, baseline report, …) without specifying which atom should
  produce it.
- The operator describes a phase (Phase 1 discovery, Phase 2
  requirements, Phase 5/6 hardening + launch, Phase 7 post-launch)
  and the next deliverable to produce isn't named.
- The operator says "draft the …", "write the …", "we need a …" for
  any artifact in the site-build SOP.
- The operator asks "which skill should I use to author X" where X
  is one of the 16 atoms claimed by this family (Tier 1 / 2 / 3 in
  `taxonomy.md`).

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
| Software requirements / FR + NFR / spec | `srs-author` |
| Single architectural decision / ADR / record-this-decision | `adr-author` |
| Deployment / incident / launch runbook | `runbook-author` |
| Post-launch baseline report at T+8 weeks | `baseline-report-author` |

The 10 Tier 2 / 3 atoms documented in `taxonomy.md` are not yet
built. Prompts for those intents fall through to the user-invocable
peers in the operator's environment (`draft-kpi-doc`,
`draft-risk-register`, `draft-threat-model`, `draft-privacy-plan`,
`draft-master-schedule`, `draft-ost`, `draft-stakeholder-map`,
`draft-design-philosophy`, `weekly-metric-report`,
`draft-change-request`). When a Tier 2 / 3 atom gets built via
`skill-author`, this router's Routing Table picks it up at the
PATCH bump.

## Disambiguation Protocol

When two atoms could plausibly handle a prompt:

- **Vision vs persona**: vision is a one-page why-the-project-exists
  artifact; persona is per-segment evidence-backed. If the prompt
  describes the project, route to `vision-author`. If the prompt
  describes a user, route to `persona-author`.
- **SRS vs ADR**: SRS captures FR/NFR rows; ADR captures one
  architectural decision. If the prompt names a *requirement* or
  *acceptance criterion*, route to `srs-author`. If the prompt
  names a *choice between alternatives*, route to `adr-author`.
- **Runbook vs ADR**: ADR records the decision (e.g., "we deploy via
  canary"); runbook records the procedure (e.g., "the canary deploy
  steps are 1, 2, 3 with rollback at step 2"). Decision → ADR;
  procedure → runbook.
- **Runbook vs baseline report**: runbook is forward-looking (what
  to do); baseline report is backward-looking (what happened).
- **Baseline report vs Tier 3 reports**: baseline is the T+8-week
  snapshot. Weekly / monthly / QBR / annual are different cadences
  with different audiences (handed off to deferred Tier 3 atoms).
- **When the prompt spans phases**: ask the operator which deliverable
  they're producing right now. The router does not fan out across
  multiple deliverables.

## Atoms in This Family

Tier 1 (built; routed):

- `vision-author`
- `persona-author`
- `srs-author`
- `adr-author`
- `runbook-author`
- `baseline-report-author`

Tier 2 (Specced, Not Yet Built — see `taxonomy.md`):

- `kpi-author`
- `risk-register-author`
- `threat-model-author`
- `privacy-plan-author`
- `master-schedule-author`

Tier 3 (Specced, Not Yet Built — see `taxonomy.md`):

- `ost-author`
- `stakeholder-map-author`
- `design-philosophy-author`
- `weekly-metric-report-author`
- `change-request-author`

## Self-Audit

Before declaring a routing decision:

- The chosen atom's `## When to Use` section names the prompt's
  trigger phrasing OR a clear paraphrase.
- The chosen atom's `## When NOT to Use` does NOT exclude the
  current prompt.
- If two atoms could fit, the **Disambiguation Protocol** above
  was consulted and the choice is justified.
- If the prompt is for a deferred atom, the operator is told
  explicitly that the atom is Specced, Not Yet Built (vs silently
  routing to the wrong place).
