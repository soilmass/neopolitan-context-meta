---
name: house-site-build-nextjs
description: >
  House conventions for the site-build family on a Next.js + Vercel +
  Sanity stack (Combo A "React-cinematic"). Overlays srs-author,
  adr-author, master-schedule-author, runbook-author, and threat-model-
  author with stack-specific NFRs, ADR templates, sprint cadence, deploy
  verbs, and threat surfaces. Do NOT use for: design-system / motion /
  component conventions on Next.js (use house-site-design-nextjs);
  hosting + launch + observability conventions on Vercel (use
  house-site-operate-nextjs or house-site-operate-vercel); generic
  Next.js coding rules outside the site-build SOP (out of scope —
  encode in your linter / CI config); composing this overlay with a
  per-team overlay (deferred per ARCHITECTURE.md "Policy overlay
  composition" until 2+ tiers exist).
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
            Cross-references performance-budget-author and
            motion-conformance-author via A62 anti-trigger
            fallback (those atoms ship in PR #7 / v0.6.0).
---

# house-site-build-nextjs

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay applying Combo A ("React-cinematic" — Next.js App Router
+ Vercel + Sanity + R3F + GSAP) conventions to the five mechanism
atoms in the `site-build` family that are most stack-sensitive.

## Purpose

Encode the conventions that turn the family's stack-neutral
mechanism atoms into Combo-A-shaped artifacts:

1. SRS NFRs cite Vercel's runtime constraints (Edge Function
   limits, ISR cadence, Streaming SSR), Next.js's bundle budgets,
   and Sanity's GROQ query patterns.
2. ADR templates name Combo-A-typical decision points (RSC vs
   client component, Edge vs Serverless, ISR cadence per page
   type, Sanity dataset strategy).
3. Master schedule cadence reflects the deploy-preview-per-PR
   tempo Vercel affords (no separate "QA on staging" tier).
4. Runbook deploy verbs use `vercel`, `next`, `sanity` CLIs.
5. Threat model attends to Sanity API exposure, RSC data leakage,
   and Vercel environment variable scoping.

## Applies On Top Of

- `srs-author` — adds Combo-A NFR rows + Next.js bundle budget
  table + Sanity query budget.
- `adr-author` — adds Combo-A decision-point catalog (the eight
  ADRs every Combo-A project should write).
- `master-schedule-author` — adopts the deploy-preview-per-PR
  cadence; sprint structure stays mechanism-driven.
- `runbook-author` — replaces generic deploy verbs with
  `vercel deploy`, `vercel rollback`, `next build`, `sanity deploy`.
- `threat-model-author` — adds Combo-A-specific threat surfaces
  (RSC data exposure, API route enumeration, Sanity webhook
  authentication, Vercel env var scoping).

If any of these mechanism atoms is uninstalled, this overlay
fails loudly; see `## Override Behavior`.

## Conventions Enforced

### Frontend

- **App Router only.** Pages Router is legacy; new Combo-A
  projects use App Router with React Server Components by
  default. Client components opt in via `"use client"` and
  must justify the boundary in their ADR.
- **TypeScript strict.** `strict: true`, `noUncheckedIndexedAccess:
  true`, `exactOptionalPropertyTypes: true` in `tsconfig.json`.
- **Server-first data fetching.** `fetch()` with Next's caching
  semantics in RSCs; client-side data fetching only for
  user-interactive flows (forms, optimistic updates).
- **No `getStaticProps` / `getServerSideProps`.** App Router only.
- **Streaming SSR via Suspense boundaries** for long-running
  RSC subtrees.

### Bundle budgets (citing E3 §1.3)

| Resource | Target | Enforcement |
|---|---|---|
| Critical-path JS (gz) | ≤ 130–170 KB marketing; ≤ 200 KB WebGL hero (excl. three.js core) | `@next/bundle-analyzer` + `size-limit` in CI |
| Total JS (gz) | ≤ 300 KB marketing; ≤ 600 KB WebGL hero | `bundlesize` in CI |
| First Load JS | ≤ 100 KB on the homepage route | `next build` output gates |

Budget enforcement details deferred to `performance-budget-author`
(PR #7); the user-invocable `draft-perf-budget` covers it now.

### CMS — Sanity

- **GROQ-only queries** for content. No GraphQL.
- **Studio embedded in repo** at `/studio` route (Sanity v3+
  default).
- **Sanity preview** uses Next.js `draftMode()` cookie.
- **Webhook-driven revalidation** via `revalidateTag()` /
  `revalidatePath()` (no time-based ISR for content unless
  justified in an ADR).
- **GROQ query budget**: ≤ 5 queries per page; ≤ 200 KB cumulative
  response weight.

### Hosting + assets

- **Vercel deployment** is assumed; if the project ships elsewhere,
  invoke `house-site-operate-{cloudflare,netlify}` instead and the
  runbook conventions here become advisory.
- **Vercel Blob** for self-hosted assets; **Cloudinary** when DAM
  features (transforms, derived assets, marketing self-service)
  matter.
- **Mux** for any non-trivial video; HLS over MP4 for everything
  longer than 15 s.
- **Resend** for transactional email; **Loops** for marketing
  sequences. (HubSpot only when client requires.)

### Analytics

- **Plausible** or **Fathom** for marketing analytics (privacy-
  posture default). **PostHog** when product analytics or
  experiments needed.
- **Vercel Web Analytics** + **Speed Insights** are enabled but
  treated as field-RUM signals, not the analytics source of truth.
- GA4 is **not** the default; explicit ADR required if a project
  chooses GA4.

### ADR catalog (the eight Combo-A ADRs)

Every Combo-A project writes ADRs for these decisions:

1. **RSC vs client component boundary** — where the line is and
   why.
2. **Edge vs Serverless function selection rule** — per-route
   defaults.
3. **ISR cadence per page type** — stale-while-revalidate vs
   revalidate-on-demand.
4. **Sanity dataset strategy** — single dataset vs production /
   staging split.
5. **Image optimization origin** — `next/image` + Vercel vs
   Cloudinary vs Imgix.
6. **Email stack selection** — Resend + Loops vs alternative,
   with deliverability evidence.
7. **Analytics privacy posture** — Plausible / Fathom / PostHog /
   GA4 with the rationale.
8. **Auth boundary** — server-side session vs client-side; cookie
   strategy.

`adr-author` produces each one when invoked; this overlay names
the *expected* set so the project doesn't ship without writing
them.

## Override Behavior

This overlay applies only when:

- The project's `srs-author` output explicitly cites the Combo-A
  stack.
- The mechanism atoms (`srs-author`, `adr-author`, `master-
  schedule-author`, `runbook-author`, `threat-model-author`) are
  installed and at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails
loudly** — invocation raises an error pointing at the missing
atom and refusing to substitute. Per `ARCHITECTURE.md` §"Mechanism
vs Policy", silent substitution is forbidden.

If the project's stack diverges from Combo A (e.g., the operator
discovers mid-Phase-2 they need Nuxt instead), the operator
either:

1. Switches to `house-site-build-nuxt` and re-runs the affected
   atoms, OR
2. Documents the divergence in an ADR and the overlay's
   conventions become advisory rather than enforced.

The runbook deploy verbs (`vercel deploy` etc.) are the only
section that is **non-overridable** — if you're not on Vercel,
you should be using a different operate-* overlay; mixing
runbook conventions across hosts is a bug.

Cross-cutting concerns (perf budget, motion conformance) defer
to dedicated atoms per A62 anti-trigger fallback:

- Performance-budget enforcement (CI gating, per-page-type
  budgets) — use `performance-budget-author`; the
  user-invocable `draft-perf-budget` covers it now.
- Motion-a11y conformance (WCAG 2.2 motion criteria) — use
  `motion-conformance-author`; the user-invocable
  `draft-motion-conformance` covers it now.
- Analytics event taxonomy (verb_noun naming, schema validation) —
  use `analytics-instrumentation-author`; the user-
  invocable `draft-analytics-spec` covers it now.

## See Also

- `house-site-design-nextjs` — design-system + motion conventions
  for the same stack.
- `house-site-operate-nextjs` — launch + observability
  conventions for the same stack.
- `house-site-operate-vercel` — hosting-platform conventions
  (cited from this overlay's runbook section).
- `docs/research/E3-technical-conventions.md` §1, §2.4, §5
  (Combo A) — evidence base.
