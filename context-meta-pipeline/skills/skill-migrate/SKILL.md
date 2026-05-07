---
name: skill-migrate
description: >
  Authors a MIGRATION-v<NEW>.md guide when a MAJOR version bump ships.
  Wraps migration-guide-gen.py to produce the structural diff, then the
  operator adds rationale, worked examples, known incompatibilities, and
  timeline. Per VERSIONING-POLICY.md every MAJOR bump produces one. Do
  NOT use for: PATCH or MINOR bumps (no migration guide required); the
  underlying breaking-change detection (use detect-breaking-changes.py
  via skill-refactor or directly); rolling back (use rollback-skill.py).
license: Apache-2.0
metadata:
  version: "0.1.2"
  archetype: tool
  tags: [lifecycle, rare]
  changelog: |
    v0.1.2 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy plus `references/migration-checklist.md` (speculative; pre-trigger disclaimer at top of each).
    v0.1.1 — patch: Stage 2 gate gains an explicit halt condition (A26): if
            migration-guide-gen.py produces an all-empty diff (Frontmatter +
            Capability + Routing + Section changes all empty), the skill
            halts and asks the operator to re-check the bump severity rather
            than synthesizing an inert guide. Surfaced by the v0.5.2 dogfood
            walkthrough.
    v0.1.0 — initial. Authored as part of v0.5.0 kitchen-sink meta-tooling release.
---

# skill-migrate

Authors the per-skill MIGRATION-v<N>.md guide that ships with every
MAJOR version bump.

## Purpose

Per `VERSIONING-POLICY.md` §"Migration Guides", every MAJOR bump
produces a migration guide. The guide is auto-generated from a
structural diff, then reviewed and extended by the author. This tool
is the procedural shell around that workflow:

1. Identify the old and new versions.
2. Run `migration-guide-gen.py` to produce the structural diff draft.
3. Operator adds rationale, examples, known incompatibilities, timeline.
4. Final guide ships at `<skill-directory>/MIGRATION-v<NEW>.md`.

## When to Use

- Every MAJOR version bump (X.Y.Z → (X+1).0.0).
- After `detect-breaking-changes.py` flags a breaking change AND the
  author bumped to MAJOR (the detector enforces this; this tool
  authors what the detector requires).
- When a refactor (`skill-refactor`) produces new skills that
  supersede an old one and the redirect note isn't enough.

## When NOT to Use

- For PATCH or MINOR bumps — those don't ship migration guides.
- For the breaking-change detection itself — use
  `scripts/detect-breaking-changes.py` (called by CI or directly).
- For rollbacks — `rollback-skill.py` handles Level 1; the rollback
  itself doesn't need a migration guide (the skill reverted to a
  previously-known version).
- For library-wide MAJOR bumps (snapshot 0.X → 1.0) — that's a
  release-note concern; use `skill-snapshot-diff` instead.

## Stage-Gated Procedure

Four stages.

### Stage 1 — Identify version pair

**Consumes:** the operator's prompt, the skill's git history, and the
current SKILL.md.

**Produces:** `migrate-target.yaml` containing
- `skill` — the skill being migrated
- `old_version` — the last MAJOR before this bump
- `new_version` — the new MAJOR
- `old_skill_md_ref` — git ref or path for the old SKILL.md
- `new_skill_md_path` — usually the current SKILL.md

**Gate:** new_version is a strict MAJOR bump from old_version (per
`VERSIONING-POLICY.md`); the old SKILL.md is fetchable.

### Stage 2 — Generate structural diff

**Consumes:** `migrate-target.yaml`.

**Produces:** the output of `scripts/migration-guide-gen.py --old <ref>
--new <path>` — a draft markdown file with sections for Frontmatter
changes, Capability changes (atoms), Routing changes (routers),
Section changes.

**Gate:** the script exits 0; the draft has at least one non-empty
section. **Halt condition (A26 — added v0.5.2):** if all four sections
(Frontmatter / Capability / Routing / Section changes) come back empty,
*halt the procedure* with an explicit message: "no structural changes
detected between `<old>` and `<new>` — this is not a MAJOR bump.
Re-run `scripts/detect-breaking-changes.py` to confirm; if it agrees,
the version bump is at most MINOR and a migration guide is not
required (see `governance/VERSIONING-POLICY.md` §"Migration Guides")."
The skill does NOT proceed to Stage 3 in that case — authoring author
context onto an empty diff produces an inert guide that pretends a
migration is needed when none is.

### Stage 3 — Add author context

**Consumes:** the Stage 2 draft.

**Produces:** an extended draft with these author-supplied sections:
- **Why this change** — rationale, problem solved.
- **Worked examples** — code or prompts that need updating.
- **Known incompatibilities** — anything the structural diff missed
  (behavioral changes, performance shifts, etc.).
- **Suggested timeline** — for users who want to delay (knowing
  they'll be on a frozen version per `GOVERNANCE.md`'s
  latest-only support model).

**Gate:** every section in the draft has substantive content;
no `<!-- TODO -->` markers remain.

### Stage 4 — Ship the guide

**Consumes:** the Stage 3 draft.

**Produces:**
- `MIGRATION-v<NEW>.md` at the skill's directory root.
- A reference from the skill's `metadata.changelog` to the migration
  guide.
- A reference from `CHANGELOG.md` `[<release>]` Breaking section to
  the migration guide path.

**Gate:** the migration guide file exists; the changelog references
resolve; `detect-breaking-changes.py` exits 2 (breaking detected with
proper handling, informational only).

## Dependencies

- `scripts/migration-guide-gen.py` — Stage 2.
- `scripts/detect-breaking-changes.py` — pre-existing; this tool's
  output complements its required-actions list.
- `VERSIONING-POLICY.md` §"Migration Guides" — the canonical source
  for migration-guide format and content.

## Evaluation

`skill-migrate` is correct when, run against a synthetic MAJOR bump
(e.g., a capability removal on a test atom), the resulting
MIGRATION-v<N>.md:

1. Names the removed / moved / renamed item explicitly.
2. Names the user-visible action ("update references from X to Y").
3. Has author rationale that goes beyond the structural diff.
4. References the changelog entry and is referenced from it
   (round-trip).

The first dogfood is whenever the meta-pipeline itself ships a MAJOR
bump on any of its skills, OR a consumer library ships its first
MAJOR. Until then, the tool is exercised against synthetic fixtures.

## Handoffs

- **From `skill-refactor` Stage 4** — refactor produces new skills;
  the source's MIGRATION-v<N>.md is authored via this tool.
- **From `skill-author`** — direct invocation when the author bumps
  MAJOR for any reason (capability removal, contract change).
- **From `detect-breaking-changes.py`** — the script's required-actions
  list points the operator at this tool.
- **To `skill-snapshot-diff`** — the migration guide path is referenced
  from the release notes.
