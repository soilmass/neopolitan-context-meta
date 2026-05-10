---
name: house-site-operate-astro
description: >
  House conventions for the site-operate family on the Combo C stack
  (Astro static-first + Vercel/Netlify/Cloudflare Pages + Sentry).
  Overlays runbook-author, launch-comms-author, optimization-loop-
  author, optimization-backlog-author, and conformance-statement-
  author with Astro-build deploy verbs, host-deferred operations,
  Sentry browser SDK conventions, Lighthouse CI gating tighter than
  Combos A/B, and axe-core a11y CI. Do NOT use for: SRS / ADR /
  threat-model on Astro (use house-site-build-astro); design-system
  / motion conventions on Astro (use house-site-design-astro);
  hosting-platform conventions independent of Astro (use
  house-site-operate-{vercel,netlify,cloudflare}); composing this
  overlay with a per-team overlay (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, stack-overlay]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 stack-
            overlay batch (Astro × 3). Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-operate-astro

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay encoding launch + post-launch operational conventions
on the Combo C stack.

This overlay applies on top of the family's mechanism atoms
with stack-specific or hosting-platform conventions. Composing
with a per-team overlay, or replacing it with a different family
overlay independent of this one, is deferred per ARCHITECTURE.md.
The site-operate family's threat-model and design coverage live
in their own overlays.

## Purpose

Encode how runbook, launch comms, optimization loops, and a11y
conformance ride on Astro static-first deploys:

1. Runbook deploy verbs use `astro build` + the chosen host's CLI.
2. Static-first deploys imply no runtime cold-starts; rollback target
   is host-dependent but typically faster than Combos A/B.
3. Sentry instrumentation uses `@sentry/browser` (no Astro-specific
   SDK as of late 2025); release markers wired via build env vars.
4. Optimization loops favor field RUM (host-provided) — Astro's
   static model produces excellent CWV by default; optimization
   surfaces tend to be image / font / island-hydration bottlenecks
   rather than server-render time.
5. Conformance statements ride axe-core CI + manual keyboard testing.

## Applies On Top Of

- `runbook-author` — replaces generic deploy verbs with `astro` + host
  CLI; static-build cadence implies build-time-heavy / runtime-light
  tradeoffs.
- `launch-comms-author` — adds status-page wiring; CDN-incident copy
  templates.
- `optimization-loop-author` — names the field-vs-lab loop favoring
  field RUM (Astro's static-first model produces excellent CWV by
  default).
- `optimization-backlog-author` — backlog row schema includes the
  preview deploy URL + Lighthouse / RUM delta + island-hydration cost
  evidence.
- `conformance-statement-author` — adds axe-core CI configuration +
  manual keyboard-test checklist.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Astro deploy verbs

| Operation | Command |
|---|---|
| Static build for the chosen adapter | `astro build` |
| Local production preview | `astro preview` |
| Add an integration / framework | `astro add <pkg>` |
| Sync content collections types | `astro sync` |

Host-specific verbs (deploy / promote / rollback / env) defer to the
chosen host overlay (`house-site-operate-{vercel,netlify,cloudflare}`).

- **Preview-deploy-per-PR** is mandatory.
- **Production deploys** are gated on Lighthouse CI + axe-core +
  type-check + visual regression.
- **Rollback target ≤ 30 s** from incident detection — typically fast
  for static deploys; immediate for atomic CDN-flip hosts.

### Static + selective SSR operations

- **Static-by-default**: most Combo-C projects deploy as fully static.
- **SSR adapters** (`@astrojs/{vercel,netlify,cloudflare,node}`) only
  when justified per the `house-site-build-astro` ADR.
- **On-demand revalidation** is host-specific:
  - Vercel: Astro builds emit static HTML; revalidation via
    `vercel build --prod` + cache purge.
  - Netlify: build hooks triggered by CMS webhook → rebuild.
  - Cloudflare Pages: Workers KV-tagged purge.
- **Time-based rebuilds** for content-heavy projects: scheduled CI
  build via cron (e.g., daily at 03:00 UTC).

### Observability stack

- **Sentry** via `@sentry/browser`:
  - Service tags: `service`, `env`, `release` (Git SHA), `tenant`
    when multi-tenant.
  - Release markers wired via build env var → Sentry CLI
    `sentry-cli releases new <release>` step in CI.
  - Source maps uploaded automatically.
- **Host RUM** (Vercel Web Analytics, Netlify Analytics, Cloudflare
  Web Analytics) for field CWV.
- **Plausible / Fathom** for marketing analytics.
- **PostHog** when product analytics + experiments matter.
- **Custom Sentry metric** for `THREE.WebGLRenderer.info` when WebGL
  hero island present.

### Lighthouse CI + axe-core CI

- **Lighthouse CI** budgets are tighter than Combos A/B (Astro's
  static model affords it):
  - LCP ≤ 1.8s p75 mobile; ≤ 1.2s p75 desktop
  - INP ≤ 200ms p75
  - CLS ≤ 0.05 p75
- **axe-core CI** via `@axe-core/playwright` E2E suite OR the chosen
  Storybook/Ladle a11y addon.
- **Honest disclaimer** in conformance-statement: axe catches ~30–
  40% of real WCAG 2.2 barriers.

### Status page + launch comms

- Same auto-incident-trigger pattern as Combos A/B.
- **Static deploys** typically don't need elaborate status pages
  (CDN failures are the main risk; Sentry frontend-error rate is the
  primary signal).
- **Launch-day comms** templates same as Combos A/B.

### Release discipline

- **Feature flags** via host-specific store (Vercel Edge Config,
  Cloudflare KV, Netlify Edge Functions) OR vendor-neutral
  (LaunchDarkly, Statsig, PostHog Feature Flags).
- **Canary** via host-specific routing (Cloudflare's traffic-splitting
  is the most native for Combo C).
- **Rollback automation** wired to Sentry: error rate > 5% sustained
  3 min triggers automated rollback via host CLI.
- **Go/no-go checklist** deferred to `release-discipline-author` (PR
  #7); the user-invocable `draft-release-plan` covers it now.

## Override Behavior

This overlay applies when:

- The project ships on Astro (static or SSR).
- All five mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

The host-specific deploy details defer to the chosen host overlay
(`house-site-operate-{vercel,netlify,cloudflare}`). Mixing operate-
overlays across hosts is a bug.

If the project moves to SSR-mode-heavy use, the static-first
optimization defaults become advisory; budgets relax toward Combos
A/B levels.

Cross-cutting concerns defer to dedicated atoms per A62 anti-trigger
fallback. See `house-site-operate-nextjs` for the canonical fallback
list.

## See Also

- `house-site-build-astro` — SRS / ADR / schedule / runbook / threat-
  model conventions for Combo C.
- `house-site-design-astro` — design-system + motion conventions for
  Combo C.
- `house-site-operate-{vercel,netlify,cloudflare}` — host-specific
  conventions.
- `docs/research/E3-technical-conventions.md` §1, §4, §5 — evidence.
