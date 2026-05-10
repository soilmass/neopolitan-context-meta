---
name: house-site-build-nuxt
description: >
  House conventions for the site-build family on a Nuxt 3 + Tailwind +
  Pinia + Storyblok/Sanity stack (Combo B "Vue/Nuxt-cinematic").
  Overlays srs-author, adr-author, master-schedule-author, runbook-
  author, and threat-model-author with Nuxt-specific NFRs, ADR
  templates, sprint cadence, deploy verbs (Nitro presets), and threat
  surfaces. Do NOT use for: design-system / motion / TresJS conventions
  on Nuxt (use house-site-design-nuxt); launch / observability
  conventions on Nuxt's Nitro hosts (use house-site-operate-nuxt or
  the host-specific operate overlay); composing this overlay with a
  per-team overlay (deferred per ARCHITECTURE.md).
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

# house-site-build-nuxt

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay applying Combo B ("Vue/Nuxt-cinematic" — Nuxt 3 +
Tailwind + Pinia + TresJS + GSAP) conventions to the site-build
family's stack-sensitive mechanism atoms.

## Purpose

Encode the conventions that turn the family's stack-neutral
mechanism atoms into Combo-B-shaped artifacts:

1. SRS NFRs cite Nuxt 3's hybrid rendering (SSR / SSG / ISR via Nitro
   `routeRules`), Pinia store conventions, auto-imports, and module
   selection rules.
2. ADR templates name Combo-B-typical decision points (Nitro preset
   per host, CMS choice — Storyblok vs Sanity, TresJS vs Three.js
   directly, server route vs API integration).
3. Master schedule cadence reflects Vue's component-per-file model and
   Nuxt's auto-import discipline.
4. Runbook deploy verbs use `nuxi`, the Nitro preset toolchain, and
   the host-specific CLI (`vercel`, `netlify`, `wrangler`).
5. Threat model attends to Storyblok/Sanity API exposure, server
   route enumeration, Pinia state hydration, and Nitro preset's
   environment-variable scoping.

## Applies On Top Of

- `srs-author` — adds Combo-B NFR rows + Nuxt bundle budget table +
  CMS query budget.
- `adr-author` — adds Combo-B decision-point catalog (Nitro preset,
  CMS choice, TresJS vs Three.js, auto-import scope).
- `master-schedule-author` — adopts the deploy-preview-per-PR cadence;
  sprint structure stays mechanism-driven.
- `runbook-author` — replaces generic deploy verbs with `nuxi build`,
  `nuxi preview`, and the chosen host's CLI.
- `threat-model-author` — adds Combo-B-specific threat surfaces (CMS
  webhook authentication, server route enumeration, Pinia hydration,
  module supply chain).

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Frontend

- **Nuxt 3 with TypeScript** (`tsconfig.json` extends Nuxt's strict
  preset).
- **Auto-imports** for composables and components (default Nuxt
  behavior); explicit imports only when the linter flags ambiguity.
- **Pinia** for state management; one store per domain area; SSR-safe
  hydration via `state()` factory pattern.
- **Server routes** (`server/api/*.ts`) for API endpoints rather than
  external API services for first-party operations.
- **Modules over plugins** when a module exists for the integration
  (Pinia, Tailwind, Sanity, Storyblok all have official modules).

### Bundle budgets

| Resource | Target | Enforcement |
|---|---|---|
| Critical-path JS (gz) | ≤ 130–170 KB marketing; ≤ 200 KB WebGL hero (excl. Three.js core) | Nuxt analyze + size-limit in CI |
| Total JS (gz) | ≤ 300 KB marketing; ≤ 600 KB WebGL hero | bundlesize in CI |
| Server bundle (Nitro) | ≤ 50 MB cold-start (host-dependent) | `nuxi build` size report gate |

Budget enforcement details deferred to `performance-budget-author`
(PR #7); the user-invocable `draft-perf-budget` covers it now.

### CMS — Storyblok or Sanity

- **Storyblok** is the default for visual-edit-heavy projects (the
  visual editor is Vue-first and a major brand-design selling point);
  use `@storyblok/nuxt` module.
- **Sanity** is preferred for content-typing-heavy projects with
  GROQ-driven queries; use `@nuxtjs/sanity` module.
- **Webhook-driven revalidation** via Nitro `routeRules`
  (`isr: 60` with on-demand purge) or via the host's revalidation API
  (Vercel / Netlify / Cloudflare).
- **CMS query budget**: ≤ 5 queries per page; ≤ 200 KB cumulative
  response weight.

### Hosting via Nitro presets

- **Nitro preset** chosen at build via `NITRO_PRESET` env var or
  `nitro.preset` in `nuxt.config.ts`.
- **Vercel / Netlify** are the most-tested presets; **Cloudflare
  Workers** is rising for static-heavy sites; **Node** for self-hosted.
- The runbook in `house-site-operate-nuxt` covers the preset-specific
  deploy verbs.

### Analytics + email

- Same defaults as Combo A: **Plausible / Fathom / PostHog** for
  analytics; **Resend + Loops** for email; HubSpot only when
  client-required.

### ADR catalog (the seven Combo-B ADRs)

1. **Nitro preset selection** — host + serverless model rationale.
2. **CMS selection** — Storyblok vs Sanity vs Strapi (anti-pattern)
   with the visual-edit / type-safety tradeoff named.
3. **3D library selection** — TresJS (Vue-native wrapper) vs raw
   Three.js + Vue components vs an iframe/island for R3F.
4. **Auto-import scope boundary** — what's auto-imported, what's not;
   linter rules.
5. **Server-route vs external-API split** — first-party vs third-party.
6. **Image optimization origin** — `<NuxtImg>` + chosen provider
   vs Cloudinary vs Imgix.
7. **State hydration strategy** — Pinia stores SSR-rehydrated vs
   client-only.

`adr-author` produces each one when invoked.

## Override Behavior

This overlay applies when:

- The project's `srs-author` output cites the Combo B stack.
- The mechanism atoms (`srs-author`, `adr-author`, `master-schedule-
  author`, `runbook-author`, `threat-model-author`) are installed at
  v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.
Per `ARCHITECTURE.md` §"Mechanism vs Policy", silent substitution is
forbidden.

If the project's stack diverges from Combo B, the operator either
switches to a different stack overlay or documents the divergence in
an ADR.

The runbook deploy verbs (`nuxi build`, host CLI) are
**non-overridable**; mixing runbook conventions across hosts is a
bug.

Cross-cutting concerns (perf budget, motion conformance, analytics
spec, error monitoring, release discipline) defer to dedicated atoms
per A62 anti-trigger fallback:

- Performance-budget enforcement — use `performance-budget-author`;
   the user-invocable `draft-perf-budget` covers it now.
- Motion-a11y conformance — use `motion-conformance-author` once
  built; the user-invocable `draft-motion-conformance` covers it now.
- Analytics event taxonomy — use `analytics-instrumentation-author`;
   the user-invocable `draft-analytics-spec` covers it now.

## See Also

- `house-site-design-nuxt` — design-system + motion conventions for
  Combo B.
- `house-site-operate-nuxt` — launch + observability conventions for
  Combo B.
- `house-site-operate-vercel` / `house-site-operate-netlify` /
  `house-site-operate-cloudflare` — host-specific overlays for the
  Nitro preset chosen.
- `docs/research/E3-technical-conventions.md` §5 (Combo B), §2
  (motion), §6 (tooling).
