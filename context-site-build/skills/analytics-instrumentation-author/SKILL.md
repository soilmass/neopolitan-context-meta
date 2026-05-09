---
name: analytics-instrumentation-author
description: >
  Authors the analytics event-taxonomy specification + the per-event
  Zod schema definitions for a site/web-app project. Writes
  docs/analytics-spec.md plus src/lib/analytics/events.ts. Codifies
  GA4 / PostHog / Plausible event shapes; verb_noun snake_case
  naming convention; per-event server-side tagging conventions; the
  privacy-posture matrix per analytics tool. Free-standing atom.
  Do NOT use for: error monitoring instrumentation (use
  error-monitoring-setup-author); AEO / Schema.org structured data
  (use aeo-schema-author); KPI definition + measurement plan (use
  kpi-author — this atom defines the events; kpi-author defines
  which events feed which KPIs); analytics-tool-selection ADR (an
  ADR via adr-author cites this atom's privacy-posture matrix).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [cross-cutting, analytics, weekly]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.6.0 Phase 5 cross-
            cutting-tools batch. Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 5; user
            explicitly approved maximalist scope on 2026-05-08.
---

# analytics-instrumentation-author

> **pre-trigger build (v0.6.0)**; reassess when first consumer
> needs codified analytics taxonomy per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 5.

Free-standing atom that produces the analytics event-taxonomy
spec + the Zod schema definitions for runtime event validation.

## When to Use

- Phase 1 Discovery: when KPIs are being authored and the
  measurement plan needs an event taxonomy.
- Phase 2 Requirements: when the SRS calls for analytics
  instrumentation as an NFR.
- Phase 5 Hardening: when the team is wiring the chosen analytics
  tool (GA4 / PostHog / Plausible / Fathom) and needs the event
  schema.
- Pre-launch: when the marketing team asks "what will we measure?"
  and the answer needs to be a typed contract.

## When NOT to Use

- For KPI / OST definition — use `kpi-author` / `ost-author`. This
  atom defines events; KPI maps events → metrics → goals.
- For error monitoring (Sentry / Datadog) — use
  `error-monitoring-setup-author`.
- For Schema.org / JSON-LD structured data (AEO / SEO) — use
  `aeo-schema-author`.
- For consent management (cookie banners, GDPR/CCPA flows) — those
  belong to a privacy-tooling atom not yet built (out of scope per
  coverage.md; the user-invocable `draft-consent-banner` covers it
  now if needed).

## Capabilities Owned

1. **Event-taxonomy schema** — the canonical event-name namespace
   (`marketing.*`, `auth.*`, `commerce.*`, `engagement.*`,
   `error.*`) with per-event property schemas.
2. **`verb_noun` snake_case naming** — `view_homepage`,
   `click_cta_primary`, `submit_lead_form`, `complete_purchase`,
   `start_session` (not camelCase / PascalCase).
3. **Zod schemas** — runtime validation; events that fail
   validation log a warning and drop rather than crashing.
4. **Per-event tool routing** — which analytics tools each event
   goes to (some are GA4-only; some are PostHog-only for product
   analytics + experiments; Plausible/Fathom typically receive only
   page views).
5. **Server-side tagging conventions** — for tools that support it
   (GA4 server-side via Cloud Run / Cloudflare Workers; PostHog
   server-side via the JS server SDK).
6. **Privacy-posture matrix** — per-tool cookie/no-cookie + EU-
   hosted/US-hosted + opt-in/opt-out defaults; the source of truth
   for the analytics-tool-selection ADR.
7. **Common-properties contract** — properties on EVERY event:
   `release` (Git SHA), `tenant`, `user_role`, `session_id`,
   `experiment_bucket` (when active).

## Handoffs to Other Skills

- **From `kpi-author`** — KPI's "Measurement Plan" cites this
  document by URL/section. Authoring sequence: KPI first with
  placeholder events, then this atom defines the schemas, then KPI
  is updated to reference real event names.
- **From `srs-author`** — SRS's "Analytics NFRs" section cites
  this document.
- **From `adr-author`** — analytics-tool-selection ADR cites this
  document's privacy-posture matrix.
- **To `weekly-metric-report-author`** — the weekly report's
  metrics are computed from this atom's events.
- **To `optimization-loop-author`** — experiments cite the
  experiment-bucket common property + custom experiment events.
- **To `house-site-operate-{nextjs,nuxt,astro,sveltekit,webflow}`**
  — operate overlays cite this document for the analytics SDK
  installation + the server-side tagging pattern per host.

## Edge Cases

- **Site is internal-only**: analytics simplifies; the document
  still applies but the events table is shortened.
- **Site uses multi-tool analytics** (Plausible + PostHog): the
  per-event tool routing matrix spans both; events may go to one
  or both depending on the property surface.
- **Event taxonomy outgrows the namespace**: when `engagement.*`
  exceeds ~30 events, split into sub-namespaces (`engagement.
  scroll.*`, `engagement.video.*`, etc.).
- **Privacy-posture conflict** (client wants GA4 but the EU office
  requires Plausible): document the dual-tool setup with the
  property-level routing decisions.

## References

- `references/event-namespace.md` — the canonical event-name
  namespace with per-event property schemas.
- `references/zod-templates.md` — the Zod schema templates per
  common event shape.
- `references/privacy-matrix.md` — per-tool privacy-posture
  matrix sourced from E3 §5 wider-stack-notes.
