---
name: house-site-build-webflow
description: >
  House conventions for the site-build family on a Webflow Designer
  + CMS + Logic stack (visual-editor / no-code combo). Overlays
  srs-author, adr-author, master-schedule-author, runbook-author, and
  threat-model-author with Webflow-specific NFRs (platform ceiling
  shapes feasibility differently from code-first stacks), Component
  conventions, custom-code embed boundaries, Workspace structure, and
  threat surfaces (CMS API exposure, custom-code XSS, Memberships
  auth scope). Do NOT use for: design-system / motion conventions on
  Webflow (use house-site-design-webflow); launch / observability
  conventions on Webflow's platform (use house-site-operate-webflow);
  composing this overlay with a per-team overlay (deferred per
  ARCHITECTURE.md).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: policy
  tags: [composition, stack-overlay]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.5.0 Phase 4 stack-
            overlay batch (Webflow × 3). Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 4; user
            explicitly approved maximalist scope on 2026-05-08.
---

# house-site-build-webflow

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay applying Webflow (visual-editor / no-code with
escape hatches) conventions to the site-build family.

## Purpose

Webflow's brand promise is "design-led marketing site speed without
engineering glue." The platform ceiling shapes what's feasible
differently from code-first stacks. This overlay encodes:

1. SRS NFRs cite the **Webflow platform ceiling**: hosting bundled,
   CDN bundled, no SSR-arbitrary-code, custom code limited to
   embeds, Logic for low-code workflows. The SRS gets a "what NOT
   to do in Webflow" section because the ceiling is load-bearing.
2. ADR templates name Webflow-specific decision points (Components
   strategy, Memberships yes/no, Logic vs external integration,
   custom-code embed boundary).
3. Master schedule reflects Webflow's two-environment model
   (Designer + Published) and the "no preview branches" reality.
4. Runbook deploy verbs describe Webflow's publish flow + Backups-
   based rollback.
5. Threat model attends to CMS API exposure, custom-code XSS in
   embeds, Memberships scope creep.

## Applies On Top Of

- `srs-author` — adds "Webflow Platform Ceiling" section + NFR rows
  reflecting the platform's constraints.
- `adr-author` — adds Webflow-specific decision-point catalog (5 ADRs).
- `master-schedule-author` — adopts the two-environment cadence
  (Designer + Published; no separate staging tier).
- `runbook-author` — replaces generic deploy verbs with Webflow's
  Publish + Backups model.
- `threat-model-author` — adds Webflow-specific threat surfaces.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Platform ceiling (the load-bearing section)

- **Hosting + CDN** are bundled — no separate hosting decision.
- **Server-side code** is not available; Logic provides low-code
  workflows (webhooks, conditional branches, integrations).
- **Custom code** is restricted to:
  - `<head>` injection (site-wide or per-page)
  - Pre-`</body>` injection
  - HTML embed elements (≤ 50 KB per page total)
- **Webflow Apps** are the supported plugin model for capabilities
  beyond core (CMS extension, payments, integrations).
- **No build pipeline** — the platform compiles styles + JS at
  publish time.
- **No version control** in the engineering sense — Webflow Backups
  + a manual "freeze" workflow (export + Git) for the export-driven
  edge cases.

### What NOT to do in Webflow

The SRS gets an explicit anti-pattern section:

- ❌ Build a backend in Webflow Logic that should live in a serverless
  function elsewhere (Logic is for orchestration, not business logic).
- ❌ Use Webflow CMS for content models with > 10K items (the editor
  performance + collection limit makes this painful).
- ❌ Build a JavaScript SPA inside a `<embed>` (the platform isn't
  designed for it).
- ❌ Use Memberships for general auth (scope creep — limited to gating
  marketing content; do not use for product auth).
- ❌ Hand-edit the exported code (the export is a one-way export; you
  cannot re-import).

### Frontend conventions

- **Webflow Components** for repeated UI; component variants for
  state.
- **Style guide page** rendered as the live design system (the
  `style-guide` URL convention).
- **Class naming**: BEM-flavored (`block__element--modifier`) using
  Webflow's combo classes; or utility-style (Webflow CSS Variables +
  Client-First convention).
- **Custom code embed boundary**: only for capabilities Webflow lacks
  (advanced motion via GSAP, Three.js hero, third-party scripts);
  every embed gets an inline comment naming why it's not native.

### CMS conventions

- **Webflow CMS** for content with up to ~10K items per collection.
- **Schema versioning**: collection-name-`-v2` suffix when the schema
  needs a breaking change (no migrations; collections are immutable
  once items exist).
- **Reference fields** preferred over self-rolled relations.
- **CMS API** for external integrations (read-only by default; write
  operations gated by API key with scoped permissions).

### ADR catalog (the five Webflow ADRs)

1. **Components strategy** — how components are organized + naming.
2. **Memberships yes/no** — gating model + auth scope.
3. **Logic vs external integration** — what stays in Logic, what
   exits to a serverless function.
4. **Custom-code embed boundary** — what gets a `<head>` script,
   what gets an HTML embed, what gets a Webflow App.
5. **Export workflow** — when (and whether) to export + the
   maintenance contract.

`adr-author` produces each one when invoked.

### Workspace structure

- **One Workspace per client** (or per agency-client engagement).
- **Site-name convention**: `<client>-<purpose>-<year>` (e.g.,
  `acme-marketing-2026`).
- **Designer access** scoped to engineering + design; **Editor**
  access scoped to client content team.
- **Backups**: weekly snapshot + per-publish; retention 90 days.

## Override Behavior

This overlay applies when:

- The project ships on Webflow.
- The mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

The "What NOT to do in Webflow" section is **non-overridable**: if
a project insists on these anti-patterns, it should not be using
Webflow.

If the project starts on Webflow but discovers mid-build that its
needs exceed the platform ceiling (e.g., needs SSR-arbitrary-code),
the operator either accepts a separate code-first project for those
needs (hybrid) or migrates the whole site to a code-first stack
(Combos A/B/C/D) and switches stack overlays.

Cross-cutting concerns (perf budget, motion conformance, analytics
spec, error monitoring, release discipline) defer to dedicated atoms
per A62 anti-trigger fallback. The Webflow context simplifies several
(perf is platform-bounded, error monitoring is Webflow-bundled), but
the atoms still apply where the project escapes the ceiling via
custom code.

## See Also

- `house-site-design-webflow` — design-system + motion conventions
  for Webflow.
- `house-site-operate-webflow` — launch + observability conventions
  for Webflow.
- `docs/research/E3-technical-conventions.md` §5 (combo notes for
  CMS distribution; Webflow noted but not deeply analyzed in
  Awwwards-tier corpus, since Webflow + Awwwards-SOTD overlap is
  thin).
