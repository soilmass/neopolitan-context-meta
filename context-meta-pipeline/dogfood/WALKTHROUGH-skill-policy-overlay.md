# Walkthrough: skill-policy-overlay

Phase 2 dogfood walkthrough #6.

## Procedure walked

4 stages, against synthetic input: house-postgres-conventions
overlaying a hypothetical postgres-history-rewriting atom (which
doesn't exist in any actual library).

- **Stage 1 (policy intake)** → policy-intake.yaml with name, 3
  conventions, fail-loud override behavior
- **Stage 2 (delegate to skill-author with archetype=policy)** →
  produced SKILL.md
- **Stage 3 (wire dependency in SNAPSHOT.lock)** → would update
  consuming library's snapshot; not applicable here
- **Stage 4 (override semantics check)** → grep for fail-loud
  commitment passed

## Result

The produced policy SKILL.md validates clean (validate-metadata.py
exit 0, all 4 archetype-required sections present and substantive).

## Findings

### A30 — Stage 1's gate is only fully testable against a real consuming library

"postgres-history-rewriting in consuming library's SNAPSHOT.lock"
is the gate condition. With no real consuming library that has a
postgres family, the gate is operator-confirmed. Same situation as
the `family-bootstrap` Stage 1 URL-reachable check (audit finding
A1 from v0.4.0).

**Remedy** (no v0.5.2 action; documented as a known limitation):
this gate is fully testable only against a real consumer. Until then,
the operator confirms manually. Same discipline as A1 — the runner
doesn't auto-fetch.

## Bug status

No structural bugs. Skill works against synthetic input.

## Walkthrough verdict

PASS — speculative skill produces a valid policy overlay end-to-end.
The "fail loudly" commitment is structurally reachable. Real
testability awaits a consuming library with a postgres family.
