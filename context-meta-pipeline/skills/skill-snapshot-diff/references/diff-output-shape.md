# diff-output-shape.md

> Note: this reference is speculative (authored v0.7.0 ahead of skill-trigger).
> Revise when the skill becomes load-bearing in a consuming library.

The shape of the markdown that `scripts/snapshot-diff.py` (the script) and
`skill-snapshot-diff` (the procedural skill) produce. Used for release
notes, governance reviews, and downstream consumption by changelog
authors.

## Sections

Every diff output has these sections (some may be empty if no items):

| Section | Contents |
|---|---|
| `## Added` | Skills present in the new snapshot but absent in the old. New depends_on entries. |
| `## Removed` | Skills that disappeared from canonical (moved to `retired:` or actually deleted, though the latter is a discipline violation). |
| `## Bumped` | Skills whose version changed. Subdivided by SemVer kind: PATCH / MINOR / MAJOR. |
| `## Health` | Skills whose `health:` enum value changed (fresh → healthy → flagged → unhealthy → rolled-back → retired). v0.6.2 onward. |
| `## Dependency changes` | depends_on edges added or removed at the per-skill level. |
| `## Provenance` | sha256 changes — tracks SKILL.md content drift between snapshots. v0.7.0 onward. |

## Per-section row format

Each section uses a markdown table:

```markdown
## Bumped
| Skill | From | To | Kind |
|---|---|---|---|
| `skill-author` | 0.1.5 | 0.1.6 | PATCH |
```

Tables stay sortable by tooling. JSON output (via `--format json`) emits
the same data in a per-section list.

## Output destinations

- **Release notes**: paste sections directly into `CHANGELOG.md` under the
  release block. Bumped + Added are most useful for users.
- **Governance reviews**: Health + Removed are most useful for governance
  (catches retired skills + flagged skills).
- **Migration triggers**: Bumped MAJOR rows trigger `skill-migrate`
  invocations (one per skill).

## What the diff does NOT include

- The *content* of the SKILL.md changes — only the version + health +
  pin bumps. For content drift, use `git diff <old-tag> <new-tag> --
  skills/`.
- Per-skill changelog entries — those are in the SKILL.md `metadata.changelog`
  block; `changelog-sync.py` cross-references them against CHANGELOG.md.
- Hash-only changes when version is unchanged. v0.7.0's snapshot-hash
  catches this differently: `--verify` mode flags content-without-version
  drift as an error (the version should bump if the content changed).

## Author conventions

- The Provenance section is purely informational at v0.7.0. When external
  publishing begins (per `governance/SKILL-PROVENANCE.md` build trigger),
  Provenance becomes load-bearing for marketplace integrity.
- The Health section was added v0.6.2 alongside `audit-skill.py
  --write-health`. Pre-v0.6.2 snapshots had perpetually `fresh` skills;
  diff against an older snapshot won't show Health rows.
