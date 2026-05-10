# Walkthrough — marketing site

A multi-page content-driven site with no auth, no checkout, no
real-time features. The most common project shape `context-site-
build` is built for. This is the walkthrough `GETTING-STARTED.md`'s
quickstart points at by default.

**Typical timeline**: 8-13 weeks (Phase 1-6); ongoing Phase 7.

**Default stack**: Combo A (Next.js + Vercel + Sanity + R3F + GSAP).
Adapt for B/C/D/Webflow per `house-site-build-<stack>`.

---

## Phase 1 — Discovery (1-2 weeks)

| Order | Atom | Notes |
|---|---|---|
| 1 | `vision-author` | The "why we exist" statement; 1 page. |
| 2 | `persona-author` | 2-4 personas typical for marketing. Skip if the audience is one homogeneous segment. |
| 3 | `kpi-author` | Marketing-funnel KPIs: organic-traffic, conversion, LCV, SEO-rank. |
| 4 | `stakeholder-map-author` | Who signs off + who's the daily contact. |
| 5 | `risk-register-author` | Top 5 risks with mitigation. |

**Skip if**: solo-founder marketing site with no internal stakeholders;
collapse personas + stakeholder-map.

**OST optional**: Opportunity-Solution-Tree useful when the marketing
site is hypothesis-driven (B2B SaaS, niche audience). Skip for clear
product-led marketing.

**Phase 1 deliverables sign-off** is the gate to Phase 2.

---

## Phase 2 — Requirements (1-2 weeks)

| Order | Atom | Notes |
|---|---|---|
| 1 | `srs-author` | Cite `house-site-build-nextjs` SRS conventions: Next.js App Router; RSC by default; Vercel deploy; Sanity CMS; bundle budgets per `performance-budget-author`. |
| 2 | `adr-author` × 8 | The 8 Combo-A ADRs from `house-site-build-nextjs`. |
| 3 | `threat-model-author` | Marketing site threat surface: form spam, scraper rate-limit, Sanity webhook auth. |
| 4 | `privacy-plan-author` | Marketing analytics consent (Plausible: no cookies; PostHog: opt-in cookies). |
| 5 | `master-schedule-author` | 8-13-week schedule with Phase 3 (3-4 wk) + Phase 4 (4-6 wk) + Phase 5-6 (1-2 wk) blocks. |

