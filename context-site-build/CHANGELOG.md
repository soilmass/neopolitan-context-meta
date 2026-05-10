# Changelog

Cross-skill change log for `context-site-build`. Every notable change
to any skill in this library produces an entry here. Skills do not
maintain their own CHANGELOG.md files — this is the canonical source.

Format follows the meta-pipeline's `GOVERNANCE.md` conventions.
Categories: Breaking, Added, Changed, Deprecated, Removed, Health,
Rolled back, Security.

---

## [Unreleased]

(Pending the next release.)

---

## [0.6.1] - 2026-05-09

PATCH bump — documentation-only release adding 9 v1.0-readiness
docs + the deferred overlay-description cleanup from PR #7. No
SKILL.md content/behavior changes; all 21 stack overlays + 7
cross-cutting atoms remain at v0.1.0.

### Added

- **`docs/GETTING-STARTED.md`** — second-consumer onboarding;
  pick-a-stack + pick-a-shape + Quickstart for marketing-site on
  Combo A; two-word summary per atom (cheat sheet); pointers to
  walkthroughs / map / versioning / troubleshooting / examples.

- **`docs/VERSIONING-POLICY.md`** — SemVer adapted from
  meta-pipeline's parent template; per-skill + per-library bump
  tables; v1.0 freeze contract (what's frozen vs not); v1.0+
  MAJOR-bump mechanics; pre-v1.0 timeline.

- **`docs/LIBRARY-MAP.md`** — visual + textual dependency graph;
  family roster (3) with phase-organized atoms; cross-family
  handoff diagram; stack-overlay composition diagram (CSS-cascade
  override stack); cross-cutting atom relations to overlays;
  dependency-direction table (DAG; no cycles); per-atom output
  file paths.

- **`docs/walkthroughs/{marketing-site,e-commerce,web-app,
  microsite}.md`** — phase-by-phase walkthroughs for the 4
  canonical project shapes. Each names the atom invocation order +
  which atoms are skippable for solo-dev variants.

- **`docs/examples/outputs/{vision,srs,art-direction,motion-
  language,kpi,conformance-statement,optimization-backlog,
  runbook-deployment}.md`** — anonymized illustrative outputs
  (8 files) of the most-cited atoms in the walkthroughs. Use as
  shape reference, not template.

- **`docs/TROUBLESHOOTING.md`** — common errors per atom +
  per-stack-overlay; drift-gate guidance + anti-trigger fallback
  patterns + coverage.md gaps + stack-overlay-specific issues +
  cross-cutting tool atom issues + verify.sh failures + audit-
  finding (B-series) filing guidance.

### Changed

- **Overlay description cleanup (deferred from PR #7)** —
  the 21 stack overlays from v0.5.0 cited the 7 cross-cutting
  atoms via the A62 anti-trigger fallback pattern with the
  qualifier `(use X-author once built; ...)`. With those atoms
  now built (v0.6.0), the "once built" qualifier is dropped via
  bulk edit across 7 overlays. Form: `use X-author; the user-
  invocable draft-X covers it now)` — both options now exist;
  draft-X remains the alternative when the atom isn't installed
  in the operator's environment.

  No per-overlay version bumps for this — it's a clarification
  not a behavior change; overlay versions remain at 0.1.0.
  (The library's CHANGELOG-sync gate isn't enforced for this
  library's verify.sh, unlike the meta-pipeline.)

### Health

- All 75 skills validate clean (`validate-metadata.py --all`).
- `verify.sh` 4/4 green at v0.6.1.

### Discipline note

This PATCH release does NOT change the v0.5.0–v1.0.0 ahead-of-
trigger window per `coverage.md`. The discipline-restoration
commitment for v1.0.x onward remains in force — post-v1.0.0
new atoms ship only on organic build triggers from real consumer
projects.

---

## [0.6.0] - 2026-05-08

Phase 5 of Option C from `docs/ARCHITECTURE-OPTIONS-v0.2.md`.
**MINOR bump** — 7 new free-standing cross-cutting tool atoms
covering perf budget, motion-a11y conformance, analytics
instrumentation, AEO schema, i18n strategy, error monitoring +
observability, and release discipline. Library version 0.5.0 →
0.6.0; `snapshot_version` 0.5.0 → 0.6.0; `plugin.json` + root
`marketplace.json` bumped.

### ⚠ Discipline-shift disclosure (continued from v0.5.0)

This release continues the v0.5.0 ahead-of-trigger window per
the `coverage.md` "v0.5.0–v1.0.0 Ahead-of-Trigger Note" section.
The cross-cutting atoms ship per the maximalist Phase 5 scope
(7 atoms) the operator approved on 2026-05-08; the build triggers
("first consumer hits perf-crisis", "first consumer hits motion-
a11y crisis", etc.) have not fired.

Each atom carries a `> pre-trigger build (v0.6.0)` quote-block
marker. The discipline-restoration commitment for v1.0.x onward
remains in force.

### Added — 7 cross-cutting tool atoms

#### Phase 5 base (2)

- **`performance-budget-author`** — per-page-type budget tables
  (marketing ≤130-170 KB critical JS / WebGL hero ≤200 KB excl.
  three.js core / ≤100 draw calls); HTML-LCP-then-canvas pattern;
  CI enforcement template (.github/workflows/bundle-check.yml +
  bundlesize + size-limit + Lighthouse CI). Cites E3 §1.3 (Tinder
  170 KB main JS public budget; Awwwards-tier WebGL reality).
  Output: `docs/performance-budget.md` + workflow template.

- **`motion-conformance-author`** — WCAG 2.2 motion-criteria
  coverage table (2.1.1 / 2.2.2 / 2.3.3 / 2.4.7 / 2.5.7 / 2.5.8);
  three prefers-reduced-motion patterns; focus-visible parity for
  custom cursors; keyboard scroll bindings; lite-mode alternative-
  experience pattern; axe-core CI + manual test plan; honest 30-
  40% automated-tooling caveat. Pairs with `house-site-design-a11y`
  (PR #6). Output: `docs/05-hardening/motion-conformance.md` +
  axe-core config + manual test plan.

#### Research-surfaced atoms (2)

- **`analytics-instrumentation-author`** — event-taxonomy spec +
  Zod schemas (verb_noun snake_case naming; per-event tool routing
  across GA4 / PostHog / Plausible / Fathom; server-side tagging
  conventions; privacy-posture matrix; common-properties contract
  with release / tenant / user_role / session_id /
  experiment_bucket). Output: `docs/analytics-spec.md` +
  `src/lib/analytics/events.ts`.

- **`aeo-schema-author`** — Schema.org / JSON-LD spec per page
  type (Organization / WebSite / Product / Article / FAQ / HowTo +
  others); Rich Results Test CI integration; AI-search citation
  discipline (Perplexity / ChatGPT-search / Gemini); AEO baseline
  metric set; OpenGraph + Twitter Card mapping. Output:
  `docs/aeo-schema-spec.md` + `src/lib/schema/<type>.ts` generators.

#### Discipline-pulled atoms (3)

- **`i18n-strategy-author`** — locale routing strategy (sub-path /
  sub-domain / domain); locale-fallback chain; RTL strategy + CSS
  Logical Properties discipline; TMS tool selection (Crowdin /
  Lokalise / Phrase / Smartling); CMS locale config (Sanity /
  Storyblok / Webflow / Hygraph); per-locale launch checklist.
  Output: `docs/i18n-spec.md`.

- **`error-monitoring-setup-author`** — tool selection (Sentry /
  Datadog / Honeycomb / Bugsnag); instrumentation conventions
  (service / env / release / tenant tags); SLI definitions
  (latency p95, error rate, availability); release-marker wiring;
  PII discipline; custom-metric template (THREE.WebGLRenderer.info
  when WebGL in use). Output: `docs/observability-spec.md` +
  `src/lib/telemetry.ts`.

- **`release-discipline-author`** — feature-flag tool selection
  (LaunchDarkly / Statsig / PostHog / Vercel Edge Config /
  Cloudflare KV); canary strategy (10% → 50% → 100% over 24h);
  blue-green when canary insufficient; rollback automation tied to
  SLI thresholds; go/no-go checklist (pre / during / post deploy
  gates); deferred-flag cleanup discipline; release-cadence
  guidance. Output: `docs/release-plan.md` + `deploy/feature-
  flags.yml`.

### Changed

- One-character description trim on `motion-conformance-author`
  (was 1025 chars; cap is 1024). Wording adjusted to fit the cap
  without losing the load-bearing capabilities listed.

### Health

- All 7 atoms validate clean (`validate-metadata.py` exit 0; atom
  archetype; 6 required sections present); marked `fresh` in
  SNAPSHOT.lock pending the v1.0-rc1 audit pass (PR #9).
- All 21 stack overlays + 47 prior atoms / routers remain
  `healthy` / `fresh` per their prior state.
- `verify.sh` 4/4 green.

### Cross-PR overlay updates (deferred)

The 21 stack overlays from v0.5.0 cite these atoms via the A62
anti-trigger fallback pattern (`use X-author once built; the user-
invocable draft-X covers it now`). With these atoms now built, the
overlay descriptions can drop the qualifiers. That cleanup is
deferred to PR #8 (v1.0-readiness documentation; the docs explain
the canonical citation pattern, after which the overlay descriptions
get the trim).

---

## [0.5.0] - 2026-05-08

Phase 4 of Option C from `docs/ARCHITECTURE-OPTIONS-v0.2.md`.
**MINOR bump** — 21 new stack-specific policy overlays authored
across 5 stack families (Next.js / Nuxt / Astro / SvelteKit /
Webflow × 3) + 2 cross-stack overlays (motion / a11y) + 1 design-
tool overlay (Figma) + 3 hosting overlays (Vercel / Cloudflare /
Netlify). Library version 0.4.0 → 0.5.0; `snapshot_version`
0.4.0 → 0.5.0; `plugin.json` + root `marketplace.json` bumped.

### ⚠ Discipline-shift disclosure

This release ships **21 ahead-of-trigger policy overlays** —
the largest single ahead-of-trigger commitment in this library
to date. Per `context-meta-pipeline` audit finding **A56** (the
v0.7.0 discipline-shift commitment), ahead-of-trigger work
requires explicit operator approval matching the v0.7.0
disclosure pattern.

The trigger that has not fired (per the meta-pipeline's
`docs/PATH-TO-V1.md` P4): "≥2 tiers of `house-*` overlays
exist on the same mechanism atom." Zero `house-*` overlays
existed before this PR; the maximalist Phase 4 scope was chosen
explicitly by the operator on 2026-05-08.

**Disclosure pattern**:
1. Each overlay's SKILL.md body begins with a top-of-body
   `> pre-trigger build (v0.5.0)` quote-block marker.
2. `coverage.md` "v0.5.0–v1.0.0 Ahead-of-Trigger Note" section
   documents the cumulative discipline shift, the operator
   approval, and the discipline-restoration commitment.
3. Audit-finding ledger entry **B9** captures the operator
   approval + the v1.0.x restoration boundary.

**Discipline-restoration commitment for v1.0.x and beyond**:
After v1.0.0 ships, no new atoms or overlays will be authored
without an organic build trigger firing on a real consumer
project. Library growth post-v1.0 is consumer-driven, not
speculation-driven.

### Added — 21 stack-specific policy overlays

#### Stack-family combos (15)

For each of 5 canonical Awwwards-tier stacks (per E3 §5), three
overlays — one per consuming family. Each overlay applies on top
of 5 mechanism atoms in its family with stack-specific conventions
(SRS NFRs, ADR catalogs, sprint cadence, deploy verbs, threat
surfaces / design-system tooling, motion stack, 3D library,
component conventions / runbook deploy verbs, observability,
release discipline).

- **Combo A "React-cinematic" (Next.js × 3)**:
  `house-site-build-nextjs`, `house-site-design-nextjs`,
  `house-site-operate-nextjs`. Vercel + Sanity + R3F + drei +
  GSAP + Motion + Storybook + Chromatic.
- **Combo B "Vue/Nuxt-cinematic" (Nuxt × 3)**:
  `house-site-build-nuxt`, `house-site-design-nuxt`,
  `house-site-operate-nuxt`. Nuxt 3 + Tailwind + Pinia + TresJS +
  GSAP + Vue native transitions + Histoire.
- **Combo C "Astro-static-with-WebGL-islands" (Astro × 3)**:
  `house-site-build-astro`, `house-site-design-astro`,
  `house-site-operate-astro`. Astro 4+ + islands architecture +
  content collections + vanilla Three.js or R3F island + GSAP +
  Lenis (hero-island-only) + tighter bundle budgets.
- **Combo D "Svelte/SvelteKit, performance-pure" (SvelteKit × 3)**
  — the Igloo Inc Site of the Year 2024 combo.
  `house-site-build-sveltekit`, `house-site-design-sveltekit`,
  `house-site-operate-sveltekit`. SvelteKit 2+ + adapter-driven +
  vanilla Three.js + GSAP + Svelte native transitions + Histoire +
  strictest bundle budgets.
- **Webflow visual-editor (× 3)**:
  `house-site-build-webflow`, `house-site-design-webflow`,
  `house-site-operate-webflow`. Webflow Designer + Variables +
  Components + Logic + custom-code embed boundary; SRS gets a
  "What NOT to do in Webflow" anti-pattern section because the
  platform ceiling is load-bearing.

#### Cross-stack overlays (2)

- **`house-site-design-motion`** — stack-agnostic motion
  conventions (motion-token schema, library selection per use case,
  scene-scoping discipline, Loom-link anti-pattern explicitly
  rejected).
- **`house-site-design-a11y`** — WCAG 2.2 motion-criteria coverage
  (2.1.1 / 2.2.2 / 2.3.3 / 2.4.7 / 2.5.7 / 2.5.8); the three
  prefers-reduced-motion patterns; focus-visible parity for custom
  cursors; lite-mode alternative experience pattern; honest 30-40%
  automated-tooling caveat. Pairs with `motion-conformance-author`
  (PR #7 / v0.6.0).

#### Design-tool overlay (1)

- **`house-site-design-figma`** — canonical Figma Variables →
  Tokens Studio → DTCG JSON → Style Dictionary v4 → CSS vars +
  Tailwind v4 + TS pipeline; Component Properties as the API
  contract; Figma Variants encode the 9-state matrix; motion-spec
  via Theatre.js / Lottie / Rive in Storybook (NOT Loom links).

#### Hosting-platform overlays (3)

Stack-agnostic hosting-platform overlays composing with the
framework-specific operate overlays:

- **`house-site-operate-vercel`** — vercel CLI deploy verbs;
  preview-per-PR via Git integration; ISR + Edge Functions via
  Vercel revalidation primitives; Vercel Blob + Cloudinary + Mux
  for assets; Web Analytics + Speed Insights for field RUM;
  KV + Postgres + Edge Config + Blob state stores; vercel.json
  cron jobs.
- **`house-site-operate-cloudflare`** — wrangler CLI deploy verbs;
  Pages vs Workers selection rules; R2 (S3-compatible, no egress) +
  KV + D1 + Durable Objects + Queues storage primitives; Cache
  Rules + Page Rules cache strategy; Workers Analytics Engine for
  custom metrics; Cron Triggers.
- **`house-site-operate-netlify`** — netlify CLI deploy verbs;
  deploy contexts (production / deploy-preview / branch-deploy)
  for preview-per-PR; Functions vs Edge Functions selection;
  Netlify Blobs + Forms + Identity first-class services; build-
  plugin extensibility model.

### Cross-PR references (per A62 anti-trigger fallback)

Several overlays reference cross-cutting atoms scheduled for PR #7
(library v0.6.0). Per A62 anti-trigger fallback discipline, those
references use the user-invocable peer fallback pattern. When PR
#7 ships, a follow-up commit (or PR #8 cleanup) will update the
overlay descriptions to drop the qualifiers.

The cross-PR atoms cited:
- `performance-budget-author` (PR #7)
- `motion-conformance-author` (PR #7)
- `analytics-instrumentation-author` (PR #7)
- `aeo-schema-author` (PR #7)
- `i18n-strategy-author` (PR #7)
- `error-monitoring-setup-author` (PR #7)
- `release-discipline-author` (PR #7)

### Health

- All 21 overlays validate clean (`validate-metadata.py` exit 0;
  policy archetype; 4 required sections present); marked `fresh`
  in SNAPSHOT.lock pending the first audit pass (PR #9).
- All 47 prior atoms + 3 routers remain `healthy`.
- `verify.sh` 4/4 green.

### Naming + structure

- Overlay names sit at the regex 4-segment cap
  (`house-site-build-nextjs` etc.). Logical decomposition:
  `<context>-<compound-domain>-<aspect>` where the compound domain
  is `site-build` / `site-design` / `site-operate` (the consuming
  family). The naming spec's "policy = 3-segment" guidance is
  loosened here because the family names are themselves 2-segment
  compounds.
- `.bootstrap/stack-overlays-intake.yaml` — Stage 1 artifact for
  the per-overlay `skill-policy-overlay` procedure; lists all 21
  overlays with their applies_on_top_of mechanism atoms.

---

## [0.4.0] - 2026-05-09

### Added — site-operate family bootstrap (14 atoms + 1 router; library v0.3.0 → v0.4.0)

Phase 3 of Option C from `docs/ARCHITECTURE-OPTIONS-v0.2.md`. The
`site-operate` family is bootstrapped from scratch covering Phase
5 a11y conformance + Phase 6 launch communications + Phase 7
full post-launch operations + Awwwards-tier polish + awards.

#### Family — site-operate

Per-family router + 14 atoms across 3 tiers. Authority is
composite: SOP §8.2 (Accessibility) + §9 (Phase 6 Launch) + §10
(Phase 7 Post-Launch) + Awwwards-tier research synthesis (E2 §C.3
Active Theory polish + §C.6 Ueno's Awards (optional) phase).
Family bootstrap walked all 6 stages of `family-bootstrap`;
bootstrap artifacts at
`.bootstrap/site-operate-{intake,capabilities,taxonomy}.md`;
family coverage at `skills/site-operate/coverage.md`.

#### Router — `site-operate` (v0.1.0, archetype: router)

Routing Table covers all 14 in-family atoms; Disambiguation
Protocol covers ~14 atom-pair distinctions including cross-family
pairs (stabilization vs T+8 baseline, weekly vs monthly across
families, AEO vs classic SEO, polish vs handoff, conformance vs
annotations, optimization-backlog vs change-request).

#### Tier 1 — Essential spine (7)

- **`stabilization-report-author`** — 30-day stabilization
  report at hypercare close (SOP §10.1).
- **`hypercare-digest-author`** — Daily memo during weeks 1-4
  (SOP §10.1.1). Tag: `daily-use`.
- **`launch-comms-author`** — Internal + external + status-page
  launch communications (SOP §9.4).
- **`conformance-statement-author`** — WCAG 2.2 conformance
  statement at Phase 5 close (SOP §8.2.7).
- **`optimization-backlog-author`** — RICE/ICE-scored
  prioritized optimization backlog (SOP §10.2.5). Tag: `weekly`.
- **`optimization-loop-author`** — Single experimentation cycle
  (SOP §10.3.1). Tag: `weekly`.
- **`polish-discipline-author`** — Polish phase plan + per-
  iteration notes (Awwwards-tier addition; research/E2 §C.3
  Active Theory's "polish taking 80%"). No user-invocable peer.

#### Tier 2 — Specialist (5)

- **`monthly-stakeholder-report-author`** — Monthly consolidation
  of 4 weekly memos (SOP §10.5.2). Tag: `weekly`.
- **`quarterly-business-review-author`** — QBR with metrics
  trends + ROI + competitive + strategic recommendations (SOP
  §10.5.3).
- **`win-regression-report-author`** — Win/regression analysis
  at T+8 (SOP §10.2.4).
- **`diagnostic-sweep-author`** — Phase-7 diagnostic across 7
  method areas (SOP §10.2.2).
- **`aeo-baseline-author`** — AI Search baseline across 5
  engines (SOP §10.2.3 + §10.3.3).

#### Tier 3 — Long tail (2)

- **`annual-retrospective-author`** — Annual retrospective +
  roadmap proposal (SOP §10 named in §12).
- **`awards-submission-author`** — Awwwards / SOTD / SOTM /
  SOTY submission package (Awwwards-tier addition; research/E2
  §C.6 Ueno's "Awards (optional)"). No user-invocable peer.

### Changed — bookkeeping

- **`SNAPSHOT.lock`** v0.3.0 → v0.4.0: 15 new entries (1 router
  + 14 atoms at v0.1.0; health: fresh on initial → healthy after
  P3.6 audit + drift iteration).
- **Library `coverage.md`** updated: site-operate promoted from
  Domains Deferred to Domains Claimed; Coverage Matrix Status
  reflects 46 skills total (16 site-build + 14 site-design + 14
  site-operate + 3 routers); Domains Deferred now lists stack
  overlays (Phase 4 of Option C), cross-cutting tools (Phase 5),
  Phase 4 build ceremonies (out of scope), and adjacent-awards-
  body submissions (build trigger via operator decision).
- **Library `CHANGELOG.md`** — this entry.
- **`plugin.json`** v0.3.0 → v0.4.0 (MINOR — new family + 14
  skills + 1 router per VERSIONING-POLICY).
- **`marketplace.json`** plugin row v0.3.0 → v0.4.0.
- **`.bootstrap/`** — 2 new files: `site-operate-intake.yaml` +
  `site-operate-capabilities.json` (taxonomy lives at
  `skills/site-operate/taxonomy.md`).

### Notes

- All 14 atoms grounded in SOP §8.2 + §9 + §10 with cross-
  references to research/E2 (Awwwards-tier additions).
- 12 of 14 atoms have user-invocable peers; 2 are Awwwards-tier
  additions with no peer (`polish-discipline-author`,
  `awards-submission-author`).
- Cross-family relationships documented (site-operate ↔
  site-build ↔ site-design at Phase 5/6/7 boundaries).
- Pre-existing v0.3.0 findings (B1–B8 / A57–A64) carry forward
  unchanged.
- Library now covers the complete site-build methodology
  including the Awwwards-tier creative + polish + awards phases.
  Phase 4 of Option C (stack overlays) and Phase 5 (cross-cutting
  tools) remain.

---

## [0.3.0] - 2026-05-09

### Added — site-design family bootstrap (14 atoms + 1 router; library v0.2.0 → v0.3.0)

Phase 2 of Option C from `docs/ARCHITECTURE-OPTIONS-v0.2.md`. The
`site-design` family is bootstrapped from scratch covering Phase 3
Design + the Awwwards-tier upstream creative phases the SOP doesn't
have as named deliverables (mood board, art direction, concept,
motion language) per `docs/research/E2-agency-methodologies.md`'s
synthesis of ~20 top agency methodologies.

#### Family — site-design

Per-family router + 14 atoms across 3 tiers. Authority is
composite: the SOP §6 (Phase 3 Design) plus the Awwwards-tier
research synthesis. Family bootstrap walked all 6 stages of
`family-bootstrap`; bootstrap artifacts at
`.bootstrap/site-design-{intake,capabilities,taxonomy}.md`; family
coverage.md at `skills/site-design/coverage.md`.

#### Router — `site-design` (v0.1.0, archetype: router)

Routing Table covers all 14 in-family atoms; Disambiguation
Protocol covers ~14 atom-pair disambiguations including
cross-family pairs (concept vs vision, design-system vs
design-philosophy, discovery-tick vs persona-author/ost-author).

#### Tier 1 — Essential creative + design-system spine (7)

- **`mood-board-author`** (atom, v0.1.0) — Mood Board + curated
  Reference list with critique. Lusion's Phase 1 of their
  three-phase methodology. The Awwwards-tier deliverable that
  enshrines visual exploration as a billable, sign-offable phase.
- **`art-direction-author`** (atom, v0.1.0) — Art Direction
  document. Defended visual language synthesized from the mood
  board: named palette (often two-color per Awwwards convention),
  type system, motion vocabulary, photography/illustration
  direction. Used as a named, billable phase by Active Theory,
  Lusion, Bonhomme, Locomotive, Build in Amsterdam, Mathematic,
  Dogstudio, Immersive Garden.
- **`concept-author`** (atom, v0.1.0) — Concept document.
  Creative thesis + narrative + lore + defended creative
  territory. Distinct from vision (business-outcome focused) by
  being creative-direction focused.
- **`motion-language-author`** (atom, v0.1.0) — Motion Language
  document. Durations, easings, choreography rules, motion
  tokens, per-interaction motion contracts, prefers-reduced-motion
  policy, performance budget for motion.
- **`design-tokens-author`** (atom, v0.1.0) — DTCG JSON →
  Style Dictionary v4 → CSS-vars + Tailwind v4 @theme + TS
  types pipeline. 8 token categories (color/type/spacing/radius/
  shadow/motion/z-index/breakpoints).
- **`component-states-matrix-author`** (atom, v0.1.0) —
  Per-component 9-state matrix. Visual / behavior / a11y row per
  state. Refuses "ready" until all states filled.
- **`engineering-handoff-spec-author`** (atom, v0.1.0) —
  Engineering Handoff Spec. Bundles tokens + matrices +
  motion language + a11y annotations into the Phase 3 close
  contract from Design to Engineering. Refuses "throw it over
  the wall" hand-offs without product-trio evidence.

#### Tier 2 — Specialist (5)

- **`concept-prototyping-author`** (atom, v0.1.0) — Concept
  prototype in 3D / runtime tools (Houdini / C4D / vvvv /
  WebGL / R3F / Unity / Unreal / Blender). Lusion's Phase 2.
  Tests technical + visual + dynamic feasibility before brief
  is signed.
- **`wireframe-author`** (atom, v0.1.0) — Wireframes across
  three fidelities (lo-fi / mid-fi / hi-fi) per Hello Monday's
  3-fidelity ladder + SOP §6.2.
- **`prototype-author`** (atom, v0.1.0) — Clickable prototype
  for usability testing top 3-5 user tasks (SOP §6.3.1).
- **`usability-synthesis-author`** (atom, v0.1.0) — Usability
  test design + synthesis with Sev-1 → Sev-4 issue ranking
  (SOP §6.3.2 + §6.3.3).
- **`a11y-annotations-author`** (atom, v0.1.0) —
  Per-component accessibility annotations on hi-fi designs
  (SOP §6.4.5). Maps WCAG 2.2 success criteria.

#### Tier 3 — Long tail (2)

- **`design-system-author`** (atom, v0.1.0) — Full design
  system documentation. Atomic Design hierarchy, per-component
  owner + version + deprecation + contribution model, content
  guidelines, internationalization, Storybook reference (SOP
  §6.4 full).
- **`discovery-tick-author`** (atom, v0.1.0) — Phase 4 weekly
  continuous-discovery synthesis (SOP §7.5 + §2.3). Pulls
  interview / analytics / support / A/B signal into 1-page memo
  with 1–3 backlog candidates in hypothesis form.

### Changed — bookkeeping

- **`SNAPSHOT.lock`** v0.2.0 → v0.3.0: 15 new entries (1 router
  + 14 atoms at v0.1.0 / fresh).
- **Library `coverage.md`** updated: site-design promoted from
  Domains Deferred to Domains Claimed; Coverage Matrix Status
  reflects 32 skills total (16 site-build + 14 site-design + 2
  routers).
- **Library `CHANGELOG.md`** — this entry.
- **`plugin.json`** v0.2.0 → v0.3.0 (MINOR — adding new family
  + 14 skills + 1 router per VERSIONING-POLICY).
- **`marketplace.json`** plugin row v0.2.0 → v0.3.0.
- **`.bootstrap/`** — 3 new files: `site-design-intake.yaml`,
  `site-design-capabilities.json`, `site-design-taxonomy.md`
  (the family-bootstrap Stages 1-3 artifacts).

### Notes

- All 14 atoms grounded composite — primary in
  `site-build-procedure.md` v2.0 §6, secondary in the v0.7.0
  Awwwards-tier research (`docs/research/`).
- 4 of the 7 Tier 1 atoms (`mood-board-author`,
  `art-direction-author`, `concept-author`, `motion-language-
  author`) are **Awwwards-tier additions with no user-invocable
  peer** — they encode named phases agencies use that the SOP
  doesn't have as named deliverables. The remaining atoms have
  `draft-*` user-invocable peers.
- Cross-family relationships documented: `site-design` atoms
  cite `site-build` atoms (vision-author, persona-author,
  design-philosophy-author) by stable name; `site-build` atoms
  remain unchanged.
- Drift audit + iteration deferred to P2.6 (separate task);
  initial validate-metadata.py PASSED for all 32 skills.
- Pre-existing v0.2.0 findings (B1–B8 / A57–A64) carry forward
  unchanged.

---

## [0.2.0] - 2026-05-09

### Added — Tier 2/3 atom completion (10 new atoms; library v0.1.2 → v0.2.0)

Phase 1 of Option C from `docs/ARCHITECTURE-OPTIONS-v0.2.md`. The
10 Tier 2/3 atoms specced in `skills/site-build/taxonomy.md` are
now built. The site-build family is feature-complete for the
methodology spine; out-of-scope rows in family coverage.md remain
for the `site-design` and `site-operate` families queued in
later phases of the v0.2.x expansion plan.

#### Tier 2 — Specialist atoms (5)

- **`kpi-author`** (atom, v0.1.0) — Phase 1 — KPI & Success Metrics
  document per SOP §4.2.6. Per KPI: definition, baseline, target
  (time-bound), owner, measurement method. Mixes leading + lagging
  indicators. Refuses vanity metrics.
- **`risk-register-author`** (atom, v0.1.0) — Phase 1 onward —
  Risk Register per SOP §4.2.8 + §5.7.3. Six categories
  (Technical, Commercial, Organizational, Regulatory, Schedule,
  External). Uses the premortem technique. Live spreadsheet.
- **`threat-model-author`** (atom, v0.1.0) — Phase 2 — STRIDE
  threat model + security baseline per SOP §5.3.7. Per-component
  threat enumeration, mitigations, security headers, auth /
  authorization, secret management, supply chain, vulnerability
  disclosure.
- **`privacy-plan-author`** (atom, v0.1.0) — Phase 2 — Privacy &
  Compliance Plan + DPIA scaffold per SOP §5.6. Multi-jurisdiction
  (GDPR, CCPA/CPRA, Quebec Law 25, LGPD, DPDP, PIPL). Data flow
  map, lawful basis, consent UX, cookie audit, DSAR handling,
  sub-processor list, breach notification.
- **`master-schedule-author`** (atom, v0.1.0) — Phase 2 — Master
  Schedule + Budget plan per SOP §5.7.1 + §5.7.2. Milestones,
  dependencies, critical path, resource allocation, 10-20%
  contingency. Re-baseline trigger on Major CR approval.

#### Tier 3 — Long-tail atoms (5)

- **`ost-author`** (atom, v0.1.0) — Phase 1 sketch / Phase 2
  refinement — Opportunity Solution Tree per SOP §4.2.7.
  Outcome → opportunities (rooted in persona pains/JTBD) →
  candidate solutions with RICE-style scoring placeholders.
- **`stakeholder-map-author`** (atom, v0.1.0) — Phase 1 —
  Stakeholder Map + RACI per SOP §3 + §4.2.1. Influence-vs-
  interest grid; named decision-makers; escalation path.
- **`design-philosophy-author`** (atom, v0.1.0) — Phase 3 — one-
  page Design Philosophy per SOP §6.1. Brand expression goals,
  audience attributes, tone, constraints, inspirations *with
  critique*, anti-references.
- **`weekly-metric-report-author`** (atom, v0.1.0) — Phase 7 —
  weekly metric memo per SOP §10.5.1. Status, KPIs, ops,
  experiments, content, issues, asks. ≤1 page.
- **`change-request-author`** (atom, v0.1.0) — cross-phase —
  single Change Request per SOP §11.1. Form fields, impact
  assessment, classification (Minor/Moderate/Major), routed
  decision-maker, captured outcome.

#### Changed — bookkeeping

- **`site-build` router** v0.1.1 → v0.1.2: Routing Table extended
  from 6 to 16 rows (now covers all in-family atoms);
  Disambiguation Protocol extended for the new atom pairs;
  "Atoms in This Family" no longer has Specced-Not-Yet-Built
  rows.
- **`SNAPSHOT.lock`** v0.1.2 → v0.2.0: 10 new skill rows
  (Tier 2 + Tier 3 atoms at v0.1.0, health: `fresh`);
  pre-existing Tier 1 atoms unchanged at v0.1.1 / `healthy`.
- **`coverage.md` (family-level)** updated: Tier 2 and Tier 3
  promoted from Specced/Deferred to "In Scope (Tier 2)" /
  "In Scope (Tier 3)"; Specced section now empty (16 atoms
  built); Out of Scope retained verbatim for the `site-design`
  and `site-operate` family deferrals.
- **`plugin.json`** v0.1.2 → v0.2.0 (MINOR — adding new skills
  per VERSIONING-POLICY).
- **`marketplace.json`** plugin row v0.1.2 → v0.2.0.

#### Notes

- All 10 atoms grounded in the operator's
  `site-build-procedure.md` v2.0 SOP (canonical path read at
  P1.1). Each atom cites its specific SOP section in description
  + References.
- Each atom's anti-trigger pattern names the user-invocable peer
  (`draft-kpi-doc`, `draft-risk-register`, etc.) as the fallback
  per the v0.1.2 self-review pattern (B6/A62).
- 5 of 10 atoms cite their existing v0.1.x sibling explicitly in
  Handoffs ("From the user-invocable `draft-X` — peer skill").
- Drift audit + iteration deferred to P1.5 (separate task);
  initial validate-metadata.py PASSED for all 17 skills.
- Pre-existing v0.1.x findings (B1–B8 / A57–A64) carry forward
  unchanged.

---

## [0.1.2] - 2026-05-08

### Changed — self-review pass on the v0.1.1 family (PATCH bump for all 7 skills)

Operator self-review of the 7 freshly-authored skills surfaced
seven substantive issues (3 anti-trigger / cross-family / router-
table issues + 4 internal-consistency / framing fixes). Bumps every
skill from v0.1.0 → v0.1.1. Findings logged as B6 / B7 / B8 (cross-
referenced as A62 / A63 / A64 in the meta-pipeline ledger).

Per-skill changes:

- **`vision-author@0.1.1`** — anti-trigger fallback for `kpi-author`
  → `draft-kpi-doc` (B6); resolved Handoff vs Edge-Case contradiction
  on no-personas (Edge-Case provisional path is canonical); References
  section reframed (no more "Authority surface" mislabeling); deferred
  `references/vision-template.md` row dropped.
- **`persona-author@0.1.1`** — anti-trigger fallback for kpi /
  ost / stakeholder-map (B6); References reframed; deferred row
  dropped.
- **`srs-author@0.1.1`** — anti-trigger fallback for threat-model
  / privacy-plan (B6); precondition "vision/personas don't exist
  yet" moved from When-NOT-to-Use to Edge Cases (correct
  categorization); References reframed; deferred row dropped.
- **`adr-author@0.1.1`** — anti-trigger fallback for threat-model /
  change-request fully aligned with the user-invocable peer pattern;
  References reframed; deferred row dropped.
- **`runbook-author@0.1.1`** — out-of-scope vs deferred re-framing
  (launch-comms, hypercare-digest, weekly-metric-report belong to
  the future site-operate family, not "deferred in this family");
  References reframed; deferred row dropped (B7).
- **`baseline-report-author@0.1.1`** — out-of-scope vs deferred
  re-framing (5 referenced siblings); cross-family Handoffs to
  optimization-backlog-author / optimization-loop reframed as future-
  site-operate-family pointers; References reframed; deferred row
  dropped (B7).
- **`site-build@0.1.1`** (router) — Routing Table no longer lists
  deferred Tier 2/3 atoms (10 of 16 rows dropped); deferred atoms
  remain in "Atoms in This Family" + `taxonomy.md`; Disambiguation
  Protocol covers the user-invocable fall-back (B8).

### Health

All 7 skills remain `healthy` post-edit. Drift gate: vision-author
0.0%, persona-author 4.2%, srs-author 8.8%, adr-author 6.7%,
runbook-author 8.3%, baseline-report-author 3.2%, site-build 3.3%.

### Notes

- Self-review surfaced these issues *before* the first real-use
  signal would have. Per `MAINTENANCE.md`, this is the right kind
  of pre-friction signal — descriptions and anti-triggers are
  cheap to revise pre-friction; cheap to revise *post*-friction
  in PATCH bumps; expensive to revise once consumers depend on
  them.

---

## [0.1.1] - 2026-05-08

### Added — site-build family (router + 6 Tier 1 atoms)

Authored via `family-bootstrap` Stages 1-4 (delegating to `skill-author`
× 7) during the v0.7.0 first-real-consumer dogfood. Closes part of P6
in `../context-meta-pipeline/docs/PATH-TO-V1.md`.

- **`site-build`** (router, v0.1.0) — per-family router; Routing Table
  covers 6 Tier 1 atoms; Tier 2/3 listed as Specced, Not Yet Built.
- **`vision-author`** (atom, v0.1.0) — Phase 1 — Vision & Value
  Proposition document per SOP §4.2.5.
- **`persona-author`** (atom, v0.1.0) — Phase 1 — evidence-backed
  persona per audience segment per SOP §4.2.3.
- **`srs-author`** (atom, v0.1.0) — Phase 2 — SRS scaffold with FR +
  NFR per SOP §5.1.
- **`adr-author`** (atom, v0.1.0) — cross-phase — single architectural
  decision record per SOP §5.3.6.
- **`runbook-author`** (atom, v0.1.0) — Phase 5/6 — deployment /
  incident / launch runbook per SOP §8.8 + §9.3.
- **`baseline-report-author`** (atom, v0.1.0) — Phase 7 — T+8-week
  baseline report per SOP §10.2.1.

All 7 pass `validate-metadata.py`. Router has expected "Tier 2/3 atoms
not yet authored" warning per the deferred-atom convention.

### Notes

- 5 Tier 2 atoms (kpi / risk-register / threat-model / privacy-plan /
  master-schedule) declared in `skills/site-build/taxonomy.md` as
  Specced, Not Yet Built. Build trigger: a real Phase-2 project
  needs the conformant skill.
- 5 Tier 3 atoms (ost / stakeholder-map / design-philosophy /
  weekly-metric-report / change-request) declared in taxonomy.md
  with their own observable build triggers.
- 21 capabilities outside the family's spine are deferred to future
  `site-design` and `site-operate` families per
  `coverage.md` Out of Scope.

---

## [0.1.0] - 2026-05-08

### Added

- Library scaffolded via `library-bootstrap` (context-meta-pipeline
  v0.7.0). First real consumer library of the meta-pipeline; closes
  build trigger on `library-bootstrap`'s deferred row.
- `.claude-plugin/plugin.json` (v0.1.0).
- Marketplace row added to `../.claude-plugin/marketplace.json`.
- Empty `SNAPSHOT.lock`, schema-valid `coverage.md` (no-skills
  stub), inherited `governance/INDEX.md`, `README.md`, operational
  scaffolding (Makefile, verify.sh, requirements.txt, .gitignore,
  CONTRIBUTING.md, LICENSE, CI workflow).
- `.bootstrap/library-intake.yaml` retained as bootstrap provenance.

### Notes

- This is a fresh library with zero skills. Next step: bootstrap
  the first family via `family-bootstrap` (the `discovery` family
  is queued; its trigger fires when the first Phase-1 deliverable
  needs a conformant skill).
- All findings produced during the bootstrap walkthrough are
  recorded in `coverage.md` under the audit-finding ledger
  (B-prefixed IDs) and cross-referenced into the meta-pipeline's
  ledger (A57+) since this is the first-real-consumer dogfood.
