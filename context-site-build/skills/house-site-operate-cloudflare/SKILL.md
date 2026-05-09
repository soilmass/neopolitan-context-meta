---
name: house-site-operate-cloudflare
description: >
  Hosting-platform overlay encoding Cloudflare-specific operational
  conventions (Pages for static + Functions; Workers for compute; R2
  for S3-compatible object storage with no egress; KV for key-value;
  Durable Objects for stateful coordination; D1 for SQLite at edge;
  wrangler CLI deploys; Cloudflare Web Analytics; Sentry browser SDK;
  Page Rules + Cache Rules for cache strategy). Stack-agnostic —
  applies on top of any frontend stack deployed to Cloudflare Pages
  (Astro / Nuxt / SvelteKit / Next.js OpenNext). Overlays
  runbook-author, launch-comms-author, optimization-loop-author,
  optimization-backlog-author. Do NOT use for: framework-specific
  conventions on Cloudflare (use house-site-operate-{nuxt,astro,
  sveltekit} which compose with this overlay); hosting on Vercel or
  Netlify (use the matching overlay); composing this overlay with a
  per-team overlay (deferred per ARCHITECTURE.md).
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

# house-site-operate-cloudflare

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Hosting-platform overlay codifying Cloudflare-specific operational
conventions, framework-agnostic. Cloudflare Pages is rising fast in
2025 (especially for Astro per E3 §5).

## Purpose

Encode the Cloudflare-specific operational patterns:

1. Pages for static + Functions; Workers for arbitrary compute.
2. R2 for object storage (S3-compatible; no egress fees).
3. KV for key-value (eventually-consistent global edge cache).
4. D1 for SQLite at edge.
5. Durable Objects for stateful coordination (single-region
   strong consistency; multi-region eventual).
6. wrangler CLI for deploys + secret management.
7. Page Rules + Cache Rules for cache strategy.
8. Cloudflare Web Analytics for field RUM (no cookies); Sentry for
   errors.

## Applies On Top Of

- `runbook-author` — adds Cloudflare-specific deploy verbs (wrangler
  deploy / publish / rollback / secret put / tail).
- `launch-comms-author` — adds Cloudflare status page wiring +
  CDN/Workers incident copy templates.
- `optimization-loop-author` — names the Cloudflare-specific RUM
  signals (Web Analytics) and the optimization surface (Worker CPU
  time, KV read latency, R2 cache hit rate).
- `optimization-backlog-author` — backlog row schema includes the
  Cloudflare deployment ID + Web Analytics segment.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### wrangler deploy verbs

| Operation | Command |
|---|---|
| Deploy a Pages project | `wrangler pages deploy <dist-dir>` |
| Deploy a Worker | `wrangler deploy` (reads `wrangler.toml`) |
| Rollback a Worker | `wrangler rollback <deployment-id>` |
| Set a secret | `wrangler secret put <NAME>` |
| Tail logs | `wrangler tail` (Workers) / `wrangler pages deployment tail` (Pages) |
| Inspect deployment | `wrangler deployments list` |
| Local dev (Workers + Miniflare) | `wrangler dev` |

- **Preview-deploy-per-PR** via the Cloudflare Pages Git integration
  (auto-comment on PR with preview URL).
- **Production deploys** are gated on framework-specific gates (per
  the framework operate overlay).
- **Rollback target ≤ 30 s**; Workers rollback is atomic.

### Pages vs Workers selection

| Use case | Tool |
|---|---|
| Static site (any framework's static build) | Cloudflare Pages |
| Static + Functions (form handlers, API routes) | Cloudflare Pages with Functions in `/functions` |
| Pure compute / scheduled tasks / event-driven | Cloudflare Workers (standalone) |
| Streaming response / WebSocket / Durable state | Workers + Durable Objects |
| Image transformation / video on the fly | Cloudflare Images / Stream |

### Storage primitives

| Store | Use case | Constraints |
|---|---|---|
| **R2** (object storage) | Assets, exports, backups, large blobs | S3-compatible; no egress fees within Cloudflare; ≤ 10 GB single object |
| **KV** (key-value) | Session state, feature flags, lightweight cache | Eventually-consistent across regions; values ≤ 25 MB; reads cached at edge |
| **D1** (SQLite at edge) | Relational data, structured queries | Single primary region; replicas eventually-consistent |
| **Durable Objects** | Single-region strong consistency, stateful coordination | Single instance per object key; in-memory state survives requests |
| **Queues** | Async work | Up to 10 producers / 10 consumers per queue |

### Cache strategy

- **Cache Rules** at the dashboard / API level for path-based caching.
- **Page Rules** legacy — use Cache Rules for new projects.
- **`Cache-Control`** headers respected by Cloudflare's edge.
- **Worker `cache.put` / `cache.match`** for programmatic caching.
- **Cache tag purging** via API (Enterprise plan) for surgical
  invalidation.

### Observability stack

- **Cloudflare Web Analytics** for page-view + CWV (privacy-friendly,
  no cookies).
- **Sentry** via `@sentry/browser` (no Cloudflare-specific SDK as
  of late 2025); release markers via `sentry-cli` in CI.
- **Workers Analytics Engine** for custom metrics (queries via
  Cloudflare API).
- **Tail logs** via `wrangler tail`; integrate with Logflare /
  Datadog for retention.
- **Custom Sentry metric** for `THREE.WebGLRenderer.info` when WebGL
  in use.

### Cron triggers

- **Cron Triggers** in `wrangler.toml` for scheduled Worker
  invocation (cron syntax).
- **Multi-cron**: configure multiple `triggers.crons` entries.
- **Free tier**: up to 10 cron triggers per Worker.

### Status page + launch comms

- **External status page** (Statuspage / BetterStack); Cloudflare
  doesn't offer a bundled status page for customer projects.
- **Auto-incident triggers** from Sentry alerts (same thresholds as
  other hosting overlays).
- **Cloudflare's own status** at `cloudflarestatus.com` is the
  upstream signal; subscribe via webhook for incident propagation
  to the customer status page.

## Override Behavior

This overlay applies when:

- The project ships on Cloudflare Pages (with optional Workers /
  Functions).
- All four mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

The wrangler deploy-verb section is **non-overridable**: mixing
across hosts is a bug.

This overlay composes with the framework-specific operate overlay
(`house-site-operate-{nuxt,astro,sveltekit}`):

- The framework overlay encodes framework-specific patterns.
- This overlay encodes Cloudflare-platform patterns regardless of
  framework.
- For Next.js on Cloudflare via OpenNext, this overlay applies and
  the operator references `house-site-operate-nextjs` advisorily
  for RSC patterns.

Cross-cutting concerns defer to dedicated atoms per A62 anti-trigger
fallback. See `house-site-operate-nextjs` for the canonical list.

## See Also

- `house-site-operate-{nuxt,astro,sveltekit}` — framework-specific
  operate overlays; this overlay composes with each.
- `house-site-operate-{vercel,netlify}` — alternative hosting
  overlays.
- `docs/research/E3-technical-conventions.md` §5 (combo notes
  re: Cloudflare Pages rising for Astro / Combo C).
