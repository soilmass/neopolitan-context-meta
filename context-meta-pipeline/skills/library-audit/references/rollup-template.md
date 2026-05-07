# library-audit-report.md template

Stage 5 of `library-audit` produces this report. Convention is
operator-driven; the template keeps reports comparable across runs.

## Format

```markdown
# Library audit — <library-name> @ <YYYY-MM-DD>

**Headline:** <one-line summary, e.g., "PASS clean" / "FLAGGED — 3 issues">

## Per-stage rollup

| Gate | Status | Detail |
|---|---|---|
| L1 — Per-skill health | <PASS / FLAGGED N skills> | <flagged skill names if any> |
| L2 — coverage.md schema | <PASS / FAIL> | <error-list if FAIL> |
| L3 — Snapshot integrity | <PASS / FAIL> | <unresolved deps / cycles / missing files> |
| L4 — Version triangulation | <PASS / FAIL> | <which file disagrees> |

## Recommended remedies

For each flagged item:

- `<skill-or-file>` — <what's wrong> — **handoff to:** `<skill-name>`

The handoff column names which lifecycle skill should fix the issue:
- description drift → `skill-author` (PATCH bump on description rewrite)
- archetype mixing → `skill-refactor`
- abandoned skill (≥12 months unhealthy) → `skill-retire`
- snapshot drift → manual edit + `library-audit` re-run

## CHANGELOG suggestion

```markdown
### Health
- <skill-or-file> flagged: <gate>; remedy via <skill>
- ...
```

## Run metadata

- audit-skill.py exit: <0 / 1>
- coverage-check.py exit: <0 / 1>
- snapshot integrity: <PASS / FAIL>
- run timestamp: <YYYY-MM-DD HH:MM>
```

## Convention

- Headline is a single line; never includes counts in prose
  (the table has counts).
- Per-stage rollup uses ✓/✗ marks consistent with other library
  rollups (audit-skill banner, verify.sh OK/FAIL).
- Recommended remedies always name a target skill (not a script);
  if the remedy is a manual edit, name "manual edit + re-run
  library-audit" explicitly.

## Storage

Reports are typically *ephemeral* (operator runs library-audit,
reads the report, takes action). If a consuming library wants to
persist reports for audit-trail purposes, the convention is
`scripts/audit-reports/<YYYY-MM-DD>.md`. The library-audit skill
does not auto-write to this location; the operator does.