**Cross-cutting setup** (in parallel):
- `performance-budget-author` (load-bearing for marketing — bundle budget IS the perf strategy)
- `analytics-instrumentation-author` (event taxonomy for marketing funnel)
- `aeo-schema-author` (AEO-Schema.org is the marketing site's primary SEO surface)
- `error-monitoring-setup-author` (Sentry for marketing-site errors)
- `release-discipline-author` (preview-per-PR discipline + canary for risky landing pages)

**Skip i18n**: most marketing sites are single-locale at launch; add
later via `i18n-strategy-author` if expansion comes.

**Skip `motion-conformance-author`**: only if the site is motion-light
(no GSAP scroll-jacking, no WebGL hero). If motion-heavy, this atom
is mandatory.

---

## Phase 3 — Design (3-4 weeks)

| Order | Atom | Notes |
|---|---|---|
| 1 | `design-philosophy-author` | The handoff doc that bridges site-build → site-design. |
| 2 | `mood-board-author` | Lusion's Phase 1: collect 30-60 references; categorize by tone, color, motion, type. |
| 3 | `art-direction-author` | The single page that turns mood board into commitments: palette, type, motion vocabulary, photography brief. |
| 4 | `concept-author` | The "why" — creative territory + narrative + lore. |
| 5 | `motion-language-author` | Cite `house-site-design-motion`: GSAP/Lenis/R3F selection rules; motion tokens. |
| 6 | `design-tokens-author` | Cite `house-site-design-figma`: DTCG → Style Dictionary v4 pipeline. |
| 7 | `design-system-author` | Cite `house-site-design-nextjs`: RSC-first; 9-state matrix; Storybook + Chromatic. |
| 8 | `component-states-matrix-author` | Auto-generated from Storybook; CI gate. |
| 9 | `wireframe-author` | Skip if direct-to-hi-fi; include for sites with non-trivial information architecture. |
| 10 | `prototype-author` | Figma prototype for stakeholder review. |
| 11 | `a11y-annotations-author` | Cite `house-site-design-a11y` for WCAG 2.2 motion criteria. |
| 12 | `engineering-handoff-spec-author` | Cite `house-site-design-figma` for the handoff scope. |

**Specialist atoms** (skip if not applicable):
- `usability-synthesis-author` — only if user testing is run during Phase 3.
- `concept-prototyping-author` — only if the marketing site has a hero-WebGL scene that needs runtime prototyping (Lusion's Phase 2 in code).

**Phase 3 deliverables sign-off** is the gate to Phase 4.

---

## Phase 4 — Build (4-6 weeks)

The library doesn't ship Phase 4 atoms — engineering builds the actual
site. The atoms shipped through Phase 3 + the cross-cutting atoms are
the **specifications** that bound Phase 4.

**Continuous discovery** (`discovery-tick-author`) for marketing sites
is typically light — biweekly digest of analytics + feedback channels.

**Sprint cadence** per `house-site-build-nextjs`'s "deploy-preview-
per-PR" — trunk-based development; preview URL on every PR; production
auto-promote on merge to main.

---

## Phase 5 — Hardening (1-2 weeks)

| Order | Atom | Notes |
|---|---|---|
| 1 | `runbook-author` × 3 | Deployment runbook + incident runbook + launch runbook. Cite `house-site-build-nextjs` deploy verbs + `house-site-operate-vercel`. |
| 2 | `motion-conformance-author` | Final motion-a11y pass; axe-core CI green; manual keyboard test passed. (Authored in Phase 2 cross-cutting; finalized here.) |
| 3 | `conformance-statement-author` | The WCAG-EM statement; cites motion-conformance + a11y-annotations + manual test results. |
| 4 | `polish-discipline-author` | The Awwwards-tier "polish phase" — budgeted; checklist; not bug-fix scraps. Optional for non-Awwwards-targeting sites. |

---

## Phase 6 — Launch (1 week)

| Order | Atom | Notes |
|---|---|---|
| 1 | `launch-comms-author` | Internal go/no-go email + external announcement + status-page initial post. Cite `house-site-operate-vercel` for status-page integration. |

**Go/no-go ceremony**: per `release-discipline-author`'s checklist —
CI green, smoke test passed, on-call ack, comms team notified, status
page in clean state.

---

## Phase 7 — Post-launch (ongoing)

| Cadence | Atom |
|---|---|
| T+24h, T+72h, T+1wk, T+4wk hypercare | `hypercare-digest-author` |
| Daily during weeks 1-4 | `hypercare-digest-author` |
| Weekly | `weekly-metric-report-author` |
| T+8wk baseline | `baseline-report-author` + `aeo-baseline-author` |
| Per experiment | `optimization-loop-author` |
| Weekly during optimization | `optimization-backlog-author` |
| Monthly | `monthly-stakeholder-report-author` |
| Quarterly | `quarterly-business-review-author` |
| Annually | `annual-retrospective-author` |
| 30-day stabilization close | `stabilization-report-author` |
| Per change request | `change-request-author` |
| Per regression | `win-regression-report-author` |
| Per Awwwards / Webby / FWA submission | `awards-submission-author` |

**Atoms typically not invoked for marketing sites**:
- `quarterly-business-review-author` — only when the project is part
  of a longer engagement with formal QBR cadence.
- `annual-retrospective-author` — only for projects that live ≥ 1
  year.
- `awards-submission-author` — only when targeting Awwwards / Webby /
  FWA.

---

## Atom-skip table for solo-dev marketing sites

The minimum viable Phase 1-7 roster:

| Phase | Required atoms |
|---|---|
| 1 | vision-author, kpi-author |
| 2 | srs-author, adr-author × 3-4 (the load-bearing decisions only), performance-budget-author, analytics-instrumentation-author |
| 3 | design-tokens-author, design-system-author, motion-language-author (if motion-heavy), a11y-annotations-author |
| 4 | (engineering builds; atoms produce no output) |
| 5 | runbook-author × 1 (deployment), conformance-statement-author |
| 6 | launch-comms-author |
| 7 | baseline-report-author (T+8wk), weekly-metric-report-author |

Skip everything else; add as needed.

---

## See also

- `GETTING-STARTED.md` — top-level pick-a-stack guide.
- `LIBRARY-MAP.md` — dependency graph.
- `walkthroughs/e-commerce.md` — for catalog + cart + checkout.
- `walkthroughs/web-app.md` — for CRUD-heavy app shells.
- `walkthroughs/microsite.md` — for time-bounded campaigns.
- `examples/outputs/` — anonymized real outputs to compare against.
