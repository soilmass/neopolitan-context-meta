# Security Audit

**Build trigger:** library starts containing skills that touch
sensitive operations (credentials, production data, user-facing
surfaces) and provenance becomes a compliance requirement.

**Pre-trigger applicability:** *None.* The meta-pipeline at v0.5.0
contains no skills touching credentials or production systems —
every skill is a meta-tool over other skills. Security audit
becomes load-bearing only when consumer libraries author skills
in sensitive domains.

---

## What a security audit covers

Three concerns:

1. **Provenance** — was every skill authored by who I think it was?
   See `governance/SKILL-PROVENANCE.md`.
2. **Audit logs** — who changed what when? Who shipped each
   release?
3. **Forensics** — when something goes wrong (a malicious skill,
   a compromised release), can we reconstruct the chain of events?

Provenance is the prerequisite. This document covers logs +
forensics.

## Audit logs

### What gets logged

- Every git commit on the meta-pipeline + every consumer library
  (the standard git history is the audit log).
- Every release tag's signed metadata (per `SKILL-PROVENANCE.md`).
- Every `SNAPSHOT.lock` change — bumped versions, retired skills,
  health transitions.
- Every `CHANGELOG.md` entry — describes what shipped and why.
- Every `coverage.md` deferred-row transition — when a deferred
  doc was authored / a deferred skill was built / an out-of-scope
  decision changed.

The git log + the four versioned ledgers (`SNAPSHOT.lock`,
`CHANGELOG.md`, `coverage.md`, `governance/INDEX.md`) form the
audit log. No additional infrastructure required.

### What's not logged

- Operator commands during a skill invocation (Claude Code-side
  concern; not this layer's responsibility).
- LLM responses (operator-side; out of scope).
- Per-skill execution timings (performance concern, not security).

## Forensics

When a security incident is identified:

1. **Identify the affected commit range** — first known-bad +
   first known-good.
2. **Verify ledger integrity** — every release tag in the range is
   GPG-signed (per `SKILL-PROVENANCE.md`); every `SNAPSHOT.lock`
   `sha256:` matches the actual SKILL.md bytes.
3. **Identify changed skills** — `scripts/snapshot-diff.py` between
   the known-good and known-bad snapshots gives the change set.
4. **Identify the responsible commits** — `git log --follow` per
   affected skill; the implicit-ownership model
   (`MAINTENANCE.md`) means whoever last touched a skill is the
   accountable contact.
5. **Roll back** if appropriate — `rollback-skill.py` for Level 1;
   procedural for Level 2-3 per `governance/ROLLBACK-PROCEDURE.md`.
6. **Postmortem** — `CHANGELOG.md` "Rollback Postmortems" section
   per `ROLLBACK-PROCEDURE.md`.

## Pre-incident hardening

Before the trigger fires (which is when security audit becomes
load-bearing), these are nice-to-haves that can land
incrementally:

- Branch protection on the meta-pipeline's main branch (require
  PRs, require CI green, restrict push).
- CODEOWNERS file (currently rejected per
  `governance/INDEX.md` §"Multi-team ownership" — reverse the
  decision when a real second team appears).
- Required signed commits (`git config commit.gpgsign true` per
  contributor).
- Two-person review for breaking changes.

None bind until the security-audit trigger fires.

## Implementation

When the trigger fires, this document is paired with:

1. `governance/SKILL-PROVENANCE.md` (already authored — provenance
   is prerequisite).
2. A `scripts/audit-log-summary.py` that consolidates the four
   ledgers into a single timeline view.
3. CI configuration enforcing signed commits + signed tags.
4. A `governance/INCIDENT-RESPONSE.md` (would be authored at the
   same time, alongside `EMERGENCY-HOTFIX.md`) covering
   non-security incidents.

## Cross-references

- `governance/SKILL-PROVENANCE.md` — provenance, prerequisite.
- `governance/EMERGENCY-HOTFIX.md` — pairs with this for incidents
  requiring lock-step bypass.
- `GOVERNANCE.md` §"Implicit Ownership" — currently load-bearing for
  forensic accountability.
- `MAINTENANCE.md` — when a security failure intersects with health
  failure (rare).

## Out of scope

- Threat modeling of specific skill domains (each domain's own
  policy overlay handles that — `house-<domain>-conventions`).
- Penetration testing (out of scope; not a meta-pipeline concern).
- Compliance certification (separate process layered on top).
