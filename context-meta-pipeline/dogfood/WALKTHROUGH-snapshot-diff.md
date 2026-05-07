# Walkthrough: skill-snapshot-diff

Phase 2 dogfood walkthrough #3.

## Procedure walked

3 stages end-to-end:

- **Stage 1 (identify diff target)** → `diff-target.yaml`:
  - old: `scripts/tests/fixtures/snapshot/snapshot-a.lock` (synthetic v0.1.0)
  - new: `SNAPSHOT.lock` (current v0.5.1)
- **Stage 2 (run runner)** → `snapshot-diff.py` exited 0 with structured output
- **Stage 3 (compose release notes)** → operator-side polish; skill provides
  the structural skeleton

## Result

Output captured 12 Added / 1 Removed / 2 Version-bumped — exactly what
v0.1.0 → v0.5.1 should yield. Categories well-formed. Markdown valid.

## Findings

None. The skill works end-to-end as designed.

## Bug status

No structural bugs. No content fixes required.

## Walkthrough verdict

PASS clean.
