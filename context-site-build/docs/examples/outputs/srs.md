# SRS — `<project>` (anonymized example output)

> **Note**: anonymized illustrative output of `srs-author`. Edited
> from a real project. Combo A (Next.js + Vercel + Sanity) stack
> per `house-site-build-nextjs`.

---

## Functional requirements

### F1 — User authentication

The site MUST support email + password authentication via
`<auth-provider>` (per ADR 0003).

| ID | Requirement | Priority |
|---|---|---|
| F1.1 | User signs up with email + password | MUST |
| F1.2 | User signs in with email + password | MUST |
| F1.3 | User resets password via email link (24h expiry) | MUST |
| F1.4 | User signs out and session invalidated | MUST |
| F1.5 | Failed signin lockout after 5 attempts in 15 min | MUST |

### F2 — Portfolio editing

| ID | Requirement | Priority |
|---|---|---|
| F2.1 | User uploads up to 50 images per portfolio | MUST |
| F2.2 | User reorders images via drag (touch + mouse) | MUST |
| F2.3 | User crops + filters via UI (no Photoshop required) | SHOULD |
| F2.4 | User publishes site to a `<project>.<domain>/<slug>` URL | MUST |
| F2.5 | User maps a custom domain (CNAME) | MUST |

### F3 — Site rendering

| ID | Requirement | Priority |
|---|---|---|
| F3.1 | Visitor sees the published portfolio at the public URL | MUST |
| F3.2 | Visitor scrolls through images on mobile + desktop | MUST |
| F3.3 | Visitor's analytics events propagate to PostHog | MUST |
| F3.4 | Visitor with `prefers-reduced-motion` gets no parallax | MUST |

[F4–F12 elided for length]

---

## Non-functional requirements

### NFR1 — Performance (cite `performance-budget.md`)

| ID | Requirement | Threshold |
|---|---|---|
| NFR1.1 | LCP at p75 mobile (4G) | ≤ 2.0s |
| NFR1.2 | INP at p75 mobile | ≤ 200ms |
| NFR1.3 | CLS at p75 | ≤ 0.05 |
| NFR1.4 | Critical-path JS gz on landing page | ≤ 130 KB |
| NFR1.5 | Critical-path JS gz on portfolio-page | ≤ 200 KB |
| NFR1.6 | Total JS gz on landing page | ≤ 300 KB |
| NFR1.7 | Total JS gz on portfolio-page (with WebGL hero) | ≤ 600 KB |
| NFR1.8 | Three-js draw calls / frame | ≤ 100 |

CI gates per `performance-budget.md`:
- bundlesize on every PR.
- size-limit on every PR.
- Lighthouse CI on every preview deploy.

### NFR2 — Availability + reliability

| ID | Requirement | Threshold |
|---|---|---|
| NFR2.1 | Uptime (calendar month) | ≥ 99.9% |
| NFR2.2 | Error rate (5xx + uncaught JS error) | ≤ 0.5% sustained |
| NFR2.3 | Rollback target from incident detection | ≤ 30s |

Per `observability-spec.md` SLI definitions; per `release-plan.md`
rollback automation.

### NFR3 — Accessibility (cite `motion-conformance.md`)

| ID | Requirement | Threshold |
|---|---|---|
| NFR3.1 | WCAG 2.2 AA compliance (per criterion table) | All AA |
| NFR3.2 | WCAG 2.2 motion criteria (2.1.1 / 2.2.2 / 2.3.3 / 2.4.7 / 2.5.7 / 2.5.8) | Per `motion-conformance.md` |
| NFR3.3 | axe-core CI fails on serious / critical | MUST |
| NFR3.4 | Manual keyboard pass before each release | MUST |
| NFR3.5 | Lite-mode alternative experience available | MUST |

### NFR4 — Security

| ID | Requirement | Threshold |
|---|---|---|
| NFR4.1 | TLS 1.3+ on all surfaces | MUST |
| NFR4.2 | HSTS preload list | SHOULD |
| NFR4.3 | CSP nonce-based; no `unsafe-inline` | MUST |
| NFR4.4 | Sanity webhook auth via shared-secret HMAC | MUST |

Per `threat-model.md` mitigations.

### NFR5 — Privacy

Per `privacy-plan.md`. GDPR/CCPA flows; cookie consent before any
analytics fires; PII discipline per `observability-spec.md`.

### NFR6 — Internationalization

Out of scope at launch (English only). Add per `i18n-spec.md` if
expansion to non-English markets.

### NFR7 — Browser + device support

| Surface | Browsers | Versions |
|---|---|---|
| Marketing site | Chrome, Edge, Safari, Firefox | Last 2 major |
| Editor (auth-required) | Chrome, Edge, Safari | Last 2 major (Firefox deferred) |

Mobile: iOS Safari 16+, Chrome Android 110+.

### NFR8 — Observability (cite `observability-spec.md`)

| ID | Requirement |
|---|---|
| NFR8.1 | Sentry release marker on every production deploy |
| NFR8.2 | Custom Sentry metric for `THREE.WebGLRenderer.info` |
| NFR8.3 | PostHog event taxonomy per `analytics-spec.md` |
| NFR8.4 | Vercel Web Analytics + Speed Insights enabled |

---

## Out of scope

- Native mobile apps (iOS / Android).
- Desktop apps.
- Internationalization at launch (deferred).
- Premium tiers (deferred to v2).
- Customer support live chat (deferred; email-only at launch).

---

## Assumptions

- Operator can deliver the agreed Phase 3 design system on schedule.
- Sanity remains the chosen CMS through v1.0.
- Vercel hosting cost model holds at projected user volumes.

## Authority

- Vision: `vision.md` v0.2 (signed off 2026-04-23).
- Personas: `personas.md` v0.1 (3 personas).
- KPIs: `kpis.md` v0.2 (6-month + 12-month targets).
- Design philosophy: `design-philosophy.md` v0.1.

## Cross-cutting documents this SRS depends on

- `performance-budget.md` — bundle + CWV thresholds (NFR1).
- `motion-conformance.md` — WCAG 2.2 motion criteria (NFR3).
- `analytics-spec.md` — event taxonomy (NFR8.3).
- `aeo-schema-spec.md` — Schema.org spec.
- `observability-spec.md` — SLI definitions (NFR2 + NFR8).
- `threat-model.md` — security threat mitigations (NFR4).
- `privacy-plan.md` — GDPR/CCPA + PII handling (NFR5).
- `release-plan.md` — release-discipline (NFR2.3).

## ADR roster (the 8 Combo-A ADRs + project-specific)

- ADR-0001 — RSC vs client-component boundary.
- ADR-0002 — Edge vs Serverless function selection.
- ADR-0003 — Auth provider selection (NextAuth.js v5 + email).
- ADR-0004 — ISR cadence per page type.
- ADR-0005 — Sanity dataset strategy (production + staging).
- ADR-0006 — Image optimization origin (next/image + Vercel).
- ADR-0007 — Email stack (Resend transactional + Loops marketing).
- ADR-0008 — Analytics privacy posture (PostHog cloud, EU region).
- ADR-0009 — Auth boundary (server-side session, httpOnly cookie).

---

*Authored 2026-05-02 by srs-author v0.1.1. Reviewed 2026-05-08 by
engineering. Sign-off: 2026-05-09.*
