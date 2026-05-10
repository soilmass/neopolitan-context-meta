---
name: performance-budget-author
description: >
  Produces the per-page-type performance-budget document. Output:
  `docs/performance-budget.md` and the CI enforcement template at
  `.github/workflows/bundle-check.yml` (bundlesize, size-limit,
  Lighthouse CI gates). Per-page-type budget tables for marketing
  (≤130-170 KB critical-path JS, ≤300 KB total) and WebGL hero
  (≤200 KB excluding three.js core, ≤600 KB total, ≤100 draw
  calls, HTML-LCP-then-canvas pattern). Cites E3 §1.3 and
  Tinder's documented public budget. Free-standing atom — applies
  across the methodology and across all five stack combos.
  Do NOT use for: budget enforcement at CI time (runtime tools —
  bundlesize, size-limit, Lighthouse CI — enforce the spec this
  atom authors); SRS NFRs (use srs-author — the perf-budget cites
  the NFRs); WCAG-conformance (use motion-conformance-author);
  analytics event taxonomy (use analytics-instrumentation-author).
license: Apache-2.0
metadata:
  version: "0.1.0"
  archetype: atom
  tags: [cross-cutting, performance, weekly]
  changelog: |
    v0.1.0 — initial. Authored as part of v0.6.0 Phase 5 cross-
            cutting-tools batch. Ahead-of-trigger per
            docs/ARCHITECTURE-OPTIONS-v0.2.md Phase 5; user
            explicitly approved maximalist scope on 2026-05-08.
---

# performance-budget-author

> **pre-trigger build (v0.6.0)**; reassess when first consumer hits
> a perf-crisis triggering the codified budgets per
> `docs/ARCHITECTURE-OPTIONS-v0.2.md` Phase 5.

Free-standing atom that produces the performance-budget document
+ the CI enforcement template. Not in any family — applies across
the site-build / site-design / site-operate methodology and across
all 5 stack combos. The document covers per-page-type budget tables,
the HTML-LCP-then-canvas pattern, the actual CI enforcement template
(with critical-path JS budgets, total page weight, time-to-
interactive thresholds), and the WCAG-conformance-adjacent rationale.
They are read by the analytics-instrumentation-author event taxonomy
for the perf-related event design, and by the motion-conformance-
author for the motion-budget alignment.

The atom outputs are read by the analytics taxonomy as event design
inputs and feed the wcag-conformance-adjacent specifications.

## When to Use

- Phase 2 Requirements: when the SRS NFRs cite "performance budgets
  per page type" and need a load-bearing document defining the
  numbers.
- Phase 5 Hardening: when CI gates need to be wired and the budgets
  document is the spec the gates implement.
- Pre-launch optimization sweep: when the team disagrees on whether
  the site is "fast enough" and needs an arbiter.
- Regression: when a subsequent release causes a CWV regression
  and the budget is the rollback threshold.

## When NOT to Use

- For the SRS itself — perf-budget cites SRS NFRs; it doesn't
  duplicate them. Use `srs-author`.
- For motion-a11y conformance — that's `motion-conformance-author`.
- For runtime CI tooling configuration — this atom authors the
  spec; bundlesize / size-limit / Lighthouse CI are the tools that
  enforce it.
- For per-stack overlays of perf budgets — those are
  `house-site-build-{nextjs,nuxt,astro,sveltekit,webflow}` (each
  references this spec from its bundle-budget table).

## Capabilities Owned

1. **Per-page-type budget table** — marketing site / WebGL hero /
   app shell / dashboard, each with critical-path JS / total JS /
   CSS / image weight / total page weight / TTI thresholds.
2. **Per-resource budget rationale** — citing E3 §1.3 evidence
   (Tinder 170 KB main JS public budget; Awwwards-tier reality of
   200 KB excl. three.js core for WebGL hero).
3. **CI enforcement template** — `.github/workflows/bundle-check.
   yml` with bundlesize / size-limit / Lighthouse CI invocations
   per the chosen page types.
4. **HTML-LCP-then-canvas pattern** — the architectural pattern
   for hero-WebGL sites that legitimately keep LCP < 2.5s.
5. **Three.js draw-call + lights-with-shadows + GPU texture
   VRAM budgets** — when WebGL is in use.
6. **Failure-mode catalog** — what happens when the budget is
   exceeded (CI fails the PR; rollback automation triggers if a
   merged PR breaks the budget in production).

## Handoffs to Other Skills

- **From `srs-author`** — the SRS's "Performance NFRs" section
  cites this document by URL/section. Authoring sequence: SRS first
  with placeholder "see docs/performance-budget.md", then this
  atom fills the document.
- **From `motion-conformance-author`** — the motion-a11y document
  cites this document for the bundle-budget context (a heavy
  motion library load violates both perf and a11y simultaneously).
- **To `runbook-author`** — Phase 5 production runbook references
  this document for the rollback threshold (auto-rollback if CWV
  regresses past the budget).
- **To `optimization-loop-author`** — Phase 7 optimization loop
  uses the budget as the constraint that bounds experiments.
- **To `house-site-build-{nextjs,nuxt,astro,sveltekit,webflow}`** —
  per-stack overlays cite this document in their bundle-budget
  tables; the per-stack overlay's budget rows specialize but do
  not contradict.

## Edge Cases

- **Project ships on Webflow**: most budget knobs are platform-
  bounded. The document still applies but the enforced surface is
  smaller (custom-code embed weight + image weight + CMS query
  patterns; the runtime is opaque).
- **Project includes a non-trivial native iOS/Android app**: this
  atom is web-only. The mobile-app perf budget belongs to a
  parallel document (out of library scope).
- **Project is internal-only / no public deploy**: the SRS may
  relax CWV thresholds, but the bundle-size discipline still
  applies (developer-experience cost of large bundles is the same).
- **Competing arbiter**: when stakeholder pressure pushes for "ship
  it; we'll fix perf later," this document is the canonical "no"
  the engineering lead points at.

## References

- `references/budget-tables.md` — the canonical per-page-type tables
  with rationale citations to E3 §1.3.
- `references/ci-enforcement-template.md` — the
  `.github/workflows/bundle-check.yml` template + size-limit
  configuration + Lighthouse CI configuration.
- `references/three-js-budgets.md` — WebGL-specific budgets
  (draw calls, lights-with-shadows, GPU texture VRAM with KTX2,
  the HTML-LCP-then-canvas pattern, Active Theory + Lusion +
  Igloo + 14islands documented practices).
