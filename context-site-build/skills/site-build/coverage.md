# site-build Coverage

Authority: `internal://site-build-procedure.md` — Edison Steele —
"Website & Web Application Build Procedure (v2.0); 7-phase
methodology"; canonical local path
`/home/edox1/Public/neopolitan/docs/claude-docs/site-build-procedure.md`.

Last verification: 2026-05-09 (v0.2.0 — 10 Tier 2/3 atoms authored;
all 16 in-family atoms now built).

Previous verification: 2026-05-08 (initial bootstrap; Tier 1
authored; library v0.1.0–v0.1.2).

## In Scope (Tier 1) — 6 atoms

| Atom | Owns | Last health check |
|---|---|---|
| `vision-author`           | Phase 1 — Vision & Value Proposition document (§4.2.5) | 2026-05-08 (healthy, drift 0.0%) |
| `persona-author`          | Phase 1 — evidence-backed persona per audience segment (§4.2.3) | 2026-05-08 (healthy, drift 4.2%) |
| `srs-author`              | Phase 2 — SRS scaffold with FR + NFR (§5.1) | 2026-05-08 (healthy, drift 8.8%) |
| `adr-author`              | Cross-phase — single architectural decision record (§5.3.6) | 2026-05-08 (healthy, drift 6.7%) |
| `runbook-author`          | Phase 5/6 — deployment / incident / launch runbook (§8.8, §9.3) | 2026-05-08 (healthy, drift 8.3%) |
| `baseline-report-author`  | Phase 7 — T+8-week post-launch baseline report (§10.2.1) | 2026-05-08 (healthy, drift 3.2%) |

Plus the per-family router `site-build` (archetype: router; v0.1.2; healthy).

## In Scope (Tier 2) — 5 atoms (newly built v0.2.0)

| Atom | Owns | Last health check |
|---|---|---|
| `kpi-author`              | Phase 1 — KPI & Success Metrics document (§4.2.6) | 2026-05-09 (fresh) |
| `risk-register-author`    | Phase 1 onward — Risk Register with categories + premortem (§4.2.8, §5.7.3) | 2026-05-09 (fresh) |
| `threat-model-author`     | Phase 2 — STRIDE threat model + security baseline (§5.3.7) | 2026-05-09 (fresh) |
| `privacy-plan-author`     | Phase 2 — Privacy & Compliance Plan + DPIA scaffold (§5.6) | 2026-05-09 (fresh) |
| `master-schedule-author`  | Phase 2 — Master Schedule & Budget plan (§5.7.1, §5.7.2) | 2026-05-09 (fresh) |

## In Scope (Tier 3) — 5 atoms (newly built v0.2.0)

| Atom | Owns | Build trigger | Last health check |
|---|---|---|---|
| `ost-author`                  | Phase 1 sketch / Phase 2 refinement — Opportunity Solution Tree (§4.2.7) | First persona+KPI pair authored AND project intends solution-tree mapping | 2026-05-09 (fresh) |
| `stakeholder-map-author`      | Phase 1 — Stakeholder Map and decision matrix (§3, §4.2.1) | Project has ≥3 distinct stakeholder groups requiring RACI clarification | 2026-05-09 (fresh) |
| `design-philosophy-author`    | Phase 3 — one-page design philosophy (§6.1) | Phase 3 begins AND no existing design-philosophy doc | 2026-05-09 (fresh) |
| `weekly-metric-report-author` | Phase 7 — weekly metric memo for Sponsor + product trio (§10.5.1) | Phase 7 begins AND ongoing weekly cadence committed | 2026-05-09 (fresh) |
| `change-request-author`       | Cross-phase — single Change Request (§11.1) | First post-launch scope change requested | 2026-05-09 (fresh) |

## Specced, Not Yet Built

None — all 16 in-family atoms are now built (v0.2.0).

## Policy Overlay

No policy overlay exists for this family yet. Stack-specific
overlays (`house-site-build-nextjs`, `house-site-build-r3f`,
`house-site-build-astro`) are queued for Phase 4 of the v0.2.x
expansion plan per `docs/ARCHITECTURE-OPTIONS-v0.2.md`. Authoring
goes through `skill-policy-overlay` in the meta-pipeline.

## Out of Scope

Load-bearing section per `family-bootstrap/references/coverage-template.md`.

| Capability | Why out of scope | Where to look instead |
|---|---|---|
| Phase 3 design-system specialists (tokens, component-states, usability synthesis, handoff spec) | Distinct family with its own router; Phase 3 has narrower expertise than the spine | Future `site-design` family — see library-root `coverage.md` Domains Deferred |
| Phase 4 ongoing-discovery synthesis (`discovery-tick`) | Single-atom, recurring-cadence scope; doesn't fit a family bootstrap | Future `site-design` family OR direct `skill-author` invocation |
| Phase 5 a11y conformance statement | Single deliverable, narrow specialist scope | Author via `skill-author` directly OR future `site-hardening` family |
| Phase 6 launch communications | Single deliverable; cadence-dependent | Future `site-operate` family OR direct `skill-author` invocation |
| Phase 7 long-tail (stabilization, hypercare, monthly/QBR/annual reports, diagnostic sweep, AEO baseline, optimization loop / backlog, win/regression) | Distinct family with its own router; Phase 7 capabilities cohere as a family | Future `site-operate` family — see library-root `coverage.md` Domains Deferred |
| Discovery findings deck (§4.3) | Synthesis derived from other Phase-1 outputs; skip-able when narrative substitutes | Manual prose write-up after Phase 1 atoms run |
| Communications plan (§5.7.4) | Phase 2 governance specialist; only when ≥2 stakeholder layers | Author via `skill-author` directly when triggered |
| Content matrix (§5.4.2) | Phase 2 IA specialist; only for content-heavy sites | Author via `skill-author` directly when triggered |
| AI feature spec (§5.5.1-§5.5.3) | Phase 2 specialist; only when AI features are scoped | Author via `skill-author` directly when triggered |
| Methodology authoring itself (the SOP doc) | The SOP is the authority, not an output | Edit `internal://site-build-procedure.md` directly |
| Stack-specific runbooks (Next.js, Astro, etc.) | Belongs in a stack adapter, not the methodology spine | `house-site-build-<stack>` overlays (queued for v0.2.x Phase 4) |
| The website code itself (components, routes, hooks) | Build artifact, not methodology output | The project's own repo |

## Coverage Matrix Status

Last `skill-audit` run: 2026-05-09 (post-Tier-2/3 author).

- Tier 1 (6 atoms): all `healthy`; drift 0.0%–8.8% (≤10% threshold).
- Tier 2 (5 atoms): all `fresh` (just authored); audit in P1.5.
- Tier 3 (5 atoms): all `fresh` (just authored); audit in P1.5.
- Router `site-build`: `healthy` after v0.1.2 update.

Tier transitions since last verification:
- All 5 Tier 2 atoms: Specced, Not Yet Built → In Scope (Tier 2)
- All 5 Tier 3 atoms: Deferred (Tier 3) → In Scope (Tier 3)
- 16-atom family complete; the deferred queue is now empty (out-of-
  scope rows remain for the `site-design` and `site-operate`
  families that will be bootstrapped in later phases of the v0.2.x
  expansion plan).
