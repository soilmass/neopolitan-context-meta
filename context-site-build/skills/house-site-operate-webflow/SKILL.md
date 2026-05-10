---
name: house-site-operate-webflow
description: >
  House conventions for the site-operate family on the Webflow stack
  (Webflow hosting + Backups + Webflow Analytics or Plausible).
  Overlays runbook-author, launch-comms-author, optimization-loop-
  author, optimization-backlog-author, and conformance-statement-
  author with Webflow's two-environment publish model, Backups-based
  rollback, Webflow Analytics + axe DevTools manual audits (no
  Webflow-native a11y CI), and the platform-bounded optimization
  surface. Do NOT use for: SRS / ADR / threat-model on Webflow (use
  house-site-build-webflow); design-system / motion conventions on
  Webflow (use house-site-design-webflow); composing this overlay
  with a per-team overlay (deferred per ARCHITECTURE.md).
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

# house-site-operate-webflow

> **pre-trigger build (v0.5.0)**; reassess when ≥2 tiers of
> `house-*` overlays exist on the same mechanism atom per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 4.

Stack overlay encoding launch + post-launch operational conventions
on the Webflow platform.

This overlay applies on top of the family's mechanism atoms
with stack-specific or hosting-platform conventions. Composing
with a per-team overlay, or replacing it with a different family
overlay independent of this one, is deferred per ARCHITECTURE.md.
The site-operate family's threat-model and design coverage live
in their own overlays.

## Purpose

Encode how runbook, launch comms, optimization loops, and a11y
conformance ride on Webflow's bundled hosting + CMS + Backups
model:

1. Runbook deploy verbs use Webflow's Publish flow + the
   Designer/Published two-environment model. There is no preview-
   per-PR — the only previewable state is the Designer.
2. Rollback uses Backups + the manual restore flow; rollback target
   is platform-dependent (typically <2 min).
3. Optimization loops are platform-bounded — Webflow's hosting,
   CDN, and image optimization are bundled. The optimization
   surface for the project is largely custom-code embeds + image
   weight + CMS query patterns.
4. Conformance statements ride manual axe DevTools audits + the
   four platform-gap component states from
   `house-site-design-webflow`. There is no Webflow-native a11y CI.
5. Launch comms use BetterStack / Statuspage for status pages
   (Webflow doesn't provide a status-page integration).

## Applies On Top Of

- `runbook-author` — replaces generic deploy verbs with Webflow's
  Publish + Backups model.
- `launch-comms-author` — adds external status-page wiring (no native
  integration); CDN-incident copy templates.
- `optimization-loop-author` — names the Webflow-bounded loop
  (custom-code embeds, image weight, CMS query patterns).
- `optimization-backlog-author` — backlog row schema reflects
  Webflow's optimization surface.
- `conformance-statement-author` — adds the four platform-gap states
  + manual axe DevTools workflow.

If any of these mechanism atoms is uninstalled, this overlay fails
loudly; see `## Override Behavior`.

## Conventions Enforced

### Webflow deploy flow

| Operation | Mechanism |
|---|---|
| Edit / preview | Designer (sole preview environment) |
| Publish to staging | Publish to `<sitename>.webflow.io` (Webflow's preview-style URL) |
| Publish to production | Publish to custom domain |
| Rollback | Backups → Restore (manual flow in Designer) |
| Schema change | New collection-version (immutable; collections cannot migrate) |
| Custom code change | Designer → Custom Code → Publish |

- **No preview-per-PR** — Webflow doesn't have a Git-aware preview
  branching model. The Designer staging environment is the only
  pre-production preview.
- **Production publish gate**: Editor approval (when client team
  uses Editor) OR Designer publish (when agency-led).
- **Rollback target ≤ 2 min** via Backups Restore.

### Two-environment model

- **Designer** — the live editing surface. Pre-publish state lives
  here.
- **Published** — the customer-facing surface. Backed by Webflow's
  CDN.
- **Custom domain** — the production publish target; staging URL
  remains accessible at `<sitename>.webflow.io` until disabled.

### Optimization surface (platform-bounded)

The runtime is opaque (Webflow controls hosting + CDN + image
optimization). Optimization surfaces:

- **Custom-code embed weight** — every embed budgeted; review
  monthly for opportunities to remove or consolidate.
- **Image weight** — Webflow's auto-optimization is good but not
  perfect; manual review for above-fold images.
- **CMS query patterns** — N+1 queries via reference fields are the
  most common platform-side issue.
- **Custom Logic flow latency** — Logic flows have a per-step
  latency budget; complex flows surface as p95 issues.

### Observability stack

- **Webflow Analytics** is bundled — basic page-view + referrer
  data; sufficient for vanity metrics.
- **Plausible / Fathom** for marketing analytics with privacy
  posture; loaded via custom-code embed.
- **Sentry** for custom-code error monitoring (when GSAP / Three.js
  custom code is in use); loaded via `<head>` embed.
- **No backend instrumentation surface** — Logic flows aren't
  externally instrumentable; rely on Logic's own logs.

### a11y CI gap

- **No Webflow-native a11y CI**. The conformance-statement should
  document this gap explicitly.
- **Manual axe DevTools audits** monthly; pre-publish for major
  releases.
- **Lighthouse browser audits** monthly via Chrome DevTools.
- **Honest disclaimer**: automated tools catch ~30–40% of WCAG 2.2
  barriers; manual keyboard + screen-reader testing covers the rest.
  Webflow's lack of CI integration shifts more burden to manual
  audits.

### Status page + launch comms

- **External status page** (BetterStack / Statuspage / Cachet) — no
  Webflow-native integration.
- **Launch-day comms** templates same as code-first combos.
- **Post-launch hypercare** SLA: 30-minute response window for the
  first 72 hours; alerting via custom-code-embedded Sentry.

### Release discipline

- **No native feature flags** — typically not needed for marketing-
  site Webflow projects (the platform doesn't lend itself to A/B
  testing complex flows). When needed, use a custom-code embed of
  PostHog Feature Flags or LaunchDarkly Web SDK.
- **Rollback automation** is manual via Backups (no API for
  programmatic restore in 2025).
- **Go/no-go checklist** deferred to `release-discipline-author`
  (PR #7); the user-invocable `draft-release-plan` covers it now.

## Override Behavior

This overlay applies when:

- The project ships on Webflow.
- All five mechanism atoms are installed at v0.1.0+.

If any mechanism atom is uninstalled, this overlay **fails loudly**.

The "no preview-per-PR" reality is **non-overridable**: any project
that requires Git-driven preview branches should not be using
Webflow.

Cross-cutting concerns defer to dedicated atoms per A62 anti-trigger
fallback. The Webflow context simplifies several:

- Performance budgets — platform-bounded; the
  `performance-budget-author` atom (PR #7) operates on custom-code
  embeds + image weight only.
- Error monitoring — Webflow doesn't expose backend errors; the
  `error-monitoring-setup-author` atom (PR #7) operates on
  custom-code-embedded Sentry only.

## See Also

- `house-site-build-webflow` — SRS / ADR / schedule / runbook /
  threat-model conventions for Webflow.
- `house-site-design-webflow` — design-system + motion conventions
  for Webflow.
- `docs/research/E3-technical-conventions.md` §4 (a11y reality;
  Webflow's lack of native a11y CI is part of the broader gap),
  §5 (combo notes — Webflow not deeply analyzed in Awwwards-tier
  corpus).
