# `context-site-build` library map

Visual + textual dependency graph for the 75-skill library at v0.6.0.

---

## Top-level structure

```
context-site-build/
├── skills/                          ← 75 SKILL.md files
│   ├── site-build/                  ← per-family router (1)
│   ├── <16 site-build atoms>        ← Phase 1/2/5/6/7 spine
│   ├── site-design/                 ← per-family router (1)
│   ├── <14 site-design atoms>       ← Phase 3 + Awwwards-tier creative
│   ├── site-operate/                ← per-family router (1)
│   ├── <14 site-operate atoms>      ← Phase 5/6/7 ops + polish + awards
│   ├── house-site-{build,design,operate}-<stack>/  ← 15 stack overlays
│   ├── house-site-design-{motion,a11y,figma}/      ← 3 cross-stack/tool overlays
│   ├── house-site-operate-{vercel,cloudflare,netlify}/  ← 3 hosting overlays
│   └── <7 cross-cutting atoms>      ← perf / motion-conformance / analytics / AEO / i18n / observability / release
├── docs/                            ← v0.6.1 readiness documentation
├── coverage.md                      ← single-source-of-truth library coverage
├── CHANGELOG.md                     ← per-version release notes
├── SNAPSHOT.lock                    ← canonical skill-version + depends_on lock
└── verify.sh                        ← 4-step library validation
```

---

## Family roster (3)

### `site-build` family — methodology spine

```
Phase 1 Discovery     vision-author → persona-author → kpi-author → ost-author → stakeholder-map-author → risk-register-author
Phase 2 Requirements  srs-author → adr-author → threat-model-author → privacy-plan-author → master-schedule-author
Phase 3 Design        design-philosophy-author (handoff to site-design)
Phase 5/6 Hardening + Launch  runbook-author
Phase 7 Post-launch   baseline-report-author → weekly-metric-report-author
Cross-phase           change-request-author
```

### `site-design` family — Phase 3 + Awwwards-tier creative

```
Phase 3 Design (essential)   mood-board-author → art-direction-author → concept-author → motion-language-author → design-tokens-author → design-system-author → component-states-matrix-author
Phase 3 Design (specialist)  wireframe-author → prototype-author → usability-synthesis-author → a11y-annotations-author → engineering-handoff-spec-author
Phase 4 Build (continuous)   discovery-tick-author
Phase 4-5 (Awwwards-tier)    concept-prototyping-author
```

### `site-operate` family — Phase 5/6/7 ops + polish + awards

```
Phase 5 a11y                 conformance-statement-author
Phase 6 Launch               launch-comms-author
Phase 7 Stabilization        stabilization-report-author → hypercare-digest-author
Phase 7 Optimization         optimization-loop-author → optimization-backlog-author → diagnostic-sweep-author
Phase 7 Reports              monthly-stakeholder-report-author → quarterly-business-review-author → annual-retrospective-author → win-regression-report-author
Phase 7 AEO                  aeo-baseline-author
Awwwards-tier                polish-discipline-author → awards-submission-author
```

---

## Cross-family handoffs

```
site-build/design-philosophy-author
                ↓ (Phase 3 entry)
site-design/(all design atoms)
                ↓ (Phase 4 entry — engineering handoff)
[Phase 4 build — out of library scope]
                ↓ (Phase 5 entry)
site-build/runbook-author + site-operate/conformance-statement-author
                ↓ (Phase 6 entry — launch)
site-operate/launch-comms-author
                ↓ (Phase 7 entry — post-launch)
site-build/baseline-report-author + site-operate/(stabilization, hypercare, optimization, reports, AEO, polish, awards)
```

Cross-family citations (atoms that explicitly cite siblings in
other families):

- `site-design/art-direction-author` cites `site-build/vision-author` + `site-build/persona-author`
- `site-design/motion-language-author` cites `site-build/srs-author` (NFRs for motion budget)
- `site-operate/polish-discipline-author` cites `site-design/art-direction-author` + `site-design/motion-language-author` + `site-design/component-states-matrix-author`
- `site-operate/awards-submission-author` cites virtually every prior atom (the awards package is the cumulative output)
- `site-operate/optimization-loop-author` cites `site-build/srs-author` + `site-build/kpi-author` (guardrail metrics)

---

## Stack overlays (21) — composition diagram

```
For a Combo A (Next.js + Vercel) project, three overlays compose:

┌──────────────────────────────────────────────┐
│ Mechanism atoms (site-build / site-design /  │
│ site-operate families)                       │
│   srs-author  adr-author  runbook-author     │
│   design-tokens-author  motion-language-...   │
│   launch-comms-author   ...                  │
└──────────────────────────────────────────────┘
      ↑ overlay (CSS-cascade-style override)
┌──────────────────────────────────────────────┐
│ house-site-{build,design,operate}-nextjs     │
│ (3 framework-specific overlays)              │
└──────────────────────────────────────────────┘
      ↑ overlay (cross-stack patterns when present)
┌──────────────────────────────────────────────┐
│ house-site-design-motion (motion conventions)│
│ house-site-design-a11y   (a11y conventions) │
│ house-site-design-figma  (Figma pipeline)   │
└──────────────────────────────────────────────┘
      ↑ overlay (host-specific patterns)
┌──────────────────────────────────────────────┐
│ house-site-operate-vercel                    │
│ (host-specific conventions)                  │
└──────────────────────────────────────────────┘
```

The CSS-cascade rule: mechanism is the default; policy overrides;
lower-in-the-stack overlays specialize patterns the higher overlays
left general.

---

## Cross-cutting tool atoms (7) — relation to overlays

