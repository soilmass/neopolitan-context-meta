---
name: house-site-build-sveltekit
description: >
  House conventions for the site-build family on a SvelteKit + Vite
  + Tailwind + adapter-driven hosting stack (Combo D
  "Svelte/SvelteKit, performance-pure" — the Igloo Inc combo).
  Overlays srs-author, adr-author, master-schedule-author, runbook-
  author, and threat-model-author with SvelteKit-specific NFRs (the
  performance-pure brand-promise budgets), adapter selection rules,
  load-function discipline, form-actions-over-fetch, deploy verbs,
  and threat surfaces. Do NOT use for: design-system / motion
  conventions on SvelteKit (use house-site-design-sveltekit); launch /
  observability conventions on SvelteKit hosts (use
  house-site-operate-sveltekit or host-specific overlay); composing
  this overlay with a per-team overlay (deferred per ARCHITECTURE.md).
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

# house-site-build-sveltekit

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay applying Combo D ("Svelte/SvelteKit, performance-pure"
— the Igloo Inc Site of the Year 2024 combo) conventions to the
site-build family.

## Purpose

Encode the conventions that make the performance-pure brand-promise
honest:

1. SRS NFRs lock JS budget tighter than Combo A — Igloo Inc's
   Site of the Year 2024 demonstrates SvelteKit + vanilla Three.js can
   ship a hero-WebGL site under aggressive payload constraints.
2. ADR templates name Combo-D-typical decision points (adapter, CMS,
   load-function vs server endpoint, progressive enhancement
   strategy, 3D library — vanilla vs Svelte-Cubed).
3. Master schedule reflects Svelte's compiler-driven model and
   form-actions-over-fetch tempo.
4. Runbook deploy verbs use the chosen adapter's commands; host
   overlays cover host specifics.
5. Threat model attends to load-function authentication, server
   endpoint enumeration, form-action CSRF defaults.

## Applies On Top Of

- `srs-author` — adds Combo-D NFR rows + tighter SvelteKit bundle
  budget table; CMS query budget.
- `adr-author` — adds Combo-D decision-point catalog (5 ADRs).
- `master-schedule-author` — adopts the deploy-preview-per-PR cadence;
  sprint structure mechanism-driven.
- `runbook-author` — replaces generic deploy verbs with `vite build`
  + adapter-specific deploy.
- `threat-model-author` — adds Combo-D-specific threat surfaces.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Frontend

- **SvelteKit 2+** with TypeScript strict mode.
- **Adapter chosen at build**: `@sveltejs/adapter-{vercel,netlify,
  cloudflare,node,static}`.
- **Form actions** over `fetch()` for first-party data mutations
  (progressive enhancement default; works with JS disabled).
- **Load functions** (`+page.ts`, `+page.server.ts`,
  `+layout.server.ts`) for data preload; client-side fetching only
  for user-driven flows.
- **Stores** (`writable`, `readable`, `derived`) for client state;
  context API for component-tree-scoped state.
- **Progressive enhancement first**: every interactive element
  works without JS unless explicitly opted out in the SRS.

### Bundle budgets (citing E3 §5 Combo D — Igloo Inc baseline)

| Resource | Target | Enforcement |
|---|---|---|
| Critical-path JS (gz) | ≤ 80 KB marketing; ≤ 150 KB WebGL hero (excl. Three.js core) | size-limit + custom Vite plugin |
| Total JS (gz) | ≤ 200 KB marketing; ≤ 500 KB WebGL hero | bundlesize CI |
| LCP target | ≤ 1.8s p75 mobile (matches Astro's tighter set) | Lighthouse CI |
| INP target | ≤ 200ms p75 (the Achilles heel of WebGL sites — strict here) | Lighthouse CI + field RUM |

Budget enforcement details deferred to `performance-budget-author`
(PR #7); the user-invocable `draft-perf-budget` covers it now.

### CMS

- **Sanity** is the default (mature ecosystem, GROQ queries
  cleanly composed in load functions).
- **Hygraph** for projects that want a tighter type-generation story
  (Hygraph generates TypeScript types from the schema).
- **Storyblok** when visual edit matters (less Svelte-native than for
  Vue, but a Svelte SDK exists).
- **Webhook-driven revalidation** via SvelteKit's `+server.ts`
  endpoint receiving the webhook → cache invalidation.

### 3D library convention (citing Igloo Inc precedent)

- **vanilla Three.js** is the default; Svelte-Cubed is less mature
  than R3F or TresJS.
- Three.js wrapped in a Svelte component with explicit lifecycle
  hooks (`onMount` / `onDestroy`) for renderer init / dispose.
- For projects requiring R3F-equivalent ergonomics, considered a
  bridge: an iframe-island carrying a React subtree (rare; usually
  not worth the boundary).

### Hosting via adapters

- **Adapter selection** documented in the build-overlay's ADR.
- **Vercel / Netlify / Cloudflare Pages / Node** are first-class.
- **Static** adapter when fully prerenderable (rare for Combo D since
  it's typically chosen for app-shaped projects).

### ADR catalog (the five Combo-D ADRs)

1. **Adapter selection** — Vercel / Netlify / Cloudflare / Node /
   static; rationale.
2. **CMS selection** — Sanity / Hygraph / Storyblok / none.
3. **Load-function vs `+server.ts` split** — what's data-load, what's
   API endpoint.
4. **Progressive enhancement strategy** — which features have JS-off
   fallbacks; what's documented as JS-required.
5. **3D library** — vanilla Three.js / Svelte-Cubed / iframe-island
   bridge.

`adr-author` produces each one when invoked.

## Override Behavior

This overlay applies when:

- The project's `srs-author` output cites Combo D.
- The mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.
Per `ARCHITECTURE.md` §"Mechanism vs Policy", silent substitution is
forbidden.

If the project diverges from the performance-pure brand promise (e.g.,
ships large CMS-driven content with relaxed budgets), the SRS NFRs
relax toward Combo A levels and the divergence is documented in an
ADR.

The runbook deploy verbs are deferred to the chosen adapter's host
overlay; mixing host conventions is a bug.

Cross-cutting concerns (perf budget, motion conformance, analytics
spec, error monitoring, release discipline) defer to dedicated atoms
per A62 anti-trigger fallback. See `house-site-build-nextjs` for the
canonical list.

## See Also

- `house-site-design-sveltekit` — design-system + motion conventions
  for Combo D.
- `house-site-operate-sveltekit` — launch + observability conventions
  for Combo D.
- `house-site-operate-{vercel,netlify,cloudflare}` — host-specific
  overlays for the chosen adapter.
- `docs/research/E3-technical-conventions.md` §5 (Combo D, Igloo Inc),
  §1 (perf budgets), §2 (motion).
