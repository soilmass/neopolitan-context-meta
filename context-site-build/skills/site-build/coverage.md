# site-build Coverage

Authority: `internal://site-build-procedure.md` — Edison Steele —
"site-build-procedure.md, 7-phase site/web-app methodology"

Last verification: 2026-05-08 (initial bootstrap; Tier 1 authored).

## In Scope (Tier 1)

| Atom | Owns | Last health check |
|---|---|---|
| `vision-author`           | Phase 1 — Vision & Value Proposition document (§4.2.5) | 2026-05-08 (fresh) |
| `persona-author`          | Phase 1 — evidence-backed persona per audience segment (§4.2.3) | 2026-05-08 (fresh) |
| `srs-author`              | Phase 2 — SRS scaffold with FR + NFR (§5.1) | 2026-05-08 (fresh) |
| `adr-author`              | Cross-phase — single architectural decision record (§5.3.6) | 2026-05-08 (fresh) |
| `runbook-author`          | Phase 5/6 — deployment / incident / launch runbook (§8.8, §9.3) | 2026-05-08 (fresh) |
| `baseline-report-author`  | Phase 7 — T+8-week post-launch baseline report (§10.2.1) | 2026-05-08 (fresh) |

Plus the per-family router `site-build` (archetype: router; v0.1.0; fresh).

## Specced, Not Yet Built (Tier 2)

| Atom | Key concepts | Edge cases | Folds into |
|---|---|---|---|
| `kpi-author`              | KPI taxonomy, leading vs lagging, target thresholds, measurement methodology | KPI without baseline; persona-less KPI; vanity metrics | `vision-author` (vision currently owns success-criteria; KPI-author splits the quantitative half out) |
| `risk-register-author`    | Risk × likelihood × impact × owner × mitigation × residual | Risks with shared mitigation; risks across phases | `vision-author` (vision currently has implicit out-of-scope; risk register makes risks explicit) |
| `threat-model-author`     | STRIDE applied per attack surface; security NFRs traceback | Authentication-system-of-systems; third-party integrations | `srs-author` (SRS NFRs currently absorb security threshold lines) |
| `privacy-plan-author`     | DPIA scaffold; data-flow mapping; consent + retention policy | Cross-border data; processor / sub-processor chains | `srs-author` (SRS privacy NFRs currently absorb requirement lines) |
| `master-schedule-author`  | Phase / milestone / deliverable timeline; budget rollup | Compressed timelines; vendor-dependent milestones | (no Tier 1 absorbs; gap is honest — schedule lives outside the methodology spine) |

Trigger to build any of the 5: a real Phase-1 / Phase-2 project needs the conformant skill.

## Deferred (Tier 3)

| Atom | Build trigger |
|---|---|
| `ost-author`                  | First persona+KPI pair authored AND project intends solution-tree mapping |
| `stakeholder-map-author`      | Project has ≥3 distinct stakeholder groups requiring RACI clarification |
| `design-philosophy-author`    | Phase 3 begins AND no existing design-philosophy doc |
| `weekly-metric-report-author` | Phase 7 begins AND ongoing weekly cadence committed |
| `change-request-author`       | First post-launch scope change requested |

## Policy Overlay

No policy overlay exists for this family. When a stack-specific
overlay is needed (e.g., `house-site-build-nextjs` extending
`runbook-author` for Next.js deploy specifics), authoring will go
through `skill-policy-overlay` in the meta-pipeline.

## Out of Scope

Load-bearing section per `family-bootstrap/references/coverage-template.md`.

| Capability | Why out of scope | Where to look instead |
|---|---|---|
| Phase 3 design-system specialists (tokens, component-states, usability synthesis, handoff spec) | Distinct family with its own router; Phase 3 has narrower expertise than the spine | Future `site-design` family — see library-root `coverage.md` Domains Deferred |
| Phase 4 ongoing-discovery synthesis (`discovery-tick`) | Single-atom, recurring-cadence scope; doesn't fit a family bootstrap | Future `site-design` family OR direct `skill-author` invocation |
| Phase 5 a11y conformance statement | Single deliverable, narrow specialist scope | Author via `skill-author` directly OR future `site-hardening` family |
| Phase 6 launch communications | Single deliverable; cadence-dependent | Future `site-operate` family OR direct `skill-author` invocation |
| Phase 7 long-tail (stabilization, hypercare, weekly/monthly/QBR/annual reports, diagnostic sweep, AEO baseline, optimization loop / backlog, win/regression) | Distinct family with its own router; Phase 7 capabilities cohere as a family | Future `site-operate` family — see library-root `coverage.md` Domains Deferred |
| Discovery findings deck (§4.3) | Synthesis derived from other Phase-1 outputs; skip-able when narrative substitutes | Manual prose write-up after Phase 1 atoms run |
| Communications plan (§5.7.4) | Phase 2 governance specialist; only when ≥2 stakeholder layers | Author via `skill-author` directly when triggered |
| Content matrix (§5.4.2) | Phase 2 IA specialist; only for content-heavy sites | Author via `skill-author` directly when triggered |
| AI feature spec (§5.5.1-§5.5.3) | Phase 2 specialist; only when AI features are scoped | Author via `skill-author` directly when triggered |
| Methodology authoring itself (the SOP doc) | The SOP is the authority, not an output | Edit `internal://site-build-procedure.md` directly |
| Stack-specific runbooks (Next.js, Astro, etc.) | Belongs in a stack adapter, not the methodology spine | `house-site-build-nextjs` overlay (when authored) |
| The website code itself (components, routes, hooks) | Build artifact, not methodology output | The project's own repo |

## Coverage Matrix Status

Last `skill-audit` run: 2026-05-08 (advisory Stage 6 audit during
family-bootstrap). All 7 skills (router + 6 atoms) at health: `fresh`.
Drift gate not yet meaningfully applicable (descriptions just authored).

Tier transitions since last verification: none (initial bootstrap).
