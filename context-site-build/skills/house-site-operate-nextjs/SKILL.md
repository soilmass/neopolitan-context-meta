---
name: house-site-operate-nextjs
description: >
  House conventions for the site-operate family on the Combo A stack
  (Next.js + Vercel + Sentry + Plausible/Fathom). Overlays
  runbook-author, launch-comms-author, optimization-loop-author,
  optimization-backlog-author, and conformance-statement-author with
  Vercel-specific deploy verbs, ISR + Edge Function operational
  patterns, Sentry instrumentation conventions, Lighthouse CI gating,
  and axe-core a11y CI. Do NOT use for: SRS / ADR / threat-model
  conventions on Next.js (use house-site-build-nextjs); design-system /
  motion conventions on Next.js (use house-site-design-nextjs);
  hosting-platform conventions independent of Next.js (use
  house-site-operate-vercel); composing this overlay with a per-team
  overlay (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, stack-overlay]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 stack-
            overlay batch (Next.js × 3). Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-operate-nextjs

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay encoding launch + post-launch operational conventions
on the Combo A stack.

This overlay applies on top of the family's mechanism atoms
with stack-specific or hosting-platform conventions. Composing
with a per-team overlay, or replacing it with a different family
overlay independent of this one, is deferred per ARCHITECTURE.md.
The site-operate family's threat-model and design coverage live
in their own overlays.

## Purpose

Encode how runbook, launch comms, optimization loops, and a11y
conformance ride on Vercel + Next.js + Sentry + analytics:

1. Runbook deploy verbs use the Vercel CLI (`vercel deploy`,
   `vercel rollback`, `vercel env`, `vercel domains`).
2. ISR + Edge Function rollouts are managed via on-demand
   revalidation (`revalidateTag()`, `revalidatePath()`) plus
   preview deploys; the runbook templates this rather than
   replicating.
3. Launch comms include a status-page integration (Statuspage,
   BetterStack, or Vercel-bundled) with auto-incident triggers
   wired from Sentry alerts.
4. Optimization loops use Vercel Web Analytics + Speed Insights
   for field RUM, Lighthouse CI for lab metrics, and a Sentry
   custom metric for `THREE.WebGLRenderer.info` (when WebGL is
   used).
5. Conformance statements ride axe-core CI + manual keyboard
   testing; automated tools cover only ~30–40% (per E3 §4.4).

## Applies On Top Of

- `runbook-author` — replaces generic deploy verbs; adds Vercel-
  specific failure modes and rollback procedures.
- `launch-comms-author` — adds status-page wiring, customer-facing
  copy templates for known Vercel/CDN incident classes.
- `optimization-loop-author` — names the field-vs-lab dual-metric
  loop (Vercel Web Analytics + Speed Insights vs Lighthouse CI).
- `optimization-backlog-author` — backlog row schema includes the
  Vercel deployment URL + the Lighthouse / RUM delta evidence.
- `conformance-statement-author` — adds axe-core CI configuration
  + the manual keyboard-test checklist.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Vercel deploy verbs

| Operation | Command |
|---|---|
| Deploy preview from branch | `vercel deploy` (auto-aliased to PR URL) |
| Promote preview to production | `vercel promote <preview-url>` |
| Rollback production | `vercel rollback` (interactive selector) or `vercel promote <prior-deployment-url>` |
| Set env var | `vercel env add <NAME> <env>` (env: development / preview / production) |
| Inspect deployment | `vercel inspect <url>` |
| Tail logs | `vercel logs <url> --follow` |

- **Preview-deploy-per-PR** is mandatory; PRs without a passing
  preview deploy are blocked at review.
- **Production deploys** are gated on Lighthouse CI + axe-core +
  type-check + Chromatic visual regression.
- **Rollback target ≤ 30 s** from incident detection; rehearsed
  monthly.

### ISR + Edge Function operations

- **On-demand revalidation** is preferred over time-based ISR for
  CMS-driven content. Webhook → `revalidateTag('<tag>')` from a
  Next.js API route; Sanity webhook with shared-secret HMAC.
