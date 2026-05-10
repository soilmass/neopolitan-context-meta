# Walkthrough — web app (CRUD-heavy)

A site that's primarily an authenticated app — dashboards, settings,
user-generated content, internal tools. Different concerns from
marketing/e-commerce: auth is the front door; perf budget is per-
route not per-page-type; motion is restraint; SEO is irrelevant for
behind-auth surfaces.

**Typical timeline**: 12-20 weeks. Phase 4 (Build) is the dominant
phase.

**Default stack**: Combo A (Next.js + Vercel) for SSR/RSC discipline;
Combo D (SvelteKit + adapter) for performance-pure apps; Combo B
(Nuxt 3) for Vue-shop apps. Combo C (Astro) is **not** typical for
web-apps — Astro's static-first model fits poorly.

---

## What's different from marketing/e-commerce

| Concern | Marketing | E-commerce | Web app |
|---|---|---|---|
| Auth | None or marketing-newsletter | Customer accounts (optional) | **Load-bearing** (every route) |
| SEO surface | Public pages | Public PDP/PLP + private cart | Public landing + auth gate (the rest is noindex) |
| Performance | Per-page-type budgets | Per-page-type budgets | Per-route budgets (TTI on dashboards is different from TTI on settings) |
| Motion | Marketing-cinematic OK | Cinematic OK in product photography; restrained in checkout | **Restrained** — motion is feedback, not décor |
| Analytics | Marketing funnel | Commerce funnel | Product analytics (PostHog / Mixpanel / Amplitude); user-flow + retention focus |
| Backend complexity | Low (CMS reads) | Medium (cart + payments + inventory) | **High** (often the whole product) |
| Real-time | None | Stock + price | Often (collaboration, notifications, live data) |

---

## Phase 1 — Discovery (2-3 weeks)

| Atom | Web-app-specific notes |
|---|---|
| `vision-author` | Product vision (≠ marketing vision); covers what the app *does* not just how it presents. |
| `persona-author` | Job-to-be-done framing; per-role personas (admin / member / guest); often more personas than marketing (5-8). |
| `kpi-author` | Activation rate, retention (D1/D7/D30), feature adoption, NPS, churn. Different metric set from marketing/e-commerce. |
| `ost-author` | **Load-bearing** for product apps; the OST IS the product roadmap structure. |
| `stakeholder-map-author` | Product team + engineering + customer success + sales (when B2B). |
| `risk-register-author` | Top risks: customer churn, feature scope creep, security incident. |

---

## Phase 2 — Requirements (3-4 weeks; heaviest of all shapes)

Web apps have the heaviest Phase 2 because the surface area is
largest and the trade-offs are deepest.

| Atom | Web-app-specific notes |
|---|---|
| `srs-author` | Per-route NFRs (TTI on `/dashboard` vs `/settings`); auth flow NFRs (login latency p95); real-time NFRs when applicable; data-consistency model NFRs. |
| `adr-author` × 15-25 | Auth strategy (session cookie vs JWT vs OAuth); database (Postgres vs MongoDB vs Firestore); ORM (Prisma vs Drizzle vs SQL-direct); state-management (Redux vs Zustand vs context); real-time tech (websocket vs SSE vs polling); caching (Redis vs Edge Cache vs in-memory); background jobs (BullMQ vs Inngest vs Temporal); search (Algolia vs Typesense vs Postgres FTS); file storage (S3 vs Vercel Blob vs Cloudflare R2); email (Resend vs Postmark vs SendGrid); payments (Stripe Billing vs Lemon Squeezy vs Paddle when SaaS); admin tooling (Retool vs Forest Admin vs custom); error budget; SLO commitments. |
| `threat-model-author` | App threat surfaces are the deepest — IDOR, broken access control, multi-tenant isolation, session-fixation, CSRF, SSRF, API abuse, secrets leakage, supply-chain (npm). |
| `privacy-plan-author` | Full GDPR/CCPA + per-feature data-retention + DSAR (data-subject-access-request) flow + right-to-be-forgotten flow. |
| `master-schedule-author` | Multi-quarter; per-feature milestones; integration test windows. |

**Cross-cutting setup**:

- `analytics-instrumentation-author` — product analytics taxonomy
  (`view_<page>`, `start_<flow>`, `complete_<flow>`, `error_<topic>`,
  `feature_<name>_used`); load-bearing.
- `aeo-schema-author` — for the **public** marketing surfaces only;
  app surfaces are noindex.
- `i18n-strategy-author` — load-bearing for B2B-international or
  consumer-international apps.
- `performance-budget-author` — per-route budgets; the dashboard
  budget often the strictest.
- `error-monitoring-setup-author` — load-bearing; SLI definitions
  at `srs-author` granularity (per route, per feature).
- `release-discipline-author` — load-bearing; feature-flag tooling
  + canary + rollback automation are minimum table stakes.

---

## Phase 3 — Design (4-5 weeks)