```
performance-budget-author   →   cited by all 15 stack-family overlays in their bundle-budget tables
motion-conformance-author    →   pairs with house-site-design-a11y; feeds conformance-statement-author
analytics-instrumentation-author → cited by kpi-author + 15 stack operate overlays + weekly-metric-report-author
aeo-schema-author            →   cited by aeo-baseline-author + 15 stack overlays for JSON-LD injection pattern
i18n-strategy-author         →   cited when target audience is multi-locale; cited by aeo-schema-author for hreflang
error-monitoring-setup-author → cited by runbook-author (incident); feeds release-discipline-author thresholds
release-discipline-author    →   cited by master-schedule-author + runbook-author + launch-comms-author
```

---

## Dependency direction (one-way)

| Layer | Depends on | Doesn't depend on |
|---|---|---|
| Cross-cutting atoms (7) | nothing in this library | overlays, family atoms |
| Family atoms (44) | nothing in this library at the SKILL.md level | overlays, cross-cutting atoms (cited via fallback for forward references) |
| Routers (3) | family atoms in their family | overlays, cross-cutting atoms |
| Stack overlays (15) | family mechanism atoms (via `depends_on:`) | cross-cutting atoms (cited via fallback) |
| Cross-stack overlays (3) | family mechanism atoms (motion-language-author, design-tokens-author, design-system-author, a11y-annotations-author, component-states-matrix-author, engineering-handoff-spec-author) | nothing else |
| Hosting overlays (3) | family mechanism atoms (runbook-author, launch-comms-author, optimization-loop-author, optimization-backlog-author) | other overlays |

**No cycles.** The library is a DAG.

---

## Where each output lives

| Atom output | File path |
|---|---|
| Vision | `docs/01-discovery/vision.md` |
| Personas | `docs/01-discovery/personas.md` |
| KPIs | `docs/01-discovery/kpis.md` |
| OST | `docs/01-discovery/ost.md` |
| Stakeholder map | `docs/01-discovery/stakeholders.md` |
| Risk register | `docs/01-discovery/risks.md` |
| SRS | `docs/02-requirements/srs.md` |
| ADRs | `docs/02-requirements/adr/<NNN>-<topic>.md` |
| Threat model | `docs/02-requirements/threat-model.md` |
| Privacy plan | `docs/02-requirements/privacy-plan.md` |
| Master schedule | `docs/02-requirements/schedule.md` |
| Design philosophy | `docs/03-design/design-philosophy.md` |
| Mood board | `docs/03-design/mood-board.md` |
| Art direction | `docs/03-design/art-direction.md` |
| Concept | `docs/03-design/concept.md` |
| Motion language | `docs/03-design/motion-language.md` |
| Tokens | `tokens/*.json` + `src/styles/tokens.css` |
| Design system | `docs/03-design/design-system.md` |
| Component states matrix | `docs/03-design/component-states.md` |
| Wireframes | `docs/03-design/wireframes.md` |
| Prototype | `docs/03-design/prototype.md` |
| Usability synthesis | `docs/03-design/usability.md` |
| A11y annotations | `docs/03-design/a11y-annotations.md` |
| Engineering handoff | `docs/03-design/handoff.md` |
| Concept prototyping | `docs/03-design/concept-prototype.md` |
| Discovery tick | `docs/04-build/discovery/<date>.md` |
| Performance budget | `docs/performance-budget.md` |
| Motion conformance | `docs/05-hardening/motion-conformance.md` |
| Analytics spec | `docs/analytics-spec.md` + `src/lib/analytics/events.ts` |
| AEO schema | `docs/aeo-schema-spec.md` + `src/lib/schema/<type>.ts` |
| i18n spec | `docs/i18n-spec.md` |
| Observability spec | `docs/observability-spec.md` + `src/lib/telemetry.ts` |
| Release plan | `docs/release-plan.md` + `deploy/feature-flags.yml` |
| Runbooks | `docs/05-hardening/runbooks/{deployment,incident,launch}.md` |
| Conformance statement | `docs/05-hardening/conformance.md` |
| Polish discipline | `docs/05-hardening/polish-plan.md` |
| Launch comms | `docs/06-launch/{internal,external,status}.md` |
| Baseline report | `docs/07-post-launch/baseline.md` |
| Stabilization report | `docs/07-post-launch/stabilization.md` |
| Hypercare digest | `docs/07-post-launch/hypercare/<date>.md` |
| Optimization loop | `docs/07-post-launch/experiments/<id>.md` |
| Optimization backlog | `docs/07-post-launch/optimization-backlog.md` |
| Diagnostic sweep | `docs/07-post-launch/diagnostics/<date>.md` |
| Weekly metric report | `docs/07-post-launch/weekly/<date>.md` |
| Monthly stakeholder report | `docs/07-post-launch/monthly/<date>.md` |
| Quarterly business review | `docs/07-post-launch/quarterly/<quarter>.md` |
| Annual retrospective | `docs/07-post-launch/annual/<year>.md` |
| AEO baseline | `docs/07-post-launch/aeo-baseline.md` |
| Win regression | `docs/07-post-launch/regressions/<id>.md` |
| Awards submission | `docs/07-post-launch/awards/<deadline>.md` |
| Change request | `docs/07-post-launch/changes/<id>.md` |

---

## See also

- `GETTING-STARTED.md` — pick a stack + shape; quickstart.
- `walkthroughs/<shape>.md` — phase-by-phase walkthroughs.
- `VERSIONING-POLICY.md` — SemVer + v1.0 freeze contract.
- `coverage.md` — single-source-of-truth coverage with audit-
  finding ledger.
- `examples/outputs/` — anonymized real outputs to compare against.
