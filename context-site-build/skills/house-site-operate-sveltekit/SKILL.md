---
name: house-site-operate-sveltekit
description: >
  House conventions for the site-operate family on the Combo D stack
  (SvelteKit + adapter + Sentry + Plausible/Fathom). Overlays
  runbook-author, launch-comms-author, optimization-loop-author,
  optimization-backlog-author, and conformance-statement-author with
  SvelteKit deploy verbs (vite build + adapter + host CLI), strict
  performance-pure RUM ties, Sentry instrumentation, Lighthouse CI
  gating with Combo D's tighter thresholds, and axe-core a11y CI.
  Do NOT use for: SRS / ADR / threat-model on SvelteKit (use
  house-site-build-sveltekit); design-system / motion conventions on
  SvelteKit (use house-site-design-sveltekit); hosting-platform
  conventions independent of SvelteKit (use
  house-site-operate-{vercel,netlify,cloudflare}); composing this
  overlay with a per-team overlay (deferred per ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, stack-overlay]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 stack-
            overlay batch (SvelteKit × 3). Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-operate-sveltekit

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay encoding launch + post-launch operational conventions
on the Combo D stack.

This overlay applies on top of the family's mechanism atoms
with stack-specific or hosting-platform conventions. Composing
with a per-team overlay, or replacing it with a different family
overlay independent of this one, is deferred per ARCHITECTURE.md.
The site-operate family's threat-model and design coverage live
in their own overlays.

## Purpose

Encode how runbook, launch comms, optimization loops, and a11y
conformance ride on SvelteKit + adapter + Sentry + analytics:

1. Runbook deploy verbs use `vite build` + the chosen adapter +
   host CLI.
2. The performance-pure brand promise locks RUM thresholds to the
   strictest of the four combos (LCP / INP / CLS p75 thresholds match
   Astro's tighter set).
3. Sentry instrumentation uses `@sentry/sveltekit`; release markers
   wired via SvelteKit hooks.
4. Optimization loops favor field RUM (host-provided) tied to the
   strict thresholds; lab Lighthouse CI is the secondary gate.
5. Conformance statements ride axe-core CI + manual keyboard testing.

## Applies On Top Of

- `runbook-author` — replaces generic deploy verbs with `vite build`
  + adapter-specific commands.
- `launch-comms-author` — adds status-page wiring; CDN-incident copy.
- `optimization-loop-author` — names the field-vs-lab loop tied to
  the performance-pure brand promise.
- `optimization-backlog-author` — backlog row schema includes the
  preview deploy URL + RUM/Lighthouse delta + Svelte-component
  hydration cost evidence.
- `conformance-statement-author` — adds axe-core CI configuration +
  manual keyboard-test checklist.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### SvelteKit deploy verbs

| Operation | Command |
|---|---|
| Build with the chosen adapter | `vite build` (adapter from `svelte.config.js`) |
| Local production preview | `vite preview` |
| Type-check | `svelte-check --tsconfig ./tsconfig.json` |
| Lint | `eslint .` + `prettier --check .` |

Host-specific verbs (deploy / promote / rollback / env) defer to the
chosen adapter's host overlay.

- **Preview-deploy-per-PR** is mandatory.
- **Production deploys** are gated on Lighthouse CI + axe-core +
  svelte-check + visual regression.
- **Rollback target ≤ 30 s** from incident detection; rehearsed
  monthly.

### Form actions + load-function operations

- **Form actions** (`+page.server.ts` `actions: { default: ... }`)
  are progressive-enhancement-default; non-JS clients still post.
- **Load functions** errors propagate via SvelteKit's `error()` helper
  with HTTP status codes.
- **Server endpoints** (`+server.ts`) for API surfaces; CSRF protected
  via SvelteKit's built-in token (form actions auto-protected).

### Observability stack

- **Sentry** via `@sentry/sveltekit`:
  - Service tags: `service`, `env`, `release` (Git SHA), `tenant`
    when multi-tenant.
  - Hooks-wired for `handleError` and `handleClientError`.
  - Release markers via Sentry CLI in CI on production deploy.
  - Source maps uploaded automatically.
- **Host RUM** for field CWV.
- **Plausible / Fathom** for marketing analytics.
- **PostHog** when product analytics + experiments matter.
- **Custom Sentry metric** for `THREE.WebGLRenderer.info` when WebGL
  in use.

### Lighthouse CI + axe-core CI (strict)

- **Lighthouse CI** budgets reflect the performance-pure brand
  promise:
  - LCP ≤ 1.8s p75 mobile (matches Astro's tighter set, NOT Combos
    A/B's relaxed set)
  - INP ≤ 200ms p75 (the Achilles heel of WebGL; strictly enforced
    here)
  - CLS ≤ 0.05 p75
- **axe-core CI** via `@axe-core/playwright` E2E suite OR Histoire/
  Storybook a11y addon.
- **Honest disclaimer** in conformance-statement: axe catches ~30–40%
  of real WCAG 2.2 barriers.

### Status page + launch comms

- Same auto-incident-trigger pattern as other combos.
- **Launch-day comms** templates same.
- **Post-launch hypercare** SLA: 30-minute response on Sentry
  critical alerts for the first 72 hours.

### Release discipline

- **Feature flags** via host-specific store OR vendor-neutral.
- **Canary** via SvelteKit hook (`handle` in `hooks.server.ts`)
  reading the flag store and rewriting based on bucket.
- **Rollback automation** wired to Sentry: error rate > 5% sustained
  3 min triggers automated rollback via host CLI.
- **Go/no-go checklist** deferred to `release-discipline-author` (PR
  #7); the user-invocable `draft-release-plan` covers it now.

## Override Behavior

This overlay applies when:

- The project ships on SvelteKit with an adapter (Combo D).
- All five mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

The host-specific deploy details defer to the chosen adapter's host
overlay (`house-site-operate-{vercel,netlify,cloudflare}`). Mixing
operate-overlays across hosts is a bug.

If the project moves away from the performance-pure brand promise,
the strict RUM thresholds become advisory; budgets relax toward
Combos A/B levels and the divergence is documented in an ADR.

Cross-cutting concerns defer to dedicated atoms per A62 anti-trigger
fallback. See `house-site-operate-nextjs` for the canonical list.

## See Also

- `house-site-build-sveltekit` — SRS / ADR / schedule / runbook /
  threat-model conventions for Combo D.
- `house-site-design-sveltekit` — design-system + motion conventions
  for Combo D.
- `house-site-operate-{vercel,netlify,cloudflare}` — host-specific
  conventions for the chosen adapter.
- `docs/research/E3-technical-conventions.md` §1, §4, §5 — evidence.
