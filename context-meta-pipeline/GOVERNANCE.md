# Governance

Operational rules for the skill library. Specifies dependency model, change notifications, lock-step upgrades, audit trails, and the discipline that keeps a 50-skill ecosystem coherent.

This document covers the cross-cutting rules. Specific procedures (breaking-change detection, metadata validation, rollback) live in `/governance/` with an INDEX.md that maps the full layer.

---

## Skill Archetypes and Their Documentation

Every skill is exactly one archetype. The archetype determines required documentation sections, validated at merge time.

The five archetypes are: Atom, Tool, Router, Orchestrator, Policy. Required sections per archetype are specified in `/governance/METADATA-VALIDATION.md`.

When a skill is "and" of two archetypes, it is two skills. The validator does not enforce this directly — it requires reviewer judgment — but the architecture treats archetype mixing as a refactor signal.

---

## Dependency Model

Skills declare what they depend on at one place — `SNAPSHOT.lock` at the library root — at two levels of detail.

**Per-skill `depends_on` entries.** Each skill that programmatically depends on other skills lists them in its `SNAPSHOT.lock` block under `depends_on:`, naming exact versions. This per-skill list is the skill's contract with its dependencies — if `family-bootstrap`'s entry declares `skill-author@1.4.2`, that pin holds until the entry is updated. This is the mechanism `scripts/detect-breaking-changes.py` reads to find dependents of a changed skill.

**Library snapshot itself.** The same `SNAPSHOT.lock` file pins the last known-good state of *every* skill in the library together via the top-level `skills:` map. The snapshot answers "what versions of all skills work together?" It updates on coordinated releases and is the rollback target when something goes wrong.

The two views work together: per-skill `depends_on` entries give per-skill version intent, the snapshot's `skills:` map gives system-level coherence. Neither view alone is sufficient.

A separate per-skill `lockfile.yaml` file or `metadata.lockfile` frontmatter field is a deferred concern. It would only be needed if per-skill dependency declarations had to live alongside the SKILL.md (e.g., for distribution outside the library snapshot). Currently (and through every v0.x release shipped so far), `SNAPSHOT.lock` `depends_on:` is the canonical mechanism.

---

## Lock-Step Upgrades

When a skill's breaking change requires another skill to update, both skills release together as a lock-step pair (or larger group). Partial states are not allowed.

**Detection.** A CI check (specified in `/governance/BREAKING-CHANGE-DETECTION.md`) analyzes every PR that bumps a skill's MAJOR version. If the bump touches a capability that other skills depend on, the check fails until the dependents are updated in the same PR (or a coordinated PR series).

**No backwards-compatibility windows.** The library runs latest-only. When skill A v2.0 ships with breaking changes, all skills that depend on A are also updated. There is no "support v1.x for 6 months" period — if you skip an upgrade, you skip it for good.

**User pins.** Users who want to stay on an older version of a skill pin explicitly in their own lockfile. The library does not maintain old versions, but it does not delete them from git history. Pinned versions remain installable; they just don't get updates.

---

## Change Notifications

When a skill ships breaking changes, only **routers** that dispatch to that skill receive automatic notifications.

The reasoning: routers are the integration points. An atom that gets refactored may rename its capabilities or shift its scope; the router that dispatches to it must update its routing table and description. Other atoms in the same family don't need to know — they don't reference each other directly.

Notification is a CI artifact, not a runtime event. When the breaking-change detector flags a router as affected, the PR description names the router and the required updates. The router's maintainer (under implicit-ownership rules — see `/MAINTENANCE.md`) handles the update.

Tools, orchestrators, and policy overlays that depend on a changed skill are not auto-notified. They are expected to track changes via the library `CHANGELOG.md`.

---

## Self-Contained Library

The library does not depend on external skill libraries. It does not reference Anthropic's public skills (`pdf`, `docx`, etc.) or any third-party skill catalog.

When a capability provided by an external skill is needed, a new internal atom is authored. This is more work upfront and produces more total skills, but it eliminates entire classes of failure: external versioning, external deprecation, external availability, external trust.

