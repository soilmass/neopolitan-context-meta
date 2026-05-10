# MIGRATION-v1.md — `context-site-build` v1.0.0

> **Note**: this is the migration document for the v0.6.1 → v1.0.0
> bump. v1.0.0 is the schema-freeze boundary; v1.0.x and v1.x.y
> after this point are bound by the v1.0 freeze contract documented
> in `docs/VERSIONING-POLICY.md`.

---

## What v1.0 means for consumers

`context-site-build` v1.0.0 is the first version with a **frozen
schema commitment**. Specifically:

1. **Family count and roster**: 3 families
   (`site-build`, `site-design`, `site-operate`). Adding or removing
   a family will be a v2.0.0 MAJOR bump.
2. **Archetype set used**: `atom`, `tool`, `router`, `policy`. New
   archetypes added at v2.0+.
3. **Atom naming convention**: `<deliverable>-author`. Deviations
   require an ADR documenting why.
4. **Overlay naming convention**: `house-<family>-<aspect>` (4
   segments, regex cap). New stack overlays continue the convention.
5. **Frontmatter required keys**: `name`, `description`, `license`,
   `metadata.version`, `metadata.archetype`, `metadata.changelog`.
6. **Per-family `coverage.md` schema**: sections required per
   meta-pipeline `governance/COVERAGE.md`.
7. **Cross-family handoff vocabulary**: documented in both directions.

## What's NOT frozen

- **Atom content** can grow MINOR after v1.0.
- **Reference docs** can be added/refactored as PATCH after v1.0.
- **Overlay scope** can land MINOR (e.g., new stack combos).
- **Cross-cutting tool atom additions** land MINOR.
- **Documentation** lands PATCH.

## Migration from v0.6.1 → v1.0.0-rc1

For consumers tracking this library, the v0.6.1 → v1.0.0-rc1 step is
**zero-breaking** — no SKILL.md content removed, no behavior changes,
no schema breaks. The bump is a commitment ceremony, not a content
delta.

### What changed in v1.0.0-rc1

- `snapshot_version`: 0.6.1 → 1.0.0-rc1.
- All 75 skills: `health` field set to `healthy` via the `audit-
  skill.py --all --write-health` ritual (previously a mix of
  `fresh` and `healthy` from prior PR audits).
- 14 skill descriptions tightened in the pre-v1.0 audit pass to
  pass the description-drift gate at <10%; per-skill versions stay
  at v0.1.0 because the changes are description-text-only.
- `MIGRATION-v1.md` (this file) authored.

### What v1.0.0-rc1 promises

- 30-day stability hold before promoting rc1 → v1.0.0.
- During the hold: any newly-discovered B-series finding affecting
  schema discipline (not content quality) restarts the hold clock.
- Promotion to v1.0.0 happens when:
  - 30 days elapsed without a MAJOR bump.
  - Zero new B-series findings affecting frozen schema.
  - `audit-skill.py --all` returns zero findings for 3 consecutive
    runs (per meta-pipeline `docs/PATH-TO-V1.md` adapted to this
    library).

### Migration from v0.6.1 → v1.0.0

For consumers tracking the rc1 → v1.0.0 promotion: **zero changes**.
v1.0.0 is the same content as v1.0.0-rc1 with the version bumped
and the freeze fully in effect.

If during the 30-day hold a MAJOR bump becomes necessary (e.g., a
schema discipline gap surfaces that warrants a structural change),
the rc1 candidacy fails and a new rc-candidate is cut at the
appropriate version.

## Migration from v1.0.0 to future v2.0+

This is documented at the time of the v2.0+ MAJOR bump per the
meta-pipeline's `skill-migrate` Stage 1-4 procedure. Specifically:

1. **`MIGRATION-v2.md`** authored documenting the breaking change.
2. **30-day deprecation window** before v2.0+ tag.
3. **Per-affected-consumer migration path** documented.
4. **Frozen v1.0+ tag** remains pullable for consumers needing more
   time.

## Cross-references

- `docs/VERSIONING-POLICY.md` — full v1.0 freeze contract.
- `docs/GETTING-STARTED.md` — onboarding for new consumers post-
  v1.0.
- `docs/LIBRARY-MAP.md` — dependency graph at v1.0 freeze.
- `coverage.md` — audit-finding ledger including B9 (v0.5.0–v1.0.0
  ahead-of-trigger window) and B10 (the audit-pass drift discipline
  documented during v1.0-rc1 authoring).
- `context-meta-pipeline/skills/skill-migrate/SKILL.md` — the parent
  procedure that authored this document.
- `context-meta-pipeline/docs/PATH-TO-V1.md` — the parent document
  defining v1.0 prerequisites adapted to this library.

---

*Authored 2026-05-09 via `skill-migrate` Stage 1-4 procedure as part
of the v0.6.1 → v1.0.0-rc1 release commit.*
