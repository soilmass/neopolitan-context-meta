---
name: house-site-operate-netlify
description: >
  Hosting-platform overlay for Netlify-specific operational
  conventions. Codifies preview-deploy-per-PR via deploy contexts,
  Edge Functions, Netlify Blobs object storage, Forms,
  Identity for auth, Functions for serverless, Lighthouse CI
  integration via build plugin, and build plugins for extra
  gates. Overlays runbook-author, launch-comms-author,
  optimization-loop-author, optimization-backlog-author.
  Composes with the framework-specific operate overlays
  (house-site-operate-nuxt, house-site-operate-astro,
  house-site-operate-sveltekit). Do NOT use for: hosting on
  Vercel or Cloudflare (use the matching overlay).
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

# house-site-operate-netlify

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Hosting-platform overlay codifying Netlify-specific operational
conventions, framework-agnostic. Netlify retains a Nuxt + Astro
footprint per E3 §5.

This overlay applies on top of the family's mechanism atoms
with stack-specific or hosting-platform conventions. Composing
with a per-team overlay, or replacing it with a different family
overlay independent of this one, is deferred per ARCHITECTURE.md.
The site-operate family's threat-model and design coverage live
in their own overlays.

## Purpose

Encode the Netlify-specific operational patterns:

1. Deploy contexts (production / branch-deploy / deploy-preview)
   provide preview-per-PR via Git integration.
2. Functions for serverless; Edge Functions for streaming + edge-
   region work.
3. Netlify Blobs for object storage; Forms for built-in form
   handling; Identity for auth.
4. Build plugins extend CI (Lighthouse CI plugin, sitemap submit,
   image optimization, etc.).
5. Netlify CLI (`netlify`) for deploys + secrets + functions invoke.

## Applies On Top Of

- `runbook-author` — adds Netlify-specific deploy verbs (deploy /
  rollback / env / functions:invoke / dev).
- `launch-comms-author` — adds Netlify status page wiring + CDN
  incident copy templates.
- `optimization-loop-author` — names the Netlify-specific RUM signals
  (Netlify Analytics) and the optimization surface (function cold
  start, build cache hit rate, asset-CDN hit rate).
- `optimization-backlog-author` — backlog row schema includes the
  Netlify deploy ID + Analytics segment.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Netlify deploy verbs

| Operation | Command |
|---|---|
| Deploy preview from local | `netlify deploy` (alias to a unique URL) |
| Deploy production from local | `netlify deploy --prod` |
| Auto preview-per-PR | Via Netlify Git integration (default) |
| Rollback production | `netlify rollback` (CLI) OR via dashboard "Restore deploy" |
| Set env var | `netlify env:set <NAME> <VALUE>` |
| Pull env to local `.env` | `netlify env:list` + manual sync (no `pull` shortcut) |
| Invoke a Function locally | `netlify functions:invoke <name>` |
| Local dev | `netlify dev` |
| Tail function logs | `netlify functions:log <name>` |

- **Preview-deploy-per-PR** is mandatory; auto via Git integration.
- **Branch deploys** for long-lived feature branches (separate from
  PR previews).
- **Production deploys** are gated on framework-specific gates +
  Netlify build plugins (Lighthouse CI).
- **Rollback target ≤ 30 s** via dashboard "Restore deploy"; CLI
  rollback is also instant.

### Deploy contexts

- **production** — main branch / production-flagged branch.
- **deploy-preview** — pull-request-triggered.
- **branch-deploy** — non-main branch pushed (configurable per
  branch).
- **`netlify.toml`** [context.production] / [context.deploy-preview]
  / [context.branch-deploy] sections configure per-context env vars
  and build settings.

### Functions vs Edge Functions

| Use case | Function type |
|---|---|
| Edge-region-sensitive (geo lookup, A/B test, redirects) | Edge Function |
| Streaming response | Edge Function |
| Simple short-lived API (auth, form post, webhook) | Function (Node.js / Deno runtime) |
| CPU-heavy or long-running | Function with extended timeout |
| Uses Node.js APIs requiring full runtime | Function (not Edge) |

- **Function selection** documented per route in the framework-
  specific build overlay's ADR.
- **Function timeout**: 10s default; up to 26s for "Background
  Functions" (async); up to 15min for "Scheduled Functions".

### Storage + first-class services

| Service | Use case |
|---|---|
| **Netlify Blobs** (object storage) | Assets, exports, K/V-shaped data; key-prefix queries supported |
| **Netlify Forms** | Built-in form-submission handling without custom backend |
| **Netlify Identity** | Auth (GoTrue under the hood); good for marketing-site light auth, not full app auth |
| **Netlify Functions** + external DB | Persistent relational data via external Postgres (Supabase / Neon / RDS) |

### Build plugins

- **`@netlify/plugin-lighthouse`** for Lighthouse CI on every
  deploy.
- **`@netlify/plugin-sitemap`** for sitemap generation.
- **`netlify-plugin-image-optim`** for asset compression.
- **`netlify-plugin-checklinks`** for broken-link detection.
- **`netlify-plugin-submit-sitemap`** for search-engine submission.
- **Custom build plugins** in `plugins/` directory of repo for
  project-specific gates.

### Observability stack

- **Netlify Analytics** (paid add-on; opt-in) for server-side
  page-view + referrer + CWV.
- **Plausible / Fathom** for marketing analytics with privacy
  posture (added via embed).
- **Sentry** via `@sentry/browser` (no Netlify-specific SDK as of
  late 2025); release markers via `sentry-cli` in CI.
- **Netlify Function logs** via `netlify functions:log` or
  dashboard; integrate with Datadog / Logflare for retention.
- **Custom Sentry metric** for `THREE.WebGLRenderer.info` when WebGL
  in use.

### Scheduled work

- **Scheduled Functions** in `netlify.toml` for cron-driven
  invocation (cron syntax).
- **Background Functions** for async work that doesn't need to
  return immediately.
- **Limit**: scheduled-function frequency capped per plan.

### Status page + launch comms

- **External status page** (Statuspage / BetterStack); Netlify
  doesn't offer a bundled customer-status-page.
- **Auto-incident triggers** from Sentry alerts (same thresholds).
- **Netlify's own status** at `netlifystatus.com` is the upstream
  signal; subscribe via webhook for propagation.

## Override Behavior

This overlay applies when:

- The project ships on Netlify.
- All four mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

The Netlify deploy-verb section is **non-overridable**: mixing
across hosts is a bug.

This overlay composes with the framework-specific operate overlay
(`house-site-operate-{nuxt,astro,sveltekit}`); the framework
overlay covers framework-specific patterns, this overlay covers
Netlify-platform patterns.

Cross-cutting concerns defer to dedicated atoms per A62 anti-trigger
fallback. See `house-site-operate-nextjs` for the canonical list.

## See Also

- `house-site-operate-{nuxt,astro,sveltekit}` — framework-specific
  operate overlays; this overlay composes with each.
- `house-site-operate-{vercel,cloudflare}` — alternative hosting
  overlays.
- `docs/research/E3-technical-conventions.md` §5 (combo notes
  re: Netlify retaining Nuxt / Astro footprint).
