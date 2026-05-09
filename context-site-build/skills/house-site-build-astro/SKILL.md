---
name: house-site-build-astro
description: >
  House conventions for the site-build family on an Astro + Vite +
  Tailwind + island-hydration stack (Combo C "Astro-static-with-WebGL-
  islands"). Overlays srs-author, adr-author, master-schedule-author,
  runbook-author, and threat-model-author with Astro-specific NFRs
  (static-by-default; >50% CWV pass rate per Web Almanac), island
  hydration discipline, content-collections-driven type safety,
  deploy verbs, and threat surfaces. Do NOT use for: design-system /
  motion conventions on Astro (use house-site-design-astro); launch /
  observability conventions on Astro hosts (use
  house-site-operate-astro or host-specific overlay); composing this
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

# house-site-build-astro

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay applying Combo C ("Astro-static-with-WebGL-islands"
— Astro + Vite + Tailwind + selective React/Vue/Svelte islands)
conventions to the site-build family.

## Purpose

Encode the conventions that make Combo C honest:

1. SRS NFRs cite Astro's static-by-default model and the **>50% CWV
   pass rate** Astro achieves (Web Almanac 2023 — only major framework
   to clear it). Performance budgets are tighter than Combo A because
   the static-first model affords it.
2. ADR templates name Combo-C-typical decision points (island vs
   static, framework selection per island, content-collections schema,
   CMS yes/no).
3. Master schedule cadence reflects the static-build tempo (no
   server cold-starts; long deploy times traded for tiny runtime).
4. Runbook deploy verbs use `astro` CLI + the chosen host's CLI; the
   host overlay (`house-site-operate-{vercel,netlify,cloudflare}`)
   handles host-specific operations.
5. Threat model attends to build-time CMS API exposure, island
   framework supply chain, and SSR-adapter security (when SSR mode
   is selected).

## Applies On Top Of

- `srs-author` — adds Combo-C NFR rows + tighter Astro bundle budget
  table + island-hydration budget per page.
- `adr-author` — adds Combo-C decision-point catalog (5 ADRs).
- `master-schedule-author` — adopts the static-build cadence; trades
  long build times for tiny runtime.
- `runbook-author` — replaces generic deploy verbs with `astro build`,
  `astro preview`, host CLI.
- `threat-model-author` — adds Combo-C-specific threat surfaces.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Frontend

- **Astro 4+** with TypeScript; `tsconfig.json` extends `astro/tsconfigs/strict`.
- **Static-by-default**; SSR adapters only when justified in an ADR
  (e.g., authenticated pages, dynamic API routes).
- **Islands architecture**: React / Vue / Svelte / SolidJS islands
  hydrated only where interactivity is needed.
  - **Hydration directives** (`client:load`, `client:idle`,
    `client:visible`, `client:media`, `client:only`) chosen
    intentionally per island.
  - Default to `client:visible` for below-fold islands;
    `client:idle` for above-fold non-critical; `client:load` only
    for above-fold critical interactivity.
- **Content collections** (`src/content/`) with Zod-validated
  schemas; `content.config.ts` is the source of truth for content
  types.
- **Markdown / MDX** for content-driven pages; component-driven for
  app-shaped pages.

### Bundle budgets (citing E3 §1.3 — tighter than Combo A)

| Resource | Target | Enforcement |
|---|---|---|
| Critical-path JS (gz) | ≤ 80 KB marketing; ≤ 150 KB with hero island | `astro build` size report + size-limit |
| Total JS (gz) | ≤ 150 KB marketing; ≤ 300 KB with islands | bundlesize CI |
| Above-fold image weight | ≤ 300 KB | astro:assets compression report |
| Total page weight | ≤ 1 MB marketing; ≤ 2 MB with hero island | Lighthouse CI gate |

The tighter budgets reflect Astro's static-first model — there is no
server cold-start tax, so the JS budget can be aggressive. Budget
enforcement details deferred to `performance-budget-author` (PR #7);
the user-invocable `draft-perf-budget` covers it now.

### Content + CMS

- **Content collections** for in-repo content; Zod schemas validated
  at build.
- **Sanity** when CMS-driven (use `@astrojs/sanity` or GROQ via
  `@sanity/client`).
- **Storyblok** when visual-edit matters (use `@storyblok/astro`).
- **Strapi / Contentful** discouraged for marketing sites — friction
  too high for Astro's tempo.

### Hosting

- **Vercel / Netlify / Cloudflare Pages** are first-class via official
  Astro adapters.
- **Cloudflare Pages** is rising fast in 2025 for static + Workers
  deployments.
- The runbook in `house-site-operate-astro` covers preset-agnostic
  conventions; host-specific verbs defer to
  `house-site-operate-{vercel,netlify,cloudflare}`.

### ADR catalog (the five Combo-C ADRs)

1. **Static vs SSR mode** — which pages are which; SSR justification.
2. **Island framework selection** — React / Vue / Svelte / SolidJS
   per island; mixing rationale.
3. **Hydration strategy** — `client:*` directives per island class;
   the policy doc.
4. **Content-collections schema** — what types, what fields, what
   indexed.
5. **CMS yes/no** — content-collections-only vs Sanity / Storyblok
   integration.

`adr-author` produces each one when invoked.

## Override Behavior

This overlay applies when:

- The project's `srs-author` output cites Combo C.
- The mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.
Per `ARCHITECTURE.md` §"Mechanism vs Policy", silent substitution is
forbidden.

If the project moves to SSR-mode-heavy use, the static-by-default
discipline and the tighter bundle budgets become advisory; the
operator documents the divergence in an ADR.

The runbook deploy verbs are deferred to the host overlay; mixing
`astro build` with non-Astro deploy patterns is a bug.

Cross-cutting concerns (perf budget, motion conformance, analytics
spec, error monitoring, release discipline) defer to dedicated atoms
per A62 anti-trigger fallback. See `house-site-build-nextjs` for the
canonical fallback list (same atoms apply across stacks).

## See Also

- `house-site-design-astro` — design-system + motion conventions for
  Combo C.
- `house-site-operate-astro` — launch + observability conventions for
  Combo C.
- `house-site-operate-{vercel,netlify,cloudflare}` — host-specific
  overlays.
- `docs/research/E3-technical-conventions.md` §5 (Combo C), §1
  (perf budgets), §2 (motion).
