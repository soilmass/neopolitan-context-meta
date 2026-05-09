# site-build family — taxonomy

Stage 3 artifact for `family-bootstrap`. Tiered groups of atoms per
`../../context-meta-pipeline/skills/family-bootstrap/references/tier-model.md`.

The site-build SOP indexes 37 capabilities (see
`.bootstrap/capabilities.json`). One family cannot fit them all
within the 12-21 atom cap (Tier 1: 6-9 + Tier 2: 4-7 + Tier 3: 2-5).
This family scopes to the **methodology spine** — the deliverables
every project authors regardless of stack, scale, or industry.
Specialist long-tail deliverables (Phase 3 design system, Phase 7
late-stage analytics) are deferred to future site-* families.

Authority: `internal://site-build-procedure.md` (Edison Steele).

---

## Tier 1 — Essential (6 atoms)

Every project authors all of these. They form the load-bearing
spine across the 7-phase methodology — one anchor deliverable per
major phase, plus the cross-phase decision-recording skill.

| Atom | Role | SOP cite |
|---|---|---|
| `vision-author`           | Phase 1 — defines the project's why                | §4.2.5 |
| `persona-author`          | Phase 1 — defines who the project serves           | §4.2.3 |
| `srs-author`              | Phase 2 — defines what gets built (requirements)   | §5.1   |
| `adr-author`              | Phase 2-onward — records architectural decisions   | §5.3.6 |
| `runbook-author`          | Phase 5/6 — defines operational contract           | §8.8, §9.3 |
| `baseline-report-author`  | Phase 7 — proves the project worked at T+8 weeks   | §10.2.1 |

## Tier 2 — Specialist (5 atoms)

Specialist needs that frequently arise but aren't every-project
load-bearing.

| Atom | Role | SOP cite |
|---|---|---|
| `kpi-author`              | Phase 1 — measurement contract              | §4.2.6 |
| `risk-register-author`    | Phase 1+ — ongoing risk tracking            | §4.2.8, §5.7.3 |
| `threat-model-author`     | Phase 2 — STRIDE security baseline          | §5.3.7 |
| `privacy-plan-author`     | Phase 2 — privacy / DPIA baseline           | §5.6   |
| `master-schedule-author`  | Phase 2 — schedule + budget contract        | §5.7.1, §5.7.2 |

## Tier 3 — Long tail (5 atoms)

Documented as deferred *within this family* with **observable build
triggers**.

| Atom | Build trigger | SOP cite |
|---|---|---|
| `ost-author`                  | First persona+KPI pair authored AND project intends solution-tree mapping | §4.2.7 |
| `stakeholder-map-author`      | Project has ≥3 distinct stakeholder groups requiring RACI clarification  | §3, §4.2.2 |
| `design-philosophy-author`    | Phase 3 begins AND no existing design-philosophy doc                     | §6.1   |
| `weekly-metric-report-author` | Phase 7 begins AND ongoing weekly cadence committed                      | §10.5.1 |
| `change-request-author`       | First post-launch scope change requested                                  | §11.1  |

---

## In-family total

6 + 5 + 5 = **16 atoms.** Within the 12-21 cap declared by
family-bootstrap Stage 3 gate.

Router: `site-build` (per-family router; archetype=router; lists
all 16 atoms in its Routing Table).

---

## Out of Scope (this family) — deferred to future site-* families

The 21 capabilities below are out of the **site-build** family's
scope. Build triggers point to where they'd land:

### Future `site-design` family (Phase 3 design-system specialists)

Trigger: a real Phase-3 project authors ≥1 of these AND another ≥3
become near-term needs (capabilities ≥10 to pass family-bootstrap
Stage 2 gate, possibly stretched to include Phase 4 discovery-tick).

| Capability | Surface | SOP cite |
|---|---|---|
| `design-system-tokens`        | draft-design-system-tokens        | §6.4.1 |
| `component-states-matrix`     | draft-component-states-matrix     | §6.4.3 |
| `usability-synthesis`         | synthesize-usability-notes        | §6.3.3 |
| `engineering-handoff-spec`    | draft-handoff-spec                | §6 handoff |
| `discovery-tick`              | discovery-tick                    | §2.3, §7.6 |

### Future `site-operate` family (Phase 7 specialists)

Trigger: a real project enters Phase 7 stabilization AND ≥3 of these
become near-term needs.

| Capability | Surface | SOP cite |
|---|---|---|
| `stabilization-report`        | draft-stabilization-report        | §10.1 |
| `hypercare-digest`            | hypercare-digest                  | §10.1.1 |
| `diagnostic-sweep`            | diagnostic-sweep                  | §10.2.2 |
| `aeo-baseline`                | aeo-baseline                      | §10.2.3, §10.3.3 |
| `win-regression-report`       | draft-win-regression-report       | §10.2.4 |
| `optimization-backlog`        | draft-optimization-backlog        | §10.2.5 |
| `optimization-loop`           | optimization-loop                 | §10.3.1 |
| `monthly-stakeholder-report`  | monthly-stakeholder-report        | §10.5.2 |
| `quarterly-business-review`   | quarterly-business-review         | §10.5.3 |
| `annual-retrospective`        | annual-retro                      | §10 |

### Other Phase deliverables (deferred individually — each waits for its trigger)

| Capability | Reason | SOP cite |
|---|---|---|
| `discovery-findings-deck`     | Phase 1 synthesis derived from other Phase-1 outputs; skip-able if synthesis is done in narrative form | §4.3 |
| `communications-plan`         | Phase 2 governance specialist; needed when ≥2 stakeholder layers | §5.7.4 |
| `content-matrix`              | Phase 2 IA specialist; only when content-heavy site                | §5.4.2 |
| `ai-feature-spec`             | Phase 2; only when AI features are scoped in                      | §5.5.1 |
| `accessibility-conformance-statement` | Phase 5; only when WCAG-EM conformance claim is required   | §8.4 |
| `launch-comms`                | Phase 6 specialist                                                 | §9.4 |

---

## Stage 3 gate self-check

- ✓ Every capability from `capabilities.json` lands in exactly one tier OR Out of Scope.
- ✓ Tier 1 size: 6 (within 6-9).
- ✓ Tier 2 size: 5 (within 4-7).
- ✓ Tier 3 size: 5 (within 2-5).
- ✓ Every Tier 3 entry has an observable build trigger.
- ✓ Every Out-of-Scope entry has a build trigger or is documented as
  deliberately-skipped.

---

## Notes

- **Atom naming**: atoms use `<deliverable>-author` (no `site-build-`
  prefix), matching the meta-pipeline pattern where atoms are named
  for what they operate on (`skill-author`, not `meta-author`).
  Recorded as design-decision DD1 in `coverage.md`; finding
  B4/A60 would document this if family-bootstrap's Stage 4 prose
  needs clarification on the convention.
- **Stage 4 hand-off plan**: this session ends after Stage 3
  approval. Stage 4 (skill-author × 6 for Tier 1 atoms) begins the
  next session. The 6 Tier 1 atoms are the gate before Stages 5-6
  can run.
