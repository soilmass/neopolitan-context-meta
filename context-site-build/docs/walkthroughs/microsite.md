# Walkthrough — microsite / campaign

A single-page (or 2-3 page) time-bounded site supporting a campaign,
launch, event, or one-off marketing moment. Often the sites that
land Awwwards SOTD/SOTY because they have the budget + concept
freedom of a marketing site without the multi-page complexity.

**Typical timeline**: 4-8 weeks (the shortest of all shapes).

**Default stack**: Combo D (SvelteKit + vanilla Three.js) for
performance-pure cinematic; Combo A (Next.js + R3F) for React-shop
teams; Combo C (Astro + WebGL island) for static-first preference.
**Combo B (Nuxt) and Webflow are less common** for microsites — Nuxt
is over-tooled for one page; Webflow has motion ceilings the
campaign aesthetic typically wants to break.

---

## What's different from the other shapes

| Concern | Microsite | Marketing | E-commerce | Web app |
|---|---|---|---|---|
| Page count | 1-3 | 10-50 | 10-200 | 20-500 |
| Lifespan | 4 weeks – 6 months | 2-5 years | 5-10 years | 5+ years |
| Auth | None | None | Optional | **Required** |
| Motion | **Cinematic / load-bearing** | Often cinematic | Restrained on PDP/cart | Restrained |
| WebGL | Often | Sometimes | Rarely | Almost never |
| SEO | Time-bounded; less critical | Long-term | Long-term | Public surface only |
| Awwwards SOTD potential | **Highest** | Moderate | Low | Very low |
| Performance budget | Hardest target (mobile + cinematic) | Standard | Standard | Per-route |
| A11y motion criteria | **Strictest** (cinematic = highest WCAG risk) | Standard | Standard | Easy |

---

## Phase 1 — Discovery (3-5 days; compressed)

| Atom | Microsite-specific notes |
|---|---|
| `vision-author` | Often provided as a brief from agency-creative-director — the brief IS the vision; this atom captures it as a 1-pager. |
| `persona-author` | Often skipped — the audience is "people who'll see the campaign"; the brief specifies persona implicitly. |
| `kpi-author` | Time-bounded KPIs: impressions, CTR, conversion-to-action, share rate, time-on-site, Awwwards-submission-success (when targeting). |
| `concept-author` | **Load-bearing for microsites** — the concept is what makes or breaks the campaign. Authored early in Phase 1, not Phase 3. |

Skip OST, stakeholder-map, risk-register for solo-dev microsites;
include for agency engagements.

---

## Phase 2 — Requirements (3-5 days; compressed)

| Atom | Microsite-specific notes |
|---|---|
| `srs-author` | The SRS is brief — bundle budget per `house-site-{stack}` WebGL-hero row; motion-conformance per `house-site-design-a11y` (mandatory); analytics minimal (page-view + share-CTA-click + main-CTA-conversion). |
| `adr-author` × 4-6 | The 4-6 load-bearing decisions: stack (Combo D vs A), 3D library (vanilla Three.js vs R3F), motion library (GSAP only vs GSAP + Lenis), CMS (none — content lives in repo for time-bounded sites), hosting, domain strategy. |
| `threat-model-author` | Light — campaign sites have minimal threat surface (no PII, no payments). Document the rate-limit + scraper protection. |

Skip `privacy-plan-author` if no PII is collected (often the case);
include if email-capture or signup is part of the campaign.

`master-schedule-author` — 4-8 week schedule with Phase 3 (1 wk) +
Phase 4 (3-5 wk) + Phase 5-6 (1 wk) blocks. Compressed but rigorous.

**Cross-cutting setup** (compressed):

- `performance-budget-author` — **load-bearing**; the WebGL-hero
  budget row IS the engineering constraint. Without this document,
  the site won't pass Lighthouse CI mobile.
- `motion-conformance-author` — **load-bearing**; cinematic
  motion = highest WCAG risk; without the alt-experience pattern,
  the site will fail audit.
- `analytics-instrumentation-author` — minimal taxonomy.
- `aeo-schema-author` — Organization + WebSite only; brief.
- `error-monitoring-setup-author` — Sentry browser SDK only.
- `release-discipline-author` — typically just preview-per-PR; no
  feature flags needed for one-page sites.

Skip `i18n-strategy-author` unless the campaign is multi-locale.

---

## Phase 3 — Design (1-2 weeks; compressed; load-bearing)