- **Time-based revalidation** is reserved for content with predictable
  freshness windows (homepage hero, status badges).
- **Edge vs Serverless function selection** documented per route in
  the SRS (per `house-site-build-nextjs`); operate-overlay verifies
  selection rules are followed in production via deployment
  inspection.
- **Function timeout monitoring**: Vercel Pro = 60s default; alert at
  p95 > 30s.

### Observability stack

- **Sentry** for error monitoring and performance tracing.
  - Service tags: `service`, `env`, `release` (Git SHA), `tenant`
    (when multi-tenant).
  - Release markers wired via `next.config.js` Sentry SDK +
    GitHub Action on production deploy.
  - Source maps uploaded automatically; sourcemaps in production
    artifacts are stripped.
- **Vercel Web Analytics + Speed Insights** for field RUM (CWV
  + custom events).
- **Plausible / Fathom** for marketing analytics (privacy posture).
- **PostHog** when product analytics + experiments matter.
- **Custom Sentry metric** for `THREE.WebGLRenderer.info` (calls,
  triangles, programs) when WebGL is in use; alerts fire on
  scene-graph regressions in the field.

### Lighthouse CI + axe-core CI

- **Lighthouse CI** runs on every preview deploy via `@lhci/cli`
  on GitHub Actions.
  - Budgets per page type from `house-site-build-nextjs` SRS bundle
    table; LCP / INP / CLS thresholds enforced.
  - Configuration in `lighthouserc.json` at repo root.
- **axe-core CI** via `@axe-core/playwright` or
  `@storybook/addon-a11y` (Chromatic-integrated).
  - Fails the build on serious / critical violations.
  - **Honest disclaimer** lives in the conformance-statement: axe-core
    catches ~30–40% of real WCAG 2.2 barriers; manual keyboard +
    screen-reader testing covers the rest.

### Status page + launch comms

- **Status page** (Statuspage, BetterStack, or Vercel-bundled status)
  with auto-incident triggers from Sentry alerts at:
  - Error rate > 1% sustained 5 min → degraded
  - p95 INP > 500 ms sustained 10 min → degraded
  - Vercel function timeout rate > 5% sustained 5 min → degraded
- **Launch-day comms** templates include:
  - Internal go/no-go email (Eng + Product + Marketing + Support)
  - External announcement (blog post + social with the launch URL)
  - Customer support FAQ (anticipated questions + escalation paths)
  - Status page initial post (clean state + monitoring channels
    listed)
- **Post-launch hypercare** SLA: 30-minute response on Sentry critical
  alerts for the first 72 hours.

### Release discipline

- **Feature flags** via Vercel Edge Config (when available) or
  LaunchDarkly / Statsig / PostHog Feature Flags.
- **Canary** for risky changes: 10% traffic via Edge Config flag,
  ramp to 50% / 100% over 24 h with monitoring.
- **Rollback automation** wired to Sentry: error rate > 5% sustained
  3 min triggers automated rollback to prior deployment.
- **Go/no-go checklist** (deferred to `release-discipline-author`
  in PR #7; the user-invocable `draft-release-plan` covers it now).

## Override Behavior

This overlay applies when:

- The project ships on Vercel + Next.js (Combo A).
- All five mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.
Per `ARCHITECTURE.md` §"Mechanism vs Policy", silent substitution is
forbidden.

The deploy-verb section is **non-overridable**: if you're not on
Vercel, use `house-site-operate-{cloudflare,netlify}` instead. Mixing
runbook conventions across hosts is a bug.

If the project ships on Vercel but uses a non-Combo-A frontend (e.g.,
Astro on Vercel), use `house-site-operate-vercel` directly — this
overlay assumes Next.js-specific patterns (RSC, ISR, Edge Functions).

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

- `house-site-build-nextjs` — SRS / ADR / schedule / runbook /
  threat-model conventions for the same stack.
- `house-site-design-nextjs` — design-system + motion conventions
  for the same stack.
- `house-site-operate-vercel` — hosting-platform conventions
  (Vercel-only, framework-agnostic; cited from this overlay).
- `docs/research/E3-technical-conventions.md` §1, §4, §5 — evidence.
