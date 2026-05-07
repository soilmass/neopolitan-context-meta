# Governance Index

The governance layer specifies how the skill library operates: how skills are versioned, validated, deprecated, rolled back, and maintained. This index maps the documents in `/governance/` to the concerns they address, and is honest about what exists versus what is deferred.

The library architecture itself lives in `/ARCHITECTURE.md` at the library root. This index covers the operational layer that sits on top of the architecture.

---

## Currently Documented

These eleven documents are authored and ready to enforce. The first three cover the load-bearing concerns at v0.1.0; the next seven were authored at v0.5.0 to claim the surface area, with each one disclaiming pre-trigger applicability where appropriate; the eleventh (`EXTENSION-POINTS.md`) was authored at v0.6.0 to make the library's existing extension seams explicit.

### `BREAKING-CHANGE-DETECTION.md`

Specifies what counts as a breaking change, how the CI check identifies them from a SKILL.md diff, and what the check requires before a breaking change can merge. Without this document, the "lock-step upgrade" rule in GOVERNANCE.md cannot be enforced — breaking changes slip through as MINOR or PATCH bumps, breaking the SemVer contract for downstream skills. Implemented at `/scripts/detect-breaking-changes.py`.

### `METADATA-VALIDATION.md`

Specifies the structural requirements every SKILL.md must satisfy: frontmatter fields, body length, archetype-specific required sections, naming conventions. Validates on every PR and during periodic audits. Without this document, frontmatter drift accumulates silently — descriptions get too long, required sections disappear, and the skill discovery layer (LLM matching against descriptions) degrades. Implemented at `/scripts/validate-metadata.py`.

### `ROLLBACK-PROCEDURE.md`

Specifies how to revert a broken skill release at three levels: single-skill, coordinated multi-skill, and full library snapshot. Specifies what "last known good" means, how user pins behave during rollback, and what communication is required. Without this document, rollback is ad-hoc and dangerous — the wrong skills get reverted, dependents are not notified, and the broken state of the library is forgotten. Level 1 implemented at `/scripts/rollback-skill.py`; Levels 2-3 remain procedural.

### `INTEGRATION-TESTING.md` *(authored v0.5.0; **mechanizer built ahead-of-trigger v0.7.0**)*

Specifies the cross-skill testing procedure — scenarios, fixtures, runner — for when integration testing becomes load-bearing (10+ skills with cross-deps + 2 cross-skill regressions). Mechanizes Health Gate 2 (test pass rate >90%). Pre-trigger: Gate 2 reports explicit N/A. Implementation: `scripts/integration-test-runner.py` (deferred until trigger fires).

### `SKILL-DISCOVERABILITY.md` *(authored v0.5.0; **mechanizer built ahead-of-trigger v0.7.0**)*

Specifies tagging, domain hierarchy, search, and skill-index generation — the discoverability layer that supplements LLM description-matching at scale. Mechanizes Health Gate 3 (triggering accuracy >85%). Pre-trigger: Gate 3 reports explicit N/A; description-matching plus the `meta` router carries the load. Implementation: `metadata.tags` field + `scripts/search-skills.py` + `scripts/gen-index.py` (deferred until 50-skill trigger fires).

### `SKILL-PROVENANCE.md` *(authored v0.5.0; **mechanizer built ahead-of-trigger v0.7.0**)*

Specifies GPG signing of release tags, per-skill SHA-256 hashes in SNAPSHOT.lock, marketplace signature verification — authenticity verification for skills crossing trust boundaries. Pre-trigger: meta-pipeline is internal; provenance not load-bearing. Implementation: `scripts/snapshot-hash.py` + signed-tag enforcement in `release-tag.sh` (deferred until external distribution).

### `SECURITY-AUDIT.md` *(authored v0.5.0; pre-trigger N/A)*

Specifies audit logs, forensics, and pre-incident hardening — the security layer that pairs with `SKILL-PROVENANCE.md` for compliance. Pre-trigger: no skills touch credentials/production. Implementation: leverages git history + the four versioned ledgers (SNAPSHOT.lock, CHANGELOG.md, coverage.md, governance/INDEX.md) — no additional infra until trigger fires.

### `EMERGENCY-HOTFIX.md` *(authored v0.5.0; placeholder skeleton)*

Specifies the bypass procedure for security/critical bugs that can't wait for lock-step. Skeleton form — to be rewritten against the first real incident, retaining only the structural shape. Builds on `BREAKING-CHANGE-DETECTION.md` §"Bypass for Emergencies" and `ROLLBACK-PROCEDURE.md` §"After Rollback".

### `DEPRECATION-COMMUNICATION.md` *(authored v0.5.0; **mechanizer built ahead-of-trigger v0.7.0**)*

Specifies the four deprecation channels (CHANGELOG entry, in-description banner, dependent notification, sunset timeline). Channels 1–2 work today (in-house); Channels 3–4 become load-bearing when external consumers exist. Implementation: `scripts/notify-dependents.py` + `governance/notification-channels.yaml` (deferred until external consumers).

### `USAGE-ANALYTICS.md` *(authored v0.5.0; **rollup script built v0.7.0; telemetry hook STUBBED**)*

