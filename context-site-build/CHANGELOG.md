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
