# Breaking Change Detection

A breaking change is any modification to a skill that requires downstream skills (or their lockfiles) to be updated. Without automated detection, breaking changes slip in as MINOR or PATCH bumps, breaking the SemVer contract.

This document specifies what counts as breaking, how the CI check works, and what happens when it fires.

---

## What Counts as Breaking

Breaking changes fall into four categories. Each is detectable from a diff of the SKILL.md file plus any referenced files.

### 1. Frontmatter changes

A change is breaking if any of these fields change:

- **`name`** — renames are always breaking. Downstream skills referencing the old name fail to resolve.
- **`description`** — material rewrites are breaking. Adding clarification is not. The detector flags any change >30% by character count for human review.
- **`allowed-tools`** — removing a tool is breaking. Adding a tool is not.
- **`model`** — changing the required model is breaking when downstream skills assume specific model behavior.

### 2. Section removal

Removing **any** section listed in the archetype's required-sections checklist is breaking. The full per-archetype list is the single source of truth in `METADATA-VALIDATION.md` §"Archetype-Specific Required Sections" — both `validate-metadata.py` and `detect-breaking-changes.py` consume that list directly. Examples below are illustrative, not exhaustive:

- **Atoms** — removal of any of the six required sections (e.g., `Capabilities Owned`, `Handoffs to Other Skills`) is breaking. The full list is in `METADATA-VALIDATION.md`.
- **Routers** — removal of any of the five required sections (e.g., `Routing Table`, `Disambiguation Protocol`) is breaking. Anti-triggers themselves live in the frontmatter `description`, not in a body section; description-level anti-trigger removal is caught by the `description` rewrite-percentage check above.
- **Tools** — removal of any of the seven required sections (e.g., `Stage-Gated Procedure`, `Evaluation`) is breaking.
- **Orchestrators** — removal of any of the seven required sections (e.g., `The Stages`, `Skills Coordinated`, `Failure Modes`) is breaking.
- **Policy overlays** — removal of any of the four required sections (e.g., `Conventions Enforced`, `Override Behavior`) is breaking.

When in doubt, defer to the table in `METADATA-VALIDATION.md`. The detector enforces all of them, not just the ones named here.

### 3. Capability changes

For atoms specifically:

- Removing a capability from the `Capabilities Owned` list is breaking.
- Moving a capability to a different atom is breaking (downstream routers may dispatch to the wrong skill).
- Changing the contract of a capability (input format, output format, side effects) is breaking.

The detector compares the `Capabilities Owned` list across versions and flags any removal or move.

### 4. Routing changes

For routers specifically:

- Removing entries from the `Routing Table` is breaking.
- Changing the target atom of an existing entry is breaking.
- Adding new anti-triggers that exclude previously-routed prompts is breaking.

---

## What Is NOT Breaking

The detector explicitly does not flag these as breaking:

- Adding new sections (Edge Cases, Examples, References).
- Adding new capabilities to an atom.
- Adding new entries to a router's Routing Table.
- Clarifying or expanding existing prose without changing meaning.
- Adding optional frontmatter fields.
- Changing internal implementation in scripts or references that the public surface doesn't expose.

When in doubt, the detector flags for human review rather than silently passing.

---

## The CI Check

The detector runs on every pull request that modifies a SKILL.md file. The flow:

1. Compare the modified SKILL.md against the version on the main branch.
2. Run the four detection passes (frontmatter, section removal, capability changes, routing changes).
3. If any breaking change is detected, check the version bump in frontmatter.
4. If the version bump is not MAJOR, fail the check.
5. If the version bump is MAJOR, require:
   - A migration guide entry generated from the diff (see `VERSIONING-POLICY.md`).
   - An entry in the library `CHANGELOG.md`.
   - Updates to any router that dispatches to this skill.
   - Confirmation that all downstream skills in the library snapshot have been updated to use the new version (lock-step requirement).

If any of these are missing, the check fails with a specific message naming what's missing.

---

## The Detector Output

When the detector finds a breaking change, it produces a structured report:

```
BREAKING CHANGE DETECTED in skill: git-history-rewriting

Category: Capability removal
Detail: `revert` removed from Capabilities Owned
Impact: 1 router (`git`) currently dispatches "revert this commit" to this skill

Required actions before merge:
[ ] Bump version to 2.0.0 (currently 1.4.2)
[ ] Add migration guide entry
[ ] Update `git` router routing table (current entry: "fix a bad commit" → git-history-rewriting)
[ ] Add entry to library CHANGELOG.md
[ ] Update library snapshot
[ ] Coordinate lock-step release with `git` router update
```

This output is posted as a PR comment and blocks merge until resolved.

---

## Bypass for Emergencies

The detector can be bypassed only with an explicit `[breaking-change-acknowledged]` tag in the commit message AND a sign-off from the library maintainer. This is reserved for security hotfixes where the breaking change is intentional and can't wait for a coordinated release. See `EMERGENCY-HOTFIX.md` (when authored) for the full procedure.

---

## What This Doesn't Catch

The detector is rule-based, not semantic. It catches structural breaking changes but not behavioral ones:

- A skill that still has all its sections but produces meaningfully different output is not flagged.
- A skill that adds a new mandatory step in its procedure is not flagged.
- A skill that changes its routing tiebreaker logic is not flagged.

These require human review at PR time. The detector is a floor, not a ceiling — it catches the obvious failures, not the subtle ones.

---

## Implementation Notes

Implemented in v0.1.0 as `scripts/detect-breaking-changes.py` (Python 3, PyYAML + stdlib + subprocess for `git show`). It needs:

- Read access to the modified SKILL.md (`--skill <path>`)
- Read access to a baseline version (`--baseline <path>` for a static file, or `--baseline-ref <git-ref>` to fetch via `git show`)
- Read access to the library snapshot at `SNAPSHOT.lock` to identify dependents (`--snapshot <path>`)
- Output to stdout in the structured format above (text or JSON via `--format`)
- Exit codes: 0 if no breaking change, 1 if breaking change detected without proper handling (blocks merge), 2 if breaking change detected with proper handling (informational only).

CI platforms invoke this script directly; the script does not reimplement CI-platform integration.
