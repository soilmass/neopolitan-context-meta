# Integration Testing

**Build trigger:** library has 10+ skills with cross-dependencies and a
single-skill regression has broken downstream skills more than twice.

**Pre-trigger applicability:** *None.* Until the trigger fires, this
document specifies the procedure for when integration testing becomes
load-bearing — but none of its rules bind a smaller library. Health
Gate 2 (test pass rate, threshold >90%) reports explicit `N/A` for
every skill in the meantime, per `MAINTENANCE.md` and
`skills/skill-audit/references/health-gates.md`.

This document is authored at v0.5.0 to claim the surface area; the
machinery it specifies ships when the trigger fires.

---

## What integration testing covers

Per `MAINTENANCE.md` §Gate 2, integration testing is the pass-rate
gate. It catches regressions that *unit tests on a single skill miss*:

- A change to skill A breaks downstream skill B (which depends on A
  via `SNAPSHOT.lock` `depends_on:` or via prose handoff).
- A change to a router's `## Routing Table` mis-routes prompts that
  used to reach the right atom.
- A description rewrite shifts the trigger surface enough that
  prompts hit the wrong skill (overlaps with `skill-evaluate`'s
  Gate 3 territory; integration tests catch behavioral
  consequences, eval catches routing errors).

Unit tests on individual skills are out of scope here — those live
in each skill's own evaluation suite per `ARCHITECTURE.md`.

## Test format

A cross-skill integration test is a YAML scenario:

```yaml
- name: family-bootstrap delegates to skill-author per atom
  scenario:
    - invoke: family-bootstrap
      with:
        domain: <fixture-domain>
        authority: <fixture-authority>
    - assert:
        - skill-author is invoked at least 6 times (once per Tier 1 atom)
        - SNAPSHOT.lock has 6+ new entries after the run
        - coverage.md has all six required sections
        - validate-metadata.py --all exits 0
```

Tests live at `scripts/tests/integration/<scenario>.yaml`.

## When tests run

- **Pre-merge** on every PR that modifies a skill referenced in any
  scenario.
- **Nightly** full-suite run, results captured in
  `scripts/tests/integration/results/<date>.json`.
- **Pre-release** as part of `verify.sh` step 7 (added when the
  trigger fires).

## Threshold + failure mode

Per `MAINTENANCE.md` Gate 2: pass rate above 90% per skill. A skill
whose integration tests fall below 90% is flagged via the standard
health-gate banner mechanism.

When a regression is detected:
- The regression's commit is identified via bisect (see
  `skills/git-inspection/` once the git family lands in a consumer
  library — bisect across the meta-pipeline's own commits otherwise).
- The triggering change is reverted via `rollback-skill.py` if the
  regression is recent and isolated.
- A test is added covering the now-known regression so the suite
  catches it next time.

## Implementation

When the trigger fires, the implementation is a Python runner under
`scripts/integration-test-runner.py` that:

1. Loads every YAML scenario.
2. For each scenario, runs the skills under controlled-input
   conditions (a fixture domain, fixture authority, fixture
   `SNAPSHOT.lock`).
3. Captures actual outputs and asserts against expected.
4. Reports per-scenario pass/fail and per-skill pass-rate rollup.

The runner is deferred. v0.5.0 ships only this specification.

## Scope of cross-references

This document is referenced from:
- `MAINTENANCE.md` §Gate 2 (test pass rate)
- `skills/skill-audit/references/health-gates.md` Gate 2
- `skills/library-audit/SKILL.md` (the library-level rollup of
  Gate 2 + Gate 3)
- `coverage.md` Domains Deferred (gates the trigger)

When the document is moved from Deferred to Currently Documented in
`governance/INDEX.md` (v0.5.0), the references above continue to
resolve; the only change is the deferred-to-current transition.

## Out of scope

- Single-skill unit tests (per-skill `## Evaluation` section in each
  SKILL.md).
- Routing accuracy (separate gate; see `skill-evaluate` and
  `routing-eval-protocol.md`).
- Performance / latency testing (out of scope until a real
  performance regression occurs in a consuming library).
- Manual exploratory testing (operator-driven; not codified here).
