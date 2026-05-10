---
name: error-monitoring-setup-author
description: >
  Produces the error-monitoring + observability spec for a site
  project. Writes docs/observability-spec.md and
  src/lib/telemetry.ts. Names the tool selection (Sentry, Datadog,
  Honeycomb, Bugsnag), instrumentation conventions
  (service, env, release, tenant tags), SLI definitions (latency
  p95, error rate, availability), release-marker wiring, and
  per-tool PII discipline. Free-standing atom — applies across
  the methodology and across all five stack combos. Do NOT use
  for: analytics event taxonomy (use analytics-instrumentation-author);
  performance budgets in CI (use performance-budget-author);
  release-flag and rollback automation (use release-discipline-author);
  per-host operate-overlay observability commands (those cite
  this spec; they live in house-site-operate-vercel,
  house-site-operate-cloudflare, or house-site-operate-netlify).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [cross-cutting, observability]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.6.0 Phase 5 cross-
            cutting-tools batch. Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 5; user
            explicitly approved maximalist scope on 2026-05-08.
---

# error-monitoring-setup-author

> **pre-trigger build (v0.6.0)**; reassess when first consumer
> needs codified observability + SLI definitions per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 5.

Free-standing atom that produces the error-monitoring + observability
specification + the SDK initialization template. Outputs:
`docs/observability-spec.md` and `src/lib/telemetry.ts`. The atom
names the tool selection (Sentry, Datadog, Honeycomb, Bugsnag),
instrumentation conventions including the release-marker wiring,
SLI definitions including latency p95, and the per-tool PII handling.
Applies across the methodology and across all five stack combos —
the `house-site-operate-vercel`, `house-site-operate-cloudflare`,
and `house-site-operate-netlify` overlays cite this spec for their
host-specific observability commands.

## When to Use

- Phase 2 Requirements: when the SRS NFRs cite SLIs (latency p95,
  error rate, availability) and the spec needs codification.
- Phase 5 Hardening: when the team is wiring Sentry / Datadog /
  Honeycomb and the per-tag conventions need documentation.
- Pre-launch: when on-call rotation is being set up and the alert-
  threshold rationale needs a written source-of-truth.
- Post-incident: when an incident retrospective surfaces a missing
  alert or a noisy alert; the spec is updated to close the gap.

## When NOT to Use

- For analytics event taxonomy — use
  `analytics-instrumentation-author`. Error monitoring is operational;
  analytics is product-measurement.
- For performance budgets enforced in CI — use
  `performance-budget-author`.
- For release flags + rollback automation — use
  `release-discipline-author`.
- For per-host operate-overlay observability commands — those go in
  `house-site-operate-{vercel,cloudflare,netlify}` (which cite this
  spec).
- For SLO-policy + error-budget management at scale — out of library
  scope as a standalone atom; the patterns live here as
  conventions, but a dedicated SLO-policy tool is deferred until
  multi-team scale demands it.

## Capabilities Owned

1. **Tool selection rationale** — Sentry (default for marketing +
   app-shell sites), Datadog (default for high-volume SaaS),
   Honeycomb (default for distributed-tracing-heavy backends),
   Bugsnag (when client mandates) — per-tool tradeoffs + per-
   stack SDK availability.
2. **Instrumentation conventions** — every event tagged with
   `service`, `env` (development / preview / production), `release`
   (Git SHA), `tenant` (when multi-tenant), `user_role` (when
   meaningful).
3. **SLI definitions** — latency p95 (per-route or per-page-type),
   error rate (% of requests producing 5xx), availability (% of
   requests with valid response within SLA). Per-SLI alert
   thresholds.
4. **Release marker wiring** — Sentry `sentry-cli releases new`
   step in CI on production deploy; source maps uploaded; previous
   release marked.
5. **PII discipline** — what's allowed in error context (user ID,
   tenant ID, request URL with stripped query params), what's
   forbidden (PII, payment info, full request body), what's hashed
   (email — SHA-256 for support correlation).
6. **Custom-metric template** — `THREE.WebGLRenderer.info`
   (calls / triangles / programs) when WebGL is in use; CMS query
   latency; build-pipeline duration.
7. **Per-stack SDK** — Sentry `@sentry/{nextjs,nuxt,sveltekit,
   browser}`; per-host integration (Vercel + Sentry, Cloudflare
   Workers + Sentry, Netlify + Sentry).

## Handoffs to Other Skills

- **From `srs-author`** — SRS's "Observability NFRs" section cites
  this document.
- **From `runbook-author`** — incident-response runbooks cite this
  document for the alert-threshold rationale.
- **From `adr-author`** — error-monitoring-tool-selection ADR cites
  this document's tool selection rationale.
- **To `release-discipline-author`** — release-flag + rollback
  automation reads this document's SLI definitions for the
  threshold-based auto-rollback configuration.
- **To `optimization-loop-author`** — Phase-7 optimization
  experiments cite this document's custom metrics.
- **To `house-site-operate-{nextjs,nuxt,astro,sveltekit,webflow}`**
  — per-stack operate overlays cite this spec for the framework-
  specific SDK installation.
- **To `house-site-operate-{vercel,cloudflare,netlify}`** — host
  overlays cite this spec for the per-host integration.

## Edge Cases

- **Static-only site, no backend**: the spec applies only to
  frontend errors + CWV field RUM; the SLI set shrinks to error
  rate + availability.
- **Multi-tool observability** (Sentry for frontend + Datadog for
  backend): the per-tool tag namespace deconflicts (`sentry.*` vs
  `datadog.*`); the SLI definitions span both.
- **PII-sensitive industries** (healthcare, financial, legal): the
  PII discipline is rigorous; before-send hooks scrub aggressively;
  consider self-hosted Sentry / Bugsnag.
- **High-volume SaaS** (>10M events/month): Sentry sampling
  becomes load-bearing; the spec defines the per-environment
  sample rate.
- **Resource-constrained tier** (Hobby / Free plan): the spec is
  abbreviated; defer SLI tracking to post-launch when pricing
  affords it.

## References

No external `references/*.md` files yet — first real authoring run
will produce templates worth promoting (per-tool selection
comparison, the SLI definition templates, the PII discipline +
before-send hook templates). Per the v0.7.0 speculative-skill
convention, the absence is flagged here rather than papered over.
