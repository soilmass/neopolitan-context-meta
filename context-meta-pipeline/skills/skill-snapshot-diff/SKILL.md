---
name: skill-snapshot-diff
description: >
  Diffs two SNAPSHOT.lock states and produces release-note markdown
  categorized into Added / Removed / Bumped / Health / Dependency
  changes. Wraps scripts/snapshot-diff.py with the release-note draft
  composition step. Do NOT use for: authoring new skills (use
  skill-author); validating metadata (use validate-metadata.py via
  skill-author Stage 4); rolling back a release (use rollback-skill.py
  / skill-retire); auditing skill health (use skill-audit / library-audit).
license: Apache-2.0
metadata:
  version: "0.1.1"
  archetype: tool
  tags: [health, weekly]
  changelog: |
    v0.1.1 — patch: metadata.tags declared per the v0.7.0 canonical taxonomy plus `references/diff-output-shape.md` (speculative; pre-trigger disclaimer at top of each).
    v0.1.0 — initial. Authored as part of v0.5.0 kitchen-sink meta-tooling release.
---

# skill-snapshot-diff

A thin tool over `scripts/snapshot-diff.py`. Produces release-note
markdown categorizing every change between two `SNAPSHOT.lock` states:
which skills were added, which were removed (no longer canonical), which
versions bumped, which health states transitioned, which `depends_on`
edges changed.

## Purpose

CHANGELOG entries from v0.2.0 onward could have been auto-drafted from
a snapshot diff. This tool closes that loop: given two snapshot
states (typically the previous tag's snapshot and HEAD's snapshot),
emit a structured release-note draft. The author edits for tone +
context; the structural skeleton is produced mechanically.

## When to Use

- Before tagging a release: produce the CHANGELOG entry from the
  snapshot diff against the previous tag.
- During a dogfood or audit: explain what changed between two known-good
  snapshots.
- During investigation: "what shipped between v0.4.1 and HEAD that
  could have caused this regression?"

## When NOT to Use

- For authoring new skills — use `skill-author`.
- For validating a SKILL.md's structural compliance — `validate-metadata.py`
  is the underlying check; use `skill-author` Stage 4 for the procedure.
- For deciding *whether* to roll back — use `skill-audit` to identify
  failures; `rollback-skill.py` / `skill-retire` for the action.
- For library-shape health (coverage.md alignment, snapshot integrity)
  — use `library-audit`.
- For a per-skill diff between two SKILL.md versions — use
  `migration-guide-gen.py` (called by `skill-migrate`).

## Stage-Gated Procedure

Three lightweight stages.

### Stage 1 — Identify the diff target

**Consumes:** the operator's release intent and `git tag --list`.

**Produces:** `diff-target.yaml` containing
- `old_snapshot_path` (path to the previous SNAPSHOT.lock — either a
  worktree file or a git ref like `v0.4.1:SNAPSHOT.lock`)
- `new_snapshot_path` (typically `SNAPSHOT.lock` in the current worktree)
- `release_target_version` (what the new snapshot's `snapshot_version`
  should be after this release lands)

**Gate:** both paths resolve; the new snapshot's `snapshot_version` is
distinct from the old (otherwise there's nothing to release).

### Stage 2 — Run the diff script

**Consumes:** `diff-target.yaml`.

**Produces:** the output of `scripts/snapshot-diff.py --old <old> --new <new>`
in markdown format, captured to a working file.

**Gate:** the script exits 0; the output has at least one
non-empty section (otherwise the snapshots are equivalent and no
release is needed).

### Stage 3 — Compose release notes

**Consumes:** the Stage 2 markdown output.

**Produces:** the release-note draft, suitable for:
- `CHANGELOG.md` under `[<new-version>]` heading
- A GitHub Release body
- The `release-tag.sh` script's `--output` flag

The author adds:
- Theme / one-line summary at the top
- Rationale for breaking changes (if any)
- Known issues / migration notes (referenced from `MIGRATION-v<N>.md`
  files)
- Verification artifacts (`make verify` exit 0; specific drift /
  health numbers)

**Gate:** the draft mentions every "Removed" entry from Stage 2's
output (silent removals are forbidden per `GOVERNANCE.md`); every
"Bumped" entry's category (PATCH / MINOR / MAJOR) is named correctly
per `VERSIONING-POLICY.md`.

## Dependencies

- `scripts/snapshot-diff.py` — the diff engine.
- `SNAPSHOT.lock` — the input format (canonical per `GOVERNANCE.md`).
- `CHANGELOG.md` — the consumer of the output.

## Evaluation

`skill-snapshot-diff` is correct when, run between two known snapshots
that differ on one skill's version, the output names the version
transition correctly, categorizes the bump (PATCH / MINOR / MAJOR),
and identifies the change as Added / Removed / Bumped / Health /
Dependency in the right bucket.

The first dogfood is the v0.5.0 release itself: this tool's output
forms the basis of the v0.5.0 CHANGELOG entry.

## Handoffs

- **From `skill-author` / `skill-refactor` / `skill-retire`** — every
  Stage 4 / 5 update to `SNAPSHOT.lock` is a candidate for a future
  diff against the next release.
- **To `skill-migrate`** — when the diff identifies a MAJOR bump, the
  migration guide is authored via `skill-migrate` (which uses
  `migration-guide-gen.py` for the per-skill diff).
- **To `release-tag.sh`** — the script consumes this tool's output as
  the release-note body when tagging.
