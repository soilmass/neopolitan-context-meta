---
name: house-site-operate-vercel
description: >
  Hosting-platform overlay encoding Vercel-specific operational
  conventions (preview-deploy-per-PR, ISR via revalidate / revalidateTag
  / revalidatePath, Edge vs Serverless function selection rules,
  Vercel Blob for assets, Vercel Web Analytics + Speed Insights, env
  variable management via Vercel CLI, vercel.json cron jobs, KV +
  Postgres + Edge Config when state needed). Stack-agnostic — applies
  on top of any frontend stack deployed to Vercel (Next.js / Nuxt /
  Astro / SvelteKit / static). Overlays runbook-author, launch-comms-
  author, optimization-loop-author, optimization-backlog-author. Do NOT
  use for: framework-specific operational conventions on Vercel (use
  house-site-operate-{nextjs,nuxt,astro,sveltekit} which compose with
  this overlay); hosting on Cloudflare Pages or Netlify (use the
  matching overlay); composing this overlay with a per-team overlay
  (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, hosting]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 hosting
            overlay batch. Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-operate-vercel

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Hosting-platform overlay codifying Vercel-specific operational
conventions, framework-agnostic.

## Purpose

Encode the Vercel-specific operational patterns that apply
regardless of frontend framework:

1. Preview-deploy-per-PR is the deploy model; production promotion
   is a manual `vercel promote` or auto-promote-on-merge.
2. ISR + Edge Functions use Vercel's revalidation primitives
   (`revalidate` time-based, `revalidateTag()` / `revalidatePath()`
   on-demand).
3. Edge vs Serverless function selection is documented per route;
   regions are configured intentionally.
4. Asset hosting uses Vercel Blob (S3-compatible) or Cloudinary;
   `next/image` (or framework-equivalent) handles optimization.
5. Vercel Web Analytics + Speed Insights provide field RUM; Sentry
   is the error monitor.
6. Environment variables, KV, Postgres, and Edge Config are
   accessed via Vercel CLI / dashboard.

## Applies On Top Of

- `runbook-author` — adds Vercel-specific deploy verbs (deploy /
  promote / rollback / env / domains / inspect / logs).
- `launch-comms-author` — adds Vercel-bundled status page wiring or
  Vercel CDN incident copy templates.
- `optimization-loop-author` — names the Vercel-specific RUM signals
  (Web Analytics + Speed Insights) and the optimization surface
  (function timeout, ISR cache hit rate, Edge function regions).
- `optimization-backlog-author` — backlog row schema includes the
  Vercel deployment URL + Web Analytics segment.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Vercel deploy verbs

| Operation | Command | Notes |
|---|---|---|
| Deploy preview from local | `vercel deploy` | Aliased to a unique preview URL |
| Deploy preview from CI | Auto via Git integration on PR push | Comments on PR with preview URL |
| Promote to production | `vercel promote <preview-url>` | Or auto-promote-on-merge to main |
| Rollback production | `vercel rollback` (interactive) OR `vercel promote <prior-deployment-url>` | ≤ 30s |
| Set env var | `vercel env add <NAME> <env>` | env: development / preview / production |
| Pull env to local `.env` | `vercel env pull` | For local-dev parity |
| Inspect deployment | `vercel inspect <url>` | Build logs, function logs, etc. |
| Tail runtime logs | `vercel logs <url> --follow` | |
| Add custom domain | `vercel domains add <domain>` | |
| Wire Git integration | One-time via dashboard | Sets PR auto-preview |