If a future decision reverses this, the gap is documented and a new governance doc covers external-skill version pinning.

---

## CHANGELOG and Audit Trail

The library maintains a single `CHANGELOG.md` at the root. Every notable change to any skill produces an entry. The format groups entries by date and categorizes them by type.

```markdown
## 2026-05-06

### Breaking
- `git-history-rewriting` v2.0 — `revert` moved to `git-recovery`
  - Affects: `git` router (anti-trigger updated, routing table updated)
  - Migration guide: /git-history-rewriting/MIGRATION-v2.md

### Added
- `git-hooks` v1.0 — split from `git-config`
- `git-submodules` v1.0 — split from `git-collaboration`

### Deprecated
- `filter-branch` references in `git-history-rewriting` — use `filter-repo` going forward

### Health
- `building-website-specs` flagged unhealthy (test pass rate 78%, threshold 90%)
- `git-recovery` description updated for clarity (no version bump)

### Rolled back
- `git-history-rewriting` v1.5.0 → v1.4.2 (regression in multi-parent merges)
```

Categories: Breaking, Added, Changed, Deprecated, Removed, Health, Rolled back, Security.

Skills do not maintain their own CHANGELOG.md files. The skill's `metadata.changelog` field captures version history; the library CHANGELOG aggregates across skills. Two changelog files per skill is duplication.

---

## Cross-References Between Skills

Skills reference each other in three ways. Each is governed differently.

**Handoff references in body prose.** A skill says "see `git-recovery` for reflog operations" inline. These are tracked through the SKILL.md text and validated weakly — the validator checks that named skills exist in the library, but the prose itself is human-authored.

**Routing table entries.** A router lists atoms by name in a structured table. The validator checks that every named atom exists, that every atom in the family appears in the table or in deferred-tier documentation, and that the routing table format is consistent.

**Snapshot `depends_on` entries.** Tools and orchestrators that programmatically depend on other skills declare versions in their `SNAPSHOT.lock` block under `depends_on:`. These entries are first-class system objects — they drive lock-step detection (via `scripts/detect-breaking-changes.py`), change notifications, and dependency resolution.

---

## Adding a New Skill

When a skill enters the library:

1. The skill passes metadata validation (see `/governance/METADATA-VALIDATION.md`, implemented at `scripts/validate-metadata.py`).
2. The skill's archetype is named in its location (under `skills/`) or a `metadata.archetype` field.
3. If the skill is in an existing family, the family's `coverage.md` is updated.
4. If the skill is in a new family, a `coverage.md` is created.
5. The library snapshot is updated.
6. A `CHANGELOG.md` entry is added under "Added".
7. Routers that should dispatch to the new skill are updated.
8. The audit ritual is run: any siblings with overlapping description keywords get anti-triggers added.

The canonical path through these eight steps is `skill-author` Stage 4 (or `family-bootstrap` Stage 6 for whole families) — the lifecycle skills exist precisely to enforce this procedure as a tool rather than a checklist. A pre-merge procedural fallback remains documented for cases where the lifecycle skills are unavailable, but is the exception.

---

## Removing a Skill

Skills are not removed. They are unmaintained, abandoned, or replaced.

When a skill stops being useful, the recommended path is to mark it unhealthy via the threshold-gate system (see `/MAINTENANCE.md`) and let the auto-warn mechanism communicate that to users. The skill remains installable for users who explicitly pin to it.

When a skill is replaced by a more comprehensive alternative, the old skill stays in git history but disappears from the library snapshot. Users who pinned to it can still install it; users who didn't migrate to the replacement.

The library does not delete skills. Deletion creates surprises for pinned users; staleness is communicated through health checks instead.

---

## What This Document Does Not Cover

- Per-skill versioning rules (what counts as MAJOR/MINOR/PATCH): see `/VERSIONING-POLICY.md`.
- Maintenance, ownership, and health checks: see `/MAINTENANCE.md`.
- Specific operational procedures (breaking-change detection, metadata validation, rollback): see `/governance/INDEX.md` for the full map.
- Library architecture (archetypes, layering, naming): see `/ARCHITECTURE.md`.
