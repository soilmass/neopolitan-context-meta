---
name: house-site-operate-nuxt
description: >
  House conventions for the site-operate family on the Combo B stack
  (Nuxt 3 + Nitro presets + Sentry + Plausible/Fathom). Overlays
  runbook-author, launch-comms-author, optimization-loop-author,
  optimization-backlog-author, and conformance-statement-author with
  Nitro-preset deploy verbs (host-agnostic via the chosen preset),
  routeRules-driven ISR, Sentry instrumentation conventions,
  Lighthouse CI gating, and axe-core a11y CI. Do NOT use for: SRS /
  ADR / threat-model on Nuxt (use house-site-build-nuxt); design-
  system / motion conventions on Nuxt (use house-site-design-nuxt);
  hosting-platform conventions independent of Nuxt (use
  house-site-operate-vercel / -netlify / -cloudflare); composing this
  overlay with a per-team overlay (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, stack-overlay]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 stack-
            overlay batch (Nuxt × 3). Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-operate-nuxt

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay encoding launch + post-launch operational conventions
on the Combo B stack.

This overlay applies on top of the family's mechanism atoms
with stack-specific or hosting-platform conventions. Composing
with a per-team overlay, or replacing it with a different family
overlay independent of this one, is deferred per ARCHITECTURE.md.
The site-operate family's threat-model and design coverage live
in their own overlays.

## Purpose

Encode how runbook, launch comms, optimization loops, and a11y
conformance ride on Nuxt 3 + Nitro + Sentry + analytics:

1. Runbook deploy verbs use `nuxi build` + the chosen Nitro preset's
   host CLI. Host-specific operational details defer to
   `house-site-operate-{vercel,netlify,cloudflare}`.
2. ISR is via Nitro `routeRules` (`isr: 60` etc.) plus on-demand
   purge through the host's revalidation API.
3. Sentry instrumentation uses `@sentry/nuxt`; release markers
   wired via Nitro hooks.
4. Optimization loops use the host's RUM (Vercel Web Analytics,
   Netlify Analytics, Cloudflare Web Analytics) for field; Lighthouse
   CI for lab.
5. Conformance statements ride axe-core CI + manual keyboard testing.

## Applies On Top Of

- `runbook-author` — replaces generic deploy verbs with `nuxi` +
  Nitro-preset-specific commands.
- `launch-comms-author` — adds status-page wiring (BetterStack /
  Statuspage / native if host provides).
- `optimization-loop-author` — names the dual-metric loop (host
  RUM + Lighthouse CI).
- `optimization-backlog-author` — backlog row schema includes the
  preview deploy URL + RUM/Lighthouse delta evidence.
- `conformance-statement-author` — adds axe-core CI configuration +
  manual keyboard-test checklist.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Nuxt deploy verbs (preset-agnostic)

| Operation | Command |
|---|---|
| Build for the chosen preset | `nuxi build` (preset from `nuxt.config.ts` or `NITRO_PRESET` env) |
| Local production preview | `nuxi preview` |
| Generate static site (SSG-only) | `nuxi generate` |
| Module ecosystem update | `nuxi upgrade` |

Host-specific verbs (deploy / promote / rollback / env) defer to the
chosen Nitro preset's host overlay (`house-site-operate-vercel`,
`-netlify`, or `-cloudflare`).

- **Preview-deploy-per-PR** is mandatory regardless of host.
- **Production deploys** are gated on Lighthouse CI + axe-core +
  type-check + visual regression.
- **Rollback target ≤ 30 s** from incident detection; rehearsed
  monthly; mechanism is host-specific.

### ISR + on-demand revalidation

- **Nitro `routeRules`** in `nuxt.config.ts` declares per-route
  rendering strategy:
  ```ts
  routeRules: {
    '/': { isr: 60 },                 // ISR with 60s cadence
    '/api/**': { cors: true },        // CORS for API routes
    '/admin/**': { ssr: false },      // SPA mode for admin
    '/static/**': { prerender: true } // SSG at build time
  }
  ```
- **On-demand revalidation** via host-specific revalidation API
  (Vercel: `revalidatePath()`; Netlify: function with cache-tag
  invalidation; Cloudflare: KV-based cache busting).