| Atom | Microsite-specific notes |
|---|---|
| `mood-board-author` | **Load-bearing**; this is where the Awwwards-tier work happens. Include 60-100 references (more than for marketing); categorize by tone, motion, color, type, 3D style. |
| `art-direction-author` | **Load-bearing**; bold + opinionated; the art-direction IS the campaign signature. |
| `concept-author` | Already authored in Phase 1 (per microsite convention). |
| `motion-language-author` | **Load-bearing**; motion is what makes/breaks the campaign. Cite `house-site-design-motion`. |
| `design-tokens-author` | Brief — campaigns often use 1-2 fonts + 3-5 colors. |
| `design-system-author` | Compressed — components are bespoke per section, not a reusable system. |
| `component-states-matrix-author` | Skip — components are typically not reused; states matrix doesn't apply. |
| `wireframe-author` | Optional; storyboard is more typical for cinematic microsites. |
| `prototype-author` | **Load-bearing**; usually a Figma + Theatre.js / GSAP prototype to validate the cinematic flow. |
| `concept-prototyping-author` | **Load-bearing for cinematic microsites** — runtime concept prototype in code (Lusion's Phase 2 in code). |
| `a11y-annotations-author` | Cite `house-site-design-a11y`; cinematic = strictest WCAG criteria. |
| `engineering-handoff-spec-author` | Brief — the prototype IS the handoff for cinematic microsites. |

Skip `usability-synthesis-author`, `discovery-tick-author` —
campaigns don't have ongoing discovery cycles.

---

## Phase 4 — Build (3-5 weeks)

Engineering-led. The art-direction + motion-language documents are
the bound that constrains Phase 4.

**Sprint cadence** is daily for short campaigns — there isn't time
for weekly retrospectives. Trunk-based; preview-per-PR.

---

## Phase 5 — Hardening (2-3 days; rigorous despite compression)

| Atom | Microsite-specific notes |
|---|---|
| `runbook-author` × 1-2 | Deployment runbook; incident runbook (the launch + 48h hypercare). Cite host overlay (typically `house-site-operate-vercel` or `-cloudflare`). |
| `motion-conformance-author` | Final pass; axe-core CI + manual keyboard pass + screen-reader pass + lite-mode validation. |
| `conformance-statement-author` | The honest WCAG-EM statement; cinematic-microsite reality is "AA on most criteria; AAA-aspirational on some; lite-mode for users who need it". |
| `polish-discipline-author` | **Load-bearing**; the budgeted polish phase IS where Awwwards-tier work crystallizes. |

---

## Phase 6 — Launch (1 day)

| Atom | Notes |
|---|---|
| `launch-comms-author` | Internal go/no-go (when agency-led) + external announcement (social + press release) + status-page (lighter than marketing — campaigns often skip status pages entirely; document the gap). |

**Pre-launch ritual** (per `release-discipline-author` minimum):
- Lighthouse CI green on production preview.
- axe-core green on production preview.
- Manual keyboard + screen-reader test passed.
- Mobile + desktop smoke test from the agency office's network.
- Agency creative-director sign-off.

---

## Phase 7 — Post-launch (1-12 weeks; bounded)

Microsite Phase 7 is shorter than other shapes — campaigns have a
defined lifespan:

| Cadence | Atom | Notes |
|---|---|---|
| 48h hypercare | `hypercare-digest-author` | Daily for first 48-72h |
| Weekly during campaign | `weekly-metric-report-author` | Reach, conversion, share rate |
| T+8wk baseline | `baseline-report-author` | Cumulative campaign performance |
| **Awwwards-submission deadline** | `awards-submission-author` | The atom whose existence is most justified by microsites |
| Per regression | `win-regression-report-author` | When a key metric drops mid-campaign |
| At campaign close | `stabilization-report-author` | Final report; cumulative outcomes |
| Annual review (when running multiple campaigns/year) | `annual-retrospective-author` | Cross-campaign learnings |

**Atoms NOT invoked for microsites**:
- `optimization-loop-author` — campaigns are usually too short for
  meaningful experimentation cycles.
- `optimization-backlog-author` — same.
- `monthly-stakeholder-report-author` — campaigns close before
  monthly cadence kicks in.
- `quarterly-business-review-author` — out of timeline.
- `aeo-baseline-author` — campaigns don't typically pursue AI-search
  citation.
- `change-request-author` — campaigns are scope-locked at the brief.

---

## Atom-skip table for solo-dev cinematic microsite

| Phase | Required atoms |
|---|---|
| 1 | vision-author, kpi-author, concept-author |
| 2 | srs-author, adr-author × 4-6, performance-budget-author (load-bearing), motion-conformance-author (load-bearing), analytics-instrumentation-author, error-monitoring-setup-author |
| 3 | mood-board-author, art-direction-author, motion-language-author, design-tokens-author, prototype-author, concept-prototyping-author, a11y-annotations-author |
| 4 | (engineering builds) |
| 5 | runbook-author × 1, motion-conformance-author (final pass), conformance-statement-author, polish-discipline-author |
| 6 | launch-comms-author |
| 7 | hypercare-digest-author (48h), baseline-report-author (T+8wk), awards-submission-author (per submission deadline), stabilization-report-author (campaign close) |

This is the smallest atom roster that produces an Awwwards-tier-
serious microsite.

---

## See also

- `walkthroughs/marketing-site.md` — for ongoing multi-page sites.
- `LIBRARY-MAP.md` — dependency graph.
- `house-site-design-motion`, `house-site-design-a11y` — cross-stack
  overlays especially load-bearing for microsites.
- `house-site-build-{sveltekit,nextjs,astro}` — stack overlays;
  `sveltekit` is the most-common Igloo-Inc-style cinematic
  microsite stack.
- `examples/outputs/` — anonymized microsite outputs.
