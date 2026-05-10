# Getting started with `context-site-build`

For a second consumer (a teammate, a collaborator, or future-you on
a new project) — this is the doc that tells you which atoms to invoke
in what order, what to expect at each step, and how to wire the
library into a real project.

If you're new to the meta-pipeline first: see `context-meta-pipeline/
README.md`. Then come back here.

---

## What this library is

`context-site-build` is a **methodology library** for site/web-app
projects. It encodes a 7-phase SOP (Discovery → Requirements →
Design → Build → Hardening → Launch → Post-launch) plus Awwwards-
tier creative additions (mood-board, art-direction, concept,
motion-language, polish-discipline, awards-submission) as 75 skills
across 3 families + 21 stack overlays + 7 cross-cutting tools.

**You don't need all 75 skills.** You need the subset for your
project shape. This document tells you which subset.

---

## The five stack combos

Pick one (or pick "no stack overlay" — the methodology atoms work
stack-agnostic, the overlays just make them sharper):

| Combo | Stack | Pick when |
|---|---|---|
| **A** "React-cinematic" | Next.js + Vercel + Sanity + R3F + GSAP | Default for marketing + product sites with React expertise |
| **B** "Vue/Nuxt-cinematic" | Nuxt 3 + Tailwind + Pinia + TresJS | Vue shop; visual-edit-heavy CMS (Storyblok) |
| **C** "Astro-static-with-WebGL-islands" | Astro + Vite + Tailwind + islands | Performance-pure marketing sites; Astro shop |
| **D** "Svelte/SvelteKit, performance-pure" | SvelteKit + adapter + vanilla Three.js | Performance-pure brand promise; Igloo Inc-style hero-WebGL |
| **Webflow** | Webflow Designer + CMS | No-code visual-editor projects; client-content-heavy marketing |

The rest of this guide assumes you've picked one. If you're picking
between A and C, read each combo's `house-site-build-{stack}` SKILL
description; the SRS NFRs differ in load-bearing ways.

---

## Your project shape

Pick the shape closest to yours:

| Shape | Walkthrough |
|---|---|
| Marketing site (multi-page, content-driven, no auth) | `walkthroughs/marketing-site.md` |
| E-commerce (catalog + cart + checkout) | `walkthroughs/e-commerce.md` |
| Web app (CRUD-heavy, auth, dashboards) | `walkthroughs/web-app.md` |
| Microsite / campaign (single-page, time-bounded, motion-heavy) | `walkthroughs/microsite.md` |

The walkthroughs name the exact atom invocation order for each
shape, including which Tier 1 atoms are core vs which are skippable.

---

## Quickstart for a new project

For a marketing site on Next.js + Vercel (Combo A) — the most common
path. Adapt for your stack/shape from the walkthroughs.

### Phase 1 — Discovery (week 1-2)

```text
1. Invoke vision-author       → docs/01-discovery/vision.md
2. Invoke persona-author      → docs/01-discovery/personas.md
3. Invoke kpi-author          → docs/01-discovery/kpis.md
4. Invoke ost-author          → docs/01-discovery/ost.md (optional)
5. Invoke stakeholder-map-author → docs/01-discovery/stakeholders.md
6. Invoke risk-register-author → docs/01-discovery/risks.md
```

**Gate before Phase 2**: vision + personas + KPIs sign-off from
the operator.

### Phase 2 — Requirements (week 2-3)

```text
1. Invoke srs-author          → docs/02-requirements/srs.md
   (cite house-site-build-nextjs SRS conventions)
2. Invoke adr-author          → docs/02-requirements/adr/000X-<topic>.md
   (write the 8 Combo-A ADRs from house-site-build-nextjs)
3. Invoke threat-model-author → docs/02-requirements/threat-model.md
4. Invoke privacy-plan-author → docs/02-requirements/privacy-plan.md
5. Invoke master-schedule-author → docs/02-requirements/schedule.md
```

**Cross-cutting setup** (in parallel with Phase 2):

```text
6. Invoke performance-budget-author → docs/performance-budget.md
   + .github/workflows/bundle-check.yml
