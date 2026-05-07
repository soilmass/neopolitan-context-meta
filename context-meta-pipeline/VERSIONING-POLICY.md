# Versioning Policy

How versions work in this library. Specifies SemVer application to skills, the latest-only support model, user pin behavior, and migration guides.

---

## Semantic Versioning

Every skill follows MAJOR.MINOR.PATCH semantic versioning. The version lives in the skill's frontmatter under `metadata.version`.

### MAJOR (X.0.0)

Increments when a breaking change ships. A change is breaking if it forces dependents to update — see `/governance/BREAKING-CHANGE-DETECTION.md` for the full catalog.

Examples:
- A capability is removed from an atom (`revert` removed from `git-history-rewriting`).
- A capability moves between atoms (`stash recovery` moved from `git-basics` to `git-recovery`).
- A required section is removed from a skill's body.
- A router changes the target atom of an existing routing table entry.
- A frontmatter field that downstream skills depend on changes (e.g., `name`, removed `allowed-tools`).

### MINOR (X.Y.0)

Increments when functionality is added without breaking dependents.

Examples:
- A new capability is added to an atom's `Capabilities Owned` list.
- A new entry is added to a router's routing table.
- A new section is added to a skill's body.
- An optional frontmatter field is added.

### PATCH (X.Y.Z)

Increments for backward-compatible fixes.

Examples:
- A typo in the description is corrected.
- A clarification is added without changing the meaning.
- A reference file is reorganized without changing what it documents.
- A skill's evaluation suite is improved.

---

## Latest-Only Support

The library supports the latest version of every skill. Older versions are not maintained.

When a skill ships v2.0.0 with breaking changes, v1.x receives no further updates. No security patches, no bug fixes, no description tweaks. The version is frozen in git history exactly as it was the day v2.0.0 shipped.

This is a deliberate trade. The cost is that users who can't immediately migrate are stuck on a fixed version. The benefit is that the library does not carry the maintenance burden of N-1, N-2, or N-3 support windows. With ~50 skills, even N-1 support would mean maintaining 100 versions.

---

## User Pins

Users who need to stay on an older version pin explicitly. Pin syntax (in the user's own consuming environment) is implementation-dependent — typical forms:

```
git-history-rewriting@1.4.2
family-bootstrap@2.0.0
```

A pinned skill installs from git history at the named version. The library makes no guarantees about pinned skills:

- They may have unpatched bugs.
- They may have unpatched security issues.
- They may not work with the current versions of skills they depend on.

Users who pin accept those risks. The library does not warn at pin time, but the pinned skill's `metadata.changelog` documents what was wrong with that version (if anything was wrong) and what the user is missing by not updating.

When a user pins to a version that was rolled back (see `/governance/ROLLBACK-PROCEDURE.md`), the pinned skill's changelog flags this prominently. The user has chosen a version the library considers broken; that choice is their own.

---

## Migration Guides

Every MAJOR version bump produces a migration guide. The guide is auto-generated from a structural diff and reviewed by the author before shipping.

### Auto-generation

A script compares the v1.x and v2.0 versions of the skill's SKILL.md and references. It produces a draft migration guide naming:

- Frontmatter changes (renamed fields, removed fields, type changes).
- Section changes (removed sections, restructured sections, renamed sections).
- Capability changes for atoms (added, removed, moved, contract changes).
- Routing changes for routers (added entries, removed entries, target changes).
- Reference file changes that affect the skill's external surface.

The draft is structured but generic. Example output:

```markdown
# Migration: git-history-rewriting v1.4.2 → v2.0.0

## Removed capabilities

- `revert` is no longer owned by this skill. It moved to `git-recovery`.
  - Update: change references from `git-history-rewriting` to `git-recovery` for revert operations.

## Section changes

- The `Edge Cases` section was restructured into three subsections.
  - No action required for downstream skills.

## Frontmatter changes

- None.
```

### Author review

The author adds context the diff cannot infer:

- Why the change was made.
- What problem it solves.
- Specific examples of code or prompts that need updating.
- Known incompatibilities the diff missed.
- Suggested timeline if users want to delay migration (knowing they'll be on a frozen version).

The reviewed migration guide ships at `<skill-directory>/MIGRATION-v<NEW>.md`. The library `CHANGELOG.md` links to it. The skill's `metadata.changelog` references it.

---

## Version Field in Frontmatter

The `metadata.version` field is required on every skill (per `/governance/METADATA-VALIDATION.md`).

```yaml
metadata:
  version: "1.4.2"
  changelog: >
    v1.4.2 — patch: clarified disambiguation protocol example.
    v1.4.0 — minor: added bisect routing entry.
    v1.3.0 — minor: added stash recovery cross-reference.
    v1.0.0 — initial.
```

The changelog field is human-readable prose. It is not machine-parsed for the library `CHANGELOG.md` — the library CHANGELOG is authored separately and is the canonical source for cross-skill change tracking.

---

## When to Bump

The breaking-change detector (specified in `/governance/BREAKING-CHANGE-DETECTION.md`) determines when a MAJOR bump is required. The detector runs on every PR.

If the detector flags a breaking change but the version bump is MINOR or PATCH, the PR fails. The author either bumps to MAJOR (and authors the migration guide, updates dependents lock-step, etc.) or restructures the change to be non-breaking.

MINOR and PATCH bumps are author-discretion. The detector does not enforce them, but the metadata validator checks that the version increased monotonically from the prior release.

---

## What This Document Does Not Cover

- Specific breaking-change detection rules: see `/governance/BREAKING-CHANGE-DETECTION.md`.
- Rollback procedures when a release goes wrong: see `/governance/ROLLBACK-PROCEDURE.md`.
- Health-check thresholds for retiring versions: see `/MAINTENANCE.md`.
- Cross-skill compatibility (lockfiles, library snapshot): see `/GOVERNANCE.md`.