- **Webhook-driven** from CMS for content-change-triggered
  revalidation; webhook authentication via shared-secret HMAC.

### Observability stack

- **Sentry** via `@sentry/nuxt`:
  - Service tags: `service`, `env`, `release` (Git SHA), `tenant`
    when multi-tenant.
  - Release markers wired via Nitro `nitro:build:public-assets` hook +
    GitHub Action on production deploy.
  - Source maps uploaded automatically.
- **Host RUM** (Vercel Web Analytics, Netlify Analytics, or Cloudflare
  Web Analytics) for field CWV.
- **Plausible / Fathom** for marketing analytics (privacy posture).
- **PostHog** when product analytics + experiments matter.
- **Custom Sentry metric** for `THREE.WebGLRenderer.info` when WebGL
  is in use.

### Lighthouse CI + axe-core CI

- **Lighthouse CI** runs on every preview deploy via `@lhci/cli` on
  GitHub Actions / the chosen CI platform.
  - Budgets per page type from `house-site-build-nuxt` SRS bundle
    table; LCP / INP / CLS thresholds enforced.
  - Configuration in `lighthouserc.json` at repo root.
- **axe-core CI** via `@axe-core/playwright` or Histoire's a11y
  addon (when available) or via E2E suite.
  - Fails the build on serious / critical violations.
  - **Honest disclaimer** in conformance-statement: axe catches ~30–
    40% of real WCAG 2.2 barriers; manual keyboard + screen-reader
    testing covers the rest.

### Status page + launch comms

- Same auto-incident-trigger pattern as Combo A.
- **BetterStack** is the rising default for non-Vercel-bundled hosts.
- **Launch-day comms** templates same as Combo A (internal go/no-go,
  external announcement, customer support FAQ, status page initial
  post).
- **Post-launch hypercare** SLA: 30-minute response on Sentry critical
  alerts for the first 72 hours.

### Release discipline

- **Feature flags** via Vercel Edge Config (when on Vercel preset),
  Netlify Edge Functions (when on Netlify), Cloudflare KV (when on
  Cloudflare), or a vendor-neutral choice (LaunchDarkly, Statsig,
  PostHog Feature Flags).
- **Canary** via Nitro middleware reading the flag store.
- **Rollback automation** wired to Sentry: error rate > 5% sustained
  3 min triggers automated rollback via host CLI.
- **Go/no-go checklist** deferred to `release-discipline-author` (PR
  #7); the user-invocable `draft-release-plan` covers it now.

## Override Behavior

This overlay applies when:

- The project ships on Nuxt 3 with a Nitro preset (Combo B).
- All five mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

The host-specific deploy details (deploy verbs, environment-variable
management, rollback automation) are deferred to the
`house-site-operate-{vercel,netlify,cloudflare}` overlay matching the
chosen Nitro preset. Mixing operate-overlays across hosts is a bug.

If the project ships on Nuxt but uses a host without a published
overlay (e.g., bare-metal Node), the host-specific section becomes
advisory and the operator authors a project-local runbook
supplement.

Cross-cutting concerns defer to dedicated atoms per A62 anti-trigger
fallback:

- Performance budgets enforced in CI — use
  `performance-budget-author`; the user-invocable
  `draft-perf-budget` covers it now.
- WCAG 2.2 motion-criteria conformance — use
  `motion-conformance-author`; the user-invocable
  `draft-motion-conformance` covers it now.
- Analytics event taxonomy + Zod schema validation — use
  `analytics-instrumentation-author`; the user-invocable
  `draft-analytics-spec` covers it now.
- Error monitoring tool selection + instrumentation conventions — use
  `error-monitoring-setup-author`; the user-invocable
  `draft-observability-spec` covers it now.
- Release flag + canary + rollback automation — use
  `release-discipline-author`; the user-invocable
  `draft-release-plan` covers it now.

## See Also

- `house-site-build-nuxt` — SRS / ADR / schedule / runbook / threat-
  model conventions for Combo B.
- `house-site-design-nuxt` — design-system + motion conventions for
  Combo B.
- `house-site-operate-{vercel,netlify,cloudflare}` — host-specific
  conventions for the chosen Nitro preset.
- `docs/research/E3-technical-conventions.md` §1, §4, §5 — evidence.
