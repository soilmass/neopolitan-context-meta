---
name: library-bootstrap
description: >
  Scaffolds a brand-new consuming library (sibling plugin to the
  meta-pipeline) — plugin manifest, marketplace.json row, SNAPSHOT.lock,
  coverage.md, governance/INDEX.md, README.md, scripts/, verify.sh,
  Makefile, CONTRIBUTING.md, LICENSE, .github/workflows. Build trigger:
  any consumer outside this plugin attempts to start a library. Do NOT
  use for: adding a domain family to an existing library (use
  family-bootstrap); republishing the meta-pipeline (out of scope per
  coverage.md); authoring a single skill (use skill-author).
license: Apache-2.0
metadata:
  version: "0.1.2"
  archetype: orchestrator
  tags: [composition, rare]
  changelog: |
    v0.1.2 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy.
    v0.1.1 — patch: added the three reference files this skill's body cites
            (A32/A33/A34 from v0.5.2 dogfood) — references/library-skeleton.md
            (full new-library template tree), references/plugin-manifest.md
            (plugin.json schema), references/marketplace-row.md (Stage 5
            marketplace.json edit pattern). v0.1.0 shipped the SKILL.md body
            with citations to these references but the files themselves were
            never authored — surfaced by the in-memory walkthrough.
    v0.1.0 — initial. Authored as part of v0.5.0 kitchen-sink meta-tooling release.
            Build trigger had not yet fired (no second consumer library exists);
            tool ships ahead of trigger to claim the surface area.
            Per the v0.5.0 risk assessment, "library-bootstrap risks the wrong
            abstraction" — the first real consumer dogfood will produce v0.5.x
            patches against this skill.
---

# library-bootstrap

The orchestrator that produces a brand-new consuming library —
sibling plugin to the meta-pipeline, with its own marketplace row,
plugin manifest, governance ledger, and operational scaffolding.

`family-bootstrap` produces a *family* (one domain) within an
existing library. `library-bootstrap` produces the *library itself*.

## Purpose

Bootstrap an entire new library so a consuming team can start
authoring families and skills the same day. The library inherits
the meta-pipeline's conventions (validators, archetype rules,
versioning policy) but gets its own snapshot, coverage, and
release lifecycle.

The output: a fully-scaffolded plugin directory ready for the team
to bootstrap its first family via `family-bootstrap`.

## When to Use

- Starting a brand-new consuming library (e.g., `context-git/`,
  `context-postgres/`, `context-frontend/`).
- When the meta-pipeline's deferred `library-bootstrap` row in
  `coverage.md` fires its trigger ("any consumer outside this plugin
  attempts to start a library").

## When NOT to Use

- For adding a family to an *existing* library — use `family-bootstrap`.
- For authoring a single skill — use `skill-author`.
- For republishing the meta-pipeline itself (e.g., to a public
  marketplace) — out of scope per `coverage.md`; see
  `governance/plugin-publish.md` (deferred) when authored.
- For forking or vendoring the meta-pipeline — that's a one-off
  manual operation.

## The Stages

Seven stages.

### Stage 1 — Library intake

**Consumes:** the operator's prompt naming the new library.

**Produces:** `library-intake.yaml` with
- `name` — bare name of the library (e.g., `context-git`).
- `parent_marketplace` — path to the marketplace.json that hosts it
  (e.g., `../.claude-plugin/marketplace.json`).
- `description` — one-paragraph what-the-library-is-for.
- `keywords` — array for plugin.json.
- `first_domains` — list of domains the library will eventually
  cover (informs the deferred section of coverage.md).

**Gate:** name passes `^[a-z][a-z0-9]*(?:-[a-z0-9]+){0,3}$`; the
parent marketplace.json exists; first_domains has ≥1 entry.

### Stage 2 — Plugin manifest

**Produces:** `<root>/.claude-plugin/plugin.json` with
`{name, version: "0.1.0", description, keywords, license: "Apache-2.0"}`.

**Gate:** JSON parses; required keys present.

### Stage 3 — Governance + ledger scaffolding

**Produces:**
- `<root>/SNAPSHOT.lock` with `snapshot_version: "0.1.0"` and an
  empty `skills:` map.
- `<root>/coverage.md` with the six required sections; "Domains
  Claimed" listing first_domains as deferred-with-trigger.
- `<root>/governance/INDEX.md` listing the three canonical
  governance docs as Currently Documented (referencing the
  meta-pipeline's), the seven optional ones as Deferred.
- `<root>/CHANGELOG.md` with `[Unreleased]` and `[0.1.0]` entries.
- `<root>/README.md` with library map + Where to Start.

**Gate:** every produced file parses; coverage.md passes
`coverage-check.py --schema library`.

### Stage 4 — Operational scaffolding

**Produces:**
- `<root>/Makefile` — same targets as the meta-pipeline (verify,
  validate, audit, lint, typecheck, install-deps, clean,
  coverage-check, snapshot-diff, dep-graph, release).
- `<root>/verify.sh` — same six-step structure.
- `<root>/requirements.txt` — `PyYAML>=6.0,<7`.
- `<root>/.gitignore` — Python + editor + caches.
- `<root>/CONTRIBUTING.md` — onboarding ramp.
- `<root>/LICENSE` — Apache-2.0 full text.
- `<root>/.github/workflows/verify.yml` — CI workflow.

**Gate:** every file present; `verify.sh` is executable.

### Stage 5 — Marketplace registration

**Produces:** an updated `parent_marketplace` JSON with a new
plugin row pointing at the new library's directory.

**Gate:** the parent marketplace.json parses; the new row's
version matches the new library's plugin.json version.

### Stage 6 — Reference the meta-pipeline

**Produces:** the new library's `governance/INDEX.md` references the
meta-pipeline's three canonical governance docs by relative or
absolute path. The new library does NOT re-author them; it inherits.

**Gate:** every governance reference resolves.

### Stage 7 — Verify

**Produces:** the output of `verify.sh` from the new library's
root. With zero skills authored, `validate-metadata.py --all`
reports zero skills (vacuously OK); `audit-skill.py --all`
reports zero skills; coverage-check passes; version triangulation
agrees.

**Gate:** new-library `verify.sh` exit 0.

## Skills Coordinated

- **`scripts/coverage-check.py`** — Stage 3 gate.
- **`family-bootstrap`** — the natural next step after this
  orchestrator finishes (the new library is ready for its first
  family).
- **`scripts/validate-metadata.py`** — invoked by Stage 7's verify.sh.

## Failure Modes

- **Stage 1 gate fails** (name conflicts, no parent marketplace).
  Halt; the operator picks a non-conflicting name or creates the
  parent marketplace first.
- **Stage 4 fails on file write** (permissions, etc.). Halt; the
  operator fixes the filesystem and re-runs from Stage 4.
- **Stage 5 fails** (parent marketplace.json malformed). Halt; the
  operator repairs the parent file before this stage applies.
- **Stage 7 fails** (verify.sh exits nonzero on the empty library).
  This is a meta-pipeline bug — file an issue against this skill.

## Handoffs

- **From the operator** — direct invocation when starting a new
  library.
- **To `family-bootstrap`** — the next step: bootstrap the library's
  first domain family.
- **To the meta-pipeline's `coverage.md`** — flip the
  `library-bootstrap` deferred row to "fired" once the first run
  completes.
