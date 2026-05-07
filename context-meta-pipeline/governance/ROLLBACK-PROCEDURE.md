# Rollback Procedure

When a skill ships broken — wrong behavior, failing tests, breaking dependents — you need a procedure to restore the previous working state. Without a procedure, rollback becomes ad-hoc and dangerous.

This document specifies how to roll back a single skill, multiple coordinated skills, and the library snapshot.

---

## When to Roll Back

Roll back when ANY of these are true:

- A skill's tests started failing after a recent release.
- A skill's triggering accuracy dropped below 85% after a description change.
- Downstream skills (routers, orchestrators) started failing because of a dependency change.
- A user reports the skill produces materially worse output than the previous version.
- A security issue is discovered in the latest version.

Do NOT roll back for:

- Stylistic preferences ("I liked the old description better").
- Edge cases that always failed (rolling back doesn't fix them).
- Performance regressions under 20% (use a hotfix, not rollback).

---

## Rollback Levels

Three scopes, each with its own procedure.

### Level 1: Single skill rollback

Use when one skill broke and nothing else is affected.

Procedure:

1. Identify the last known-good version from the library snapshot.
2. Revert the skill's directory to that version's state. This means restoring the SKILL.md, its references, and its scripts to the prior version.
3. Update the skill's `metadata.changelog` with a rollback entry: "Rolled back to v1.4.2 due to [reason]. Previous v1.5.0 is no longer recommended; users with explicit pins to v1.5.0 should investigate the issue before pinning to a new version."
4. Update the library `CHANGELOG.md` with a rollback entry.
5. Update the library snapshot to reflect the rolled-back version.
6. Notify dependents (routers that dispatch to this skill) that the rollback occurred.

The original v1.5.0 is preserved in git history. It is not deleted. Users who explicitly pinned to v1.5.0 in their lockfile continue to get v1.5.0 — they accepted that risk by pinning.

### Level 2: Coordinated multi-skill rollback

Use when a lock-step release introduced breakage and multiple skills need to revert together.

Procedure:

1. Identify the last known-good library snapshot.
2. Revert all skills involved in the lock-step release to their state in that snapshot.
3. Update each skill's `metadata.changelog` with a coordinated rollback entry referencing the others.
4. Update the library `CHANGELOG.md` with a single coordinated rollback entry listing all affected skills.
5. Update the library snapshot.
6. Notify dependents across the entire lock-step group.

Coordinated rollbacks are higher risk than single-skill rollbacks. Verify the rollback target snapshot was actually working before reverting — don't roll back to an even older broken state.

### Level 3: Full library snapshot rollback

Use only when something has gone systemically wrong — many skills broken, library snapshot corrupted, or a cascading failure.

Procedure:

1. Identify a known-good prior snapshot (likely days or weeks old).
2. Restore all skills to their state in that snapshot.
3. Document what changed between the broken snapshot and the rollback target in CHANGELOG.md.
4. Notify all maintainers that the rollback occurred.
5. Do not delete the broken snapshot — it's needed for forensics.

Full library rollback should be rare. If you find yourself doing it more than once a year, the issue is upstream (in the release process, the validation gates, or the testing) and that's where to focus.

---

## What "Last Known Good" Means

The library snapshot is the source of truth. A snapshot is "known good" when:

- All skills in it pass their own tests.
- All routing accuracy checks pass.
- All metadata validation passes.
- No skill in it has a flagged health-check failure.

When you ship a new version of a skill, the library snapshot is updated to reflect the new state. If that update is the source of breakage, the prior snapshot is your rollback target.

---

## User Pin Behavior During Rollback

When a skill is rolled back from v1.5.0 to v1.4.2:

- Users with `git-history-rewriting@1.4.2` in their lockfile: unaffected. They were already on v1.4.2.
- Users with `git-history-rewriting@1.5.0` in their lockfile: also unaffected. They explicitly pinned to v1.5.0 and continue using it. They should investigate the issue before any future updates.
- Users with no pin (always-latest): get v1.4.2 on their next sync.

The point of "user pins for old versions" is exactly this: rollback is non-disruptive for users who pinned, automatic for users who didn't.

---

## Rollback Communication

A rollback must produce three artifacts:

### 1. CHANGELOG entry

Library-level CHANGELOG.md gets a rollback entry under today's date:

```markdown
## 2026-05-06

### Rolled back
- `git-history-rewriting` v1.5.0 → v1.4.2 (rebase logic regressed; investigation ongoing)
  - Affects: `git` router (no description change required)
  - Users with explicit pins to v1.5.0: investigate before updating
```

### 2. Skill-level changelog

The skill's own `metadata.changelog` field gets the rollback entry:

```yaml
changelog: >
  v1.5.0 (rolled back, 2026-05-06) — rebase logic regression on multi-parent merges.
  v1.4.2 (current) — restored as canonical version pending investigation.
  v1.4.2 (original) — last known-good before regression.
```

### 3. Notification to dependents

Routers that dispatch to the rolled-back skill receive a notification (per the change-notification policy in GOVERNANCE.md). The notification names:

- The rolled-back skill.
- The version that was rolled back FROM and TO.
- Any router-level changes required (typically none for a pure rollback).

---

## After Rollback

A rollback is not the end. Within 1 week of a rollback:

1. Investigate the root cause of the regression.
2. Determine if the issue is fixable (yes → ship a v1.5.1 or v1.6.0 with the fix; no → mark v1.5.0 as a known-bad version permanently).
3. Update the skill's evaluation suite to catch the issue that caused the regression.
4. Document the lessons learned in the library `CHANGELOG.md` under a "Rollback Postmortems" section.

This is how the library learns. A rollback without a postmortem is debt accumulating.

---

## What Rollback Does NOT Do

- It does not delete the broken version. v1.5.0 stays in git history and remains pinnable. Users who explicitly pinned to it continue to get it.
- It does not retroactively fix dependents that broke during v1.5.0's brief lifetime. If a router updated its description to match v1.5.0's behavior, the rollback may require the router to update again.
- It does not bypass the breaking-change detection check. A rolled-back skill that's effectively reverting to an older version is still a version change and goes through the normal release procedure.

---

## Implementation Notes

Rollback is partly automated and partly procedural. The git operations are standard (`git revert`, `git checkout`). The rest is communication and snapshot management.

`scripts/rollback-skill.py` (Python 3, PyYAML + stdlib + subprocess) automates Level 1 single-skill rollback: restoring SKILL.md and references via `git checkout`, prepending the rollback entry to the skill's `metadata.changelog`, and updating both `SNAPSHOT.lock` and the library `CHANGELOG.md`. Levels 2 (coordinated multi-skill) and 3 (full library snapshot) remain procedural — the blast radius and forensic requirements are too case-specific to safely automate. Tooling supports the procedure; it doesn't replace it.
