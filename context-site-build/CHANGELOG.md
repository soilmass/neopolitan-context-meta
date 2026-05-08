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
