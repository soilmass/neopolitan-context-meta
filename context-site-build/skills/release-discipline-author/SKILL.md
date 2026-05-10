---
name: release-discipline-author
description: >
  Authors the release-discipline specification + the per-release
  go/no-go checklist + feature-flag tool selection ADR. Writes
  docs/release-plan.md plus deploy/feature-flags.yml. Codifies
  feature-flag tool choice (LaunchDarkly / Statsig / PostHog /
  Vercel Edge Config / Cloudflare KV); canary + blue-green strategy;
  rollback automation thresholds tied to the SLI definitions in
  observability-spec; release-marker wiring; release-day comms
  cadence. Free-standing atom outside any family. Do NOT use for:
  per-incident response runbook (use runbook-author with kind=
  incident); the SLI definitions themselves (use
  error-monitoring-setup-author); launch-day external comms (use
  launch-comms-author — release-discipline is operational, launch-
  comms is communications); per-host deploy / rollback verbs
  (those go in house-site-operate-{vercel,cloudflare,netlify}).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [cross-cutting, release]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.6.0 Phase 5 cross-
            cutting-tools batch. Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 5; user
            explicitly approved maximalist scope on 2026-05-08.
---

# release-discipline-author

> **pre-trigger build (v0.6.0)**; reassess when first consumer
> needs codified release discipline + canary strategy per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 5.

Free-standing atom that produces the release-discipline specification
covering feature flags, canary strategy, rollback automation, and the
go/no-go checklist. Outputs: `docs/release-plan.md` and
`deploy/feature-flags.yml`. Codifies the operational launch ceremonies
including per-release communication threads. The atom names the
feature-flag tool choice, the canary rollout shape, and the rollback
automation thresholds (which read from `observability-spec.md` SLI
definitions).

## When to Use

- Phase 5 Hardening: when the team is wiring feature-flag tooling
  + canary infrastructure + rollback automation.
- Pre-launch: when the go/no-go checklist needs codification so
  release decisions don't depend on tribal knowledge.
- Post-incident: when an incident retrospective surfaces a release
  discipline gap (canary skipped, rollback threshold too lax, flag
  not used).
- Quarterly review: when the team reflects on how releases went
  and the spec needs an update.

## When NOT to Use

- For per-incident response runbook — use `runbook-author` with
  kind=incident. This atom defines the release plan; runbook
  defines what to do when something goes wrong.
- For SLI / SLO / alert thresholds — use
  `error-monitoring-setup-author` (which this atom cites for the
  rollback threshold mapping).
- For launch-day external comms — use `launch-comms-author`
  (release-discipline is the engineering plan; launch-comms is
  the customer-facing announcement).
- For per-host deploy / rollback CLI verbs — those go in
  `house-site-operate-{vercel,cloudflare,netlify}`.
- For deployment frequency / DORA metrics — those are tracked in
  `weekly-metric-report-author` / `monthly-stakeholder-report-
  author`; this atom defines what to do on each release, not how
  often to release.

## Capabilities Owned

1. **Feature-flag tool selection** — LaunchDarkly (enterprise
   default), Statsig (experimentation-heavy), PostHog Feature
   Flags (when PostHog is the analytics tool), Vercel Edge Config
   (when on Vercel + simple flags), Cloudflare KV (when on
   Cloudflare + simple flags). Per-tool pros/cons + cost matrix.
2. **Canary strategy** — 10% traffic via flag → ramp to 50% / 100%
   over 24h; per-stack canary mechanism (Vercel Edge Config flag,
   Cloudflare traffic-splitting, Netlify Edge Function).
3. **Blue-green strategy** — when canary is insufficient (major
   architectural change); per-stack mechanism.
4. **Rollback automation** — error-rate / latency thresholds tied
   to the SLI definitions in `error-monitoring-setup-author` spec;
   automated rollback via host CLI when thresholds breached for
   sustained duration.
5. **Go/no-go checklist** — pre-deploy gates (CI green, manual
   smoke test passed, on-call ack, comms team notified, status
   page in clean state); deploy-day gates (release marker wired,
   canary cleared 1h, monitoring acknowledged); post-deploy gates
   (24h soak, alerts quiet, RUM stable).
6. **Release-marker wiring** — Sentry release / Datadog release /
   PostHog release; the same Git SHA across systems.
7. **Release cadence guidance** — daily / weekly / per-feature
   trade-offs by team size + risk tolerance + product type.
8. **Deferred-flag cleanup discipline** — flags older than 30 days
   that are 100% / 0% are removed; the spec includes a quarterly
   cleanup ritual.

## Handoffs to Other Skills

- **From `srs-author`** — SRS's "Release Cadence" section cites
  this document.
- **From `master-schedule-author`** — schedule's release-day
  ceremonies cite this document's go/no-go checklist.
- **From `error-monitoring-setup-author`** — observability spec's
  SLI definitions feed this atom's rollback-automation thresholds.
- **From `adr-author`** — feature-flag-tool-selection ADR cites
  this document's tool matrix.
- **To `runbook-author`** — incident runbooks cite this document
  for the rollback procedure (the "what to do when canary fails"
  flow).
- **To `launch-comms-author`** — launch-day comms templates cite
  this document's go/no-go status (clean vs degraded vs hold).
- **To `optimization-loop-author`** — experiments use the
  feature-flag infrastructure defined here.
- **To `house-site-operate-{vercel,cloudflare,netlify}`** — host
  overlays cite this document for the host-specific canary +
  rollback mechanisms.

## Edge Cases

- **Solo-developer project**: the spec is abbreviated; canary may
  be skipped; go/no-go checklist becomes a self-review.
- **Static-only site without backend**: rollback is atomic CDN
  flip; canary unnecessary; the spec is brief.
- **High-traffic site requiring blue-green** (>1M req/min): the
  spec is heavy; per-stack blue-green mechanism is load-bearing.
- **Compliance-bound release** (SOC2 / FedRAMP / HIPAA): the
  go/no-go checklist includes audit-trail gates; release-marker
  wiring is mandatory; the spec is rigorous.
- **Frequently-broken release** (>5% rollback rate sustained):
  the spec becomes the retrospective input — what's missing in
  the checklist that lets bad releases through?

## References

No external `references/*.md` files yet — first real authoring run
will produce templates worth promoting (the feature-flag tool
comparison, the per-stack canary configuration template, the
go/no-go checklist). Per the v0.7.0 speculative-skill convention,
the absence is flagged here rather than papered over.