7. Invoke analytics-instrumentation-author → docs/analytics-spec.md
   + src/lib/analytics/events.ts
8. Invoke aeo-schema-author    → docs/aeo-schema-spec.md
   + src/lib/schema/<type>.ts
9. Invoke error-monitoring-setup-author → docs/observability-spec.md
   + src/lib/telemetry.ts
10. Invoke release-discipline-author → docs/release-plan.md
    + deploy/feature-flags.yml
```

**Gate before Phase 3**: SRS approved; ADRs written; perf-budget
+ analytics + AEO + observability + release-plan all in place.

### Phase 3 — Design (week 3-6)

```text
1. Invoke design-philosophy-author → docs/03-design/design-philosophy.md
2. Invoke mood-board-author    → docs/03-design/mood-board.md
3. Invoke art-direction-author → docs/03-design/art-direction.md
4. Invoke concept-author       → docs/03-design/concept.md
5. Invoke motion-language-author → docs/03-design/motion-language.md
   (cite house-site-design-motion conventions)
6. Invoke design-tokens-author → tokens/*.json + src/styles/tokens.css
   (cite house-site-design-figma pipeline)
7. Invoke design-system-author → docs/03-design/design-system.md
   (cite house-site-design-nextjs conventions)
8. Invoke component-states-matrix-author → docs/03-design/component-states.md
9. Invoke wireframe-author     → docs/03-design/wireframes.md (optional)
10. Invoke prototype-author    → docs/03-design/prototype.md (optional)
11. Invoke a11y-annotations-author → docs/03-design/a11y-annotations.md
    (cite house-site-design-a11y for WCAG 2.2 motion criteria)
12. Invoke engineering-handoff-spec-author → docs/03-design/handoff.md
    (cite house-site-design-figma for the handoff scope)
```

**Cross-cutting setup**:

```text
13. Invoke motion-conformance-author → docs/05-hardening/motion-conformance.md
    + axe-core CI config + manual test plan
```

**Gate before Phase 4**: design system rendered in Storybook;
all component states ready; tokens flowing Figma → CSS vars +
Tailwind v4 + TS types.

### Phase 4 — Build (week 6-12)

The library doesn't ship Phase 4 atoms — the operator + engineering
team build the actual site. The atoms ship the documentation +
specifications that **bound** Phase 4. Phase 4 ceremonies (sprint
planning, daily standup, sprint review) are out of library scope.

### Phase 5 — Hardening (week 11-13)

```text
1. Invoke runbook-author       → docs/05-hardening/runbooks/{deployment,incident,launch}.md
   (cite house-site-build-nextjs deploy verbs + house-site-operate-vercel)
2. Invoke conformance-statement-author → docs/05-hardening/conformance.md
   (reads motion-conformance + axe-core CI results + manual test results)
3. Invoke polish-discipline-author → docs/05-hardening/polish-plan.md
   (Awwwards-tier polish phase budget)
```

### Phase 6 — Launch (week 13)

```text
1. Invoke launch-comms-author  → docs/06-launch/{internal,external,status}.md
   (cite house-site-operate-vercel status-page integration)
```

### Phase 7 — Post-launch (week 13+)

```text
1. Invoke baseline-report-author → docs/07-post-launch/baseline.md
   (T+8 weeks)
2. Invoke stabilization-report-author → docs/07-post-launch/stabilization.md
   (30-day stabilization close)
3. Invoke hypercare-digest-author → docs/07-post-launch/hypercare/<date>.md
   (daily during weeks 1-4)
4. Invoke optimization-loop-author → docs/07-post-launch/experiments/<id>.md
   (per experiment)
5. Invoke optimization-backlog-author → docs/07-post-launch/optimization-backlog.md
   (weekly)
6. Invoke weekly-metric-report-author → docs/07-post-launch/weekly/<date>.md
   (weekly)
7. Invoke monthly-stakeholder-report-author → docs/07-post-launch/monthly/<date>.md
   (monthly)
8. Invoke quarterly-business-review-author → docs/07-post-launch/quarterly/<quarter>.md
   (quarterly)
9. Invoke annual-retrospective-author → docs/07-post-launch/annual/<year>.md
   (annually)
10. Invoke aeo-baseline-author → docs/07-post-launch/aeo-baseline.md
    (T+8 weeks; reads aeo-schema-spec)
11. Invoke awards-submission-author → docs/07-post-launch/awards/<deadline>.md
    (when submitting to Awwwards / Webby / FWA / etc.)
12. Invoke change-request-author → docs/07-post-launch/changes/<id>.md
    (per change request)
```

---

## Two-word summary per atom

If you forget what an atom does, this is the cheat sheet:

### `site-build` family (16 atoms)

- **vision-author** — write vision
- **persona-author** — define personas
- **kpi-author** — set KPIs
- **ost-author** — opportunity tree
- **stakeholder-map-author** — map stakeholders
- **risk-register-author** — track risks
- **srs-author** — write SRS
- **adr-author** — record decision
- **threat-model-author** — model threats
- **privacy-plan-author** — privacy plan
- **master-schedule-author** — schedule project
- **design-philosophy-author** — design philosophy
- **runbook-author** — write runbook
- **baseline-report-author** — T+8 baseline
- **weekly-metric-report-author** — weekly metric
- **change-request-author** — change request

### `site-design` family (14 atoms)

- **mood-board-author** — mood board
- **art-direction-author** — art direction
- **concept-author** — creative concept
- **motion-language-author** — motion language
- **design-tokens-author** — DTCG tokens
- **design-system-author** — design system
- **component-states-matrix-author** — 9-state matrix
- **wireframe-author** — wireframes
- **prototype-author** — prototypes
- **usability-synthesis-author** — usability synthesis
- **a11y-annotations-author** — a11y per component
- **engineering-handoff-spec-author** — engineering handoff
- **discovery-tick-author** — discovery tick (P4)
- **concept-prototyping-author** — runtime concept prototype

### `site-operate` family (14 atoms)

- **launch-comms-author** — launch comms
- **conformance-statement-author** — WCAG statement
- **stabilization-report-author** — 30-day stabilization
- **hypercare-digest-author** — daily hypercare
- **optimization-loop-author** — single experiment
- **optimization-backlog-author** — RICE-scored backlog
- **polish-discipline-author** — polish plan
- **monthly-stakeholder-report-author** — monthly report
- **quarterly-business-review-author** — quarterly QBR
- **annual-retrospective-author** — annual retro
- **win-regression-report-author** — regression report
- **diagnostic-sweep-author** — diagnostic sweep
- **aeo-baseline-author** — AEO baseline
- **awards-submission-author** — awards package

### Cross-cutting tool atoms (7)

- **performance-budget-author** — perf budgets
- **motion-conformance-author** — WCAG motion criteria
- **analytics-instrumentation-author** — event taxonomy
- **aeo-schema-author** — Schema.org JSON-LD
- **i18n-strategy-author** — i18n strategy
- **error-monitoring-setup-author** — observability spec
- **release-discipline-author** — release plan + flags

### Stack overlays (21)

Read these per stack:

- **`house-site-{build,design,operate}-{nextjs,nuxt,astro,sveltekit,webflow}`** —
  per-stack-per-family conventions (15)
- **`house-site-design-motion`** — cross-stack motion conventions
- **`house-site-design-a11y`** — cross-stack WCAG 2.2 conventions
- **`house-site-design-figma`** — Figma → DTCG → Style Dict pipeline
- **`house-site-operate-{vercel,cloudflare,netlify}`** — per-host conventions

---

## What to read next

- For your project shape: pick a walkthrough.
- For library architecture: `LIBRARY-MAP.md`.
- For SemVer + v1.0 freeze contract: `VERSIONING-POLICY.md`.
- When stuck: `TROUBLESHOOTING.md`.
- Real outputs to compare against: `examples/outputs/`.
