# site-operate Coverage

Authority (composite):
- Primary: `internal://site-build-procedure.md` §8.2
  (Accessibility) + §9 (Phase 6 Launch) + §10 (Phase 7 Post-
  Launch) — Edison Steele — "Website & Web Application Build
  Procedure (v2.0)"; canonical local path
  `/home/edox1/Public/neopolitan/docs/claude-docs/site-build-procedure.md`.
- Secondary: `internal://docs/research/SYNTHESIS.md` (Awwwards-
  tier research, 2026-05-08) — adds polish-discipline + awards-
  submission named phases per E2 §C.3 + §C.6.

Last verification: 2026-05-09 (initial bootstrap; all 14
in-family atoms authored).

## In Scope (Tier 1) — 7 atoms

| Atom | Owns | Last health check |
|---|---|---|
| `stabilization-report-author`    | 30-day stabilization report at hypercare close (SOP §10.1) | 2026-05-09 (fresh) |
| `hypercare-digest-author`        | Daily hypercare memo during weeks 1-4 (SOP §10.1.1)        | 2026-05-09 (fresh) |
| `launch-comms-author`            | Launch communications — internal + external + status-page (SOP §9.4) | 2026-05-09 (fresh) |
| `conformance-statement-author`   | WCAG 2.2 Accessibility Conformance Statement (SOP §8.2.7) | 2026-05-09 (fresh) |
| `optimization-backlog-author`    | Prioritized optimization backlog with RICE / ICE (SOP §10.2.5) | 2026-05-09 (fresh) |
| `optimization-loop-author`       | Single experimentation cycle (SOP §10.3.1)                | 2026-05-09 (fresh) |
| `polish-discipline-author`       | Polish phase plan + per-iteration notes (research/E2 §C.3 Active Theory) | 2026-05-09 (fresh) |

Plus the per-family router `site-operate` (archetype: router; v0.1.0; fresh).

## In Scope (Tier 2) — 5 atoms

| Atom | Owns | Last health check |
|---|---|---|
| `monthly-stakeholder-report-author` | Monthly stakeholder report consolidating 4 weeklies (SOP §10.5.2) | 2026-05-09 (fresh) |
| `quarterly-business-review-author`  | QBR — metrics + ROI + competitive + strategic recommendations (SOP §10.5.3) | 2026-05-09 (fresh) |
| `win-regression-report-author`      | Win/regression at T+8 (SOP §10.2.4)                                | 2026-05-09 (fresh) |
| `diagnostic-sweep-author`           | Phase-7 diagnostic sweep across 7 method areas (SOP §10.2.2)       | 2026-05-09 (fresh) |
| `aeo-baseline-author`               | AI Search baseline across 5 engines (SOP §10.2.3 + §10.3.3)        | 2026-05-09 (fresh) |

## In Scope (Tier 3) — 2 atoms

| Atom | Owns | Build trigger | Last health check |
|---|---|---|---|
| `annual-retrospective-author`    | Annual retrospective + roadmap proposal (SOP §10 named in §12)              | One year of post-launch operations | 2026-05-09 (fresh) |
| `awards-submission-author`       | Awwwards / SOTD / SOTM / SOTY submission package (research/E2 §C.6 Ueno's "Awards (optional)") | Operator decides to submit; polish-discipline has shipped | 2026-05-09 (fresh) |

## Specced, Not Yet Built

None — all 14 in-family atoms are now built.

## Policy Overlay

No policy overlay exists for this family yet. Stack-specific
overlays (`house-site-operate-vercel`, `house-site-operate-
cloudflare`, etc. for hosting-specific runbook patterns) are
queued for Phase 4 of the v0.2.x expansion plan per
`docs/ARCHITECTURE-OPTIONS-v0.2.md`. Authoring goes through
`skill-policy-overlay` in the meta-pipeline.

## Out of Scope

| Capability | Why out of scope | Where to look instead |
|---|---|---|
| `baseline-report-author` (T+8 baseline) | Already in `site-build` Tier 1 (v0.1.0 decision) | `site-build/baseline-report-author` — `win-regression-report-author` here cross-references it |
| `weekly-metric-report-author` (Phase 7 weekly cadence) | Already in `site-build` Tier 3 (v0.2.0) | `site-build/weekly-metric-report-author` — `monthly-stakeholder-report-author` here consolidates four of these |
| `change-request-author` (cross-phase scope changes) | Already in `site-build` Tier 3 (v0.2.0) | `site-build/change-request-author` |
| `runbook-author` (deployment / incident / launch runbooks) | Already in `site-build` Tier 1 (v0.1.0); cross-references launch comms | `site-build/runbook-author` |
| Phase 5 functional QA test plan | Sprint output, not a named SOP deliverable; QA Lead owns directly | Project's test management tool (Linear, Jira, etc.) |
| Phase 5 performance verification report | Folds into `srs-author`'s NFRs being verified pass / fail | `srs-author` (site-build) NFRs |
| Phase 5 security review report | Folds into `threat-model-author`'s mitigations being verified | `threat-model-author` (site-build) |
| Classic SEO baseline (Search Console / Ahrefs / Semrush) | Operator-driven; AEO baseline (this family) is the AI-search counterpart | Marketing tooling |
| Content audit (§10.3.4) | Folds into `optimization-backlog-author` (this family) and content-team work | `optimization-backlog-author` |
| Performance trend analysis (§10.3.5) | Folds into `optimization-loop-author` per-experiment perf measurement + a future `performance-budget-author` cross-cutting tool | `optimization-loop-author` here + future cross-cutting tool |
| A11y maintenance (§10.3.6 quarterly re-audit) | Folds into `conformance-statement-author` re-issue + `a11y-annotations-author` (site-design) for new components | `conformance-statement-author` here + `a11y-annotations-author` (site-design) |
| Awwwards Conference talk authoring | Out of methodology scope | Operator-driven talk preparation |
| Stakeholder onboarding for ongoing-ops team | Operational handoff is procedural, not skill-driven | SOP §10.1.5 operator-driven checklist |
| Marketing case studies for sales | Different audience than awards-submission; can be derived but separate scope | Adjacent marketing artefact (out of family) |

## Coverage Matrix Status

Last `skill-audit` run: 2026-05-09 (Stage 6 advisory audit
during family-bootstrap).

- Tier 1 (7 atoms): all `fresh` (just authored); audit in P3.6.
- Tier 2 (5 atoms): all `fresh`; audit in P3.6.
- Tier 3 (2 atoms): all `fresh`; audit in P3.6.
- Router `site-operate`: `fresh`.

Tier transitions since last verification: none (initial
bootstrap). 14-atom family fully built at v0.1.0; no Specced-
Not-Yet-Built queue carried forward.
