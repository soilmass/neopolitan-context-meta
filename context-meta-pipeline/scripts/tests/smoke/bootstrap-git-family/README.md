# Smoke fixture: bootstrap-git-family

Persistent fixture from the v0.4.0 dogfood that walked
`family-bootstrap`'s 6 stages on the canonical `git` domain. The
fixture captures the input artifacts and the expected output shape
so future runs of `family-bootstrap` can be regression-tested
against this known-good case.

## Files

- `input.yaml` — the operator inputs that drove the dogfood:
  domain, authority, scope, expected_size, adjacent_families,
  existing_overlap. Equivalent to `domain-intake.yaml` per
  `family-bootstrap` Stage 1.
- `expected/` — the expected artifacts:
  - `taxonomy.md` — Tier 1/2/3 taxonomy that should result
  - `coverage.md` — family coverage.md with all six sections
  - `skills/` — list of 8 expected SKILL.md atoms + 1 router
    (filenames + their archetypes; full contents are not snapshotted
    because the dogfood was in-memory and not persisted)

## Why fixed input, fixed expected

Per the v0.5.0 plan §Risks, the smoke fixture must NOT regenerate
from upstream Pro Git documentation. If the canonical git docs
change, the fixture stays stable; the test catches regressions in
*the family-bootstrap procedure*, not regressions in upstream docs.

## How to run

There is no automated runner at v0.5.0. The smoke test is
operator-driven: walk the family-bootstrap procedure against this
input, compare the result to `expected/`, fail-loud on divergence
beyond the documented allow-list (e.g., descriptions tightened
for the drift gate are expected to differ).

A future `scripts/smoke-runner.py` (deferred until family-bootstrap
gets script-driven mode — currently rejected per coverage.md
out-of-scope) would automate the comparison.

## Cross-references

- `skills/family-bootstrap/SKILL.md` — the procedure under test
- `CHANGELOG.md` v0.4.0 — the dogfood that produced this fixture
  and the 21 audit findings (A1–A21)
- `coverage.md` — captures the dogfood-driven changes that landed
  in v0.4.0 and v0.4.1
