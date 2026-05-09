# site-operate family — taxonomy

Stage 3 artifact for `family-bootstrap`. Tiered groups of atoms per
`../../context-meta-pipeline/skills/family-bootstrap/references/tier-model.md`.

The site-operate family covers Phase 5 hardening (a11y conformance
specifically — perf + security live in `srs-author` NFRs and
`threat-model-author`), Phase 6 launch (launch communications), and
Phase 7 post-launch (stabilization, measurement, ongoing
optimization, monthly + quarterly + annual reports). Plus the
Awwwards-tier "polish discipline" and "awards submission" phases
the SOP doesn't have as named deliverables.

Authority (composite):
- Primary: `internal://site-build-procedure.md` §8.2 (Accessibility)
  + §9 (Phase 6 Launch) + §10 (Phase 7 Post-Launch). Edison Steele.
- Secondary: `docs/research/SYNTHESIS.md` (Awwwards-tier polish +
  awards from E2 §C.3 and §C.6).

---

## Tier 1 — Essential (7 atoms)

The every-project spine. From Phase 5 a11y through Phase 6 launch
through Phase 7 stabilization + ongoing optimization.

| Atom | Role | Primary cite |
|---|---|---|
| `stabilization-report-author`    | 30-day stabilization report at hypercare window close                                  | SOP §10.1 + §10.5 implicit |
| `hypercare-digest-author`        | Daily hypercare memo during weeks 1-4 — error rate, perf, conversion, hot issues       | SOP §10.1.1 |
| `launch-comms-author`            | Launch communications — internal + external + status-page entries                      | SOP §9.4 |
| `conformance-statement-author`   | WCAG 2.2 Accessibility Conformance Statement at Phase 5 close                          | SOP §8.2.7 |
| `optimization-backlog-author`    | Prioritized optimization backlog (RICE/ICE-scored) at T+8; ongoing through Phase 7    | SOP §10.2.5 |
| `optimization-loop-author`       | Single experimentation cycle (hypothesize → design → build → run → analyze → decide)   | SOP §10.3.1 |
| `polish-discipline-author`       | Polish phase plan — areas to polish, budget, polish gate / readiness criteria          | research/E2 §C.3 (Active Theory) |

## Tier 2 — Specialist (5 atoms)

| Atom | Role | Primary cite |
|---|---|---|
| `monthly-stakeholder-report-author` | Monthly stakeholder report consolidating 4 weekly memos                              | SOP §10.5.2 |
| `quarterly-business-review-author`  | QBR — comprehensive metrics + ROI + competitive + strategic recommendations          | SOP §10.5.3 |
| `win-regression-report-author`      | Win/regression report at T+8 — wins, regressions, surprises, stable                  | SOP §10.2.4 |
| `diagnostic-sweep-author`           | Phase 7 diagnostic sweep — heatmaps, funnels, surveys, form analytics, perf, a11y    | SOP §10.2.2 |
| `aeo-baseline-author`               | AI Search baseline — manual prompt testing across ChatGPT / Perplexity / AI Overviews | SOP §10.2.3 + §10.3.3 |

## Tier 3 — Long tail (2 atoms)

