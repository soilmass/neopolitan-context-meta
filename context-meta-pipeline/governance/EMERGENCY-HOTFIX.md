# Emergency Hotfix

**Build trigger:** the first time a security or critical bug in a
skill cannot be fixed within the normal release process. Per
`governance/INDEX.md`, "premature standardization here is worse than
no procedure — emergency procedures should be authored against real
cases."

**Pre-trigger applicability:** *None* — no emergency hotfix has been
needed at v0.5.0. This document is a placeholder skeleton; it will
be rewritten against the first real incident, retaining only the
shape sketched here.

---

## What an emergency hotfix is

A change that bypasses the normal release process because waiting
for the lock-step coordination would cause unacceptable harm.
Examples that *would* qualify:

- A skill is exfiltrating credentials via its hook scripts (active
  exploitation).
- A skill's `## Capabilities Owned` includes destructive operations
  that weren't intended (data loss in progress).
- A breaking-change detector misclassified a major bump and a
  consumer library is broken in production.

Examples that **do not** qualify (use the normal process):

- A drift gate failure (description mismatch).
- A test pass rate dipping below 90%.
- A skill flagged as "unhealthy" — the auto-warn banner already
  communicates the staleness; latest-only support means consumers
  who care can pin and skip.

## Bypass authorization

Per `governance/BREAKING-CHANGE-DETECTION.md` §"Bypass for
Emergencies", the detector can be bypassed only with:

- An explicit `[breaking-change-acknowledged]` tag in the commit
  message
- A sign-off from the library maintainer (today: implicit owner per
  `MAINTENANCE.md`)

The emergency-hotfix flow extends this:

- The bypass ALSO requires the operator to commit to filing a
  postmortem within 1 week (per
  `governance/ROLLBACK-PROCEDURE.md` §"After Rollback").
- The hotfix release ships as a PATCH with a `[hotfix]` tag in the
  CHANGELOG entry.
- The hotfix release is GPG-signed (per `SKILL-PROVENANCE.md`)
  even if normal releases aren't, so the bypass is auditable.

## Procedure (skeleton — to be filled in against the first real case)

1. **Triage.** Confirm the issue meets the emergency definition. If
   it doesn't, route to the normal process.
2. **Communicate.** Notify consumers (emails, channel post,
   CHANGELOG `[Unreleased]` entry) before the hotfix ships, not
   after.
3. **Author the fix.** Smallest possible change. Resist the
   temptation to also fix unrelated issues.
4. **Author the test.** The hotfix ships with a regression test
   covering the bug — captured in
   `scripts/tests/integration/regressions/<bug-id>.yaml` (when
   integration testing exists).
5. **Bypass + ship.** Commit with `[breaking-change-acknowledged]`
   if needed; tag a PATCH; push; release.
6. **Postmortem.** Within 1 week, file a `CHANGELOG.md`
   "Rollback Postmortems" entry covering: what happened, why the
   normal process would have been too slow, what gates failed to
   catch this, what gate is being added.

## Lock-step rule does not apply

The emergency hotfix bypasses lock-step (`GOVERNANCE.md` §"Lock-Step
Upgrades"). Dependents are NOT updated in the same release. Instead:

- The hotfix release ships with explicit "this is a unilateral fix"
  language in the CHANGELOG.
- A follow-up coordinated release within 2 weeks updates dependents
  to the post-hotfix state.

If the hotfix introduces a new breaking change (rare — the goal is
to remove the harm, not change shape), the follow-up coordinated
release handles the lock-step propagation properly.

## Cross-references

- `governance/BREAKING-CHANGE-DETECTION.md` §"Bypass for
  Emergencies" — defines the bypass mechanism.
- `governance/ROLLBACK-PROCEDURE.md` — when the hotfix ITSELF is
  the cause of harm and needs rollback.
- `governance/SECURITY-AUDIT.md` — security-incident hotfixes
  intersect with audit / forensics.
- `MAINTENANCE.md` — implicit-ownership identifies the responsible
  contact.

## Out of scope

- Routine bug fixes (use the normal release process).
- Security disclosures to external parties (handled by the
  consumer library's own communication channels, not this
  document).
- "Emergency" releases that aren't actually emergencies (the
  normal process is fast enough for most "I want to ship this
  now" cases).