- **Preview-deploy-per-PR** is mandatory.
- **Production deploys** are gated on the framework-specific gates
  (Lighthouse CI, axe-core, type-check, visual regression — wired
  per the framework's operate-overlay).
- **Rollback target ≤ 30 s** from incident detection; rehearsed
  monthly.

### ISR + on-demand revalidation

- **Time-based ISR** via the framework's revalidate semantics
  (Next.js `revalidate: 60` in fetch options; Nuxt `routeRules:
  { isr: 60 }`; Astro static + revalidate adapter).
- **On-demand revalidation** via `revalidateTag()` /
  `revalidatePath()` (Next.js); Nitro's revalidation API for Nuxt;
  build-trigger webhook for Astro.
- **CMS webhooks** trigger revalidation; webhook auth via shared-
  secret HMAC.

### Edge vs Serverless function selection

| Use case | Function type |
|---|---|
| Edge-region-sensitive (geo lookup, A/B test, redirects) | Edge Function |
| Streaming response (LLM, data fetching) | Edge Function |
| Simple short-lived API (auth, form post, webhook) | Serverless Function (default) |
| CPU-heavy or long-running (PDF generation, video processing) | Serverless Function (with extended timeout) |
| Uses Node.js APIs (fs, child_process) | Serverless Function (Edge doesn't support) |
| Stateful with long-lived connection | Vercel KV / Postgres / external service |

- **Function selection** is documented per route in the framework-
  specific build overlay's ADR.
- **Region configuration**: Edge auto-distributes; Serverless
  defaults to `iad1` (US East), configurable per function.
- **Function timeout**: Vercel Pro = 60s default; Hobby = 10s; alert
  at p95 > 30s.

### Asset hosting + image optimization

- **Vercel Blob** for self-hosted assets (S3-compatible API; no
  egress fees within Vercel network).
- **Cloudinary** when DAM features (transforms, derived assets,
  marketing self-service) matter.
- **Mux** for non-trivial video.
- **Framework `<Image>` component** handles optimization (Next.js
  `next/image`, Nuxt `<NuxtImg>`, Astro `<Image>` from
  `astro:assets`).

### Observability stack

- **Vercel Web Analytics** for page-view / referrer / CWV (privacy-
  friendly; no cookies).
- **Vercel Speed Insights** for field CWV (LCP / INP / CLS p75).
- **Sentry** for errors and performance tracing; release markers
  via `sentry-cli` step in CI.
- **Custom Sentry metric** for `THREE.WebGLRenderer.info` when WebGL
  in use.
- **Vercel Logs** for function-level inspection; integrate with
  Datadog / Splunk for long-term retention.

### State stores

| Store | Use case |
|---|---|
| **Vercel KV** (Redis-backed) | Session state, rate limits, feature flags |
| **Vercel Postgres** | Relational data (managed Neon under the hood) |
| **Edge Config** | Read-heavy configuration accessed at edge (feature flags, redirects, A/B test variants) |
| **Vercel Blob** | Object storage |

### Cron jobs + scheduled tasks

- **`vercel.json`** `crons` section for scheduled function invocation
  (cron syntax).
- **Limit**: Pro plan = 40 cron jobs across the team.
- **For higher volume / more complex schedules**: external service
  (Inngest, Temporal, Cloudflare Cron Triggers via a separate
  worker).

### Status page + launch comms

- **Vercel-bundled status page** (Vercel-hosted projects can opt
  into Vercel Status integration).
- **External status page** (Statuspage / BetterStack) for projects
  with custom-domain status pages or multi-platform footprint.
- **Auto-incident triggers** from Sentry alerts:
  - Error rate > 1% sustained 5 min → degraded
  - p95 INP > 500 ms sustained 10 min → degraded
  - Vercel function timeout rate > 5% sustained 5 min → degraded

## Override Behavior

This overlay applies when:

- The project ships on Vercel.
- All four mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

The Vercel deploy-verb section is **non-overridable**: if a project
ships on Cloudflare Pages or Netlify, switch to that hosting overlay.
Mixing host-specific runbook conventions across hosts is a bug.

This overlay composes with the framework-specific operate overlay
(`house-site-operate-{nextjs,nuxt,astro,sveltekit}`):

- The framework overlay encodes framework-specific patterns (RSC
  caching for Next.js; Nitro routeRules for Nuxt; static-first for
  Astro; adapter-driven for SvelteKit).
- This overlay encodes Vercel-platform patterns regardless of
  framework.
- When both apply, the framework overlay's patterns are richer for
  the framework-specific decisions; this overlay covers the
  platform-specific decisions.

Cross-cutting concerns defer to dedicated atoms per A62 anti-trigger
fallback. See `house-site-operate-nextjs` for the canonical list.

## See Also

- `house-site-operate-{nextjs,nuxt,astro,sveltekit}` — framework-
  specific operate overlays; this overlay composes with each.
- `house-site-operate-{cloudflare,netlify}` — alternative hosting
  overlays.
- `docs/research/E3-technical-conventions.md` §5 (combo notes
  re: Vercel as Combo A's default; rising for Astro / Combo C),
  §1 (perf budgets).