| Atom | Build trigger | Primary cite |
|---|---|---|
| `annual-retrospective-author`    | Year mark of post-launch operations; triggers annual retro + roadmap proposal       | SOP §10 (named in §12) |
| `awards-submission-author`       | Operator decides to submit for Awwwards SOTD / Honors / SOTM / SOTY                  | research/E2 §C.6 (Ueno's Phase 6 "Awards (optional)") |

---

## In-family total

7 + 5 + 2 = **14 atoms.** Within the 12-21 cap declared by
family-bootstrap Stage 3 gate.

Router: `site-operate` (per-family router; archetype=router; lists
all 14 atoms in its Routing Table).

---

## Out of Scope (this family)

Considered and explicitly out-of-scoped — fold into existing atoms
or belong to other families.

| Capability | Why out of scope | Where it lives instead |
|---|---|---|
| `baseline-report-author` (T+8 baseline) | Already in `site-build` Tier 1 (v0.1.0 decision) | `site-build/baseline-report-author` — cross-link from `win-regression-report-author` here |
| `weekly-metric-report-author` (Phase 7 weekly cadence) | Already in `site-build` Tier 3 (v0.2.0) | `site-build/weekly-metric-report-author` — `monthly-stakeholder-report-author` consolidates four of these |
| `change-request-author` (cross-phase scope changes) | Already in `site-build` Tier 3 (v0.2.0) | `site-build/change-request-author` |
| Phase 5 functional QA test plan | Sprint output, not a named SOP deliverable; QA Lead owns it directly | Project's test management tool (Linear, Jira, etc.) |
| Phase 5 performance verification report | Folds into `srs-author`'s NFR rows being passed/failed | `srs-author` (site-build) NFRs |
| Phase 5 security review report | Folds into `threat-model-author`'s mitigations being verified | `threat-model-author` (site-build) |
| Phase 5 SEO baseline audit | Folds into `aeo-baseline-author` (this family Tier 2) for AI search; classic SEO baseline lives in marketing tooling | `aeo-baseline-author` here + Search Console / Ahrefs |
| Content audit (§10.3.4) | Folds into `optimization-backlog-author` (this family Tier 1) and ongoing content-team work | `optimization-backlog-author` |
| Performance trend analysis (§10.3.5) | Folds into `optimization-loop-author` (each cycle measures perf delta) and a future `performance-budget-author` | `optimization-loop-author` here + future cross-cutting tool |
| A11y maintenance (§10.3.6 quarterly re-audit) | Folds into `conformance-statement-author` re-issue + `a11y-annotations-author` (site-design) for new components | `conformance-statement-author` here + `a11y-annotations-author` (site-design) |
| Polish discipline applied to a single artifact (per-page polish) | Implementation is per-feature-area, not a methodology atom | Project's own design + dev work |
| Awwwards Conference talk authoring | Out of methodology scope | Operator-driven talk preparation |
| Stakeholder onboarding for ongoing-ops team | Operational handoff is procedural, not skill-driven | SOP §10.1.5 operator-driven checklist |

---

## Stage 3 gate self-check

- ✓ Every capability from `capabilities.json` lands in exactly one tier OR Out of Scope.
- ✓ Tier 1 size: 7 (within 6-9).
- ✓ Tier 2 size: 5 (within 4-7).
- ✓ Tier 3 size: 2 (within 2-5).
- ✓ Every Tier 3 entry has an observable build trigger.
- ✓ Every Out-of-Scope entry names where it lives instead.

---

## Notes

- **Atom naming**: atoms use `<deliverable>-author` matching the
  site-build and site-design family conventions.
- **Relationship to site-build family**: site-operate covers Phase
  5/6/7 specialist deliverables. Three Phase 5/6/7 spine atoms
  remain in site-build by v0.1.0–v0.2.0 decisions
  (baseline-report-author, weekly-metric-report-author,
  change-request-author); cross-linked from this family's
  related atoms.
- **Relationship to site-design family**: site-design produces the
  Phase 3 design + creative artefacts; site-operate consumes them
  during launch + post-launch (e.g., `polish-discipline-author`
  references `art-direction-author`'s polish criteria;
  `optimization-loop-author` references `motion-language-author`'s
  performance budget).
- **Relationship to draft-* user-invocable peers**: 12 of 14 atoms
  have user-invocable peers (`draft-stabilization-report`,
  `hypercare-digest`, `draft-launch-comms`, `draft-conformance-
  statement`, `draft-optimization-backlog`, `optimization-loop`,
  `monthly-stakeholder-report`, `quarterly-business-review`,
  `draft-win-regression-report`, `diagnostic-sweep`, `aeo-baseline`,
  `annual-retro`). 2 are Awwwards-tier additions with no peer:
  `polish-discipline-author` and `awards-submission-author`.
