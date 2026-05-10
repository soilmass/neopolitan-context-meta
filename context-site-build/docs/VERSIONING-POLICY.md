# `context-site-build` versioning policy

This is the SemVer policy adapted from the meta-pipeline's
`governance/VERSIONING-POLICY.md`. The base rules carry over;
this document records this library's specific constraints +
the v1.0 freeze contract.

---

## Per-skill SemVer

| Bump | When |
|---|---|
| **PATCH** (0.X.Y → 0.X.Y+1) | Body / reference clarifications; description-text-only updates; non-behavior fixes; metadata.changelog entries; per-atom anti-trigger refinements (B6/A62 pattern) |
| **MINOR** (0.X.Y → 0.X+1.0) | New required-section content (additive); new references; expanded `Capabilities Owned` (no removals); new edge cases |
| **MAJOR** (0.X.Y → 0.X.Y+1, but with library impact) | Breaking change to a load-bearing section (description anti-trigger removed without successor; required-section schema change; archetype change) — these are rare |

Per-skill MAJOR bumps in pre-1.0 (currently) are pre-emptive — the
library is at v0.6.x; per-skill MAJOR bumps before library v1.0 are
**discouraged** because the schema isn't frozen yet.

---

## Per-library SemVer

The library version (in `plugin.json` + `marketplace.json` +
`SNAPSHOT.lock` `snapshot_version`) follows the meta-pipeline's
rules:

| Bump | When |
|---|---|
| **PATCH** | Documentation-only changes; no SKILL.md content changes; per-atom PATCH bumps (cumulatively) |
| **MINOR** | New skills (atoms / routers / overlays); new families; new references aggregated from multiple PATCH bumps |
| **MAJOR** | Breaking change to library structure (family removed; archetype taxonomy changed; schema for SKILL.md frontmatter or required sections changed in a way that breaks existing skills) |

Library MAJOR bumps in pre-1.0 are tracked but de-prioritized —
v0.x → v0.y across multiple MAJOR-shaped changes is the pre-1.0
norm. **After v1.0.0**, MAJOR bumps require a `MIGRATION-vN.md`
authored via `skill-migrate` and a 30-day deprecation window
(deferred until v1.0+ via the meta-pipeline's `skill-migrate`
discipline).

---

## v1.0 freeze contract

When this library hits v1.0.0 (planned PR #9 with a 30-day
stability hold between rc1 and final), the following commitments
go into effect.

### What's frozen at v1.0.0

1. **Family count and roster** — 3 families (`site-build`,
   `site-design`, `site-operate`); MAJOR bump required to add or
   remove a family.
2. **Archetype set used** — `atom`, `tool`, `router`, `policy`;
   no `orchestrator` archetype is used in this library at v1.0.0
   (the meta-pipeline ships orchestrators; this library does not).
3. **Atom naming convention** — `<deliverable>-author` is the
   canonical shape (e.g., `vision-author`, `runbook-author`).
   Deviations require an ADR + an explicit description of why the
   shape doesn't fit.
4. **Overlay naming convention** — `house-<family>-<aspect>` (4
   segments at the regex cap) for the v0.5.0 overlays. New
   overlays added in v1.x continue the convention.
5. **Frontmatter required keys** — `name`, `description`,
   `license`, `metadata.version`, `metadata.archetype`,
   `metadata.changelog`. `metadata.tags` and `metadata.recency_pin`
   remain optional but documented.
6. **Per-family `coverage.md` schema** — sections
   `## Domains Claimed` / `## Domains Deferred` / `## Domains Out
   of Scope` / `## Coverage Matrix Status` / `## Audit-finding
   ledger` are required.
7. **Cross-family handoff vocabulary** — "Handoffs to Other
   Skills" sections cite siblings by name; cross-family handoffs
   are documented in both directions.

### What's NOT frozen at v1.0.0

- **Atom content** — atoms can grow MINOR after v1.0 as new
  evidence surfaces (research papers, agency case studies, real-
  consumer feedback).
- **Reference docs** — references can be added / refactored /
  retired as PATCH bumps after v1.0.
- **Overlay scope** — new overlays can land MINOR (e.g., a new
  stack combo `house-site-build-solidstart` if SolidStart joins
  the canonical Awwwards stacks); existing overlays can be revised
  MINOR for new conventions.
- **Cross-cutting tool atoms** — additions land MINOR.
- **Documentation** (this `docs/` directory) — landlines PATCH
  always.

### How v1.0+ MAJOR bumps work

Per the meta-pipeline's `skill-migrate` procedure, every library
MAJOR bump produces a `MIGRATION-vN.md` documenting:

1. The breaking change(s).
2. The deprecation window (default 30 days).
3. The migration path per affected consumer.
4. The fallback (where applicable; a frozen v(N-1) tag remains
   pullable for consumers who need more time).

A library MAJOR bump after v1.0 also triggers:

- A signed Git tag (`v(N).0.0`) via `release-tag.sh`.
- A snapshot-diff report at the tag.
- A 30-day stability hold before the tag is recommended for new
  consumers.

---

## Pre-v1.0 versioning timeline (history)

| Version | Date | Notable |
|---|---|---|
| 0.1.0–0.1.2 | 2026-05-08 | Initial library + site-build Tier 1 + self-review |
| 0.2.0 | 2026-05-08 | site-build Tier 2/3 completion (10 new atoms) |
| 0.3.0 | 2026-05-08 | site-design family bootstrap (14 atoms + 1 router) |
| 0.4.0 | 2026-05-08 | site-operate family bootstrap (14 atoms + 1 router) |
| 0.5.0 | 2026-05-08 | Phase 4: 21 stack-specific policy overlays |
| 0.6.0 | 2026-05-08 | Phase 5: 7 cross-cutting tool atoms |
| 0.6.1 | 2026-05-09 | Phase post-Phase-5: v1.0-readiness documentation |
| 1.0.0-rc1 | (next PR) | Schema-freeze candidate; 30-day hold |
| 1.0.0 | (rc1 + 30 days) | Promotion if no MAJOR bumps + zero new B-series findings |

---

## How to read SNAPSHOT.lock for version info

```bash
# Library snapshot version
yq '.snapshot_version' SNAPSHOT.lock

# Per-skill versions
yq '.skills | to_entries | map(.key + " " + .value.version)' SNAPSHOT.lock

# Skills that depend on a specific version
yq '.skills | to_entries | map(select(.value.depends_on)) | .[] | .key + " → " + (.value.depends_on | join(", "))' SNAPSHOT.lock
```

---

## See also

- `context-meta-pipeline/governance/VERSIONING-POLICY.md` — the
  parent template this document specializes.
- `context-meta-pipeline/docs/PATH-TO-V1.md` — the meta-pipeline's
  own v1.0 path, which provides the discipline pattern for this
  library's v1.0 commitments.
- `coverage.md` — the audit-finding ledger (B-series) tracking
  this library's discipline shifts.