| Atom | Web-app-specific notes |
|---|---|
| `mood-board-author` | Less Lusion-style cinematic; more Linear / Vercel-Dashboard restraint. |
| `art-direction-author` | Color palette typically more restrained (max 1-2 brand colors + neutral grays); type system mature (often Inter / IBM Plex / SF Pro). |
| `concept-author` | Often skipped for B2B SaaS (the concept is "be useful"); included for consumer apps. |
| `motion-language-author` | **Restrained motion** — Framer Motion / Motion (motion.dev) for layout transitions; minimal scroll-jacking; no GSAP cinematic timelines. |
| `design-tokens-author` | DTCG → Style Dictionary; same pipeline. |
| `design-system-author` | App-shaped design system: layout primitives (Stack, Grid, Cluster), data-display primitives (Table, List, Card), input primitives (Input, Select, Combobox, DatePicker), feedback primitives (Toast, Modal, Alert, ConfirmDialog). |
| `component-states-matrix-author` | The 9-state matrix is **rigorous** for web apps — empty / loading / skeleton states are NOT optional (they're load-bearing for app UX). |
| `wireframe-author` | Load-bearing — per-route wireframes before Hi-Fi. |
| `prototype-author` | Multiple prototypes per surface (dashboard + onboarding + key flows). |
| `usability-synthesis-author` | Mandatory for new flows; usability testing pre-launch is cheaper than post-launch refactor. |
| `a11y-annotations-author` | Forms a11y is the sharpest discipline for apps (label association, error announcement, required-field indication). |
| `engineering-handoff-spec-author` | Cite `house-site-design-figma` for the handoff scope; per-feature handoffs typically. |

**Specialist atoms**:

- `discovery-tick-author` — load-bearing; weekly product feedback
  digest (analytics + support tickets + sales feedback).
- `concept-prototyping-author` — typically not needed (web apps are
  not motion-cinematic).

---

## Phase 4 — Build (6-12 weeks; the heart of web-app work)

Engineering-led; the library doesn't ship Phase 4 atoms.

**Continuous discovery** (`discovery-tick-author`) is **mandatory** for
web apps — weekly digest at minimum; bi-weekly for slower-tempo teams.

**Sprint cadence** typically 1-2 week sprints; trunk-based with feature
flags for risky changes (per `release-discipline-author`).

---

## Phase 5 — Hardening (2-3 weeks; rigorous)

| Atom | Web-app-specific notes |
|---|---|
| `runbook-author` × 5+ | Deployment + incident + launch + auth-incident + database-failover + per-feature rollback (one per high-risk feature). |
| `motion-conformance-author` | Restrained-motion sites typically pass WCAG 2.2 motion criteria easily; document is brief. |
| `conformance-statement-author` | Forms a11y + keyboard pass + screen-reader pass mandatory; document is thorough. |
| `polish-discipline-author` | Skip — web apps don't typically have a budgeted Awwwards-tier polish phase. The optimization-loop pattern in Phase 7 is the analogous discipline. |

---

## Phase 6 — Launch (1-2 weeks)

| Atom | Notes |
|---|---|
| `launch-comms-author` | Customer-facing announcement (when the app is new); customer-base communication (when this is a major-feature launch); status-page initial post. |

**Soft-launch + canary** (per `release-discipline-author`):
- Internal users for 1 week (employee accounts).
- 5% of customer base for 1 week.
- 25% for 1 week.
- 100%.

This is more cautious than marketing/e-commerce because the cost of
a regression is higher (customer trust, retention).

---

## Phase 7 — Post-launch (ongoing; load-bearing)

Web-app Phase 7 is the most heavyweight of all project shapes:

| Cadence | Atom | Notes |
|---|---|---|
| Daily during weeks 1-4 | `hypercare-digest-author` | Customer-support backlog + error-rate trend + retention cohort |
| Weekly | `weekly-metric-report-author` | Activation, retention, churn, NPS, error rate |
| Per experiment | `optimization-loop-author` | Continuous experimentation post-launch |
| Weekly | `optimization-backlog-author` | RICE-scored backlog of next experiments |
| Monthly | `monthly-stakeholder-report-author` | Customer success + sales review |
| Quarterly | `quarterly-business-review-author` | Customer QBRs (B2B) + roadmap planning |
| Annually | `annual-retrospective-author` | Year-in-review + next-year roadmap |
| 30-day stabilization close | `stabilization-report-author` | Wraps the launch hypercare |
| Per regression | `win-regression-report-author` | Common when shipping fast |
| Per change request | `change-request-author` | Per significant scope change |
| Per quarter | `diagnostic-sweep-author` | Health check across features |

**Atoms typically NOT invoked for web apps**:
- `aeo-baseline-author` — only for the public marketing pages, not the
  app surfaces.
- `awards-submission-author` — web apps rarely submit to Awwwards
  (interaction-design awards exist — Webby, FWA — but Awwwards is
  marketing-site-focused).

---

## Atom-skip table for solo-dev SaaS web app

| Phase | Required atoms |
|---|---|
| 1 | vision-author, persona-author × 1-2 (the job-to-be-done), kpi-author, ost-author |
| 2 | srs-author, adr-author × 6-8 (auth + DB + state + real-time + caching + email), threat-model-author, privacy-plan-author, performance-budget-author, analytics-instrumentation-author, error-monitoring-setup-author, release-discipline-author |
| 3 | design-tokens-author, design-system-author, component-states-matrix-author (rigorous), wireframe-author, a11y-annotations-author |
| 4 | (engineering builds; discovery-tick weekly) |
| 5 | runbook-author × 3 (deployment, incident, auth-incident), conformance-statement-author |
| 6 | launch-comms-author |
| 7 | baseline-report-author, hypercare-digest-author (load-bearing), weekly-metric-report-author, optimization-loop-author, optimization-backlog-author |

Skip mood-board / art-direction / concept / motion-language / polish
/ awards-submission for solo-dev SaaS — they're not where the value is.

---

## See also

- `walkthroughs/marketing-site.md` — for the marketing surface that
  fronts the web app (often a separate project / build).
- `walkthroughs/microsite.md` — for one-off campaign sites unrelated
  to the app.
- `walkthroughs/e-commerce.md` — when the app IS commerce.
- `LIBRARY-MAP.md` — dependency graph.
- `examples/outputs/` — anonymized outputs.