Specifies telemetry on which skills fire, dead-code detection, co-invocation patterns. Privacy-preserving (prompt hashes only, no content). Pre-trigger: 14 skills are inspectable directly; `audit-skill.py` recency gate covers dead-code detection adequately. Implementation: `scripts/telemetry-hook.py` + `scripts/analytics-rollup.py` (deferred until 25-skill trigger fires; partly blocked on Claude Code core load-hook support).

### `EXTENSION-POINTS.md` *(authored v0.6.0)*

Documents the five stable seams through which new skills, validators, health gates, and (future) archetypes extend the library. The seams existed before the doc; v0.6.0 makes them explicit so consumers do not re-discover them. §1 names the SKILL.md authoring seam; §2 names the validator interface contract; §3 names the `gate_<name>()` signature; §4 explicitly bars 6th-archetype authoring at v0.6.0 with a fail-as-expected fixture; §5 names the six artifact contracts (`SNAPSHOT.lock` / `coverage.md` / `SKILL.md` / `MIGRATION-v<N>.md` / `routing-eval.yaml` / `CHANGELOG.md`). Implemented by extension-seam fixtures at `/scripts/tests/fixtures/extension-seams/` exercised in `verify.sh` step 9. Cross-references `docs/PATH-TO-V1.md` for when these seams become immutable.

---

## Adjacent Implementation (Outside `/governance/`)

`/MAINTENANCE.md` lives at the library root, not under `/governance/`, but its Gates 1 (recency) and 4 (description drift) are mechanized in v0.2.0 by `/scripts/audit-skill.py`. The drift formula (asymmetric containment with prefix-based token matching) is pinned in `/skills/skill-audit/references/health-gates.md`. Gates 2 (test pass rate) and 3 (triggering accuracy) report explicit N/A pending the deferred infrastructure named below.

---

## Deferred (Authored When Needed)

After v0.5.0 moved seven previously-deferred docs to Currently Documented (each with a pre-trigger N/A disclaimer), one concern remains genuinely deferred — the library has not yet attempted any external publishing.

### `plugin-publish.md`

Specifies the procedure for publishing a plugin to a Claude Code marketplace beyond the author's own environment. Covers manifest validation against marketplace schema, signing requirements (intersect with `SKILL-PROVENANCE.md`), versioning conventions for public releases, sunset/deprecation across an external consumer base. **Build trigger**: first attempt to publish to a public Claude Code marketplace.

Currently the meta-pipeline ships only via the `neopolitan-context-meta` marketplace, which is internal. When a public marketplace publish becomes a goal, this document gets authored against the actual mechanics that emerge.

---

## Out of Scope

These concerns exist but the library has explicitly chosen not to address them.

### Cross-library version pinning

The library is self-contained — no external skill dependencies (per Decision 14 in GOVERNANCE.md). This means there is no concern about pinning external skill versions. If this changes, the gap is documented here for future authoring.

### Multi-team ownership

The library uses implicit ownership (last-toucher is responsible) — there is no formal ownership tracking, CODEOWNERS file, or maintainer rotation. If the library scales to multiple teams or external contributors, ownership tracking would need to be added.

### Skill marketplace mechanics

The library is internal, not a public marketplace. Curation policies, contributor onboarding, license management, and similar marketplace concerns are out of scope. If the library is ever published externally, these concerns surface and need their own governance documents.

---

## Reading Order

For someone new to the library:

1. Start with `/ARCHITECTURE.md` for the system design.
2. Read `/GOVERNANCE.md` for the operational decisions.
3. Read `/VERSIONING-POLICY.md` for how versions and pins work.
4. Read `/MAINTENANCE.md` for ownership and health.
5. Read this index.
6. Read the three load-bearing governance docs (`BREAKING-CHANGE-DETECTION.md`, `METADATA-VALIDATION.md`, `ROLLBACK-PROCEDURE.md`) in any order.
7. Skim the seven v0.5.0-authored docs (INTEGRATION-TESTING / SKILL-DISCOVERABILITY / SKILL-PROVENANCE / SECURITY-AUDIT / EMERGENCY-HOTFIX / DEPRECATION-COMMUNICATION / USAGE-ANALYTICS) to know what's specified for when their build triggers fire. Each is N/A pre-trigger.

For someone authoring a skill: the relevant docs are `METADATA-VALIDATION.md` (what the skill must include) and `BREAKING-CHANGE-DETECTION.md` (what counts as a breaking change when you bump versions).

For someone reviewing a PR: the three load-bearing docs apply, plus the archetype-specific section list from `METADATA-VALIDATION.md` to verify required sections are present.

For someone responding to a broken skill: `ROLLBACK-PROCEDURE.md` is the authoritative procedure.

For someone responding to a security incident: `SECURITY-AUDIT.md` (post-trigger) + `EMERGENCY-HOTFIX.md` (skeleton, to be rewritten against the real case) are the references — paired with `ROLLBACK-PROCEDURE.md` if rollback applies.

---

## Maintenance of This Index

When a deferred document is authored, move it from "Deferred" to "Currently Documented" with its summary. When a new concern emerges, add it to "Deferred" with a build trigger.

This index is the source of truth for the governance layer's scope. If a concern is not in this index, it is not addressed — and that absence is the failure mode the index exists to prevent.
